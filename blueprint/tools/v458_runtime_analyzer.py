#!/usr/bin/env python3
"""Fail-closed R1-R6 analyzer for BBMA v4.58 broker-runtime bundles."""
from __future__ import annotations
import argparse, json, math, re, sys, tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
BLOB="a166ffb23aba5e6b4011a28d9de8896cd00e33a1"
SHA="ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc"
SCHEMA="BBMA_V458_RUNTIME_BUNDLE_V1"
EXPECTED_BLOB=BLOB
EXPECTED_SHA256=SHA
GATES={"BASELINE":{"d1_tpw":False,"c044":False},"R1_D1TPW":{"d1_tpw":True,"c044":False},"R2_C044":{"d1_tpw":False,"c044":True}}
PROFILE_GATES=GATES
CASES=("R1_CHECKPOINT_RESTART","R1_TPW_COMPLETION_CLOSE","R1_IDEMPOTENCY","R2_CHECKPOINT_RESTART","R2_FAILED_MOMENTUM_CLOSE","R2_MOMENTUM_REARM","R2_CYCLE_SUPERSESSION","R2_M20_PRECEDENCE","R3_D1_OWNER_MATRIX","R3_D1O_IDENTITY","R4_VALIDATION_TIMING","R4_M17_SL_GEOMETRY","R5_TRADELOCK","R5_CUMULATIVE_RISK","R5_P3_BCD","R6_N2_CHAIN","N3_FIREWALL")
KV=re.compile(r"([A-Za-z0-9_]+)=([^\s]+)")
GV=re.compile(r"\[V458-OBS\]\[GV\].*?TS=(\d+).*?Name=([^\s]+).*?Value=([-+0-9.eE]+)")
START=re.compile(r"\[V458-OBS\]\[START\].*?TS=(\d+)")
HIST=re.compile(r"\[V458-OBS\]\[HIST\].*?Ticket=(\d+).*?CloseTime=(\d+)")
EXECID=re.compile(r"\[P3S5\]\[EXEC_ID\].*?Ticket=(\d+).*?ExpectedHash=([^\s]+)")
TIME_TOKEN=r"\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}(?::\d{2})?"
EXEC=re.compile(r"\[P3M[12]\]\[EXEC\].*?Ticket=(\d+).*?Signal=([^\s]+).*?ValidateCandle=("+TIME_TOKEN+r")\s+OrderOpen=("+TIME_TOKEN+r")")
OWNER=re.compile(r"\[D1-10A\]\s+[^\s]+\s+D1=([BSTU])\b")
REC=re.compile(r"\[P3S5\]\[RECOVERY\].*?Ticket=(\d+).*?State=([^\s]+)")
FINAL=re.compile(r"\[P3M[12]\]\[DECISION_FINAL\].*?Reason=([^\s]+)")

@dataclass
class R:
    status:str; detail:str; evidence:list
    def d(self): return {"status":self.status,"detail":self.detail,"evidence":self.evidence}

def fields(s): return {m.group(1):m.group(2) for m in KV.finditer(s)}
def parse_mt4_time(value:str)->datetime:
    for fmt in ("%Y.%m.%d %H:%M:%S","%Y.%m.%d %H:%M"):
        try:return datetime.strptime(value,fmt)
        except ValueError:pass
    raise ValueError(f"unsupported MT4 timestamp: {value}")

def load(bundle):
    p=bundle/"manifest.json"
    if not p.is_file(): raise ValueError(f"missing manifest: {p}")
    m=json.loads(p.read_text(encoding="utf-8-sig")); issues=[]
    if m.get("schema")!=SCHEMA: issues.append("schema mismatch")
    profile=m.get("profile")
    if profile not in GATES: issues.append("unsupported profile")
    src=m.get("canonical_source",{})
    if src.get("blob")!=BLOB or src.get("sha256")!=SHA: issues.append("canonical identity mismatch")
    if profile in GATES and m.get("expected_gates")!=GATES[profile]: issues.append("profile/gate mismatch")
    paths=[]; lines=[]
    for name in m.get("files",[]):
        q=bundle/"raw"/str(name)
        if not q.is_file(): raise ValueError(f"missing raw log: {q}")
        paths.append(q); lines += q.read_text(encoding="utf-8",errors="ignore").splitlines()
    if not paths: raise ValueError("bundle has no logs")
    return m,issues,paths,lines

