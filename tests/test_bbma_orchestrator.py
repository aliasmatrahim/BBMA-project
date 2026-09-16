from __future__ import annotations

import json
import sys
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

    def test_closeout_requires_closed_pass_and_unique_explicit_candidate(self):
        from tools.bbma_orchestrator.core import build_closeout

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = TaskStore(root / "current")
            manifest = TaskManifest("CURRENT", "R1", "current", "implementation")
            current.save(manifest)
            current.append_event(manifest, "INIT")
            current.checkpoint(manifest, "before-close")
            with self.assertRaisesRegex(ValueError, "CLOSED/PASS"):
                build_closeout(current, [], root / "package.json")

            manifest.transition("PREFLIGHT")
            manifest.transition("IN_PROGRESS")
            manifest.transition("VALIDATION")
            manifest.transition("CLOSED")
            manifest.result = "PASS"
            current.save(manifest)
            current.checkpoint(manifest, "closed")

            candidate = TaskStore(root / "candidate")
            next_manifest = TaskManifest(
                "NEXT", "R1", "next", "implementation",
                latest_verified_step="CURRENT CLOSED/PASS",
            )
            candidate.save(next_manifest)
            package = build_closeout(current, [candidate], root / "package.json")
            self.assertEqual(package["next_task_id"], "NEXT")
            self.assertIn("ACTIVE_TASK.json", package["files"][0]["path"])
            self.assertIn("Task: CURRENT", package["handoff"])

    def test_closeout_rejects_noneligible_candidates_and_missing_artifacts(self):
        from tools.bbma_orchestrator.core import build_closeout

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = TaskStore(root / "current")
            manifest = TaskManifest("CURRENT", "R1", "current", "implementation")
            for phase in ("PREFLIGHT", "IN_PROGRESS", "VALIDATION", "CLOSED"):
                manifest.transition(phase)
            manifest.result = "PASS"
            current.save(manifest)
            current.append_event(manifest, "CLOSED")
            current.checkpoint(manifest, "closed")

            def candidate(name, result="NOT VERIFIED"):
                store = TaskStore(root / name)
                state = TaskManifest(
                    name, "R1", name, "implementation",
                    result=result,
                    latest_verified_step="CURRENT CLOSED/PASS",
                )
                store.save(state)
                return store

            with self.assertRaisesRegex(ValueError, "exactly one"):
                build_closeout(current, [], root / "zero.json")
            with self.assertRaisesRegex(ValueError, "exactly one"):
                build_closeout(
                    current, [candidate("ONE"), candidate("TWO")], root / "two.json"
                )
            with self.assertRaisesRegex(ValueError, "exactly one"):
                build_closeout(current, [candidate("HOLD", "HOLD")], root / "hold.json")

            current.events_path.unlink()
            with self.assertRaises(FileNotFoundError):
                build_closeout(current, [candidate("NEXT")], root / "missing.json")

    def test_closeout_rejects_self_successor_and_unverified_lineage(self):
        from tools.bbma_orchestrator.core import build_closeout

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = TaskStore(root / "current")
            manifest = TaskManifest("CURRENT", "R1", "current", "implementation")
            for phase in ("PREFLIGHT", "IN_PROGRESS", "VALIDATION", "CLOSED"):
                manifest.transition(phase)
            manifest.result = "PASS"
            current.save(manifest)
            current.append_event(manifest, "CLOSED")
            current.checkpoint(manifest, "closed")

            self_store = TaskStore(root / "self")
            self_store.save(TaskManifest(
                "CURRENT", "R2", "self", "implementation",
                latest_verified_step="CURRENT CLOSED/PASS",
            ))
            with self.assertRaisesRegex(ValueError, "exactly one"):
                build_closeout(current, [self_store], root / "self.json")

            stale_lineage = TaskStore(root / "stale-lineage")
            stale_lineage.save(TaskManifest(
                "NEXT", "R2", "next", "implementation",
                latest_verified_step="CURRENT NOT VERIFIED",
            ))
            with self.assertRaisesRegex(ValueError, "exactly one"):
                build_closeout(current, [stale_lineage], root / "stale.json")

    def test_closeout_selects_latest_checkpoint_by_timestamp_not_label(self):
        from tools.bbma_orchestrator.core import atomic_write_json, build_closeout

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = TaskStore(root / "current")
            manifest = TaskManifest("CURRENT", "R1", "current", "implementation")
            for phase in ("PREFLIGHT", "IN_PROGRESS", "VALIDATION", "CLOSED"):
                manifest.transition(phase)
            manifest.result = "PASS"
            current.save(manifest)
            current.append_event(manifest, "CLOSED")
            current.checkpoints_dir.mkdir(parents=True, exist_ok=True)
            old_path = current.checkpoints_dir / "CURRENT_z-old_20260101T000000Z.json"
            new_path = current.checkpoints_dir / "CURRENT_a-new_20260102T000000Z.json"
            atomic_write_json(old_path, manifest.to_dict())
            atomic_write_json(new_path, manifest.to_dict())

            candidate = TaskStore(root / "candidate")
            next_manifest = TaskManifest(
                "NEXT", "R1", "next", "implementation",
                latest_verified_step="CURRENT CLOSED/PASS",
            )
            candidate.save(next_manifest)

            package = build_closeout(current, [candidate], root / "package.json")
            packaged_paths = {item["path"] for item in package["files"]}
            self.assertIn(str(new_path), packaged_paths)
            self.assertNotIn(str(old_path), packaged_paths)

    def test_closeout_requires_closed_pass_checkpoint_snapshot(self):
        from tools.bbma_orchestrator.core import atomic_write_json, build_closeout

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            current = TaskStore(root / "current")
            stale = TaskManifest("CURRENT", "R1", "current", "implementation")
            current.save(stale)
            current.append_event(stale, "INIT")
            current.checkpoints_dir.mkdir(parents=True, exist_ok=True)
            atomic_write_json(
                current.checkpoints_dir / "CURRENT_stale_20260101T000000Z.json",
                stale.to_dict(),
            )
            for phase in ("PREFLIGHT", "IN_PROGRESS", "VALIDATION", "CLOSED"):
                stale.transition(phase)
            stale.result = "PASS"
            current.save(stale)

            candidate = TaskStore(root / "candidate")
            next_manifest = TaskManifest(
                "NEXT", "R1", "next", "implementation",
                latest_verified_step="CURRENT CLOSED/PASS",
            )
            candidate.save(next_manifest)

            with self.assertRaisesRegex(ValueError, "CLOSED/PASS checkpoint"):
                build_closeout(current, [candidate], root / "package.json")

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

    def test_regression_selector_walks_all_cited_consumers(self):
        selector = RegressionSelector(
            {
                "M06": {"tests": ["t06"], "consumers": ["M08"]},
                "M08": {"tests": ["t08"], "consumers": ["M13"]},
                "M13": {"tests": ["t13"], "consumers": []},
            }
        )
        self.assertEqual(selector.select(["M06"]), ["t06", "t08", "t13"])

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


