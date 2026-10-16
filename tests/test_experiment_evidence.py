from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.bbma_orchestrator.experiment import (
    classify_run_status,
    validate_manifest,
    verify_artifacts,
)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def valid_manifest(root: Path) -> dict:
    files = {}
    for kind, name, content in (
        ("source", "EA.mq4", "source"),
        ("ex4", "EA.ex4", "ex4"),
        ("set", "EA.set", "set"),
        ("parameters", "parameters.json", "parameters"),
        ("dataset", "dataset.csv", "dataset"),
        ("trade_history", "trades.csv", "ticket,net\n1,10\n"),
        ("tester_report", "report.htm", "tester report"),
        ("tester_log", "tester.log", "tester log"),
    ):
        (root / name).write_text(content, encoding="utf-8")
        files[kind] = {"kind": kind, "path": name, "sha256": _hash(content)}
    return {
        "schema_version": 1,
        "run_id": "BBMA-EXP-0001",
        "hypothesis": {
            "id": "HYP-001", "statement": "Pre-registered test hypothesis",
            "preregistered_at": "2026-01-01T00:00:00Z",
            "parameter_sha256": _hash("parameters"), "parameters_frozen": True,
        },
        "build": {
            "build_id": "BUILD-TEST-1", "source_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "source_sha256": _hash("source"), "ex4_sha256": _hash("ex4"),
            "set_sha256": _hash("set"),
        },
        "dataset": {
            "dataset_id": "DATA-001", "sha256": _hash("dataset"),
            "symbol": "GBPUSD", "timeframe": "M15", "source_type": "broker-native",
            "price_basis": "BID_ASK_TICKS", "synthetic_ticks": False,
            "timezone": "UTC", "start": "2026-01-01T00:00:00Z",
            "end": "2026-09-01T00:00:00Z", "warmup_start": "2025-12-01T00:00:00Z",
            "evaluation_start": "2026-02-01T00:00:00Z",
            "evaluation_end": "2026-08-01T00:00:00Z", "closed_candles_only": True,
        },
        "environment": {
            "broker": "DemoBroker", "terminal_build": "MT4-test", "tester_mode": "real-ticks",
        },
        "costs": {
            "spread_model": "recorded Bid/Ask", "commission_model": "broker schedule",
            "swap_included": True, "slippage_model": "recorded/explained",
        },
        "protocol": {
            "partition": "OOS", "frozen_at": "2026-01-15T00:00:00Z",
            "parameter_freeze_sha256": _hash("parameters"), "oos_tuning_performed": False,
        },
        "artifacts": list(files.values()),
    }


class ExperimentEvidenceTests(unittest.TestCase):
    def test_valid_manifest_passes_schema_checks_and_artifact_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = valid_manifest(root)
            self.assertEqual(validate_manifest(manifest), [])
            self.assertEqual(verify_artifacts(manifest, root), [])
            self.assertEqual(classify_run_status([], [], process_exit_code=0, validation_complete=True), "EVIDENCE_ACCEPTED")

    def test_missing_identity_and_malformed_hash_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = valid_manifest(Path(tmp))
            manifest["run_id"] = ""
            manifest["build"]["ex4_sha256"] = "bad"
            errors = validate_manifest(manifest)
            self.assertTrue(any("run_id" in item for item in errors))
            self.assertTrue(any("ex4_sha256" in item for item in errors))
            self.assertEqual(classify_run_status(errors, [], process_exit_code=0, validation_complete=True), "INVALID_RUN")

    def test_oos_tuning_or_late_freeze_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = valid_manifest(Path(tmp))
            manifest["protocol"]["oos_tuning_performed"] = True
            manifest["protocol"]["frozen_at"] = "2026-03-01T00:00:00Z"
            errors = validate_manifest(manifest)
            self.assertTrue(any("oos_tuning_performed" in item for item in errors))
            self.assertTrue(any("frozen_at" in item for item in errors))

    def test_invalid_time_window_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = valid_manifest(Path(tmp))
            manifest["dataset"]["evaluation_start"] = "2026-09-01T00:00:00Z"
            manifest["dataset"]["evaluation_end"] = "2026-08-01T00:00:00Z"
            errors = validate_manifest(manifest)
            self.assertTrue(any("chronology" in item or "warmup_start" in item for item in errors))

    def test_synthetic_ticks_and_live_candle_contract_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = valid_manifest(Path(tmp))
            manifest["dataset"]["synthetic_ticks"] = True
            manifest["dataset"]["closed_candles_only"] = False
            errors = validate_manifest(manifest)
            self.assertTrue(any("synthetic_ticks" in item for item in errors))
            self.assertTrue(any("closed_candles_only" in item for item in errors))

    def test_artifact_hash_mismatch_and_root_escape_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = valid_manifest(root)
            (root / "trades.csv").write_text("tampered", encoding="utf-8")
            errors = verify_artifacts(manifest, root)
            self.assertTrue(any("mismatch" in item for item in errors))
            manifest["artifacts"][0]["path"] = "../outside.csv"
            errors = verify_artifacts(manifest, root)
            self.assertTrue(any("escapes evidence root" in item for item in errors))

    def test_failed_process_and_incomplete_validation_are_not_accepted(self):
        self.assertEqual(classify_run_status([], [], process_exit_code=2, validation_complete=True), "RUN_FAILED")
        self.assertEqual(classify_run_status([], [], process_exit_code=0, validation_complete=False), "VALIDATION_FAILED")
        self.assertEqual(classify_run_status(["bad"], [], process_exit_code=0, validation_complete=True), "INVALID_RUN")
