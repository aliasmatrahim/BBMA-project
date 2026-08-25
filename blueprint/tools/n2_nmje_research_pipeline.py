#!/usr/bin/env python3
"""Run the N2 NMJE research pipeline end-to-end on MT4 logs + closed-trade outcomes.

Research/diagnostic only. No EA source or trading logic is modified.

Usage:
  python blueprint/tools/n2_nmje_research_pipeline.py logs/*.log \
      --outcomes outcomes.csv --out-dir n2_report

Outputs:
- correlation.json
- outcome_attribution.json
- evidence.json
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
import n2_nmje_outcome_attributor as attributor
import n2_nmje_evidence_sufficiency as evidence_tool


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def run(log_paths: list[Path], outcomes_csv: Path, out_dir: Path) -> dict:
    observations, decisions = correlator.iter_records(log_paths)
    correlation = correlator.correlate(observations, decisions)

    outcomes, duplicates = attributor.load_outcomes(outcomes_csv)
    attribution = attributor.attribute(correlation, outcomes, duplicates)
    evidence = evidence_tool.build_evidence(attribution)

    correlation_path = out_dir / "correlation.json"
    attribution_path = out_dir / "outcome_attribution.json"
    evidence_path = out_dir / "evidence.json"
    write_json(correlation_path, correlation)
    write_json(attribution_path, attribution)
    write_json(evidence_path, evidence)

    return {
        "correlation": correlation,
        "attribution": attribution,
        "evidence": evidence,
        "paths": {
            "correlation": str(correlation_path),
            "outcome_attribution": str(attribution_path),
            "evidence": str(evidence_path),
        },
    }


def print_summary(result: dict) -> None:
    correlation = result["correlation"]
    attribution = result["attribution"]
    evidence = result["evidence"]
    print("N2 NMJE RESEARCH PIPELINE")
    print("=========================")
    print(f"N1 observations       : {correlation['n1_observation_count']}")
    print(f"N2 validated decisions: {correlation['n2_decision_count']}")
    print(f"Matched outcomes      : {attribution['matched_outcomes']}")
    print(f"Data status           : {evidence['data_status']}")
    cov = evidence["coverage"]["coverage_pct"]
    cov_text = "n/a" if cov is None else f"{cov:.2f}%"
    print(f"Outcome coverage      : {cov_text}")
    overall = evidence["overall"]
    wr = overall["win_rate_ex_be_pct"]
    wr_text = "n/a" if wr is None else f"{wr:.2f}%"
    print(f"Observed WR (ex-BE)   : {wr_text}")
    ci = overall["win_rate_wilson_95"]
    if ci is None:
        print("Wilson 95% interval   : n/a")
    else:
        print(f"Wilson 95% interval   : {ci['low_pct']:.2f}%..{ci['high_pct']:.2f}%")
    print(f"Observed net profit   : {overall['net_profit']:.2f}")
    print("Interpretation        : DESCRIPTIVE_RESEARCH_ONLY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="+", type=Path, help="MT4 Experts/Journal log file(s)")
    parser.add_argument("--outcomes", required=True, type=Path, help="closed-trade outcome CSV")
    parser.add_argument("--out-dir", required=True, type=Path, help="output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing_logs = [str(p) for p in args.logs if not p.is_file()]
    if missing_logs:
        raise SystemExit("Missing log file(s): " + ", ".join(missing_logs))
    if not args.outcomes.is_file():
        raise SystemExit(f"Missing outcomes CSV: {args.outcomes}")

    result = run(args.logs, args.outcomes, args.out_dir)
    print_summary(result)

    evidence = result["evidence"]
    if evidence["data_status"] == "IDENTITY_INVALID":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
