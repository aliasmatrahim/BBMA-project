#!/usr/bin/env python3
"""Model guards for C10 evaluation-window and provenance-domain hygiene."""
import importlib.util
import sys
from datetime import date
from pathlib import Path


TOOL = Path(__file__).resolve().parent / "report_c10_evaluation.py"
SPEC = importlib.util.spec_from_file_location("c10_reporter", TOOL)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def signal(
    event: str,
    decision: str,
    stamp: str,
    attempt: int = 1,
    build: str = "4.78",
    source: str = "H",
    config: str = "C",
) -> dict[str, str]:
    row = {key: "NA" for key in MODULE.SIGNAL_HEADER}
    row.update({
        "Schema": "C10S1", "BuildID": build, "SourceHash": source,
        "ConfigFingerprint": config, "RunID": "R", "EventID": event,
        "EventTimeUTC": stamp, "DecisionID": decision,
        "AttemptSeq": str(attempt), "Pair": "GBPUSD", "Direction": "DIR_BUY",
        "SetupFamily": "SIGNAL_RE_ENTRY", "EntryTimeframe": "M15",
        "SignalState": "DEC_VALIDATED", "ReasonCode": "REJ_NONE",
    })
    return row


def outcome(
    event: str,
    decision: str,
    stamp: str,
    mode: str,
    reason: str,
    build: str = "4.78",
    source: str = "H",
    config: str = "C",
) -> dict[str, str]:
    row = {key: "NA" for key in MODULE.OUTCOME_HEADER}
    row.update({
        "Schema": "C10O1", "BuildID": build, "SourceHash": source,
        "ConfigFingerprint": config, "RunID": "R", "OutcomeEventID": event,
        "OutcomeTimeUTC": stamp, "Mode": mode, "DecisionID": decision,
        "Pair": "GBPUSD", "Direction": "DIR_BUY",
        "SetupFamily": "SIGNAL_RE_ENTRY", "EntryTimeframe": "M15",
        "SpreadPips": "1.2", "SlippagePips": "0.1" if mode == "REALIZED" else "NA",
        "MFEPips": "8.0", "MAEPips": "2.0", "ExitReason": reason,
    })
    return row


def main() -> None:
    dev = MODULE.Window("development", date(2026, 8, 1), date(2026, 8, 14))
    eva = MODULE.Window("evaluation", date(2026, 8, 15), date(2026, 8, 28))
    cases = 0
    report = MODULE.build_report(
        [signal("S1", "D1", "2026-08-02T00:00:00Z"),
         signal("S2", "D2", "2026-08-16T00:00:00Z")],
        [outcome("O1", "D1", "2026-08-03T00:00:00Z", "SHADOW", "TP"),
         outcome("O2", "D2", "2026-08-17T00:00:00Z", "REALIZED", "SL")],
        dev, eva,
    )
    assert len(report["groups"]) == 2; cases += 1
    assert {group["mode"] for group in report["groups"]} == {"SHADOW", "REALIZED"}; cases += 1
    assert report["policy"]["authority"] == "NONE"; cases += 1
    assert sum(group["spread_coverage"] for group in report["groups"]) == 2; cases += 1
    assert sum(group["slippage_coverage"] for group in report["groups"]) == 1; cases += 1
    try:
        MODULE.validate_windows(dev, MODULE.Window("evaluation", date(2026, 8, 14), date(2026, 8, 20)))
        raise AssertionError("overlap accepted")
    except MODULE.EvidenceError:
        cases += 1
    try:
        MODULE.build_report([], [outcome("O1", "D1", "2026-08-03T00:00:00Z", "SHADOW", "TP"),
                                 outcome("O2", "D1", "2026-08-04T00:00:00Z", "SHADOW", "SL")], dev, eva)
        raise AssertionError("duplicate DecisionID accepted")
    except MODULE.EvidenceError:
        cases += 1
    try:
        MODULE.build_report([signal("S1", "D1", "2026-08-03T00:00:00Z"),
                             signal("S2", "D1", "2026-08-17T00:00:00Z", 2)], [], dev, eva)
        raise AssertionError("cross-window DecisionID accepted")
    except MODULE.EvidenceError:
        cases += 1
    mixed = MODULE.build_report(
        [signal("COLLIDE", "D3", "2026-08-16T00:00:00Z",
                build="4.74", source="H74", config="C74"),
         signal("COLLIDE", "D3", "2026-08-16T00:00:00Z",
                build="4.80", source="H80", config="C80")],
        [outcome("OUT_COLLIDE", "D3", "2026-08-17T00:00:00Z", "SHADOW", "UNKNOWN",
                 build="4.74", source="H74", config="C74"),
         outcome("OUT_COLLIDE", "D3", "2026-08-17T00:00:00Z", "SHADOW", "UNKNOWN",
                 build="4.80", source="H80", config="C80")],
        dev, eva,
    )
    assert len(mixed["groups"]) == 2; cases += 1
    assert mixed["signal_denominators"]["evaluation"]["DEC_VALIDATED"] == 2; cases += 1
    try:
        MODULE.build_report(
            [signal("SAME_DOMAIN", "D4", "2026-08-16T00:00:00Z"),
             signal("SAME_DOMAIN", "D5", "2026-08-16T00:00:00Z")],
            [], dev, eva,
        )
        raise AssertionError("conflicting duplicate inside one provenance accepted")
    except MODULE.EvidenceError:
        cases += 1
    print(f"BBMA_CORE_C10_EVALUATION_REPORTER=PASS cases={cases}")


if __name__ == "__main__":
    main()
