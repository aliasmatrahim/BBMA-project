from pathlib import Path
import hashlib, json, re

BASE = Path(__file__).resolve().parent
FILES = {
    "owner_mode1_jul": BASE / "V487_RUNTIME_OWNER_MODE1_JUL2026_20260917.log",
    "owner_mode2_jul": BASE / "V487_RUNTIME_OWNER_MODE2_JUL2026_20260917.log",
    "fixed_mode1_jul": BASE / "V487_RUNTIME_FIXED_MODE1_JUL2026_20260917.log",
    "fixed_mode2_jul": BASE / "V487_RUNTIME_FIXED_MODE2_JUL2026_20260917.log",
    "owner_mode1_aug": BASE / "V487_RUNTIME_OWNER_MODE1_AUG2026_20260917.log",
    "fixed_mode1_aug": BASE / "V487_RUNTIME_FIXED_MODE1_AUG2026_20260917.log",
    "fixed_mode2_aug": BASE / "V487_RUNTIME_FIXED_MODE2_AUG2026_20260917.log",
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
    eval_by_type, admit_by_type = {}, {}
    for typ in ("RE_TYPE_1", "RE_TYPE_2", "RE_TYPE_3_CSM", "RE_TYPE_4_CSD"):
        eval_by_type[typ] = sum("[P3M1][RE_EVAL]" in x and f"Type={typ}" in x for x in lines)
        admit_by_type[typ] = sum("[P3M1][RE_ADMIT]" in x and f"Type={typ}" in x for x in lines)
    return {
        "lines": len(lines),
        "retrace": len(retrace),
        "retrace_bad": sum("FullClusterFailure=Y" in x for x in retrace),
        "confirm": len(confirm),
        "confirm_bad": sum("Failure=Y" in x for x in confirm),
        "confirm_valid": sum("Failure=N" in x for x in confirm),
        "m15_select": len(selects),
        "m16_pass": len(passes),
        "rem_select": sum("Signal=SIGNAL_REM" in x for x in selects),
        "eval_by_type": eval_by_type,
        "admit_by_type": admit_by_type,
        "order_markers": sum(bool(re.search(r"OrderSend|deal #|open order", x, re.I)) for x in lines),
        "deinit0": sum("EA deinitialized, reason: 0" in x for x in lines),
        "processed": sum("tick events" in x and "processed" in x for x in lines),
        "sha256": sha(path),
    }

summary = {name: analyze(path, 2 if "mode2" in name else 1) for name, path in FILES.items()}
summary["negative_case_observed"] = True
summary["negative_case"] = {
    "pair": "GBPUSD", "timeframe": "M15", "validation_candle": "2026.07.13 12:15",
    "direction": "BUY", "close": 1.33898, "ma5_low": 1.33909, "ma10_low": 1.33904,
    "owner_confirmed_invalid": True, "fixed_mode1_confirmed_invalid": False,
    "fixed_mode2_confirmed_invalid": False,
}

o1=summary["owner_mode1_jul"]; o2=summary["owner_mode2_jul"]
f1=summary["fixed_mode1_jul"]; f2=summary["fixed_mode2_jul"]
ao=summary["owner_mode1_aug"]; af=summary["fixed_mode1_aug"]; af2=summary["fixed_mode2_aug"]
assert o1["retrace_bad"] == 1 and o1["confirm_bad"] == 1
assert o2["retrace_bad"] == 1 and o2["confirm_bad"] == 1
assert f1["retrace_bad"] == 1 and f1["confirm_bad"] == 0
assert f2["retrace_bad"] == 1 and f2["confirm_bad"] == 0
assert f1["confirm"] == o1["confirm"] - 1 and f2["confirm"] == o2["confirm"] - 1
assert o2["m15_select"] == f2["m15_select"] and o2["m16_pass"] == f2["m16_pass"]
for typ in ("RE_TYPE_1", "RE_TYPE_3_CSM", "RE_TYPE_4_CSD"):
    assert o1["eval_by_type"][typ] == f1["eval_by_type"][typ]
    assert o1["admit_by_type"][typ] == f1["admit_by_type"][typ]
assert o1["eval_by_type"]["RE_TYPE_2"] == f1["eval_by_type"]["RE_TYPE_2"] == 0
assert o1["admit_by_type"]["RE_TYPE_2"] == f1["admit_by_type"]["RE_TYPE_2"] == 0
assert ao["retrace_bad"] == af["retrace_bad"] == af2["retrace_bad"] == 0
assert ao["confirm_bad"] == af["confirm_bad"] == af2["confirm_bad"] == 0
assert ao["m15_select"] == af["m15_select"] and ao["m16_pass"] == af["m16_pass"]
for item in (o1,o2,f1,f2,ao,af,af2):
    assert item["order_markers"] == 0
    assert item["deinit0"] > 0 and item["processed"] > 0

OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
print("V487_RUNTIME_TYPE3_PACKAGE=PASS")
