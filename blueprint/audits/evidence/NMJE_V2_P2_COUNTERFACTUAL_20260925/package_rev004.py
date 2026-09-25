from pathlib import Path
import hashlib,json,shutil

root=Path(r"D:\BBMA\Workspace\nmje-v2-counterfactual-p2-101")
ev=root/"blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925"
external_report=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2_COUNTERFACTUAL_20260925\SMOKE_514_REV004_202608.html")
external_log=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log")
production_ex4=Path(r"D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\BBMA_EA_NMJE_V2_514.ex4")
harness_ex4=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_NMJE_V2_514_HARNESS.ex4")
copies={
 "native_compile_rev004.log":Path(r"D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\nmje514_rev004_compile.log"),
 "harness_compile_rev004.log":Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\nmje514_rev004_harness_compile.log"),
}
for name,src in copies.items(): shutil.copy2(src,ev/name)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()

analysis=json.loads((ev/"final_runtime_analysis_rev004.json").read_text(encoding="utf-8"))
manifest={
 "schema":"NMJE_V2_P2_COUNTERFACTUAL_EVIDENCE_MANIFEST_V1",
 "build":"5.14",
 "build_tag":"V514_NMJE_P2_COUNTERFACTUAL_SHADOW_20260925",
 "source_rev":"NMJE_P2_COUNTERFACTUAL_SHADOW_004_20260925",
 "owner_base":"d1-owner-dev@0034f31aced4e630d0b76ce64009a41078ba7cb3",
 "strategy_core_delta":"NONE",
 "authority":"TESTER_ONLY_SHADOW_RESEARCH",
 "engineering_mappings":[
   "baseline actual fill price/time is the common counterfactual entry proxy",
   "candidate-specific semantic SL/TP is resolved through existing approved source logic",
   "paired outcome window uses complete closed M1 bars from baseline fill to baseline close",
   "SELL outcome uses frozen preflight spread as Ask-side proxy",
   "same-M1-bar SL+TP hit is AMBIGUOUS_SAME_M1_BAR",
   "targetless lifecycle candidates remain UNCOMPARABLE_TARGETLESS; no TP is invented"
 ],
 "artifacts":{
   "source_mq4":{"path":"blueprint/source/BBMA_EA.mq4","sha256":sha(root/"blueprint/source/BBMA_EA.mq4")},
   "production_ex4":{"external_path":str(production_ex4),"sha256":sha(production_ex4)},
   "harness_ex4":{"external_path":str(harness_ex4),"sha256":sha(harness_ex4)},
   "native_compile":{"path":"native_compile_rev004.log","sha256":sha(ev/"native_compile_rev004.log")},
   "harness_compile":{"path":"harness_compile_rev004.log","sha256":sha(ev/"harness_compile_rev004.log")},
   "targeted_regression":{"path":"targeted_regression_result.json","sha256":sha(ev/"targeted_regression_result.json")},
   "runtime_analysis":{"path":"final_runtime_analysis_rev004.json","sha256":sha(ev/"final_runtime_analysis_rev004.json")},
   "runtime_key_rows":{"path":"runtime_rev004_key_rows.log","sha256":sha(ev/"runtime_rev004_key_rows.log")},
   "execution_trace":{"path":"execution_trace_514_rev004.txt","sha256":sha(ev/"execution_trace_514_rev004.txt")},
   "tester_report":{"external_path":str(external_report),"sha256":sha(external_report)},
   "tester_log":{"external_path":str(external_log),"sha256":sha(external_log),
                 "bound_segment_lines":[analysis["segment_start_line"],analysis["segment_end_line"]]}
 },
 "runtime_pass":analysis["pass"]
}
(ev/"evidence_manifest_rev004.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")

keep={
 "targeted_regression.py","targeted_regression_result.json",
 "final_runtime_analysis_rev004.py","final_runtime_analysis_rev004.json",
 "runtime_rev004_key_rows.log","execution_trace_514_rev004.txt",
 "native_compile_rev004.log","harness_compile_rev004.log",
 "evidence_manifest_rev004.json","package_rev004.py"
}
for p in ev.iterdir():
    if p.is_file() and p.name not in keep:
        p.unlink()
print(json.dumps(manifest,indent=2))
print("FINAL_FILES")
for p in sorted(ev.iterdir()):
    if p.is_file(): print(p.name,p.stat().st_size)
