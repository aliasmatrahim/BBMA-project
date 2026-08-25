#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "blueprint" / "tools" / "d1o_opportunity_log_analyzer.py"
spec = importlib.util.spec_from_file_location("d1o_analyzer", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

LOG = """
2026.08.25 00:00 [D1-OPP] EURUSD F=CSD DIR=B ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 00:00 CYCLE=AAA111 R=Confirmed D1 CSD opportunity
2026.08.25 00:15 [D1-OPP-WATCH] EURUSD eCSD=B Action=WATCH_ONLY
2026.08.25 01:00 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_OWNER/B J=J1 DID=X DIDH=H1 AUTH=OPP OFAM=CSD OC=AAA111
2026.08.25 02:00 [D1-OPP] GBPUSD F=EXT_TPW DIR=S ACTIVE=Y TACT=Y SRC=2026.08.24 00:00 ACT=2026.08.25 00:00 CYCLE=BBB222 R=Reversal-confirmed D1 Extreme with active TP-Wajib path
2026.08.25 03:00 [N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=S REL=BUILDING P=H4_OWNER/S J=J2 DID=Y DIDH=H2 AUTH=OPP OFAM=EXT_TPW OC=BBB222
""".strip()

with tempfile.TemporaryDirectory() as td:
    path = Path(td) / "sample.log"
    path.write_text(LOG, encoding="utf-8")
    opp, watches, decisions = mod.parse([path])
    report = mod.analyze(opp, watches, decisions)

assert report["opportunity_log_rows"] == 2
assert report["unique_active_cycles"] == 2
assert report["watch_only_ecsd_rows"] == 1
assert report["active_cycles_by_family"] == {"CSD": 1, "EXT_TPW": 1}
assert report["opportunity_validated_decisions"] == 2
assert report["decisions_by_opportunity_family"] == {"CSD": 1, "EXT_TPW": 1}
assert report["cycles_without_validated_decision"] == []
assert report["integrity"]["cycle_identity_conflicts"] == []
assert report["integrity"]["unknown_cycle_decisions"] == []
assert report["integrity"]["family_mismatch_decisions"] == []
print("D1O opportunity log analyzer synthetic self-test: PASS")
