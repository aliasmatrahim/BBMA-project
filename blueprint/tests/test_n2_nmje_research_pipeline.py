#!/usr/bin/env python3
from pathlib import Path
import csv
import importlib.util
import json
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_research_pipeline.py"
spec = importlib.util.spec_from_file_location("n2_nmje_research_pipeline", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    td_path = Path(td)
    log = td_path / "expert.log"
    outcomes = td_path / "outcomes.csv"
    out_dir = td_path / "report"

    log.write_text(
        "\n".join(
            [
                "[N1-NMJE] EURUSD REL=BUILDING P=H4_RE/S J=J1 D1=OWN/S H4=RE:F/S H1=EXT:R/B M15=- R=LTF_STRUCTURE_BUILDING",
                "[N1-NMJE] EURUSD REL=SUPPORTING P=H4_RE/S J=J1 D1=OWN/S H4=RE:F/S H1=EXT:REV/B M15=MHV:F/B R=LTF_STRUCTURE_SUPPORTING_PARENT",
                "[N2-NMJE-DEC] EURUSD SIG=SIGNAL_REM DIR=S REL=SUPPORTING P=H4_RE/S J=J1 DID=D1",
                "[N1-NMJE] GBPUSD REL=ALIGNED P=H4_RE/B J=J2 D1=OWN/B H4=RE:F/B H1=RE:F/B M15=- R=H1_RE_ALIGNED_WITH_PARENT",
                "[N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_RE/B J=J2 DID=D2",
            ]
        ),
        encoding="utf-8",
    )

    with outcomes.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["decision_id", "net_profit", "ticket"])
        writer.writeheader()
        writer.writerow({"decision_id": "D1", "net_profit": "12.0", "ticket": "101"})
        writer.writerow({"decision_id": "D2", "net_profit": "-3.0", "ticket": "102"})

    result = mod.run([log], outcomes, out_dir)

    assert result["correlation"]["n1_observation_count"] == 3, result
    assert result["correlation"]["n2_decision_count"] == 2, result
    assert result["correlation"]["exact_journey_matches"] == 2, result
    assert result["attribution"]["matched_outcomes"] == 2, result
    assert result["attribution"]["overall"]["net_profit"] == 9.0, result
    assert result["evidence"]["data_status"] == "COMPLETE_OBSERVED_SAMPLE", result
    assert result["evidence"]["coverage"]["coverage_pct"] == 100.0, result
    assert result["evidence"]["overall"]["win_rate_ex_be_pct"] == 50.0, result

    for name in ("correlation.json", "outcome_attribution.json", "evidence.json"):
        path = out_dir / name
        assert path.is_file(), path
        json.loads(path.read_text(encoding="utf-8"))

print("N2-05 NMJE research pipeline synthetic self-test PASS")
