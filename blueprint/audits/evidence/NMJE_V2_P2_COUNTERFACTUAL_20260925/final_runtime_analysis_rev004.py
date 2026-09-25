from pathlib import Path
import re,json,collections,hashlib,sys

ROOT=Path(r"D:\BBMA\Workspace\nmje-v2-counterfactual-p2-101")
logp=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log")
lines=logp.read_text(encoding="utf-8",errors="ignore").splitlines()
tag="SourceRev=NMJE_P2_COUNTERFACTUAL_SHADOW_004_20260925"
starts=[i for i,l in enumerate(lines) if tag in l and "BBMA_EA_NMJE_V2_514_HARNESS GBPUSD,M15" in l]
if not starts: raise SystemExit("no rev004 start")
start=starts[-1];end=None
for i in range(start,len(lines)):
    if "BBMA_EA_NMJE_V2_514_HARNESS GBPUSD,M15" in lines[i] and "EA deinitialized, reason: 0" in lines[i]:
        end=i;break
if end is None: raise SystemExit("no clean end")
seg=lines[start:end+1]; txt="\n".join(seg)

def rows(m): return [x for x in seg if m in x]
def kv(line,marker):
    tail=line[line.find(marker):]
    return dict(re.findall(r'(\w+)=([^ ]+)',tail))

open_rows=[kv(x,"[Q9-P2-CF-OPEN]") for x in rows("[Q9-P2-CF-OPEN]")]
out_rows=[kv(x,"[Q9-P2-CF-OUT]") for x in rows("[Q9-P2-CF-OUT]")]
set_rows=[kv(x,"[Q9-P2-CF-SET]") for x in rows("[Q9-P2-CF-SET]")]
execs=[x[x.find("[P3M2][EXEC]"):] for x in rows("[P3M2][EXEC]")]
basep=ROOT/"blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/execution_trace_513_rev006.txt"
base=[x.strip() for x in basep.read_text(encoding="utf-8").splitlines() if x.strip()]

sets=collections.defaultdict(list)
for r in open_rows: sets[(r.get("Ticket"),r.get("Set"))].append(r)
out_by=collections.defaultdict(list)
for r in out_rows: out_by[(r.get("Ticket"),r.get("Set"))].append(r)

# Execution-equivalent duplicate identity includes candidate identity plus
# source-owned protective geometry. Geometry-distinct variants remain valid
# research alternatives even if their sequence identity is otherwise equal.
def execution_key(r):
    return (r.get("Sig"),r.get("Dir"),r.get("Seq"),r.get("Anchor"),r.get("Start"),
            r.get("Src"),r.get("SLTP"),r.get("Targetless"),r.get("SL"),r.get("TP"))

duplicate=[]
selected_errors=[]
pairing_errors=[]
cid_mismatch=[]
for k,rs in sets.items():
    seen=collections.Counter(execution_key(r) for r in rs)
    dups={str(kk):vv for kk,vv in seen.items() if vv>1}
    if dups: duplicate.append((k,dups))
    selected=sum(r.get("Selected")=="Y" for r in rs)
    if selected!=1:selected_errors.append((k,selected))
    outs=out_by.get(k,[])
    if len(outs)!=len(rs):pairing_errors.append((k,len(rs),len(outs)))
    oi=collections.Counter(r.get("CID") for r in rs)
    oo=collections.Counter(r.get("CID") for r in outs)
    if oi!=oo: cid_mismatch.append((k,dict(oi),dict(oo)))

def report_fields(path):
    b=Path(path).read_bytes(); t=""
    for enc in ("utf-16le","utf-8","cp1252"):
        try:
            x=b.decode(enc)
            if "<html" in x.lower():t=x;break
        except: pass
    if not t: raise SystemExit("report decode failed: "+str(path))
    flat=re.sub(r"<[^>]+>"," ",t).replace("&nbsp;"," ")
    flat=re.sub(r"\s+"," ",flat)
    f={}
    for lab in ["Total trades","Net profit","Gross profit","Gross loss","Profit factor",
                "Expected payoff","Maximal drawdown","Relative drawdown"]:
        m=re.search(re.escape(lab)+r"\s*:?\s*([\-0-9.,% ()]+)",flat,re.I)
        if m:f[lab]=m.group(1).strip()
    return {"sha256":hashlib.sha256(b).hexdigest().upper(),"size":len(b),"fields":f}

