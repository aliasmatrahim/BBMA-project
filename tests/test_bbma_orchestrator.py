from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.bbma_orchestrator.core import (
    RegressionSelector,
    TaskManifest,
    TaskStore,
    atomic_write_json,
    build_context_pack,
    compute_risk_score,
    route_model,
)
from tools.bbma_orchestrator.evidence import ContentAddressedStore, EvidenceDB, build_evidence_package, sha256_file
from tools.bbma_orchestrator.telemetry import TelemetryStore
from tools.bbma_orchestrator.native import NativeAdapter, artifact_identity
from tools.bbma_orchestrator.trace import (
    DEFAULT_TRANSITIONS,
    LifecycleModel,
    classify_build_delta,
    compare_shadow,
    mutation_self_test,
    randomized_lifecycle_check,
    validate_transition_table,
)

class TaskStateTests(unittest.TestCase):
    def test_manifest_phase_and_pass_gate(self):
        manifest = TaskManifest("T1", "R1", "x", "implementation")
        manifest.transition("PREFLIGHT")
        manifest.transition("IN_PROGRESS")
        manifest.transition("VALIDATION")
        manifest.transition("CLOSED")
        manifest.result = "PASS"
        manifest.validate()
        self.assertEqual(manifest.phase, "CLOSED")

    def test_manifest_rejects_skip(self):
        manifest = TaskManifest("T1", "R1", "x", "runtime")
        with self.assertRaises(ValueError):
            manifest.transition("VALIDATION")

    def test_pass_before_closed_rejected(self):
        manifest = TaskManifest("T1", "R1", "x", "runtime", result="PASS")
        with self.assertRaises(ValueError):
            manifest.validate()

    def test_atomic_write_preserves_old_file_on_injected_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            atomic_write_json(path, {"version": 1})
            with self.assertRaises(RuntimeError):
                atomic_write_json(path, {"version": 2}, inject_failure=True)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["version"], 1)

    def test_store_checkpoint_handoff_and_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(tmp)
            manifest = TaskManifest(
                "T1",
                "R1",
                "x",
                "implementation",
                branch="b",
                commit="abc",
                latest_verified_step="phase-1",
                next_safe_action="phase-2",
                do_not_redo=["phase-1"],
            )
            store.save(manifest)
            store.append_event(manifest, "START")
            checkpoint = store.checkpoint(manifest, "after-phase-1")
            self.assertTrue(checkpoint.exists())
            self.assertTrue(store.events_path.exists())
            capsule = store.handoff_capsule(manifest)
            self.assertLessEqual(len(capsule.splitlines()), 40)
            self.assertIn("DoNotRedo: phase-1", capsule)

    def test_risk_and_model_routing(self):
        risk = compute_risk_score(strategy_core=True, execution_authority=True, code_change=True)
        self.assertGreaterEqual(risk, 60)
        self.assertEqual(route_model("implementation", risk_score=risk, strategy_core=True), "HIGH/XHIGH")
        self.assertEqual(route_model("hash", risk_score=0), "LIGHT")

    def test_regression_selector_uses_supplied_map_only(self):
        selector = RegressionSelector(
            {
                "M12": {"tests": ["t12"], "consumers": ["M13"]},
                "M13": {"tests": ["t13"], "consumers": []},
            },
            mandatory_global=["global"],
        )
        self.assertEqual(selector.select(["M12"]), ["global", "t12", "t13"])
        self.assertEqual(selector.select(["UNKNOWN"]), ["global"])

    def test_context_pack_is_bounded_to_supplied_refs(self):
        manifest = TaskManifest("T1", "R1", "x", "source")
        pack = build_context_pack(
            manifest,
            authority_refs=["CURRENT", "SOURCE_INDEX"],
            changed_modules=["M12"],
            selected_validations=["t12"],
            evidence_nodes=["core:re"],
        )
        self.assertEqual(pack["authority_refs"], ["CURRENT", "SOURCE_INDEX"])
        self.assertNotIn("history", pack)

