#!/usr/bin/env python3
"""Extract canonical N2 closed-outcome shadow records from MT4 logs.

Research/diagnostic only. It converts `[N2-NMJE-OUT]` records with a full
DecisionID into the exact DecisionID CSV consumed by n2_nmje_outcome_attributor.py.
N2 telemetry encodes spaces inside DecisionID as `~` so each diagnostic field
remains one log token; this parser restores the original DecisionID before
identity attribution. Hash-only recovered outcomes are surfaced separately and
are never silently promoted to a full DecisionID.

Usage:
  python blueprint/tools/n2_nmje_outcome_log_extractor.py logs/*.log \
      --csv outcomes.csv --json extraction.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

OUT_RE = re.compile(
    r"\[N2-NMJE-OUT\]\s+"
    r"PAIR=(?P<pair>\S+)\s+"
    r"TICKET=(?P<ticket>\d+)\s+"
    r"DID=(?P<decision_id>\S+)\s+"
    r"DIDH=(?P<decision_hash>\S+)\s+"
    r"NET=(?P<net_profit>[-+]?\d+(?:\.\d+)?)\s+"
    r"CLOSE=(?P<close_time>\d+)\s+"
    r"REC=(?P<recovery_state>\S+)"
)


def decode_identity_token(token: str) -> str:
    if token == "-":
        return token
    return token.replace("~", " ")


@dataclass(frozen=True)
class OutcomeRecord:
    file: str
    line_no: int
    pair: str
    ticket: int
    decision_id: str
    decision_hash: str
    net_profit: float
    close_time: int
    recovery_state: str


def parse_logs(paths: Iterable[Path]) -> list[OutcomeRecord]:
    records: list[OutcomeRecord] = []
    for path in paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                match = OUT_RE.search(line)
                if not match:
                    continue
                gd = match.groupdict()
                records.append(
                    OutcomeRecord(
                        file=str(path),
                        line_no=line_no,
                        pair=gd["pair"],
                        ticket=int(gd["ticket"]),
                        decision_id=decode_identity_token(gd["decision_id"]),
                        decision_hash=gd["decision_hash"],
                        net_profit=float(gd["net_profit"]),
                        close_time=int(gd["close_time"]),
                        recovery_state=gd["recovery_state"],
                    )
                )
    return records


def analyze(records: list[OutcomeRecord]) -> dict:
    ticket_counts = Counter(r.ticket for r in records)
    did_counts = Counter(r.decision_id for r in records if r.decision_id != "-")
    exact = [r for r in records if r.decision_id != "-"]
    hash_only = [r for r in records if r.decision_id == "-"]

    duplicate_tickets = sorted(ticket for ticket, count in ticket_counts.items() if count > 1)
    duplicate_decision_ids = sorted(did for did, count in did_counts.items() if count > 1)

    valid_exact = [
        r for r in exact
        if r.ticket not in duplicate_tickets and r.decision_id not in duplicate_decision_ids
    ]

    return {
        "record_count": len(records),
        "exact_decision_outcomes": len(exact),
        "hash_only_outcomes": len(hash_only),
        "valid_exact_outcomes": len(valid_exact),
        "duplicate_tickets": duplicate_tickets,
        "duplicate_decision_ids": duplicate_decision_ids,
        "hash_only_rows": [asdict(r) for r in hash_only],
        "valid_exact_rows": [asdict(r) for r in valid_exact],
        "all_rows": [asdict(r) for r in records],
    }


def write_exact_csv(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "decision_id", "net_profit", "ticket", "close_time", "pair",
        "decision_hash", "recovery_state",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in report["valid_exact_rows"]:
            writer.writerow({key: row[key] for key in fieldnames})


def print_report(report: dict) -> None:
    print("N2 NMJE OUTCOME LOG EXTRACTION")
    print("==============================")
    print(f"Outcome records       : {report['record_count']}")
    print(f"Exact DecisionID      : {report['exact_decision_outcomes']}")
    print(f"Hash-only recovered   : {report['hash_only_outcomes']}")
    print(f"Valid exact outcomes  : {report['valid_exact_outcomes']}")
    print(f"Duplicate tickets     : {len(report['duplicate_tickets'])}")
    print(f"Duplicate DecisionIDs : {len(report['duplicate_decision_ids'])}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="+", type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing = [str(path) for path in args.logs if not path.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))

    report = analyze(parse_logs(args.logs))
    write_exact_csv(args.csv, report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print_report(report)

    if report["duplicate_tickets"] or report["duplicate_decision_ids"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