class ArchitectureInvariantTests(unittest.TestCase):
    @staticmethod
    def _paths():
        root = Path(__file__).resolve().parents[1]
        return (
            root / "config" / "bbma_architecture_invariants.json",
            root / "config" / "bbma_module_graph.json",
        )

    def test_catalog_binds_exact_contract_cited_ownership_boundaries(self):
        from tools.bbma_orchestrator.verified import (
            load_verified_architecture_invariants,
        )

        catalog_path, graph_path = self._paths()
        catalog = load_verified_architecture_invariants(
            catalog_path, graph_path
        )
        expected_modules = {
            "M12N", "M13", "M14", "M15", "M18", "M19", "M22", "M27",
        }
        self.assertEqual(
            {item["module"] for item in catalog["invariants"].values()},
            expected_modules,
        )
        self.assertEqual(
            catalog["coverage"]["runtime_enforcement"], "NOT VERIFIED"
        )
        for item in catalog["invariants"].values():
            self.assertTrue(any(ref != "EA_HEADERS" for ref in item["evidence"]))

    def test_catalog_rejects_scope_deletion_addition_or_substitution(self):
        from tools.bbma_orchestrator.verified import (
            validate_architecture_invariants,
        )

        catalog_path, graph_path = self._paths()
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        original = json.loads(catalog_path.read_text(encoding="utf-8"))

        deleted = json.loads(json.dumps(original))
        removed_id = next(iter(deleted["invariants"]))
        del deleted["invariants"][removed_id]

        added = json.loads(json.dumps(original))
        added["invariants"]["ARCH-M06-UNAPPROVED"] = {
            "module": "M06",
            "ownership": graph["modules"]["M06"]["ownership"],
            "evidence": graph["modules"]["M06"]["evidence"],
        }

        substituted = json.loads(json.dumps(added))
        del substituted["invariants"][removed_id]

        for label, catalog in (
            ("deleted", deleted),
            ("added", added),
            ("substituted", substituted),
        ):
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    ValueError, "approved architecture invariant module set"
                ):
                    validate_architecture_invariants(catalog, graph)

    def test_catalog_rejects_non_contract_evidence_path(self):
        from tools.bbma_orchestrator.verified import (
            validate_architecture_invariants,
        )

        catalog_path, graph_path = self._paths()
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        graph["evidence_catalog"]["C_M12N"]["path"] = (
            "docs/M12N_NESTED_MTF_JOURNEY_ENGINE_CONTRACT.md"
        )
        with self.assertRaisesRegex(ValueError, "standalone contract evidence"):
            validate_architecture_invariants(catalog, graph)

    def test_catalog_rejects_ownership_or_evidence_drift(self):
        from tools.bbma_orchestrator.verified import (
            load_verified_architecture_invariants,
            validate_architecture_invariants,
        )

        catalog_path, graph_path = self._paths()
        catalog = load_verified_architecture_invariants(
            catalog_path, graph_path
        )
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        module = next(iter(catalog["invariants"].values()))["module"]
        graph["modules"][module]["ownership"] += " MUTATED"
        with self.assertRaisesRegex(ValueError, "ownership mismatch"):
            validate_architecture_invariants(catalog, graph)

        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        first = next(iter(catalog["invariants"].values()))
        first["evidence"] = ["EA_HEADERS"]
        with self.assertRaisesRegex(ValueError, "evidence mismatch"):
            validate_architecture_invariants(catalog, graph)

    def test_catalog_rejects_false_runtime_verification(self):
        from tools.bbma_orchestrator.verified import (
            validate_architecture_invariants,
        )

        catalog_path, graph_path = self._paths()
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        catalog["coverage"]["runtime_enforcement"] = "VERIFIED"
        with self.assertRaisesRegex(ValueError, "runtime enforcement"):
            validate_architecture_invariants(catalog, graph)

    def test_exhaustive_mutation_check_detects_every_boundary(self):
        from tools.bbma_orchestrator.verified import (
            architecture_invariant_mutation_check,
        )

        catalog_path, graph_path = self._paths()
        result = architecture_invariant_mutation_check(
            catalog_path, graph_path
        )
        self.assertEqual(result["mutations"], 8)
        self.assertEqual(result["detected"], result["mutations"])

    def test_architecture_invariant_cli_reports_runtime_boundary(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        catalog_path, graph_path = self._paths()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main([
                "architecture-invariants",
                "--catalog", str(catalog_path),
                "--module-graph", str(graph_path),
            ])
        result = json.loads(output.getvalue())
        self.assertEqual(result["invariants"], 8)
        self.assertEqual(result["detected_mutations"], 8)
        self.assertEqual(result["runtime_enforcement"], "NOT VERIFIED")


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


class VerifiedRegressionMapTests(unittest.TestCase):
    def test_regression_map_matches_accepted_graph_and_verified_trace_tests(self):
        from tools.bbma_orchestrator.verified import load_verified_regression_map

        root = Path(__file__).resolve().parents[1]
        mapping = load_verified_regression_map(
            root / "config" / "bbma_regression_map.json",
            root / "config" / "bbma_module_graph.json",
            root / "config" / "bbma_traceability.json",
        )
        expected_modules = {f"M{i:02d}" for i in range(1, 28)} | {"M12N"}
        self.assertEqual(set(mapping["modules"]), expected_modules)
        self.assertEqual(
            sum(len(item["consumers"]) for item in mapping["modules"].values()),
            38,
        )
        self.assertEqual(
            set(mapping["tests"]),
            {
                "TEST_DRIVER_F1",
                "TEST_DRIVER_F2",
                "TEST_DRIVER_F3",
                "TEST_DRIVER_F5",
                "TEST_DRIVER_F6",
            },
        )
        self.assertEqual(mapping["mandatory_global"], [])
        self.assertEqual(
            mapping["modules"]["M12"]["tests"],
            ["TEST_DRIVER_F3", "TEST_DRIVER_F6"],
        )
        for module_id in ("M11", "M15", "M16"):
            self.assertEqual(mapping["modules"][module_id]["tests"], [])

    def test_verified_selector_uses_transitive_cited_blast_radius(self):
        from tools.bbma_orchestrator.verified import load_verified_regression_map

        root = Path(__file__).resolve().parents[1]
        mapping = load_verified_regression_map(
            root / "config" / "bbma_regression_map.json",
            root / "config" / "bbma_module_graph.json",
            root / "config" / "bbma_traceability.json",
        )
        selector = RegressionSelector(
            mapping["modules"], mapping["mandatory_global"], strict=True
        )
        self.assertEqual(
            selector.select(["M06"]),
            ["TEST_DRIVER_F2", "TEST_DRIVER_F3", "TEST_DRIVER_F6", "TEST_DRIVER_F1"],
        )
        self.assertEqual(selector.select(["M07"]), ["TEST_DRIVER_F5"])
        with self.assertRaisesRegex(ValueError, "unknown changed modules"):
            selector.select(["UNKNOWN"])
        self.assertEqual(
            set(selector.select([], release_candidate=True)),
            set(mapping["tests"]),
        )

    def test_verified_regression_map_cli_selects_transitive_tests(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        root = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = main([
                "select-tests",
                "--map", str(root / "config" / "bbma_regression_map.json"),
                "--module-graph", str(root / "config" / "bbma_module_graph.json"),
                "--traceability", str(root / "config" / "bbma_traceability.json"),
                "--module", "M06",
            ])
        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(output.getvalue())["selected"],
            ["TEST_DRIVER_F2", "TEST_DRIVER_F3", "TEST_DRIVER_F6", "TEST_DRIVER_F1"],
        )

    def test_verified_regression_map_cli_cannot_bypass_authority_validation(self):
        from tools.bbma_orchestrator.cli import main

        root = Path(__file__).resolve().parents[1]
        with self.assertRaisesRegex(ValueError, "verified regression map requires"):
            main([
                "select-tests",
                "--map", str(root / "config" / "bbma_regression_map.json"),
                "--module", "M06",
            ])

    def test_verified_regression_map_cli_rejects_unknown_module(self):
        from tools.bbma_orchestrator.cli import main

        root = Path(__file__).resolve().parents[1]
        with self.assertRaisesRegex(ValueError, "unknown changed modules"):
            main([
                "select-tests",
                "--map", str(root / "config" / "bbma_regression_map.json"),
                "--module-graph", str(root / "config" / "bbma_module_graph.json"),
                "--traceability", str(root / "config" / "bbma_traceability.json"),
                "--module", "UNKNOWN",
            ])

    def test_verified_regression_map_cli_requires_both_authorities(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        root = Path(__file__).resolve().parents[1]
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            with self.assertRaises(SystemExit) as raised:
                main([
                    "select-tests",
                    "--map", str(root / "config" / "bbma_regression_map.json"),
                    "--module-graph", str(root / "config" / "bbma_module_graph.json"),
                    "--module", "M06",
                ])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--module-graph and --traceability must be supplied together", error.getvalue())

    def test_regression_map_rejects_consumer_drift(self):
        data = self._regression_data()
        data["modules"]["M06"]["consumers"].append("M13")
        self._assert_invalid_regression(data, "consumer set mismatch")

    def test_regression_map_rejects_uncited_test_assignment(self):
        data = self._regression_data()
        data["modules"]["M11"]["tests"].append("TEST_DRIVER_F1")
        self._assert_invalid_regression(data, "assignment mismatch")

    def test_regression_map_rejects_invented_mandatory_global(self):
        data = self._regression_data()
        data["mandatory_global"] = ["TEST_DRIVER_F1"]
        self._assert_invalid_regression(data, "mandatory global regression")

    def _regression_data(self):
        root = Path(__file__).resolve().parents[1]
        return json.loads(
            (root / "config" / "bbma_regression_map.json").read_text(encoding="utf-8")
        )

    def _assert_invalid_regression(self, data, message):
        from tools.bbma_orchestrator.verified import load_verified_regression_map

        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "regression.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                load_verified_regression_map(
                    path,
                    root / "config" / "bbma_module_graph.json",
                    root / "config" / "bbma_traceability.json",
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

    def test_mt4_log_ingest_is_attributable_idempotent_and_never_implies_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "20260910.log"
            journey = "EURUSD|H4_OWNER|240|SIGNAL_ECSD|B|1788768000"
            decision_token = "EURUSD|2026.09.10~03:00|1|7|ABC"
            decision_id = decision_token.replace("~", " ")
            rows = [
                f"0\\t10:29:27.700\\tEA_BUILD GBPUSD,M15: [N1-NMJE] EURUSD REL=ALIGNED SUB=NONE MAT=CONFIRMED P=H4_OWNER/B PRETAIN=Y PSEL=CANONICAL PHASE=CONFIRMED PDUR=Y PE=ABC J={journey} D1=- H4=B H1=B M15=B R=OK",
                f"0\\t10:29:27.800\\tEA_BUILD GBPUSD,M15: [N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=ALIGNED P=H4_OWNER/B PE=ABC J={journey} DID={decision_token} DIDH=ABC AUTH=STRAT OFAM=NONE OC= LTF=- OSH=ABC",
                f"0\\t10:29:27.900\\tEA_BUILD GBPUSD,M15: [N2-NMJE-OUT] PAIR=EURUSD TICKET=123 DID={decision_token} DIDH=ABC NET=-1.25 CLOSE=1789000000 REC=REC_NORMAL",
            ]
            source.write_text("\n".join(rows) + "\n", encoding="utf-8")
            with TelemetryStore(root / "t.db") as store:
                self.assertEqual(store.ingest_mt4_log(source, source="g40-fixture", source_kind="mt4-expert"), 3)
                self.assertEqual(store.ingest_mt4_log(source, source="g40-fixture", source_kind="mt4-expert"), 0)
                journey_rows = store.lookup(journey_id=journey)
                self.assertEqual(len(journey_rows), 2)
                self.assertEqual(journey_rows[0]["payload"]["fields"]["sub"], "NONE")
                decision_rows = store.lookup(decision_id=decision_id)
                self.assertEqual([row["event_type"] for row in decision_rows], ["N2_NMJE_DECISION", "N2_NMJE_OUTCOME"])
                self.assertEqual(decision_rows[0]["payload"]["fields"]["parent_event"], "ABC")
                self.assertEqual(decision_rows[0]["payload"]["fields"]["opportunity_cycle"], "")
                self.assertEqual(decision_rows[0]["payload"]["source_sha256"], sha256_file(source))
                self.assertEqual(decision_rows[0]["payload"]["runtime_verification"], "NOT VERIFIED")
                summary = store.failure_first_summary()
                self.assertEqual(summary["total"], 3)
                self.assertEqual(summary["pass_like"], 0)
                self.assertEqual(summary["failure_like"], 0)

    def test_mt4_log_ingest_fails_closed_before_partial_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "20260910.log"
            source.write_text(
                "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4_OWNER/B J=J1 D1=- H4=B H1=B M15=B R=OK\n"
                "0\\t10:00:01.000\\tEA: [N2-NMJE-OUT] PAIR=EURUSD TICKET=123 DID=broken\n",
                encoding="utf-8",
            )
            with TelemetryStore(root / "t.db") as store:
                with self.assertRaisesRegex(ValueError, "line 2: malformed.*N2-NMJE-OUT"):
                    store.ingest_mt4_log(source, source_kind="strategy-tester")
                self.assertEqual(store.failure_first_summary()["total"], 0)

    def test_mt4_log_ingest_rolls_back_on_injected_publish_fault(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "20260910.log"
            row = (
                "0\t10:29:27.700\tEA_BUILD GBPUSD,M15: [N1-NMJE] EURUSD "
                "REL=ALIGNED SUB=NONE MAT=CONFIRMED P=H4_OWNER/B PRETAIN=Y "
                "PSEL=CANONICAL PHASE=CONFIRMED PDUR=Y PE=ABC "
                "J=EURUSD|H4_OWNER|240|SIGNAL_ECSD|B|1788768000 D1=- "
                "H4=B H1=B M15=B R=OK"
            )
            source.write_text((row + "\n") * 2, encoding="utf-8")
            with TelemetryStore(root / "t.db") as store:
                original = store.ingest_event
                calls = {"count": 0}

                def injected(payload, **kwargs):
                    calls["count"] += 1
                    if calls["count"] == 2:
                        raise RuntimeError("injected publish fault")
                    return original(payload, **kwargs)

                store.ingest_event = injected
                with self.assertRaisesRegex(RuntimeError, "injected publish fault"):
                    store.ingest_mt4_log(source, source_kind="mt4-expert")
                self.assertEqual(store.failure_first_summary()["total"], 0)

    def test_mt4_log_ingest_rejects_file_changed_during_read(self):
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "20260910.log"
            source.write_text(
                "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4_OWNER/B J=J1 D1=- H4=B H1=B M15=B R=OK\n",
                encoding="utf-8",
            )
            with TelemetryStore(root / "t.db") as store:
                with patch(
                    "tools.bbma_orchestrator.telemetry._sha256_file",
                    side_effect=["a" * 64, "b" * 64],
                ):
                    with self.assertRaisesRegex(ValueError, "changed during ingestion"):
                        store.ingest_mt4_log(source, source_kind="runtime-smoke")
                self.assertEqual(store.failure_first_summary()["total"], 0)

    def test_mt4_log_ingest_captures_append_only_current_n2_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "20260910.log"
            source.write_text(
                "0\\t10:00:00.000\\tEA: [N2-NMJE-DEC] EURUSD SIG=RE DIR=B REL=ALIGNED P=H4/B J=J1 DID=D1 DIDH=H1 AUTH=OPP OFAM=CSD OC=CYCLE1 PE=ABC LTF=H1 OSH=SEQ1\n",
                encoding="utf-8",
            )
            with TelemetryStore(root / "t.db") as store:
                self.assertEqual(store.ingest_mt4_log(source, source_kind="mt4-expert"), 1)
                row = store.lookup(decision_id="D1")[0]
                self.assertEqual(row["payload"]["fields"]["parent_event"], "ABC")
                self.assertEqual(row["payload"]["fields"]["ltf_cluster"], "H1")
                self.assertEqual(row["payload"]["fields"]["opportunity_sequence_hash"], "SEQ1")

    def test_mt4_log_ingest_rejects_ambiguous_or_unparsed_tokens(self):
        invalid_rows = [
            "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4/B J=J1 D1=- H4=B H1=B M15=B R=OK BROKEN=",
            "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4/B J=J1 D1=- H4=B H1=B M15=B R=OK [N2-NMJE-OUT] BROKEN",
            "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4/B J=J1 J=J2 D1=- H4=B H1=B M15=B R=OK",
        ]
        for raw_line in invalid_rows:
            with self.subTest(raw_line=raw_line), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = root / "20260910.log"
                source.write_text(raw_line + "\n", encoding="utf-8")
                with TelemetryStore(root / "t.db") as store:
                    with self.assertRaisesRegex(ValueError, "line 1: malformed"):
                        store.ingest_mt4_log(source, source_kind="mt4-expert")
                    self.assertEqual(store.failure_first_summary()["total"], 0)

    def test_mt4_log_ingest_requires_current_identity_fields(self):
        invalid_rows = [
            "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED SUB=NONE MAT=CONFIRMED P=H4/B PRETAIN=Y PSEL=CANONICAL PHASE=CONFIRMED PDUR=Y J=J1 D1=- H4=B H1=B M15=B R=OK",
            "0\\t10:00:00.000\\tEA: [N2-NMJE-DEC] EURUSD SIG=RE DIR=B REL=ALIGNED P=H4/B PE=ABC J=J1 DID=D1 AUTH=OPP OFAM=CSD OC=CYCLE1 LTF=H1",
        ]
        for raw_line in invalid_rows:
            with self.subTest(raw_line=raw_line), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = root / "20260910.log"
                source.write_text(raw_line + "\n", encoding="utf-8")
                with TelemetryStore(root / "t.db") as store:
                    with self.assertRaisesRegex(ValueError, "line 1: malformed"):
                        store.ingest_mt4_log(source, source_kind="mt4-expert")
                    self.assertEqual(store.failure_first_summary()["total"], 0)

    def test_mt4_log_ingest_rejects_invalid_utf8_without_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "20260910.log"
            source.write_bytes(
                b"0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4/B J=J1 D1=- H4=B H1=B M15=B R=OK"
                + bytes([255]) + b"\n"
            )
            with TelemetryStore(root / "t.db") as store:
                with self.assertRaises(UnicodeDecodeError):
                    store.ingest_mt4_log(source, source_kind="mt4-expert")
                self.assertEqual(store.failure_first_summary()["total"], 0)

    def test_mt4_log_cli_ingests_with_explicit_source_kind(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "tester.log"
            source.write_text(
                "0\\t10:00:00.000\\tEA: [N1-NMJE] EURUSD REL=ALIGNED P=H4_OWNER/B J=J1 D1=- H4=B H1=B M15=B R=OK\n",
                encoding="utf-8",
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                main([
                    "ingest-mt4-log", "--db", str(root / "t.db"),
                    "--path", str(source), "--source-kind", "strategy-tester",
                    "--source", "fixture",
                ])
            result = json.loads(output.getvalue())
            self.assertEqual(result["ingested"], 1)
            self.assertEqual(result["summary"]["pass_like"], 0)

class AttributableTraceTests(unittest.TestCase):
    @staticmethod
    def _payload(source_sha256, emitter, *, line=1, direction="B"):
        event_key = ("1" if source_sha256.startswith("a") else "2") * 64
        return {
            "event_type": "N2_NMJE_DECISION",
            "journey_id": "J1",
            "decision_id": "D1",
            "symbol": "EURUSD",
            "status": "OBSERVED",
            "source_sha256": source_sha256,
            "source_path": "C:\\fixture\\tester.log",
            "source_kind": "strategy-tester",
            "source_line": line,
            "event_key": event_key,
            "emitter": emitter,
            "runtime_verification": "NOT VERIFIED",
            "fields": {
                "pair": "EURUSD",
                "journey": "J1",
                "decision_id": "D1",
                "direction": direction,
                "decision_hash": "H1",
            },
        }

    def _artifact(self, source_sha256, emitter, *, role, direction="B",
                  authority_ref=""):
        from tools.bbma_orchestrator.trace import build_trace_artifact

        with tempfile.TemporaryDirectory() as tmp:
            with TelemetryStore(Path(tmp) / "t.db") as store:
                payload = self._payload(
                    source_sha256, emitter, direction=direction
                )
                store.ingest_event(payload, event_key=payload["event_key"])
                rows = store.attributable_events(
                    source_sha256=source_sha256, emitter=emitter
                )
                return build_trace_artifact(
                    rows,
                    source_sha256=source_sha256,
                    emitter=emitter,
                    role=role,
                    authority_ref=authority_ref,
                )

    def test_attributable_events_require_exact_source_and_emitter(self):
        source_sha256 = "a" * 64
        with tempfile.TemporaryDirectory() as tmp:
            with TelemetryStore(Path(tmp) / "t.db") as store:
                payload = self._payload(source_sha256, "BUILD1")
                store.ingest_event(payload, event_key=payload["event_key"])
                rows = store.attributable_events(
                    source_sha256=source_sha256, emitter="BUILD1"
                )
                self.assertEqual(len(rows), 1)
                with self.assertRaisesRegex(ValueError, "no attributable events"):
                    store.attributable_events(
                        source_sha256=source_sha256, emitter="BUILD2"
                    )

    def test_trace_artifact_is_deterministic_attributable_and_not_runtime_pass(self):
        artifact = self._artifact("a" * 64, "BUILD1", role="candidate")
        self.assertEqual(artifact["record_count"], 1)
        self.assertEqual(artifact["source_sha256"], "a" * 64)
        self.assertEqual(artifact["emitter"], "BUILD1")
        self.assertEqual(artifact["runtime_verification"], "NOT VERIFIED")
        self.assertEqual(artifact["records"][0]["provenance"]["source_line"], 1)
        self.assertEqual(len(artifact["trace_sha256"]), 64)
        self.assertEqual(
            artifact,
            self._artifact("a" * 64, "BUILD1", role="candidate"),
        )

    def test_trace_artifact_rejects_column_payload_identity_mismatch(self):
        from tools.bbma_orchestrator.trace import build_trace_artifact

        source_sha256 = "a" * 64
        with tempfile.TemporaryDirectory() as tmp:
            with TelemetryStore(Path(tmp) / "t.db") as store:
                payload = self._payload(source_sha256, "BUILD1")
                store.ingest_event(payload, event_key=payload["event_key"])
                rows = store.attributable_events(
                    source_sha256=source_sha256, emitter="BUILD1"
                )
                rows[0]["decision_id"] = "D2"
                with self.assertRaisesRegex(ValueError, "row/payload mismatch"):
                    build_trace_artifact(
                        rows,
                        source_sha256=source_sha256,
                        emitter="BUILD1",
                    )

    def test_golden_role_requires_external_authority_reference(self):
        with self.assertRaisesRegex(ValueError, "authority_ref"):
            self._artifact("a" * 64, "BUILD1", role="golden")

    def test_artifact_delta_requires_authorization_reference(self):
        from tools.bbma_orchestrator.trace import compare_trace_artifacts

        baseline = self._artifact(
            "a" * 64, "BUILD1", role="golden",
            authority_ref="evidence:approved-baseline",
        )
        same = self._artifact("b" * 64, "BUILD2", role="candidate")
        self.assertEqual(
            compare_trace_artifacts(baseline, same)["classification"],
            "NO_DELTA",
        )
        changed = self._artifact(
            "b" * 64, "BUILD2", role="candidate", direction="S"
        )
        self.assertEqual(
            compare_trace_artifacts(baseline, changed)["classification"],
            "UNEXPECTED_DELTA",
        )
        result = compare_trace_artifacts(
            baseline, changed, authorization_ref="decision:approved-delta"
        )
        self.assertEqual(result["classification"], "EXPECTED_DELTA")
        self.assertEqual(result["authorization_ref"], "decision:approved-delta")

    def test_trace_artifact_tampering_fails_closed(self):
        from tools.bbma_orchestrator.trace import compare_trace_artifacts

        baseline = self._artifact(
            "a" * 64, "BUILD1", role="golden",
            authority_ref="evidence:approved-baseline",
        )
        candidate = self._artifact("b" * 64, "BUILD2", role="candidate")
        candidate["records"][0]["fields"]["direction"] = "S"
        with self.assertRaisesRegex(ValueError, "trace hash mismatch"):
            compare_trace_artifacts(baseline, candidate)

    def test_trace_artifact_rejects_self_hashed_invalid_metadata(self):
        from tools.bbma_orchestrator.trace import (
            _canonical_digest,
            validate_trace_artifact,
        )

        artifact = self._artifact("a" * 64, "BUILD1", role="candidate")
        invalid_values = {
            "authority_ref": 7,
            "source_path": 7,
            "source_kind": "",
            "runtime_verification": "",
        }
        for field, value in invalid_values.items():
            with self.subTest(field=field):
                damaged = json.loads(json.dumps(artifact))
                damaged[field] = value
                body = dict(damaged)
                del body["trace_sha256"]
                damaged["trace_sha256"] = _canonical_digest(body)
                with self.assertRaisesRegex(
                    ValueError, f"invalid trace {field}"
                ):
                    validate_trace_artifact(damaged)

    def test_trace_artifact_cli_export_and_diff(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db_path = root / "t.db"
            source_sha256 = "b" * 64
            with TelemetryStore(db_path) as store:
                payload = self._payload(source_sha256, "BUILD2")
                store.ingest_event(payload, event_key=payload["event_key"])
            candidate_path = root / "candidate.json"
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                main([
                    "trace-export-telemetry",
                    "--db", str(db_path),
                    "--source-sha256", source_sha256,
                    "--emitter", "BUILD2",
                    "--output", str(candidate_path),
                ])
            export_result = json.loads(stdout.getvalue())
            self.assertEqual(export_result["record_count"], 1)
            self.assertEqual(export_result["role"], "candidate")

            baseline_path = root / "baseline.json"
            baseline_path.write_text(
                json.dumps(self._artifact(
                    "a" * 64, "BUILD1", role="golden",
                    authority_ref="evidence:approved-baseline",
                )),
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                main([
                    "trace-diff-artifacts",
                    "--baseline", str(baseline_path),
                    "--candidate", str(candidate_path),
                ])
            self.assertEqual(
                json.loads(stdout.getvalue())["classification"],
                "NO_DELTA",
            )

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

    def test_native_adapter_rejects_disabled_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "runtime": {
                        "argv": [sys.executable, "-c", "print('must not run')"],
                        "cwd": str(root),
                        "enabled": False,
                        "blocked_reason": "MT4 launch is not authorized",
                    }
                }
            }), encoding="utf-8")
            adapter = NativeAdapter(config)
            with self.assertRaisesRegex(PermissionError, "MT4 launch is not authorized"):
                adapter.run("runtime")

    def test_native_adapter_rejects_input_identity_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "candidate.mq4"
            source.write_text("candidate", encoding="utf-8")
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "compile": {
                        "argv": [sys.executable, "-c", "print('must not run')"],
                        "cwd": str(root),
                        "expected_inputs": [
                            {"path": str(source), "sha256": "0" * 64}
                        ],
                    }
                }
            }), encoding="utf-8")
            adapter = NativeAdapter(config)
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                adapter.run("compile")

    def test_native_adapter_rejects_duplicate_process_before_execute(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "compile": {
                        "argv": [sys.executable, "-c", "print('must not run')"],
                        "cwd": str(root),
                        "exclusive_process_names": ["metaeditor.exe"],
                    }
                }
            }), encoding="utf-8")
            adapter = NativeAdapter(
                config, process_names_provider=lambda: {"metaeditor.exe"}
            )
            with self.assertRaisesRegex(RuntimeError, "matching process already active"):
                adapter.run("compile", execute=True)

    def test_native_adapter_verifies_metaeditor_result_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "candidate.mq4"
            log = root / "compile.log"
            ex4 = root / "candidate.ex4"
            source.write_text("candidate", encoding="utf-8")
            script = (
                "from pathlib import Path;"
                "Path('compile.log').write_text('Result: 0 errors, 0 warnings', encoding='utf-16');"
                "Path('candidate.ex4').write_bytes(b'ex4');"
                "raise SystemExit(1)"
            )
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "compile": {
                        "argv": [sys.executable, "-c", script],
                        "cwd": str(root),
                        "expected_inputs": [
                            {"path": str(source), "sha256": sha256_file(source)}
                        ],
                        "result_contract": {
                            "kind": "metaeditor_0e0w",
                            "log_path": str(log),
                            "artifacts": [str(ex4)],
                        },
                    }
                }
            }), encoding="utf-8")
            adapter = NativeAdapter(config, process_names_provider=lambda: set())
            result = adapter.run("compile", execute=True)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["returncode"], 1)
            self.assertEqual(result["metaeditor_errors"], 0)
            self.assertEqual(result["metaeditor_warnings"], 0)
            self.assertTrue(result["artifacts"][0]["sha256"])

    def test_native_adapter_fails_nonzero_metaeditor_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "compile.log"
            ex4 = root / "candidate.ex4"
            script = (
                "from pathlib import Path;"
                "Path('compile.log').write_text('Result: 1 error, 0 warnings', encoding='utf-16');"
                "Path('candidate.ex4').write_bytes(b'ex4')"
            )
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "compile": {
                        "argv": [sys.executable, "-c", script],
                        "cwd": str(root),
                        "result_contract": {
                            "kind": "metaeditor_0e0w",
                            "log_path": str(log),
                            "artifacts": [str(ex4)],
                        },
                    }
                }
            }), encoding="utf-8")
            adapter = NativeAdapter(config, process_names_provider=lambda: set())
            result = adapter.run("compile", execute=True)
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("not 0E0W", result["verification_error"])

    def test_native_adapter_rejects_stale_metaeditor_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "compile.log"
            ex4 = root / "candidate.ex4"
            log.write_text("Result: 0 errors, 0 warnings", encoding="utf-16")
            ex4.write_bytes(b"old-ex4")
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "compile": {
                        "argv": [sys.executable, "-c", "raise SystemExit(1)"],
                        "cwd": str(root),
                        "result_contract": {
                            "kind": "metaeditor_0e0w",
                            "log_path": str(log),
                            "artifacts": [str(ex4)],
                        },
                    }
                }
            }), encoding="utf-8")
            adapter = NativeAdapter(config, process_names_provider=lambda: set())
            result = adapter.run("compile", execute=True)
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("not refreshed", result["verification_error"])

    def test_native_run_cli_exits_nonzero_for_failed_execution(self):
        import contextlib
        import io
        from tools.bbma_orchestrator.cli import main

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "native.json"
            config.write_text(json.dumps({
                "commands": {
                    "fail": {
                        "argv": [sys.executable, "-c", "raise SystemExit(2)"],
                        "cwd": str(root),
                    }
                }
            }), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with self.assertRaises(SystemExit) as raised:
                    main([
                        "native-run", "--config", str(config),
                        "--name", "fail", "--execute",
                    ])
            self.assertEqual(raised.exception.code, 1)
            self.assertEqual(json.loads(output.getvalue())["status"], "FAIL")

    def test_artifact_identity_hashes_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "x.txt"
            file.write_text("x", encoding="utf-8")
            rows = artifact_identity([file, Path(tmp) / "missing"])
            self.assertTrue(rows[0]["exists"])
            self.assertTrue(rows[0]["sha256"])
            self.assertFalse(rows[1]["exists"])


class SourceDiscoveryTests(unittest.TestCase):
    def test_discover_paths_is_bounded_sorted_and_patterned(self):
        from tools.bbma_orchestrator.source_discovery import discover_paths
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "z.pdf").write_text("z", encoding="utf-8")
            (root / "a.pdf").write_text("a", encoding="utf-8")
            (root / "note.txt").write_text("n", encoding="utf-8")
            self.assertEqual(
                discover_paths([root], patterns=("*.pdf",)),
                [root / "a.pdf", root / "z.pdf"],
            )

    def test_artifact_role_explicit_and_filename_classification_are_separate(self):
        from tools.bbma_orchestrator.source_discovery import classify_artifact_role
        self.assertEqual(classify_artifact_role(Path("raw.pdf"), "RAW"), "RAW")
        self.assertEqual(classify_artifact_role(Path("corrected_transcript.txt"), ""), "CORRECTED")
        self.assertEqual(classify_artifact_role(Path("derived_summary.md"), ""), "DERIVED")
        self.assertEqual(classify_artifact_role(Path("unknown.bin"), ""), "UNKNOWN")

    def test_unknown_provenance_stays_unverified_without_phase_promotion(self):
        from tools.bbma_orchestrator.source_discovery import record_provenance
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            with SourceRegistry(Path(tmp) / "sources.db") as registry:
                registry.register_discovered("SRC-1", "file:///a.pdf")
                unknown = record_provenance(registry, "SRC-1", "", "", ())
                self.assertEqual(unknown.provenance, "UNVERIFIED")
                self.assertEqual(unknown.phase, "DISCOVERED")
                verified = record_provenance(
                    registry,
                    "SRC-1",
                    "SOURCE_INDEX",
                    "PRIMARY",
                    ("SOURCE_INDEX.md",),
                )
                self.assertEqual(verified.provenance, "SOURCE_INDEX")
                self.assertEqual(verified.tier, "PRIMARY")
                self.assertEqual(verified.authority_refs, ("SOURCE_INDEX.md",))
                self.assertEqual(verified.phase, "DISCOVERED")

