from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.bbma_orchestrator.evidence import EvidenceDB


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _manifest(root: Path, run_id: str, *, parent_run_id: str | None = None) -> dict:
    artifact_text = "immutable test artifact"
    (root / "artifact.txt").write_text(artifact_text, encoding="utf-8")
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "hypothesis": {"id": "HYP-1", "parameter_sha256": _sha("parameters")},
        "build": {
            "build_id": "BUILD-1", "source_commit": "a" * 40,
            "source_sha256": _sha("source"), "ex4_sha256": _sha("ex4"), "set_sha256": _sha("set"),
        },
        "dataset": {"dataset_id": "DATA-1", "sha256": _sha("dataset"), "symbol": "GBPUSD", "timeframe": "M15"},
        "environment": {"broker": "demo", "terminal_build": "MT4-test"},
        "costs": {"spread_model": "Bid/Ask", "commission_model": "broker", "swap_included": True},
        "protocol": {"partition": "OOS"},
        "artifacts": [{"kind": "report", "path": "artifact.txt", "sha256": _sha(artifact_text)}],
    }
    if parent_run_id:
        result["parent_run_id"] = parent_run_id
    return result


def _write_manifest(root: Path, manifest: dict) -> Path:
    path = root / f"{manifest['run_id']}.json"
    path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path


class ExperimentInventoryTests(unittest.TestCase):
    def test_register_is_idempotent_and_run_id_collision_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = _manifest(root, "RUN-1")
            path = _write_manifest(root, manifest)
            with EvidenceDB(root / "evidence.sqlite") as db:
                first = db.register_experiment(manifest, path, root, run_status="EVIDENCE_ACCEPTED")
                second = db.register_experiment(manifest, path, root, run_status="EVIDENCE_ACCEPTED")
                self.assertTrue(first["created"])
                self.assertFalse(second["created"])
                self.assertEqual(first["manifest_sha256"], second["manifest_sha256"])
                self.assertEqual(db.get_node("experiment:RUN-1")["status"], "NOT VERIFIED")
                changed = dict(manifest)
                changed["hypothesis"] = {**manifest["hypothesis"], "statement": "changed manifest"}
                path.write_text(json.dumps(changed, sort_keys=True, indent=2) + "\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "run_id collision"):
                    db.register_experiment(changed, path, root, run_status="INVALID_RUN")

    def test_same_configuration_runs_and_parent_lineage_are_queryable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first_manifest = _manifest(root, "RUN-1")
            first_path = _write_manifest(root, first_manifest)
            second_manifest = _manifest(root, "RUN-2", parent_run_id="RUN-1")
            second_path = _write_manifest(root, second_manifest)
            with EvidenceDB(root / "evidence.sqlite") as db:
                first = db.register_experiment(first_manifest, first_path, root, run_status="EVIDENCE_ACCEPTED")
                second = db.register_experiment(second_manifest, second_path, root, run_status="RUN_FAILED")
                self.assertEqual(first["fingerprint"], second["fingerprint"])
                runs = db.find_experiment_runs(first["fingerprint"])
                self.assertEqual({item["run_id"] for item in runs}, {"RUN-1", "RUN-2"})
                self.assertEqual(db.get_experiment_run("RUN-2")["parent_run_id"], "RUN-1")
                edge = db.conn.execute(
                    "SELECT 1 FROM edges WHERE src=? AND dst=?",
                    ("experiment:RUN-1", "experiment:RUN-2"),
                ).fetchone()
                self.assertIsNotNone(edge)
                artifact_edge = db.conn.execute(
                    "SELECT 1 FROM edges WHERE src=? AND dst=?",
                    ("experiment-artifact:RUN-2:report", "experiment:RUN-2"),
                ).fetchone()
                self.assertIsNotNone(artifact_edge)
                self.assertEqual(db.get_node("experiment:RUN-2")["status"], "NOT VERIFIED")

    def test_missing_or_tampered_artifact_is_recorded_as_failed_evidence_not_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = _manifest(root, "RUN-INVALID")
            manifest["artifacts"][0]["sha256"] = "0" * 64
            path = _write_manifest(root, manifest)
            with EvidenceDB(root / "evidence.sqlite") as db:
                result = db.register_experiment(manifest, path, root, run_status="INVALID_RUN")
                record = db.get_experiment_run("RUN-INVALID")
                self.assertEqual(record["run_status"], "INVALID_RUN")
                self.assertTrue(result["created"])
                self.assertEqual(db.conn.execute(
                    "SELECT COUNT(*) FROM nodes WHERE node_id='experiment-artifact:RUN-INVALID:report'"
                ).fetchone()[0], 0)
                self.assertTrue(db.get_node("experiment:RUN-INVALID")["metadata"]["artifact_errors"])


if __name__ == "__main__":
    unittest.main()
