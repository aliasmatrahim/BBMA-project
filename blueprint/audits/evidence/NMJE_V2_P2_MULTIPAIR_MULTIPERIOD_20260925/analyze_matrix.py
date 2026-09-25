from pathlib import Path
import re,json,collections,datetime as dt
ROOT=Path(r"D:\BBMA\Workspace\q9-nmje-v2-p2-multipair-evidence-101")
E=ROOT/"blueprint/audits/evidence/NMJE_V2_P2_MULTIPAIR_MULTIPERIOD_20260925"
runs=[]
for p in sorted(E.glob("*_summary.json")):
    if p.name=="matrix_summary.json": continue
    s=json.loads(p.read_text())
    stem=p.name[:-13]
    key=E/f"{stem}_key_rows.log"
    lines=key.read_text(encoding="utf-8",errors="ignore").splitlines()
    def kv(line,marker):
        return dict(re.findall(r'(\w+)=([^ ]+)',line[line.find(marker):]))
    opens=[kv(x,"[Q9-P2-CF-OPEN]") for x in lines if "[Q9-P2-CF-OPEN]" in x]
    outs=[kv(x,"[Q9-P2-CF-OUT]") for x in lines if "[Q9-P2-CF-OUT]" in x]
    f7={}
    f7line={}
    for x in lines:
        if "[F7-TELEM] Event=EXIT_LATCHED" in x:
            d=kv(x,"[F7-TELEM]")
            f7[d.get("Ticket")]=d; f7line[d.get("Ticket")]=x
    outcid={x.get("CID"):x for x in outs}
    parity=[]
    reason_map={"C044_EXIT_FAILED_MOMENTUM":"C044_FAILED_MOMENTUM","C044_EXIT_CYCLE_SUPERSEDED":"C044_CYCLE_SUPERSEDED","C044_EXIT_OPPOSITE_CSM":"C044_OPPOSITE_CSM"}
    for o in [x for x in opens if x.get("Selected")=="Y" and x.get("Targetless")=="Y"]:
        q=outcid.get(o.get("CID"),{})
        a=f7.get(o.get("Ticket"))
        outcome=q.get("Outcome")
        uncmp=bool(outcome and outcome.startswith("UNCOMPARABLE_C044_"))
        rec={"ticket":o.get("Ticket"),"cid":o.get("CID"),"outcome":outcome,"seed_match":o.get("C044SeedMatch"),"owner_tf":int(o.get("OwnerTF") or 0),"canonical_reason":a.get("Reason") if a else None,"comparable":not uncmp}
        if a and q and not uncmp:
            m=re.search(r'LatchCandle=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})',f7line.get(o.get("Ticket"),""))
            expected=0
            if m:
                expected=int(dt.datetime.strptime(m.group(1),"%Y.%m.%d %H:%M").replace(tzinfo=dt.timezone.utc).timestamp())+int(o.get("OwnerTF") or 0)*60
            rec["reason_match"]=reason_map.get(a.get("Reason"))==outcome
            rec["time_match"]=expected>0 and int(q.get("Hit") or 0)==expected
            rec["pass"]=o.get("C044SeedMatch")=="Y" and rec["reason_match"] and rec["time_match"]
        else:
            rec["pass"]=None
        parity.append(rec)
    sets=collections.defaultdict(list)
    for o in opens: sets[(o.get("Ticket"),o.get("Set"))].append(o)
    rel_div=sum(len({x.get("REL") for x in rs})>1 for rs in sets.values())
    srel_div=sum(len({x.get("SREL") for x in rs})>1 for rs in sets.values())
    mat_div=sum(len({x.get("MAT") for x in rs})>1 for rs in sets.values())
    sig_div=sum(len({x.get("Sig") for x in rs})>1 for rs in sets.values())
    pm_div=sum(len({x.get("ParentMatch") for x in rs})>1 for rs in sets.values())
    sd_div=sum(len({x.get("SD") for x in rs})>1 for rs in sets.values())
    runtime_integrity=bool(s["clean_deinit"] and s["open_rows"]==s["out_rows"] and s["duplicate_sets"]==0 and s["selected_count_errors"]==0 and s["pairing_errors"]==0 and s["capacity_skips"]==0 and s["m5_semantic_y"]==0 and s["selected_static_base_match_errors"]==0 and sum(s["fatal_counts"].values())==0)
    s["runtime_integrity_pass"]=runtime_integrity
    s["selected_targetless_parity"]=parity
    s["selected_targetless_comparable"]=sum(x["comparable"] for x in parity)
    s["selected_targetless_comparable_pass"]=sum(x.get("pass") is True for x in parity)
    s["selected_targetless_uncomparable"]=sum(not x["comparable"] for x in parity)
    s["relation_diverse_sets"]=rel_div
    s["structural_relation_diverse_sets"]=srel_div
    s["maturity_diverse_sets"]=mat_div
    s["signal_type_diverse_sets"]=sig_div
    s["parent_match_diverse_sets"]=pm_div
    s["structure_mask_diverse_sets"]=sd_div
    runs.append((s,opens,outs,sets))

