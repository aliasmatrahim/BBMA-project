from __future__ import annotations

import argparse, hashlib, itertools, json, re, shutil, subprocess, time
from pathlib import Path

BUILD = "5.19"
BUILD_TAG = "V519_NMJE_CURRENT_CANDIDATE_LIFECYCLE_20260926"
HARNESS_SHA = "22F1525B04DB37B2B5BB6594ADED4E1F2041EB87F0AE299FD8C1B33EA8FB049E"
HST_SHA = {
    1:"64D5BED21B61CC119507FD552D6A86091B2CF4A580EEFB5C589AA97654F56019",
    5:"6F7A16A1A6BDAF6F6871F56AF399530974C2429D51E35F7584D37A2A88EC549D",
    15:"74DB0196F4D77FC66548CD41614ADFDDE9CA96F9E2DA91DAEBCD17E304C5E7B5",
    60:"566762B35FCE7EF2DCB5985A57DAC6BC5D0476A6A76DDEF2D680EF0905632389",
    240:"AA58B7E1114D20B135573168FD414DB7F210AB260427C8596CADFB8052E5015F",
    1440:"6EE8DED5B0027A2340D15196F34DA603899D648A772919AF6FACD156F81800AC",
}
PERIODS = {
    "TRAIN":("2025.09.01","2026.03.01"),
    "OOS":("2026.03.01","2026.05.01"),
    "HOLDOUT":("2026.05.01","2026.07.01"),
    "ROBUST":("2026.07.01","2026.09.01"),
}
BASE = {
    "EntryMode":"2","PairList":"GBPUSD","MaxTradePerPair":"2","MaxTotalTrade":"2","MaxActivePair":"1",
    "MMMode":"2","AutoLotPercent":"1.0","FixedLot":"0.01","MaxAutoLot":"1.0","TradeLockMode":"0",
    "MaxSpreadPips":"10.0","MaxDrawdownPercent":"20.0","BasketLossPercent":"10.0","MaxTotalRiskPercent":"5.0",
    "ShowDashboard":"false","MinRRRatio":"0.0","BlockNMJEConflict":"true","BlockNMJEBuilding":"true",
    "EnableNMJEForwardEvidence":"true","EnableNMJESelectionPolicy":"true","MaxSLPips":"100.0","Slippage":"3",
    "DebugLevel":"4","StrategyID":"99","InstanceID":"99",
}
FATAL = ("zero divide","array out of range","critical error","unresolved stack function","access violation")

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

def verify_history(root: Path) -> dict:
    out={}
    for tf, expected in HST_SHA.items():
        p=root/"history"/"MetaQuotes-Demo"/f"GBPUSD{tf}.hst"
        if not p.is_file(): raise RuntimeError(f"missing history: {p}")
        actual=sha(p)
        if actual!=expected: raise RuntimeError(f"GBPUSD{tf} hash mismatch: {actual}")
        out[str(tf)]={"path":str(p),"sha256":actual}
    return out

def find_harness(root: Path, explicit: Path|None) -> Path:
    dirs=[root/"MQL4"/"Experts",Path(r"D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts")]
    candidates=[explicit] if explicit else []
    for d in dirs:
        if d.exists(): candidates += list(d.glob("*.ex4"))
    for p in candidates:
        if p and p.is_file() and sha(p)==HARNESS_SHA: return p
    raise RuntimeError("exact Build 5.19 harness EX4 not found by SHA-256")

def setfile(path: Path, vals: dict) -> None:
    path.write_text("\n".join(f"{k}={v}" for k,v in vals.items())+"\n",encoding="utf-8",newline="\n")

def snap_logs(root: Path) -> dict[str,int]:
    out={}
    for d in (root/"tester"/"logs",root/"MQL4"/"Logs",root/"logs"):
        if d.exists():
            for p in d.glob("*"):
                if p.is_file(): out[str(p)]=p.stat().st_size
    return out

