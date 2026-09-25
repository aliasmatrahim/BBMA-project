from pathlib import Path
import subprocess,re,json,hashlib,sys

ROOT=Path(r"D:\BBMA\Workspace\nmje-v2-counterfactual-p2-101")
SRC=ROOT/"blueprint/source/BBMA_EA.mq4"
s=SRC.read_text(encoding="utf-8",errors="ignore")
base=subprocess.check_output(
 ["git","show","origin/d1-owner-dev:blueprint/source/BBMA_EA.mq4"],
 cwd=ROOT,text=True,encoding="utf-8",errors="ignore")

def fn(text,name):
    m=re.search(r'(?m)^[^{;\n]*\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{',text)
    if not m:return None
    b=text.find("{",m.start());d=0
    for i in range(b,len(text)):
        if text[i]=="{":d+=1
        elif text[i]=="}":
            d-=1
            if d==0:return text[m.start():i+1]
    return None

checks={}
def ck(k,v,d=""):checks[k]={"pass":bool(v),"detail":str(d)}

ck("version_514",'#property version   "5.14"' in s)
ck("build_tag",'V514_NMJE_P2_COUNTERFACTUAL_SHADOW_20260925' in s)
ck("source_rev",'NMJE_P2_COUNTERFACTUAL_SHADOW_004_20260925' in s)
ck("runtime_identity",'Build=5.14 BuildTag=' in s)

protected=[
 "CompareCanonicalCandidates","PriorityEngine_Atomic","InvalidationEngine_Atomic",
 "CheckRiskBeforeTrade","IsSignalAllowed","ResolveExecutionReferencePrice",
 "ResolveSelectedSLTPSourceComponent","IsApprovedSLTPSourceComponent",
 "SendOrderWithRetry","RunEntryPreflightAndExecute"
]
prot={}
for n in protected:
    a=fn(base,n);b=fn(s,n)
    same=a is not None and b is not None and re.sub(r'\s+','',a)==re.sub(r'\s+','',b)
    prot[n]={"same":same,
             "base_sha256":hashlib.sha256((a or "").encode()).hexdigest().upper(),
             "current_sha256":hashlib.sha256((b or "").encode()).hexdigest().upper()}
ck("protected_authority_exact",all(v["same"] for v in prot.values()),json.dumps(prot,sort_keys=True))
ck("broker_primitive_counts",
   (base.count("OrderSend("),base.count("OrderClose("))==
   (s.count("OrderSend("),s.count("OrderClose(")),
   f"base={base.count('OrderSend(')}/{base.count('OrderClose(')} current={s.count('OrderSend(')}/{s.count('OrderClose(')}")

names=[
 "NMJE_P2_RegisterCounterfactualOpen",
 "NMJE_P2_ResolvePairedWindowOutcome",
 "NMJE_P2_PrintCounterfactualOutcomes",
 "NMJE_P2_BuildCounterfactualDecision"
]
cf="\n".join(fn(s,n) or "" for n in names)
ck("cf_helpers_present",all(fn(s,n) for n in names))
ck("cf_no_order_send_close","OrderSend(" not in cf and "OrderClose(" not in cf)
ck("cf_no_risk_approval",all(x not in cf for x in [
 "CheckRiskBeforeTrade(","CalculateLotSize(","FinalPortfolioGuard(","ProcessEntry("
]))
ck("cf_register_tester_only","if(!IsTesting()) return;" in (fn(s,"NMJE_P2_RegisterCounterfactualOpen") or ""))
ck("cf_outcome_tester_only","if(!IsTesting()) return;" in (fn(s,"NMJE_P2_PrintCounterfactualOutcomes") or ""))
p2=fn(s,"NMJE_P2_PrintEqualEligibilityShadow") or ""
ck("p2_live_authority_unchanged",all(x not in p2 for x in [
 "PriorityEngine_Atomic(","CompareCanonicalCandidates(","DecisionState","RejectionReason","OrderSend("
]))
ck("p2_pending_guarded","if(IsTesting())" in p2 and "g_nmje_cf_pending" in p2)
ck("cf_baseline_fill_proxy","info.initial_entry_price" in (fn(s,"NMJE_P2_RegisterCounterfactualOpen") or ""))
ck("cf_paired_window_closed_m1","PERIOD_M1" in (fn(s,"NMJE_P2_ResolvePairedWindowOutcome") or "") and
   "UNRESOLVED_AT_BASELINE_CLOSE" in (fn(s,"NMJE_P2_ResolvePairedWindowOutcome") or ""))
ck("cf_targetless_no_invented_tp","UNCOMPARABLE_TARGETLESS" in (fn(s,"NMJE_P2_ResolvePairedWindowOutcome") or ""))
ck("cf_same_bar_ambiguous","AMBIGUOUS_SAME_M1_BAR" in (fn(s,"NMJE_P2_ResolvePairedWindowOutcome") or ""))
ck("cf_sell_spread_proxy","FrozenSpreadPrice" in (fn(s,"NMJE_P2_ResolvePairedWindowOutcome") or ""))
ck("cf_no_m5_semantic_inference","M5SemanticResolved" not in (fn(s,"NMJE_P2_BuildCounterfactualDecision") or ""))
ck("cf_logs_authority_none",s.count("[Q9-P2-CF-")>=4 and s.count("Authority=NONE")>=4)
reg=fn(s,"NMJE_P2_RegisterCounterfactualOpen") or ""
dedup=fn(s,"NMJE_P2_IsSameCounterfactualExecutionIdentity") or ""
ck("cf_selected_first_two_pass",
   "for(int pass = 0; pass < 2; pass++)" in reg and
   "if(pass == 0 && !selected) continue;" in reg and
   "if(pass == 1 && selected) continue;" in reg)
ck("cf_execution_equivalent_dedup",
   "SLTPSourceType" in dedup and "SLTPSourceTimeframe" in dedup and
   "SLTPSourceCandleTime" in dedup and "StopLoss" in dedup and
   "TakeProfit" in dedup and "Targetless" in dedup and
   "NMJE_P2_IsSameCounterfactualExecutionIdentity" in reg)
ck("cf_preselection_pool_not_claimed_unique",
   '" Pending="' in s and '" Unique="' not in (fn(s,"NMJE_P2_PrintEqualEligibilityShadow") or ""))
ck("cf_open_emitted_only_for_active_set",
   reg.find("if(active.Count >= 2)") >= 0 and
   reg.find('Print("[Q9-P2-CF-OPEN]') > reg.find("if(active.Count >= 2)") and
   reg.find("g_nmje_cf_active[activeIndex] = active;") <
      reg.find('Print("[Q9-P2-CF-OPEN]'))

result={"schema":"NMJE_V2_P2_COUNTERFACTUAL_TARGETED_REGRESSION_V1",
        "source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest().upper(),
        "base_ref":"origin/d1-owner-dev@0034f31",
        "checks":checks,"protected":prot}
out=ROOT/"blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/targeted_regression_result.json"
out.write_text(json.dumps(result,indent=2),encoding="utf-8")
bad=[k for k,v in checks.items() if not v["pass"]]
print("NMJE_P2_COUNTERFACTUAL_TARGETED="+("PASS" if not bad else "FAIL"))
for k,v in checks.items():print(k,"PASS" if v["pass"] else "FAIL",v["detail"][:180])
print("SOURCE_SHA256="+result["source_sha256"])
sys.exit(1 if bad else 0)
