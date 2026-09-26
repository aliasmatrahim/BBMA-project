from pathlib import Path
import subprocess,re,json,hashlib,sys

ROOT=Path(r"D:\BBMA\Workspace\q9-nmje-v2-build516-forward-m5-prep-101")
SRC=ROOT/"blueprint/source/BBMA_EA.mq4"
OUT=ROOT/"blueprint/audits/evidence/NMJE_V2_BUILD516_20260926"
s=SRC.read_text(encoding="utf-8",errors="ignore")
BASE_COMMIT="459c0588e625d7f7630f0fb5612b7f04fda496de"
base=subprocess.check_output(
 ["git","show",BASE_COMMIT+":blueprint/source/BBMA_EA.mq4"],
 cwd=ROOT,text=True,encoding="utf-8",errors="ignore")

def fn(text,name):
    pat=re.compile(r"(?m)^[A-Za-z_][A-Za-z0-9_<>*& \t]*\b"+re.escape(name)+r"\s*\(")
    for m in pat.finditer(text):
        op=text.find("(",m.start()); depth=0; close=-1
        for i in range(op,len(text)):
            if text[i]=="(": depth+=1
            elif text[i]==")":
                depth-=1
                if depth==0: close=i; break
        if close<0: continue
        j=close+1
        while j<len(text) and text[j].isspace(): j+=1
        if j>=len(text) or text[j]!="{": continue
        d=0
        for k in range(j,len(text)):
            if text[k]=="{": d+=1
            elif text[k]=="}":
                d-=1
                if d==0: return text[m.start():k+1]
    return None

def norm(x): return re.sub(r"\s+","",x or "")
checks={}
def ck(k,v,d=""): checks[k]={"pass":bool(v),"detail":str(d)}

ck("version_516",'#property version   "5.16"' in s)
ck("build_tag",'V516_NMJE_FORWARD_M5_OWNER_PREP_20260926' in s)
ck("source_rev",'NMJE_FORWARD_M5_OWNER_PREP_001_20260926' in s)
ck("forward_input_default_off",
   'input bool     EnableNMJEForwardEvidence          = false;' in s)

forward=fn(s,"NMJE_IsForwardEvidenceEnabled") or ""
ck("forward_mode_demo_or_tester_only",
   "IsTesting()" in forward and "EnableNMJEForwardEvidence && IsDemo()" in forward)
ck("no_real_forward_override",
   "IsDemo()" in forward and "IsConnected()" not in forward and "Account" not in forward)

protected=[
 "CompareCanonicalCandidates","PriorityEngine_Atomic","InvalidationEngine_Atomic",
 "CheckRiskBeforeTrade","IsSignalAllowed","ResolveExecutionReferencePrice",
 "ResolveSelectedSLTPSourceComponent","IsApprovedSLTPSourceComponent",
 "SendOrderWithRetry","RunEntryPreflightAndExecute"
]
prot={}
for n in protected:
    a=fn(base,n); b=fn(s,n)
    same=norm(a)==norm(b) and a is not None and b is not None
    prot[n]={"same":same,
             "base_sha256":hashlib.sha256((a or "").encode()).hexdigest().upper(),
             "current_sha256":hashlib.sha256((b or "").encode()).hexdigest().upper()}
ck("protected_authority_exact",all(v["same"] for v in prot.values()),
   json.dumps(prot,sort_keys=True))

canonical_c044=["ProcessC044OwnerClosedCandle","InitializeC044TradeStateFromDecision",
                "AdvanceC044OwnerEventOneCandle"]
c044={}
for n in canonical_c044:
    a=fn(base,n); b=fn(s,n)
    same=norm(a)==norm(b) and a is not None and b is not None
    c044[n]={"same":same}
ck("canonical_c044_state_machine_exact",all(v["same"] for v in c044.values()),
   json.dumps(c044,sort_keys=True))

ck("broker_primitive_counts",
   (base.count("OrderSend("),base.count("OrderClose("))==
   (s.count("OrderSend("),s.count("OrderClose(")),
   f"base={base.count('OrderSend(')}/{base.count('OrderClose(')} current={s.count('OrderSend(')}/{s.count('OrderClose(')}")

p2set=fn(s,"NMJE_P2_PrintEqualEligibilityShadow") or ""
p2open=fn(s,"NMJE_P2_RegisterCounterfactualOpen") or ""
p2out=fn(s,"NMJE_P2_PrintCounterfactualOutcomes") or ""
ck("p2_forward_uses_bounded_helper",
   "NMJE_IsForwardEvidenceEnabled()" in p2set and
   "NMJE_IsForwardEvidenceEnabled()" in p2open and
   "NMJE_IsForwardEvidenceEnabled()" in p2out)
