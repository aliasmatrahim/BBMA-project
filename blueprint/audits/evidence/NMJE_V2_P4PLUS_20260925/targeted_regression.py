from pathlib import Path
import subprocess, re, json, hashlib, sys

ROOT=Path(r"D:\BBMA\Workspace\nmje-v2-p4plus-current-owner-101")
SRC=ROOT/"blueprint/source/BBMA_EA.mq4"
source=SRC.read_text(encoding="utf-8",errors="ignore")
base=subprocess.check_output(
    ["git","show","origin/d1-owner-dev:blueprint/source/BBMA_EA.mq4"],
    cwd=ROOT, text=True, encoding="utf-8", errors="ignore"
)

def fn(text,name):
    m=re.search(r'(?m)^[^{;\n]*\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{', text)
    if not m: return None
    brace=text.find("{",m.start()); d=0
    for i in range(brace,len(text)):
        if text[i]=="{": d+=1
        elif text[i]=="}":
            d-=1
            if d==0: return text[m.start():i+1]
    return None

checks={}
def check(name,cond,detail=""):
    checks[name]={"pass":bool(cond),"detail":str(detail)}

check("version_513", '#property version   "5.13"' in source)
check("build_tag", 'V513_NMJE_P4PLUS_SHADOW_20260925' in source)
check("source_rev_006", 'NMJE_P4PLUS_SHADOW_006_20260925' in source)
check("runtime_build_identity_513", 'Build=5.13 BuildTag=' in source)

# P3/P5: current-owner M5 remains raw closed-candle snapshot only.
p3=fn(source,"NMJE_P3_UpdateClosedM5Shadow") or ""
check("p3_no_signal_detector", all(x not in p3 for x in [
    "DetectExtreme(","DetectCSD(","DetectECSD(","DetectCSM(","UpdateReEntryState(",
    "UpdateCanonicalExtremeState(","UpdateCanonicalMLVState("
]))
check("p5_true_conflict_hold",
      "M5_SIGNAL_SEMANTICS_NOT_MATERIALIZED_TRUE_CONFLICT_HOLD" in p3 and
      "M5DiagnosticRelation = NESTED_UNRESOLVED" in p3 and
      "M5SemanticResolved = false" in p3)
check("no_m5_context_enum_resurrection", "ENUM_NMJE_M5_CONTEXT_CODE" not in source)

# P6/P7/P8/P11 metadata-only boundaries.
p6=fn(source,"NMJE_ClassifyJourneyMaturity") or ""
p8=fn(source,"NMJE_ApplyJourneyProvenanceStability") or ""
p11=fn(source,"NMJE_ApplyStrictJourneyLineage") or ""
freeze=fn(source,"NMJE_FreezeValidatedDecisionAttribution") or ""
save=fn(source,"SaveNMJEShadowAttribution") or ""
load=fn(source,"LoadNMJEShadowAttribution") or ""
p10=fn(source,"NMJE_BuildEntryDisplacementAttribution") or ""
check("p6_no_score_rank_gate", all(x not in p6 for x in [
    "Score","PriorityTier","DecisionState","RejectionReason","OrderSend(","RunEntryPreflightAndExecute("
]))
check("p8_identity_only_no_time_delay", all(x not in p8 for x in [
    "Sleep(","TimeCurrent(","GetTickCount","MaxWaitBars","barIndex +","barIndex -"
]))
check("p8_raw_relation_not_rewritten",
      "journey.Relation =" not in p8 and "journey.StableRelation =" in p8)
check("p11_strict_a_no_continuation_assignment",
      "journey.LineageClass = NMJE_LINEAGE_CONTINUATION" not in p11)
check("p11_root_is_parent",
      "journey.LineageRootEventID = journey.ParentEventID" in p11)
check("p4_freeze_requires_validated",
      "decision.DecisionState != DEC_VALIDATED" in freeze)
check("p4_persistence_diagnostic_only",
      all(x not in save+load for x in [
          "DecisionState","RejectionReason","recovery_state","OrderSend(","OrderClose("
      ]))
check("optional_hash_writes_explicit",
      '!= "" && !NMJEStoreHash16' not in save)
check("p10_no_rejection_threshold",
      all(x not in p10 for x in [
          "DecisionState","RejectionReason","OrderSend(","Max","Min","threshold","Threshold"
      ]))

# Freeze sequencing: validated -> freeze -> telemetry -> preflight.
block=re.search(r'if\(decision\.DecisionState == DEC_VALIDATED\)\s*\{(.*?)\n\s*\}',source,re.S)
body=block.group(1) if block else ""
positions=[body.find("NMJE_FreezeValidatedDecisionAttribution"),
           body.find("NMJE_PrintValidatedDecisionShadow"),
           body.find("RunEntryPreflightAndExecute")]
check("p4_freeze_order",
      all(x>=0 for x in positions) and positions==sorted(positions),positions)

# P10 must be post-fill in the successful execution branch, not recovery/adoption.
exec_start=source.find("int ticket = SendOrderWithRetry")
pos_open=source.find("info.initial_entry_price = OrderOpenPrice();",exec_start)
pos_disp=source.find("NMJE_BuildEntryDisplacementAttribution(decision, info.initial_entry_price",exec_start)
pos_add=source.find("AddToMonitoredTrades(info);",exec_start)
check("p10_post_fill_before_registry",
      pos_open>=0 and pos_disp>pos_open and pos_add>pos_disp,(pos_open,pos_disp,pos_add))

