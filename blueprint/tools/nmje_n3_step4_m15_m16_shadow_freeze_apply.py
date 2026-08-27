#!/usr/bin/env python3
"""Materialize N3 M15/M16 shadow provenance freeze without execution gating.

This patch is metadata/diagnostic only. It freezes the current NMJE journey
identity into BBMA_Decision at M15 selection and compares it again in M16.
Mismatch is logged only; it cannot reject, validate, promote, or execute a trade.
"""
from pathlib import Path
import sys

TARGET = Path('blueprint/source/BBMA_EA.mq4')


def once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'expected exactly one match, got {count}: {old[:120]!r}')
    return text.replace(old, new, 1)


def main() -> int:
    if not TARGET.exists():
        print(f'ERROR target missing: {TARGET}', file=sys.stderr)
        return 2
    src = TARGET.read_text(encoding='utf-8')
    if 'NMJESnapshotPresent' in src and 'FreezeNMJEShadowSnapshot' in src:
        print('PASS: N3 M15/M16 shadow provenance already materialized')
        return 0

    try:
        src = once(src,
'''   string                       D1OpportunityCycleID;
   bool                         D1OpportunitySnapshotValid;
   
   // MUTABLE LIFECYCLE''',
'''   string                       D1OpportunityCycleID;
   bool                         D1OpportunitySnapshotValid;

   // N3 shadow-only frozen NMJE provenance. No execution authority at this stage.
   string                       NMJEJourneyID;
   string                       NMJEParentEventID;
   ENUM_NESTED_RELATION         NMJERelation;
   datetime                     NMJEUpdateCandleTime;
   bool                         NMJESnapshotPresent;
   
   // MUTABLE LIFECYCLE''')

        anchor = '''int CompareCanonicalCandidates(ValidatedSequenceCandidate &a,
                               ValidatedSequenceCandidate &b)
{
   datetime aAnchor = GetCandidateAnchorTime(a);
   datetime bAnchor = GetCandidateAnchorTime(b);
   if(aAnchor > bAnchor) return 1;
   if(aAnchor < bAnchor) return -1;

   if(a.SequenceStartTime > b.SequenceStartTime) return 1;
   if(a.SequenceStartTime < b.SequenceStartTime) return -1;

   if(a.SequenceHash > b.SequenceHash) return 1;
   if(a.SequenceHash < b.SequenceHash) return -1;
   return 0;
}

'''
        helpers = anchor + '''// N3 Step-4 shadow phase: freeze provenance only. This helper must never
// decide eligibility or mutate canonical owner state.
bool FreezeNMJEShadowSnapshot(PairState &pairState, BBMA_Decision &decision)
{
   decision.NMJEJourneyID = "";
   decision.NMJEParentEventID = "";
   decision.NMJERelation = NESTED_NOT_APPLICABLE;
   decision.NMJEUpdateCandleTime = 0;
   decision.NMJESnapshotPresent = false;

   int pairIndex = -1;
   for(int i = 0; i < g_pair_count; i++)
   {
      if(g_pair_states[i].actual_symbol == pairState.actual_symbol)
      {
         pairIndex = i;
         break;
      }
   }
   if(pairIndex < 0) return false;

   NestedJourneyState journey = g_nested_journeys[pairIndex];
   if(journey.Pair != pairState.actual_symbol || journey.UpdateCandleTime <= 0)
      return false;

   decision.NMJEJourneyID = journey.JourneyID;
   decision.NMJEParentEventID = journey.ParentEventID;
   decision.NMJERelation = journey.Relation;
   decision.NMJEUpdateCandleTime = journey.UpdateCandleTime;
   decision.NMJESnapshotPresent = true;
   return true;
}

bool ValidateNMJEShadowSnapshot(int pairIndex, BBMA_Decision &decision,
                                string &reason)
{
   reason = "";
   if(pairIndex < 0 || pairIndex >= g_pair_count)
   {
      reason = "PAIR_INDEX_INVALID";
      return false;
   }
   if(!decision.NMJESnapshotPresent)
   {
      reason = "SNAPSHOT_MISSING";
      return false;
   }

   NestedJourneyState current = g_nested_journeys[pairIndex];
   if(current.Pair != decision.Pair)
   {
      reason = "PAIR_MISMATCH";
      return false;
   }
   if(current.UpdateCandleTime != decision.NMJEUpdateCandleTime)
   {
      reason = "UPDATE_CANDLE_MISMATCH";
      return false;
   }
   if(current.JourneyID != decision.NMJEJourneyID)
   {
      reason = "JOURNEY_ID_MISMATCH";
      return false;
   }
   if(current.ParentEventID != decision.NMJEParentEventID)
   {
      reason = "PARENT_EVENT_ID_MISMATCH";
      return false;
   }
   if(current.Relation != decision.NMJERelation)
   {
      reason = "RELATION_MISMATCH";
      return false;
   }
   return true;
}

'''
        src = once(src, anchor, helpers)

        src = once(src,
'''   decision.SLTPSource = SIGNAL_NONE;
   decision.DecisionState = DEC_CREATED;

   decision.DecisionID = GenerateDecisionID''',
'''   decision.SLTPSource = SIGNAL_NONE;
   decision.DecisionState = DEC_CREATED;

   // Shadow-only: absence/mismatch is diagnostic and MUST NOT alter selection.
   FreezeNMJEShadowSnapshot(pairState, decision);

   decision.DecisionID = GenerateDecisionID''')

        src = once(src,
'''   if(decision.CandidateExpiry > 0 && g_processing_time > decision.CandidateExpiry)
   {
      decision.DecisionState = DEC_EXPIRED;
      decision.RejectionReason = REJ_EXPIRED;
      return;
   }

   decision.DecisionState = DEC_VALIDATED;''',
'''   if(decision.CandidateExpiry > 0 && g_processing_time > decision.CandidateExpiry)
   {
      decision.DecisionState = DEC_EXPIRED;
      decision.RejectionReason = REJ_EXPIRED;
      return;
   }

   // N3 shadow comparison only. No rejection is permitted from this result.
   string nmjeShadowReason = "";
   bool nmjeShadowMatch = ValidateNMJEShadowSnapshot(pairIndex, decision,
                                                      nmjeShadowReason);
   if(DebugLevel >= DBG_SIGNAL)
      Print("[N3-NMJE-SHADOW][M16] Pair=", decision.Pair,
            " DecisionID=", decision.DecisionID,
            " Match=", nmjeShadowMatch ? "Y" : "N",
            " Relation=", NMJE_RelationText(decision.NMJERelation),
            " Journey=", decision.NMJEJourneyID == "" ? "-" : decision.NMJEJourneyID,
            " ParentEvent=", decision.NMJEParentEventID == "" ? "-" : decision.NMJEParentEventID,
            " Reason=", nmjeShadowMatch ? "MATCH" : nmjeShadowReason);

   decision.DecisionState = DEC_VALIDATED;''')

    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 3

    for token in (
        'NMJESnapshotPresent', 'FreezeNMJEShadowSnapshot(',
        'ValidateNMJEShadowSnapshot(', '[N3-NMJE-SHADOW][M16]'
    ):
        if token not in src:
            print(f'ERROR required token missing after apply: {token}', file=sys.stderr)
            return 4

    TARGET.write_text(src, encoding='utf-8')
    print('PASS: N3 Step-4 M15/M16 shadow provenance freeze materialized')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
