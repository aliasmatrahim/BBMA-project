# AUTONOMY-EFF-AB #154 Benchmark Report

Tooling head: `b0db1b652a0f46691b5aad52299239ae42a98994`
D1 authority: `23def0919386263007ead1898b94637cc17f7f36`

## Warm-run efficiency
- Context bytes: 916773 -> 4016 (99.56% reduction)
- Repeated validations: 3 -> 0 (100.00% reduction)
- Wall clock: 105.154s -> 1.476s (98.60% reduction)

## Required task classes
- `docs_traceability`: context 58449 -> 1131 bytes; route `MEDIUM`; validation `REUSED_PASS`
- `strategy_f6_readonly`: context 477720 -> 1609 bytes; route `HIGH/XHIGH`; validation `REUSED_PASS`
- `telemetry_tooling`: context 380604 -> 1276 bytes; route `HIGH`; validation `REUSED_PASS`

## Strategy-Core safety
- CORE-V2-F6 overall: `NOT VERIFIED`.
- Runtime remains: `NOT VERIFIED` (not promoted by this benchmark).
- Targeted verified-map selection: ['TEST_DRIVER_F3', 'TEST_DRIVER_F6', 'TEST_DRIVER_F1'] from ['TEST_DRIVER_F1', 'TEST_DRIVER_F2', 'TEST_DRIVER_F3', 'TEST_DRIVER_F5', 'TEST_DRIVER_F6'].
- Selected test drivers are measurement output only; this read-only benchmark does not claim they were executed as new Core acceptance.

## Acceptance
- warm_context_reduction_ge_30pct: PASS
- repeated_work_reduction_ge_20pct: PASS
- no_source_authority_regression: PASS
- no_validation_gate_bypass: PASS
- no_strategy_runtime_promotion: PASS
- no_strategy_or_runtime_ownership_duplication: PASS
- all_required_task_classes_present: PASS

Fixture preparation (authority snapshots/raw telemetry export) is excluded from timed runs and is hash-recorded in the evidence package.
