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
- `dataset`: `dataset_id`, `sha256`, `symbol`, `timeframe`, `source_type`, `price_basis`, `synthetic_ticks`, `timezone`, `start`, `end`, `warmup_start`, `evaluation_start`, `evaluation_end`, `data_as_of`, `timestamp_convention`, `closed_candles_only`. Optional `allowed_gap_windows` must list exact timezone-aware `start`/`end` windows; tick datasets must supply a preregistered positive integer `dataset.max_gap_seconds`; a CLI override, if used, must match.
- `environment`: `broker`, `terminal_build`, `tester_mode`.
- `costs`: `spread_model`, `commission_model`, `swap_included`, `slippage_model`.
- `protocol`: `partition` (`IS`, `VALIDATION`, or `OOS`), `frozen_at`, `parameter_freeze_sha256`, `oos_tuning_performed`.
- `artifacts`: non-empty list of `kind`, `path`, and `sha256` records, including source, EX4, SET, parameters, dataset, complete trade history, tester report/log, general validation report, and `dataset_validation_report`. Both reports must be UTF-8 JSON and bind `run_id`, `build_id`, `dataset_sha256`, and `parameter_sha256` to the manifest. The G1 report must also contain `validation_status=PASS`, `dataset_status=VALID`, and `validator_version=G1-DATASET-VALIDATOR-1.0`.

All SHA-256 values must be 64 hexadecimal characters. `price_basis` must explicitly identify Bid/Ask ticks or Bid/Ask bars. Reconstructed/synthetic ticks are not accepted as native tick evidence. The manifest must state the actual timezone and separate warm-up from evaluation windows. G1 CSV schema is strict: ticks require `timestamp,bid,ask`; bars require `timestamp` plus `bid_open/high/low/close` and `ask_open/high/low/close`. Timestamps are timezone-aware ISO-8601; bar timestamps are `BAR_OPEN` and must align to the declared timeframe. The G1 validator rejects duplicate/non-monotonic timestamps, invalid or inconsistent OHLC, Ask below Bid, unexpected gaps, evaluation boundaries not aligned to closed-candle boundaries, and data-as-of times before evaluation end. Gaps are not silently interpreted as weekends/holidays; only explicitly declared `allowed_gap_windows` are exempted. No interpolation or repair occurs. Both `dataset-validate` and `experiment-validate` execute the G1 checks against the actual CSV; `experiment-validate` recomputes the result and compares the complete critical metrics to the identity-bound report, so a hand-authored PASS report cannot bypass the data gate. The validator verifies file hash and report identity but does not prove broker provenance or source authenticity; those require separate evidence.

## Hard-fail conditions

Fail closed as `INVALID_RUN` when a required field is absent/empty, schema is unknown, a hash is malformed, a time window is invalid, a required artifact is absent, or the run identity cannot be tied to exact build/data/config artifacts. Also reject a missing/non-PASS G1 dataset report, wrong timestamp convention, data-as-of before evaluation end, or data integrity errors. Reject:
- `closed_candles_only=false` for this BBMA experiment contract;
- unsupported/non-Bid-Ask price basis or synthetic/reconstructed ticks;
- warm-up/evaluation chronology violations;
- OOS parameter tuning, parameter changes after freeze, or a freeze timestamp after OOS evaluation starts;
- missing spread/commission/slippage assumptions or omitted swap accounting;
- artifact hash mismatch, path traversal outside the declared evidence root, or missing trade history, tester report/log, general validation report, or G1 dataset validation report.

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

The manifest is registered in the existing EvidenceDB inventory with a unique run ID, canonical setup fingerprint, artifact-to-run DAG edges and optional parent-run lineage. Re-registering identical manifest bytes is idempotent; reusing a run ID for different manifest bytes fails closed. Evidence nodes remain NOT VERIFIED after registration. A run manifest validator can validate schema, chronology and artifact identity only. The G1 validator checks the CSV bytes and declared data quality rules, but cannot prove the data source is truthful, the tester is correct, the strategy is profitable, or runtime behaviour matches the backtest. Those require separate attributable data-source, test and runtime evidence. No evidence status grants Strategy-Core, risk, execution or production authority.