def log_delta(root: Path, before: dict[str,int]) -> tuple[str,list[dict]]:
    text=[]; meta=[]; seen=set()
    for d in (root/"tester"/"logs",root/"MQL4"/"Logs",root/"logs"):
        if not d.exists(): continue
        for p in d.glob("*"):
            if not p.is_file() or str(p) in seen: continue
            seen.add(str(p)); start=before.get(str(p),0); raw=p.read_bytes()[start:]
            if not raw: continue
            try: s=raw.decode("utf-8")
            except UnicodeError: s=raw.decode("cp1252",errors="ignore")
            text.append(s); meta.append({"path":str(p),"delta_bytes":len(raw)})
    return "\n".join(text),meta

def report_text(path: Path) -> str:
    raw=path.read_bytes()
    for enc in ("utf-16","utf-8","cp1252"):
        try: s=raw.decode(enc); break
        except UnicodeError: pass
    else: s=raw.decode("cp1252",errors="ignore")
    s=re.sub(r"(?s)<[^>]+>"," ",s).replace("&nbsp;"," ").replace("&amp;","&")
    return re.sub(r"\s+"," ",s)

def num(label: str, text: str):
    m=re.search(re.escape(label)+r"\s*:?\s*(-?\d[\d,]*(?:\.\d+)?)",text,re.I)
    return None if not m else float(m.group(1).replace(",",""))

def drawdown(label: str, text: str):
    m=re.search(re.escape(label)+r"\s*:?\s*(-?\d[\d,]*(?:\.\d+)?)\s*(?:\(([\d.]+)%\))?",text,re.I)
    return (None,None) if not m else (float(m.group(1).replace(",","")),float(m.group(2)) if m.group(2) else None)

def parse_report(path: Path) -> dict:
    t=report_text(path)
    md,mdp=drawdown("Maximal drawdown",t)
    rdm=re.search(r"Relative drawdown\\s*:?\\s*([\\d.]+)%\\s*\\(([-\\d,.]+)\\)",t,re.I)
    rdp=float(rdm.group(1)) if rdm else None
    vals={"net_profit":num("Total net profit",t),"profit_factor":num("Profit factor",t),"total_trades":num("Total trades",t),
          "max_drawdown_abs":md,"max_drawdown_pct":mdp,"relative_drawdown_pct":rdp,"initial_deposit":num("Initial deposit",t)}
    if any(vals[k] is None for k in ("net_profit","profit_factor","total_trades","max_drawdown_abs")):
        raise RuntimeError(f"report parse failed: {path}")
    vals["total_trades"]=int(vals["total_trades"]); return vals

def cfg(expert,setname,period,report):
    a,b=PERIODS[period]
    return "\n".join(["ExpertsEnable=true","ExpertsTrades=true","ExpertsDllImport=false","ExpertsExpImport=false",
        f"TestExpert={expert}",f"TestExpertParameters={setname}","TestSymbol=GBPUSD","TestPeriod=M15","TestModel=0","TestSpread=20",
        "TestOptimization=false","TestDateEnable=true",f"TestFromDate={a}",f"TestToDate={b}",f"TestReport={report}",
        "TestReplaceReport=true","TestShutdownTerminal=true","TestVisualEnable=false",""])

def sig(vals: dict) -> str:
    keys=("EntryMode","TradeLockMode","MaxTradePerPair","MinRRRatio","MaxSLPips","MMMode","AutoLotPercent")
    return "_".join(f"{k}{vals[k]}" for k in keys).replace(".","p")

