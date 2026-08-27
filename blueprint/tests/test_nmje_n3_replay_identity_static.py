#!/usr/bin/env python3
"""Static replay/identity invariants for NMJE N3 staging.

This test deliberately checks provenance mechanics only. It must not encode new
BBMA trading rules or authorize NMJE execution gating.
"""
from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4').read_text(encoding='utf-8')


def fn_slice(name: str) -> str:
    marker = f'string {name}('
    start = SRC.find(marker)
    if start < 0:
        raise AssertionError(f'missing helper: {name}')
    nxt = SRC.find('\nstring ', start + len(marker))
    if nxt < 0:
        nxt = SRC.find('\nvoid ', start + len(marker))
    if nxt < 0:
        nxt = start + 4000
    return SRC[start:nxt]


re_id = fn_slice('NMJE_ReEntryEventID')
ext_id = fn_slice('NMJE_ExtremeEventID')
mlv_id = fn_slice('NMJE_MLVEventID')
d1_id = fn_slice('NMJE_D1OwnerEventID')
h4_id = fn_slice('NMJE_H4OwnerEventID')

# Re-Entry identity is installed from structural/start ownership, not confirmation maturity.
assert 'StartCandleTime' in re_id
assert 'state.Type' in re_id
assert 'ConfirmationCandle' not in re_id

# Extreme identity is cycle-owned by RAW anchor; later maturity cannot silently change it.
assert 'RawCandleTime' in ext_id
assert 'ConfirmationCandleTime' not in ext_id

# MLV identity stays tied to the canonical parent Extreme provenance.
assert 'ParentRawCandleTime' in mlv_id
assert 'ParentConfirmationCandleTime' in mlv_id

# Strategic owner identities use source-owned candle provenance.
assert 'SourceCandleTime' in d1_id
assert 'SourceCandleTime' in h4_id

# No wall-clock/random identity source is permitted in any identity helper.
identity_text = re_id + ext_id + mlv_id + d1_id + h4_id
for forbidden in ('TimeCurrent(', 'TimeLocal(', 'GetTickCount(', 'MathRand('):
    assert forbidden not in identity_text, forbidden

# M15 freezes shadow provenance; M16 compares the same fields.
for required in (
    'NMJESnapshotPresent',
    'FreezeNMJEShadowSnapshot(',
    'ValidateNMJEShadowSnapshot(',
    'current.JourneyID != decision.NMJEJourneyID',
    'current.ParentEventID != decision.NMJEParentEventID',
    'current.Relation != decision.NMJERelation',
    'current.UpdateCandleTime != decision.NMJEUpdateCandleTime',
    '[N3-NMJE-SHADOW][M16]',
):
    assert required in SRC, required

# Shadow phase firewall: no dedicated N3 rejection/gate marker is allowed yet.
for forbidden in ('REJ_NMJE', 'EnableNMJEExecutionGate', 'EnableNestedExecutionGate', 'N3_POLICY_ACTIVE'):
    assert forbidden not in SRC, forbidden

print('NMJE_N3_REPLAY_IDENTITY_STATIC=PASS')
