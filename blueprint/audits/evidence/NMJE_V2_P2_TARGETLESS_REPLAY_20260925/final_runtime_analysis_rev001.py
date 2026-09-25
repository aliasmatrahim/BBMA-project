from pathlib import Path
import re,json,collections,hashlib,sys

ROOT=Path(r"D:\BBMA\Workspace\nmje-v2-targetless-replay-101")
OUT=ROOT/"blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925"
LOG=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log")
lines=LOG.read_text(encoding="utf-8",errors="ignore").splitlines()
tag="SourceRev=NMJE_P2_TARGETLESS_REPLAY_001_20260925"
starts=[i for i,l in enumerate(lines) if tag in l and "BBMA_EA_NMJE_V2_515_HARNESS GBPUSD,M15" in l]
if not starts: raise SystemExit("no Build5.15 rev001 start")
start=starts[-1]; end=None
for i in range(start,len(lines)):
    if "BBMA_EA_NMJE_V2_515_HARNESS GBPUSD,M15" in lines[i] and "EA deinitialized, reason: 0" in lines[i]:
        end=i; break
if end is None: raise SystemExit("no clean deinit")
seg=lines[start:end+1]; txt="\n".join(seg)

def rows(m): return [x for x in seg if m in x]
def kv(line,marker):
    tail=line[line.find(marker):]
    return dict(re.findall(r'(\w+)=([^ ]+)',tail))

opens=[kv(x,"[Q9-P2-CF-OPEN]") for x in rows("[Q9-P2-CF-OPEN]")]
outs=[kv(x,"[Q9-P2-CF-OUT]") for x in rows("[Q9-P2-CF-OUT]")]
sets=collections.defaultdict(list); out_by=collections.defaultdict(list)
for r in opens: sets[(r.get("Ticket"),r.get("Set"))].append(r)
for r in outs: out_by[(r.get("Ticket"),r.get("Set"))].append(r)

dup=[]; selerr=[]; pairerr=[]; ciderr=[]
def exec_key(r):
    return (r.get("Sig"),r.get("Dir"),r.get("Seq"),r.get("Anchor"),r.get("Start"),
            r.get("Src"),r.get("SLTP"),r.get("Targetless"),r.get("SL"),r.get("TP"))
for k,rs in sets.items():
    c=collections.Counter(exec_key(r) for r in rs)
    if any(v>1 for v in c.values()): dup.append((k,{str(x):v for x,v in c.items() if v>1}))
    n=sum(r.get("Selected")=="Y" for r in rs)
    if n!=1: selerr.append((k,n))
    ors=out_by.get(k,[])
    if len(ors)!=len(rs): pairerr.append((k,len(rs),len(ors)))
    if collections.Counter(r.get("CID") for r in rs)!=collections.Counter(r.get("CID") for r in ors):
        ciderr.append(k)

# Parse canonical F7 selected targetless latches and compare to shadow replay.
f7={}
for line in rows("[F7-TELEM] Event=EXIT_LATCHED"):
    d=kv(line,"[F7-TELEM]")
    t=d.get("Ticket")
    if t: f7[t]=d
out_by_cid={r.get("CID"):r for r in outs}
selected_targetless=[r for r in opens if r.get("Selected")=="Y" and r.get("Targetless")=="Y"]
parity=[]
reason_map={
 "C044_EXIT_FAILED_MOMENTUM":"C044_FAILED_MOMENTUM",
 "C044_EXIT_CYCLE_SUPERSEDED":"C044_CYCLE_SUPERSEDED",
 "C044_EXIT_OPPOSITE_CSM":"C044_OPPOSITE_CSM",
}
for r in selected_targetless:
    actual=f7.get(r.get("Ticket"))
    shadow=out_by_cid.get(r.get("CID"))
    owner_tf=int(r.get("OwnerTF") or 0)
    latch_open=int(actual.get("LatchCandle") or 0) if actual and (actual.get("LatchCandle") or "").isdigit() else 0
    # F7 TimeToString fields are not numeric; derive canonical owner-candle open
    # from the 'Candle=' / 'LatchCandle=' textual timestamp by parsing log time context below.
    actual_line=next((x for x in rows("[F7-TELEM] Event=EXIT_LATCHED")
                      if "Ticket="+str(r.get("Ticket"))+" " in x), "")
    m=re.search(r'LatchCandle=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})',actual_line)
    import datetime as _dt
    latch_epoch=0
    if m:
        latch_epoch=int(_dt.datetime.strptime(m.group(1),"%Y.%m.%d %H:%M").replace(tzinfo=_dt.timezone.utc).timestamp())
    expected_hit=latch_epoch + owner_tf*60 if latch_epoch and owner_tf else 0
    parity.append({
      "ticket":r.get("Ticket"),"cid":r.get("CID"),"seed_match":r.get("C044SeedMatch"),
      "owner_tf":owner_tf,
      "canonical_reason":actual.get("Reason") if actual else None,
      "shadow_outcome":shadow.get("Outcome") if shadow else None,
      "shadow_hit":int(shadow.get("Hit") or 0) if shadow else 0,
      "expected_event_time":expected_hit,
      "reason_match":bool(actual and shadow and reason_map.get(actual.get("Reason"))==shadow.get("Outcome")),
      "time_match":bool(actual and shadow and expected_hit>0 and int(shadow.get("Hit") or 0)==expected_hit),
    })

execs=[x[x.find("[P3M2][EXEC]"):] for x in rows("[P3M2][EXEC]")]
base=[x.strip() for x in (ROOT/"blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/execution_trace_514_rev004.txt").read_text(encoding="utf-8").splitlines() if x.strip()]

