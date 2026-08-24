#!/usr/bin/env python3
"""Reconcile hash-only N2 closed outcomes to validated DecisionIDs, fail-closed.

Research/diagnostic only. This implements the existing MQL4 SHORT_HASH identity
algorithm and resolves a recovered `[N2-NMJE-OUT] DID=- DIDH=<hash>` only when
that hash maps to exactly one validated DecisionID in the analyzed N2
correlation dataset. Pair identity must also match. If `[N2-NMJE-DEC]` carries
DIDH, that logged hash must equal the locally reconstructed hash of the decoded
DecisionID. Collisions, mismatches, duplicates and ambiguous mappings are never
guessed.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

MASK64 = (1 << 64) - 1
MULTIPLIER = 1099511628211
HEX_DIGITS = "0123456789ABCDEF"


def mql4_short_hash(text: str, chars: int = 16) -> str:
    """Mirror BBMA_EA.mq4 SHORT_HASH for ASCII DecisionID payloads."""
    value = 0
    for ch in text:
        value = (value * MULTIPLIER + ord(ch)) & MASK64

    out: list[str] = []
    for _ in range(min(chars, 16)):
        out.append(HEX_DIGITS[value & 0xF])
        value >>= 4
    return "".join(out)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_decision_hash_index(correlation: dict) -> tuple[dict[str, list[dict]], list[str], list[dict]]:
    by_hash: dict[str, list[dict]] = defaultdict(list)
    seen_ids: set[str] = set()
    duplicate_ids: list[str] = []
    logged_hash_mismatches: list[dict] = []

    for row in correlation.get("rows", []):
        decision = (row or {}).get("decision") or {}
        did = str(decision.get("decision_id") or "").strip()
        if not did:
            continue
        if did in seen_ids:
            duplicate_ids.append(did)
        seen_ids.add(did)

        computed = mql4_short_hash(did)
        logged = str(decision.get("decision_hash") or "").strip()
        if logged and logged != computed:
            logged_hash_mismatches.append(
                {
                    "decision_id": did,
                    "pair": str(decision.get("pair") or ""),
                    "logged_hash": logged,
                    "computed_hash": computed,
                }
            )
            # Corrupted/mismatched telemetry must not participate in recovery.
            continue

        by_hash[computed].append(decision)

    return dict(by_hash), sorted(set(duplicate_ids)), logged_hash_mismatches


def reconcile(correlation: dict, extraction: dict) -> dict:
    by_hash, duplicate_correlation_ids, logged_hash_mismatches = build_decision_hash_index(correlation)

    exact_rows = list(extraction.get("valid_exact_rows") or [])
    hash_only_rows = list(extraction.get("hash_only_rows") or [])
    duplicate_tickets = set(extraction.get("duplicate_tickets") or [])
    duplicate_dids = set(extraction.get("duplicate_decision_ids") or [])

    exact_ids = {str(row.get("decision_id") or "") for row in exact_rows}
    exact_tickets = {int(row.get("ticket")) for row in exact_rows if row.get("ticket") is not None}

    reconciled: list[dict] = []
    unresolved: list[dict] = []
    collision_hashes: dict[str, list[str]] = {}
    seen_reconciled_ids: set[str] = set()
    seen_reconciled_tickets: set[int] = set()

    for raw in hash_only_rows:
        row = dict(raw)
        h = str(row.get("decision_hash") or "").strip()
        pair = str(row.get("pair") or "").strip()
        ticket = int(row.get("ticket") or 0)

        if not h:
            row["unresolved_reason"] = "MISSING_DECISION_HASH"
            unresolved.append(row)
            continue
        if ticket in duplicate_tickets:
            row["unresolved_reason"] = "DUPLICATE_TICKET_IN_EXTRACTION"
            unresolved.append(row)
            continue

        candidates = by_hash.get(h, [])
        if len(candidates) > 1:
            collision_hashes[h] = sorted(str(c.get("decision_id")) for c in candidates)
            row["unresolved_reason"] = "HASH_COLLISION"
            unresolved.append(row)
            continue
        if len(candidates) == 0:
            row["unresolved_reason"] = "HASH_NOT_FOUND_IN_VALIDATED_DECISIONS"
            unresolved.append(row)
            continue

        decision = candidates[0]
        did = str(decision.get("decision_id") or "")
        decision_pair = str(decision.get("pair") or "")
        if not did:
            row["unresolved_reason"] = "CANDIDATE_DECISION_ID_EMPTY"
            unresolved.append(row)
            continue
        if decision_pair != pair:
            row["unresolved_reason"] = "PAIR_IDENTITY_MISMATCH"
            row["candidate_decision_id"] = did
            row["candidate_pair"] = decision_pair
            unresolved.append(row)
            continue
        if did in duplicate_dids or did in duplicate_correlation_ids:
            row["unresolved_reason"] = "DUPLICATE_DECISION_ID"
            unresolved.append(row)
            continue
        if did in exact_ids or ticket in exact_tickets:
            row["unresolved_reason"] = "ALREADY_PRESENT_AS_EXACT_OUTCOME"
            unresolved.append(row)
            continue
        if did in seen_reconciled_ids or ticket in seen_reconciled_tickets:
            row["unresolved_reason"] = "DUPLICATE_RECONCILED_IDENTITY"
            unresolved.append(row)
            continue

        reconciled_row = dict(row)
        reconciled_row["decision_id"] = did
        reconciled_row["identity_provenance"] = "UNIQUE_SHORT_HASH_PLUS_PAIR"
        reconciled.append(reconciled_row)
        seen_reconciled_ids.add(did)
        seen_reconciled_tickets.add(ticket)

    combined = []
    for raw in exact_rows:
        row = dict(raw)
        row["identity_provenance"] = "FULL_DECISION_ID"
        combined.append(row)
    combined.extend(reconciled)

    did_counts = Counter(str(r.get("decision_id") or "") for r in combined)
    ticket_counts = Counter(int(r.get("ticket") or 0) for r in combined)
    combined_duplicate_dids = sorted(k for k, v in did_counts.items() if k and v > 1)
    combined_duplicate_tickets = sorted(k for k, v in ticket_counts.items() if k > 0 and v > 1)

    identity_valid = not (
        duplicate_correlation_ids
        or logged_hash_mismatches
        or collision_hashes
        or combined_duplicate_dids
        or combined_duplicate_tickets
    )

    return {
        "correlation_decision_count": sum(len(v) for v in by_hash.values()) + len(logged_hash_mismatches),
        "unique_hash_count": len(by_hash),
        "exact_outcome_count": len(exact_rows),
        "hash_only_input_count": len(hash_only_rows),
        "reconciled_hash_only_count": len(reconciled),
        "combined_outcome_count": len(combined),
        "identity_valid": identity_valid,
        "duplicate_correlation_decision_ids": duplicate_correlation_ids,
        "logged_decision_hash_mismatches": logged_hash_mismatches,
        "collision_hashes": collision_hashes,
        "combined_duplicate_decision_ids": combined_duplicate_dids,
        "combined_duplicate_tickets": combined_duplicate_tickets,
        "unresolved_hash_only_rows": unresolved,
        "reconciled_rows": reconciled,
        "combined_rows": combined,
    }


def write_csv(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "decision_id", "net_profit", "ticket", "close_time", "pair",
        "decision_hash", "recovery_state", "identity_provenance",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in report["combined_rows"]:
            writer.writerow({key: row.get(key, "") for key in fields})


def print_report(report: dict) -> None:
    print("N2 NMJE HASH IDENTITY RECONCILIATION")
    print("====================================")
    print(f"Validated DecisionIDs : {report['correlation_decision_count']}")
    print(f"Exact outcomes        : {report['exact_outcome_count']}")
    print(f"Hash-only inputs      : {report['hash_only_input_count']}")
    print(f"Hash reconciled       : {report['reconciled_hash_only_count']}")
    print(f"Combined outcomes     : {report['combined_outcome_count']}")
    print(f"Unresolved hash-only  : {len(report['unresolved_hash_only_rows'])}")
    print(f"DIDH mismatches       : {len(report['logged_decision_hash_mismatches'])}")
    print(f"Hash collisions       : {len(report['collision_hashes'])}")
    print(f"Identity valid        : {'YES' if report['identity_valid'] else 'NO'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("correlation_json", type=Path)
    parser.add_argument("extraction_json", type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = reconcile(load_json(args.correlation_json), load_json(args.extraction_json))
    write_csv(args.csv, report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print_report(report)
    return 0 if report["identity_valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
