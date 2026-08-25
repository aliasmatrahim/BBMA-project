#!/usr/bin/env python3
"""Patch D1O opportunity execution identity to canonical LTF setup identity.

Safety correction for the already-approved multi-LTF dedup rule:
- when H1 is present, H1 owns the cluster identity even if M15 also supports it;
- M15-only opportunity uses the canonical M15 Re-Entry identity;
- D1 opportunity family/CycleID remain frozen attribution metadata, not a reason
  to execute the same LTF Re-Entry again.

Expected baseline: D1O-06 LTF Cluster Telemetry. The patch does not change
opportunity eligibility, family maturity, risk, SL/TP or broker execution rules.
"""

from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4")
text = SRC.read_text(encoding="utf-8")

if "Version 4.5.1 - D1O-06 LTF Cluster Telemetry" not in text:
    raise SystemExit("unexpected baseline: D1O-06 required")
if "D1O-07 Canonical LTF Dedup" in text:
    raise SystemExit("D1O-07 already applied")

old_hash_block = r'''   candidate.SequenceType = SIGNAL_RE_ENTRY;
   candidate.Direction = opportunity.Direction;
   candidate.ComponentCount = componentCount;
   candidate.SequenceStartTime = opportunity.SourceCandleTime;
   candidate.SequenceHash = SHORT_HASH("D1OPP|" + opportunity.CycleID + "|" +
                                      IntegerToString((int)opportunity.Family) + ltfIdentity, 16);
   candidate.Expiry = expiry;'''
new_hash_block = r'''   candidate.SequenceType = SIGNAL_RE_ENTRY;
   candidate.Direction = opportunity.Direction;
   candidate.ComponentCount = componentCount;

   // D1O-07: execution dedup identity belongs to the fresh LTF Re-Entry, not
   // to the D1 opportunity label. If H1 and M15 are one cluster, H1 owns the
   // structural identity; M15 remains a supporting/validated component.
   ReEntryData identityRE = h1Fresh ? h1 : m15;
   candidate.SequenceStartTime = identityRE.ConfirmationCandle;
   string canonicalIdentity = "RE_ENTRY|" + IntegerToString(identityRE.Direction) + "|" +
                              IntegerToString(identityRE.Timeframe) + "|" +
                              TimeToString(identityRE.ConfirmationCandle);
   candidate.SequenceHash = SHORT_HASH(canonicalIdentity, 16);
   candidate.Expiry = expiry;'''
if text.count(old_hash_block) != 1:
    raise SystemExit("D1O candidate identity block mismatch")
text = text.replace(old_hash_block, new_hash_block, 1)

old_anchor = r'''datetime GetCandidateAnchorTime(ValidatedSequenceCandidate &candidate)
{
   datetime anchor = candidate.Components[0].CandleTime;
   for(int i = 1; i < 3; i++)
   {
      if(candidate.Components[i].CandleTime > anchor)
         anchor = candidate.Components[i].CandleTime;
   }
   return anchor;
}'''
new_anchor = r'''datetime GetCandidateAnchorTime(ValidatedSequenceCandidate &candidate)
{
   // D1O-07: simultaneous H1+M15 is one cluster and H1 is the structural
   // owner. Returning H1 here keeps its DecisionID identical to the canonical
   // standalone H1 Re-Entry, preventing a later duplicate execution merely
   // because D1 opportunity attribution changed.
   if(candidate.UsesD1Opportunity)
   {
      for(int i = 0; i < candidate.ComponentCount && i < 3; i++)
      {
         if(candidate.Components[i].ComponentType == SIGNAL_RE_ENTRY &&
            candidate.Components[i].Timeframe == PERIOD_H1 &&
            candidate.Components[i].CandleTime > 0)
            return candidate.Components[i].CandleTime;
      }
   }

   datetime anchor = candidate.Components[0].CandleTime;
   for(int i = 1; i < 3; i++)
   {
      if(candidate.Components[i].CandleTime > anchor)
         anchor = candidate.Components[i].CandleTime;
   }
   return anchor;
}'''
if text.count(old_anchor) != 1:
    raise SystemExit("candidate anchor function mismatch")
text = text.replace(old_anchor, new_anchor, 1)

text = text.replace("Version 4.5.1 - D1O-06 LTF Cluster Telemetry",
                    "Version 4.5.1 - D1O-07 Canonical LTF Dedup", 1)

# The old family/CycleID-based execution hash must be gone, while attribution
# fields remain frozen elsewhere in the candidate/decision payload.
if 'SHORT_HASH("D1OPP|" + opportunity.CycleID' in text:
    raise SystemExit("old D1 opportunity execution identity remains")
for required in (
    'candidate.D1OpportunityCycleID = opportunity.CycleID;',
    'candidate.D1OpportunityFamily = opportunity.Family;',
    'ResolveSelectedSLTPSourceComponent',
    'RunEntryPreflightAndExecute(decision, actual)',
):
    if required not in text:
        raise SystemExit(f"protected attribution/execution anchor missing: {required}")

SRC.write_text(text, encoding="utf-8")
print("D1O-07 canonical LTF dedup patch applied")
