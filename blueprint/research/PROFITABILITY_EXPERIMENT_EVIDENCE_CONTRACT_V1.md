# Profitability Experiment Evidence Contract V1

Status: proposed implementation contract for Issue #291. Scope is research evidence/tooling only; it does not authorize BBMA trade decisions.

## Purpose and boundaries

This contract joins existing SHA-256/evidence-package tooling to a deterministic, immutable experiment record. It does not replace the existing evidence DAG, NMJE identity/outcome attribution, task manifest, MT4 runtime acceptance, or Strategy-Core source hierarchy.

Evidence validity and hypothesis result are separate axes:
- `run_status`: `INVALID_RUN`, `RUN_FAILED`, `VALIDATION_FAILED`, `EVIDENCE_ACCEPTED`.
- `hypothesis_result`: `NOT_EVALUATED`, `SUPPORTED`, `NOT_SUPPORTED`, `INCONCLUSIVE`.

`EVIDENCE_ACCEPTED` means only that required evidence is complete, attributable and valid. It is not a claim of profitability, Core compliance, runtime PASS, or production readiness. Hypothesis results require a separate preregistered decision report; a validator must not infer `SUPPORTED` from a point estimate.

## Required run manifest (schema version 1)

A JSON object contains:

- `schema_version`: integer 1.
- `run_id`: unique immutable identifier; reruns use a new ID.
- `hypothesis`: `id`, `statement`, `preregistered_at`, `parameter_sha256`, `parameters_frozen`.
- `build`: `build_id`, `source_commit`, `source_sha256`, `ex4_sha256`, `set_sha256`.
- `dataset`: `dataset_id`, `sha256`, `symbol`, `timeframe`, `source_type`, `price_basis`, `synthetic_ticks`, `timezone`, `start`, `end`, `warmup_start`, `evaluation_start`, `evaluation_end`, `closed_candles_only`.
- `environment`: `broker`, `terminal_build`, `tester_mode`.
- `costs`: `spread_model`, `commission_model`, `swap_included`, `slippage_model`.
- `protocol`: `partition` (`IS`, `VALIDATION`, or `OOS`), `frozen_at`, `parameter_freeze_sha256`, `oos_tuning_performed`.
- `artifacts`: non-empty list of `kind`, `path`, and `sha256` records, including complete trade history, tester report/log, and a validation report whose contents can be independently reviewed. The machine-readable validation report must be UTF-8 JSON and bind `validation_status=PASS`, `run_id`, `build_id`, `dataset_sha256`, and `parameter_sha256` to the manifest.

All SHA-256 values must be 64 hexadecimal characters. `price_basis` must explicitly identify Bid/Ask ticks or Bid/Ask bars. Reconstructed/synthetic ticks are not accepted as native tick evidence. The manifest must state the actual timezone and separate warm-up from evaluation windows. The validator verifies the validation report’s exact run/build/dataset/parameter identity and PASS marker; this still does not independently prove that the underlying validation method is correct.

## Hard-fail conditions

Fail closed as `INVALID_RUN` when a required field is absent/empty, schema is unknown, a hash is malformed, a time window is invalid, a required artifact is absent, or the run identity cannot be tied to exact build/data/config artifacts. Reject:
- `closed_candles_only=false` for this BBMA experiment contract;
- unsupported/non-Bid-Ask price basis or synthetic/reconstructed ticks;
- warm-up/evaluation chronology violations;
- OOS parameter tuning, parameter changes after freeze, or a freeze timestamp after OOS evaluation starts;
- missing spread/commission/slippage assumptions or omitted swap accounting;
- artifact hash mismatch, path traversal outside the declared evidence root, or missing trade history/report/log/validation report.

A process error is `RUN_FAILED`. A completed run missing required validation evidence is `VALIDATION_FAILED`. Zero trades are not automatically a data-invalid run: report the run as inconclusive unless the preregistered hypothesis explicitly makes zero trades a protocol failure.

## OOS protocol

1. Register the hypothesis and parameters before viewing the relevant evaluation outcomes; hash the frozen parameter/config file.
2. Record data identity, symbol, timeframe, broker/tester build, timezone, warm-up window, evaluation window and complete cost model before the run.
3. Keep warm-up bars outside the scored evaluation window. Use BBMA's approved M15 processing clock and closed-candle rules; this contract does not redefine Core.
4. Separate chronological IS, validation and untouched OOS segments. Freeze the split boundaries and configuration before OOS evaluation. Do not tune or select parameters based on OOS results.
5. If OOS is reused to revise a hypothesis, it is no longer untouched OOS; the revised hypothesis requires a new holdout period or previously unused pair/period.
6. Report all attempted runs, including failed, zero-trade and rejected runs. Identical reruns are reproducibility checks, not independent replications.
7. Report full costs and uncertainty. A trade-order permutation/Monte Carlo path analysis is drawdown/path-risk evidence, not proof that signals have edge. IID bootstrap can ignore serial dependence; use a dependence-aware method such as block bootstrap where appropriate, and document its assumptions.
8. No sample-size threshold or acceptance threshold is silently invented. Preregister the decision criteria and show sample counts, uncertainty, costs, drawdown and all exclusions.

## Final decision boundary

A run manifest validator can validate schema, chronology and artifact identity only. It cannot prove the data source is truthful, the tester is correct, the strategy is profitable, or runtime behaviour matches the backtest. Those require separate attributable data-source, test and runtime evidence. No evidence status grants Strategy-Core, risk, execution or production authority.
