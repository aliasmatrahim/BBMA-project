from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "blueprint" / "tools" / "q10_demo_acceptance.py"
SPEC = importlib.util.spec_from_file_location("q10_demo_acceptance", TOOL)
q10 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(q10)

MANIFEST_PATH = ROOT / "blueprint" / "runtime" / "q10_demo_acceptance" / "FINAL_BUILD511_CANDIDATE.json"
MATRIX_PATH = ROOT / "blueprint" / "runtime" / "q10_demo_acceptance" / "FINAL_BUILD511_STAGE_MATRIX.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_candidate_identity_is_exact():
    manifest = load(MANIFEST_PATH)
    result = q10.verify_candidate(ROOT, manifest)
    assert result["status"] == "PASS"
    assert result["source_sha256"] == manifest["source_sha256"]
    assert result["source_neutral_after_freeze"] is True


def test_demo_probe_accepts_hfm_demo_and_blocks_live(tmp_path: Path):
    manifest = load(MANIFEST_PATH)
    demo_log = tmp_path / "demo.log"
    demo_log.write_text(
        "x [Q10-DEMO-ID]|Demo=Y|Connected=Y|TradeAllowed=N|"
        "Server=HFM-Demo|Company=HF Markets|TerminalBuild=1479\n",
        encoding="utf-8",
    )
    good = q10.inspect_demo_log(demo_log, manifest)
    assert good["status"] == "PASS"
    assert good["demo"] is True
    assert good["connected"] is True

    live_log = tmp_path / "live.log"
    live_log.write_text(
        "[Q10-DEMO-ID]|Demo=N|Connected=Y|TradeAllowed=Y|"
        "Server=HFM-Live|Company=HF Markets|TerminalBuild=1479\n",
        encoding="utf-8",
    )
    blocked = q10.inspect_demo_log(live_log, manifest)
    assert blocked["status"] == "BLOCKED"
    assert "ACCOUNT_NOT_DEMO" in blocked["reason"]


def test_demo_gate_blocks_missing_or_non_hfm_evidence(tmp_path: Path):
    manifest = load(MANIFEST_PATH)
    missing = q10.inspect_demo_log(tmp_path / "missing.log", manifest)
    assert missing["status"] == "BLOCKED"

    other = tmp_path / "other.log"
    other.write_text(
        "[Q10-DEMO-ID]|Demo=Y|Connected=Y|TradeAllowed=Y|"
        "Server=OtherBroker-Demo|Company=Other Broker|TerminalBuild=1479\n",
        encoding="utf-8",
    )
    result = q10.inspect_demo_log(other, manifest)
    assert result["status"] == "BLOCKED"
    assert "BROKER_NOT_HFM" in result["reason"]


def test_probe_launch_is_read_only_and_credential_free(tmp_path: Path):
    root = tmp_path / "dedicated"
    experts = root / "MQL4" / "Experts"
    experts.mkdir(parents=True)
    terminal = root / "terminal.exe"
    terminal.write_bytes(b"terminal")
    probe = experts / "Q10_DEMO_IDENTITY_PROBE.ex4"
    probe.write_bytes(b"probe")

    manifest = load(MANIFEST_PATH)
    manifest = dict(manifest)
    manifest["demo_probe_ex4_sha256"] = q10.sha256_file(probe)
    out = tmp_path / "probe.ini"
    result = q10.generate_probe_launch_config(
        root, probe, out, "GBPUSD", "M15", manifest
    )
    text = out.read_text(encoding="utf-8")
    assert result["status"] == "PASS"
    assert result["experts_trades"] is False
    assert "ExpertsTrades=false" in text
    assert "Login=" not in text
    assert "Password=" not in text

    with pytest.raises(q10.Q10Error, match="primary terminal"):
        q10.generate_probe_launch_config(
            root, probe, tmp_path / "blocked.ini", "GBPUSD", "M15",
            manifest, primary_terminal=terminal
        )


