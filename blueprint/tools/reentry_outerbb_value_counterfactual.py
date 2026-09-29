from __future__ import annotations

import argparse
import bisect
import calendar
import hashlib
from array import array
import html
import json
import math
import re
import struct
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

FMT = "%Y.%m.%d %H:%M"
POINT = 0.00001
CONTRACT = 100000.0
TEST_SPREAD_POINTS = 20
FRACTIONS = (0.25, 0.50, 0.75, 1.00)
HST_SHA = {
    1: "64D5BED21B61CC119507FD552D6A86091B2CF4A580EEFB5C589AA97654F56019",
    60: "566762B35FCE7EF2DCB5985A57DAC6BC5D0476A6A76DDEF2D680EF0905632389",
    240: "AA58B7E1114D20B135573168FD414DB7F210AB260427C8596CADFB8052E5015F",
}
PERIODS = ("Q8_2024", "Q8_2025H1", "Q8_2025H2", "Q8_2026YTD")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def dt(text: str) -> datetime:
    return datetime.strptime(text, FMT)


def decode_file(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "cp1252", "utf-16"):
        try:
            return raw.decode(enc)
        except UnicodeError:
            continue
    return raw.decode("cp1252", errors="ignore")


def strip_cell(value: str) -> str:
    value = re.sub(r"(?is)<[^>]+>", " ", value)
    return html.unescape(value).replace("&nbsp;", " ").strip()

def parse_report(path: Path) -> dict[int, dict]:
    text = decode_file(path)
    rows = []
    for tr in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", text):
        cells = re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", tr)
        vals = [strip_cell(x) for x in cells]
        if vals:
            rows.append(vals)
    trades: dict[int, dict] = {}
    for row in rows:
        if len(row) < 8 or not row[0].isdigit():
            continue
        kind = row[2].lower()
        if not row[3].isdigit():
            continue
        order = int(row[3])
        if kind in ("buy", "sell"):
            trades[order] = {
                "order": order, "side": kind, "open_time": dt(row[1]),
                "lot": float(row[4]), "entry": float(row[5]),
                "sl": float(row[6]), "tp": float(row[7]),
            }
        elif order in trades and kind in ("close", "s/l", "t/p", "stop out"):
            trades[order].update(
                close_type=kind, close_time=dt(row[1]), close=float(row[5]),
                profit=float(row[8]) if len(row) > 8 and row[8] else 0.0,
            )
    return {k: v for k, v in trades.items() if "close_time" in v}

M17_RE = re.compile(
    r"\[M17-SL\]\[STRUCT\].*?Dir=(DIR_BUY|DIR_SELL) TF=(\d+) "
    r"Start=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) "
    r"Confirm=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}).*?"
    r"TP=([-\d.]+) C044=([YN])"
)
PREFLIGHT_RE = re.compile(r"\[P3M[12]\]\[PREFLIGHT_PASS\] DecisionID=(.*?) Entry=")
EXEC_RE = re.compile(
    r"\[P3M[12]\]\[EXEC\] Ticket=(\d+) Pair=\S+ DecisionID=(.*?) "
    r"Signal=(\S+) Dir=(\S+) ValidateCandle=(.*?) OrderOpen=(.*)$"
)
F7_RE = re.compile(
    r"\[F7-TELEM\] Event=(\S+) Ticket=(\d+).*?Reason=(\S+).*?"
    r"OwnerTF=(\d+) Candle=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})"
)


