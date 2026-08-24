#!/usr/bin/env python3
from pathlib import Path
import tempfile
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n1_nmje_log_analyzer.py"
spec = importlib.util.spec_from_file_location("n1_nmje_log_analyzer", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

sample = """
2026.08.24 13:00:00 [N1-NMJE] EURUSD REL=BUILDING P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 D1=OWN/S H4=RE:F/S H1=EXT:R/B M15=- R=LTF_STRUCTURE_BUILDING
2026.08.24 13:15:00 [N1-NMJE] EURUSD REL=SUPPORTING P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 D1=OWN/S H4=RE:F/S H1=EXT:REV/B M15=MHV:F/B R=LTF_STRUCTURE_SUPPORTING_PARENT
2026.08.24 13:30:00 [N1-NMJE] EURUSD REL=ALIGNED P=H4_RE/S J=EURUSD|H4_RE|240|SIGNAL_RE_ENTRY|S|100 D1=OWN/S H4=RE:F/S H1=RE:F/S M15=MHV:F/B R=H1_RE_ALIGNED_WITH_PARENT
2026.08.24 13:00:00 [N1-NMJE] GBPUSD REL=UNRESOLVED P=NONE J=- D1=UNRESOLVED H4=- H1=- M15=- R=D1_OWNER_UNRESOLVED
""".strip() + "\n"

with tempfile.TemporaryDirectory() as td:
    path = Path(td) / "sample.log"
    path.write_text(sample, encoding="utf-8")
    observations = list(mod.iter_observations([path]))
    report = mod.build_report(observations)

assert report["observation_count"] == 4, report
assert report["unique_pairs"] == 2, report
assert report["unique_journeys"] == 1, report
assert report["relation_counts"] == {
    "BUILDING": 1,
    "SUPPORTING": 1,
    "ALIGNED": 1,
    "UNRESOLVED": 1,
}, report
assert report["pair_relation_transitions"]["EURUSD"] == {
    "BUILDING->SUPPORTING": 1,
    "SUPPORTING->ALIGNED": 1,
}, report
assert report["deterministic_journey_violations"] == [], report
assert report["invalid_relation_rows"] == [], report
assert len(report["unresolved_rows"]) == 1, report
print("N1-05 analyzer synthetic self-test PASS")
