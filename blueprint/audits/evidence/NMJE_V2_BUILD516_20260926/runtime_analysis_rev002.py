from pathlib import Path
import re,json,collections,hashlib,sys

ROOT=Path(r"D:\BBMA\Workspace\q9-nmje-v2-build516-forward-m5-prep-101")
OUT=ROOT/"blueprint/audits/evidence/NMJE_V2_BUILD516_20260926"
LOG=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260926.log")
lines=LOG.read_text(encoding="utf-8",errors="ignore").splitlines()
tag="SourceRev=NMJE_FORWARD_M5_OWNER_PREP_001_20260926"
expert="BBMA_EA_NMJE_V2_516_HARNESS GBPUSD,M15"
starts=[i for i,l in enumerate(lines) if tag in l and expert in l]
if not starts: raise SystemExit("no Build5.16 rev001 marker")
start=starts[-1]; end=None
for i in range(start,len(lines)):
    if expert in lines[i] and "EA deinitialized, reason: 0" in lines[i]:
        end=i; break
if end is None: raise SystemExit("no clean deinit")
seg=lines[start:end+1]; txt="\n".join(seg)

def rows(marker): return [x for x in seg if marker in x]
def kv(line,marker):
    tail=line[line.find(marker):]
    return dict(re.findall(r'(\w+)=([^ ]+)',tail))

execs=[x[x.find("[P3M2][EXEC]"):] for x in rows("[P3M2][EXEC]")]
base=[x.strip() for x in (ROOT/"blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/execution_trace_515_rev001.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
m5=[kv(x,"[Q9-P5-M5-OWNER]") for x in rows("[Q9-P5-M5-OWNER]")]
rels=collections.Counter(r.get("REL") for r in m5)
reasons=collections.Counter(r.get("R") for r in m5)
m5sem=collections.Counter(r.get("M5SEM") for r in m5)
cfopen=[kv(x,"[Q9-P2-CF-OPEN]") for x in rows("[Q9-P2-CF-OPEN]")]
cfout=[kv(x,"[Q9-P2-CF-OUT]") for x in rows("[Q9-P2-CF-OUT]")]
sets=collections.Counter((r.get("Ticket"),r.get("Set")) for r in cfopen)
fatal_patterns=["zero divide","array out of range","stack overflow","access violation",
                "critical runtime error","initialization failed","init_failed"]
fatal={p:txt.lower().count(p) for p in fatal_patterns}
conflict_rows=[x for x in rows("[Q9-P5-M5-OWNER]") if " REL=CONFLICT " in x or "REL=CONFLICT" in x]
broker_actions={"OrderSend_runtime":len(rows("open #")),"OrderClose_runtime":len(rows("close #"))}

summary={
 "schema":"NMJE_V2_BUILD516_RUNTIME_ANALYSIS_V1",
 "source_rev":"NMJE_FORWARD_M5_OWNER_PREP_001_20260926",
 "segment_start_line":start+1,"segment_end_line":end+1,"segment_lines":len(seg),
 "build_identity_count":sum(tag in x for x in seg),
 "clean_deinit":True,
 "execution_count":len(execs),
 "baseline_515_execution_count":len(base),
 "execution_trace_exact_515":execs==base,
 "m5_owner_rows":len(m5),
 "m5_semantic_counts":dict(m5sem),
 "m5_relation_counts":dict(rels),
 "m5_reason_counts":dict(reasons),
 "m5_conflict_rows":len(conflict_rows),
 "cf_open_rows":len(cfopen),"cf_out_rows":len(cfout),"cf_set_count":len(sets),
 "fatal_counts":fatal,
 "runtime_broker_action_lines":broker_actions,
}
checks={
 "build_exact_once":summary["build_identity_count"]==1,
 "clean_deinit":summary["clean_deinit"],
 "execution_trace_exact_515":summary["execution_trace_exact_515"],
 "m5_owner_observed":summary["m5_owner_rows"]>0,
 "m5_semantics_resolved_observed":m5sem.get("Y",0)>0,
 "bounded_relations_observed":all(k in rels for k in ["ALIGNED","SUPPORTING","BUILDING","UNRESOLVED"]),
 "no_m5_conflict_activation":summary["m5_conflict_rows"]==0,
 "no_fatal_runtime":sum(fatal.values())==0,
 "counterfactual_open_out_pairing":len(cfopen)==len(cfout),
}
summary["checks"]=checks
summary["pass"]=all(checks.values())
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"final_runtime_analysis_rev002.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
(OUT/"execution_trace_516_rev002.txt").write_text("\n".join(execs)+"\n",encoding="utf-8")
(OUT/"runtime_rev002_key_rows.log").write_text("\n".join(x for x in seg if any(m in x for m in [
 "[F7-BUILD]","[Q9-NMJE-FWD]","[Q9-P5-M5-OWNER]","[Q9-P2-CF-OPEN]",
 "[Q9-P2-CF-OUT]","[P3M2][EXEC]","EA deinitialized, reason: 0"
]))+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
sys.exit(0 if summary["pass"] else 1)
