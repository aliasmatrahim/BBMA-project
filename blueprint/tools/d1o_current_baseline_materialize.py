#!/usr/bin/env python3
from pathlib import Path
p=Path('blueprint/source/BBMA_EA.mq4')
s=p.read_text(encoding='utf-8')
if 'D1O-07 Canonical LTF Dedup' in s:
    raise SystemExit('already materialized')
if 'Version 4.5.1 - D1O-02 Opportunity Execution' not in s:
    raise SystemExit('unexpected current baseline')
# First restore the observation-only LTF cluster telemetry required for validation.
anchor='void NMJE_PrintValidatedDecisionShadow(int pairIndex, BBMA_Decision &decision)\n{'
helper='''string D1OpportunityLTFClusterText(BBMA_Decision &decision)\n{\n   if(decision.D1AuthorityMode != D1_AUTH_OPPORTUNITY) return "-";\n   bool hasH1=false, hasM15=false;\n   for(int i=0; i<decision.ComponentCount && i<3; i++)\n   {\n      if(decision.Components[i].ComponentType != SIGNAL_RE_ENTRY) continue;\n      if(decision.Components[i].Timeframe == PERIOD_H1) hasH1=true;\n      if(decision.Components[i].Timeframe == PERIOD_M15) hasM15=true;\n   }\n   if(hasH1 && hasM15) return "H1+M15";\n   if(hasH1) return "H1";\n   if(hasM15) return "M15";\n   return "-";\n}\n\n'''
if s.count(anchor)!=1: raise SystemExit('shadow anchor mismatch')
s=s.replace(anchor,helper+anchor,1)
old='''         " AUTH=", D1AuthorityModeText(decision.D1AuthorityMode),\n         " OFAM=", D1OpportunityFamilyText(decision.D1OpportunityFamily),\n         " OC=", (decision.D1OpportunityCycleID == "" ? "-" : decision.D1OpportunityCycleID));'''
new='''         " AUTH=", D1AuthorityModeText(decision.D1AuthorityMode),\n         " OFAM=", D1OpportunityFamilyText(decision.D1OpportunityFamily),\n         " OC=", (decision.D1OpportunityCycleID == "" ? "-" : decision.D1OpportunityCycleID),\n         " LTF=", D1OpportunityLTFClusterText(decision),\n         " OSH=", (decision.SequenceHash == "" ? "-" : decision.SequenceHash));'''
if s.count(old)!=1: raise SystemExit('telemetry tail mismatch')
s=s.replace(old,new,1)
old_hash='''   candidate.SequenceType = SIGNAL_RE_ENTRY;\n   candidate.Direction = opportunity.Direction;\n   candidate.ComponentCount = componentCount;\n   candidate.SequenceStartTime = opportunity.SourceCandleTime;\n   candidate.SequenceHash = SHORT_HASH("D1OPP|" + opportunity.CycleID + "|" +\n                                      IntegerToString((int)opportunity.Family) + ltfIdentity, 16);\n   candidate.Expiry = expiry;'''
new_hash='''   candidate.SequenceType = SIGNAL_RE_ENTRY;\n   candidate.Direction = opportunity.Direction;\n   candidate.ComponentCount = componentCount;\n   // D1O-07: fresh LTF Re-Entry owns execution identity; D1 is attribution only.\n   ReEntryData identityRE = h1Fresh ? h1 : m15;\n   candidate.SequenceStartTime = identityRE.ConfirmationCandle;\n   string canonicalIdentity = "RE_ENTRY|" + IntegerToString(identityRE.Direction) + "|" +\n                              IntegerToString(identityRE.Timeframe) + "|" +\n                              TimeToString(identityRE.ConfirmationCandle);\n   candidate.SequenceHash = SHORT_HASH(canonicalIdentity, 16);\n   candidate.Expiry = expiry;'''
if s.count(old_hash)!=1: raise SystemExit('candidate identity mismatch')
s=s.replace(old_hash,new_hash,1)
old_anchor='''datetime GetCandidateAnchorTime(ValidatedSequenceCandidate &candidate)\n{\n   datetime anchor = candidate.Components[0].CandleTime;\n   for(int i = 1; i < 3; i++)\n   {\n      if(candidate.Components[i].CandleTime > anchor)\n         anchor = candidate.Components[i].CandleTime;\n   }\n   return anchor;\n}'''
new_anchor='''datetime GetCandidateAnchorTime(ValidatedSequenceCandidate &candidate)\n{\n   if(candidate.UsesD1Opportunity)\n   {\n      for(int i=0; i<candidate.ComponentCount && i<3; i++)\n      {\n         if(candidate.Components[i].ComponentType == SIGNAL_RE_ENTRY &&\n            candidate.Components[i].Timeframe == PERIOD_H1 &&\n            candidate.Components[i].CandleTime > 0)\n            return candidate.Components[i].CandleTime;\n      }\n   }\n   datetime anchor=candidate.Components[0].CandleTime;\n   for(int i=1;i<3;i++) if(candidate.Components[i].CandleTime>anchor) anchor=candidate.Components[i].CandleTime;\n   return anchor;\n}'''
if s.count(old_anchor)!=1: raise SystemExit('candidate anchor mismatch')
s=s.replace(old_anchor,new_anchor,1)
s=s.replace('Version 4.5.1 - D1O-02 Opportunity Execution','Version 4.5.1 - D1O-07 Canonical LTF Dedup',1)
for x in ('candidate.D1OpportunityCycleID = opportunity.CycleID;','candidate.D1OpportunityFamily = opportunity.Family;','ResolveSelectedSLTPSourceComponent','RunEntryPreflightAndExecute(decision, actual)'):
    if x not in s: raise SystemExit('protected anchor missing: '+x)
if 'SHORT_HASH("D1OPP|" + opportunity.CycleID' in s: raise SystemExit('old execution hash remains')
p.write_text(s,encoding='utf-8')
print('D1O-08 current-baseline materialization PASS')