allopens=[o for _,op,_,_ in runs for o in op]
allouts=[o for _,_,out,_ in runs for o in out]
outcid={o.get("CID"):o for o in allouts}
alts=[o for o in allopens if o.get("Selected")=="N"]
selected=[o for o in allopens if o.get("Selected")=="Y"]
def cross(rows,key):
    c=collections.defaultdict(collections.Counter)
    for o in rows:
        q=outcid.get(o.get("CID"),{})
        c[o.get(key) or "-"][q.get("Outcome") or "-"]+=1
    return {k:dict(v) for k,v in sorted(c.items())}
def dist(rows,key): return dict(collections.Counter(o.get(key) or "-" for o in rows))
uncomp=[x for s,_,_,_ in runs for x in s["selected_targetless_parity"] if not x["comparable"]]
agg={
 "schema":"NMJE_V2_P2_MULTIPAIR_MULTIPERIOD_ANALYSIS_V2",
 "build":"5.15",
 "owner_head":"459c0588e625d7f7630f0fb5612b7f04fda496de",
 "source_sha256":"B9F3876F61645B2F98009A4251A4142EDC7644ED728E41EDECA245FF1E243C45",
 "scope":"TESTER_ONLY_SHADOW_EVIDENCE_EXPANSION_NO_AUTHORITY_CHANGE",
 "runs":[s for s,_,_,_ in runs],
 "totals":{
  "runs":len(runs),
  "runtime_integrity_pass_runs":sum(s["runtime_integrity_pass"] for s,_,_,_ in runs),
  "raw_equal_cycles":sum(s["raw_equal_cycles"] for s,_,_,_ in runs),
  "executed_cf_sets":sum(s["executed_cf_sets"] for s,_,_,_ in runs),
  "open_rows":len(allopens),"out_rows":len(allouts),
  "selected_rows":len(selected),"alternative_rows":len(alts),
  "selected_targetless_rows":sum(o.get("Selected")=="Y" and o.get("Targetless")=="Y" for o in allopens),
  "alternative_targetless_rows":sum(o.get("Selected")=="N" and o.get("Targetless")=="Y" for o in allopens),
  "selected_targetless_comparable":sum(s["selected_targetless_comparable"] for s,_,_,_ in runs),
  "selected_targetless_comparable_pass":sum(s["selected_targetless_comparable_pass"] for s,_,_,_ in runs),
  "selected_targetless_strict_uncomparable":sum(s["selected_targetless_uncomparable"] for s,_,_,_ in runs),
  "relation_diverse_sets":sum(s["relation_diverse_sets"] for s,_,_,_ in runs),
  "structural_relation_diverse_sets":sum(s["structural_relation_diverse_sets"] for s,_,_,_ in runs),
  "maturity_diverse_sets":sum(s["maturity_diverse_sets"] for s,_,_,_ in runs),
  "signal_type_diverse_sets":sum(s["signal_type_diverse_sets"] for s,_,_,_ in runs),
  "parent_match_diverse_sets":sum(s["parent_match_diverse_sets"] for s,_,_,_ in runs),
  "structure_mask_diverse_sets":sum(s["structure_mask_diverse_sets"] for s,_,_,_ in runs),
  "executions":sum(s["exec_count"] for s,_,_,_ in runs)
 },
 "selected_relation_distribution":dist(selected,"REL"),
 "alternative_relation_distribution":dist(alts,"REL"),
 "selected_signal_distribution":dist(selected,"Sig"),
 "alternative_signal_distribution":dist(alts,"Sig"),
 "alternative_outcomes_by_relation":cross(alts,"REL"),
 "alternative_outcomes_by_signal":cross(alts,"Sig"),
 "selected_outcomes_by_relation":cross(selected,"REL"),
 "selected_targetless_strict_uncomparable_details":uncomp,
 "classification":{
  "runtime_mechanics":"PASS" if all(s["runtime_integrity_pass"] for s,_,_,_ in runs) else "FAIL",
  "selected_targetless_parity":"PASS_FOR_ALL_COMPARABLE" if sum(s["selected_targetless_comparable"] for s,_,_,_ in runs)==sum(s["selected_targetless_comparable_pass"] for s,_,_,_ in runs) else "FAIL",
  "strict_uncomparable_boundary":"RETAIN_FAIL_CLOSED",
  "p2_ordering":"HOLD_NON_EXECUTABLE",
  "strategy_core_delta":"NONE",
  "ea_fix":"NONE"
 }
}
agg["pass"]=agg["classification"]["runtime_mechanics"]=="PASS" and agg["classification"]["selected_targetless_parity"]=="PASS_FOR_ALL_COMPARABLE"
(E/"matrix_analysis_v2.json").write_text(json.dumps(agg,indent=2),encoding="utf-8")
print(json.dumps({"totals":agg["totals"],"selected_relation_distribution":agg["selected_relation_distribution"],"alternative_relation_distribution":agg["alternative_relation_distribution"],"alternative_outcomes_by_relation":agg["alternative_outcomes_by_relation"],"uncomparable":uncomp,"classification":agg["classification"],"pass":agg["pass"]},indent=2))
