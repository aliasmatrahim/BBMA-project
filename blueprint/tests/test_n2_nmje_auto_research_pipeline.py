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
    log.write_text(
        "\n".join(
            [
                "[N1-NMJE] EURUSD REL=SUPPORTING P=H4_RE/S J=J1 D1=OWN/S H4=RE:F/S H1=EXT:REV/B M15=MHV:F/B R=LTF_STRUCTURE_SUPPORTING_PARENT",
                "[N2-NMJE-DEC] EURUSD SIG=SIGNAL_REM DIR=S REL=SUPPORTING P=H4_RE/S J=J1 DID=D1",
                "[N2-NMJE-OUT] PAIR=EURUSD TICKET=101 DID=D1 DIDH=H1 NET=12.5 CLOSE=1770000000 REC=REC_NORMAL",
                "[N1-NMJE] GBPUSD REL=ALIGNED P=H4_RE/B J=J2 D1=OWN/B H4=RE:F/B H1=RE:F/B M15=- R=H1_RE_ALIGNED_WITH_PARENT",
                "[N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_RE/B J=J2 DID=D2",
                "[N2-NMJE-OUT] PAIR=GBPUSD TICKET=102 DID=D2 DIDH=H2 NET=-2.5 CLOSE=1770000100 REC=REC_NORMAL",
                "[N2-NMJE-OUT] PAIR=USDJPY TICKET=103 DID=- DIDH=H3 NET=4.0 CLOSE=1770000200 REC=REC_IDENTITY_HASH_ONLY",
            ]
        ),
        encoding="utf-8",
    )

    result = mod.run([log], out_dir)
    assert result["correlation"]["n1_observation_count"] == 2, result
    assert result["correlation"]["n2_decision_count"] == 2, result
    assert result["extraction"]["record_count"] == 3, result
    assert result["extraction"]["valid_exact_outcomes"] == 2, result
    assert result["extraction"]["hash_only_outcomes"] == 1, result
    assert result["attribution"]["matched_outcomes"] == 2, result
    assert result["evidence"]["data_status"] == "COMPLETE_OBSERVED_SAMPLE", result
    assert result["evidence"]["overall"]["net_profit"] == 10.0, result

    for name in (
        "correlation.json",
        "extraction.json",
        "outcomes_exact.csv",
        "outcome_attribution.json",
        "evidence.json",
    ):
        assert (out_dir / name).is_file(), name

print("N2-08 NMJE auto research pipeline synthetic self-test PASS")
