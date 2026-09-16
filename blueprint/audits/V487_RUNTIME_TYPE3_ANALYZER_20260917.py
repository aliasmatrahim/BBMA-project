from pathlib import Path
import hashlib, json, re

BASE = Path(__file__).resolve().parent
FILES = {
    "owner_mode1": BASE / "V487_RUNTIME_OWNER_MODE1_AUG2026_20260917.log",
    "fixed_mode1": BASE / "V487_RUNTIME_FIXED_MODE1_AUG2026_20260917.log",
    "fixed_mode2": BASE / "V487_RUNTIME_FIXED_MODE2_AUG2026_20260917.log",
}
OUT = BASE / "V487_RUNTIME_TYPE3_SUMMARY_20260917.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def analyze(path, mode):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    retrace = [x for x in lines if "[Q5T3][RETRACE]" in x]
    confirm = [x for x in lines if "[Q5T3][CONFIRM]" in x]
    tag = f"[P3M{mode}]"
    selects = [x for x in lines if tag + "[M15_SELECT]" in x]
    passes = [x for x in lines if tag + "[M16_PASS]" in x]
    return {
        "lines": len(lines),
        "retrace": len(retrace),
        "retrace_bad": sum("FullClusterFailure=Y" in x for x in retrace),
        "confirm": len(confirm),
        "confirm_bad": sum("Failure=Y" in x for x in confirm),
        "m15_select": len(selects),
        "m16_pass": len(passes),
        "rem_select": sum("Signal=SIGNAL_REM" in x for x in selects),
        "order_markers": sum(bool(re.search(r"OrderSend|deal #|open order", x, re.I)) for x in lines),
        "deinit0": sum("EA deinitialized, reason: 0" in x for x in lines),
        "processed": sum("tick events" in x and "processed" in x for x in lines),
        "sha256": sha(path),
    }

summary = {
    "owner_mode1": analyze(FILES["owner_mode1"], 1),
    "fixed_mode1": analyze(FILES["fixed_mode1"], 1),
    "fixed_mode2": analyze(FILES["fixed_mode2"], 2),
    "negative_case_observed": False,
    "negative_case_claim": "NOT OBSERVED in bounded GBPUSD Aug-2026 runtime; prevention is TDD/static verified",
}

owner = summary["owner_mode1"]
fix1 = summary["fixed_mode1"]
fix2 = summary["fixed_mode2"]
assert owner["retrace"] > 0
assert owner["retrace_bad"] == 0 and owner["confirm_bad"] == 0
assert fix1["retrace"] == owner["retrace"] == fix1["confirm"]
assert fix2["retrace"] == owner["retrace"] == fix2["confirm"]
assert fix1["m15_select"] > 0 and fix1["m16_pass"] == fix1["m15_select"]
assert fix2["m15_select"] > 0 and fix2["m16_pass"] == fix2["m15_select"]
assert fix2["rem_select"] > 0
for item in (owner, fix1, fix2):
    assert item["order_markers"] == 0
    assert item["deinit0"] > 0 and item["processed"] > 0

OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
print("V487_RUNTIME_TYPE3_PACKAGE=PASS")
