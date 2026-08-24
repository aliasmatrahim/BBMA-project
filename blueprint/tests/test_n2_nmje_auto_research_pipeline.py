#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_auto_research_pipeline.py"
spec = importlib.util.spec_from_file_location("n2_nmje_auto_research_pipeline", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    td_path = Path(td)
    log = td_path / "expert.log"
    out_dir = td_path / "report"

    did1 = "D1"
    did2 = "D2"
    did3 = "USDJPY|2026.08.25 00:30|1|7|CCC"
    did3_hash = mod.reconciler.mql4_short_hash(did3)

    log.write_text(
        "\n".join(
            [
                "[N1-NMJE] EURUSD REL=SUPPORTING P=H4_RE/S J=J1 D1=OWN/S H4=RE:F/S H1=EXT:REV/B M15=MHV:F/B R=LTF_STRUCTURE_SUPPORTING_PARENT",
                f"[N2-NMJE-DEC] EURUSD SIG=SIGNAL_REM DIR=S REL=SUPPORTING P=H4_RE/S J=J1 DID={did1}",
                f"[N2-NMJE-OUT] PAIR=EURUSD TICKET=101 DID={did1} DIDH=H1 NET=12.5 CLOSE=1770000000 REC=REC_NORMAL",
                "[N1-NMJE] GBPUSD REL=ALIGNED P=H4_RE/B J=J2 D1=OWN/B H4=RE:F/B H1=RE:F/B M15=- R=H1_RE_ALIGNED_WITH_PARENT",
                f"[N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_RE/B J=J2 DID={did2}",
                f"[N2-NMJE-OUT] PAIR=GBPUSD TICKET=102 DID={did2} DIDH=H2 NET=-2.5 CLOSE=1770000100 REC=REC_NORMAL",
                "[N1-NMJE] USDJPY REL=BUILDING P=D1_OWNER/B J=J3 D1=OWN/B H4=OWN/B H1=- M15=- R=PARENT_WAITING_FOR_CHILD",
                f"[N2-NMJE-DEC] USDJPY SIG=SIGNAL_RE_ENTRY DIR=B REL=BUILDING P=D1_OWNER/B J=J3 DID={did3}",
                f"[N2-NMJE-OUT] PAIR=USDJPY TICKET=103 DID=- DIDH={did3_hash} NET=4.0 CLOSE=1770000200 REC=REC_IDENTITY_HASH_ONLY",
            ]
        ),
        encoding="utf-8",
    )

    result = mod.run([log], out_dir)
    assert result["correlation"]["n1_observation_count"] == 3, result
    assert result["correlation"]["n2_decision_count"] == 3, result
    assert result["extraction"]["record_count"] == 3, result
    assert result["extraction"]["valid_exact_outcomes"] == 2, result
    assert result["extraction"]["hash_only_outcomes"] == 1, result
    assert result["reconciliation"]["reconciled_hash_only_count"] == 1, result
    assert result["reconciliation"]["combined_outcome_count"] == 3, result
    assert result["reconciliation"]["identity_valid"] is True, result
    assert result["attribution"]["matched_outcomes"] == 3, result
    assert result["evidence"]["data_status"] == "COMPLETE_OBSERVED_SAMPLE", result
    assert result["evidence"]["overall"]["net_profit"] == 14.0, result

    for name in (
        "correlation.json",
        "extraction.json",
        "reconciliation.json",
        "outcomes_reconciled.csv",
        "outcome_attribution.json",
        "evidence.json",
    ):
        assert (out_dir / name).is_file(), name

print("N2-10 NMJE auto research pipeline + hash reconciliation synthetic self-test PASS")