class VerifiedModuleGraphTests(unittest.TestCase):
    def test_graph_covers_all_modules_and_cites_every_verified_edge(self):
        from tools.bbma_orchestrator.verified import load_verified_module_graph

        root = Path(__file__).resolve().parents[1]
        graph = load_verified_module_graph(root / "config" / "bbma_module_graph.json")
        expected = {f"M{i:02d}" for i in range(1, 28)} | {"M12N"}
        self.assertEqual(set(graph["modules"]), expected)
        for module_id, module in graph["modules"].items():
            self.assertEqual(module["module_id"], module_id)
            self.assertIn(module["status"], {"VERIFIED", "NOT VERIFIED", "HOLD"})
            self.assertTrue(module["ownership"])
            self.assertTrue(module["evidence"])
            for consumer in module["consumers"]:
                self.assertIn(consumer["module"], expected)
                self.assertTrue(consumer["evidence"])

    def test_graph_rejects_uncited_consumer_edge(self):
        from tools.bbma_orchestrator.verified import load_verified_module_graph

        graph = self._minimal_graph()
        graph["modules"]["M01"]["consumers"] = [
            {"module": "M02", "relationship": "declares shared types", "evidence": []}
        ]
        self._assert_invalid_graph(graph, "consumer evidence")

    def test_graph_rejects_unknown_consumer_module(self):
        from tools.bbma_orchestrator.verified import load_verified_module_graph

        graph = self._minimal_graph()
        graph["modules"]["M01"]["consumers"] = [
            {"module": "M99", "relationship": "invalid", "evidence": ["SOURCE"]}
        ]
        self._assert_invalid_graph(graph, "unknown consumer")

    def test_graph_rejects_malformed_authority_commit(self):
        graph = self._minimal_graph()
        graph["authority"]["commit"] = "not-a-commit"
        self._assert_invalid_graph(graph, "authority commit")

    def test_graph_rejects_invalid_coverage_claim(self):
        graph = self._minimal_graph()
        graph["coverage"]["consumer_edges"] = "COMPLETE"
        self._assert_invalid_graph(graph, "consumer-edge coverage")

    def test_graph_rejects_false_verified_module_coverage(self):
        graph = self._minimal_graph()
        graph["modules"]["M01"]["status"] = "NOT VERIFIED"
        self._assert_invalid_graph(graph, "module-identity coverage")

    def test_graph_rejects_partial_coverage_without_known_unknowns(self):
        graph = self._minimal_graph()
        graph["known_unknowns"] = []
        self._assert_invalid_graph(graph, "known_unknowns")

    def test_graph_rejects_evidence_from_other_commit(self):
        graph = self._minimal_graph()
        graph["evidence_catalog"]["SOURCE"]["commit"] = "c" * 40
        self._assert_invalid_graph(graph, "evidence SOURCE commit")

    def _minimal_graph(self):
        evidence = {
            "SOURCE": {
                "repository": "owner/repo",
                "commit": "a" * 40,
                "path": "source",
                "blob_sha": "b" * 40,
                "locator": "module header",
            }
        }
        modules = {
            module_id: {
                "module_id": module_id,
                "ownership": "owner",
                "status": "VERIFIED",
                "evidence": ["SOURCE"],
                "consumers": [],
            }
            for module_id in ({f"M{i:02d}" for i in range(1, 28)} | {"M12N"})
        }
        return {
            "schema_version": 1,
            "authority": {
                "repository": "owner/repo",
                "branch": "verified-source",
                "commit": "a" * 40,
            },
            "coverage": {
                "module_identity": "VERIFIED",
                "consumer_edges": "PARTIAL",
                "tests": "NOT VERIFIED",
            },
            "evidence_catalog": evidence,
            "modules": modules,
            "known_unknowns": ["Consumer edges are intentionally partial."],
        }

    def _assert_invalid_graph(self, graph, message):
        from tools.bbma_orchestrator.verified import load_verified_module_graph

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graph.json"
            path.write_text(json.dumps(graph), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                load_verified_module_graph(path)


class VerifiedTraceabilityTests(unittest.TestCase):
    def test_traceability_covers_existing_core_ids_without_false_runtime_pass(self):
        from tools.bbma_orchestrator.verified import load_verified_traceability

        root = Path(__file__).resolve().parents[1]
        traceability = load_verified_traceability(
            root / "config" / "bbma_traceability.json",
            root / "config" / "bbma_module_graph.json",
        )
        expected = {f"CORE-V2-F{i}" for i in range(1, 7)}
        self.assertEqual(set(traceability["rules"]), expected)
        for rule in traceability["rules"].values():
            self.assertEqual(rule["stages"]["runtime"]["status"], "NOT VERIFIED")
            self.assertEqual(rule["stages"]["runtime"]["evidence"], [])

    def test_traceability_uses_regression_drivers_and_preserves_f4_test_gap(self):
        from tools.bbma_orchestrator.verified import load_verified_traceability

        root = Path(__file__).resolve().parents[1]
        traceability = load_verified_traceability(
            root / "config" / "bbma_traceability.json",
            root / "config" / "bbma_module_graph.json",
        )
        catalog = traceability["evidence_catalog"]
        expected_drivers = {
            "CORE-V2-F1": ".github/workflows/core-v2-f1-pr-dispatch.yml",
            "CORE-V2-F2": ".github/workflows/core-v2-f2-pr-dispatch.yml",
            "CORE-V2-F3": ".github/workflows/core-v2-f3-pr-dispatch.yml",
            "CORE-V2-F5": ".github/workflows/core-v2-f5-pr-dispatch.yml",
            "CORE-V2-F6": ".github/workflows/core-v2-f6-pr-dispatch.yml",
        }
        for rule_id, expected_path in expected_drivers.items():
            refs = traceability["rules"][rule_id]["stages"]["test"]["evidence"]
            self.assertIn(expected_path, {catalog[ref]["path"] for ref in refs})

        f4_source_refs = traceability["rules"]["CORE-V2-F4"]["stages"]["source_evidence"]["evidence"]
        f4_source_paths = {catalog[ref]["path"] for ref in f4_source_refs}
        self.assertIn(
            "blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md",
            f4_source_paths,
        )
        self.assertIn(
            "blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md",
            f4_source_paths,
        )
        f4_code = traceability["rules"]["CORE-V2-F4"]["stages"]["code"]
        self.assertEqual(f4_code["status"], "SOURCE CONFLICT")
        self.assertEqual(
            {catalog[ref]["path"] for ref in f4_code["evidence"]},
            {
                "blueprint/source/BBMA_EA.mq4",
                "blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md",
                "blueprint/audits/POSTFREEZE_D1_M11_M15_M16_REAUDIT_20260909.md",
            },
        )
        self.assertTrue(f4_code["gap"])
        f4_test = traceability["rules"]["CORE-V2-F4"]["stages"]["test"]
        self.assertEqual(f4_test["status"], "PARTIAL")
        self.assertTrue(f4_test["gap"])

    def test_traceability_materializes_into_existing_evidence_dag(self):
        from tools.bbma_orchestrator.verified import materialize_traceability

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            result = materialize_traceability(
                root / "config" / "bbma_traceability.json",
                root / "config" / "bbma_module_graph.json",
                Path(tmp) / "evidence.db",
            )
            self.assertEqual(result, {"rules": 6, "nodes": 42, "edges": 36})
            with EvidenceDB(Path(tmp) / "evidence.db") as db:
                node = db.get_node("trace:CORE-V2-F2:runtime")
                self.assertEqual(node["status"], "NOT VERIFIED")
                edge_count = db.conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
                self.assertEqual(edge_count, 36)

    def test_traceability_materialization_binds_resolved_evidence_identity(self):
        from tools.bbma_orchestrator.verified import materialize_traceability

        root = Path(__file__).resolve().parents[1]
        original = json.loads(
            (root / "config" / "bbma_traceability.json").read_text(encoding="utf-8")
        )
        changed = json.loads(json.dumps(original))
        changed["evidence_catalog"]["SRC_PRIMARY_PDF"]["locator"] = "different verified locator"
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            original_path = work / "original.json"
            changed_path = work / "changed.json"
            original_path.write_text(json.dumps(original), encoding="utf-8")
            changed_path.write_text(json.dumps(changed), encoding="utf-8")
            materialize_traceability(
                original_path, root / "config" / "bbma_module_graph.json", work / "original.db"
            )
            materialize_traceability(
                changed_path, root / "config" / "bbma_module_graph.json", work / "changed.db"
            )
            with EvidenceDB(work / "original.db") as db:
                original_node = db.get_node("trace:CORE-V2-F1:source_evidence")
            with EvidenceDB(work / "changed.db") as db:
                changed_node = db.get_node("trace:CORE-V2-F1:source_evidence")

        self.assertNotEqual(original_node["digest"], changed_node["digest"])
        evidence_record = changed_node["metadata"]["evidence_records"][0]
        self.assertEqual(evidence_record["evidence_id"], "SRC_PRIMARY_PDF")
        self.assertEqual(evidence_record["locator"], "different verified locator")

    def test_traceability_rejects_forged_blob_identity(self):
        data = self._traceability_data()
        data["evidence_catalog"]["SRC_PRIMARY_PDF"]["blob_sha"] = "f" * 40
        self._assert_invalid_traceability(data, "blob mismatch")

    def test_traceability_cli_materializes_verified_map(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp, io.StringIO() as output:
            with contextlib.redirect_stdout(output):
                exit_code = main([
                    "traceability-materialize",
                    "--traceability", str(root / "config" / "bbma_traceability.json"),
                    "--module-graph", str(root / "config" / "bbma_module_graph.json"),
                    "--db", str(Path(tmp) / "evidence.db"),
                ])
            self.assertEqual(exit_code, 0)
            self.assertEqual(json.loads(output.getvalue())["nodes"], 42)

    def test_traceability_rejects_duplicate_evidence_reference(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads(
            (root / "config" / "bbma_traceability.json").read_text(encoding="utf-8")
        )
        refs = data["rules"]["CORE-V2-F1"]["stages"]["source_evidence"]["evidence"]
        refs.append(refs[0])
        self._assert_invalid_traceability(data, "duplicate evidence")

    def test_traceability_rejects_false_verified_runtime(self):
        data = self._traceability_data()
        runtime = data["rules"]["CORE-V2-F2"]["stages"]["runtime"]
        runtime["status"] = "VERIFIED"
        self._assert_invalid_traceability(data, "verified runtime stage needs evidence")

    def test_traceability_rejects_unknown_module(self):
        data = self._traceability_data()
        data["rules"]["CORE-V2-F3"]["stages"]["module"]["modules"] = ["M99"]
        self._assert_invalid_traceability(data, "unknown modules")

    def test_traceability_rejects_evidence_kind_mismatch(self):
        data = self._traceability_data()
        data["rules"]["CORE-V2-F3"]["stages"]["code"]["evidence"] = ["SRC_V01"]
        self._assert_invalid_traceability(data, "evidence kind mismatch")

    def test_traceability_rejects_authority_mismatch(self):
        data = self._traceability_data()
        data["authority"]["commit"] = "c" * 40
        self._assert_invalid_traceability(data, "must match module graph authority")

    def test_traceability_rejects_rules_outside_exact_f1_through_f6_scope(self):
        for unsupported in ("CORE-V2-F7", "CORE-V2-F1-BOGUS"):
            with self.subTest(unsupported=unsupported):
                data = self._traceability_data()
                data["rules"][unsupported] = data["rules"].pop("CORE-V2-F6")
                self._assert_invalid_traceability(data, "rule set mismatch")

    def _traceability_data(self):
        root = Path(__file__).resolve().parents[1]
        return json.loads(
            (root / "config" / "bbma_traceability.json").read_text(encoding="utf-8")
        )

    def _assert_invalid_traceability(self, data, message):
        from tools.bbma_orchestrator.verified import load_verified_traceability

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "traceability.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                load_verified_traceability(
                    path, root / "config" / "bbma_module_graph.json"
                )


class EvidenceTests(unittest.TestCase):
    def test_hash_store_cache_and_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "a.txt"
            file.write_text("abc", encoding="utf-8")
            digest = sha256_file(file)
            store = ContentAddressedStore(root / "cas")
            stored_digest, stored_path = store.put(file)
            self.assertEqual(digest, stored_digest)
            self.assertTrue(stored_path.exists())
            package = build_evidence_package(root / "package.json", [file], metadata={"build": "x"})
            self.assertEqual(package["files"][0]["sha256"], digest)

    def test_evidence_cache_reuse_requires_digest_and_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "a.txt"
            file.write_text("abc", encoding="utf-8")
            with EvidenceDB(root / "evidence.db") as db:
                db.record_artifact(file, reviewed_status="PASS", authority_fingerprint="AUTH1")
                self.assertTrue(db.can_reuse(file, "AUTH1"))
                self.assertFalse(db.can_reuse(file, "AUTH2"))
                file.write_text("changed", encoding="utf-8")
                self.assertFalse(db.can_reuse(file, "AUTH1"))

    def test_evidence_dag_stales_only_descendants(self):
        with tempfile.TemporaryDirectory() as tmp:
            with EvidenceDB(Path(tmp) / "e.db") as db:
                db.add_node("source:a", "source", "1", status="VALID")
                db.add_node("core:a", "core_rule", "2", status="VALID")
                db.add_node("contract:a", "contract", "3", status="VALID")
                db.add_node("unrelated", "artifact", "4", status="VALID")
                db.add_edge("source:a", "core:a")
                db.add_edge("core:a", "contract:a")
                stale = db.mark_changed("source:a", "1b")
                self.assertEqual(stale, ["core:a", "contract:a"])
                self.assertEqual(db.get_node("unrelated")["status"], "VALID")
                self.assertEqual(db.get_node("contract:a")["status"], "STALE")

    def test_evidence_dag_rejects_cycles(self):
        with tempfile.TemporaryDirectory() as tmp:
            with EvidenceDB(Path(tmp) / "e.db") as db:
                db.add_node("a", "artifact", "1")
                db.add_node("b", "artifact", "2")
                db.add_edge("a", "b")
                with self.assertRaises(ValueError):
                    db.add_edge("b", "a")

class TelemetryTests(unittest.TestCase):
    def test_jsonl_failure_first_and_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "events.jsonl"
            rows = [
                {"ts": "1", "event_type": "ENTRY", "JourneyID": "J1", "DecisionID": "D1", "symbol": "EURUSD", "status": "PASS"},
                {"ts": "2", "event_type": "EXIT", "JourneyID": "J1", "DecisionID": "D1", "symbol": "EURUSD", "status": "FAIL", "reason": "x"},
            ]
            source.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            with TelemetryStore(root / "t.db") as store:
                self.assertEqual(store.ingest_jsonl(source, source="test"), 2)
                summary = store.failure_first_summary()
                self.assertEqual(summary["total"], 2)
                self.assertEqual(summary["pass_like"], 1)
                self.assertEqual(summary["failure_like"], 1)
                self.assertEqual(summary["failures"][0]["status"], "FAIL")
                self.assertEqual(len(store.lookup(journey_id="J1")), 2)

    def test_csv_ingest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "events.csv"
            source.write_text("timestamp,event,status,journey_id\n1,A,OK,J1\n", encoding="utf-8")
            with TelemetryStore(root / "t.db") as store:
                self.assertEqual(store.ingest_csv(source), 1)
                self.assertEqual(store.failure_first_summary()["pass_like"], 1)

class TraceTests(unittest.TestCase):
    def test_golden_trace_and_authorized_delta(self):
        baseline = [{"event_type": "A", "state": "CANDIDATE"}]
        same = [{"event_type": "A", "state": "CANDIDATE"}]
        changed = [{"event_type": "A", "state": "CONFIRMED"}]
        self.assertEqual(classify_build_delta(baseline, same)["classification"], "NO_DELTA")
        self.assertEqual(classify_build_delta(baseline, changed)["classification"], "UNEXPECTED_DELTA")
        self.assertEqual(classify_build_delta(baseline, changed, authorized_delta=True)["classification"], "EXPECTED_DELTA")

    def test_shadow_is_read_only_comparison(self):
        result = compare_shadow(
            [{"event_type": "A", "state": "CANDIDATE"}],
            [{"event_type": "A", "state": "CANDIDATE"}],
        )
        self.assertEqual(result.result["classification"], "NO_DELTA")

    def test_lifecycle_valid_path(self):
        model = LifecycleModel()
        for state in ("CANDIDATE", "CONFIRMED", "SELECTED", "VALIDATED", "RISK_APPROVED", "ENTRY_READY", "EXECUTED"):
            model.transition(state)
        self.assertEqual(model.state, "EXECUTED")

    def test_lifecycle_rejects_skip_and_terminal_exit(self):
        model = LifecycleModel()
        model.transition("CANDIDATE")
        with self.assertRaises(ValueError):
            model.transition("SELECTED")
        model.transition("VOID")
        with self.assertRaises(ValueError):
            model.transition("CANDIDATE")

    def test_randomized_property_style_check(self):
        result = randomized_lifecycle_check(seed=7, iterations=300)
        self.assertGreater(result["valid_attempts"], 0)
        self.assertGreater(result["invalid_attempts"], 0)

    def test_mutation_self_test_detects_damaged_transition_table(self):
        self.assertTrue(mutation_self_test())
        self.assertEqual(validate_transition_table(DEFAULT_TRANSITIONS), [])

class NativeAdapterTests(unittest.TestCase):
    def test_native_adapter_is_dry_run_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "native.json"
            config.write_text(
                json.dumps(
                    {
                        "commands": {
                            "probe": {
                                "argv": ["python", "-c", "print('ok')"],
                                "cwd": str(root),
                                "timeout_seconds": 5,
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            adapter = NativeAdapter(config)
            result = adapter.run("probe")
            self.assertEqual(result["status"], "NOT RUN")
            self.assertEqual(result["native_status"], "NOT NATIVE VERIFIED")

    def test_native_adapter_blocks_forbidden_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "native.json"
            config.write_text(
                json.dumps(
                    {
                        "commands": {
                            "unsafe": {
                                "argv": ["echo", "git reset --hard"],
                                "cwd": str(root),
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            adapter = NativeAdapter(config)
            with self.assertRaises(PermissionError):
                adapter.run("unsafe")

    def test_artifact_identity_hashes_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "x.txt"
            file.write_text("x", encoding="utf-8")
            rows = artifact_identity([file, Path(tmp) / "missing"])
            self.assertTrue(rows[0]["exists"])
            self.assertTrue(rows[0]["sha256"])
            self.assertFalse(rows[1]["exists"])

if __name__ == "__main__":
    unittest.main()
