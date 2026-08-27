#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
TOOLS = REPO / "blueprint" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import v459_runtime_analyzer as tool


def make_bundle(root: Path, name: str, lines: list[str], *, hosted=False, connected=True, authenticated=True, bad_identity=False) -> Path:
    bundle = root / name
    raw = bundle / "raw"
    raw.mkdir(parents=True)
    (raw / "runtime.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest = {
        "schema": tool.SCHEMA,
        "profile": "BASELINE",
        "canonical_source": {
            "path": "blueprint/source/BBMA_EA.mq4",
            "blob": tool.BLOB,
            "sha256": "0" * 64 if bad_identity else tool.SHA,
            "build": "Version 4.5.9 - P0 Execution Identity Persistence Fix",
            "property_version": "4.59",
        },
        "expected_gates": tool.GATES["BASELINE"],
        "hosted_smoke_only": hosted,
        "broker_connected": connected,
        "session_authenticated": authenticated,
        "observer_seen": True,
        "files": ["runtime.log"],
    }
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return bundle


def status(report: dict, case: str) -> str:
    return report["cases"][case]["status"]


def main() -> int:
    base_lines = [
        "[V459-OBS][START] TS=100 StrategyID=1 InstanceID=0 MagicMin=110001 MagicMax=110099",
        "[V459-OBS][ENV] TS=100 Connected=Y TradeAllowed=Y",
        "[P3S5][EXEC_ID] Ticket=10 Pair=EURUSD Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y ExpectedHash=ABCDEF0123456789 BrokerHash=ABCDEF0123456789 RawLen=23 RawComment=<BBMA|H:ABCDEF0123456789>",
        "[D1-10A] EURUSD D1=B",
        "[D1-10A] EURUSD D1=S",
        "[D1-10A] EURUSD D1=T",
        "[D1-10A] EURUSD D1=U",
        "[V459-OBS][START] TS=200 StrategyID=1 InstanceID=0 MagicMin=110001 MagicMax=110099",
        "[V459-OBS][ENV] TS=200 Connected=Y TradeAllowed=Y",
        "[P3S5][RECOVERY] Ticket=10 Pair=EURUSD State=REC_IDENTITY_HASH_ONLY Cause=EXECUTION_HASH_ONLY HashFound=Y FullMeta=N",
        "[V459-OBS][OPEN] TS=200 Ticket=10 Pair=EURUSD Type=BUY Magic=110013 OpenTime=90 Open=1.10000 SL=1.09000 TP=1.12000 Lots=0.0100 Comment=BBMA|H:ABCDEF0123456789",
    ]

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        good = make_bundle(root, "good", base_lines)
        report = tool.analyze_bundle(good)
        assert status(report, "P0_EXEC_ID_DURABLE") == "PASS"
        assert status(report, "P0_RESTART_RECOVERY") == "PASS"
        assert status(report, "P0_EXEC_ID_UNIQUENESS") == "PASS"
        assert status(report, "R3_D1_OWNER_MATRIX") == "PASS"
        assert status(report, "N3_FIREWALL") == "PASS"

        duplicate_lines = list(base_lines)
        duplicate_lines.insert(4, "[P3S5][EXEC_ID] Ticket=11 Pair=EURUSD Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y ExpectedHash=ABCDEF0123456789 BrokerHash=ABCDEF0123456789 RawLen=23 RawComment=<BBMA|H:ABCDEF0123456789>")
        duplicate = make_bundle(root, "duplicate", duplicate_lines)
        dup_report = tool.analyze_bundle(duplicate)
        assert status(dup_report, "P0_EXEC_ID_UNIQUENESS") == "FAIL"
        assert status(dup_report, "R3_D1O_IDENTITY") == "FAIL"

        missing_lines = [line for line in base_lines if "[RECOVERY]" not in line]
        missing_lines.append("[P3S5][RECOVERY] Ticket=10 Pair=EURUSD State=REC_IDENTITY_MISSING_FROZEN Cause=NO_IDENTITY HashFound=N FullMeta=N")
        missing = make_bundle(root, "missing", missing_lines)
        missing_report = tool.analyze_bundle(missing)
        assert status(missing_report, "P0_RESTART_RECOVERY") == "FAIL"

        hosted = make_bundle(root, "hosted", base_lines, hosted=True, connected=False, authenticated=False)
        hosted_report = tool.analyze_bundle(hosted)
        assert status(hosted_report, "P0_EXEC_ID_DURABLE") == "BLOCKED"
        assert status(hosted_report, "P0_RESTART_RECOVERY") == "BLOCKED"
        assert status(hosted_report, "N3_FIREWALL") == "PASS"

        bad = make_bundle(root, "bad-identity", base_lines, bad_identity=True)
        bad_report = tool.analyze_bundle(bad)
        assert bad_report["manifest_issues"] == ["canonical identity mismatch"]
        assert all(row["status"] == "FAIL" for row in bad_report["cases"].values())

    print("V459_RUNTIME_ANALYZER_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
