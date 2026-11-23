# Diagnostic-only replay. Requires local tick archive, trade ledger, and signal-event CSV.
# Set TENGRI_HEDGE_REPLAY_ROOT to the existing Statement_Floating_Audit data directory.
import csv
import datetime as dt
import json
import os
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(os.environ.get("TENGRI_HEDGE_REPLAY_ROOT", str(Path(__file__).resolve().parent)))
REPLAY = ROOT / "replay.py"
base_code = REPLAY.read_text().split("# Check broker-clock alignment")[0]
ns = {"__file__": str(REPLAY)}
exec(compile(base_code, str(REPLAY), "exec"), ns)
orders = ns["orders"]
symbols = tuple(ns["symbols"])
snapshots = ns["snapshots"]
stamp = ns["stamp"]
quotes = ns["quotes"]
marks = ns["marks"]

FIRST = dt.date(2026, 5, 1)
LAST = dt.date(2026, 11, 18)
START_MS = stamp("2026.05.01 00:00:00")
END_MS = stamp("2026.11.19 00:00:00")
OPENING_BALANCE_USC = 4000.0
MIN_LOT = 0.01
LOT_STEP = 0.01
MIN_LAYERS = 6
HEDGE_RATIO = 0.25
SPREAD_CAP_PIPS = 3.0
BASE_EXTRA_PIPS_PER_ACTION = 1.0
STRESS_EXTRA_PIPS_PER_ACTION = 2.0
MAX_MARK_AGE_MS = 300_000

event_file = ROOT.parent / "BBMA516_SourceAudit" / "BBMA516_signal_events.csv"
events_by_symbol = defaultdict(list)
event_counts = defaultdict(lambda: defaultdict(int))
gate_blocked_counts = defaultdict(lambda: defaultdict(int))
with event_file.open(newline="", encoding="utf-8-sig") as fh:
    for row in csv.DictReader(fh):
        approved = row.get("d1_h4_m15_approved", "").strip().lower() == "true"
        event_dt = dt.datetime.strptime(row["first_m15"], "%Y.%m.%d %H:%M").replace(tzinfo=dt.UTC)
        event_ms = int(event_dt.timestamp() * 1000)
        if not (START_MS <= event_ms < END_MS):
            continue
        kind = int(row["type"].split("_")[2])
        direction = 1 if row["direction"] == "DIR_BUY" else -1
        ev = {"time": event_ms, "kind": kind, "direction": direction,
              "type": row["type"], "hash": row["hash"], "approved": approved}
        events_by_symbol[row["symbol"]].append(ev)
        if approved:
            event_counts[row["symbol"]][kind] += 1
        else:
            gate_blocked_counts[row["symbol"]][kind] += 1
for pair in events_by_symbol:
    events_by_symbol[pair].sort(key=lambda e: (e["time"], e["kind"], e["direction"]))

core_events = {s: defaultdict(list) for s in symbols}
initial_active = {s: {} for s in symbols}
core_cash_events = []
for order in orders:
    ticket, pair, side, lot, opened, open_price, closed = order[:7]
    if pair not in symbols:
        continue
    open_ms = stamp(opened)
    close_ms = stamp(closed) if closed else None
    if open_ms < START_MS and (close_ms is None or close_ms >= START_MS):
        initial_active[pair][ticket] = order
    if START_MS <= open_ms < END_MS:
        core_events[pair][open_ms].append(("open", order))
    if close_ms is not None and START_MS <= close_ms < END_MS:
        core_events[pair][close_ms].append(("close", order))
        core_cash_events.append((close_ms, float(order[10]) + float(order[8]) + float(order[9])))

flows = []
for time_text, amount in json.loads((ROOT / "cash_flows.json").read_text()):
    t = stamp(time_text)
    if START_MS <= t < END_MS:
        flows.append((t, float(amount)))
flows.sort(key=lambda x: x[0])
cash_events = sorted(core_cash_events + flows, key=lambda x: x[0])
cash_times = np.array([x[0] for x in cash_events], dtype=np.int64)
cash_delta = np.array([x[1] for x in cash_events], dtype=float)
cash_cum = np.r_[0.0, np.cumsum(cash_delta)]


def down_lots(value):
    return max(0.0, round(math.floor((value + 1e-10) / LOT_STEP) * LOT_STEP, 2))


