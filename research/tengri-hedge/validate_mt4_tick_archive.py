#!/usr/bin/env python3
"""Validate the locked HFM MT4 Bid/Ask tick files before replay.

Expected CSV columns are the ones written by MT4_TickCapture_Research.mq4:
timestamp_utc,server_time,server_utc_offset_seconds,bid,ask,symbol,server,
company,platform,terminal_build,is_demo.

This checks file integrity, quote validity, metadata consistency, timezone
conversion, warm-up sessions, and evaluation-day coverage. It cannot prove
that a CSV came from a broker; preserve the MT4 terminal logs and file hashes
as separate provenance evidence. A passing result is a data-quality gate only.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


EXPECTED_SERVER = "HFMarketsSV-Demo Server"
EXPECTED_PLATFORM = "MT4"
WARMUP_START_UTC = dt.datetime(2026, 2, 1, tzinfo=dt.timezone.utc)
EVAL_START_UTC = dt.datetime(2026, 5, 1, tzinfo=dt.timezone.utc)
EVAL_END_UTC = dt.datetime(2026, 11, 18, 23, 59, 59, tzinfo=dt.timezone.utc)
MIN_WARMUP_D1_SESSIONS = 51
MAX_ENTRY_SPREAD_PIPS = 3.0
HFM_UTC_OFFSETS = {7200, 10800}  # HFM winter GMT+2 / summer GMT+3.


def parse_utc(value: str) -> dt.datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    stamp = dt.datetime.fromisoformat(value)
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("timestamp_utc must include Z or an explicit UTC offset")
    return stamp.astimezone(dt.timezone.utc)


def parse_server_wall_time(value: str, zone: ZoneInfo) -> dt.datetime:
    value = value.strip()
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(value, fmt)
        except ValueError:
            pass
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return parsed
    return parsed.astimezone(zone).replace(tzinfo=None)


def valid_zone_offsets(wall_time: dt.datetime, zone: ZoneInfo) -> set[int]:
    """Return valid offsets, handling the repeated hour at the autumn DST change."""
    offsets: set[int] = set()
    for fold in (0, 1):
        aware = wall_time.replace(tzinfo=zone, fold=fold)
        round_trip = aware.astimezone(dt.timezone.utc).astimezone(zone).replace(tzinfo=None)
        if round_trip == wall_time:
            offsets.add(int(aware.utcoffset().total_seconds()))
    return offsets


def weekdays(start: dt.date, end: dt.date) -> set[dt.date]:
    days: set[dt.date] = set()
    day = start
    while day <= end:
        if day.weekday() < 5:
            days.add(day)
        day += dt.timedelta(days=1)
    return days


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "demo"}


def matches_pair(actual: str, expected: str) -> bool:
    # Allows a broker suffix such as EURUSD.a while keeping the base pair exact.
    actual = actual.strip().upper()
    expected = expected.strip().upper()
    return actual == expected or actual.startswith(expected + ".") or actual.startswith(expected + "_") or actual.startswith(expected + "+")


def inspect_csv(
    path: Path,
    symbol: str,
    zone: ZoneInfo,
    source_server: str,
    warmup_start: dt.datetime,
    eval_start: dt.datetime,
    eval_end: dt.datetime,
    min_warmup_sessions: int,
    max_entry_spread_pips: float,
) -> dict:
    errors: list[str] = []
    row_examples: list[str] = []
    counters = Counter()
    eval_dates: set[dt.date] = set()
    warmup_dates: set[dt.date] = set()
    first_utc: dt.datetime | None = None
    last_utc: dt.datetime | None = None
    previous_utc: dt.datetime | None = None
    max_same_server_day_gap = 0.0
    gaps_over_5m = gaps_over_15m = gaps_over_30m = 0
    min_spread = math.inf
    max_spread = 0.0
    spread_over_cap = 0
    valid_rows = 0
    out_of_order = 0

    if not path.is_file():
        return {"symbol": symbol, "path": str(path), "status": "HOLD", "errors": [f"file not found: {path}"]}

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                return {"symbol": symbol, "path": str(path), "status": "HOLD", "errors": ["CSV has no header"]}
            columns = {name.strip().lower(): name for name in reader.fieldnames if name}
            required = {
                "timestamp_utc", "server_time", "server_utc_offset_seconds", "bid", "ask",
                "symbol", "server", "platform", "is_demo",
            }
            missing_columns = sorted(required - columns.keys())
            if missing_columns:
                return {"symbol": symbol, "path": str(path), "status": "HOLD",
                        "errors": ["missing required columns: " + ", ".join(missing_columns)]}

            for line_no, row in enumerate(reader, start=2):
                try:
                    stamp = parse_utc(row.get(columns["timestamp_utc"], ""))
                    server_time = parse_server_wall_time(row.get(columns["server_time"], ""), zone)
                    offset = int(row.get(columns["server_utc_offset_seconds"], ""))
                    bid = float(row.get(columns["bid"], ""))
                    ask = float(row.get(columns["ask"], ""))
                    actual_symbol = row.get(columns["symbol"], "")
                    actual_server = row.get(columns["server"], "").strip()
                    actual_platform = row.get(columns["platform"], "").strip().upper()
                    demo = truthy(row.get(columns["is_demo"], ""))

                    if not matches_pair(actual_symbol, symbol):
                        raise ValueError(f"symbol is {actual_symbol!r}; expected {symbol} with optional suffix")
                    if actual_server != source_server:
                        raise ValueError(f"server is {actual_server!r}; expected {source_server!r}")
                    if actual_platform != EXPECTED_PLATFORM:
                        raise ValueError(f"platform is {actual_platform!r}; expected MT4")
                    if not demo:
                        raise ValueError("capture is not marked as a demo account")
                    if not math.isfinite(bid) or not math.isfinite(ask) or bid <= 0 or ask < bid:
                        raise ValueError("invalid Bid/Ask quote")
                    expected_offsets = valid_zone_offsets(server_time, zone)
                    if not expected_offsets or not expected_offsets.issubset(HFM_UTC_OFFSETS):
                        raise ValueError(f"server_time is invalid for HFM timezone {zone.key}")
                    if offset not in expected_offsets:
                        raise ValueError(f"row offset {offset} disagrees with {zone.key} offsets {sorted(expected_offsets)}")
                    derived_utc = (server_time - dt.timedelta(seconds=offset)).replace(tzinfo=dt.timezone.utc)
                    if abs((derived_utc - stamp).total_seconds()) > 1:
                        raise ValueError("timestamp_utc does not match server_time and server timezone")
                except (ValueError, TypeError, OverflowError) as exc:
                    counters["invalid_rows"] += 1
                    if len(row_examples) < 10:
                        row_examples.append(f"line {line_no}: {exc}")
                    continue

                valid_rows += 1
                local_day = stamp.astimezone(zone).date()
                first_utc = stamp if first_utc is None else min(first_utc, stamp)
                last_utc = stamp if last_utc is None else max(last_utc, stamp)
                if previous_utc is not None:
                    gap = (stamp - previous_utc).total_seconds()
                    if gap < 0:
                        out_of_order += 1
                    elif gap == 0:
                        counters["duplicate_timestamps"] += 1
                    if local_day == previous_utc.astimezone(zone).date() and gap > 0:
                        max_same_server_day_gap = max(max_same_server_day_gap, gap)
                        gaps_over_5m += gap > 300
                        gaps_over_15m += gap > 900
                        gaps_over_30m += gap > 1800
                previous_utc = stamp

                spread = (ask - bid) * 10000.0
                min_spread = min(min_spread, spread)
                max_spread = max(max_spread, spread)
                spread_over_cap += spread > max_entry_spread_pips
                if eval_start <= stamp <= eval_end:
                    eval_dates.add(local_day)
                elif warmup_start <= stamp < eval_start and local_day.weekday() < 5:
                    warmup_dates.add(local_day)
    except OSError as exc:
        return {"symbol": symbol, "path": str(path), "status": "HOLD", "errors": [f"could not read file: {exc}"]}

    eval_start_local = eval_start.astimezone(zone).date()
    eval_end_local = eval_end.astimezone(zone).date()
    expected_eval = weekdays(eval_start_local, eval_end_local)
    missing_eval = sorted(expected_eval - eval_dates)
    if valid_rows == 0:
        errors.append("no valid quotes")
    if out_of_order:
        errors.append(f"{out_of_order} out-of-order timestamps")
    if counters["invalid_rows"]:
        errors.append(f"{counters['invalid_rows']} invalid rows")
    if len(warmup_dates) < min_warmup_sessions:
        errors.append(f"only {len(warmup_dates)} warm-up D1 sessions; need {min_warmup_sessions}")
    if missing_eval:
        errors.append(f"{len(missing_eval)} evaluation weekdays missing")
    if last_utc is None or last_utc.astimezone(zone).date() < eval_end_local:
        errors.append("history does not reach the configured final evaluation date")

    return {
        "symbol": symbol,
        "path": str(path),
        "sha256": sha256_file(path),
        "valid_rows": valid_rows,
        "first_utc": first_utc.isoformat() if first_utc else None,
        "last_utc": last_utc.isoformat() if last_utc else None,
        "warmup_d1_sessions": len(warmup_dates),
        "evaluation_weekdays_expected": len(expected_eval),
        "evaluation_weekdays_covered": len(expected_eval & eval_dates),
        "missing_evaluation_weekdays": [day.isoformat() for day in missing_eval],
        "duplicate_timestamps": counters["duplicate_timestamps"],
        "out_of_order_timestamps": out_of_order,
        "invalid_rows": counters["invalid_rows"],
        "spread_pips": {
            "minimum": None if not math.isfinite(min_spread) else min_spread,
            "maximum": max_spread,
            "quotes_over_entry_cap": spread_over_cap,
            "entry_cap_pips": max_entry_spread_pips,
        },
        "same_server_day_gaps": {
            "maximum_seconds": max_same_server_day_gap,
            "over_5_minutes": gaps_over_5m,
            "over_15_minutes": gaps_over_15m,
            "over_30_minutes": gaps_over_30m,
        },
        "row_error_examples": row_examples,
        "status": "PASS" if not errors else "HOLD",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eurusd", required=True, type=Path)
    parser.add_argument("--usdchf", required=True, type=Path)
    parser.add_argument("--source-server", required=True)
    parser.add_argument("--server-timezone", required=True, help="IANA zone; HFM GMT+2/+3 corresponds to Europe/Helsinki")
    parser.add_argument("--warmup-start-utc", type=parse_utc, default=WARMUP_START_UTC)
    parser.add_argument("--eval-start-utc", type=parse_utc, default=EVAL_START_UTC)
    parser.add_argument("--eval-end-utc", type=parse_utc, default=EVAL_END_UTC)
    parser.add_argument("--min-warmup-sessions", type=int, default=MIN_WARMUP_D1_SESSIONS)
    parser.add_argument("--max-entry-spread-pips", type=float, default=MAX_ENTRY_SPREAD_PIPS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if args.source_server != EXPECTED_SERVER:
        print(json.dumps({"status": "HOLD", "errors": [f"source server must be {EXPECTED_SERVER!r}"]}, indent=2))
        return 2
    if args.eval_end_utc < args.eval_start_utc or args.warmup_start_utc >= args.eval_start_utc:
        print(json.dumps({"status": "HOLD", "errors": ["invalid date window"]}, indent=2))
        return 2
    try:
        zone = ZoneInfo(args.server_timezone)
    except ZoneInfoNotFoundError:
        print(json.dumps({"status": "HOLD", "errors": [f"unknown timezone {args.server_timezone!r}"]}, indent=2))
        return 2

    pairs = [
        inspect_csv(args.eurusd, "EURUSD", zone, args.source_server, args.warmup_start_utc, args.eval_start_utc,
                    args.eval_end_utc, args.min_warmup_sessions, args.max_entry_spread_pips),
        inspect_csv(args.usdchf, "USDCHF", zone, args.source_server, args.warmup_start_utc, args.eval_start_utc,
                    args.eval_end_utc, args.min_warmup_sessions, args.max_entry_spread_pips),
    ]
    result = {
        "schema_version": 2,
        "status": "PASS_DATA_QA_ONLY" if all(p["status"] == "PASS" for p in pairs) else "HOLD",
        "source": {
            "server_label_expected": args.source_server,
            "platform_expected": EXPECTED_PLATFORM,
            "server_timezone": args.server_timezone,
            "price_data_type": "MT4 OnTick Bid/Ask observations",
            "provenance_limit": "CSV metadata and hashes do not cryptographically prove broker origin; preserve terminal evidence separately.",
        },
        "window_utc": {
            "warmup_start": args.warmup_start_utc.isoformat(),
            "evaluation_start": args.eval_start_utc.isoformat(),
            "evaluation_end": args.eval_end_utc.isoformat(),
        },
        "gates": {
            "minimum_warmup_d1_sessions": args.min_warmup_sessions,
            "all_evaluation_weekdays_covered": True,
            "HFM_offsets_seconds": sorted(HFM_UTC_OFFSETS),
            "not_a_profitability_or_execution_validation": True,
        },
        "pairs": pairs,
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)
    print(rendered)
    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS_DATA_QA_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