def test_runtime_artifact_hash_and_primary_terminal_guards(tmp_path: Path):
    root = tmp_path / "dedicated"
    (root / "MQL4" / "Experts").mkdir(parents=True)
    (root / "presets").mkdir()
    terminal = root / "terminal.exe"
    terminal.write_bytes(b"terminal")
    ex4 = root / "MQL4" / "Experts" / "BBMA_EA.ex4"
    ex4.write_bytes(b"candidate-ex4")
    settings = root / "presets" / "candidate.set"
    settings.write_bytes(b"settings")

    manifest = load(MANIFEST_PATH)
    manifest = dict(manifest)
    manifest["native_ex4_sha256"] = q10.sha256_file(ex4)
    manifest["settings_sha256"] = q10.sha256_file(settings)

    result = q10.verify_runtime_artifacts(root, ex4, settings, manifest)
    assert result["status"] == "PASS"

    with pytest.raises(q10.Q10Error, match="primary terminal"):
        q10.verify_runtime_artifacts(
            root, ex4, settings, manifest, primary_terminal=terminal
        )

    outside = tmp_path / "outside.set"
    outside.write_bytes(b"settings")
    with pytest.raises(q10.Q10Error, match="settings must reside"):
        q10.verify_runtime_artifacts(root, ex4, outside, manifest)


def make_state():
    return {
        "demo_auth": {"status": "PASS", "log_sha256": "DEMOHASH"},
        "candidate": {
            "source_sha256": "SRC",
            "build_tag": "V511_EVENT_DRIVEN_OBSERVER_20260922",
        },
        "stage_order": ["R3", "R4", "R5", "R6"],
        "stages": {
            x: {"status": "INCOMPLETE", "evidence": []}
            for x in ["R3", "R4", "R5", "R6"]
        },
    }


def write_analysis(tmp_path: Path, state, stage: str, status: str) -> Path:
    path = tmp_path / f"{stage}_{status}.json"
    path.write_text(
        json.dumps(
            {
                "schema": "BBMA_Q10_STAGE_ANALYSIS_V1",
                "stage": stage,
                "status": status,
                "candidate_source_sha256": state["candidate"]["source_sha256"],
                "candidate_build_tag": state["candidate"]["build_tag"],
                "bundle_sha256": "BUNDLE",
                "cases": {},
            }
        ),
        encoding="utf-8",
    )
    return path


def make_bundle(tmp_path: Path, stage: str = "R3"):
    raw = tmp_path / f"{stage}_raw.log"
    raw.write_text("[D1-03][OWNER] BUY\n", encoding="utf-8")
    excerpt = tmp_path / f"{stage}_matched.log"
    excerpt.write_text("[D1-03][OWNER] BUY\n", encoding="utf-8")
    return {
        "schema": "BBMA_Q10_STAGE_BUNDLE_V1",
        "stage": stage,
        "candidate_source_sha256": "SRC",
        "candidate_build_tag": "V511_EVENT_DRIVEN_OBSERVER_20260922",
        "demo_evidence_sha256": "DEMOHASH",
        "raw_log_path": str(raw),
        "raw_log_sha256": q10.sha256_file(raw),
        "matched_excerpt": str(excerpt),
        "matched_excerpt_sha256": q10.sha256_file(excerpt),
        "marker_counts": {},
        "marker_lines": 1,
    }


def test_stage_selection_is_ordered_and_fail_closed(tmp_path: Path):
    state = make_state()
    assert q10.next_stage(state) == {"status": "INCOMPLETE", "next": "R3"}
    r3 = write_analysis(tmp_path, state, "R3", "PASS")
    q10.record_stage(state, "R3", "PASS", str(r3))
    assert q10.next_stage(state)["next"] == "R4"
    r4 = write_analysis(tmp_path, state, "R4", "FAIL")
    q10.record_stage(state, "R4", "FAIL", str(r4))
    assert q10.next_stage(state) == {"status": "FAIL", "next": "R4"}

    blocked = make_state()
    blocked["demo_auth"]["status"] = "BLOCKED"
    assert q10.next_stage(blocked) == {"status": "BLOCKED", "next": "AUTH"}