def report_fields(path):
    b=Path(path).read_bytes(); t=""
    for enc in ("utf-16le","utf-8","cp1252"):
        try:
            x=b.decode(enc)
            if "<html" in x.lower(): t=x; break
        except: pass
    if not t: raise SystemExit("cannot decode "+str(path))
    flat=re.sub(r"<[^>]+>"," ",t).replace("&nbsp;"," ")
    flat=re.sub(r"\s+"," ",flat)
    f={}
    for lab in ["Total trades","Net profit","Gross profit","Gross loss","Profit factor",
                "Expected payoff","Maximal drawdown","Relative drawdown"]:
        m=re.search(re.escape(lab)+r"\s*:?\s*([\-0-9.,% ()]+)",flat,re.I)
        if m:f[lab]=m.group(1).strip()
    return {"sha256":hashlib.sha256(b).hexdigest().upper(),"size":len(b),"fields":f}

r515=report_fields(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2_TARGETLESS_REPLAY_20260925\SMOKE_515_REV001_202608.html")
r514=report_fields(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2_COUNTERFACTUAL_20260925\SMOKE_514_REV004_202608.html")

fatal_patterns=["zero divide","array out of range","stack overflow","access violation",
                "critical runtime error","initialization failed","init_failed"]
fatal={p:txt.lower().count(p) for p in fatal_patterns}
alt_targetless_out=[r for r in outs if r.get("Selected")=="N" and r.get("CID") in
                    {x.get("CID") for x in opens if x.get("Selected")=="N" and x.get("Targetless")=="Y"}]
outcome_counts=collections.Counter(r.get("Outcome") for r in outs)
alt_targetless_counts=collections.Counter(r.get("Outcome") for r in alt_targetless_out)

summary={
 "schema":"NMJE_V2_P2_TARGETLESS_REPLAY_RUNTIME_V1",
 "source_rev":"NMJE_P2_TARGETLESS_REPLAY_001_20260925",
 "segment_start_line":start+1,"segment_end_line":end+1,"segment_lines":len(seg),
 "build_identity_count":sum(tag in x for x in seg),
 "executed_cf_sets":len(sets),"cf_open_rows":len(opens),"cf_out_rows":len(outs),
 "selected_rows":sum(r.get("Selected")=="Y" for r in opens),
 "alternative_rows":sum(r.get("Selected")=="N" for r in opens),
 "selected_targetless_rows":len(selected_targetless),
 "selected_targetless_seed_match_y":sum(r.get("C044SeedMatch")=="Y" for r in selected_targetless),
 "alternative_targetless_rows":sum(r.get("Selected")=="N" and r.get("Targetless")=="Y" for r in opens),
 "alternative_targetless_replay_present":sum(r.get("Selected")=="N" and r.get("Targetless")=="Y" and r.get("C044R")=="Y" for r in opens),
 "alternative_targetless_outcomes":dict(alt_targetless_counts),
 "all_outcomes":dict(outcome_counts),
 "selected_c044_parity":parity,
 "duplicate_execution_equivalent_sets":len(dup),"duplicate_details":dup,
 "selected_count_errors":selerr,"open_out_pairing_errors":pairerr,"cid_pairing_errors":ciderr,
 "cf_skip_count":len(rows("[Q9-P2-CF-SKIP]")),
 "m5_semantic_y_rows":sum(r.get("M5SEM")=="Y" for r in opens),
 "exec_count":len(execs),"baseline_exec_count":len(base),"execution_trace_exact_514":execs==base,
 "report_515":r515,"report_514":r514,"report_fields_equal_514":r515["fields"]==r514["fields"],
 "fatal_counts":fatal,
}
checks={
 "build_exact_once":summary["build_identity_count"]==1,
 "same_three_cf_sets":summary["executed_cf_sets"]==3,
 "open_out_pairing_exact":summary["cf_open_rows"]==summary["cf_out_rows"] and not pairerr and not ciderr,
 "one_selected_per_set":not selerr,
 "no_execution_equivalent_duplicates":not dup,
 "selected_targetless_seed_match":summary["selected_targetless_rows"]>0 and summary["selected_targetless_rows"]==summary["selected_targetless_seed_match_y"],
 "all_alt_targetless_have_replay":summary["alternative_targetless_rows"]>0 and summary["alternative_targetless_rows"]==summary["alternative_targetless_replay_present"],
 "alt_targetless_no_legacy_uncomparable":sum(v for k,v in alt_targetless_counts.items() if k and k.startswith("UNCOMPARABLE_TARGETLESS"))==0,
 "selected_c044_reason_time_parity":len(parity)>0 and all(x["seed_match"]=="Y" and x["reason_match"] and x["time_match"] for x in parity),
 "no_cf_capacity_skip":summary["cf_skip_count"]==0,
 "no_m5_semantic_inference":summary["m5_semantic_y_rows"]==0,
 "no_fatal_runtime":sum(fatal.values())==0,
 "execution_trace_exact_514":summary["execution_trace_exact_514"],
 "report_fields_equal_514":summary["report_fields_equal_514"],
}
summary["checks"]=checks; summary["pass"]=all(checks.values())
(OUT/"final_runtime_analysis_rev001.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
(OUT/"runtime_rev001_key_rows.log").write_text("\n".join(x for x in seg if any(m in x for m in [
 "[F7-BUILD]","[Q9-P2-CF-OPEN]","[Q9-P2-CF-OUT]","[F7-TELEM] Event=EXIT_LATCHED","EA deinitialized, reason: 0"
]))+"\n",encoding="utf-8")
(OUT/"execution_trace_515_rev001.txt").write_text("\n".join(execs)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
sys.exit(0 if summary["pass"] else 1)