def pip_value_usc(symbol, bid):
    # HFM Cent: one Cent lot is 1,000 base units and the account is USC.
    return 10.0 if symbol == "EURUSD" else 10.0 / bid


def price_multiplier(symbol, bid):
    return 100000.0 if symbol == "EURUSD" else 100000.0 / bid


def core_snapshot(active):
    buys = [o for o in active.values() if int(o[2]) == 1]
    sells = [o for o in active.values() if int(o[2]) == -1]
    buy_lots = sum(float(o[3]) for o in buys)
    sell_lots = sum(float(o[3]) for o in sells)
    net = buy_lots - sell_lots
    if net > 1e-8:
        direction, layers = 1, len(buys)
    elif net < -1e-8:
        direction, layers = -1, len(sells)
    else:
        direction, layers = 0, 0
    return {"buy_lots": buy_lots, "sell_lots": sell_lots, "net": net,
            "direction": direction, "layers": layers,
            "buy_count": len(buys), "sell_count": len(sells)}


def core_row(active):
    buys = [o for o in active.values() if int(o[2]) == 1]
    sells = [o for o in active.values() if int(o[2]) == -1]
    return [sum(float(o[3]) for o in buys),
            sum(float(o[3]) * float(o[5]) for o in buys), len(buys),
            sum(float(o[3]) for o in sells),
            sum(float(o[3]) * float(o[5]) for o in sells), len(sells)]