class SourceReconcileTests(unittest.TestCase):
    def test_enqueue_claims_preserves_adjudicated_dispositions_and_holds(self):
        from tools.bbma_orchestrator.source_reconcile import enqueue_claims
        items = enqueue_claims(
            "SRC-1",
            [
                {"claim_id": "C2", "disposition": "UNCLEAR", "hold_items": ["missing page"]},
                {"claim_id": "C1", "disposition": "MATCH"},
            ],
        )
        self.assertEqual([item.claim_id for item in items], ["C2", "C1"])
        self.assertEqual(items[0].hold_items, ("missing page",))
        self.assertEqual(items[0].disposition, "UNCLEAR")

    def test_reconciliation_hold_is_preserved_and_not_core_eligible(self):
        from tools.bbma_orchestrator.source_reconcile import eligible_for_core_link, record_reconciliation
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            with SourceRegistry(Path(tmp) / "sources.db") as registry:
                registry.register_discovered("SRC-1", "file:///a.pdf")
                for phase in ("INGESTED", "INTEGRITY_VERIFIED", "PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                record = record_reconciliation(registry, "SRC-1", "PARTIAL", hold_items=("conflict",))
                self.assertEqual(record.hold_items, ("conflict",))
                self.assertFalse(eligible_for_core_link(record))

    def test_accepted_core_requires_explicit_authority_and_no_hold(self):
        from tools.bbma_orchestrator.source_reconcile import eligible_for_core_link, record_reconciliation
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            with SourceRegistry(Path(tmp) / "sources.db") as registry:
                registry.register_discovered("SRC-1", "file:///a.pdf")
                for phase in ("INGESTED", "INTEGRITY_VERIFIED", "PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                with self.assertRaises(ValueError):
                    record_reconciliation(registry, "SRC-1", "ACCEPTED_CORE")
                accepted = record_reconciliation(
                    registry, "SRC-1", "ACCEPTED_CORE", accepted_authority="decision:CORE-001"
                )
                self.assertTrue(eligible_for_core_link(accepted))

class SourceLibraryRegistryTests(unittest.TestCase):
    def test_source_phase_progression_and_skip_rejected(self):
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            with SourceRegistry(Path(tmp) / "sources.db") as registry:
                registry.register_discovered("SRC-1", "file:///a.pdf", media_type="pdf")
                self.assertEqual(registry.get("SRC-1").phase, "DISCOVERED")
                registry.transition_phase("SRC-1", "INGESTED")
                registry.transition_phase("SRC-1", "INTEGRITY_VERIFIED")
                self.assertEqual(registry.get("SRC-1").phase, "INTEGRITY_VERIFIED")
                with self.assertRaises(ValueError):
                    registry.transition_phase("SRC-1", "EXTRACTED")
                with self.assertRaises(ValueError):
                    registry.transition_phase("SRC-1", "DISCOVERED")

    def test_disposition_independent_and_accepted_core_is_guarded(self):
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            with SourceRegistry(Path(tmp) / "sources.db") as registry:
                registry.register_discovered("SRC-1", "file:///a.pdf")
                registry.set_disposition("SRC-1", "UNCLEAR")
                self.assertEqual(registry.get("SRC-1").disposition, "UNCLEAR")
                with self.assertRaises(ValueError):
                    registry.set_disposition("SRC-1", "ACCEPTED_CORE")
                for phase in ("INGESTED", "INTEGRITY_VERIFIED", "PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                with self.assertRaises(ValueError):
                    registry.set_disposition("SRC-1", "ACCEPTED_CORE")
                registry.set_disposition("SRC-1", "ACCEPTED_CORE", accepted_authority="decision:CORE-001")
                self.assertEqual(registry.get("SRC-1").accepted_authority, "decision:CORE-001")

    def test_ingest_is_idempotent_and_detects_duplicate_digest(self):
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "source.txt"
            file.write_text("same", encoding="utf-8")
            with SourceRegistry(root / "sources.db") as registry:
                first = registry.ingest_file("SRC-1", file, media_type="text")
                again = registry.ingest_file("SRC-1", file, media_type="text")
                duplicate = registry.ingest_file("SRC-2", file, media_type="text")
                self.assertEqual(first.status, "NEW")
                self.assertEqual(again.status, "UNCHANGED")
                self.assertEqual(duplicate.status, "DUPLICATE")
                self.assertEqual(duplicate.duplicate_of, "SRC-1")
                self.assertEqual(registry.get("SRC-1").digest, registry.get("SRC-2").digest)
                self.assertEqual([r.source_id for r in registry.find_by_digest(first.record.digest)], ["SRC-1", "SRC-2"])

    def test_source_change_stales_only_explicit_evidence_descendants(self):
        from tools.bbma_orchestrator.evidence import EvidenceDB
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "source.txt"
            file.write_text("v1", encoding="utf-8")
            with SourceRegistry(root / "sources.db") as registry, EvidenceDB(root / "evidence.db") as evidence:
                ingested = registry.ingest_file("SRC-1", file)
                for phase in ("PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                registry.set_disposition("SRC-1", "ACCEPTED_CORE", accepted_authority="decision:CORE-001")

                evidence.add_node("source:SRC-1", "source", ingested.record.digest, status="VALID")
                evidence.add_node("core:RE", "core_rule", "core-v1", status="VALID")
                evidence.add_node("contract:M12", "contract", "contract-v1", status="VALID")
                evidence.add_node("code:M12", "code", "code-v1", status="VALID")
                evidence.add_node("test:M12", "test", "test-v1", status="VALID")
                evidence.add_node("core:OTHER", "core_rule", "other-v1", status="VALID")
                evidence.add_node("code:OTHER", "code", "other-code-v1", status="VALID")
                evidence.add_edge("source:SRC-1", "core:RE")
                evidence.add_edge("core:RE", "contract:M12")
                evidence.add_edge("contract:M12", "code:M12")
                evidence.add_edge("code:M12", "test:M12")
                evidence.add_edge("core:OTHER", "code:OTHER")
                edge_count = evidence.conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]

                registry.link_evidence_node("SRC-1", "source:SRC-1")
                file.write_text("v2", encoding="utf-8")
                changed = registry.ingest_file("SRC-1", file)
                stale = registry.propagate_source_change("SRC-1", changed.record.digest, evidence)

                self.assertEqual(stale, ["core:RE", "contract:M12", "code:M12", "test:M12"])
                self.assertEqual(evidence.get_node("source:SRC-1")["digest"], changed.record.digest)
                self.assertEqual(evidence.get_node("source:SRC-1")["status"], "NOT VERIFIED")
                for node_id in stale:
                    self.assertEqual(evidence.get_node(node_id)["status"], "STALE")
                self.assertEqual(evidence.get_node("core:OTHER")["status"], "VALID")
                self.assertEqual(evidence.get_node("code:OTHER")["status"], "VALID")
                self.assertEqual(evidence.conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0], edge_count)

    def test_source_impact_bridge_is_fail_closed_and_idempotent(self):
        from tools.bbma_orchestrator.evidence import EvidenceDB
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "source.txt"
            file.write_text("v1", encoding="utf-8")
            with SourceRegistry(root / "sources.db") as registry, EvidenceDB(root / "evidence.db") as evidence:
                registry.register_discovered("NO-DIGEST", "file:///missing.pdf")
                for phase in ("INGESTED", "INTEGRITY_VERIFIED", "PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("NO-DIGEST", phase)
                registry.set_disposition("NO-DIGEST", "ACCEPTED_CORE", accepted_authority="decision:CORE-000")
                with self.assertRaisesRegex(ValueError, "digest"):
                    registry.link_evidence_node("NO-DIGEST", "source:NO-DIGEST")

                ingested = registry.ingest_file("SRC-1", file)
                with self.assertRaisesRegex(ValueError, "ACCEPTED_CORE"):
                    registry.link_evidence_node("SRC-1", "source:SRC-1")
                for phase in ("PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                registry.set_disposition("SRC-1", "ACCEPTED_CORE", accepted_authority="decision:CORE-001")
                evidence.add_node("source:SRC-1", "source", ingested.record.digest, status="VALID")
                evidence.add_node("core:RE", "core_rule", "core-v1", status="VALID")
                evidence.add_edge("source:SRC-1", "core:RE")
                registry.link_evidence_node("SRC-1", "source:SRC-1")
                self.assertEqual(registry.propagate_source_change("SRC-1", ingested.record.digest, evidence), [])
                self.assertEqual(evidence.get_node("core:RE")["status"], "VALID")

                bad_file = root / "bad.txt"
                bad_file.write_text("b1", encoding="utf-8")
                bad = registry.ingest_file("SRC-BAD", bad_file)
                for phase in ("PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-BAD", phase)
                registry.set_disposition("SRC-BAD", "ACCEPTED_CORE", accepted_authority="decision:CORE-BAD")
                evidence.add_node("core:BAD", "core_rule", bad.record.digest, status="VALID")
                registry.link_evidence_node("SRC-BAD", "core:BAD")
                bad_file.write_text("b2", encoding="utf-8")
                bad_changed = registry.ingest_file("SRC-BAD", bad_file)
                with self.assertRaisesRegex(ValueError, "source evidence node"):
                    registry.propagate_source_change("SRC-BAD", bad_changed.record.digest, evidence)

    def test_source_impact_bridge_prevalidates_all_links_before_staling(self):
        from tools.bbma_orchestrator.evidence import EvidenceDB
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "source.txt"
            file.write_text("v1", encoding="utf-8")
            with SourceRegistry(root / "sources.db") as registry, EvidenceDB(root / "evidence.db") as evidence:
                ingested = registry.ingest_file("SRC-1", file)
                for phase in ("PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                registry.set_disposition("SRC-1", "ACCEPTED_CORE", accepted_authority="decision:CORE-001")
                evidence.add_node("a:valid-source", "source", ingested.record.digest, status="VALID")
                evidence.add_node("core:child", "core_rule", "core-v1", status="VALID")
                evidence.add_node("z:invalid-kind", "core_rule", ingested.record.digest, status="VALID")
                evidence.add_edge("a:valid-source", "core:child")
                registry.link_evidence_node("SRC-1", "a:valid-source")
                registry.link_evidence_node("SRC-1", "z:invalid-kind")

                file.write_text("v2", encoding="utf-8")
                changed = registry.ingest_file("SRC-1", file)
                with self.assertRaisesRegex(ValueError, "source evidence node"):
                    registry.propagate_source_change("SRC-1", changed.record.digest, evidence)
                self.assertEqual(evidence.get_node("a:valid-source")["digest"], ingested.record.digest)
                self.assertEqual(evidence.get_node("a:valid-source")["status"], "VALID")
                self.assertEqual(evidence.get_node("core:child")["status"], "VALID")

    def test_changed_digest_resets_semantic_acceptance_fail_closed(self):
        from tools.bbma_orchestrator.source_library import SourceRegistry
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "source.txt"
            file.write_text("v1", encoding="utf-8")
            with SourceRegistry(root / "sources.db") as registry:
                registry.ingest_file("SRC-1", file)
                for phase in ("PROVENANCE_CLASSIFIED", "EXTRACTED", "RECONCILIATION_PENDING", "RECONCILED"):
                    registry.transition_phase("SRC-1", phase)
                registry.set_disposition("SRC-1", "ACCEPTED_CORE", accepted_authority="decision:CORE-001")
                file.write_text("v2", encoding="utf-8")
                changed = registry.ingest_file("SRC-1", file)
                record = registry.get("SRC-1")
                self.assertEqual(changed.status, "CHANGED")
                self.assertEqual(record.phase, "INTEGRITY_VERIFIED")
                self.assertEqual(record.disposition, "UNREVIEWED")
                self.assertEqual(record.accepted_authority, "")

if __name__ == "__main__":
    unittest.main()
