from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib, json, re

BASE = Path(__file__).resolve().parent
MODE1 = BASE / "V486_RUNTIME_LIFETIME_MODE1_RUN_20260917.log"
MODE2 = BASE / "V486_RUNTIME_LIFETIME_MODE2_RUN_20260917.log"
SUMMARY = BASE / "V486_RUNTIME_LIFETIME_SUMMARY_20260917.json"

def read(path):
    return path.read_text(encoding="utf-8", errors="replace").splitlines()

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def owner_stats(lines, marker):
    ages, by_type, by_tf = [], defaultdict(list), defaultdict(list)
    for line in lines:
        if marker not in line:
            continue
        m = re.search(r"AgeBars=([-0-9.]+)", line)
        if not m:
            continue
        age = float(m.group(1)); ages.append(age)
        t = re.search(r"Type=([^ ]+)", line)
        tf = re.search(r"TF=(\d+)", line)
        if t: by_type[t.group(1)].append(age)
        if tf: by_tf[tf.group(1)].append(age)
    return ages, by_type, by_tf
def select_gt5(lines):
    hits = []
    for line in lines:
        if "[P3M2][M15_SELECT]" not in line or "Signal=SIGNAL_RE_ENTRY" not in line:
            continue
        pt = re.search(r"\t(2026\.\d\d\.\d\d \d\d:\d\d:\d\d)  ", line)
        ct = re.search(r" Candle=(2026\.\d\d\.\d\d \d\d:\d\d)", line)
        did = re.search(r"DecisionID=(.+)$", line)
        if not (pt and ct and did):
            continue
        process = datetime.strptime(pt.group(1), "%Y.%m.%d %H:%M:%S")
        candle = datetime.strptime(ct.group(1), "%Y.%m.%d %H:%M")
        age_h = (process - candle).total_seconds() / 3600.0
        if age_h > 5:
            hits.append((pt.group(1), did.group(1), age_h, line))
    return hits

m1, m2 = read(MODE1), read(MODE2)
r1, rt1, _ = owner_stats(m1, "[Q5LIFE][RE_OWNER]")
e1, _, ef1 = owner_stats(m1, "[Q5LIFE][EXT_OWNER]")
r2, rt2, _ = owner_stats(m2, "[Q5LIFE][RE_OWNER]")
e2, _, ef2 = owner_stats(m2, "[Q5LIFE][EXT_OWNER]")
old_expiry = lambda xs: sum("MaxWaitBars_ReEntry expired" in x or "Extreme component expired" in x for x in xs)
orders = lambda xs: sum(bool(re.search(r"OrderSend|deal #|open order", x, re.I)) for x in xs)
mode2_gt5 = select_gt5(m2)
matched_m16 = []
for ts, did, age_h, line in mode2_gt5:
    if any(ts in x and "[P3M2][M16_PASS]" in x and did in x for x in m2):
        matched_m16.append((ts, did, age_h))
summary = {
    "mode1": {"lines": len(m1), "re_owner": len(r1), "re_gt5": sum(a > 5 for a in r1),
              "re_max": max(r1), "ext_owner": len(e1), "ext_gt5": sum(a > 5 for a in e1),
              "ext_max": max(e1), "expired": old_expiry(m1), "orders": orders(m1)},
    "mode2": {"lines": len(m2), "re_owner": len(r2), "re_gt5": sum(a > 5 for a in r2),
              "re_max": max(r2), "ext_owner": len(e2), "ext_gt5": sum(a > 5 for a in e2),
              "ext_max": max(e2), "select_gt5": len(mode2_gt5), "m16_gt5": len(matched_m16),
              "expired": old_expiry(m2), "orders": orders(m2)},
    "mode1_re_types": {k: {"gt5": sum(a > 5 for a in v), "max": max(v)} for k, v in rt1.items()},
    "mode1_ext_tf": {k: {"gt5": sum(a > 5 for a in v), "max": max(v)} for k, v in ef1.items()},
    "mode1_sha256": sha256(MODE1), "mode2_sha256": sha256(MODE2),
}
assert summary["mode1"]["re_gt5"] > 0 and summary["mode1"]["ext_gt5"] > 0
assert summary["mode1_re_types"].get("RE_TYPE_3_CSM", {}).get("gt5", 0) > 0
assert summary["mode1_re_types"].get("RE_TYPE_4_CSD", {}).get("gt5", 0) > 0
assert summary["mode1_ext_tf"].get("60", {}).get("gt5", 0) > 0
assert summary["mode1_ext_tf"].get("240", {}).get("gt5", 0) > 0
assert summary["mode1"]["expired"] == 0 and summary["mode2"]["expired"] == 0
assert summary["mode1"]["orders"] == 0 and summary["mode2"]["orders"] == 0
assert summary["mode2"]["select_gt5"] > 0 and summary["mode2"]["m16_gt5"] == summary["mode2"]["select_gt5"]
SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
print("V486_RUNTIME_LIFETIME_PACKAGE=PASS")
