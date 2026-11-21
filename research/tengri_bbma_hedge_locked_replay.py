import csv
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
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
with event_file.open(newline="", encoding="utf-8-sig") as fh:
    for row in csv.DictReader(fh):
        if row.get("d1_h4_m15_approved", "").strip().lower() != "true":
            continue
        event_dt = dt.datetime.strptime(row["first_m15"], "%Y.%m.%d %H:%M").replace(tzinfo=dt.UTC)
        event_ms = int(event_dt.timestamp() * 1000)
        if not (START_MS <= event_ms < END_MS):
            continue
        kind = int(row["type"].split("_")[2])
        direction = 1 if row["direction"] == "DIR_BUY" else -1
        ev = {"time": event_ms, "kind": kind, "direction": direction,
              "type": row["type"], "hash": row["hash"]}
        events_by_symbol[row["symbol"]].append(ev)
        event_counts[row["symbol"]][kind] += 1
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
                        hedge_action_events[n].append(hs.actions[-1])
                    if hs.positions:
                        target = down_lots(abs(core_now["net"]) * HEDGE_RATIO)
                        held = sum(p["lots"] for p in hs.positions)
                        if held > target + LOT_STEP * 0.25:
                            before = len(hs.actions)
                            hs.close(s, held - target, bid, ask, int(times[j]), "basket shrank")
                            hedge_action_events[n].append(hs.actions[-1])
                    update_change(hedge_indices[n], hedge_rows[n], j, hs.state_row())
            if signal_batch:
                signals = [ev["signal"] for ev in signal_batch]
                core_now = core_snapshot(active)
                bid = float(a["bid"][j])
                ask = float(a["ask"][j])
                spread_pips = (ask - bid) / 0.0001
                # The common exit uses the first approved confirmed RE back toward current Tengri net side.
                for n, hs in states[s].items():
                    if hs.positions and core_now["direction"] != 0 and any(
                        ev["direction"] == core_now["direction"] and not ev["stale"] for ev in signals
                    ):
                        hs.counts["exit_reentry_signals"] += 1
                        hs.close(s, sum(p["lots"] for p in hs.positions), bid, ask,
                                 int(times[j]), "first H1 RE back to Tengri direction")
                        hedge_action_events[n].append(hs.actions[-1])
                    selected = [ev for ev in signals if ev["kind"] == variants[n]]
                    hs.counts["entry_events_for_type"] += len(selected)
                    for ev in selected:
                        if ev["stale"]:
                            hs.counts["stale_signal_blocked"] += 1
                            continue
                        if core_now["direction"] == 0 or ev["direction"] == core_now["direction"]:
                            hs.counts["ineligible_direction_or_flat"] += 1
                            continue
                        if core_now["layers"] < MIN_LAYERS:
                            hs.counts["ineligible_layers"] += 1
                            continue
                        target = down_lots(abs(core_now["net"]) * HEDGE_RATIO)
                        if target < MIN_LOT:
                            hs.counts["target_below_minimum"] += 1
                            continue
                        hs.counts["eligible_entry_events"] += 1
                        if spread_pips > SPREAD_CAP_PIPS:
                            hs.counts["spread_blocked"] += 1
                            continue
                        held = sum(p["lots"] for p in hs.positions)
                        if target > held + LOT_STEP * 0.25:
                            add = down_lots(target - held)
                            if add >= MIN_LOT and hs.open(s, ev["direction"], add,
                                                         bid, ask, int(times[j]), ev["kind"]):
                                hedge_action_events[n].append(hs.actions[-1])
                        break
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

def state_at(change_times, change_rows, pre_row, query_times):
    ix = np.searchsorted(change_times, query_times, side="right") - 1
    result = np.tile(pre_row, (len(query_times), 1))
    ok = ix >= 0
    result[ok] = change_rows[ix[ok]]
    return result


def cumulative_at(opening, action_rows, query_times, key):
    if not action_rows:
        return np.full(len(query_times), float(opening))
    ts = np.array([int(r["time"]) for r in action_rows], dtype=np.int64)
    ds = np.array([float(r[key]) for r in action_rows], dtype=float)
    order = np.argsort(ts, kind="stable")
    ts, ds = ts[order], ds[order]
    cum = float(opening) + np.r_[0.0, np.cumsum(ds)]
    return cum[np.searchsorted(ts, query_times, side="right")]


def pfloat(row, bid, ask, symbol):
    mult = 100000.0 if symbol == "EURUSD" else 100000.0 / np.maximum(bid, 1e-12)
    return ((bid * row[:, 0] - row[:, 1]) + (row[:, 4] - ask * row[:, 3])) * mult


