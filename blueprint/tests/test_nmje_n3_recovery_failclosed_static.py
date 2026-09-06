#!/usr/bin/env python3
"""N3 recovery/replay fail-closed invariants.

No strategy behavior is added here. The test verifies that existing recovery
patterns use exact closed-candle provenance and freeze/unresolve on missing data,
which is the required model for later NMJE lineage recovery.
"""
from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4').read_text(encoding='utf-8')

# Existing recovery architecture must retain exact-history replay and fail-closed states.
for required in (
    'REC_IDENTITY_MISSING_FROZEN',
    'H4_OWNER_RECOVERY_UNRESOLVED',
    'iBarShift(',
    'GetLatestClosedCandleTime(',
    'LoadC044ReplaySeed(',
    'SaveC044ReplaySeed(',
    'REPLAY_CANDLE_ORDER_INVALID',
    'REPLAY_CURSOR_DID_NOT_REACH_LATEST',
    'OWNER_EVENT_CANDLE_NOT_EXACT_CLOSED_BAR',
):
    assert required in SRC, required

# N3 canonical identity remains reconstructible from source-owned structural anchors.
for required in (
    'NMJE_ReEntryEventID(',
    'StartCandleTime',
    'NMJE_ExtremeEventID(',
    'RawCandleTime',
    'NMJE_H4OwnerEventID(',
    'SourceCandleTime',
    'NMJE_D1OwnerEventID(',
):
    assert required in SRC, required

# Current staging must remain shadow-only while replay equivalence is being proven.
for forbidden in (
    'EnableNMJEExecutionGate',
    'EnableNestedExecutionGate',
    'REJ_NMJE',
    'N3_POLICY_ACTIVE',
):
    assert forbidden not in SRC, forbidden

print('NMJE_N3_RECOVERY_FAILCLOSED_STATIC=PASS')
