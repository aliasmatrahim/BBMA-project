from pathlib import Path
import re,json,hashlib,sys

LOG=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log")
lines=LOG.read_text(encoding="utf-8",errors="ignore").splitlines()
tag="SourceRev=NMJE_P4PLUS_SHADOW_006_20260925"
start_idxs=[i for i,l in enumerate(lines) if "BBMA_EA_NMJE_V2_513_HARNESS GBPUSD,M15" in l and tag in l]
if not start_idxs: raise SystemExit("no rev006 start")
start=start_idxs[-1]
end=None
for i in range(start,len(lines)):
    if "BBMA_EA_NMJE_V2_513_HARNESS GBPUSD,M15" in lines[i] and "EA deinitialized, reason: 0" in lines[i]:
        end=i; break
if end is None: raise SystemExit("no rev006 clean end")
seg=lines[start:end+1]; txt="\n".join(seg)
def rows(s): return [l for l in seg if s in l]
open_rows=rows("[Q9-P4PLUS-OPEN]")
out_rows=rows("[N2-NMJE-OUT]")
exec_rows=rows("[P3M2][EXEC]")
dec_rows=rows("[Q9-P4PLUS-DEC]")
p7_rows=rows("[Q9-P7-DENSITY]")
p8_rows=rows("[Q9-P8-STABILITY]")
fail_rows=rows("[Q9-P4PLUS-PERSIST-FAIL]")

def payload(line):
    p=line.find("[P3M2][EXEC]")
    return line[p:] if p>=0 else line
exec513=[payload(x) for x in exec_rows]
all512=[payload(x) for x in lines if "BBMA_EA_NMJE_V2_512_HARNESS GBPUSD,M15" in x and "[P3M2][EXEC]" in x]
exec512=all512[:14]

def report_fields(path):
    b=Path(path).read_bytes(); t=""
    for enc in ("utf-16le","utf-8","cp1252"):
        try:
            x=b.decode(enc)
            if "<html" in x.lower(): t=x; break
        except: pass
    flat=re.sub(r"<[^>]+>"," ",t).replace("&nbsp;"," ")
    flat=re.sub(r"\s+"," ",flat)
    fields={}
    for lab in ["Total trades","Net profit","Gross profit","Gross loss","Profit factor",
                "Expected payoff","Maximal drawdown","Relative drawdown"]:
        m=re.search(re.escape(lab)+r"\s*:?\s*([\-0-9.,% ()]+)",flat,re.I)
        if m: fields[lab]=m.group(1).strip()
    return {"sha256":hashlib.sha256(b).hexdigest().upper(),"size":len(b),"fields":fields}

r512=report_fields(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2P3_20260925\SMOKE_HARNESS_202608.html")
r513=report_fields(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P4PLUS_20260925\SMOKE_REV006_202608.html")
fatal_patterns=["zero divide","array out of range","stack overflow","access violation","critical runtime error","init_failed","initialization failed"]
fatal={p:txt.lower().count(p) for p in fatal_patterns}
summary={
 "schema":"NMJE_V2_P4PLUS_REV006_RUNTIME_ANALYSIS_V1",
 "source_rev":"NMJE_P4PLUS_SHADOW_006_20260925",
 "segment_start_line":start+1,"segment_end_line":end+1,"segment_lines":len(seg),
 "build_identity_count":sum(tag in x for x in seg),
 "p4_dec_count":len(dec_rows),
 "p4_open_count":len(open_rows),
 "p4_open_durable_count":sum("DUR=Y" in x for x in open_rows),
 "p10_displacement_open_count":sum("DISP=Y" in x for x in open_rows),
 "closed_outcome_count":len(out_rows),
 "closed_outcome_durable_count":sum("DUR=Y" in x for x in out_rows),
 "closed_outcome_dload_count":sum("DLOAD=Y" in x for x in out_rows),
 "closed_outcome_dmatch_count":sum("DMATCH=Y" in x for x in out_rows),
 "closed_outcome_displacement_count":sum("DISP=Y" in x for x in out_rows),
 "p7_density_count":len(p7_rows),
 "p8_stability_count":len(p8_rows),
 "p5_m5_semantic_unresolved_decisions":sum("M5SEM=N" in x for x in dec_rows),
 "p11_lineage_classes":sorted(set(re.findall(r"\bLC=([A-Z_]+)",txt))),
 "persistence_fail_count":len(fail_rows),
 "fatal_counts":fatal,
 "exec_count":len(exec_rows),"baseline_512_exec_count":len(exec512),
 "execution_trace_exact_512":exec513==exec512,
 "report_512":r512,"report_513_rev006":r513,
 "report_fields_equal_512":r512["fields"]==r513["fields"],
}
checks={
 "build_exact_once":summary["build_identity_count"]==1,
 "14_natural_opens":summary["p4_open_count"]==14,
 "all_opens_durable":summary["p4_open_durable_count"]==14,
 "all_opens_displacement":summary["p10_displacement_open_count"]==14,
 "14_closed_outcomes":summary["closed_outcome_count"]==14,
 "all_outcomes_durable":summary["closed_outcome_durable_count"]==14,
 "all_outcomes_reload":summary["closed_outcome_dload_count"]==14,
 "all_outcomes_match":summary["closed_outcome_dmatch_count"]==14,
 "all_outcomes_displacement":summary["closed_outcome_displacement_count"]==14,
 "p7_exercised":summary["p7_density_count"]>0,
 "p8_exercised":summary["p8_stability_count"]>0,
 "p5_m5_semantics_fail_closed":summary["p5_m5_semantic_unresolved_decisions"]==summary["p4_dec_count"],
 "p11_strict_classes_only":set(summary["p11_lineage_classes"]).issubset({"FIRST","NEW_JOURNEY","UNRESOLVED","NONE"}),
 "no_persist_fail":summary["persistence_fail_count"]==0,
 "no_fatal_runtime":sum(fatal.values())==0,
 "execution_trace_exact_512":summary["execution_trace_exact_512"],
 "report_fields_equal_512":summary["report_fields_equal_512"],
}
summary["checks"]=checks; summary["pass"]=all(checks.values())
root=Path(r"D:\BBMA\Workspace\nmje-v2-p4plus-current-owner-101\blueprint\audits\evidence\NMJE_V2_P4PLUS_20260925")
(root/"final_runtime_analysis_rev006.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
(root/"runtime_rev006_segment.log").write_text("\n".join(seg)+"\n",encoding="utf-8")
(root/"execution_trace_513_rev006.txt").write_text("\n".join(exec513)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
sys.exit(0 if summary["pass"] else 1)
