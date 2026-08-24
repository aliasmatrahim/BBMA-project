#!/usr/bin/env python3
from pathlib import Path
import tempfile
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_decision_correlator.py"
spec = importlib.util.spec_from_file_location("n2_nmje_decision_correlator", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

sample = """
2026.08.25 01:00:00 [N1-NMJE] EURUSD REL=BUILDING P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 D1=OWN/S H4=RE:F/S H1=EXT:R/B M15=- R=LTF_STRUCTURE_BUILDING
2026.08.25 01:15:00 [N1-NMJE] EURUSD REL=SUPPORTING P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 D1=OWN/S H4=RE:F/S H1=EXT:REV/B M15=MHV:F/B R=LTF_STRUCTURE_SUPPORTING_PARENT
2026.08.25 01:16:00 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_REM DIR=S REL=SUPPORTING P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 DID=D1
2026.08.25 01:30:00 [N1-NMJE] EURUSD REL=ALIGNED P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 D1=OWN/S H4=RE:F/S H1=RE:F/S M15=MHV:F/B R=H1_RE_ALIGNED_WITH_PARENT
2026.08.25 01:31:00 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=S REL=ALIGNED P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 DID=D2
2026.08.25 01:00:00 [N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=UNRESOLVED P=NONE/- J=- DID=D3
""".strip() + "\n"

with tempfile.TemporaryDirectory() as td:
    log = Path(td) / "sample.log"
    log.write_text(sample, encoding="utf-8")
    observations, decisions = mod.iter_records([log])
    report = mod.correlate(observations, decisions)

assert report["n1_observation_count"] == 3, report
assert report["n2_decision_count"] == 3, report
assert report["unique_decision_ids"] == 3, report
assert report["unique_decision_journeys"] == 1, report
assert report["decision_relation_counts"] == {
    "SUPPORTING": 1,
    "ALIGNED": 1,
    "UNRESOLVED": 1,
}, report
assert report["decision_signal_counts"] == {
    "SIGNAL_REM": 1,
    "SIGNAL_RE_ENTRY": 2,
}, report
assert report["exact_journey_matches"] == 2, report
assert report["pair_fallback_matches"] == 0, report
assert len(report["orphan_decisions"]) == 1, report
assert report["context_mismatches"] == [], report
assert report["duplicate_decision_ids"] == [], report

print("N2-02 NMJE decision correlator synthetic self-test PASS")