def test_launch_config_is_credential_free_and_ordered(tmp_path: Path):
    root = tmp_path / "dedicated"
    (root / "MQL4" / "Experts").mkdir(parents=True)
    (root / "presets").mkdir()
    (root / "terminal.exe").write_bytes(b"terminal")
    ex4 = root / "MQL4" / "Experts" / "BBMA_EA_BUILD511.ex4"
    ex4.write_bytes(b"candidate")
    settings = root / "presets" / "final.set"
    settings.write_bytes(b"settings")

    manifest = load(MANIFEST_PATH)
    manifest = dict(manifest)
    manifest["native_ex4_sha256"] = q10.sha256_file(ex4)
    manifest["settings_sha256"] = q10.sha256_file(settings)
    state = make_state()
    out = tmp_path / "r3.ini"

    primary = tmp_path / "primary" / "terminal.exe"
    result = q10.generate_launch_config(
        "R3", state, root, ex4, settings, out, "GBPUSD", "M15", manifest,
        primary_terminal=primary,
    )
    text = out.read_text(encoding="utf-8")
    assert result["status"] == "PASS"
    assert "ExpertsTrades=true" in text
    assert "Expert=BBMA_EA_BUILD511" in text
    assert "Login=" not in text
    assert "Password=" not in text
    assert result["contains_credentials"] is False

    with pytest.raises(q10.Q10Error, match="primary terminal"):
        q10.generate_launch_config(
            "R3", state, root, ex4, settings, tmp_path / "primary.ini",
            "GBPUSD", "M15", manifest, primary_terminal=root / "terminal.exe"
        )

    with pytest.raises(q10.Q10Error, match="stage ordering"):
        q10.generate_launch_config(
            "R4", state, root, ex4, settings, tmp_path / "r4.ini",
            "GBPUSD", "M15", manifest, primary_terminal=primary
        )


def test_collector_redacts_account_login_and_counts_markers(tmp_path: Path):
    state = make_state()
    log = tmp_path / "runtime.log"
    log.write_text(
        "Account=123456 [D1-03][OWNER] BUY\n"
        "Login: 987654 [P3M2][DECISION_FINAL] State=DEC_EXECUTED\n"
        "noise\n",
        encoding="utf-8",
    )
    bundle = q10.collect_stage_log("R3", log, tmp_path / "bundle", state)
    excerpt = Path(bundle["matched_excerpt"]).read_text(encoding="utf-8")
    assert "123456" not in excerpt
    assert "987654" not in excerpt
    assert "Account=<redacted>" in excerpt
    assert "Login=<redacted>" in excerpt
    assert bundle["marker_counts"]["[D1-03][OWNER]"] == 1
    assert bundle["marker_counts"]["[P3M2][DECISION_FINAL]"] == 1


