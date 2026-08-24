#!/usr/bin/env python3
"""Run the full N2 NMJE research pipeline directly from MT4 logs.

Requires logs containing:
- [N1-NMJE] journey observations
- [N2-NMJE-DEC] validated-decision shadows
- [N2-NMJE-OUT] closed-outcome shadows

Hash-only recovered outcomes are preserved in extraction.json but are not silently
attributed until a separate unique-hash identity rule is implemented and verified.

Research/diagnostic only; no EA source or trading behavior is modified.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import n2_nmje_decision_correlator as correlator
import n2_nmje_outcome_log_extractor as extractor
import n2_nmje_outcome_attributor as attributor
import n2_nmje_evidence_sufficiency as evidence_tool


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def run(log_paths: list[Path], out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)

    observations, decisions = correlator.iter_records(log_paths)
    correlation = correlator.correlate(observations, decisions)

    extraction = extractor.analyze(extractor.parse_logs(log_paths))
    outcomes_csv = out_dir / "outcomes_exact.csv"
    extractor.write_exact_csv(outcomes_csv, extraction)

    outcomes, duplicate_rows = attributor.load_outcomes(outcomes_csv)
    attribution = attributor.attribute(correlation, outcomes, duplicate_rows)
    evidence = evidence_tool.build_evidence(attribution)

    write_json(out_dir / "correlation.json", correlation)
    write_json(out_dir / "extraction.json", extraction)
    write_json(out_dir / "outcome_attribution.json", attribution)
    write_json(out_dir / "evidence.json", evidence)

    return {
        "correlation": correlation,
        "extraction": extraction,
        "attribution": attribution,
        "evidence": evidence,
        "outcomes_csv": str(outcomes_csv),
    }


def print_summary(result: dict) -> None:
    c = result["correlation"]
    x = result["extraction"]
    a = result["attribution"]
    e = result["evidence"]
    print("N2 NMJE AUTO RESEARCH PIPELINE")
    print("==============================")
    print(f"Journey observations   : {c['n1_observation_count']}")
    print(f"Validated decisions    : {c['n2_decision_count']}")
    print(f"Closed outcomes        : {x['record_count']}")
    print(f"Exact outcome identity : {x['valid_exact_outcomes']}")
    print(f"Hash-only outcomes     : {x['hash_only_outcomes']}")
    print(f"Attributed outcomes    : {a['matched_outcomes']}")
    print(f"Data status            : {e['data_status']}")
    print("Interpretation         : DESCRIPTIVE_RESEARCH_ONLY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="+", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing = [str(path) for path in args.logs if not path.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))
    result = run(args.logs, args.out_dir)
    print_summary(result)

    extraction = result["extraction"]
    if extraction["duplicate_tickets"] or extraction["duplicate_decision_ids"]:
        return 2
    if result["evidence"]["data_status"] == "IDENTITY_INVALID":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