def parse_log(path: Path) -> dict[int, dict]:
    latest_struct = None
    struct_by_decision: dict[str, dict] = {}
    executions: dict[int, dict] = {}
    events: dict[int, list[dict]] = defaultdict(list)
    for line in decode_file(path).splitlines():
        m = M17_RE.search(line)
        if m:
            latest_struct = {
                "dir": m.group(1), "owner_tf": int(m.group(2)),
                "start": dt(m.group(3)), "confirm": dt(m.group(4)),
                "m17_tp": float(m.group(5)), "c044": m.group(6) == "Y",
            }
            continue

        m = PREFLIGHT_RE.search(line)
        if m and latest_struct is not None:
            struct_by_decision[m.group(1)] = dict(latest_struct)
            continue
        m = EXEC_RE.search(line)
        if m:
            ticket = int(m.group(1))
            did = m.group(2)
            rec = {
                "ticket": ticket, "decision_id": did, "signal": m.group(3),
                "dir": m.group(4), "validate": dt(m.group(5)),
                "open_time_log": dt(m.group(6)),
            }
            rec.update(struct_by_decision.get(did, {}))
            executions[ticket] = rec
            continue
        m = F7_RE.search(line)
        if m:
            events[int(m.group(2))].append({
                "event": m.group(1), "reason": m.group(3),
                "owner_tf": int(m.group(4)), "candle": dt(m.group(5)),
            })
    for ticket, rec in executions.items():
        rec["events"] = events.get(ticket, [])
        rec["momentum_candles"] = [
            x["candle"] for x in rec["events"] if x["event"] == "MOMENTUM_HOLD"
        ]
        rec["momentum_hold"] = bool(rec["momentum_candles"])
        latched = [x for x in rec["events"] if x["event"] == "EXIT_LATCHED"]
        rec["lifecycle_reason"] = latched[-1]["reason"] if latched else ""
    return executions

def load_hst(path: Path, expected_hash: str) -> tuple[list[datetime], dict[datetime, dict]]:
    if sha256(path) != expected_hash:
        raise RuntimeError(f"HST hash mismatch: {path}")
    raw = path.read_bytes()
    if len(raw) < 208 or raw[:4] != struct.pack("<I", 401):
        raise RuntimeError(f"unsupported HST format: {path}")
    times: list[datetime] = []
    rows: dict[datetime, dict] = {}
    for off in range(148, len(raw) - 59, 60):
        ts, opn, high, low, close, tv, spread, rv = struct.unpack(
            "<qddddqiq", raw[off:off + 60]
        )
        when = datetime.fromtimestamp(ts, timezone.utc).replace(tzinfo=None)
        times.append(when)
        rows[when] = {
            "open": opn, "high": high, "low": low, "close": close,
            "tick_volume": tv, "spread": spread, "real_volume": rv,
        }
    return times, rows


def bollinger(times: list[datetime], rows: dict[datetime, dict]) -> dict[datetime, tuple[float, float, float]]:
    out = {}
    closes: list[float] = []
    for when in times:
        closes.append(rows[when]["close"])
        if len(closes) < 20:
            continue
        window = closes[-20:]
        mid = sum(window) / 20.0
        std = math.sqrt(sum((x - mid) ** 2 for x in window) / 20.0)
        out[when] = (mid + 2.0 * std, mid, mid - 2.0 * std)
    return out

def pnl(side: str, entry: float, exit_price: float, lot: float) -> float:
    move = exit_price - entry if side == "buy" else entry - exit_price
    return move * CONTRACT * lot


def time_slice(times: list[datetime], start: datetime, end: datetime) -> list[datetime]:
    left = bisect.bisect_left(times, start)
    right = bisect.bisect_right(times, end)
    return times[left:right]


def frozen_hit(trade: dict, m1: tuple[array, array, array], target: float) -> dict | None:
    side, entry = trade["side"], trade["entry"]
    forward = target > entry if side == "buy" else target < entry
    if not forward:
        return None
    times, highs, lows = m1
    left = bisect.bisect_left(times, epoch(trade["open_time"]))
    right = bisect.bisect_left(times, epoch(trade["close_time"]))
    for i in range(left, right):
        hit = highs[i] >= target if side == "buy" else lows[i] <= target
        if hit:
            fill = target if side == "buy" else target + TEST_SPREAD_POINTS * POINT
            when = datetime.fromtimestamp(times[i], timezone.utc).replace(tzinfo=None)
            return {"time": when, "structural": target, "fill": fill, "pnl": pnl(side, entry, fill, trade["lot"])}
    return None