def campaign_metrics(hs):
    closed = hs.closed_campaigns
    net = [c["net_base"] for c in closed]
    wins = [x for x in net if x > 0]
    losses = [x for x in net if x < 0]
    expectancy = (sum(net) / len(net)) if net else None
    pf = (sum(wins) / abs(sum(losses))) if losses else (None if not wins else "infinite_no_losses")
    return {
        "closed_campaign_count": len(closed),
        "campaign_expectancy_USC": None if expectancy is None else round(expectancy, 4),
        "campaign_profit_factor": pf,
        "winning_campaigns": len(wins), "losing_campaigns": len(losses),
        "closed_campaign_net_USC": round(sum(net), 4),
        "closed_campaigns_stress_net_USC": round(sum(c["net_stress"] for c in closed), 4),
    }


equity_metrics = {n: {"peak": None, "max_dd_USC": 0.0, "max_dd_pct": 0.0,
                       "min_equity_flow_adjusted_USC": None,
                       "min_floating_USC": 0.0, "first_equity": None,
                       "last_equity": None, "valid_marks": 0}
                  for n in variant_names}
variant_pair_final = {n: {} for n in variant_names}
stress_equity_metrics = {n: {"peak": None, "max_dd_USC": 0.0, "max_dd_pct": 0.0,
                             "min_equity_flow_adjusted_USC": None, "first_equity": None,
                             "last_equity": None, "valid_marks": 0}
                         for n in variant_names}

dates = sorted(set(d for s in symbols for d in daily[s]))
for day in dates:
    day_arrays = [daily[s][day]["ticks"]["time_msc"].astype(np.int64)
                  for s in symbols if day in daily[s]]
    all_times = np.unique(np.concatenate(day_arrays))
    pair_mark = {}
    pair_core_state = {}
    pair_core_float = {}
    pair_fresh = {}
    for s in symbols:
        if day not in daily[s]:
            pair_mark[s] = None
            pair_core_state[s] = None
            pair_core_float[s] = np.zeros(len(all_times))
            pair_fresh[s] = np.zeros(len(all_times), dtype=bool)
            continue
        d = daily[s][day]
        bid, ask, fresh = marks(d["ticks"], all_times)
        core = state_at(d["core_times"], d["core_rows"], d["pre_core"], all_times)
        pair_mark[s] = (bid, ask)
        pair_core_state[s] = core
        pair_core_float[s] = pfloat(core, bid, ask, s)
        pair_fresh[s] = fresh

    cash_ix = np.searchsorted(cash_times, all_times, side="right")
    cash_value = OPENING_BALANCE_USC + cash_cum[cash_ix]
    funding_times = np.array([t for t, _ in flows], dtype=np.int64)
    funding_values = np.array([v for _, v in flows], dtype=float)
    funding_cum = np.r_[0.0, np.cumsum(funding_values)]
    funding_value = funding_cum[np.searchsorted(funding_times, all_times, side="right")]

    for n in variant_names:
        total_hedge_float = np.zeros(len(all_times))
        total_hedge_realized = np.zeros(len(all_times))
        total_stress_realized = np.zeros(len(all_times))
        valid = np.ones(len(all_times), dtype=bool)
        combined_core_float = np.zeros(len(all_times))
        combined_float = np.zeros(len(all_times))
        for s in symbols:
            combined_core_float += pair_core_float[s]
            if pair_mark[s] is not None:
                bid, ask = pair_mark[s]
                hd = daily[s][day]["hedge"].get(n)
                if hd is not None:
                    hr = state_at(hd["times"], hd["rows"], hd["pre"], all_times)
                    hf = pfloat(hr, bid, ask, s)
                    total_hedge_float += hf
                    realized0 = hd["realized_open"]
                    stress0 = hd["stress_open"]
                    total_hedge_realized += cumulative_at(realized0, hd["actions"], all_times, "net_balance_delta_base")
                    total_stress_realized += cumulative_at(stress0, hd["actions"], all_times, "net_balance_delta_stress")
            open_counts = (pair_core_state[s][:, 2] + pair_core_state[s][:, 5]) if pair_core_state[s] is not None else np.zeros(len(all_times))
            hd_row = None
            if pair_mark[s] is not None and n != "BASELINE":
                hd = daily[s][day]["hedge"].get(n)
                if hd is not None:
                    hd_row = state_at(hd["times"], hd["rows"], hd["pre"], all_times)
                    open_counts = open_counts + hd_row[:, 2] + hd_row[:, 5]
            valid &= (open_counts < 0.5) | pair_fresh[s]
        combined_float = combined_core_float + total_hedge_float
        equity_base = cash_value + total_hedge_realized + combined_core_float + total_hedge_float
        equity_stress = cash_value + total_stress_realized + combined_core_float + total_hedge_float
        adjusted_base = equity_base - funding_value
        adjusted_stress = equity_stress - funding_value
        for key, series, target in [
            (n, adjusted_base, equity_metrics),
            (n, adjusted_stress, stress_equity_metrics),
        ]:
            stats = target[key]
            good = np.flatnonzero(valid)
            if not len(good):
                continue
            vals = series[good]
            floats = combined_float[good]
            if stats["first_equity"] is None:
                stats["first_equity"] = float(vals[0])
            stats["last_equity"] = float(vals[-1])
            local_peak = np.maximum.accumulate(vals)
            prior_peak = stats["peak"]
            if prior_peak is not None:
                local_peak = np.maximum(local_peak, prior_peak)
            dd = local_peak - vals
            pct = np.divide(dd * 100.0, local_peak, out=np.zeros_like(dd), where=local_peak > 0)
            stats["max_dd_USC"] = max(stats["max_dd_USC"], float(dd.max()))
            stats["max_dd_pct"] = max(stats["max_dd_pct"], float(pct.max()))
            stats["peak"] = float(local_peak[-1])
            current_min = float(vals.min())
            if stats["min_equity_flow_adjusted_USC"] is None:
                stats["min_equity_flow_adjusted_USC"] = current_min
            else:
                stats["min_equity_flow_adjusted_USC"] = min(stats["min_equity_flow_adjusted_USC"], current_min)
            if target is equity_metrics:
                stats["min_floating_USC"] = min(stats["min_floating_USC"], float(floats.min()))
            stats["valid_marks"] += len(good)
        if day == dates[-1]:
            for s in symbols:
                hs = states[s].get(n)
                if n == "BASELINE" or hs is None:
                    variant_pair_final[n][s] = {"hedge_net_PnL_USC": 0.0, "open_lots": 0.0,
                                                "open_float_USC": 0.0, "base_cost_USC": 0.0,
                                                "stress_cost_USC": 0.0, "spread_cost_est_USC": 0.0}
                    continue
                d = daily[s].get(day)
                if d is not None:
                    tick = d["ticks"][-1]
                    open_float = hs.float_pnl(s, float(tick["bid"]), float(tick["ask"]))
                else:
                    open_float = 0.0
                variant_pair_final[n][s] = {
                    "hedge_net_PnL_USC": round(hs.realized_base + open_float, 4),
                    "open_lots": round(sum(p["lots"] for p in hs.positions), 4),
                    "open_float_USC": round(open_float, 4),
                    "base_cost_USC": round(hs.fixed_base, 4),
                    "stress_cost_USC": round(hs.fixed_base + hs.fixed_extra, 4),
                    "spread_cost_est_USC": round(hs.spread_cost, 4),
                }

