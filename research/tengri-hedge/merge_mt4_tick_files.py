#!/usr/bin/env python3
"""Concatenate daily MT4 capture CSVs without changing quote fields."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import tempfile
from pathlib import Path


FIELDS = [
    "timestamp_utc", "server_time", "server_utc_offset_seconds", "bid", "ask",
    "symbol", "server", "company", "platform", "terminal_build", "is_demo",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def utc_stamp(value: str) -> dt.datetime:
    stamp = dt.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError(f"timestamp has no timezone: {value!r}")
    return stamp.astimezone(dt.timezone.utc)


def merge(symbol: str, input_dir: Path, output: Path) -> dict:
    files = sorted(input_dir.glob(f"{symbol}_*.csv"))
    if not files:
        raise FileNotFoundError(f"no {symbol} daily CSV files under {input_dir}")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=output.name + ".", suffix=".tmp", dir=output.parent)
    os.close(fd)
    rows = 0
    duplicates = 0
    first = last = None
    previous = None
    try:
        with Path(temp_name).open("w", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=FIELDS, extrasaction="raise", lineterminator="\n")
            writer.writeheader()
            for path in files:
                with path.open("r", encoding="utf-8-sig", newline="") as source:
                    reader = csv.DictReader(source)
                    if reader.fieldnames is None or [x.strip().lower() for x in reader.fieldnames] != FIELDS:
                        raise ValueError(f"unexpected CSV header in {path}")
                    for row in reader:
                        normalized = {key.strip().lower(): value for key, value in row.items() if key is not None}
                        if not normalized or any(normalized.get(key) is None for key in FIELDS):
                            raise ValueError(f"malformed row in {path}")
                        stamp = utc_stamp(normalized["timestamp_utc"])
                        if previous is not None and stamp < previous:
                            raise ValueError(f"files are not chronological at {path}; source files left unchanged")
                        if previous is not None and stamp == previous:
                            duplicates += 1
                        writer.writerow(normalized)
                        previous = stamp
                        first = stamp if first is None else min(first, stamp)
                        last = stamp if last is None else max(last, stamp)
                        rows += 1
        Path(temp_name).replace(output)
    except Exception:
        Path(temp_name).unlink(missing_ok=True)
        raise

    return {
        "symbol": symbol,
        "output": str(output),
        "output_sha256": sha256_file(output),
        "rows": rows,
        "first_utc": first.isoformat() if first else None,
        "last_utc": last.isoformat() if last else None,
        "duplicate_timestamps": duplicates,
        "source_files": [{"path": str(p), "sha256": sha256_file(p)} for p in files],
        "source_files_unchanged": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--symbol", required=True, choices=("EURUSD", "USDCHF"))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    result = merge(args.symbol, args.input_dir, args.out)
    manifest = args.out.with_suffix(args.out.suffix + ".manifest.json")
    manifest.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    result["manifest"] = str(manifest)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