def mfe_value(trade: dict, m1: tuple[array, array, array], start: datetime | None = None) -> float:
    times, highs, lows = m1
    begin = start or trade["open_time"]
    left = bisect.bisect_left(times, epoch(begin))
    right = bisect.bisect_left(times, epoch(trade["close_time"]))
    if left >= right:
        return trade["profit"]
    if trade["side"] == "buy":
        exit_price = max(highs[left:right])
    else:
        exit_price = min(lows[left:right]) + TEST_SPREAD_POINTS * POINT
    return pnl(trade["side"], trade["entry"], exit_price, trade["lot"])

def dynamic_closed_event(
    trade: dict,
    owner_tf: int,
    owner_data: tuple[list[datetime], dict],
    bands: dict[datetime, tuple[float, float, float]],
) -> dict | None:
    times, rows = owner_data
    tf_delta = timedelta(minutes=owner_tf)
    for when in time_slice(times, trade["open_time"], trade["close_time"]):
        event_time = when + tf_delta
        if event_time > trade["close_time"] or when not in bands:
            continue
        row = rows[when]
        upper, _mid, lower = bands[when]
        structural = upper if trade["side"] == "buy" else lower
        touched = row["high"] >= structural if trade["side"] == "buy" else row["low"] <= structural
        if not touched:
            continue
        action_fill = row["close"]
        if trade["side"] == "sell":
            action_fill += TEST_SPREAD_POINTS * POINT
        return {
            "bar": when, "time": event_time, "structural": structural,
            "action_fill": action_fill,
            "action_pnl": pnl(trade["side"], trade["entry"], action_fill, trade["lot"]),
        }
    return None


def cf_profit(baseline: float, realized: float, fraction: float) -> float:
    return fraction * realized + (1.0 - fraction) * baseline

def analyze_period(
    period: str,
    report_path: Path,
    log_path: Path,
    m1: tuple[list[datetime], dict],
    owner_data: dict[int, tuple[list[datetime], dict]],
    owner_bands: dict[int, dict],
) -> tuple[list[dict], dict]:
    trades = parse_report(report_path)
    execs = parse_log(log_path)
    out: list[dict] = []
    skipped = defaultdict(int)
    for ticket, ex in execs.items():
        trade = trades.get(ticket)
        if trade is None:
            skipped["missing_report_trade"] += 1
            continue
        if not ex.get("c044"):
            skipped["non_c044"] += 1
            continue
        tf = ex.get("owner_tf")
        if tf not in (60, 240):
            skipped[f"owner_tf_{tf}"] += 1
            continue
        if ex.get("confirm") not in owner_bands[tf]:
            skipped["band_unresolved"] += 1
            continue
        upper, _mid, lower = owner_bands[tf][ex["confirm"]]
        frozen_target = upper if trade["side"] == "buy" else lower
        fwd = frozen_target > trade["entry"] if trade["side"] == "buy" else frozen_target < trade["entry"]
        fhit = frozen_hit(trade, m1, frozen_target)
        devent = dynamic_closed_event(trade, tf, owner_data[tf], owner_bands[tf])
        same_candle_momentum = (
            devent is not None and devent["bar"] in ex.get("momentum_candles", [])
        )
        row = {
            "period": period, "ticket": ticket, "signal": ex["signal"],
            "owner_tf": tf, "side": trade["side"], "decision_id": ex["decision_id"],
            "confirm": ex["confirm"].strftime(FMT), "open_time": trade["open_time"].strftime(FMT),
            "close_time": trade["close_time"].strftime(FMT), "close_type": trade["close_type"],
            "entry": trade["entry"], "close": trade["close"], "lot": trade["lot"],
            "baseline_profit": trade["profit"], "lifecycle_reason": ex["lifecycle_reason"],
            "momentum_hold": ex["momentum_hold"], "mfe_profit": mfe_value(trade, m1),
            "frozen_target": frozen_target, "frozen_forward": fwd,
        }

        if fhit:
            row.update(
                frozen_hit=True,
                frozen_hit_time=fhit["time"].strftime(FMT),
                frozen_realized_profit=fhit["pnl"],
                frozen_post_hit_mfe=mfe_value(trade, m1, fhit["time"]),
            )
        else:
            row.update(
                frozen_hit=False, frozen_hit_time="",
                frozen_realized_profit=None, frozen_post_hit_mfe=None,
            )
        if devent:
            row.update(
                dynamic_event=True,
                dynamic_event_time=devent["time"].strftime(FMT),
                dynamic_structural=devent["structural"],
                dynamic_action_profit=devent["action_pnl"],
                dynamic_post_event_mfe=mfe_value(trade, m1, devent["time"]),
                dynamic_same_candle_momentum=same_candle_momentum,
            )
        else:
            row.update(
                dynamic_event=False, dynamic_event_time="",
                dynamic_structural=None, dynamic_action_profit=None,
                dynamic_post_event_mfe=None,
                dynamic_same_candle_momentum=False,
            )
        for fraction in FRACTIONS:
            pct = int(fraction * 100)
            row[f"frozen_cf_{pct}"] = (
                cf_profit(trade["profit"], fhit["pnl"], fraction)
                if fhit else trade["profit"]
            )
            row[f"dynamic_cf_{pct}"] = (
                cf_profit(trade["profit"], devent["action_pnl"], fraction)
                if devent else trade["profit"]
            )
            row[f"dynamic_nm_cf_{pct}"] = (
                cf_profit(trade["profit"], devent["action_pnl"], fraction)
                if devent and not same_candle_momentum else trade["profit"]
            )
        out.append(row)
    meta = {
        "report_trades": len(trades), "log_executions": len(execs),
        "included_h1_h4_c044": len(out), "skipped": dict(skipped),
    }
    return out, meta

