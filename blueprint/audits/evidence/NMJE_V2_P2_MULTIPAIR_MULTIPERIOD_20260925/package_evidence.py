from pathlib import Path
import hashlib,json
ROOT=Path(r"D:\BBMA\Workspace\q9-nmje-v2-p2-multipair-evidence-101")
E=ROOT/"blueprint/audits/evidence/NMJE_V2_P2_MULTIPAIR_MULTIPERIOD_20260925"
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
files={}
for p in sorted(E.iterdir()):
    if p.is_file() and p.name not in {"evidence_manifest.json"} and p.suffix!=".pyc":
        files[p.name]={"sha256":sha(p),"size":p.stat().st_size}
manifest={
 "schema":"NMJE_V2_P2_MULTIPAIR_MULTIPERIOD_EVIDENCE_MANIFEST_V1",
 "owner_head":"459c0588e625d7f7630f0fb5612b7f04fda496de",
 "build":"5.15",
 "build_tag":"V515_NMJE_P2_TARGETLESS_REPLAY_20260925",
 "source_rev":"NMJE_P2_TARGETLESS_REPLAY_001_20260925",
 "source_sha256":sha(ROOT/"blueprint/source/BBMA_EA.mq4"),
 "harness_ex4":{"external_path":r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_NMJE_V2_515_HARNESS.ex4","sha256":sha(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_NMJE_V2_515_HARNESS.ex4")},
 "strategy_core_delta":"NONE",
 "ea_source_delta":"NONE",
 "p2_ordering":"HOLD_NON_EXECUTABLE",
 "matrix_analysis_pass":json.loads((E/"matrix_analysis_v2.json").read_text())["pass"],
 "artifacts":files
}
(E/"evidence_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps({"artifacts":len(files),"matrix_analysis_pass":manifest["matrix_analysis_pass"],"source_sha256":manifest["source_sha256"]},indent=2))
