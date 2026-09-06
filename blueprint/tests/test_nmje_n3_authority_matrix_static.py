#!/usr/bin/env python3
"""Cross-module authority invariants for NMJE N3 staging.

Checks architecture ownership only; does not encode or change BBMA strategy rules.
"""
from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4').read_text(encoding='utf-8')


def module(start: str, end: str) -> str:
    s = SRC.find(start)
    assert s >= 0, start
    e = SRC.find(end, s + len(start))
    assert e >= 0, end
    return SRC[s:e]

m08 = module('MODULE 08: EXTREME DETECTOR', 'MODULE 09:')
m09 = module('MODULE 09:', 'MODULE 10:')
m12 = module('MODULE 12: RE-ENTRY ENGINE', 'MODULE 12N:')
m12n = module('MODULE 12N: NESTED MTF JOURNEY ENGINE', 'MODULE 13:')
m15 = module('MODULE 15: PRIORITY ENGINE', 'MODULE 16:')
m16 = module('MODULE 16: CONFLICT & INVALIDATION ENGINE', 'MODULE 17:')
m22 = module('MODULE 22:', 'MODULE 23:')

# Canonical owners remain in their owner modules.
for marker in ('UpdateExtremeLifecycle(', 'ResetExtremeLifecycle(', 'ResolveOppositeExtremeSupersession('):
    assert marker in m08, marker
for marker in ('UpdateReEntryState(', 'ResetReEntryState(', 'ConfirmReEntryState('):
    assert marker in m12, marker

# M09 consumes but cannot install/reset/redetect canonical Extreme ownership.
for forbidden in ('ResetExtremeLifecycle(parent', 'InstallMHVSupersessionParent(', 'DetectExtreme(pair, parentDirection'):
    assert forbidden not in m09, forbidden

# NMJE has no broker/execution ownership or upstream owner mutation.
for forbidden in (
    'OrderSend(', 'OrderClose(', 'OrderModify(', 'ProcessEntry(',
    'ResetExtremeLifecycle(', 'UpdateExtremeLifecycle(',
    'ResetReEntryState(', 'UpdateReEntryState(', 'ConfirmReEntryState('
):
    assert forbidden not in m12n, forbidden

# M15/M16 and M22 keep the established authority chain.
assert 'PriorityEngine_Atomic(' in m15
assert 'InvalidationEngine_Atomic(' in m16
assert 'OrderSend(' in m22

# N3 remains shadow-only in current staging.
for forbidden in ('REJ_NMJE', 'EnableNMJEExecutionGate', 'EnableNestedExecutionGate', 'N3_POLICY_ACTIVE'):
    assert forbidden not in SRC, forbidden

print('NMJE_N3_AUTHORITY_MATRIX_STATIC=PASS')