def avg(values: list[float]) -> float | None:
    return None if not values else sum(values) / len(values)


def summarize(rows: list[dict]) -> dict:
    if not rows:
        return {"trades": 0}
    baseline = sum(x["baseline_profit"] for x in rows)
    fwd = [x for x in rows if x["frozen_forward"]]
    fhits = [x for x in rows if x["frozen_hit"]]
    devs = [x for x in rows if x["dynamic_event"]]
    devs_momentum = [x for x in devs if x["dynamic_same_candle_momentum"]]
    devs_no_momentum = [x for x in devs if not x["dynamic_same_candle_momentum"]]
    result = {
        "trades": len(rows),
        "baseline_profit": round(baseline, 2),
        "baseline_winners": sum(x["baseline_profit"] > 0 for x in rows),
        "momentum_hold_trades": sum(x["momentum_hold"] for x in rows),
        "frozen_forward": len(fwd),
        "frozen_hits": len(fhits),
        "frozen_hit_rate_all_pct": round(100.0 * len(fhits) / len(rows), 2),
        "frozen_hit_rate_forward_pct": round(100.0 * len(fhits) / len(fwd), 2) if fwd else None,
        "dynamic_events": len(devs),
        "dynamic_event_rate_pct": round(100.0 * len(devs) / len(rows), 2),
        "dynamic_events_same_candle_momentum": len(devs_momentum),
        "dynamic_events_no_momentum": len(devs_no_momentum),
        "avg_mfe_profit": round(avg([x["mfe_profit"] for x in rows]) or 0.0, 4),
        "avg_frozen_distance_pips": round(avg([
            abs(x["frozen_target"] - x["entry"]) / 0.0001 for x in fwd
        ]) or 0.0, 2),
        "frozen_hits_with_momentum": sum(x["momentum_hold"] for x in fhits),
        "dynamic_events_with_momentum": sum(x["momentum_hold"] for x in devs),
        "close_reasons": dict(sorted({
            reason: sum(x["lifecycle_reason"] == reason for x in rows)
            for reason in {x["lifecycle_reason"] for x in rows}
        }.items())),
    }

    if fhits:
        result.update({
            "frozen_full_better_than_baseline": sum(
                x["frozen_realized_profit"] > x["baseline_profit"] for x in fhits
            ),
            "frozen_full_worse_than_baseline": sum(
                x["frozen_realized_profit"] < x["baseline_profit"] for x in fhits
            ),
            "frozen_full_equal_baseline": sum(
                abs(x["frozen_realized_profit"] - x["baseline_profit"]) < 0.005 for x in fhits
            ),
            "avg_frozen_full_delta_on_hits": round(avg([
                x["frozen_realized_profit"] - x["baseline_profit"] for x in fhits
            ]) or 0.0, 4),
            "avg_frozen_post_hit_giveback_vs_baseline": round(avg([
                x["frozen_post_hit_mfe"] - x["baseline_profit"] for x in fhits
            ]) or 0.0, 4),
        })
    if devs:
        result.update({
            "dynamic_action_better_than_baseline": sum(
                x["dynamic_action_profit"] > x["baseline_profit"] for x in devs
            ),
            "dynamic_action_worse_than_baseline": sum(
                x["dynamic_action_profit"] < x["baseline_profit"] for x in devs
            ),
            "avg_dynamic_action_delta_on_events": round(avg([
                x["dynamic_action_profit"] - x["baseline_profit"] for x in devs
            ]) or 0.0, 4),
            "avg_dynamic_post_event_giveback_vs_baseline": round(avg([
                x["dynamic_post_event_mfe"] - x["baseline_profit"] for x in devs
            ]) or 0.0, 4),
        })
    if devs_no_momentum:
        result.update({
            "dynamic_nm_better_than_baseline": sum(
                x["dynamic_action_profit"] > x["baseline_profit"] for x in devs_no_momentum
            ),
            "dynamic_nm_worse_than_baseline": sum(
                x["dynamic_action_profit"] < x["baseline_profit"] for x in devs_no_momentum
            ),
            "avg_dynamic_nm_action_delta": round(avg([
                x["dynamic_action_profit"] - x["baseline_profit"] for x in devs_no_momentum
            ]) or 0.0, 4),
        })
    for fraction in FRACTIONS:
        pct = int(fraction * 100)
        for mode in ("frozen", "dynamic", "dynamic_nm"):
            total = sum(x[f"{mode}_cf_{pct}"] for x in rows)
            result[f"{mode}_cf_{pct}_profit"] = round(total, 2)
            result[f"{mode}_cf_{pct}_delta"] = round(total - baseline, 2)
    return result