def final_state_metrics(hs):
    open_float = 0.0
    if hs.positions:
        # last quote is recovered from the final data day for this symbol
        symbol = next(s for s in symbols if hs is states[s].get(hs.name))
        last_day = max(daily[symbol])
        tick = daily[symbol][last_day]["ticks"][-1]
        open_float = hs.float_pnl(symbol, float(tick["bid"]), float(tick["ask"]))
    result = campaign_metrics(hs)
    result.update({
        "entry_or_add_orders": hs.counts["entries_or_adds"],
        "close_or_trim_actions": hs.counts["close_or_trim_actions"],
        "open_campaign_at_end": bool(hs.positions),
        "open_campaign_net_to_market_USC": None if not hs.positions or hs.campaign is None else
            round(hs.campaign["raw_realized"] + open_float - hs.campaign["fixed_base"], 4),
        "open_campaign_stress_net_to_market_USC": None if not hs.positions or hs.campaign is None else
            round(hs.campaign["raw_realized"] + open_float - hs.campaign["fixed_base"] - hs.campaign["fixed_extra"], 4),
        "entry_events_for_type": hs.counts["entry_events_for_type"],
        "eligible_entry_events": hs.counts["eligible_entry_events"],
        "ineligible_layers": hs.counts["ineligible_layers"],
        "ineligible_direction_or_flat": hs.counts["ineligible_direction_or_flat"],
        "target_below_minimum": hs.counts["target_below_minimum"],
        "spread_blocked": hs.counts["spread_blocked"],
        "stale_signal_blocked": hs.counts["stale_signal_blocked"],
        "exit_reentry_signals": hs.counts["exit_reentry_signals"],
        "closed_campaigns": hs.closed_campaigns,
    })
    return result

