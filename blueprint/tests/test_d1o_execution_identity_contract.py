#!/usr/bin/env python3
from pathlib import Path

src = Path('blueprint/source/BBMA_EA.mq4').read_text(encoding='utf-8')

standard = '''string hashInput = "RE_ENTRY|" + IntegerToString(reEntry.Direction) + "|" +
                      IntegerToString(reEntry.Timeframe) + "|" +
                      TimeToString(reEntry.ConfirmationCandle);
   candidate.SequenceHash = SHORT_HASH(hashInput, 16);'''

opportunity = '''string canonicalIdentity = "RE_ENTRY|" + IntegerToString(identityRE.Direction) + "|" +
                              IntegerToString(identityRE.Timeframe) + "|" +
                              TimeToString(identityRE.ConfirmationCandle);
   candidate.SequenceHash = SHORT_HASH(canonicalIdentity, 16);'''

assert src.count(standard) == 1, 'standard H1 Re-Entry canonical hash contract drifted'
assert src.count(opportunity) == 1, 'D1 opportunity canonical hash contract drifted'
assert 'SHORT_HASH("D1OPP|" + opportunity.CycleID' not in src, 'D1 attribution re-entered execution hash'

start = src.index('string GenerateDecisionID(')
end = src.index('string SHORT_HASH(', start)
fn = src[start:end]
assert 'sequenceHash' in fn
for forbidden in ('CycleID', 'OpportunityFamily', 'D1Opportunity'):
    assert forbidden not in fn, f'{forbidden} leaked into DecisionID'

anchor_start = src.index('datetime GetCandidateAnchorTime(')
anchor_end = src.index('bool ResolveSelectedSLTPSourceComponent(', anchor_start)
anchor_fn = src[anchor_start:anchor_end]
assert 'candidate.UsesD1Opportunity' in anchor_fn
assert 'component.Timeframe == PERIOD_H1' in anchor_fn

print('D1O execution identity contract drift guard: PASS')