def snapshots(lines,prefix):
    out=defaultdict(lambda:defaultdict(dict))
    for line in lines:
        m=GV.search(line)
        if not m or not m.group(2).startswith(prefix+"|"): continue
        z=re.search(r"\|T(\d+)\|([^\s]+)$",m.group(2))
        if z: out[int(z.group(1))][int(m.group(1))][z.group(2)]=float(m.group(3))
    return out

def history(lines):
    out={}
    for line in lines:
        m=HIST.search(line)
        if m: out[int(m.group(1))]=max(out.get(int(m.group(1)),0),int(m.group(2)))
    return out

def recover(lines,ticket):
    return [x for x in lines if (m:=REC.search(x)) and int(m.group(1))==ticket and m.group(2)=="REC_NORMAL"]
def identity(lines):
    by=defaultdict(set)
    for x in lines:
        m=EXECID.search(x)
        if m and m.group(2)!="-": by[m.group(2)].add(int(m.group(1)))
    dup={k:sorted(v) for k,v in by.items() if len(v)>1}
    if dup:return R("FAIL","same execution hash maps to multiple tickets",[str(dup)])
    return R("PASS","observed execution hashes are one-ticket-per-hash",[f"hashes={len(by)}"]) if by else R("INCOMPLETE","no EXEC_ID evidence",[])
def assertions(bundle,paths):
    p=bundle/"assertions.json"
    if not p.is_file(): return {}
    j=json.loads(p.read_text())
    if j.get("schema")!="BBMA_V458_RUNTIME_ASSERTIONS_V1": raise ValueError("assertion schema mismatch")
    texts={"raw/"+x.name:x.read_text(encoding="utf-8",errors="ignore") for x in paths}; out={}
    for row in j.get("assertions",[]):
        cid,status,refs=row.get("case_id"),row.get("status"),row.get("evidence_refs",[])
        if cid not in CASES or status not in ("PASS","FAIL") or not refs: raise ValueError("invalid assertion row")
        for ref in refs:
            if "#" not in ref: raise ValueError("bad assertion ref")
            rel,needle=ref.split("#",1)
            if rel not in texts or not needle or needle not in texts[rel]: raise ValueError(f"assertion ref not found: {ref}")
        out[cid]=R(status,str(row.get("note","indexed raw evidence")),refs)
    return out

def lifecycle(profile,lines):
    out={}; starts=sum(bool(START.search(x)) for x in lines); hist=history(lines)
    if profile=="R1_D1TPW":
        s=snapshots(lines,"D1TPW"); tickets=[t for t,v in s.items() if any("LP" in f for f in v.values())]
        frozen=[x for x in lines if "D1TPW lifecycle frozen" in x]
        good=[(t,recover(lines,t)) for t in tickets if recover(lines,t)]
        out["R1_CHECKPOINT_RESTART"]=R("FAIL","D1TPW freeze observed",frozen[:3]) if frozen else R("PASS","checkpoint recovered REC_NORMAL after restart",good[0][1][:2]) if starts>=2 and good else R("INCOMPLETE","need 2 START epochs + checkpoint + REC_NORMAL",[])
        done=[]
        for t,v in s.items():
            for ts,f in sorted(v.items()):
                if f.get("L")==1 and f.get("XL",0)>0 and hist.get(t,0)>=int(f["XL"]): done.append((t,int(f["XL"]),hist[t]))
        out["R1_TPW_COMPLETION_CLOSE"]=R("FAIL","D1TPW freeze observed",frozen[:3]) if frozen else R("PASS","TPW latch followed by same-ticket history close",[str(done[0])]) if done else R("INCOMPLETE","need L=1 XL>0 then same ticket closed",[])
    if profile=="R2_C044":
        s=snapshots(lines,"C044"); tickets=[t for t,v in s.items() if any("ST" in f for f in v.values())]
        frozen=[x for x in lines if "C044 lifecycle frozen" in x]; good=[(t,recover(lines,t)) for t in tickets if recover(lines,t)]
        out["R2_CHECKPOINT_RESTART"]=R("FAIL","C044 freeze observed",frozen[:3]) if frozen else R("PASS","checkpoint/replay recovered REC_NORMAL after restart",good[0][1][:2]) if starts>=2 and good else R("INCOMPLETE","need 2 START epochs + checkpoint + REC_NORMAL",[])
        for cid,reason in (("R2_FAILED_MOMENTUM_CLOSE",1),("R2_CYCLE_SUPERSESSION",2)):
            done=[]
            for t,v in s.items():
                for ts,f in sorted(v.items()):
                    if f.get("ST")==3 and f.get("XR")==reason and f.get("XL",0)>0 and hist.get(t,0)>=int(f["XL"]): done.append((t,int(f["XL"]),hist[t]))
            out[cid]=R("FAIL","C044 freeze observed",frozen[:3]) if frozen else R("PASS",f"latched XR={reason} then closed",[str(done[0])]) if done else R("INCOMPLETE",f"need ST=3 XR={reason} XL>0 then close",[])
        rearms=[]
        for t,v in s.items():
            z=sorted(v.items())
            for i,(a,fa) in enumerate(z):
                if fa.get("ST")!=2:continue
                if any(fb.get("ST")==1 and fb.get("EP",0)>fa.get("EP",-1) for _,fb in z[i+1:]): rearms.append(t);break
        out["R2_MOMENTUM_REARM"]=R("PASS","ST=2 -> ST=1 with newer epoch",[str(rearms[0])]) if rearms else R("INCOMPLETE","need WAIT_NEXT_REENTRY -> newer WAIT_OUTER_TEST epoch",[])
    return out