result = {
    "window": [FIRST.isoformat(), LAST.isoformat()],
    "opening_balance_USC": OPENING_BALANCE_USC,
    "tick_quote_days": trade_day_count,
    "coverage_missing": coverage_missing,
    "signal_events_approved": {s: {str(k): event_counts[s][k] for k in (1,2,3,4)} for s in symbols},
    "locked_rules": {
        "minimum_net_side_Tengri_layers": MIN_LAYERS,
        "hedge_target_percent_of_net_lots": HEDGE_RATIO * 100,
        "entry_spread_cap_pips": SPREAD_CAP_PIPS,
        "same_exit": "first approved confirmed H1 Re-Entry in current net Tengri direction; safety close if Tengri is flat or Hedge direction is no longer opposite",
        "signal_fill_time": "first HFM quote at/after the first M15 decision row after the H1 close",
        "fixed_cost_base_pips_per_lot_action": BASE_EXTRA_PIPS_PER_ACTION,
        "fixed_cost_stress_pips_per_lot_action": STRESS_EXTRA_PIPS_PER_ACTION,
        "hedge_order_book": "fixed historical Tengri stream; Hedge P&L does not recalculate later Tengri lots",
    },
    "variants": {}
}
for n in variant_names:
    if n == "BASELINE":
        result["variants"][n] = {
            "combined_equity": equity_metrics[n],
            "combined_equity_stress": stress_equity_metrics[n],
            "pairs": {s: {"hedge_net_PnL_USC": 0.0, "open_lots": 0.0} for s in symbols},
            "hedge_campaigns": None,
        }
        continue
    pair_details = {}
    for s in symbols:
        pair_details[s] = {
            "hedge": final_state_metrics(states[s][n]),
            "ending": variant_pair_final[n].get(s, {}),
        }
    combined = {
        "combined_equity": equity_metrics[n],
        "combined_equity_stress": stress_equity_metrics[n],
        "hedge_campaigns": {
            "closed_campaign_count": sum(len(states[s][n].closed_campaigns) for s in symbols),
            "campaign_expectancy_USC": None,
            "campaign_profit_factor": None,
        },
        "pairs": pair_details,
    }
    closed = [c for s in symbols for c in states[s][n].closed_campaigns]
    vals = [c["net_base"] for c in closed]
    wins = [v for v in vals if v > 0]
    losses = [v for v in vals if v < 0]
    combined["hedge_campaigns"].update({
        "campaign_expectancy_USC": None if not vals else round(sum(vals)/len(vals), 4),
        "campaign_profit_factor": (sum(wins)/abs(sum(losses))) if losses else (None if not wins else "infinite_no_losses"),
        "winning_campaigns": len(wins), "losing_campaigns": len(losses),
        "closed_campaign_net_USC": round(sum(vals), 4),
        "closed_campaign_stress_net_USC": round(sum(c["net_stress"] for c in closed), 4),
    })
    combined["totals"] = {
        "entry_or_add_orders": sum(states[s][n].counts["entries_or_adds"] for s in symbols),
        "close_or_trim_actions": sum(states[s][n].counts["close_or_trim_actions"] for s in symbols),
        "base_fixed_cost_USC": round(sum(states[s][n].fixed_base for s in symbols), 4),
        "stress_fixed_cost_USC": round(sum(states[s][n].fixed_base + states[s][n].fixed_extra for s in symbols), 4),
        "spread_cost_est_USC": round(sum(states[s][n].spread_cost for s in symbols), 4),
        "hedge_net_PnL_including_open_float_USC": round(sum(
            states[s][n].realized_base + variant_pair_final[n][s]["open_float_USC"] for s in symbols), 4),
        "open_campaigns_at_end": sum(bool(states[s][n].positions) for s in symbols),
    }
    result["variants"][n] = combined

for n in variant_names:
    stats = equity_metrics[n]
    if stats["first_equity"] is not None and stats["last_equity"] is not None:
        stats["net_flow_adjusted_PnL_USC"] = round(stats["last_equity"] - stats["first_equity"], 4)
    stress = stress_equity_metrics[n]
    if "first_equity" in stress and stress["first_equity"] is not None and stress["last_equity"] is not None:
        stress["net_flow_adjusted_PnL_USC"] = round(stress["last_equity"] - stress["first_equity"], 4)
output = ROOT / "BBMA516_Tengri_Hedge_Type1_4_locked_replay_result.json"
output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
summary = {n: {"net_PnL_USC": result["variants"][n].get("combined_equity", {}).get("net_flow_adjusted_PnL_USC"),
               "max_DD_USC": result["variants"][n].get("combined_equity", {}).get("max_dd_USC")}
           for n in variant_names}
print(json.dumps({"result_file": str(output), "summary": summary}, separators=(",", ":")), flush=True)
