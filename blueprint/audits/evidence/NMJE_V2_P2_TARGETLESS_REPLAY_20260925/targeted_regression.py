from pathlib import Path
import subprocess,re,json,hashlib,sys

ROOT=Path(r"D:\BBMA\Workspace\nmje-v2-targetless-replay-101")
SRC=ROOT/"blueprint/source/BBMA_EA.mq4"
OUT=ROOT/"blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925"
s=SRC.read_text(encoding="utf-8",errors="ignore")
BASE_COMMIT="ce73919556ec458efd5b1d962b9d7e5cdb348e4a"
base=subprocess.check_output(
 ["git","show",BASE_COMMIT+":blueprint/source/BBMA_EA.mq4"],
 cwd=ROOT,text=True,encoding="utf-8",errors="ignore")

def fn(text,name):
    pat=re.compile(r"(?m)^[A-Za-z_][A-Za-z0-9_<>*& \t]*\b"+re.escape(name)+r"\s*\(")
    for m in pat.finditer(text):
        op=text.find("(",m.start())
        depth=0; close=-1
        for i in range(op,len(text)):
            if text[i]=="(": depth+=1
            elif text[i]==")":
                depth-=1
                if depth==0:
                    close=i; break
        if close<0: continue
        j=close+1
        while j<len(text) and text[j].isspace(): j+=1
        if j>=len(text) or text[j]!="{": continue
        brace=j; d=0
        for k in range(brace,len(text)):
            if text[k]=="{": d+=1
            elif text[k]=="}":
                d-=1
                if d==0: return text[m.start():k+1]
    return None

def norm(x): return re.sub(r"\s+","",x or "")
checks={}
def ck(k,v,d=""): checks[k]={"pass":bool(v),"detail":str(d)}

ck("version_515",'#property version   "5.15"' in s)
ck("build_tag",'V515_NMJE_P2_TARGETLESS_REPLAY_20260925' in s)
ck("source_rev",'NMJE_P2_TARGETLESS_REPLAY_001_20260925' in s)
ck("runtime_identity",'Build=5.15 BuildTag=' in s)

protected=[
 "CompareCanonicalCandidates","PriorityEngine_Atomic","InvalidationEngine_Atomic",
 "CheckRiskBeforeTrade","IsSignalAllowed","ResolveExecutionReferencePrice",
 "ResolveSelectedSLTPSourceComponent","IsApprovedSLTPSourceComponent",
 "SendOrderWithRetry","RunEntryPreflightAndExecute"
]
prot={}
for n in protected:
    a=fn(base,n); b=fn(s,n); same=norm(a)==norm(b) and a is not None and b is not None
    prot[n]={"same":same,
             "base_sha256":hashlib.sha256((a or "").encode()).hexdigest().upper(),
             "current_sha256":hashlib.sha256((b or "").encode()).hexdigest().upper()}
ck("protected_authority_exact",all(v["same"] for v in prot.values()),json.dumps(prot,sort_keys=True))

canonical_c044=["ProcessC044OwnerClosedCandle","InitializeC044TradeStateFromDecision",
                "AdvanceC044OwnerEventOneCandle"]
c044={}
for n in canonical_c044:
    a=fn(base,n); b=fn(s,n); same=norm(a)==norm(b) and a is not None and b is not None
    c044[n]={"same":same,
             "base_sha256":hashlib.sha256((a or "").encode()).hexdigest().upper(),
             "current_sha256":hashlib.sha256((b or "").encode()).hexdigest().upper()}
ck("canonical_c044_state_machine_exact",all(v["same"] for v in c044.values()),json.dumps(c044,sort_keys=True))

ck("broker_primitive_counts",
   (base.count("OrderSend("),base.count("OrderClose("))==
   (s.count("OrderSend("),s.count("OrderClose(")),
   f"base={base.count('OrderSend(')}/{base.count('OrderClose(')} current={s.count('OrderSend(')}/{s.count('OrderClose(')}")