class HedgeState:
    def __init__(self, name):
        self.name = name
        self.positions = []
        self.campaign = None
        self.closed_campaigns = []
        self.realized_base = 0.0
        self.realized_stress = 0.0
        self.fixed_base = 0.0
        self.fixed_extra = 0.0
        self.spread_cost = 0.0
        self.actions = []
        self.counts = {
            "entry_events_for_type": 0, "eligible_entry_events": 0,
            "entries_or_adds": 0, "close_or_trim_actions": 0,
            "closed_campaigns": 0, "open_at_end_campaigns": 0,
            "ineligible_layers": 0, "ineligible_direction_or_flat": 0,
            "target_below_minimum": 0, "spread_blocked": 0,
            "stale_signal_blocked": 0, "exit_reentry_signals": 0,
        }

    def state_row(self):
        if not self.positions:
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        side = self.positions[0]["side"]
        if any(p["side"] != side for p in self.positions):
            raise RuntimeError("mixed hedge sides")
        lots = sum(p["lots"] for p in self.positions)
        weighted = sum(p["lots"] * p["entry"] for p in self.positions)
        if side > 0:
            return [lots, weighted, len(self.positions), 0.0, 0.0, 0.0]
        return [0.0, 0.0, 0.0, lots, weighted, len(self.positions)]

    def float_pnl(self, symbol, bid, ask):
        if not self.positions:
            return 0.0
        mult = price_multiplier(symbol, bid)
        return sum(((bid if p["side"] > 0 else ask) - p["entry"]) *
                   p["side"] * p["lots"] * mult for p in self.positions)

    def _record(self, time_ms, action, reason, lots, raw=0.0,
                fixed=0.0, extra=0.0, spread=0.0):
        self.realized_base += raw - fixed
        self.realized_stress += raw - fixed - extra
        self.fixed_base += fixed
        self.fixed_extra += extra
        self.spread_cost += spread
        self.actions.append({
            "time": int(time_ms), "action": action, "reason": reason,
            "lots": float(lots), "raw_quote_pnl": float(raw),
            "fixed_cost_base": float(fixed), "fixed_cost_extra": float(extra),
            "spread_cost_estimate": float(spread),
            "net_balance_delta_base": float(raw - fixed),
            "net_balance_delta_stress": float(raw - fixed - extra),
        })
        if self.campaign is not None:
            self.campaign["raw_realized"] += raw
            self.campaign["fixed_base"] += fixed
            self.campaign["fixed_extra"] += extra
            self.campaign["spread_cost"] += spread
            self.campaign["actions"] += 1

    def open(self, symbol, side, lots, bid, ask, time_ms, kind):
        lots = down_lots(lots)
        if lots < MIN_LOT:
            return False
        if self.positions and self.positions[0]["side"] != side:
            raise RuntimeError("attempted opposite-side add before safety close")
        if not self.positions:
            self.campaign = {
                "entry_type": kind, "opened": int(time_ms), "raw_realized": 0.0,
                "fixed_base": 0.0, "fixed_extra": 0.0, "spread_cost": 0.0,
                "actions": 0, "initial_lots": 0.0,
            }
        price = ask if side > 0 else bid
        base = lots * pip_value_usc(symbol, bid) * BASE_EXTRA_PIPS_PER_ACTION
        extra = lots * pip_value_usc(symbol, bid) * (STRESS_EXTRA_PIPS_PER_ACTION - BASE_EXTRA_PIPS_PER_ACTION)
        spread = lots * price_multiplier(symbol, bid) * (ask - bid) * 0.5
        self.positions.append({"side": side, "lots": lots, "entry": price})
        self._record(time_ms, "open/add", "BBMA type " + str(kind), lots,
                     raw=0.0, fixed=base, extra=extra, spread=spread)
        self.counts["entries_or_adds"] += 1
        if self.campaign is not None:
            self.campaign["initial_lots"] += lots
        return True

    def close(self, symbol, lots, bid, ask, time_ms, reason):
        if not self.positions:
            return 0.0
        total = sum(p["lots"] for p in self.positions)
        lots = min(total, down_lots(lots))
        if lots < MIN_LOT:
            return 0.0
        side = self.positions[0]["side"]
        close_price = bid if side > 0 else ask
        mult = price_multiplier(symbol, bid)
        remain = lots
        raw = 0.0
        while remain >= MIN_LOT - 1e-9 and self.positions:
            p = self.positions[-1]  # latest ticket first, matching the EA close order
            amount = min(remain, p["lots"])
            raw += (close_price - p["entry"]) * side * amount * mult
            p["lots"] = round(p["lots"] - amount, 8)
            remain = round(remain - amount, 8)
            if p["lots"] < MIN_LOT - 1e-9:
                self.positions.pop()
        base = lots * pip_value_usc(symbol, bid) * BASE_EXTRA_PIPS_PER_ACTION
        extra = lots * pip_value_usc(symbol, bid) * (STRESS_EXTRA_PIPS_PER_ACTION - BASE_EXTRA_PIPS_PER_ACTION)
        spread = lots * mult * (ask - bid) * 0.5
        self._record(time_ms, "trim/close", reason, lots,
                     raw=raw, fixed=base, extra=extra, spread=spread)
        self.counts["close_or_trim_actions"] += 1
        if not self.positions and self.campaign is not None:
            camp = self.campaign
            base_net = camp["raw_realized"] - camp["fixed_base"]
            stress_net = base_net - camp["fixed_extra"]
            self.closed_campaigns.append({
                "entry_type": camp["entry_type"], "opened": camp["opened"],
                "closed": int(time_ms), "net_base": base_net,
                "net_stress": stress_net, "raw_quote_pnl": camp["raw_realized"],
                "fixed_cost_base": camp["fixed_base"],
                "fixed_cost_extra": camp["fixed_extra"],
                "spread_cost_estimate": camp["spread_cost"],
                "actions": camp["actions"], "initial_lots": camp["initial_lots"],
            })
            self.counts["closed_campaigns"] += 1
            self.campaign = None
        return raw


def hfloat_row(state, symbol, bid, ask):
    row = state.state_row()
    mult = price_multiplier(symbol, bid)
    floating = ((bid * row[0] - row[1]) + (row[4] - ask * row[3])) * mult
    return floating, row


def update_change(indices, rows, index, row):
    if indices[-1] == index:
        rows[-1] = row
    elif rows[-1] != row:
        indices.append(index)
        rows.append(row)


def make_day_events(symbol):
    day_map = defaultdict(list)
    for time_ms, items in core_events[symbol].items():
        for action, order in items:
            day = dt.datetime.fromtimestamp(time_ms / 1000, dt.UTC).date()
            day_map[day].append({"time": time_ms, "kind": "core_" + action, "order": order})
    for ev in events_by_symbol.get(symbol, []):
        day = dt.datetime.fromtimestamp(ev["time"] / 1000, dt.UTC).date()
        day_map[day].append({"time": ev["time"], "kind": "signal", "signal": ev})
    for day in day_map:
        day_map[day].sort(key=lambda x: (x["time"], 0 if x["kind"].startswith("core_") else 1))
    return day_map