# P4 recovery is additive; missing state cannot mutate canonical recovery.
recovery_load=source.find("if(hasExecutionHash) LoadNMJEShadowAttribution(info);")
check("p4_optional_recovery_load", recovery_load>=0)

# Protected authority functions must remain byte-normalized exact from current owner.
protected=[
 "CompareCanonicalCandidates","PriorityEngine_Atomic","InvalidationEngine_Atomic",
 "CheckRiskBeforeTrade","IsSignalAllowed","ResolveApprovedInitialSLTP",
 "ResolveExecutionReferencePrice","ResolveSelectedSLTPSourceComponent",
 "IsApprovedSLTPSourceComponent","SendOrderWithRetry","RunEntryPreflightAndExecute"
]
prot={}
for name in protected:
    a=fn(base,name); b=fn(source,name)
    same=(a is not None and b is not None and re.sub(r'\s+','',a)==re.sub(r'\s+','',b))
    prot[name]={"same":same,
                "base_sha256":hashlib.sha256((a or "").encode()).hexdigest().upper(),
                "current_sha256":hashlib.sha256((b or "").encode()).hexdigest().upper(),
                "nmje_refs":(b or "").count("NMJE_"),
                "m5_refs":(b or "").count("PERIOD_M5")}
check("protected_functions_exact",all(v["same"] for v in prot.values()),json.dumps(prot,sort_keys=True))
check("protected_functions_no_nmje_m5",
      all(v["nmje_refs"]==0 and v["m5_refs"]==0 for v in prot.values()),
      json.dumps(prot,sort_keys=True))

check("broker_primitive_counts_unchanged",
      (base.count("OrderSend("),base.count("OrderClose("))==
      (source.count("OrderSend("),source.count("OrderClose(")),
      f"base={base.count('OrderSend(')}/{base.count('OrderClose(')} current={source.count('OrderSend(')}/{source.count('OrderClose(')}")

# No P4+ metadata is consumed in comparator/risk/execution authority.
forbidden_tokens=["NMJEMaturity","NMJEStructureDensity","NMJEStableRelation",
                  "NMJELineageClass","M5DiagnosticRelation","M5SemanticResolved"]
authority="".join(fn(source,n) or "" for n in protected)
check("p4plus_not_consumed_by_authority",
      all(t not in authority for t in forbidden_tokens))

# StageCount/maturity are never written into existing quality fields.
check("no_density_to_existing_score",
      all(x not in source for x in [
          "PatternStrength = decision.NMJEStructureDensity",
          "PriorityTier = decision.NMJEStructureDensity",
          "RequirementCompleteness = decision.NMJEStructureDensity",
          "SequenceCompleteness = decision.NMJEStructureDensity"
      ]))
p7=fn(source,"NMJE_PrintStructuralDensityShadow") or ""
p8tele=fn(source,"NMJE_PrintP8StabilityShadow") or ""
outcome=fn(source,"NMJE_PrintClosedOutcomeShadow") or ""
check("p7_candidate_shadow_present",
      "NMJE_BuildCandidateStructuralDensity" in p7 and
      "ObserverPrintChanged" in p7 and
      all(x not in p7 for x in ["RejectionReason","DecisionState","OrderSend(","OrderClose("]))
check("p7_before_priority",
      source.find("NMJE_PrintStructuralDensityShadow(pairIndex") >= 0 and
      source.find("NMJE_PrintStructuralDensityShadow(pairIndex") <
      source.find("PriorityEngine_Atomic(allCandidates"))
check("p8_changed_only_telemetry",
      "ObserverPrintChanged" in p8tele and "Authority=NONE" in p8tele)
check("p4_outcome_durable_reload",
      "LoadNMJEShadowAttribution(durableRead)" in outcome and
      "NMJE_AttributionEquivalent" in outcome and
      "DLOAD=" in outcome and "DMATCH=" in outcome)
opt=fn(source,"NMJE_OptionalStringEqual") or ""
check("optional_string_normalization",
      "StringLen(left) == 0 && StringLen(right) == 0" in opt and
      "NMJE_OptionalStringEqual(left.PreviousLineageRootHash" in source and
      "NMJE_OptionalStringEqual(left.M5EventHash" in source)

result={
 "schema":"NMJE_V2_P4PLUS_TARGETED_REGRESSION_V1",
 "source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest().upper(),
 "base_ref":"origin/d1-owner-dev",
 "checks":checks,
 "protected":prot
}
out=ROOT/"blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/targeted_regression_result.json"
out.write_text(json.dumps(result,indent=2),encoding="utf-8")
failed=[k for k,v in checks.items() if not v["pass"]]
print("NMJE_P4PLUS_TARGETED_REGRESSION="+("PASS" if not failed else "FAIL"))
for k,v in checks.items(): print(k,"PASS" if v["pass"] else "FAIL",v["detail"][:180])
print("RESULT="+str(out))
sys.exit(1 if failed else 0)
