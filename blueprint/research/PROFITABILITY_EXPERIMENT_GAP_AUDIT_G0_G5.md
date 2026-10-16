# Profitability Experiment Evidence Gap Audit — G0–G5

Date: 2026-10-16  
Status: **STATIC AUDIT / NOT RUNTIME VERIFIED**  
Scope: evidence and experiment tooling only. No Strategy-Core, EA source, execution authority, or Q10 runtime changes.

## Status definitions

- **EXISTS** — a named function/contract/test directly implements the capability stated.
- **PARTIAL** — a related primitive exists, but the experiment-level gate or required binding is incomplete.
- **MISSING** — no adequate implementation was confirmed in the inspected files. This is not a repository-wide proof of absence.

G0–G5 are audit work-package labels for this research task, not previously established canonical BBMA module identifiers.

## Gap matrix

| Gate | Capability | Status | Current evidence | Confirmed gap |
|---|---|---|---|---|
| G0 | SHA-256 of files | EXISTS | `tools/bbma_orchestrator/evidence.py`: `sha256_file` | None for the primitive. |
| G0 | Content-addressed cache / evidence DAG / stale descendants | EXISTS | `ContentAddressedStore`, `EvidenceDB.record_artifact`, `add_node`, `add_edge`, `mark_changed`; tests `test_source_change_stales_only_explicit_evidence_descendants`, `test_ingest_is_idempotent_and_detects_duplicate_digest` | These are general evidence primitives, not a profitability-run identity contract. |
| G0 | Unified immutable run manifest binding source commit, MQ4, EX4, SET, dataset, costs and outputs | PARTIAL | `experiment.py::validate_manifest`, `EvidenceDB.register_experiment`, `find_experiment_runs`, `get_experiment_run`; `experiment-register` CLI; `tests/test_experiment_inventory.py` | Run ID collision and exact-manifest idempotency are implemented; CI for latest head is not yet verified. Fingerprint groups matching setups but is not itself a profitability replication claim. |
| G1 | Telemetry source provenance and raw record identity | EXISTS | `tools/bbma_orchestrator/telemetry.py`: source SHA, line, emitter/build marker, raw line, `runtime_verification=NOT VERIFIED` | Does not validate source price-data integrity. |
| G1 | Generic OHLC/tick data quality gate for experiment datasets | PARTIAL | `tools/bbma_orchestrator/dataset_validator.py::validate_dataset_file`, `write_dataset_validation_report`; `dataset-validate` CLI; `tests/test_dataset_validator.py` | Static implementation covers timestamp ordering/duplicates/gaps, OHLC consistency, Bid/Ask coverage, timeframe alignment, data-as-of and report identity. CI is not yet verified; broker provenance, tick source authenticity and any broker-specific gap calendar remain separate evidence. |
| G1 | Manifest-level price basis, synthetic tick rejection, timezone/window and closed-candle declarations | PARTIAL | New `experiment.py::validate_manifest` checks declarations and chronology | Declarations do not prove the underlying dataset source is genuine or complete; dataset validation remains a separate gate. |
| G2 | Task lifecycle manifest and pass-before-close guards | EXISTS | `core.py::TaskManifest`; tests `test_manifest_phase_and_pass_gate`, `test_manifest_rejects_skip`, `test_pass_before_closed_rejected` | These govern engineering tasks, not preregistered strategy hypotheses. |
| G2 | Hypothesis registry, frozen parameters and explicit run linkage | PARTIAL | New manifest requires hypothesis ID/statement, parameter hash, freeze state and protocol partition | No cross-run registry prevents duplicate IDs or verifies that a hypothesis was registered before outcomes were inspected. |
| G3 | Native-command dry-run, exact input hash checks and fail-closed execution | EXISTS | `NativeAdapter`; tests `test_native_adapter_is_dry_run_by_default`, `test_native_adapter_rejects_input_identity_drift`, `test_native_adapter_rejects_duplicate_process_before_execute` | This is command orchestration, not a complete MT4 profitability runner contract. |
| G3 | Required artifact hash verification and explicit run status | PARTIAL | `verify_artifacts`, `classify_run_status`, `experiment-validate`, G1 `dataset_validation_report`, and `EvidenceDB.register_experiment`; focused tests in `tests/test_experiment_evidence.py` and `tests/test_experiment_inventory.py` | Latest-head CI and full regression are not yet verified; static tooling is not tester/runtime PASS. |
| G4 | NMJE realized-outcome correlation and uncertainty reporting | EXISTS | `blueprint/N2_NMJE_RESEARCH_METHODOLOGY.md`, N2 correlator/attributor/evidence-sufficiency pipeline | This is forward telemetry attribution, not IS/validation/untouched-OOS backtest partitioning. |
| G4 | Frozen chronological IS → validation → untouched OOS protocol | MISSING before this PR; protocol defined, enforcement PARTIAL | Contract V1 defines freeze-before-OOS and no OOS tuning; validator rejects late freeze/tuning for OOS | No splitter/walk-forward engine or multi-run OOS reuse registry was confirmed. |
| G5 | Wilson interval, sample visibility and evidence sufficiency | EXISTS | N2 methodology requires decisive win rate, Wilson 95% interval, sample and data-integrity reporting | Those outputs do not establish that a new profitability experiment has passed a preregistered statistical gate. |
| G5 | Path-risk simulation separated from edge evidence | PARTIAL | Contract V1 explicitly limits trade-order permutation to path-risk interpretation | No profitability statistical engine with dependence-aware block bootstrap or validated decision criteria was confirmed. |
| G5 | Distinct evidence validity vs hypothesis result | PARTIAL | New contract/validator separates `run_status` from `hypothesis_result` and never auto-infers profitability | Hypothesis-result adjudication still requires a separate report and preregistered criteria. |

