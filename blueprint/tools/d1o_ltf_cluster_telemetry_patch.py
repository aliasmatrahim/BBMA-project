#!/usr/bin/env python3
"""Patch D1O validated-decision telemetry with LTF cluster identity.

Telemetry only: adds LTF=H1/M15/H1+M15 and OSH=<SequenceHash> to the existing
[N2-NMJE-DEC] line. No candidate, priority, invalidation, risk, SL/TP or order
execution semantics are changed.
"""

from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4")
text = SRC.read_text(encoding="utf-8")

if "Version 4.5.1 - D1O-02 Opportunity Execution" not in text:
    raise SystemExit("unexpected D1O-02 baseline build")
if "D1OpportunityLTFClusterText" in text:
    raise SystemExit("D1O-06 telemetry already present")

anchor = "void NMJE_PrintValidatedDecisionShadow(int pairIndex, BBMA_Decision &decision)\n{"
helper = r'''string D1OpportunityLTFClusterText(BBMA_Decision &decision)
{
   if(decision.D1AuthorityMode != D1_AUTH_OPPORTUNITY) return "-";
   bool hasH1 = false;
   bool hasM15 = false;
   for(int i = 0; i < decision.ComponentCount && i < 3; i++)
   {
      if(decision.Components[i].ComponentType != SIGNAL_RE_ENTRY) continue;
      if(decision.Components[i].Timeframe == PERIOD_H1) hasH1 = true;
      if(decision.Components[i].Timeframe == PERIOD_M15) hasM15 = true;
   }
   if(hasH1 && hasM15) return "H1+M15";
   if(hasH1) return "H1";
   if(hasM15) return "M15";
   return "-";
}

'''
if text.count(anchor) != 1:
    raise SystemExit("validated decision shadow anchor mismatch")
text = text.replace(anchor, helper + anchor, 1)

old_tail = r'''         " AUTH=", D1AuthorityModeText(decision.D1AuthorityMode),
         " OFAM=", D1OpportunityFamilyText(decision.D1OpportunityFamily),
         " OC=", (decision.D1OpportunityCycleID == "" ? "-" : decision.D1OpportunityCycleID));'''
new_tail = r'''         " AUTH=", D1AuthorityModeText(decision.D1AuthorityMode),
         " OFAM=", D1OpportunityFamilyText(decision.D1OpportunityFamily),
         " OC=", (decision.D1OpportunityCycleID == "" ? "-" : decision.D1OpportunityCycleID),
         " LTF=", D1OpportunityLTFClusterText(decision),
         " OSH=", (decision.SequenceHash == "" ? "-" : decision.SequenceHash));'''
if text.count(old_tail) != 1:
    raise SystemExit("telemetry print tail mismatch")
text = text.replace(old_tail, new_tail, 1)

text = text.replace("Version 4.5.1 - D1O-02 Opportunity Execution",
                    "Version 4.5.1 - D1O-06 LTF Cluster Telemetry", 1)

for protected in (
    "BuildPossibleCombinations(rem, rre, ree",
    "PriorityEngine_Atomic(allCandidates, allCandidateCount",
    "InvalidationEngine_Atomic(pairIndex, decision, conflict)",
    "RunEntryPreflightAndExecute(decision, actual)",
):
    if protected not in text:
        raise SystemExit(f"protected execution anchor missing: {protected}")

SRC.write_text(text, encoding="utf-8")
print("D1O-06 LTF cluster telemetry patch applied")
