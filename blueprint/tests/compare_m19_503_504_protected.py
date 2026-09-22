#!/usr/bin/env python3
"""Prove all Build503 source outside scoped M19 repair and identity is unchanged."""
from pathlib import Path
import hashlib, subprocess
from run_m19_selection_probe import body
BASE = "f48a74e9d87c8c7ae2ac5b9f0ac6cf28e87391fd"
base = subprocess.check_output(["git","show",BASE+":blueprint/source/BBMA_EA.mq4"]).decode().replace("\r\n","\n")
cand = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")
sig = "double CalculateTotalRisk("
old, new = body(base,sig), body(cand,sig)
assert old != new
identity = [
("Version 5.0.3 - D1O EXTREME_TPW Identity Enrichment","Version 5.0.4 - M19 Selection Failure Fail-Closed"),
('#property version   "5.03"','#property version   "5.04"'),
("V503_D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_20260921","V504_M19_SELECTION_FAIL_CLOSED_20260921"),
("D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_214_20260921","M19_SELECTION_FAIL_CLOSED_101_20260921"),
("EA=BBMA_EA Build=5.03 BuildTag=","EA=BBMA_EA Build=5.04 BuildTag=")]
expected = base.replace(old,new,1)
for a,b in identity:
    assert expected.count(a)==1 and cand.count(b)==1
    expected=expected.replace(a,b,1)
assert expected == cand, "Unauthorized source difference outside M19 function/build identity"
print("M19_504_COMPLETE_PROTECTED_SOURCE=PASS")
print("BASE_LF_SHA256="+hashlib.sha256(base.encode()).hexdigest())
print("CANDIDATE_LF_SHA256="+hashlib.sha256(cand.encode()).hexdigest())
