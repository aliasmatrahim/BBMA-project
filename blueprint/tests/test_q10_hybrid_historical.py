from __future__ import annotations

import calendar
import importlib.util
import json
import struct
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "blueprint" / "tools" / "q10_hybrid_historical.py"
SPEC = importlib.util.spec_from_file_location("q10_hybrid_historical", TOOL)
q10h = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(q10h)

POLICY = ROOT / "blueprint" / "runtime" / "q10_demo_acceptance" / "FINAL_BUILD511_HYBRID_EVIDENCE_POLICY.json"
MATRIX = ROOT / "blueprint" / "runtime" / "q10_demo_acceptance" / "FINAL_BUILD511_STAGE_MATRIX.json"


def write_fixture(tmp_path: Path):
    stem = "FINAL511_SYNTH"
    lines = [
        "0\t00:00:00.000\t2024.01.02 00:00:01  EA: Build=5.11 BuildTag=V511_EVENT_DRIVEN_OBSERVER_20260922 SourceRev=OBSERVER_EVENT_DRIVEN_237_20260922",
        "2\t00:00:00.001\t2024.01.02 00:00:00  EA inputs: TradeLockMode=0; MMMode=2; FixedLot=0.01;",
        "0\t00:00:00.002\t2024.01.02 00:00:01  EA: [D1-03][OWNER] Pair=GBPUSD Candle=2023.12.29 00:00 Epoch=2023.12.01 00:00 State=D1_OWNER_BUY_CONFIRMED Dir=DIR_BUY Close=1.2 MA50=1.1 PrevMA50=1.0",
        "0\t00:00:00.003\t2024.01.02 00:00:01  EA: [N1-NMJE] GBPUSD REL=BUILDING D1=OWN/B H4=OWN/S R=H4_LOCAL_OPPOSES_D1",
        "0\t00:00:00.004\t2024.01.02 00:00:01  EA: [M17-SL][STRUCT] Pair=GBPUSD Dir=DIR_BUY TF=60 Start=2024.01.01 22:00 Confirm=2024.01.01 23:00 StructuralAnchor=1.20000 RawSpreadPips=0.0 SpreadBufferPips=0.0 StructuralSL=1.19999 FinalBrokerSL=1.19999 TP=0.00000",
        "0\t00:00:00.005\t2024.01.02 00:00:01  EA: [M17-SL][STRUCT] Pair=GBPUSD Dir=DIR_SELL TF=60 Start=2024.01.01 22:00 Confirm=2024.01.01 23:00 StructuralAnchor=1.21000 RawSpreadPips=1.2 SpreadBufferPips=2.0 StructuralSL=1.21001 FinalBrokerSL=1.21021 TP=0.00000",
        "0\t00:00:00.006\t2024.01.02 00:00:01  EA: [P3M2][PREFLIGHT_PASS] DecisionID=GBPUSD|2024.01.01 23:00|1|7|ABC Entry=1.20500 SL=1.19999 TP=0.00000 Lot=0.01",
        "0\t00:00:00.007\t2024.01.02 00:00:01  EA: [P3S5][EXEC_ID] Ticket=1 Pair=GBPUSD Persist=PASS Local=Y ExpectedHash=HASH1 BrokerHash=HASH1",
        "0\t00:00:00.008\t2024.01.02 00:00:01  EA: [P3M2][EXEC] Ticket=1 Pair=GBPUSD DecisionID=GBPUSD|2024.01.01 23:00|1|7|ABC Signal=SIGNAL_RE_ENTRY Dir=DIR_BUY ValidateCandle=2024.01.01 23:00 OrderOpen=2024.01.02 00:00",
        "0\t00:00:00.009\t2024.01.02 00:15:01  EA: [N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=B DID=GBPUSD|2024.01.01~23:00|1|7|ABC DIDH=HASH1 AUTH=STRAT OFAM=NONE",
        "0\t00:00:00.010\t2024.01.02 00:30:01  EA: [N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=B DID=GBPUSD|2024.01.01~23:00|1|7|ABC DIDH=HASH1 AUTH=STRAT OFAM=NONE",
        "0\t00:00:00.011\t2024.01.02 01:00:01  EA: [N2-NMJE-OUT] PAIR=GBPUSD TICKET=1 DID=GBPUSD|2024.01.01~23:00|1|7|ABC DIDH=HASH1 NET=1.0 REC=REC_NORMAL",
    ]
    log = tmp_path / f"{stem}_tester_newlog.bin"
    log.write_text("\n".join(lines) + "\n", encoding="cp1252")
    matrix = {
        "label": "ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE",
        "candidate": "Build 5.11 / V511_EVENT_DRIVEN_OBSERVER_20260922",
        "canonical_mq4_sha256": "SRC",
        "tester_adapter_mq4_sha256": "ADAPTER_SRC",
        "tester_adapter_ex4_sha256": "ADAPTER_EX4",
        "settings_sha256": "SET",
        "periods": [{"stem": stem, "log_sha256": q10h.sha256_file(log)}],
    }
    (tmp_path / "FINAL_BUILD511_GBPUSD_MATRIX.json").write_text(json.dumps(matrix), encoding="utf-8")

    hst = tmp_path / "GBPUSD60.hst"
    header = struct.pack("<I", 401) + bytes(144)
    rows = []
    for when, o, h, l, c in (
        (datetime(2024, 1, 1, 22, 0), 1.2050, 1.2100, 1.2000, 1.2060),
        (datetime(2024, 1, 1, 23, 0), 1.2060, 1.2090, 1.2010, 1.2070),
    ):
        ts = calendar.timegm(when.timetuple())
        rows.append(struct.pack("<qddddqiq", ts, o, h, l, c, 1, 20, 0))
    hst.write_bytes(header + b"".join(rows))
    q10h.GBPUSD_HST_SHA256[60] = q10h.sha256_file(hst)

    checks = {
        name: {"pass": True}
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
            "m19_m21_no_candidate_builder",
            "order_send_single",
        )
    }
    invariants = tmp_path / "FINAL_INVARIANTS.json"
    invariants.write_text(
        json.dumps(
            {
                "build": "5.11",
                "all_pass": True,
                "canonical_git_blob_sha256": "SRC",
                "checks": checks,
            }
        ),
        encoding="utf-8",
    )
    return log, hst, invariants


