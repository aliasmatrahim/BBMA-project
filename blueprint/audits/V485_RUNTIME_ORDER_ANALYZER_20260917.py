from pathlib import Path
import re, json
base = Path(__file__).resolve().parent
run = (base / "V485_RUNTIME_ORDER_HARNESS_RUN_20260917.log").read_text(encoding="utf-8").splitlines()
pat = re.compile(r"\t(2026\.\d\d\.\d\d \d\d:\d\d:\d\d)  ")
def simtime(line):
    m = pat.search(line)
    return m.group(1) if m else None
n1 = [(i, simtime(x)) for i, x in enumerate(run) if "[N1-NMJE]" in x]
reval = [(i, simtime(x)) for i, x in enumerate(run) if "[P3M1][RE_EVAL]" in x]
admit = [(i, simtime(x)) for i, x in enumerate(run) if "[P3M1][RE_ADMIT]" in x]
viol = []
for ri, rt in reval:
    if not any(nt == rt and ni < ri for ni, nt in n1):
        viol.append({"re_eval_line": ri + 1, "time": rt, "reason": "no prior same-time N1"})
summary = {"run_lines": len(run), "n1_count": len(n1), "re_eval_count": len(reval), "re_admit_count": len(admit), "unique_n1_times": len(set(t for _, t in n1)), "ordering_violations": viol, "init_fail_count": sum("initialization failed" in x for x in run), "order_markers": sum(bool(re.search(r"OrderSend|open order|deal #", x, re.I)) for x in run)}
print(json.dumps(summary, indent=2))
expected = json.loads((base / "V485_RUNTIME_ORDER_HARNESS_SUMMARY_20260917.json").read_text(encoding="utf-8"))
assert summary == expected, "packaged summary mismatch"
assert not viol and len(reval) > 0, "runtime ordering validation failed"
print("V485_RUNTIME_ORDER_PACKAGE=PASS")