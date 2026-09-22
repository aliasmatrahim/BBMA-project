from pathlib import Path
from datetime import datetime
import subprocess, hashlib, json, shutil, time
repo=Path(r"D:\BBMA\Workspace\m19-selection-failclosed-101")
root=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag")
out=Path(r"D:\BBMA\Compile\M19_504_101")
ev=root/"evidence/M19_504_101_20260922"
archive=repo/"blueprint/audits/evidence/M19_BUILD504_20260921"
ps=r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
def terminals():
    raw=subprocess.check_output([ps,"-NoProfile","-Command","Get-Process terminal -ErrorAction SilentlyContinue | Select-Object Id,Path | ConvertTo-Json -Compress"],text=True).strip()
    data=json.loads(raw) if raw else []
    return data if isinstance(data,list) else [data]
before_processes=terminals()
assert any(p["Id"]==13064 for p in before_processes),"Primary identity changed; inspect first"
assert all(Path(p["Path"])!=root/"terminal.exe" for p in before_processes),"Tester already running"
assert not ev.exists(),"Existing output: inspect/reuse, do not duplicate"
ev.mkdir(parents=True)
cfg=(root/"config/d1o503_gbpusd_smoke_202608.ini").read_text()
cfg=cfg.replace("D1O_503_20260921","M19_504_101_20260922").replace("D1O503_SMOKE_202608","M19504_SMOKE_202608").replace("D1O_503_GBPUSD","M19_504_GBPUSD")
cfg=cfg.replace("#214 Build 5.03 D1O EXTREME_TPW same-identity enrichment","#101 Build 5.04 M19 selection fail-closed")
for setting in ["ProxyEnable=true","ProxyServer=127.0.0.1:1","DataServer=127.0.0.1:1","TestShutdownTerminal=true"]:
    assert setting in cfg
config=root/"config/m19504_gbpusd_smoke_202608.ini"
config.write_text(cfg)
gv=root/"profiles/gvariables.dat"
existed=gv.exists()
original=gv.read_bytes() if existed else b""
(ev/"gvariables.pre.dat").write_bytes(original)
def sha(b): return hashlib.sha256(b).hexdigest()
manifest={"before_sha256":sha(original),"before_bytes":len(original),"existed":existed,"primary_before":before_processes}
(ev/"GV_BEFORE.json").write_text(json.dumps(manifest,indent=2))
tlog=root/("tester/logs/"+datetime.now().strftime("%Y%m%d")+".log")
offset=tlog.stat().st_size if tlog.exists() else 0
proc=None
try:
    proc=subprocess.Popen([str(root/"terminal.exe"),"/portable",r"config\m19504_gbpusd_smoke_202608.ini"],cwd=root,creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)
    (ev/"smoke.pid").write_text(str(proc.pid))
    print("M19504_SMOKE_PID="+str(proc.pid),flush=True)
    try:
        proc.wait(timeout=300)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=20)
        raise RuntimeError("Smoke timeout; only isolated tester terminated")
    print("TESTER_EXIT="+str(proc.returncode),flush=True)
finally:
    if proc is not None and proc.poll() is None:
        proc.terminate()
        proc.wait(timeout=20)
    if tlog.exists():
        raw=tlog.read_bytes()
        assert len(raw)>=offset
        (ev/"M19504_SMOKE_202608_tester_newlog.bin").write_bytes(raw[offset:])
    if existed:
        gv.write_bytes(original)
    elif gv.exists():
        gv.unlink()
    restored=gv.read_bytes() if gv.exists() else b""
    manifest.update({"after_sha256":sha(restored),"after_bytes":len(restored),"bytes_equal":restored==original,"existence_equal":gv.exists()==existed,"primary_after":terminals()})
    assert manifest["bytes_equal"] and manifest["existence_equal"],"Exact GV restoration failed"
    assert any(p["Id"]==13064 for p in manifest["primary_after"]),"Primary process missing"
    assert all(Path(p["Path"])!=root/"terminal.exe" for p in manifest["primary_after"]),"Tester still running"
    (ev/"GV_RESTORE.json").write_text(json.dumps(manifest,indent=2))
    shutil.copyfile(ev/"GV_RESTORE.json",archive/"GV_RESTORE.json")
    print("GV_RESTORE=EXACT "+manifest["after_sha256"],flush=True)
report=ev/"M19504_SMOKE_202608.html"
assert report.exists(),"Report missing"
manifest={"config_sha256":sha(config.read_bytes()),"report_sha256":sha(report.read_bytes()),"log_sha256":sha((ev/"M19504_SMOKE_202608_tester_newlog.bin").read_bytes()),"source_artifacts":"COMPILE_MANIFEST.json"}
(archive/"SMOKE_ARTIFACTS.json").write_text(json.dumps(manifest,indent=2))
print("M19504_SMOKE_CAPTURE=COMPLETE",flush=True)