def test_hybrid_policy_partitions_every_case_once():
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    for stage, spec in policy["stages"].items():
        hist = set(spec["historical_required_cases"])
        live = set(spec["live_only_cases"])
        reconfirm = set(spec["live_reconfirm_cases"])
        all_cases = set(spec["all_cases"])
        matrix_cases = {x["id"] for x in matrix["stages"][stage]["cases"]}
        assert hist.isdisjoint(live)
        assert hist | live == all_cases
        assert reconfirm <= hist
        assert all_cases == matrix_cases


def test_analyzer_is_hash_bound_and_fail_closed(tmp_path: Path):
    log, hst, invariants = write_fixture(tmp_path)
    result = q10h.analyse(tmp_path, MATRIX, POLICY, hst, invariants)
    assert result["summary"]["fail_count"] == 0
    assert result["historical_cases"]["R3-01"]["status"] == "PASS"
    assert result["historical_cases"]["R3-06"]["status"] == "PASS"
    assert result["historical_cases"]["R4-04"]["status"] == "PASS"
    assert result["historical_cases"]["R4-07"]["status"] == "PASS"
    assert result["historical_cases"]["R6-04"]["status"] == "PASS"
    assert result["historical_cases"]["R5-02"]["status"] == "INCOMPLETE"

    log.write_text(log.read_text(encoding="cp1252") + "tamper\n", encoding="cp1252")
    with pytest.raises(RuntimeError, match="log hash mismatch"):
        q10h.analyse(tmp_path, MATRIX, POLICY, hst, invariants)


def test_no_live_only_case_is_emitted_as_historical_case(tmp_path: Path):
    _log, hst, invariants = write_fixture(tmp_path)
    result = q10h.analyse(tmp_path, MATRIX, POLICY, hst, invariants)
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    live_only = {x for s in policy["stages"].values() for x in s["live_only_cases"]}
    assert live_only.isdisjoint(result["historical_cases"])
