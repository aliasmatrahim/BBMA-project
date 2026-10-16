from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import math

VALIDATOR_VERSION = "G1-DATASET-VALIDATOR-1.0"
_TIMEFRAMES = {
    "M1": 60, "M5": 300, "M15": 900, "M30": 1800,
    "H1": 3600, "H4": 14400, "D1": 86400,
}
_BAR_FIELDS = (
    "bid_open", "bid_high", "bid_low", "bid_close",
    "ask_open", "ask_high", "ask_low", "ask_close",
)


def _time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _number(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _allowed_gap(start: datetime, end: datetime, windows: list[dict[str, Any]]) -> bool:
    for window in windows:
        left = _time(window.get("start"))
        right = _time(window.get("end"))
        if left is not None and right is not None and left <= start and end <= right and left < right:
            return True
    return False


def validate_dataset_file(
    dataset_path: str | Path,
    manifest: dict[str, Any],
    *,
    max_gap_seconds: int | None = None,
) -> dict[str, Any]:
    """Validate raw Bid/Ask tick or bar CSV data; no repair/interpolation is performed."""
    path = Path(dataset_path)
    dataset = manifest.get("dataset") if isinstance(manifest, dict) else None
    run_id = manifest.get("run_id") if isinstance(manifest, dict) else None
    build = manifest.get("build", {}) if isinstance(manifest, dict) else {}
    hypothesis = manifest.get("hypothesis", {}) if isinstance(manifest, dict) else {}
    errors: list[str] = []
    if not isinstance(dataset, dict):
        return {
            "validator_version": VALIDATOR_VERSION, "validation_status": "FAIL",
            "dataset_status": "INVALID_DATA", "run_id": run_id, "errors": ["dataset: expected object"],
        }

    expected_digest = str(dataset.get("sha256", "")).lower()
    actual_digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
    if not path.is_file():
        errors.append("dataset_file: missing")
    elif expected_digest != actual_digest:
        errors.append("dataset.sha256: dataset file hash mismatch")

    timeframe = dataset.get("timeframe")
    interval = _TIMEFRAMES.get(str(timeframe))
    if interval is None:
        errors.append("dataset.timeframe: unsupported timeframe for alignment validation")
        interval = 0
    for field in ("dataset_id", "source_type", "timezone", "symbol"):
        if not isinstance(dataset.get(field), str) or not dataset.get(field, "").strip():
            errors.append(f"dataset.{field}: required non-empty string")
    basis = dataset.get("price_basis")
    source_type = str(dataset.get("source_type", "")).strip().lower()
    if dataset.get("synthetic_ticks") is not False:
        errors.append("dataset.synthetic_ticks: reconstructed/synthetic ticks are not accepted")
    if any(term in source_type for term in ("synthetic", "reconstructed", "interpolated", "generated tick", "simulated tick")):
        errors.append("dataset.source_type: synthetic/reconstructed tick data is not accepted")
    convention = dataset.get("timestamp_convention")
    if basis == "BID_ASK_BARS" and convention != "BAR_OPEN":
        errors.append("dataset.timestamp_convention: BID_ASK_BARS requires BAR_OPEN timestamps")
    if basis == "BID_ASK_TICKS" and convention != "TICK_TIME":
        errors.append("dataset.timestamp_convention: BID_ASK_TICKS requires TICK_TIME")
    if dataset.get("closed_candles_only") is not True:
        errors.append("dataset.closed_candles_only: must be true")
    if basis not in {"BID_ASK_TICKS", "BID_ASK_BARS"}:
        errors.append("dataset.price_basis: expected BID_ASK_TICKS or BID_ASK_BARS")
    declared_gap = dataset.get("max_gap_seconds")
    if basis == "BID_ASK_TICKS":
        if isinstance(declared_gap, bool) or not isinstance(declared_gap, int) or declared_gap <= 0:
            errors.append("dataset.max_gap_seconds: preregister a positive integer for tick gap validation")
        elif max_gap_seconds is not None and max_gap_seconds != declared_gap:
            errors.append("max_gap_seconds: CLI value differs from preregistered dataset.max_gap_seconds")
        else:
            max_gap_seconds = declared_gap
    if max_gap_seconds is not None and (isinstance(max_gap_seconds, bool) or not isinstance(max_gap_seconds, int) or max_gap_seconds <= 0):
        errors.append("max_gap_seconds: must be a positive integer")
    windows = dataset.get("allowed_gap_windows", [])
    if not isinstance(windows, list) or any(not isinstance(w, dict) for w in windows):
        errors.append("dataset.allowed_gap_windows: expected list of start/end objects")
        windows = []
    else:
        for index, window in enumerate(windows):
            left, right = _time(window.get("start")), _time(window.get("end"))
            if left is None or right is None or left >= right:
                errors.append(f"dataset.allowed_gap_windows[{index}]: expected timezone-aware start < end")
    start = _time(dataset.get("start"))
    end = _time(dataset.get("end"))
    warmup = _time(dataset.get("warmup_start"))
    eval_start = _time(dataset.get("evaluation_start"))
    eval_end = _time(dataset.get("evaluation_end"))
    as_of = _time(dataset.get("data_as_of"))
    for name, value in (("start", start), ("end", end), ("warmup_start", warmup),
                        ("evaluation_start", eval_start), ("evaluation_end", eval_end),
                        ("data_as_of", as_of)):
        if value is None:
            errors.append(f"dataset.{name}: expected timezone-aware ISO-8601 timestamp")
    if all(v is not None for v in (warmup, start, eval_start, eval_end, end)):
        if not (warmup <= start <= eval_start < eval_end <= end):
            errors.append("dataset: invalid warm-up/start/evaluation/end chronology")
    if interval and eval_start and eval_end:
        if int(eval_start.timestamp()) % interval or int(eval_end.timestamp()) % interval:
            errors.append("dataset: evaluation window is not aligned to closed-candle timeframe boundaries")
    if eval_end and as_of and as_of < eval_end:
        errors.append("dataset.data_as_of: evaluation end has not closed at the declared data-as-of time")

    rows: list[tuple[int, datetime, dict[str, str]]] = []
    if path.is_file():
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                field_list = reader.fieldnames or []
                fields = set(field_list)
                if len(field_list) != len(fields):
                    errors.append("dataset.columns: duplicate column names")
                required = {"timestamp", "bid", "ask"} if basis == "BID_ASK_TICKS" else {"timestamp", *_BAR_FIELDS}
                missing = sorted(required - fields)
                if missing:
                    errors.append("dataset.columns: missing " + ", ".join(missing))
                else:
                    for line_no, row in enumerate(reader, start=2):
                        ts = _time(row.get("timestamp"))
                        if ts is None:
                            errors.append(f"line {line_no}: timestamp must be timezone-aware ISO-8601")
                            continue
                        rows.append((line_no, ts, row))
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            errors.append(f"dataset.csv: cannot read ({type(exc).__name__})")

    if not rows:
        errors.append("dataset: no valid data rows")

    duplicates = 0
    non_monotonic = 0
    gaps: list[dict[str, Any]] = []
    previous: tuple[int, datetime, dict[str, str]] | None = None
    for line_no, ts, row in rows:
        if basis == "BID_ASK_BARS" and interval and int(ts.timestamp()) % interval:
            errors.append(f"line {line_no}: timestamp is not aligned to {timeframe} boundary")
        if basis == "BID_ASK_TICKS":
            bid, ask = _number(row.get("bid")), _number(row.get("ask"))
            if bid is None or ask is None or bid <= 0 or ask <= 0:
                errors.append(f"line {line_no}: Bid/Ask must be finite positive numbers")
            elif ask < bid:
                errors.append(f"line {line_no}: Ask is below Bid")
        elif basis == "BID_ASK_BARS":
            values = {name: _number(row.get(name)) for name in _BAR_FIELDS}
            if any(value is None or value <= 0 for value in values.values()):
                errors.append(f"line {line_no}: Bid/Ask OHLC must be finite positive numbers")
            else:
                for side in ("bid", "ask"):
                    o, h, low, close = (values[f"{side}_{part}"] for part in ("open", "high", "low", "close"))
                    if h < max(o, close, low) or low > min(o, close, h):
                        errors.append(f"line {line_no}: inconsistent {side.upper()} OHLC")
                if any(values[f"ask_{part}"] < values[f"bid_{part}"] for part in ("open", "high", "low", "close")):
                    errors.append(f"line {line_no}: Ask OHLC is below corresponding Bid OHLC")
        if previous is not None:
            prev_line, prev_ts, _ = previous
            delta = (ts - prev_ts).total_seconds()
            if delta == 0:
                duplicates += 1
                errors.append(f"line {line_no}: duplicate timestamp with line {prev_line}")
            elif delta < 0:
                non_monotonic += 1
                errors.append(f"line {line_no}: timestamp is not strictly increasing after line {prev_line}")
            else:
                gap_threshold = interval if basis == "BID_ASK_BARS" else (max_gap_seconds or interval)
                if gap_threshold and delta > gap_threshold:
                    gap = {"from": prev_ts.isoformat(), "to": ts.isoformat(), "seconds": int(delta)}
                    gaps.append(gap)
                    if not _allowed_gap(prev_ts, ts, windows):
                        errors.append(f"timestamp gap {int(delta)}s from {prev_ts.isoformat()} to {ts.isoformat()}")
        previous = (line_no, ts, row)

    if rows and start and end:
        first, last = rows[0][1], rows[-1][1]
        if first < start or last > end:
            errors.append("dataset: row timestamps fall outside declared data start/end")
        if eval_start and first > eval_start:
            errors.append("dataset: data does not cover evaluation_start")
        if eval_end and last < eval_end - (interval or 0):
            errors.append("dataset: data does not cover through the final closed evaluation candle")
    if basis == "BID_ASK_BARS" and rows and as_of and interval:
        last_ts = rows[-1][1]
        if last_ts.timestamp() + interval > as_of.timestamp():
            errors.append("dataset: final bar is not confirmed closed by data_as_of")

    result = {
        "validator_version": VALIDATOR_VERSION,
        "validation_status": "PASS" if not errors else "FAIL",
        "dataset_status": "VALID" if not errors else "INVALID_DATA",
        "run_id": run_id,
        "build_id": build.get("build_id") if isinstance(build, dict) else None,
        "dataset_sha256": actual_digest or None,
        "parameter_sha256": hypothesis.get("parameter_sha256") if isinstance(hypothesis, dict) else None,
        "price_basis": basis,
        "timeframe": timeframe,
        "rows": len(rows),
        "duplicate_timestamps": duplicates,
        "non_monotonic_timestamps": non_monotonic,
        "gap_count": len(gaps),
        "gaps": gaps,
        "errors": errors,
    }
    return result


def write_dataset_validation_report(
    dataset_path: str | Path,
    manifest: dict[str, Any],
    output_path: str | Path,
    *,
    max_gap_seconds: int | None = None,
) -> dict[str, Any]:
    result = validate_dataset_file(dataset_path, manifest, max_gap_seconds=max_gap_seconds)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
