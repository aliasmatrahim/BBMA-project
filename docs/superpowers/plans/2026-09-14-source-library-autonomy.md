# BBMA Source Library Autonomy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic, interruption-safe source-library lifecycle that can ingest, classify, reconcile, index and impact-route BBMA evidence without gaining Strategy-Core authority.

**Architecture:** Extend PR #151's deterministic orchestrator instead of creating a second control plane. Source processing phase and semantic disposition are independent state dimensions; SHA-256 identity reuses `evidence.sha256_file`; Evidence DAG carries only verified provenance dependencies.

**Tech Stack:** Python 3.12 standard library, SQLite, existing `tools.bbma_orchestrator` primitives, unittest, G40 adapters only for local-media/native evidence.

**Spec:** GitHub Issue #152 and `docs/BBMA_AUTONOMOUS_ENGINEERING_INFRASTRUCTURE.md`.

## Global Constraints
- No BBMA Strategy-Core rule, entry/exit/filter, SL/TP, lifecycle or execution authority may be created by tooling.
- HOLD/PARTIAL/UNCLEAR/SOURCE_CONFLICT/REJECTED evidence stays non-executable.
- `ACCEPTED_CORE` requires explicit accepted authority; it is never inferred from model confidence, ASR, filename, majority vote or weak provenance.
- Original, corrected and derived artifacts remain separate by role.
- Zero-result search is never treated as proof of absence.
- PR #149/#151 are dependencies only; no automatic merge/deploy/restart/trading enablement.

---
### Task 1: Source registry, lifecycle and idempotent ingestion

**Files:**
- Create: `tools/bbma_orchestrator/source_library.py`
- Modify: `tools/bbma_orchestrator/__init__.py`
- Modify/Test: `tests/test_bbma_orchestrator.py`

**Interfaces:** `SourceRegistry(db_path)`, `SourceRecord`, `ingest_file(source_id, path, ...)`, `transition_phase(source_id, phase)`, `set_disposition(source_id, disposition, accepted_authority='')`, `get(source_id)`, `find_by_digest(digest)`.

- [x] Add failing tests for valid sequential phase progression, rejected skips/backwards transitions, independent semantic disposition, and `ACCEPTED_CORE` requiring explicit accepted authority.
- [x] Add failing tests proving unchanged digest ingestion is idempotent and same digest under another SourceID is reported as duplicate without rewriting the original record.
- [x] Implement the SQLite schema and invariants using existing `sha256_file` and `utc_now`; do not add another hash implementation.
- [x] Run focused source-registry tests, then the full orchestrator suite and `compileall`.
- [x] Commit only Task 1 files after the green evidence boundary.

### Task 2: Discovery/import and provenance recording

**Files:** Create `tools/bbma_orchestrator/source_discovery.py`; modify tests and package exports.

**Interfaces:** `discover_paths(roots, patterns)`, `classify_artifact_role(path, explicit_role)`, `record_provenance(registry, source_id, provenance, tier, authority_refs)`.

- [x] Test deterministic sorted discovery, digest duplicate suppression, raw/corrected/derived role separation and unknown provenance remaining `UNVERIFIED` rather than promoted.
- [x] Implement bounded filesystem discovery only from caller-supplied roots; no ad-hoc internet crawling.
- [x] Run focused/full tests and commit the independent deliverable.

### Task 3: Reconciliation queue and no-promotion guard

**Files:** Create `tools/bbma_orchestrator/source_reconcile.py`; modify tests/exports.

**Interfaces:** `ReconciliationItem`, `enqueue_claims(...)`, `record_reconciliation(...)`, `eligible_for_core_link(...)`.

- [x] Test MATCH/CORROBORATION/PARTIAL/UNCLEAR/SOURCE_CONFLICT/REJECTED outcomes and HOLD preservation.
- [x] Test that `ACCEPTED_CORE` fails unless an explicit accepted decision/authority reference is supplied.
- [x] Implement queue state without embedding BBMA semantic judgments in code; callers provide adjudicated disposition.
- [x] Run focused/full tests and commit.
### Task 4: Source-to-Core impact bridge