day_events = {s: make_day_events(s) for s in symbols}
variant_names = ["BASELINE", "TYPE1", "TYPE2", "TYPE3", "TYPE4"]
variants = {n: (None if n == "BASELINE" else int(n[-1])) for n in variant_names}
states = {s: {n: HedgeState(n) for n in variant_names if n != "BASELINE"} for s in symbols}
core_active = {s: dict(initial_active[s]) for s in symbols}
daily = {s: {} for s in symbols}
actions_by_pair = {n: {s: [] for s in symbols} for n in variant_names}
decision_log = {n: {s: [] for s in symbols} for n in variant_names if n != "BASELINE"}
trade_day_count = 0
coverage_missing = []

current_day = FIRST
while current_day <= LAST:
    tick_by_symbol = {s: quotes(s, current_day) for s in symbols}
    day_has_quotes = any(a is not None and len(a) for a in tick_by_symbol.values())
    if not day_has_quotes:
        for s in symbols:
            for ev in day_events[s].get(current_day, []):
                pass
        current_day += dt.timedelta(days=1)
        continue
    trade_day_count += 1
    for s in symbols:
        a = tick_by_symbol[s]
        if a is None or len(a) == 0:
            if current_day.weekday() < 5:
                coverage_missing.append({"date": current_day.isoformat(), "symbol": s})
            continue
        times = a["time_msc"].astype(np.int64)
        if np.any(np.diff(times) < 0):
            raise AssertionError("tick times are not strictly ordered for " + s + " " + current_day.isoformat())
        evs = day_events[s].get(current_day, [])
        mapped = defaultdict(list)
        for ev in evs:
            j = int(np.searchsorted(times, ev["time"], side="left"))
            if j >= len(times):
                continue
            em = dict(ev)
            em["index"] = j
            em["fill_time"] = int(times[j])
            em["stale"] = bool(times[j] - ev["time"] > MAX_MARK_AGE_MS)
            if em["kind"] == "signal":
                em["signal"] = dict(em["signal"])
                em["signal"]["stale"] = em["stale"]
            mapped[j].append(em)

        active = core_active[s]
        core_indices = [0]
        core_rows = [core_row(active)]
        pre_core = core_rows[0]
        pre_hedge = {n: states[s][n].state_row() for n in states[s]}
        hedge_indices = {n: [0] for n in states[s]}
        hedge_rows = {n: [pre_hedge[n]] for n in states[s]}
        hedge_realized_open = {n: states[s][n].realized_base for n in states[s]}
        hedge_stress_open = {n: states[s][n].realized_stress for n in states[s]}
        hedge_action_events = {n: [] for n in states[s]}

        def capture_action(n, hs, core_now, fill_time):
            item = hs.actions[-1]
            hedge_lots = sum(p["lots"] for p in hs.positions)
            hedge_action_events[n].append({
                **item,
                "fill_time": int(fill_time),
                "core_layers": int(core_now["layers"]),
                "core_direction": int(core_now["direction"]),
                "core_net_lots": float(core_now["net"]),
                "hedge_tickets_after": len(hs.positions),
                "hedge_lots_after": float(hedge_lots),
            })

        for j in sorted(mapped):
            batch = mapped[j]
            core_batch = [ev for ev in batch if ev["kind"].startswith("core_")]
            signal_batch = [ev for ev in batch if ev["kind"] == "signal"]
            if core_batch:
                for ev in core_batch:
                    order = ev["order"]
                    if ev["kind"] == "core_open":
                        active[order[0]] = order
                for ev in core_batch:
                    order = ev["order"]
                    if ev["kind"] == "core_close":
                        active.pop(order[0], None)
                update_change(core_indices, core_rows, j, core_row(active))
                core_now = core_snapshot(active)
                bid = float(a["bid"][j])
                ask = float(a["ask"][j])
                for n, hs in states[s].items():
                    if hs.positions and (core_now["direction"] == 0 or
                                         hs.positions[0]["side"] != -core_now["direction"]):
                        before = len(hs.actions)
                        hs.close(s, sum(p["lots"] for p in hs.positions), bid, ask,
                                 int(times[j]), "core flat/side changed")
                        capture_action(n, hs, core_now, int(times[j]))
                    if hs.positions:
                        target = down_lots(abs(core_now["net"]) * HEDGE_RATIO)
                        held = sum(p["lots"] for p in hs.positions)
                        if held > target + LOT_STEP * 0.25:
                            before = len(hs.actions)
                            hs.close(s, held - target, bid, ask, int(times[j]), "basket shrank")
                            capture_action(n, hs, core_now, int(times[j]))
                    update_change(hedge_indices[n], hedge_rows[n], j, hs.state_row())
            if signal_batch:
                signals = [ev["signal"] for ev in signal_batch]
                core_now = core_snapshot(active)
                bid = float(a["bid"][j])
                ask = float(a["ask"][j])
                fill_time = int(times[j])
                spread_pips = (ask - bid) / 0.0001
                # The common exit uses the first approved confirmed RE back toward current Tengri net side.
                for n, hs in states[s].items():
                    gate_blocked = [ev for ev in signals
                                    if ev["kind"] == variants[n] and not ev.get("approved", True)]
                    for ev in gate_blocked:
                        decision_log[n][s].append({
                            "role": "entry", "status": "BLOCKED",
                            "reason": "D1/H4/M15 approval gate false",
                            "signal_time": int(ev["time"]),
                            "decision_quote_time": fill_time,
                            "signal_age_ms": fill_time - int(ev["time"]),
                            "signal_type": ev["type"],
                            "signal_direction": "BUY" if ev["direction"] > 0 else "SELL",
                            "core_direction": int(core_now["direction"]),
                            "core_layers": int(core_now["layers"]),
                            "core_net_lots": float(core_now["net"]),
                            "hedge_tickets_before": len(states[s][n].positions),
                            "hedge_lots_before": float(sum(p["lots"] for p in states[s][n].positions)),
                        })
                    exit_candidates = [ev for ev in signals
                                       if ev.get("approved", True)
                                       and ev["direction"] == core_now["direction"]
                                       and core_now["direction"] != 0
                                       and not ev["stale"]]
                    if hs.positions and exit_candidates:
                        ev = exit_candidates[0]
                        decision_log[n][s].append({
                            "role": "exit", "status": "ACCEPTED",
                            "reason": "first H1 RE back to Tengri direction",
                            "signal_time": int(ev["time"]), "decision_quote_time": fill_time,
                            "signal_age_ms": fill_time - int(ev["time"]),
                            "signal_type": ev["type"],
                            "signal_direction": "BUY" if ev["direction"] > 0 else "SELL",
                            "core_direction": int(core_now["direction"]),
                            "core_layers": int(core_now["layers"]),
                            "core_net_lots": float(core_now["net"]),
                            "hedge_tickets_before": len(hs.positions),
                            "hedge_lots_before": float(sum(p["lots"] for p in hs.positions)),
                        })
                        hs.counts["exit_reentry_signals"] += 1
                        hs.close(s, sum(p["lots"] for p in hs.positions), bid, ask,
                                 fill_time, "first H1 RE back to Tengri direction")
                        capture_action(n, hs, core_now, fill_time)

                    selected = [ev for ev in signals
                                if ev["kind"] == variants[n] and ev.get("approved", True)]
                    hs.counts["entry_events_for_type"] += len(selected)
                    consumed = False
                    for ev in selected:
                        base = {
                            "role": "entry", "signal_time": int(ev["time"]),
                            "decision_quote_time": fill_time,
                            "signal_age_ms": fill_time - int(ev["time"]),
                            "signal_type": ev["type"],
                            "signal_direction": "BUY" if ev["direction"] > 0 else "SELL",
                            "core_direction": int(core_now["direction"]),
                            "core_layers": int(core_now["layers"]),
                            "core_net_lots": float(core_now["net"]),
                            "hedge_tickets_before": len(hs.positions),
                            "hedge_lots_before": float(sum(p["lots"] for p in hs.positions)),
                            "spread_pips": float(spread_pips),
                        }
                        if consumed:
                            decision_log[n][s].append({
                                **base, "status": "BLOCKED",
                                "reason": "another same-timestamp signal already consumed",
                            })
                            continue
                        if ev["stale"]:
                            hs.counts["stale_signal_blocked"] += 1
                            decision_log[n][s].append({
                                **base, "status": "BLOCKED", "reason": "quote age exceeds 300 seconds",
                            })
                            continue
                        if core_now["direction"] == 0 or ev["direction"] == core_now["direction"]:
                            hs.counts["ineligible_direction_or_flat"] += 1
                            reason = "Tengri is flat" if core_now["direction"] == 0 else "signal is not opposite Tengri"
                            decision_log[n][s].append({
                                **base, "status": "BLOCKED", "reason": reason,
                            })
                            continue
                        if core_now["layers"] < MIN_LAYERS:
                            hs.counts["ineligible_layers"] += 1
                            decision_log[n][s].append({
                                **base, "status": "BLOCKED",
                                "reason": f"Tengri layers below {MIN_LAYERS}",
                            })
                            continue
                        target = down_lots(abs(core_now["net"]) * HEDGE_RATIO)
                        if target < MIN_LOT:
                            hs.counts["target_below_minimum"] += 1
                            decision_log[n][s].append({
                                **base, "status": "BLOCKED", "reason": "25% hedge target below minimum lot",
                                "target_hedge_lots": float(target),
                            })
                            continue
                        hs.counts["eligible_entry_events"] += 1
                        if spread_pips > SPREAD_CAP_PIPS:
                            hs.counts["spread_blocked"] += 1
                            decision_log[n][s].append({
                                **base, "status": "BLOCKED",
                                "reason": f"spread exceeds {SPREAD_CAP_PIPS} pips",
                                "target_hedge_lots": float(target),
                            })
                            continue
                        held = sum(p["lots"] for p in hs.positions)
                        if target > held + LOT_STEP * 0.25:
                            add = down_lots(target - held)
                            reentry = not hs.positions and bool(hs.closed_campaigns)
                            if add >= MIN_LOT and hs.open(s, ev["direction"], add,
                                                         bid, ask, fill_time, ev["kind"]):
                                capture_action(n, hs, core_now, fill_time)
                                decision_log[n][s].append({
                                    **base, "status": "ACCEPTED",
                                    "reason": "hedge re-entry" if reentry else ("hedge opened" if held == 0 else "hedge added"),
                                    "target_hedge_lots": float(target),
                                    "accepted_lots": float(add),
                                    "hedge_tickets_after": len(hs.positions),
                                    "hedge_lots_after": float(sum(p["lots"] for p in hs.positions)),
                                    "reentry": bool(reentry),
                                })
                            else:
                                decision_log[n][s].append({
                                    **base, "status": "BLOCKED", "reason": "calculated add is below minimum lot",
                                    "target_hedge_lots": float(target), "add_lots": float(add),
                                })
                        else:
                            decision_log[n][s].append({
                                **base, "status": "ACCEPTED_NO_CHANGE",
                                "reason": "hedge is already at or above target",
                                "target_hedge_lots": float(target),
                                "hedge_lots_after": float(held),
                                "hedge_tickets_after": len(hs.positions),
                                "reentry": False,
                            })
                        consumed = True
                    update_change(hedge_indices[n], hedge_rows[n], j, hs.state_row())

        daily[s][current_day] = {
            "ticks": a, "core_times": times[np.array(core_indices, dtype=int)],
            "core_rows": np.asarray(core_rows, dtype=float), "pre_core": np.asarray(pre_core, dtype=float),
            "hedge": {}
        }
        for n, hs in states[s].items():
            daily[s][current_day]["hedge"][n] = {
                "times": times[np.array(hedge_indices[n], dtype=int)],
                "rows": np.asarray(hedge_rows[n], dtype=float),
                "pre": np.asarray(pre_hedge[n], dtype=float),
                "realized_open": hedge_realized_open[n],
                "stress_open": hedge_stress_open[n],
                "actions": list(hedge_action_events[n]),
            }
            actions_by_pair[n][s].extend(hedge_action_events[n])
    current_day += dt.timedelta(days=1)