save=fn(s,"SaveC044Checkpoint") or ""
tele=fn(s,"F7Telemetry") or ""
reset=fn(s,"ResetC044TradeState") or ""
ck("shadow_checkpoint_noop_guard",'if(info.c044_shadow_replay) return true;' in save)
ck("shadow_f7_telemetry_suppressed",'if(info.c044_shadow_replay) return;' in tele)
ck("live_shadow_default_false",'info.c044_shadow_replay = false;' in reset)

helper_names=[
 "NMJE_P2_CaptureC044ReplayState","NMJE_P2_RestoreC044ReplayTrade",
 "NMJE_P2_FindHardSLHitInClosedM1Window","NMJE_P2_C044OutcomeText",
 "NMJE_P2_ResolveTargetlessC044Outcome","NMJE_P2_RegisterCounterfactualOpen",
 "NMJE_P2_ResolvePairedWindowOutcome","NMJE_P2_PrintCounterfactualOutcomes"
]
helpers="\n".join(fn(s,n) or "" for n in helper_names)
ck("targetless_helpers_present",all(fn(s,n) for n in helper_names))
ck("targetless_no_broker_or_risk_authority",all(x not in helpers for x in [
 "OrderSend(","OrderClose(","CheckRiskBeforeTrade(","CalculateLotSize(",
 "FinalPortfolioGuard(","ProcessEntry("
]))
target=fn(s,"NMJE_P2_ResolveTargetlessC044Outcome") or ""
ck("reuses_canonical_c044_processor",
   "ProcessC044OwnerClosedCandle(replay, pairIndex, candleTime)" in target)
ck("no_duplicate_strategy_detectors",all(x not in target for x in [
 "DetectCSM(","DetectExtreme(","UpdateExtremeLifecycle(","UpdateReEntryState("
]))
ck("targetless_hard_sl_only_proxy",
   "NMJE_P2_FindHardSLHitInClosedM1Window" in target and "PERIOD_M1" in helpers and
   "FrozenSpreadPrice" in helpers)
ck("targetless_fail_closed_states",all(x in target for x in [
 "UNCOMPARABLE_C044_REPLAY_UNRESOLVED","UNCOMPARABLE_C044_OWNER_HISTORY",
 "UNCOMPARABLE_C044_M1_HISTORY","UNCOMPARABLE_C044_REPLAY_FROZEN"
]))
reg=fn(s,"NMJE_P2_RegisterCounterfactualOpen") or ""
ck("d1tpw_excluded_from_replay",
   "shadow.C044LifecycleManaged" in reg and "!shadow.D1TPWLifecycleManaged" in reg)
ck("selected_seed_identity_check",
   "record.C044SeedMatch" in reg and "info.c044_owner_timeframe" in reg and
   "info.c044_epoch_anchor_candle" in reg and
   "info.c044_last_processed_owner_candle" in reg)
outcome=fn(s,"NMJE_P2_ResolvePairedWindowOutcome") or ""
ck("static_path_preserved",all(x in outcome or x in helpers for x in [
 "TP_FIRST","SL_FIRST","AMBIGUOUS_SAME_M1_BAR"
]))
ck("targetless_routes_to_c044_replay",
   "record.C044Replay.Present" in outcome and
   "NMJE_P2_ResolveTargetlessC044Outcome" in outcome)
ck("m5_not_used_for_targetless_replay","M5SemanticResolved" not in target)
ck("d1tpw_gate_still_off","bool           EnableD1TPWLifecycle               = false;" in s)

result={
 "schema":"NMJE_V2_P2_TARGETLESS_REPLAY_TARGETED_REGRESSION_V1",
 "base_commit":BASE_COMMIT,
 "source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest().upper(),
 "checks":checks,"protected":prot,"canonical_c044":c044
}
(OUT/"targeted_regression_result.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
bad=[k for k,v in checks.items() if not v["pass"]]
print("NMJE_P2_TARGETLESS_TARGETED="+("PASS" if not bad else "FAIL"))
for k,v in checks.items():
    print(k,"PASS" if v["pass"] else "FAIL",v["detail"][:220])
print("SOURCE_SHA256="+result["source_sha256"])
sys.exit(1 if bad else 0)