**Files:** Modify `tools/bbma_orchestrator/source_library.py`, `tools/bbma_orchestrator/evidence.py`; modify tests.

**Interfaces:** `link_evidence_node(source_id, node_id)`, `propagate_source_change(source_id, new_digest, evidence_db)`.

- [x] Test that only explicitly linked downstream Core/contract/code/test nodes become stale after an accepted evidence digest changes.
- [x] Test that unrelated Evidence-DAG nodes remain VALID and unknown semantic edges are never invented.
- [x] Implement the minimal bridge by delegating staleness to `EvidenceDB.mark_changed`.
- [x] Run focused/full tests and commit.

### Task 5: Bounded SOURCE_INDEX/register update generator

**Files:** Create `tools/bbma_orchestrator/source_updates.py`; modify tests/exports.

**Interfaces:** `build_index_patch(records, current_text, anchor)`, `build_register_rows(records)` returning proposed text/diff data only.

- [ ] Test deterministic output, single-anchor enforcement, no mutation of original evidence, and refusal to emit Core promotion for unresolved dispositions.
- [ ] Implement proposal generation only; writing/committing stays under normal Issue/branch/PR workflow.
- [ ] Run focused/full tests and commit.

### Task 6: Failure-first source dashboard and context integration

**Files:** Modify `source_library.py` and `core.py`; modify tests.

**Interfaces:** `SourceRegistry.failure_first_summary()`, source summary field in bounded context pack.

- [ ] Test ordering: conflicts/unclear/partial/missing/stale first, aggregate registered MATCH volume, no raw transcript/log streaming.
- [ ] Extend context packs with caller-requested source summary only; never inject whole project history.
- [ ] Run focused/full tests and commit.

### Task 7: G40 Primary-15/Group-3/media adapters

**Files:** Create `tools/bbma_orchestrator/source_g40.py`; modify tests and native adapter configuration examples.

**Interfaces:** `scan_manifest(path)`, `classify_manifest_state(payload)`, `plan_resume(manifests)`.

- [ ] Test completed manifests are never blindly rerun, partial work resumes only missing units, and ASR-DRAFT never equals reconciled/accepted Core.
- [ ] Implement read-only manifest inspection first; any long-running local process remains explicit through the native adapter.
- [ ] Validate against fixture data, then bounded live G40 manifests; record local evidence separately.
- [ ] Commit deterministic code only; do not alter original media/transcripts.
### Task 8: End-to-end acceptance and immutable evidence package

**Files:** Modify orchestrator README/docs, CI workflow path filters if needed, and tests; use existing evidence-package generator.

- [ ] Build a fixture source through DISCOVERED -> REGISTERED while keeping semantic disposition independent.
- [ ] Verify duplicate ingestion, changed-digest staleness, reconciliation HOLD, bounded index proposal, failure-first summary and interruption/resume checkpoint in one integration test.
- [ ] Run `python -m compileall tools/bbma_orchestrator` and the full orchestrator test suite from a clean checkout/worktree.
- [ ] Generate immutable evidence package containing changed files, hashes, test result references and authority metadata.
- [ ] Open/update Draft PR stacked on PR #151; do not merge PR #149/#151/#152 implementation automatically.

## Execution routing
Runtime model routing: Task 1 is executed on Luna Medium for deterministic implementation and tests. Warn before escalation if a later step requires Sol/Astra because of source-authority ambiguity, recovery semantics, or unresolved Core/source conflict. Task 2-8 retain the same escalation boundary; G40/local evidence remains required for live media claims. No automatic model escalation or XHigh routing.

## Self-review
- Spec coverage: all Issue #152 deliverables map to Tasks 1-8.
- Placeholder scan: no TBD/TODO implementation steps.
- Authority check: processing state is independent from semantic disposition; `ACCEPTED_CORE` is guarded by explicit authority.
- Duplication check: hashing, atomic writes, Evidence DAG, task manifest/checkpoint and evidence package reuse PR #151 primitives.