def test_assertion_analyzer_never_promotes_incomplete_to_pass(tmp_path: Path):
    matrix = load(MATRIX_PATH)
    bundle = make_bundle(tmp_path)
    evidence = bundle["raw_log_path"]

    incomplete = tmp_path / "incomplete.json"
    incomplete.write_text(
        json.dumps({"cases": {"R3-00": {"status": "PASS", "evidence": [evidence]}}}),
        encoding="utf-8",
    )
    result = q10.analyze_assertions("R3", incomplete, matrix, bundle)
    assert result["status"] == "INCOMPLETE"
    assert result["cases"]["R3-00"]["evidence"][0]["sha256"] == bundle["raw_log_sha256"]

    all_cases = {
        row["id"]: {"status": "PASS", "evidence": [evidence]}
        for row in matrix["stages"]["R3"]["cases"]
    }
    complete = tmp_path / "complete.json"
    complete.write_text(json.dumps({"cases": all_cases}), encoding="utf-8")
    result = q10.analyze_assertions("R3", complete, matrix, bundle)
    assert result["status"] == "PASS"

    all_cases["R3-07"]["status"] = "FAIL"
    failed = tmp_path / "failed.json"
    failed.write_text(json.dumps({"cases": all_cases}), encoding="utf-8")
    result = q10.analyze_assertions("R3", failed, matrix, bundle)
    assert result["status"] == "FAIL"

    missing = tmp_path / "missing.json"
    missing.write_text(
        json.dumps({"cases": {"R3-00": {"status": "PASS", "evidence": ["missing.log"]}}}),
        encoding="utf-8",
    )
    with pytest.raises(q10.Q10Error, match="evidence missing"):
        q10.analyze_assertions("R3", missing, matrix, bundle)

    tampered = dict(bundle)
    tampered["raw_log_sha256"] = "0" * 64
    with pytest.raises(q10.Q10Error, match="bundle evidence hash mismatch"):
        q10.analyze_assertions("R3", incomplete, matrix, tampered)




def test_record_stage_requires_bound_analysis(tmp_path: Path):
    state = make_state()
    good = write_analysis(tmp_path, state, "R3", "PASS")
    q10.record_stage(state, "R3", "PASS", str(good))
    assert state["stages"]["R3"]["status"] == "PASS"
    assert state["stages"]["R3"]["evidence"][0]["sha256"] == q10.sha256_file(good)

    with pytest.raises(q10.Q10Error, match="analysis artifact"):
        q10.record_stage(make_state(), "R3", "PASS", None)

    bad = write_analysis(tmp_path, make_state(), "R3", "PASS")
    doc = json.loads(bad.read_text(encoding="utf-8"))
    doc["candidate_source_sha256"] = "WRONG"
    bad.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(q10.Q10Error, match="candidate source mismatch"):
        q10.record_stage(make_state(), "R3", "PASS", str(bad))


def test_identity_probe_is_read_only_and_hash_bound():
    probe_path = (
        ROOT
        / "blueprint"
        / "runtime"
        / "q10_demo_acceptance"
        / "Q10_DEMO_IDENTITY_PROBE.mq4"
    )
    probe = probe_path.read_text(encoding="utf-8")
    manifest = load(MANIFEST_PATH)
    for forbidden in ("OrderSend(", "OrderClose(", "OrderModify(", "OrderDelete("):
        assert forbidden not in probe
    assert "AccountNumber(" not in probe
    assert "[Q10-DEMO-ID]" in probe
    assert q10.sha256_file(probe_path) == manifest["demo_probe_mq4_sha256"]


def test_stage_matrix_is_bound_to_current_build_semantics():
    matrix = load(MATRIX_PATH)
    semantics = matrix["current_build_semantics"]
    assert semantics["processing_clock"] == "M15"
    assert semantics["closed_candle_core"] is True
    assert semantics["n3_execution_policy"] == "NONE"
    assert semantics["m12n_authority"] == "observation/read-only"
    assert semantics["trade_lock"]["LOCK_OFF"] == 0
    assert semantics["trade_lock"]["LOCK_SAME_DIRECTION"] == 1
    assert semantics["trade_lock"]["LOCK_ONE_POSITION"] == 2


def test_clean_restart_helper_is_graceful_fail_closed():
    script = (
        ROOT
        / "blueprint"
        / "runtime"
        / "q10_demo_acceptance"
        / "q10_demo_clean_restart.ps1"
    ).read_text(encoding="utf-8")
    assert "CloseMainWindow()" in script
    assert "force_kill = $false" in script
    assert "GRACEFUL_CLOSE_TIMEOUT" in script
    assert "post_close" in script
    assert "Start-Process" in script
    assert "Stop-Process" not in script
    assert "taskkill" not in script.lower()
    assert "CREDENTIAL_FIELD_PRESENT" in script
    assert "DEDICATED_EQUALS_PRIMARY" in script
