# BBMA v4.58 Broker Runtime Validation Runbook

Status: autonomous-prep package for broker/demo validation only. Canonical EA remains frozen.

## Frozen source identity

- Source: `blueprint/source/BBMA_EA.mq4`
- Build: `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage`
- Property: `4.58`
- Git blob: `a166ffb23aba5e6b4011a28d9de8896cd00e33a1`
- SHA-256: `ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc`
- Canonical gates: `EnableD1TPWLifecycle=false`, `EnableC044Lifecycle=false`

The runtime variant builder is source-bound to the identity above and must fail closed if the canonical source changes.

## Test profiles

| Profile | D1 TPW | C044 | Purpose |
|---|---:|---:|---|
| BASELINE | OFF | OFF | R3-R6 baseline/runtime evidence |
| R1_D1TPW | ON | OFF | D1 Extreme TP-Wajib lifecycle only |
| R2_C044 | OFF | ON | C044 failed-momentum lifecycle only |

Never run both lifecycle gates ON in this validation package.

## Required autonomous/native gate before broker testing

Run `blueprint/runtime/v458_native_compile_matrix.ps1`. It must report:

- `V458_RUNTIME_VARIANT_BUILDER_SELFTEST=PASS`
- `V458_RUNTIME_ANALYZER_SELFTEST=PASS`
- `OBSERVER_READ_ONLY_STATIC=PASS`
- `METAEDITOR_0E0W_BASELINE=PASS`
- `METAEDITOR_0E0W_R1_D1TPW=PASS`
- `METAEDITOR_0E0W_R2_C044=PASS`
- `METAEDITOR_0E0W_OBSERVER=PASS`
- `V458_NATIVE_COMPILE_MATRIX=PASS`

No broker-runtime conclusion is valid if this gate fails.

## Runtime evidence components

1. Build the required test-only EA variant with `blueprint/tools/v458_runtime_variant_builder.py`.
2. Attach `blueprint/runtime/V458_Runtime_Observer.mq4` to a separate chart in the same MT4 terminal.
3. Keep `DebugLevel` high enough to emit M17, D1/D1O, P3 and N2 diagnostic records needed by the selected test.
4. Run only on a demo/broker-authenticated session for broker-runtime conclusions.
5. Collect logs with `blueprint/runtime/collect_v458_runtime_bundle.ps1`.
6. Analyze one or more bundles with `blueprint/tools/v458_runtime_analyzer.py`.

Hosted smoke runs, disconnected terminals or unauthenticated sessions are classified `BLOCKED`, never PASS.

## R1 — D1 Extreme TP-Wajib lifecycle

Required evidence families:

- targetless D1TPW-managed order with hard SL and TP=0;
- D1TPW checkpoint exists for the exact ticket;
- restart produces exact-ticket `REC_NORMAL`, or fail-closed evidence if checkpoint identity is invalid;
- TP-Wajib completion latches the same ticket and the order subsequently appears in closed history;
- no duplicate execution identity across tickets;
- lifecycle freeze is a FAIL for the affected scenario unless the test intentionally validates fail-closed corruption handling.

## R2 — C044 lifecycle

Required scenarios:

- checkpoint + deterministic replay survives restart as `REC_NORMAL`;
- direction-side outer-BB test without valid same-direction Momentum closes by failed-momentum reason;
- valid Momentum after outer test enters WAIT_NEXT_REENTRY and does not close;
- later fresh same-direction Re-Entry creates a newer epoch and returns to WAIT_OUTER_TEST;
- mature opposite Extreme closes by cycle-superseded reason;
- M20 emergency close has precedence over normal C044 lifecycle close;
- any missing replay seed/history/cursor identity must fail closed/freeze, never guess.

## R3 — D1 owner / D1 Opportunity

Collect enough runtime observations to cover:

- D1 BUY confirmed;
- D1 SELL confirmed;
- D1 transition;
- D1 unresolved/fail-closed;
- D1O decision identity and dedup telemetry;
- tactical EXT_TPW remains distinct from normal strategic-owner-aligned families.

The analyzer may report `INCOMPLETE` until all four D1 owner states are observed. That is not a strategy defect by itself.

## R4 — timing and M17 structural SL

Timing evidence must show broker order open time strictly after the validation candle timestamp.

M17 evidence must cover BUY and SELL plus at least one JPY and one non-JPY pair. Runtime checks verify:

- BUY: no spread buffer is added to the structural SL;
- SELL: rounded spread buffer is at least `max(2 pips, ceil(raw spread pips))` and the final broker SL is not inside the structural SL;
- lifecycle-managed targetless orders retain TP=0;
- source-owned structural window remains StartCandle..ConfirmationCandle only.

## R5 — execution/risk controls

Scenario-indexed evidence is required for:

- TradeLock behavior for the configured mode;
- cumulative total-risk rejection at `MaxTotalRiskPercent`;
- P3 execution identity / recovery / duplicate controls;
- portfolio-limit and broker-result ambiguity handling where applicable.

A rejection marker alone is not enough to prove arithmetic or mode semantics; use `assertions.json` only to index exact raw evidence supporting a scenario.

## R6 — N2 identity/outcome chain

The same bundle set must contain:

- `[N1-NMJE]` journey observations;
- `[N2-NMJE-DEC]` validated decision shadows;
- `[N2-NMJE-OUT]` closed outcome shadows.

The existing N2 pipeline is reused for exact DecisionID/hash reconciliation and outcome attribution. Identity ambiguity is FAIL-closed.

## N3 firewall

N3 remains `execution_policy=NONE`. Runtime research cannot activate N3. The analyzer fails if unapproved `N3_POLICY_ACTIVE` or `N3_EXECUTION_POLICY` markers appear.

## Evidence status meanings

- `PASS`: required evidence for that case is positively demonstrated.
- `FAIL`: contradictory, unsafe, identity-invalid or explicitly failing evidence was observed.
- `INCOMPLETE`: authenticated runtime exists but the scenario has not produced enough evidence.
- `BLOCKED`: broker-authenticated runtime was not available; no runtime conclusion is made.

Do not reinterpret `INCOMPLETE` or `BLOCKED` as PASS.
