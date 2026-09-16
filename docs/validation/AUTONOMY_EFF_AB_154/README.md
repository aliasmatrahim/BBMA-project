# AUTONOMY-EFF-AB #154 Validation Evidence

Issue: #154 — end-to-end autonomy efficiency validation.
Tooling authority: `b0db1b652a0f46691b5aad52299239ae42a98994` (PR #151 head at execution).
D1/source authority: `23def0919386263007ead1898b94637cc17f7f36`.

This directory preserves the reproducible benchmark harness, protocol, full run results, report, authority manifest, independent recomputation, telemetry summary, and the original immutable evidence-package index.

Measured warm-run results:
- model-facing context: 916,773 -> 4,016 bytes (99.56% reduction);
- repeated validations: 3 -> 0 (100% reduction);
- measured workflow wall clock: 105.154s -> 1.476s (98.60% reduction).

Required task classes covered: docs/traceability, telemetry/tooling, and Strategy-Core-sensitive read-only (`CORE-V2-F6`).

Safety boundary: this validation does not change EA source, M01-M27/M12N semantics, Strategy Core, runtime authority, merge/deploy state, or trading behaviour. `CORE-V2-F6` overall and runtime remain `NOT VERIFIED`; targeted test selection is measurement evidence only, not new Core acceptance.

The original evidence-package SHA-256 is stored in `evidence_package.sha256`. `closure_manifest.json` binds the Git-committed closure artifacts by relative path and SHA-256.