def d1(lines,paths):
    states={m.group(1) for x in lines if (m:=OWNER.search(x))}
    matrix=R("PASS","B/S/T/U all observed",[str(sorted(states))]) if states>={"B","S","T","U"} else R("INCOMPLETE",f"owner states={sorted(states)}",[])
    ident=identity(lines)
    try:
        import d1_runtime_evidence_analyzer as tool
        rep=tool.analyze(paths); dd=rep.get("dedup",{})
        if dd.get("fatal"): ident=R("FAIL","D1/D1O analyzer fatal identity/dedup",[str(dd)])
    except Exception: pass
    return matrix,ident

def timing(lines):
    rows=[]
    for x in lines:
        m=EXEC.search(x)
        if m:
            a=parse_mt4_time(m.group(3)); b=parse_mt4_time(m.group(4)); rows.append((int(m.group(1)),(b-a).total_seconds()))
    bad=[x for x in rows if x[1]<=0]
    if bad:return R("FAIL","order at/before validation timestamp",[str(x) for x in bad[:3]])
    return R("PASS","all observed orders strictly after validation timestamp",[f"executions={len(rows)}"]) if rows else R("INCOMPLETE","no EXEC timing evidence",[])
def m17(lines):
    cov={"BUY":0,"SELL":0,"JPY":0,"NONJPY":0}; bad=[]; n=0
    for x in lines:
        if "[M17-SL][STRUCT]" not in x:continue
        f=fields(x); n+=1
        try:d=f["Dir"]; pair=f["Pair"]; raw=float(f["RawSpreadPips"]); buf=float(f["SpreadBufferPips"]); st=float(f["StructuralSL"]); final=float(f["FinalBrokerSL"]); tp=float(f["TP"])
        except Exception:bad.append("unparseable M17 row");continue
        if d=="DIR_BUY": cov["BUY"]=1
        elif d=="DIR_SELL": cov["SELL"]=1
        else: bad.append("unknown M17 direction: "+d); continue
        cov["JPY" if "JPY" in pair.upper() else "NONJPY"]=1
        if d=="DIR_BUY" and (abs(buf)>1e-9 or final>st+1e-12):bad.append(x)
        if d=="DIR_SELL" and (buf+1e-9<max(2,math.ceil(raw-1e-9)) or final+1e-12<st):bad.append(x)
        if (f.get("C044")=="Y" or f.get("D1TPW")=="Y") and abs(tp)>1e-9:bad.append(x)
    if bad:return R("FAIL","M17 geometry violation",bad[:3])
    if n and all(cov.values()):return R("PASS","BUY+SELL and JPY+non-JPY geometry observed",[f"rows={n}"])
    return R("INCOMPLETE",f"M17 valid rows={n}; coverage={cov}",[])
def n2(lines,paths):
    counts={k:sum(k in x for x in lines) for k in ("[N1-NMJE]","[N2-NMJE-DEC]","[N2-NMJE-OUT]")}
    if not all(counts.values()):return R("INCOMPLETE",f"chain counts={counts}",[])
    try:
        import n2_nmje_auto_research_pipeline as tool
        with tempfile.TemporaryDirectory() as td: rep=tool.run(paths,Path(td))
        rec=rep["reconciliation"]; ev=rep["evidence"]; matched=rep["attribution"].get("matched_outcomes",0)
        if not rec.get("identity_valid") or ev.get("data_status")=="IDENTITY_INVALID":return R("FAIL","N2 identity reconciliation invalid",[])
        return R("PASS","N2 closed outcome identity attributed",[f"matched={matched}"]) if matched else R("INCOMPLETE","N2 markers exist; no attributed close yet",[])
    except Exception as e:return R("FAIL",f"N2 pipeline error: {e}",[])