def run(root: Path, expert: str, out: Path, tag: str, period: str, vals: dict, timeout: int) -> dict:
    tester=root/"tester"; tester.mkdir(exist_ok=True); (root/"config").mkdir(exist_ok=True)
    setname=f"opt519_{tag}.set"; setfile(tester/setname,vals)
    rel=rf"tester\opt519_reports\{tag}_{period}.htm"; report=root/rel; report.parent.mkdir(parents=True,exist_ok=True)
    if report.exists(): report.unlink()
    c=root/"config"/f"opt519_{tag}_{period}.ini"; c.write_text(cfg(expert,setname,period,rel),encoding="utf-8",newline="\n")
    before=snap_logs(root); start=time.time()
    p=subprocess.Popen([str(root/"terminal.exe"),"/portable",str(c)],cwd=str(root),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try: p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill(); p.wait(timeout=30); raise RuntimeError(f"timeout {tag} {period}")
    if not report.is_file(): raise RuntimeError(f"missing report {report}")
    logs,logmeta=log_delta(root,before); low=logs.lower()
    dids=re.findall(r"\[P3M[12]\]\[EXEC\].*?DecisionID=(.*?)\s+Signal=",logs)
    tickets=re.findall(r"\[P3M[12]\]\[EXEC\]\s+Ticket=(\d+)",logs)
    safety={"fatal":{x:low.count(x) for x in FATAL},"duplicate_decision_ids":len(dids)-len(set(dids)),
            "duplicate_tickets":len(tickets)-len(set(tickets)),"exec_count":len(tickets),
            "nmje_active":"[N3-NMJE-POLICY] Mode=ACTIVE" in logs,"build519":f"Build={BUILD}" in logs and BUILD_TAG in logs}
    r={"tag":tag,"period":period,"inputs":vals,"metrics":parse_report(report),"safety":safety,
       "elapsed_sec":round(time.time()-start,2),"report":str(report),"report_sha256":sha(report),"log_delta":logmeta}
    (out/f"{tag}_{period}.json").write_text(json.dumps(r,indent=2),encoding="utf-8"); return r

def clean(r: dict, min_trades=20) -> bool:
    s=r["safety"]
    return (
        s["build519"]
        and s["nmje_active"]
        and all(v==0 for v in s["fatal"].values())
        and s["duplicate_decision_ids"]==0
        and s["duplicate_tickets"]==0
        and s["exec_count"] == r["metrics"]["total_trades"]
        and r["metrics"]["total_trades"]>=min_trades
    )

def key(r: dict):
    m=r["metrics"]; dd=m["relative_drawdown_pct"] or m["max_drawdown_pct"] or 999.0
    return (m["net_profit"],m["profit_factor"],-dd)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag")); ap.add_argument("--harness",type=Path)
    ap.add_argument("--out",type=Path,default=Path(r"D:\BBMA\OPT_BUILD519_GBPUSD")); ap.add_argument("--timeout",type=int,default=1800); ap.add_argument("--dry-run",action="store_true"); a=ap.parse_args()
    if not (a.root/"terminal.exe").is_file(): raise RuntimeError("isolated MT4 tester terminal missing")
    history=verify_history(a.root); source=find_harness(a.root,a.harness); dst=a.root/"MQL4"/"Experts"/"BBMA_EA_BUILD519_OPT_HARNESS.ex4"
    if source.resolve()!=dst.resolve(): shutil.copy2(source,dst)
    if sha(dst)!=HARNESS_SHA: raise RuntimeError("harness hash mismatch")
    a.out.mkdir(parents=True,exist_ok=True)
    pre={"build":BUILD,"tag":BUILD_TAG,"pair":"GBPUSD","harness":str(dst),"harness_sha256":sha(dst),"history":history,"periods":PERIODS,
         "class":"ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE"}
    (a.out/"PRECHECK.json").write_text(json.dumps(pre,indent=2),encoding="utf-8")
    structural=[]
    for entry,lock,mx in itertools.product((1,2),(0,1,2),(1,2)):
        v=BASE.copy(); v.update(EntryMode=str(entry),TradeLockMode=str(lock),MaxTradePerPair=str(mx),MaxTotalTrade=str(mx)); structural.append(v)
    if a.dry_run:
        print(json.dumps({"precheck":pre,"structural":structural,"filter":{"MinRRRatio":[0,1,1.5],"MaxSLPips":[60,80,100,120]},"risk":[0.25,0.5,1,1.5,2]},indent=2)); return 0
    s1=[run(a.root,dst.stem,a.out,f"S1_{i:02d}_{sig(v)}","TRAIN",v,a.timeout) for i,v in enumerate(structural,1)]
    top3=sorted([r for r in s1 if clean(r)],key=key,reverse=True)[:3]
    if not top3: raise RuntimeError("no clean Stage-1 candidate")
    s2=[]
    for base in top3:
        for rr,sl in itertools.product((0.0,1.0,1.5),(60.0,80.0,100.0,120.0)):
            v=base["inputs"].copy(); v.update(MinRRRatio=str(rr),MaxSLPips=str(sl))
            s2.append(run(a.root,dst.stem,a.out,f"S2_{len(s2)+1:02d}_{sig(v)}","TRAIN",v,a.timeout))
    top5=sorted([r for r in s2 if clean(r)],key=key,reverse=True)[:5]
    oos=[run(a.root,dst.stem,a.out,f"S3_{i:02d}_{sig(r['inputs'])}","OOS",r["inputs"],a.timeout) for i,r in enumerate(top5,1)]
    oos=[r for r in oos if clean(r,10) and r["metrics"]["net_profit"]>0]
    top_oos=sorted(oos,key=key,reverse=True)[:3]
    if not top_oos: raise RuntimeError("NO ROBUST WINNER: no positive clean OOS candidate")
    hold=[run(a.root,dst.stem,a.out,f"S4_{i:02d}_{sig(r['inputs'])}","HOLDOUT",r["inputs"],a.timeout) for i,r in enumerate(top_oos,1)]
    hold=[r for r in hold if clean(r,10) and r["metrics"]["net_profit"]>0]
    if not hold: raise RuntimeError("NO ROBUST WINNER: no positive clean holdout candidate")
    structure=max(hold,key=key)["inputs"]
    risk=[]
    for pct in (0.25,0.5,1.0,1.5,2.0):
        v=structure.copy(); v.update(MMMode="1",AutoLotPercent=str(pct))
        rows=[run(a.root,dst.stem,a.out,f"S5_R{pct}_{sig(v)}",p,v,a.timeout) for p in ("OOS","HOLDOUT")]
        if all(clean(x,10) and x["metrics"]["net_profit"]>0 for x in rows):
            dd=max((x["metrics"]["relative_drawdown_pct"] or x["metrics"]["max_drawdown_pct"] or 999.0) for x in rows)
            risk.append({"risk":pct,"profit":sum(x["metrics"]["net_profit"] for x in rows),"worst_dd_pct":dd,"rows":rows})
    eligible=[x for x in risk if x["worst_dd_pct"]<=10.0]
    if not eligible: raise RuntimeError("NO ROBUST WINNER: no sizing candidate <=10% worst DD")
    rw=max(eligible,key=lambda x:(x["profit"],-x["worst_dd_pct"])); final=structure.copy(); final.update(MMMode="1",AutoLotPercent=str(rw["risk"]))
    robust=run(a.root,dst.stem,a.out,f"S6_FINAL_{sig(final)}","ROBUST",final,a.timeout)
    result={"classification":"ENGINEERING OPTIMIZATION RESULT / NOT STRATEGY CORE / NOT PRODUCTION AUTHORITY","structural":structure,"risk":rw,
            "final_inputs":final,"robust":robust,"pass":clean(robust,10) and robust["metrics"]["net_profit"]>0,
            "selection":"maximize OOS+holdout profit under positive OOS/holdout, clean runtime, zero duplicates, <=10% worst relative DD, then untouched Jul-Aug positive robustness"}
    (a.out/"FINAL_RESULT.json").write_text(json.dumps(result,indent=2),encoding="utf-8"); print(json.dumps(result,indent=2)); return 0 if result["pass"] else 2

if __name__=="__main__": raise SystemExit(main())