## Minimal contract decisions

1. Keep existing SHA-256, content-addressed cache, evidence DAG, telemetry and native adapter; do not create a parallel evidence store.
2. Required manifest identities: run ID, hypothesis/parameter hash, source commit + MQ4/EX4/SET hashes, dataset hash and metadata, broker/tester identity, cost model, warm-up/evaluation window, frozen protocol partition, trade history, report and log hashes.
3. Hard-fail malformed/missing identities, hash mismatch, unsafe artifact path, invalid chronology, synthetic/reconstructed ticks, non-closed-candle declaration, incomplete cost assumptions, OOS tuning, or missing required artifacts.
4. Keep `INVALID_RUN`, `RUN_FAILED`, `VALIDATION_FAILED`, and `EVIDENCE_ACCEPTED` distinct. Keep hypothesis outcome separate: `NOT_EVALUATED`, `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`.
5. `EVIDENCE_ACCEPTED` is evidence integrity only; never infer profitability, BBMA Core compliance, runtime PASS or release readiness from it.
6. Do not invent a universal minimum sample size. Preregister criteria and report uncertainty, costs, exclusions and all attempts.
7. A reused OOS period is no longer untouched after it influences parameter/hypothesis changes; require a fresh holdout or unused pair/period.
8. Data authenticity and actual OHLC/tick integrity remain a separate required validator; manifest declarations alone are insufficient.

## Queue and dependency check

The active `d1-owner-dev` `blueprint/CURRENT.md` and `blueprint/MASTER_QUEUE.md` state that **Q10 Phase L R5 remains the highest-priority active final-acceptance task**. The exact Build 5.11 / R2 candidate remains bound to R5; R5-14 and R5-16 require naturally occurring broker events, and R6 is not promoted until R5 passes. See [Q10 Phase-L R5 live-state audit](https://github.com/aliasmatrahim/BBMA-project/blob/d1-owner-dev/blueprint/audits/Q10_PHASE_L_R5_LIVE_STATE_20260924.md).

This research tooling task is isolated on a scoped branch from `main`. It must not restart/modify the Q10 terminal, synthesize broker events, alter the frozen candidate, or change Q10 queue status.

## Validation record

- GitHub source review: performed.
- New focused tests: authored, **not locally executed in this session**.
- GitHub Actions for the PR head: pending/in progress at time of this audit.
- Native MT4 compile / Strategy Tester / broker runtime: **NOT RUN / NOT VERIFIED**.
- Strategy-Core delta: none.
