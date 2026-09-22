from pathlib import Path
import hashlib,json,re,shutil
root=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\evidence")
base=root/"D1O_503_20260921"
cur=root/"M19_504_101_20260922"
archive=Path(r"D:\BBMA\Workspace\m19-selection-failclosed-101\blueprint\audits\evidence\M19_BUILD504_20260921")
a=(base/"D1O503_SMOKE_202608_tester_newlog.bin").read_text(encoding="cp1252")
b=(cur/"M19504_SMOKE_202608_tester_newlog.bin").read_text(encoding="cp1252")
old=(base/"D1O503_SMOKE_202608.html").read_text(encoding="cp1252")
new=(cur/"M19504_SMOKE_202608.html").read_text(encoding="cp1252")
def cell(label,html):
    m=re.search(r">"+re.escape(label)+r"</td><td[^>]*>(.*?)</td>",html,re.I|re.S)
    return re.sub("<[^>]+>","",m[1]).strip() if m else None
def trace(text,marker):
    return [line[line.index(marker):] for line in text.splitlines() if marker in line]
markers=["[P3M2][M15_COUNTS]","[P3M2][M15_SELECT]","[P3M2][M16_PASS]","[P3M2][DECISION_FINAL]","[P3M2][PREFLIGHT_PASS]","[P3M2][EXEC]","[F7-TELEM] Event=MOMENTUM_HOLD","[F7-TELEM] Event=EXIT_LATCHED","[F7-TELEM] Event=CLOSE_SUCCESS"]
checks={}
for marker in markers:
    x,y=trace(a,marker),trace(b,marker)
    checks[marker]={"baseline_count":len(x),"candidate_count":len(y),"exact_equal":x==y,"baseline_sha256":hashlib.sha256("\n".join(x).encode()).hexdigest(),"candidate_sha256":hashlib.sha256("\n".join(y).encode()).hexdigest()}
result={"baseline_build":"5.03","candidate_build":"5.04","comparisons":checks,
"build_marker":b.count("Build=5.04 BuildTag=V504_M19_SELECTION_FAIL_CLOSED_20260921 SourceRev=M19_SELECTION_FAIL_CLOSED_101_20260921"),
"init_pass":b.count("[P3S1][PASS] EA initialized successfully with 1 pairs"),
"init_failed":b.count("initialization failed (1)"),
"deinit_reason0":b.count("EA deinitialized, reason: 0"),
"every_tick":"Every tick" in new,
"mismatched_chart_errors":cell("Mismatched charts errors",new),
"total_trades":cell("Total trades",new),"baseline_total_trades":cell("Total trades",old),
"fatal_runtime":{s:b.lower().count(s) for s in ["zero divide","array out of range","critical error","unresolved stack function","access violation"]},
"limitation":"Historical smoke does not inject OrderSelect failure; source-extracted host probe proves that fault path. No broker live/demo claim."}
(cur/"ANALYSIS.json").write_text(json.dumps(result,indent=2))
assert all(v["exact_equal"] for v in checks.values()),result
assert result["build_marker"] and result["init_pass"] and result["deinit_reason0"]
assert not result["init_failed"] and result["every_tick"]
assert result["mismatched_chart_errors"]=="0"
assert result["total_trades"]==result["baseline_total_trades"]
assert not any(result["fatal_runtime"].values())
result["acceptance"]="PASS"
(cur/"ANALYSIS.json").write_text(json.dumps(result,indent=2))
shutil.copyfile(cur/"ANALYSIS.json",archive/"SMOKE_ANALYSIS.json")
print(json.dumps(result,indent=2))