def analyze_bundle(bundle):
    m,issues,paths,lines=load(bundle); ass=assertions(bundle,paths); res={c:R("INCOMPLETE","no applicable evidence in this bundle",[]) for c in CASES}
    if issues:
        return {"bundle":str(bundle),"profile":m.get("profile"),"manifest_issues":issues,"cases":{c:R("FAIL","; ".join(issues),[]).d() for c in CASES}}
    blocked=m.get("hosted_smoke_only") or not m.get("broker_connected") or not m.get("session_authenticated")
    if blocked:
        why="hosted/no authenticated connected broker session"
        for c in CASES:
            if c!="N3_FIREWALL":res[c]=R("BLOCKED",why,[])
    alltext="\n".join(lines)
    res["N3_FIREWALL"]=R("FAIL","unapproved N3 execution marker observed",[]) if any(x in alltext for x in ("N3_POLICY_ACTIVE","N3_EXECUTION_POLICY")) else R("PASS","N3 policy remains NONE/inactive",[])
    if not blocked:
        for k,v in lifecycle(m["profile"],lines).items():res[k]=v
        if m["profile"]=="R1_D1TPW":res["R1_IDEMPOTENCY"]=identity(lines)
        res["R3_D1_OWNER_MATRIX"],res["R3_D1O_IDENTITY"]=d1(lines,paths)
        res["R4_VALIDATION_TIMING"]=timing(lines);res["R4_M17_SL_GEOMETRY"]=m17(lines);res["R6_N2_CHAIN"]=n2(lines,paths)
        reasons=[mm.group(1) for x in lines if (mm:=FINAL.search(x))]
        if "REJ_TRADE_LOCK" in reasons:res["R5_TRADELOCK"]=R("INCOMPLETE","REJ_TRADE_LOCK seen; exact mode scenario needs indexed raw evidence",[])
        if "REJ_TOTAL_RISK" in reasons:res["R5_CUMULATIVE_RISK"]=R("INCOMPLETE","REJ_TOTAL_RISK seen; cumulative arithmetic needs indexed raw evidence",[])
        if "[P3S5][EXEC_ID]" in alltext and "[P3S5][RECOVERY]" in alltext:res["R5_P3_BCD"]=R("INCOMPLETE","P3 exec+recovery seen; B/C/D still scenario-indexed",[])
        for cid,a in ass.items():
            if res[cid].status!="FAIL":res[cid]=a
    return {"bundle":str(bundle),"profile":m["profile"],"manifest_issues":[],"cases":{k:v.d() for k,v in res.items()}}
def merge(reports):
    out={}
    for c in CASES:
        attempts=[{"bundle":r["bundle"],**r["cases"][c]} for r in reports]; ss=[x["status"] for x in attempts]
        status="FAIL" if "FAIL" in ss else "PASS" if "PASS" in ss else "BLOCKED" if ss and all(x=="BLOCKED" for x in ss) else "INCOMPLETE"
        out[c]={"status":status,"attempts":attempts}
    ss=[x["status"] for x in out.values()]; overall="FAIL" if "FAIL" in ss else "INCOMPLETE" if any(x in ("INCOMPLETE","BLOCKED") for x in ss) else "PASS"
    return {"schema":"BBMA_V458_RUNTIME_ANALYSIS_V1","overall":overall,"execution_policy":"NONE","n3_activation_authorized":False,"canonical_blob":BLOB,"canonical_sha256":SHA,"bundles":reports,"cases":out}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("bundles",nargs="+",type=Path);p.add_argument("--json-out",type=Path);a=p.parse_args()
    try: report=merge([analyze_bundle(x.resolve()) for x in a.bundles])
    except Exception as e: print(f"RUNTIME_ANALYZER_FATAL={e}",file=sys.stderr);return 3
    text=json.dumps(report,indent=2,sort_keys=True)
    if a.json_out:a.json_out.parent.mkdir(parents=True,exist_ok=True);a.json_out.write_text(text+"\n",encoding="utf-8")
    print(text);return 2 if report["overall"]=="FAIL" else 0
if __name__=="__main__":raise SystemExit(main())
