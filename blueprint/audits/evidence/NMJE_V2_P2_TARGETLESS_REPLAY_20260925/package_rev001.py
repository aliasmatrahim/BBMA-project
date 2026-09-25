from pathlib import Path
import hashlib,json,shutil

root=Path(r"D:\BBMA\Workspace\nmje-v2-targetless-replay-101")
ev=root/"blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925"
copies={
 "native_compile_rev001.log":Path(r"D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\nmje515_rev001_compile.log"),
 "harness_compile_rev001.log":Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\nmje515_rev001_harness_compile.log"),
}
for n,p in copies.items(): shutil.copy2(p,ev/n)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
analysis=json.loads((ev/"final_runtime_analysis_rev001.json").read_text(encoding="utf-8"))
manifest={
 "schema":"NMJE_V2_P2_TARGETLESS_REPLAY_EVIDENCE_MANIFEST_V1",
 "build":"5.15",
 "build_tag":"V515_NMJE_P2_TARGETLESS_REPLAY_20260925",
 "source_rev":"NMJE_P2_TARGETLESS_REPLAY_001_20260925",
 "owner_base":"d1-owner-dev@ce73919556ec458efd5b1d962b9d7e5cdb348e4a",
 "strategy_core_delta":"NONE",
 "authority":"TESTER_ONLY_SHADOW_RESEARCH",
 "scope":"C044_TARGETLESS_COUNTERFACTUAL_LIFECYCLE_REPLAY",
 "engineering_mappings":[
   "baseline actual fill time/price remains the common counterfactual exposure proxy",
   "canonical C044 owner-timeframe state machine is reused without duplicate detector formulas",
   "complete closed M1 bars provide only hard-SL ordering between owner events",
   "SELL hard-SL replay uses frozen spread as Ask-side proxy",
   "baseline close bounds observation horizon but is not a counterfactual exit rule",
   "D1 TPW targetless lifecycle is excluded while its activation gate remains OFF"
 ],
 "artifacts":{
   "source_mq4":{"path":"blueprint/source/BBMA_EA.mq4","sha256":sha(root/"blueprint/source/BBMA_EA.mq4")},
   "production_ex4":{"external_path":r"D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\BBMA_EA_NMJE_V2_515.ex4","sha256":sha(r"D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\BBMA_EA_NMJE_V2_515.ex4")},
   "harness_ex4":{"external_path":r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_NMJE_V2_515_HARNESS.ex4","sha256":sha(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_NMJE_V2_515_HARNESS.ex4")},
   "native_compile":{"path":"native_compile_rev001.log","sha256":sha(ev/"native_compile_rev001.log")},
   "harness_compile":{"path":"harness_compile_rev001.log","sha256":sha(ev/"harness_compile_rev001.log")},
   "targeted_regression":{"path":"targeted_regression_result.json","sha256":sha(ev/"targeted_regression_result.json")},
   "runtime_analysis":{"path":"final_runtime_analysis_rev001.json","sha256":sha(ev/"final_runtime_analysis_rev001.json")},
   "runtime_key_rows":{"path":"runtime_rev001_key_rows.log","sha256":sha(ev/"runtime_rev001_key_rows.log")},
   "execution_trace":{"path":"execution_trace_515_rev001.txt","sha256":sha(ev/"execution_trace_515_rev001.txt")},
   "tester_report":{"external_path":r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2_TARGETLESS_REPLAY_20260925\SMOKE_515_REV001_202608.html","sha256":sha(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence\NMJE_V2_P2_TARGETLESS_REPLAY_20260925\SMOKE_515_REV001_202608.html")},
   "tester_log":{"external_path":r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log","sha256":sha(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log"),"bound_segment_lines":[analysis["segment_start_line"],analysis["segment_end_line"]]}
 },
 "runtime_pass":analysis["pass"]
}
(ev/"evidence_manifest_rev001.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