if coverage_missing:
    raise RuntimeError("Missing weekday tick files: " + json.dumps(coverage_missing[:10]))
if trade_day_count == 0:
    raise RuntimeError("No quote days found")

def utc(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def slim_event(item):
    clean = dict(item)
    clean["signal_time_utc"] = utc(clean.pop("signal_time"))
    clean["decision_quote_time_utc"] = utc(clean.pop("decision_quote_time"))
    if clean.get("fill_time") is not None:
        clean["fill_time_utc"] = utc(clean.pop("fill_time"))
    return clean

def slim_action(item):
    return {
        "time_utc": utc(item["time"]),
        "fill_time_utc": utc(item["fill_time"]),
        "action": item["action"],
        "reason": item["reason"],
        "lots": float(item["lots"]),
        "core_layers": int(item["core_layers"]),
        "core_direction": int(item["core_direction"]),
        "core_net_lots": float(item["core_net_lots"]),
        "hedge_tickets_after": int(item["hedge_tickets_after"]),
        "hedge_lots_after": float(item["hedge_lots_after"]),
    }

variants_out = {}
for n in variant_names:
    if n == "BASELINE":
        continue
    variants_out[n] = {}
    for s in symbols:
        decisions = [slim_event(x) for x in decision_log[n][s]]
        actions = [slim_action(x) for x in actions_by_pair[n][s]]
        reasons = defaultdict(int)
        statuses = defaultdict(int)
        for x in decisions:
            statuses[x["status"]] += 1
            reasons[x["reason"]] += 1
        variants_out[n][s] = {
            "summary": {
                "approved_type_events_received": int(event_counts[s][int(n[-1])]),
                "blocked_by_d1_h4_gate": int(gate_blocked_counts[s][int(n[-1])]),
                "decisions_logged": len(decisions),
                "accepted": int(statuses["ACCEPTED"]),
                "accepted_no_change": int(statuses["ACCEPTED_NO_CHANGE"]),
                "blocked": int(statuses["BLOCKED"]),
                "block_reasons": dict(sorted(reasons.items())),
                "entry_actions": sum(x["action"] == "open/add" for x in actions),
                "exit_or_trim_actions": sum(x["action"] == "trim/close" for x in actions),
                "reentry_decisions": sum(bool(x.get("reentry")) for x in decisions),
                "hedge_tickets_at_end": int(len(states[s][n].positions)),
                "hedge_lots_at_end": float(sum(p["lots"] for p in states[s][n].positions)),
            },
            "decisions": decisions,
            "actions": actions,
        }

result = {
    "classification": "DIAGNOSTIC_ONLY_SOURCE_MISMATCH",
    "performance_status": "NOT_VALIDATED",
    "window_utc": [FIRST.isoformat(), LAST.isoformat()],
    "source_feed": {
        "platform": "MT5",
        "broker_server": "HFMarketsGlobal-Demo4",
        "requested_target": "MT4 HFMarketsSV-Demo Server",
        "usage": "exploratory mechanics replay only; not a valid MT4 performance test",
        "warmup_and_tick_coverage": "not proven complete for the locked period",
    },
    "locked_mechanics": {
        "signal_gate": "approved D1/H4/M15 event rows only",
        "variants": "Type 1, Type 2, Type 3, Type 4 evaluated separately",
        "entry_minimum_tengri_layers": MIN_LAYERS,
        "hedge_sizing": "25% of current net Tengri lots, rounded down to 0.01 lot",
        "entry_spread_cap_pips": SPREAD_CAP_PIPS,
        "entry_fill": "first available quote at or after event decision time",
        "common_signal_exit": "first fresh approved H1 Re-Entry in current Tengri net direction",
        "safety_exit": "Tengri flat or Hedge no longer opposite; trim when Tengri basket shrinks",
    },
    "signal_events_approved_by_type": {
        s: {str(k): int(event_counts[s][k]) for k in (1, 2, 3, 4)} for s in symbols
    },
    "variants": variants_out,
    "explicitly_unreported": [
        "P&L", "expectancy", "profit factor", "floating drawdown",
        "margin usage", "stop-out safety", "production validity",
    ],
}
output = ROOT / "BBMA516_Tengri_Hedge_Type1_4_DIAGNOSTICS_ONLY_20261123.json"
output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
summary = {n: {s: result["variants"][n][s]["summary"] for s in symbols}
           for n in result["variants"]}
print(json.dumps({"result_file": str(output), "summary": summary}, separators=(",", ":")), flush=True)

raise SystemExit(0)