p2_helpers="\n".join(filter(None,[p2set,p2open,p2out,
    fn(s,"NMJE_P2_ResolvePairedWindowOutcome"),
    fn(s,"NMJE_P2_ResolveTargetlessC044Outcome")]))
ck("p2_no_broker_or_risk_authority",all(x not in p2_helpers for x in [
 "OrderSend(","OrderClose(","CheckRiskBeforeTrade(","CalculateLotSize(",
 "FinalPortfolioGuard(","ProcessEntry("
]))

m5owner=fn(s,"UpdateCanonicalM5SemanticOwners") or ""
ck("m5_owner_present",bool(m5owner))
ck("m5_owner_reuses_canonical_owners",all(x in m5owner for x in [
 "DetectExtreme(","UpdateExtremeLifecycle(","ResolveOppositeExtremeSupersession(",
 "BuildCanonicalM5DirectionSnapshots(","UpdateCanonicalMLVState(","UpdateReEntryState("
]))
ck("m5_owner_no_trade_authority",all(x not in m5owner for x in [
 "PriorityEngine_Atomic(","InvalidationEngine_Atomic(","CheckRiskBeforeTrade(",
 "RunEntryPreflightAndExecute(","OrderSend(","OrderClose("
]))
ck("m5_owner_closed_candle_sequence",
   "for(int shift = firstShift; shift >= latestShift; shift--)" in m5owner and
   "GetDataForTimeframe(pair, PERIOD_M5, candleTime, data)" in m5owner)
ck("m5_owner_gap_fail_closed",
   "HistoryGap = true" in m5owner and "M5 closed-candle continuity unresolved" in m5owner)

p3=fn(s,"NMJE_P3_UpdateClosedM5Shadow") or ""
ck("nmje_p3_consumes_only",
   all(x not in p3 for x in ["DetectExtreme(","DetectCSD(","DetectECSD(","DetectCSM(",
                              "UpdateExtremeLifecycle(","UpdateCanonicalMLVState(",
                              "UpdateReEntryState("]))
ck("p5_true_conflict_still_hold",
   "NESTED_CONFLICT" not in p3 and
   "M5_CONFIRMED_RE_OPPOSES_PARENT_TRUE_CONFLICT_HOLD" in p3)
ck("p5_bounded_mapping_present",all(x in p3 for x in [
 "M5_CONFIRMED_RE_ALIGNED_WITH_PARENT",
 "M5_CANDIDATE_RE_SUPPORTS_PARENT",
 "M5_CANDIDATE_RE_OPPOSES_PARENT_BUILDING",
 "M5_ACTIVE_EXTREME_SUPPORTS_PARENT",
 "M5_ACTIVE_EXTREME_OPPOSES_PARENT_BUILDING"
]))

mhv_parent=fn(s,"IsMHVParentExtremeMature") or ""
reset_mlv=fn(s,"ResetMLVState") or ""
mlv_event=fn(s,"NMJE_MLVEventID") or ""
export_mhv=fn(s,"ExportCanonicalMHVSignal") or ""
ck("m09_same_tf_generalized",
   "expectedTimeframe" in mhv_parent and "parent.Timeframe != expectedTimeframe" in mhv_parent and
   "int timeframe" in reset_mlv and "mlv.Timeframe = timeframe;" in reset_mlv)
ck("m15_mhv_execution_signature_unchanged",
   "mlv.Timeframe != PERIOD_M15" in export_mhv)
ck("mlv_event_id_timeframe_generic",
   "state.Timeframe <= 0" in mlv_event and "IntegerToString(state.Timeframe)" in mlv_event)

process=fn(s,"ProcessPair") or ""
ck("m15_clock_owns_m5_update",
   "UpdateCanonicalM5SemanticOwners(pairIndex);" in process and
   process.find("UpdateCanonicalM5SemanticOwners(pairIndex);") <
   process.find("UpdateNestedJourneyObservation(pairIndex);"))
ck("d1tpw_gate_still_off",
   "bool           EnableD1TPWLifecycle               = false;" in s)

result={
 "schema":"NMJE_V2_BUILD516_TARGETED_REGRESSION_V1",
 "base_commit":BASE_COMMIT,
 "source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest().upper(),
 "checks":checks,
 "protected":prot,
 "canonical_c044":c044
}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"targeted_regression_result.json").write_text(
    json.dumps(result,indent=2),encoding="utf-8")
bad=[k for k,v in checks.items() if not v["pass"]]
print("NMJE_V516_TARGETED="+("PASS" if not bad else "FAIL"))
for k,v in checks.items():
    print(k,"PASS" if v["pass"] else "FAIL",v["detail"][:240])
print("SOURCE_SHA256="+result["source_sha256"])
sys.exit(1 if bad else 0)
