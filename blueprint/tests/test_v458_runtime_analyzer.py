#!/usr/bin/env python3
"""Synthetic fail-closed checks for the v4.58 unified runtime analyzer."""
from __future__ import annotations
import json, tempfile, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import v458_runtime_analyzer as a


def make_bundle(root: Path, profile: str, connected: bool, authenticated: bool, bad_identity: bool=False) -> Path:
    b = root / profile
    raw = b / "raw"
    raw.mkdir(parents=True)
    log = raw / "synthetic.log"
    log.write_text(
        "\n".join([
            "[V458-OBS][START] TS=100 StrategyID=1 InstanceID=0 MagicMin=110001 MagicMax=110099",
            f"[V458-OBS][ENV] TS=101 Connected={'Y' if connected else 'N'} TradeAllowed=N",
            "[D1-10A] EURUSD D1=B H4=B F=NONE",
            "[D1-10A] EURUSD D1=S H4=S F=NONE",
            "[D1-10A] EURUSD D1=T H4=N F=NONE",
            "[D1-10A] EURUSD D1=U H4=U F=NONE",
            "[P3M2][EXEC] Ticket=10 Pair=EURUSD DecisionID=x Signal=SIGNAL_RE_ENTRY Dir=DIR_BUY ValidateCandle=2026.08.25 10:00 OrderOpen=2026.08.25 11:00",
            "[M17-SL][STRUCT] Pair=EURUSD Dir=DIR_BUY TF=60 Start=2026.08.25 09:00 Confirm=2026.08.25 10:00 StructuralAnchor=1.10000 ConfirmationWick=1.10100 RawSpreadPips=0.0000 SpreadBufferPips=0.0 StructuralSL=1.09999 FinalBrokerSL=1.09999 TP=1.12000 C044=N D1TPW=N",
            "[M17-SL][STRUCT] Pair=USDJPY Dir=DIR_SELL TF=60 Start=2026.08.25 09:00 Confirm=2026.08.25 10:00 StructuralAnchor=150.000 ConfirmationWick=149.900 RawSpreadPips=1.2000 SpreadBufferPips=2.0 StructuralSL=150.001 FinalBrokerSL=150.021 TP=149.000 C044=N D1TPW=N",
            "[P3S5][EXEC_ID] Ticket=10 Pair=EURUSD Persist=PASS HashFound=Y HashMatch=Y ExpectedHash=ABC PersistedHash=ABC RawLen=1 RawComment=<x>",
        ]) + "\n", encoding="utf-8")
    gates = a.GATES[profile]
    manifest = {
        "schema": a.SCHEMA,
        "profile": profile,
        "canonical_source": {"blob": "bad" if bad_identity else a.BLOB, "sha256": a.SHA},
        "expected_gates": gates,
        "broker_connected": connected,
        "session_authenticated": authenticated,
        "hosted_smoke_only": not connected,
        "files": [log.name],
    }
    (b / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return b


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        good = a.analyze_bundle(make_bundle(root, "BASELINE", True, True))
        assert not good["manifest_issues"]
        assert good["cases"]["N3_FIREWALL"]["status"] == "PASS"
        assert good["cases"]["R3_D1_OWNER_MATRIX"]["status"] == "PASS"
        assert good["cases"]["R4_VALIDATION_TIMING"]["status"] == "PASS"
        assert good["cases"]["R4_M17_SL_GEOMETRY"]["status"] == "PASS"

        hosted = a.analyze_bundle(make_bundle(root, "R1_D1TPW", False, False))
        assert hosted["cases"]["R1_CHECKPOINT_RESTART"]["status"] == "BLOCKED"
        assert hosted["cases"]["N3_FIREWALL"]["status"] == "PASS"

        bad = a.analyze_bundle(make_bundle(root, "R2_C044", True, True, bad_identity=True))
        assert bad["manifest_issues"]
        assert all(v["status"] == "FAIL" for v in bad["cases"].values())

    print("V458_RUNTIME_ANALYZER_SELFTEST=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