def epoch(value: datetime) -> int:
    return calendar.timegm(value.timetuple())


def load_m1_compact(path: Path, expected_hash: str, min_time: datetime) -> tuple[array, array, array]:
    if sha256(path) != expected_hash:
        raise RuntimeError(f"HST hash mismatch: {path}")
    times = array("q")
    highs = array("d")
    lows = array("d")
    min_epoch = epoch(min_time)
    with path.open("rb") as f:
        header = f.read(148)
        if len(header) != 148 or header[:4] != struct.pack("<I", 401):
            raise RuntimeError(f"unsupported HST format: {path}")
        while True:
            chunk = f.read(60)
            if len(chunk) < 60:
                break
            ts, _opn, high, low, _close, _tv, _spread, _rv = struct.unpack(
                "<qddddqiq", chunk
            )
            if ts < min_epoch:
                continue
            times.append(ts)
            highs.append(high)
            lows.append(low)
    return times, highs, lows

def verify_artifact(path: Path, expected: str) -> dict:
    actual = sha256(path)
    if actual != expected:
        raise RuntimeError(f"artifact hash mismatch {path}: expected={expected} actual={actual}")
    return {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}


def manifest_hashes(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        Path(item["path"]).name: item["sha256"].upper()
        for item in data["files"]
    }


