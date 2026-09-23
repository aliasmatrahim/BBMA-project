from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import math
import re
import struct
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CANDIDATE_MARKER = "Build=5.11 BuildTag=V511_EVENT_DRIVEN_OBSERVER_20260922 SourceRev=OBSERVER_EVENT_DRIVEN_237_20260922"
OWNER_TAG = "[D1-03][OWNER]"
N1_TAG = "[N1-NMJE]"
D1OPP_TAG = "[D1-OPP]"
M17_TAG = "[M17-SL][STRUCT]"
M16_TAG = "[P3M2][M16_PASS]"
PREFLIGHT_TAG = "[P3M2][PREFLIGHT_PASS]"
EXEC_TAG = "[P3M2][EXEC]"
FINAL_TAG = "[P3M2][DECISION_FINAL]"
EXEC_ID_TAG = "[P3S5][EXEC_ID]"
N2_DEC_TAG = "[N2-NMJE-DEC]"
N2_OUT_TAG = "[N2-NMJE-OUT]"
GBPUSD_HST_SHA256 = {
    15: "74DB0196F4D77FC66548CD41614ADFDDE9CA96F9E2DA91DAEBCD17E304C5E7B5",
    60: "566762B35FCE7EF2DCB5985A57DAC6BC5D0476A6A76DDEF2D680EF0905632389",
    240: "AA58B7E1114D20B135573168FD414DB7F210AB260427C8596CADFB8052E5015F",
    1440: "6EE8DED5B0027A2340D15196F34DA603899D648A772919AF6FACD156F81800AC",
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def sim_time(line: str) -> datetime | None:
    m = re.search(r"\t(20\d\d\.\d\d\.\d\d \d\d:\d\d:\d\d)\s+", line)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")

def fields(line: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"([A-Za-z0-9_]+)=([^\s]+)", line):
        out[m.group(1)] = m.group(2).rstrip(";,")
    return out

def normalize_did(value: str | None) -> str:
    return (value or "").replace("~", " ")

def dt_field(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y.%m.%d~%H:%M", "%Y.%m.%d %H:%M", "%Y.%m.%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None

def load_hst(path: Path, expected_hash: str, tf: int) -> tuple[list[datetime], dict[datetime, tuple[float, float]]]:
    if not path.is_file():
        raise RuntimeError(f"missing GBPUSD{tf} HST: {path}")
    actual = sha256_file(path)
    if actual != expected_hash:
        raise RuntimeError(
            f"GBPUSD{tf} HST hash mismatch: expected={expected_hash} actual={actual}"
        )
    raw = path.read_bytes()
    if len(raw) < 208 or raw[:4] != struct.pack("<I", 401):
        raise RuntimeError("unsupported HST header/version; expected MT4 HST 401")
    times: list[datetime] = []
    values: dict[datetime, tuple[float, float]] = {}
    for off in range(148, len(raw) - 59, 60):
        ts, _o, high, low, _c, _tv, _spread, _rv = struct.unpack(
            "<qddddqiq", raw[off : off + 60]
        )
        when = datetime.fromtimestamp(ts, timezone.utc).replace(tzinfo=None)
        times.append(when)
        values[when] = (high, low)
    return times, values

def reconstruct_h1_anchor(
    hst: tuple[list[datetime], dict[datetime, tuple[float, float]]],
    start: datetime,
    confirm: datetime,
    direction: str,
) -> float | None:
    if confirm < start:
        return None
    times, values = hst
    left = bisect_left(times, start)
    right = bisect_right(times, confirm)
    selected = times[left:right]
    if not selected:
        return None
    rows = [values[t] for t in selected]
    if direction == "DIR_BUY":
        return min(low for _high, low in rows)
    if direction == "DIR_SELL":
        return max(high for high, _low in rows)
    return None

def parse_exec(line: str) -> dict[str, Any] | None:
    m = re.search(
        r"Ticket=(\d+) Pair=([^ ]+) DecisionID=(.*?) Signal=([^ ]+) Dir=([^ ]+) "
        r"ValidateCandle=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) "
        r"OrderOpen=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})",
        line,
    )
    if not m:
        return None
    return {
        "ticket": m.group(1),
        "pair": m.group(2),
        "decision_id": m.group(3),
        "signal": m.group(4),
        "dir": m.group(5),
        "validate": datetime.strptime(m.group(6), "%Y.%m.%d %H:%M"),
        "open": datetime.strptime(m.group(7), "%Y.%m.%d %H:%M"),
        "sim": sim_time(line),
        "line": line.rstrip(),
    }

def parse_m17(line: str) -> dict[str, Any] | None:
    if M17_TAG not in line:
        return None
    f = fields(line)
    tm = re.search(
        r"TF=(\d+) Start=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}) "
        r"Confirm=(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})",
        line,
    )
    needed = ("Pair", "Dir", "StructuralAnchor", "SpreadBufferPips", "StructuralSL", "FinalBrokerSL", "TP")
    if not tm or not all(k in f for k in needed):
        return None
    try:
        return {
            "pair": f["Pair"],
            "dir": f["Dir"],
            "tf": int(tm.group(1)),
            "start": datetime.strptime(tm.group(2), "%Y.%m.%d %H:%M"),
            "confirm": datetime.strptime(tm.group(3), "%Y.%m.%d %H:%M"),
            "anchor": float(f["StructuralAnchor"]),
            "raw_spread": float(f.get("RawSpreadPips", "0")),
            "spread_buffer": float(f["SpreadBufferPips"]),
            "structural_sl": float(f["StructuralSL"]),
            "final_sl": float(f["FinalBrokerSL"]),
            "tp": float(f["TP"]),
            "c044": f.get("C044") == "Y",
            "d1tpw": f.get("D1TPW") == "Y",
            "extreme": f.get("Extreme") == "Y",
            "sim": sim_time(line),
            "line": line.rstrip(),
        }
    except ValueError:
        return None

def find_identity_ambiguities(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Fail-closed identity conflict detector used by deterministic R6-08 tests."""
    by_hash: dict[tuple[str, str], dict[str, set[str]]] = defaultdict(
        lambda: {"directions": set(), "decision_ids": set()}
    )
    by_ticket: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    for row in rows:
        stem = str(row.get("stem") or "")
        identity_hash = str(row.get("hash") or row.get("expected_hash") or "")
        direction = str(row.get("dir") or "")
        decision_id = normalize_did(row.get("did") or row.get("decision_id"))
        ticket = str(row.get("ticket") or "")
        if identity_hash:
            if direction:
                by_hash[(stem, identity_hash)]["directions"].add(direction)
            if decision_id:
                by_hash[(stem, identity_hash)]["decision_ids"].add(decision_id)
        if ticket and (decision_id or identity_hash):
            by_ticket[(stem, ticket)].add((decision_id, identity_hash))

    conflicts: list[dict[str, Any]] = []
    for (stem, identity_hash), values in by_hash.items():
        if len(values["directions"]) > 1 or len(values["decision_ids"]) > 1:
            conflicts.append({
                "type": "HASH_CONFLICT",
                "stem": stem,
                "hash": identity_hash,
                "directions": sorted(values["directions"]),
                "decision_ids": sorted(values["decision_ids"]),
            })
    for (stem, ticket), identities in by_ticket.items():
        if len(identities) > 1:
            conflicts.append({
                "type": "TICKET_CONFLICT",
                "stem": stem,
                "ticket": ticket,
                "identities": sorted([list(x) for x in identities]),
            })
    return conflicts


def case(status: str, reason: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    out = {"status": status, "reason": reason}
    if evidence:
        out["evidence"] = evidence
    return out

def analyse(root: Path, matrix_path: Path, policy_path: Path, hst60_path: Path, invariants_path: Path) -> dict[str, Any]:
    matrix = load_json(matrix_path)
    policy = load_json(policy_path)
    aggregate = load_json(root / "FINAL_BUILD511_GBPUSD_MATRIX.json")
    hst_cache: dict[int, tuple[list[datetime], dict[datetime, tuple[float, float]]]] = {
        60: load_hst(hst60_path, GBPUSD_HST_SHA256[60], 60)
    }
    invariants = load_json(invariants_path)
    if (
        invariants.get("build") != "5.11"
        or not invariants.get("all_pass")
        or invariants.get("canonical_git_blob_sha256")
        != aggregate["canonical_mq4_sha256"]
    ):
        raise RuntimeError("cross-module invariant evidence is not attributable to exact Build 5.11")
    inv = invariants["checks"]
    expected_hashes = {
        row["stem"]: row["log_sha256"].upper()
        for row in aggregate["periods"]
    }

    owner_counts = Counter()
    n1_reasons = Counter()
    n1_same = 0
    n1_opposite = 0
    d1opp_families = Counter()
    final_reasons = Counter()
    input_modes = Counter()
    mm_modes = Counter()
    fixed_lots = Counter()
    n3_active = 0
    fatal = Counter()
    execs: list[dict[str, Any]] = []
    m17: list[dict[str, Any]] = []
    preflight: list[dict[str, Any]] = []
    exec_ids: list[dict[str, Any]] = []
    n2_dec: list[dict[str, Any]] = []
    n2_out: list[dict[str, Any]] = []
    owner_events: list[dict[str, Any]] = []
    m15_select: list[dict[str, Any]] = []
    d1opp_ext_tpw_tactical = 0
    exact_markers = Counter()
    source_logs: dict[str, Any] = {}

    for stem, expected_hash in expected_hashes.items():
        path = root / f"{stem}_tester_newlog.bin"
        if not path.is_file():
            raise RuntimeError(f"missing historical log: {path}")
        actual = sha256_file(path)
        if actual != expected_hash:
            raise RuntimeError(f"log hash mismatch for {stem}: expected={expected_hash} actual={actual}")
        source_logs[stem] = {"path": str(path), "sha256": actual}
        with path.open("r", encoding="cp1252", errors="ignore") as fh:
            for line in fh:
                if CANDIDATE_MARKER in line:
                    exact_markers[stem] += 1
                low = line.lower()
                for name in ("zero divide", "array out of range", "critical error", "unresolved stack function", "access violation"):
                    if name in low:
                        fatal[name] += 1
                if " inputs:" in line:
                    f = fields(line)
                    if "TradeLockMode" in f:
                        input_modes[f["TradeLockMode"]] += 1
                    if "MMMode" in f:
                        mm_modes[f["MMMode"]] += 1
                    if "FixedLot" in f:
                        fixed_lots[f["FixedLot"]] += 1
                if OWNER_TAG in line:
                    f = fields(line)
                    state = f.get("State", "UNKNOWN")
                    owner_counts[state] += 1
                    ev = {"stem": stem, "state": state, "dir": f.get("Dir"), "candle": f.get("Candle"), "sim": sim_time(line), "line": line.rstrip()}
                    owner_events.append(ev)
                if N1_TAG in line:
                    f = fields(line)
                    reason = f.get("R", "UNKNOWN")
                    n1_reasons[reason] += 1
                    d1 = f.get("D1", "")
                    h4 = f.get("H4", "")
                    if d1.startswith("OWN/") and h4.startswith("OWN/"):
                        if d1[-1:] == h4[-1:]:
                            n1_same += 1
                        else:
                            n1_opposite += 1
                if D1OPP_TAG in line:
                    f = fields(line)
                    family = f.get("F", "UNKNOWN")
                    d1opp_families[family] += 1
                    if family == "EXT_TPW" and f.get("TACT") == "Y":
                        d1opp_ext_tpw_tactical += 1
                if "[P3M2][M15_SELECT]" in line:
                    f = fields(line)
                    dm = re.search(r"DecisionID=(.+?)\s*$", line)
                    m15_select.append({
                        "stem": stem,
                        "d1_state": f.get("D1State"),
                        "dir": f.get("Dir"),
                        "decision_id": dm.group(1) if dm else "",
                        "line": line.rstrip(),
                    })
                if FINAL_TAG in line:
                    f = fields(line)
                    final_reasons[f.get("Reason", "UNKNOWN")] += 1
                if N3_active := ("N3_POLICY_ACTIVE" in line or "N3_EXECUTION_POLICY" in line):
                    n3_active += int(bool(N3_active))
                if EXEC_TAG in line:
                    x = parse_exec(line)
                    if x:
                        x["stem"] = stem
                        execs.append(x)
                x17 = parse_m17(line)
                if x17:
                    x17["stem"] = stem
                    m17.append(x17)
                if PREFLIGHT_TAG in line:
                    f = fields(line)
                    try:
                        dm = re.search(r"DecisionID=(.*?) Entry=", line)
                        preflight.append({
                            "stem": stem,
                            "decision_id": dm.group(1) if dm else "",
                            "entry": float(f["Entry"]),
                            "sl": float(f["SL"]),
                            "tp": float(f["TP"]),
                            "lot": float(f["Lot"]),
                            "sim": sim_time(line),
                            "line": line.rstrip(),
                        })
                    except (KeyError, ValueError):
                        pass
                if EXEC_ID_TAG in line:
                    f = fields(line)
                    exec_ids.append({
                        "stem": stem,
                        "ticket": f.get("Ticket"),
                        "persist": f.get("Persist"),
                        "local": f.get("Local"),
                        "expected_hash": f.get("ExpectedHash"),
                        "broker_hash": f.get("BrokerHash"),
                        "line": line.rstrip(),
                    })
                if N2_DEC_TAG in line:
                    f = fields(line)
                    n2_dec.append({
                        "stem": stem,
                        "did": f.get("DID"),
                        "hash": f.get("DIDH"),
                        "dir": f.get("DIR"),
                        "auth": f.get("AUTH"),
                        "ofam": f.get("OFAM"),
                        "line": line.rstrip(),
                    })
                if N2_OUT_TAG in line:
                    f = fields(line)
                    n2_out.append({
                        "stem": stem,
                        "ticket": f.get("TICKET"),
                        "did": f.get("DID"),
                        "hash": f.get("DIDH"),
                        "rec": f.get("REC"),
                        "sim": sim_time(line),
                        "line": line.rstrip(),
                    })

    if any(v != 1 for v in exact_markers.values()):
        raise RuntimeError(f"exact Build 5.11 marker count invalid: {dict(exact_markers)}")
    if fatal:
        raise RuntimeError(f"fatal runtime markers present: {dict(fatal)}")

    exec_decisions = [(x["stem"], x["decision_id"]) for x in execs]
    exec_ticket_keys = [(x["stem"], x["ticket"]) for x in execs]
    exec_dirs = Counter(x["dir"] for x in execs)
    closed_timing_ok = bool(execs) and all(x["validate"] < x["open"] for x in execs)
    duplicate_decisions = len(exec_decisions) - len(set(exec_decisions))
    duplicate_tickets = len(exec_ticket_keys) - len(set(exec_ticket_keys))

    closed_d1_ok = True
    closed_d1_samples = 0
    for ev in owner_events:
        c = dt_field(ev["candle"])
        sim = ev["sim"]
        if c and sim and c.year >= 2000:
            closed_d1_samples += 1
            if c.date() >= sim.date():
                closed_d1_ok = False
                break

    point = 0.00001
    pip = 0.0001
    anchor_cache: dict[tuple[datetime, datetime, str], float | None] = {}
    anchor_mismatch: list[dict[str, Any]] = []
    anchor_missing = 0
    for x in m17:
        if x["pair"] != "GBPUSD" or x["tf"] not in GBPUSD_HST_SHA256:
            anchor_missing += 1
            continue
        if x["tf"] not in hst_cache:
            tf_path = hst60_path.parent / f"GBPUSD{x['tf']}.hst"
            hst_cache[x["tf"]] = load_hst(
                tf_path, GBPUSD_HST_SHA256[x["tf"]], x["tf"]
            )
        key = (x["tf"], x["start"], x["confirm"], x["dir"])
        if key not in anchor_cache:
            anchor_cache[key] = reconstruct_h1_anchor(
                hst_cache[x["tf"]], x["start"], x["confirm"], x["dir"]
            )
        reconstructed = anchor_cache[key]
        if reconstructed is None:
            anchor_missing += 1
        elif abs(reconstructed - x["anchor"]) > point * 0.5:
            anchor_mismatch.append({
                "stem": x["stem"],
                "start": x["start"].isoformat(" "),
                "confirm": x["confirm"].isoformat(" "),
                "dir": x["dir"],
                "logged": x["anchor"],
                "reconstructed": reconstructed,
            })

    buy17 = [x for x in m17 if x["dir"] == "DIR_BUY"]
    sell17 = [x for x in m17 if x["dir"] == "DIR_SELL"]
    buy_anchor_ok = bool(buy17) and anchor_missing == 0 and not anchor_mismatch
    sell_anchor_ok = bool(sell17) and anchor_missing == 0 and not anchor_mismatch

    def safety_buffer_price(x: dict[str, Any]) -> float:
        # Current Build 5.11 contract: standalone H1 Extreme uses a 3-pip
        # wick buffer; ordinary source-owned Re-Entry windows use one Point.
        return 3.0 * pip if x["extreme"] else point

    buy_sl_ok = bool(buy17) and all(
        abs(
            x["anchor"] - x["structural_sl"] - safety_buffer_price(x)
        ) <= point * 0.6
        and abs(x["spread_buffer"]) < 1e-9
        and abs(x["final_sl"] - x["structural_sl"]) <= point * 0.6
        for x in buy17
    )
    sell_sl_ok = bool(sell17) and all(
        abs(
            x["structural_sl"] - x["anchor"] - safety_buffer_price(x)
        ) <= point * 0.6
        and abs(
            x["spread_buffer"] - max(2.0, float(math.ceil(x["raw_spread"] - 1e-9)))
        ) <= 1e-9
        and abs(
            x["final_sl"]
            - (x["structural_sl"] + x["spread_buffer"] * pip)
        ) <= point * 0.6
        for x in sell17
    )
    targetless = [x for x in m17 if x["c044"] or x["d1tpw"]]
    targetless_ok = bool(targetless) and all(abs(x["tp"]) < 1e-9 for x in targetless)
    non_jpy_ok = bool(m17) and all(x["pair"] == "GBPUSD" for x in m17)
    sell_sl_varies = len({round(x["final_sl"], 5) for x in sell17}) > 1

    preflight_lots = [x["lot"] for x in preflight]
    fixed_lot_ok = (
        mm_modes["2"] > 0
        and fixed_lots["0.01"] > 0
        and bool(preflight_lots)
        and all(abs(lot - 0.01) < 1e-12 for lot in preflight_lots)
    )

    persist_ok = bool(exec_ids) and all(
        x["persist"] == "PASS" and x["local"] == "Y" for x in exec_ids
    )
    hash_pair_ok = bool(exec_ids) and all(
        x["expected_hash"] and x["broker_hash"]
        and x["expected_hash"] == x["broker_hash"]
        for x in exec_ids
    )

    n2_hash_dirs: dict[tuple[str, str], set[str]] = defaultdict(set)
    n2_obs = Counter()
    for x in n2_dec:
        if x["hash"]:
            n2_hash_dirs[(x["stem"], x["hash"])].add(x["dir"] or "")
        if x["did"]:
            n2_obs[(x["stem"], normalize_did(x["did"]))] += 1
    n2_dir_invariant = bool(n2_hash_dirs) and all(
        len(v) == 1 for v in n2_hash_dirs.values()
    )
    repeated_n2 = any(v > 1 for v in n2_obs.values())

    n2_out_by_ticket = {
        (x["stem"], x["ticket"]): x
        for x in n2_out if x["ticket"]
    }
    n2_chain_count = 0
    for x in exec_ids:
        key = (x["stem"], x["ticket"])
        if (
            key in n2_out_by_ticket
            and x["expected_hash"] == n2_out_by_ticket[key]["hash"]
        ):
            n2_chain_count += 1

    d1o_dec = [
        x for x in n2_dec
        if x.get("auth") == "OPP" or x.get("ofam") not in (None, "", "NONE")
    ]
    d1o_hash_dirs: dict[tuple[str, str], set[str]] = defaultdict(set)
    d1o_dids: dict[tuple[str, str], set[str]] = defaultdict(set)
    d1o_keys: set[tuple[str, str]] = set()
    for x in d1o_dec:
        did = normalize_did(x.get("did"))
        if did:
            d1o_keys.add((x["stem"], did))
            d1o_dids[(x["stem"], did)].add(x.get("hash") or "")
        if x.get("hash"):
            d1o_hash_dirs[(x["stem"], x["hash"])].add(x.get("dir") or "")
    d1o_stable = bool(d1o_dec) and all(len(v) == 1 for v in d1o_dids.values())
    d1o_dir_ok = bool(d1o_hash_dirs) and all(
        len(v) == 1 for v in d1o_hash_dirs.values()
    )
    d1o_decision_keys = {
        (x["stem"], normalize_did(x.get("did")))
        for x in d1o_dec
        if normalize_did(x.get("did"))
    }
    d1o_authority_by_key = {
        (x["stem"], normalize_did(x.get("did"))): (
            x.get("auth") or "",
            x.get("ofam") or "",
        )
        for x in d1o_dec
        if normalize_did(x.get("did"))
    }
    strategic_selection_violations = []
    tactical_ext_tpw_opposite_selections = 0
    for x in m15_select:
        key = (x["stem"], normalize_did(x.get("decision_id")))
        expected_dir = None
        if x["d1_state"] == "D1_OWNER_BUY_CONFIRMED":
            expected_dir = "DIR_BUY"
        elif x["d1_state"] == "D1_OWNER_SELL_CONFIRMED":
            expected_dir = "DIR_SELL"
        elif x["d1_state"] in ("D1_TRANSITION", "D1_OWNER_UNRESOLVED"):
            strategic_selection_violations.append(x)
            continue

        if expected_dir is not None and x["dir"] != expected_dir:
            auth, ofam = d1o_authority_by_key.get(key, ("", ""))
            if auth == "OPP" and ofam == "EXT_TPW":
                tactical_ext_tpw_opposite_selections += 1
            else:
                strategic_selection_violations.append(x)
    d1o_execs = [
        x for x in execs
        if (x["stem"], normalize_did(x["decision_id"])) in d1o_keys
    ]
    d1o_exec_keys = [(x["stem"], normalize_did(x["decision_id"])) for x in d1o_execs]
    d1o_ticket_keys = [(x["stem"], x["ticket"]) for x in d1o_execs]
    d1o_dedup_ok = (
        bool(d1o_execs)
        and len(d1o_exec_keys) == len(set(d1o_exec_keys))
        and len(d1o_ticket_keys) == len(set(d1o_ticket_keys))
    )

    # R3-14: reconstruct exact-open-position lifetime across a canonical D1 owner
    # update. An execution that opened before the owner update and only emitted
    # its closed outcome afterwards is positive proof that the D1 update itself
    # did not directly close that position.
    outcomes_by_ticket = {
        (x["stem"], x["ticket"]): x
        for x in n2_out
        if x.get("ticket") and x.get("sim")
    }
    owner_updates: list[dict[str, Any]] = []
    by_stem_owner: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ev in owner_events:
        if ev.get("sim"):
            by_stem_owner[ev["stem"]].append(ev)
    for stem, rows in by_stem_owner.items():
        rows.sort(key=lambda x: x["sim"])
        previous_key = None
        previous_ev = None
        for ev in rows:
            key = (ev.get("state"), ev.get("dir"), ev.get("candle"))
            if previous_key is not None and key != previous_key:
                owner_updates.append({
                    "stem": stem,
                    "time": ev["sim"],
                    "before": previous_key,
                    "after": key,
                    "direction_flip": (
                        previous_ev is not None
                        and previous_ev.get("dir") != ev.get("dir")
                    ),
                })
            previous_key = key
            previous_ev = ev

    owner_update_spans = 0
    owner_flip_spans = 0
    owner_update_samples: list[dict[str, Any]] = []
    for ex in execs:
        outcome = outcomes_by_ticket.get((ex["stem"], ex["ticket"]))
        if outcome is None or outcome.get("sim") is None:
            continue
        for update in owner_updates:
            if update["stem"] != ex["stem"]:
                continue
            if ex["open"] < update["time"] < outcome["sim"]:
                owner_update_spans += 1
                if update["direction_flip"]:
                    owner_flip_spans += 1
                if len(owner_update_samples) < 12:
                    owner_update_samples.append({
                        "stem": ex["stem"],
                        "ticket": ex["ticket"],
                        "open": ex["open"].isoformat(" "),
                        "owner_update": update["time"].isoformat(" "),
                        "before": list(update["before"]),
                        "after": list(update["after"]),
                        "direction_flip": update["direction_flip"],
                        "outcome_observed": outcome["sim"].isoformat(" "),
                        "recovery": outcome.get("rec"),
                    })

    cases: dict[str, dict[str, Any]] = {}
    def setc(cid: str, ok: bool, yes: str, no: str, ev: dict[str, Any] | None = None):
        cases[cid] = case("PASS" if ok else "INCOMPLETE", yes if ok else no, ev)

    setc("R3-01", owner_counts["D1_OWNER_BUY_CONFIRMED"] > 0, "D1 BUY confirmed repeatedly in exact Build 5.11 history.", "No D1 BUY owner evidence.")
    setc("R3-02", owner_counts["D1_OWNER_SELL_CONFIRMED"] > 0, "D1 SELL confirmed repeatedly in exact Build 5.11 history.", "No D1 SELL owner evidence.")
    setc("R3-03", owner_counts["D1_TRANSITION"] > 0, "D1 TRANSITION positively observed.", "No D1 TRANSITION observed.")
    setc("R3-04", owner_counts["D1_OWNER_UNRESOLVED"] > 0, "D1 UNRESOLVED positively observed.", "No D1 UNRESOLVED observed.")
    setc("R3-05", n1_same > 0, "Compatible D1/H4 owner relationship positively observed.", "No compatible D1/H4 owner observation.")
    setc("R3-06", (n1_opposite > 0 or n1_reasons["H4_LOCAL_OPPOSES_D1"] > 0) and not strategic_selection_violations, "Opposite H4/D1 states were observed and blocked from ordinary strategic/opportunity override; all opposite selections were the approved tactical EXT_TPW exception.", "Opposite H4/D1 proof incomplete or a non-EXT_TPW D1 selection invariant was violated.")
    missing_reason_count = sum(v for k,v in n1_reasons.items() if "H4" in k and ("MISSING" in k or "NO_" in k or "UNRESOLVED" in k))
    setc("R3-07", missing_reason_count > 0, "Required H4-missing/unresolved path positively observed.", "No attributable required H4-missing scenario.")
    setc("R3-08", bool(d1o_dec), "D1 Opportunity attribution is present on exact Build 5.11 decision telemetry.", "No D1O-attributed executable decision observed.")
    setc("R3-09", d1o_stable, "D1O DecisionID maps to one stable hash.", "No sufficient D1O hash-stability evidence.")
    setc("R3-10", d1o_dir_ok, "D1O execution hash direction is invariant.", "No sufficient D1O direction-invariance evidence.")
    setc("R3-11", d1o_dedup_ok, "Observed D1O execution identities map one-to-one to run-scoped tester tickets.", "No sufficient D1O execution/dedup evidence.")
    ext_tpw = d1opp_families["EXT_TPW"] + d1opp_families["D1_OPP_EXTREME_TPW"]
    setc("R3-13", ext_tpw > 0 and d1opp_ext_tpw_tactical > 0, "EXT_TPW family positively observed with tactical attribution separated in D1 opportunity telemetry.", "No tactical EXT_TPW family observation.")
    setc(
        "R3-14",
        owner_update_spans > 0,
        "Exact historical executions remained open across canonical D1 owner updates and only produced closed outcomes later; D1 owner update alone did not directly close the position.",
        "No exact open-position-across-owner-update lifetime could be reconstructed.",
        {
            "spanning_owner_update_count": owner_update_spans,
            "spanning_direction_flip_count": owner_flip_spans,
            "samples": owner_update_samples,
        },
    )
    setc("R3-15", closed_d1_samples > 0 and closed_d1_ok, "All attributable owner events use an earlier fully closed D1 candle.", "Closed-D1 proof incomplete or violated.")

    setc("R4-00", bool(execs), "Executions carry exact DecisionID and validation provenance.", "No executable validation provenance.")
    setc("R4-02", closed_timing_ok, "Every execution opens strictly after its validation candle.", "Validation/open chronology incomplete or invalid.")
    setc("R4-03", buy_anchor_ok, "Every attributable BUY M17 StructuralAnchor matches the minimum Low over the exact source-TF Start..Confirm HST window.", "BUY structural-window reconstruction incomplete or mismatched.")
    setc("R4-04", buy_sl_ok, "BUY structural SL uses no spread buffer and remains outside structural anchor.", "BUY structural-SL proof incomplete.")
    setc("R4-05", sell_anchor_ok, "Every attributable SELL M17 StructuralAnchor matches the maximum High over the exact source-TF Start..Confirm HST window.", "SELL structural-window reconstruction incomplete or mismatched.")
    setc("R4-06", bool(sell17) and all(x["structural_sl"] > x["anchor"] for x in sell17), "SELL structural SL lies beyond structural high anchor.", "SELL structural-SL proof incomplete.")
    setc("R4-07", sell_sl_ok, "SELL final SL equals the source-family structural SL plus max(2 pips, ceil(raw frozen spread pips)) for every observed record.", "SELL spread-buffer formula proof incomplete.")
    cases["R4-08"] = case("INCOMPLETE", "Requires per-decision frozen-snapshot correlation between M17 and M21/preflight; deferred to targeted analyzer.")
    cases["R4-09"] = case("INCOMPLETE", "AutoLot response to changing final SL not proven by aggregate marker scan.")
    setc("R4-10", fixed_lot_ok, "MMMode=2 FixedLot=0.01 is attributable and every preflight lot remains exactly 0.01.", "FixedLot invariance proof incomplete.")
    cases["R4-11"] = case("INCOMPLETE", "Current exact historical matrix is GBPUSD-only; no JPY geometry evidence.")
    setc("R4-12", non_jpy_ok and buy_sl_ok and sell_sl_ok, "GBPUSD non-JPY geometry positively covered for BUY and SELL.", "Non-JPY geometry proof incomplete.")
    setc("R4-14", targetless_ok, "All observed C044/D1TPW lifecycle-managed M17 payloads retain hard SL with broker TP=0.", "Targetless lifecycle payload proof incomplete.")
    cases["R4-15"] = case("INCOMPLETE", "Aggregate history proves targetless TP=0 but does not isolate a same-decision changed-final-SELL-SL experiment; retain for targeted Phase H evidence.")
    cases["R4-16"] = case("INCOMPLETE", "Source-owner mismatch rejection requires a targeted attributable rejection record.")

    setc("R5-00", bool(input_modes), "TradeLock mode is explicitly attributable in historical input logs.", "TradeLock mode attribution absent.")
    setc("R5-01", input_modes["0"] > 0 and bool(execs), "LOCK_OFF allow path executed under attributable mode 0.", "No attributable LOCK_OFF allow case.")
    cases["R5-02"] = case("INCOMPLETE", "No dedicated LOCK_SAME_DIRECTION/LOCK_ONE_POSITION block variant in current matrix.")
    cases["R5-03"] = case("INCOMPLETE", "No dedicated opposite-direction TradeLock variant in current matrix.")
    for cid in ("R5-04","R5-05","R5-06","R5-07","R5-08","R5-10"):
        cases[cid] = case("INCOMPLETE", "Requires targeted risk/recovery scenario analysis or variant run.")
    setc("R5-09", final_reasons["REJ_PORTFOLIO_LIMIT_ATOMIC"] > 0,
         "Historical decisions positively hit REJ_PORTFOLIO_LIMIT_ATOMIC before execution.",
         "No attributable portfolio-limit rejection.")
    cases["R5-14"] = case("INCOMPLETE", "Broker-comment blank/replaced behavior is not proven by current tester history.")
    for cid in ("R5-15","R5-16","R5-17","R5-18"):
        cases[cid] = case("INCOMPLETE", "Requires deterministic fault/invalid fixture or targeted historical evidence.")
    cases["R5-19"] = case("INCOMPLETE", "Conditional emergency precedence not exercised.")
    cases["R5-20"] = case("INCOMPLETE", "Needs exact-owned registry-vs-open-position reconciliation.")

    setc("R6-00", sum(n1_reasons.values()) > 0, "N1 observation telemetry is abundant.", "N1 observation absent.")
    setc("R6-01", bool(n2_dec), "N2 validated decision shadow telemetry is present.", "N2 decision shadow absent.")
    setc("R6-04", n2_dir_invariant, "N2 execution hashes retain one direction.", "N2 direction-invariance proof incomplete.")
    setc("R6-05", repeated_n2 and duplicate_decisions == 0 and duplicate_tickets == 0, "Repeated N2 observations do not create duplicate execution identities/tickets.", "Duplicate-observation safety proof incomplete.")
    cases["R6-08"] = case("INCOMPLETE", "Identity ambiguity requires deterministic malformed/conflicting fixture.")
    setc("R6-10", n3_active == 0 and matrix["current_build_semantics"]["n3_execution_policy"] == "NONE", "No active N3 execution-policy marker and current build policy is NONE.", "N3 firewall proof incomplete or contradicted.")
    n3_static_read_only = all(
        inv[name]["pass"]
        for name in (
            "m12n_no_OrderSend_",
            "m12n_no_OrderClose_",
            "m12n_no_RunEntryPreflightAndExecute_",
            "m12n_no_DecisionState_",
            "m12n_no_RejectionReason_",
            "forbidden_absent_NMJE_PassExecutionGate",
            "forbidden_absent_REJ_NMJE_RELATION",
            "forbidden_absent_N3_POLICY_ACTIVE",
            "forbidden_absent_N3_EXECUTION_POLICY",
        )
    )
    setc("R6-11", n3_static_read_only and bool(execs),
         "Exact-source invariants prove NMJE/N3 has no entry authority while historical execution proceeds through the approved pipeline.",
         "N3 entry-firewall proof incomplete.")
    setc("R6-12", n3_static_read_only and inv["m19_m21_no_candidate_builder"]["pass"],
         "Exact-source invariants prove NMJE/N3 cannot create decisions or enter M19/M21 sizing authority.",
         "N3 risk/sizing firewall proof incomplete.")
    setc("R6-13", n3_static_read_only and inv["m12n_no_OrderClose_"]["pass"],
         "Exact-source invariants prove NMJE/N3 has no broker/lifecycle close authority.",
         "N3 SL/TP/lifecycle firewall proof incomplete.")
    setc("R6-14", n3_static_read_only and inv["order_send_single"]["pass"],
         "Observer/NMJE authority is read-only; canonical source retains one production OrderSend owner.",
         "Observer read-only proof incomplete.")
    cases["R6-15"] = case("INCOMPLETE", "Bundle assertion integrity is a tooling test, not inferred from tester marker history.")
    cases["R6-16"] = case("INCOMPLETE", "Incompleteness handling is a tooling test, not inferred from tester marker history.")

    historical_required = {
        cid
        for stage in policy["stages"].values()
        for cid in stage["historical_required_cases"]
    }
    statuses = {cid: cases.get(cid, case("INCOMPLETE", "No automatic historical adjudication implemented.")) for cid in sorted(historical_required)}
    pass_ids = [cid for cid,x in statuses.items() if x["status"] == "PASS"]
    incomplete_ids = [cid for cid,x in statuses.items() if x["status"] == "INCOMPLETE"]
    fail_ids = [cid for cid,x in statuses.items() if x["status"] == "FAIL"]

    return {
        "schema": "BBMA_Q10_HYBRID_HISTORICAL_ANALYSIS_V1",
        "label": aggregate["label"],
        "candidate": aggregate["candidate"],
        "canonical_mq4_sha256": aggregate["canonical_mq4_sha256"],
        "tester_adapter_mq4_sha256": aggregate["tester_adapter_mq4_sha256"],
        "tester_adapter_ex4_sha256": aggregate["tester_adapter_ex4_sha256"],
        "settings_sha256": aggregate["settings_sha256"],
        "source_logs": source_logs,
        "facts": {
            "owner_states": dict(owner_counts),
            "n1_reasons": dict(n1_reasons),
            "n1_same_direction": n1_same,
            "n1_opposite_direction": n1_opposite,
            "d1op_families": dict(d1opp_families),
            "d1opp_ext_tpw_tactical": d1opp_ext_tpw_tactical,
            "strategic_selection_violations": len(strategic_selection_violations),
            "tactical_ext_tpw_opposite_selections": tactical_ext_tpw_opposite_selections,
            "exec_count": len(execs),
            "exec_directions": dict(exec_dirs),
            "duplicate_exec_decision_ids": duplicate_decisions,
            "duplicate_tickets": duplicate_tickets,
            "m17_buy_records": len(buy17),
            "m17_sell_records": len(sell17),
            "m17_anchor_cache_windows": len(anchor_cache),
            "m17_anchor_missing": anchor_missing,
            "m17_anchor_mismatch_count": len(anchor_mismatch),
            "m17_targetless_records": len(targetless),
            "preflight_records": len(preflight),
            "exec_id_records": len(exec_ids),
            "exec_id_persist_local_ok": persist_ok,
            "exec_id_hash_pair_ok": hash_pair_ok,
            "n2_dec_records": len(n2_dec),
            "n2_out_records": len(n2_out),
            "n2_end_to_end_ticket_hash_chains": n2_chain_count,
            "n3_active_markers": n3_active,
            "decision_final_reasons": dict(final_reasons),
            "trade_lock_modes": dict(input_modes),
            "mm_modes": dict(mm_modes),
            "fixed_lot_inputs": dict(fixed_lots),
            "d1o_decision_observations": len(d1o_dec),
            "d1o_exec_count": len(d1o_execs),
            "owner_update_open_position_spans": owner_update_spans,
            "owner_direction_flip_open_position_spans": owner_flip_spans,
            "closed_d1_samples": closed_d1_samples,
            "closed_d1_only_ok": closed_d1_ok,
        },
        "historical_cases": statuses,
        "summary": {
            "pass_count": len(pass_ids),
            "incomplete_count": len(incomplete_ids),
            "fail_count": len(fail_ids),
            "pass_cases": pass_ids,
            "incomplete_cases": incomplete_ids,
            "fail_cases": fail_ids,
            "phase_h_status": "FAIL" if fail_ids else ("PASS" if not incomplete_ids else "INCOMPLETE"),
        },
    }

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--matrix", required=True)
    p.add_argument("--policy", required=True)
    p.add_argument("--hst60", required=True)
    p.add_argument("--invariants", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = analyse(Path(args.root), Path(args.matrix), Path(args.policy), Path(args.hst60), Path(args.invariants))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    return 2 if result["summary"]["phase_h_status"] == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())