r514=report_fields(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2_COUNTERFACTUAL_20260925\SMOKE_514_REV004_202608.html")
r513=report_fields(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P4PLUS_20260925\SMOKE_REV006_202608.html")
fatal_patterns=["zero divide","array out of range","stack overflow","access violation",
                "critical runtime error","initialization failed","init_failed"]
fatal={p:txt.lower().count(p) for p in fatal_patterns}

outcomes=collections.Counter(r.get("Outcome") for r in out_rows)
sel_out=collections.Counter(r.get("Outcome") for r in out_rows if r.get("Selected")=="Y")
alt_out=collections.Counter(r.get("Outcome") for r in out_rows if r.get("Selected")=="N")
signals=collections.Counter(r.get("Sig") for r in open_rows)
raw_pending=collections.Counter((r.get("RawEligible"),r.get("Pending")) for r in set_rows)
comparable_alt=sum(v for k,v in alt_out.items() if k and not k.startswith("UNCOMPARABLE_"))
m5_semantic_y=sum(r.get("M5SEM")=="Y" for r in open_rows)

summary={
 "schema":"NMJE_V2_P2_COUNTERFACTUAL_RUNTIME_V2",
 "source_rev":"NMJE_P2_COUNTERFACTUAL_SHADOW_004_20260925",
 "segment_start_line":start+1,"segment_end_line":end+1,"segment_lines":len(seg),
 "build_identity_count":sum(tag in x for x in seg),
 "raw_cf_set_rows":len(set_rows),
 "raw_pending_distribution":{f"{k[0]}->{k[1]}":v for k,v in raw_pending.items()},
 "executed_cf_sets":len(sets),
 "cf_open_rows":len(open_rows),"cf_out_rows":len(out_rows),
 "selected_rows":sum(r.get("Selected")=="Y" for r in open_rows),
 "alternative_rows":sum(r.get("Selected")=="N" for r in open_rows),
 "selected_base_match_y":sum(r.get("Selected")=="Y" and r.get("BaseMatch")=="Y" for r in open_rows),
 "selected_base_match_n":sum(r.get("Selected")=="Y" and r.get("BaseMatch")=="N" for r in open_rows),
 "nonselected_base_match_dash":sum(r.get("Selected")=="N" and r.get("BaseMatch")=="-" for r in open_rows),
 "m5_semantic_y_rows":m5_semantic_y,
 "signals":dict(signals),
 "outcomes_all":dict(outcomes),
 "outcomes_selected":dict(sel_out),
 "outcomes_alternative":dict(alt_out),
 "comparable_alternative_rows":comparable_alt,
 "duplicate_execution_equivalent_sets":len(duplicate),
 "duplicate_details":duplicate,
 "selected_count_errors":selected_errors,
 "open_out_pairing_errors":pairing_errors,
 "cid_pairing_errors":cid_mismatch,
 "exec_count":len(execs),"baseline_exec_count":len(base),
 "execution_trace_exact_513":execs==base,
 "report_514":r514,"report_513":r513,
 "report_fields_equal_513":r514["fields"]==r513["fields"],
 "fatal_counts":fatal,
 "cf_skip_count":len(rows("[Q9-P2-CF-SKIP]")),
}
checks={
 "build_exact_once":summary["build_identity_count"]==1,
 "counterfactual_sets_exercised":summary["executed_cf_sets"]>0,
 "alternatives_exercised":summary["alternative_rows"]>0,
 "comparable_alternative_exercised":summary["comparable_alternative_rows"]>0,
 "open_out_rows_equal":summary["cf_open_rows"]==summary["cf_out_rows"],
 "one_selected_per_set":not selected_errors,
 "all_selected_geometry_match":summary["selected_rows"]==summary["selected_base_match_y"] and summary["selected_base_match_n"]==0,
 "nonselected_basematch_na":summary["alternative_rows"]==summary["nonselected_base_match_dash"],
 "dedup_execution_equivalent":not duplicate,
 "candidate_id_pairing":not cid_mismatch,
 "set_row_pairing":not pairing_errors,
 "no_cf_capacity_skip":summary["cf_skip_count"]==0,
 "no_m5_semantic_inference":summary["m5_semantic_y_rows"]==0,
 "no_fatal_runtime":sum(fatal.values())==0,
 "execution_trace_exact_513":summary["execution_trace_exact_513"],
 "report_fields_equal_513":summary["report_fields_equal_513"],
}
summary["checks"]=checks;summary["pass"]=all(checks.values())
out=ROOT/"blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/final_runtime_analysis_rev004.json"
out.write_text(json.dumps(summary,indent=2),encoding="utf-8")
(ROOT/"blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/runtime_rev004_key_rows.log").write_text(
 "\n".join(x for x in seg if any(m in x for m in [
  "[F7-BUILD]","[Q9-P2-CF-SET]","[Q9-P2-CF-OPEN]","[Q9-P2-CF-OUT]","EA deinitialized, reason: 0"
 ]))+"\n",encoding="utf-8")
(ROOT/"blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/execution_trace_514_rev004.txt").write_text(
 "\n".join(execs)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
sys.exit(0 if summary["pass"] else 1)
