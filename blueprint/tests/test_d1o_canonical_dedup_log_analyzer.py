#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "blueprint" / "tools" / "d1o_canonical_dedup_log_analyzer.py"
spec = importlib.util.spec_from_file_location("d1o_canonical_analyzer", TOOL)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

LOG_OK = """
2026.08.25 00:00 [D1-OPP] EURUSD F=CSD DIR=B ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 00:00 CYCLE=CYCLE_A R=D1 attribution A
2026.08.25 00:15 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_OWNER/B J=J1 DID=X DIDH=H1 AUTH=OPP OFAM=CSD OC=CYCLE_A LTF=H1 OSH=CANON1
2026.08.25 01:00 [D1-OPP] EURUSD F=RE_ENTRY DIR=B ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 01:00 CYCLE=CYCLE_B R=D1 attribution changed while LTF identity remains
2026.08.25 01:15 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_OWNER/B J=J1 DID=Y DIDH=H1 AUTH=OPP OFAM=RE_ENTRY OC=CYCLE_B LTF=H1 OSH=CANON1
""".strip()

LOG_BAD_DIRECTION = """
2026.08.25 00:00 [D1-OPP] EURUSD F=CSD DIR=B ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 00:00 CYCLE=CYCLE_A R=A
2026.08.25 00:15 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_OWNER/B J=J1 DID=X DIDH=H1 AUTH=OPP OFAM=CSD OC=CYCLE_A LTF=H1 OSH=CANON1
2026.08.25 01:00 [D1-OPP] EURUSD F=RE_ENTRY DIR=S ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 01:00 CYCLE=CYCLE_B R=B
2026.08.25 01:15 [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=S REL=ALIGNED P=H4_OWNER/S J=J2 DID=Y DIDH=H1 AUTH=OPP OFAM=RE_ENTRY OC=CYCLE_B LTF=H1 OSH=CANON1
""".strip()

with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "ok.log"
    p.write_text(LOG_OK, encoding="utf-8")
    opp, dec = mod.parse([p])
    report = mod.analyze(opp, dec)
    assert report["unique_execution_hashes"] == 1
    assert len(report["cross_d1_attribution_hash_reuse"]) == 1
    assert report["integrity"]["sequence_hash_direction_conflicts"] == []
    assert report["integrity"]["missing_sequence_hash_decisions"] == []

with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "bad.log"
    p.write_text(LOG_BAD_DIRECTION, encoding="utf-8")
    opp, dec = mod.parse([p])
    report = mod.analyze(opp, dec)
    assert len(report["integrity"]["sequence_hash_direction_conflicts"]) == 1

print("D1O-09 canonical dedup analyzer synthetic self-test: PASS")