def grouped_summaries(rows: list[dict]) -> dict:
    out = {"ALL_H1_H4": summarize(rows)}
    for tf, label in ((60, "H1"), (240, "H4")):
        subset = [x for x in rows if x["owner_tf"] == tf]
        out[label] = summarize(subset)
        for period in PERIODS:
            out[f"{label}_{period}"] = summarize([
                x for x in subset if x["period"] == period
            ])
    for period in PERIODS:
        out[period] = summarize([x for x in rows if x["period"] == period])
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--history-root",
        type=Path,
        default=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\history\MetaQuotes-Demo"),
    )
    ap.add_argument(
        "--evidence-root",
        type=Path,
        default=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\Q8_BUILD486_GBPUSD_20260918"),
    )
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "audits" / "evidence" / "Q8_BUILD486_GBPUSD_20260918"
        / "local_evidence_manifest.json",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=Path(r"D:\BBMA\OUTERBB_VALUE_289"),
    )
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    expected = manifest_hashes(args.manifest)
    evidence_identity = {}

    m1_path = args.history_root / "GBPUSD1.hst"
    h1_path = args.history_root / "GBPUSD60.hst"
    h4_path = args.history_root / "GBPUSD240.hst"
    m1 = load_m1_compact(m1_path, HST_SHA[1], datetime(2023, 12, 1))
    h1 = load_hst(h1_path, HST_SHA[60])
    h4 = load_hst(h4_path, HST_SHA[240])
    owner_data = {60: h1, 240: h4}
    owner_bands = {60: bollinger(*h1), 240: bollinger(*h4)}
    evidence_identity["GBPUSD1.hst"] = {
        "path": str(m1_path), "sha256": HST_SHA[1], "rows_loaded": len(m1[0])
    }
    evidence_identity["GBPUSD60.hst"] = {
        "path": str(h1_path), "sha256": HST_SHA[60], "rows_loaded": len(h1[0])
    }
    evidence_identity["GBPUSD240.hst"] = {
        "path": str(h4_path), "sha256": HST_SHA[240], "rows_loaded": len(h4[0])
    }
    all_rows: list[dict] = []
    period_meta = {}
    for period in PERIODS:
        report = args.evidence_root / f"{period}.html"
        log = args.evidence_root / f"{period}_tester_newlog.bin"
        evidence_identity[report.name] = verify_artifact(report, expected[report.name])
        evidence_identity[log.name] = verify_artifact(log, expected[log.name])
        rows, meta = analyze_period(
            period, report, log, m1, owner_data, owner_bands
        )
        all_rows.extend(rows)
        period_meta[period] = meta

    pnl_diffs = [
        abs(pnl(x["side"], x["entry"], x["close"], x["lot"]) - x["baseline_profit"])
        for x in all_rows
    ]
    result = {
        "classification": "ENGINEERING COUNTERFACTUAL / NOT BBMA CORE / NO EXECUTION AUTHORITY",
        "baseline": "Q8 Build 4.86 GBPUSD verified engineering historical profile",
        "scope": "C044-managed H1 and H4 Re-Entry owners only",
        "method": {
            "frozen": "owner-TF outer BB(20,2) on exact Re-Entry confirmation candle; first post-entry M1 structural hit",
            "dynamic": "first fully post-entry closed owner-TF candle whose own range touches its own outer BB; action at that candle close",
            "dynamic_nm": "same dynamic event, but hypothetical realization is suppressed when that exact owner candle emits canonical same-direction MOMENTUM_HOLD",
            "sell_execution": "structural Bid reference plus fixed 20-point Strategy Tester spread for hypothetical SELL close",
            "partial": "25/50/75/100% hypothetical realization; un-realized remainder keeps exact baseline close outcome",
        },
        "period_meta": period_meta,
        "integrity": {
            "included_rows": len(all_rows),
            "max_report_pnl_recalc_abs_diff": round(max(pnl_diffs) if pnl_diffs else 0.0, 6),
            "signal_counts": dict(sorted({
                s: sum(x["signal"] == s for x in all_rows)
                for s in {x["signal"] for x in all_rows}
            }.items())),
            "owner_tf_counts": {
                str(tf): sum(x["owner_tf"] == tf for x in all_rows)
                for tf in (60, 240)
            },
        },
        "summaries": grouped_summaries(all_rows),
        "evidence_identity": evidence_identity,
    }

    (args.output / "OUTERBB_VALUE_RESULT.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    (args.output / "OUTERBB_VALUE_TRADE_ROWS.json").write_text(
        json.dumps(all_rows, indent=2), encoding="utf-8"
    )
    print(json.dumps({
        "classification": result["classification"],
        "integrity": result["integrity"],
        "H1": result["summaries"]["H1"],
        "H4": result["summaries"]["H4"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
