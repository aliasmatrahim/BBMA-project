# NMJE V2 P4+ Current-Owner Rematerialization Audit — 2026-09-25

Status: **VALIDATED / P4-P8 + P10-P11 SHADOW REMATERIALIZATION COMPLETE / P5 TRUE-CONFLICT HOLD / P9 NO FIX**

## Base and identity
- Owner base: `d1-owner-dev@facb1d6c2adea4d8ec6eacfbf3b9e83e0a27cd95`.
- Historical Build 4.96 / PR #205 is provenance only; no historical source-bearing commit was merged, cherry-picked or transplanted.
- Candidate build: `5.13`.
- Build tag: `V513_NMJE_P4PLUS_SHADOW_20260925`.
- Final source revision: `NMJE_P4PLUS_SHADOW_006_20260925`.
- Final MQ4 SHA-256: `2D433B92452A4A062822594A6B3842F1FABB32EF5FDBA4F766AA4125999AA417`.
- Production EX4 SHA-256: `2D33DB5F1D1F51D5DB35E699D15F94D5560979BC5446BB8FD9288A4C70A5731E`.
- Accepted Strategy-Core delta: **NONE**.

## Rematerialized scope
- **P4 — durable base-journey attribution:** frozen only after canonical M16 validation; persisted by exact ticket/open-time/execution-hash identity; recovery absence/corruption is diagnostic only and cannot alter canonical trade recovery.
- **P5 — M5 true-conflict refinement:** **HOLD / NON-EXECUTABLE**. Current P3 owns only latest closed-M5 OHLC snapshot; it does not own M5 Re-Entry/Extreme semantic state. Therefore `M5SemanticResolved=false` and diagnostic relation remains fail-closed `UNRESOLVED`; no conflict invalidation is materialized.
- **P6 — journey maturity:** categorical observer metadata derived from already-owned journey/lifecycle state; no score/rank/reject/delay authority.
- **P7 — structural density:** presence/prefix/count fingerprint for already-valid candidates and frozen validated decisions; telemetry only, never a score or priority input.
- **P8 — provenance stability:** current relation and last-proven same-parent relation are kept separate; parent transitions clear inherited evidence. No time-delay/bar-count heuristic is used.
- **P9 — semantic SL/TP-source ownership:** **NO FIX**. Current M17/M22 source ownership remains authoritative; no NMJE change is required.
- **P10 — entry displacement:** measured only after successful fill from approved semantic SL/TP source -> preflight reference -> actual broker open. No threshold, rejection or execution modification.
- **P11 — strict-A lineage:** canonical `ParentEventID` is the lineage root; a changed canonical root is `NEW_JOURNEY`; unchanged root is `FIRST`; `CONTINUATION` is never inferred without a distinct source-owned continuation-event identity.

## Locked authority boundaries
- M15 remains the sole processing/final-decision clock.
- P2 ordering remains HOLD / non-executable.
- P3 remains latest-closed-M5 snapshot only.
- P4-P8/P10/P11 cannot create, reject, rank, validate, risk-approve or execute a trade.
- M5 has no execution authority.
- Risk/MM and M22 execution ownership are unchanged.
- Protected comparator, M16, risk, preflight and broker-call functions remain exact to the Build 5.12 owner base.
- Broker primitive counts remain `OrderSend=1 / OrderClose=3`.

## Validation
- `git diff --check`: **PASS**.
- Native MetaEditor final rev006 compile: **PASS — 0 errors / 0 warnings**.
- Tester-only adapter compile: **PASS — 0 errors / 0 warnings**.
- Targeted P4+ regression: **PASS**, including protected-function equality, no NMJE/M5 references in protected authority functions, P5 fail-closed semantics, P7 telemetry-before-priority without ranking writes, P8 identity-only stability, P10 post-fill ordering, P11 strict-A lineage and optional-hash normalization.
- Full repository Python suite: **72/72 PASS**. The first full-suite run exposed a Q10 tooling regression: the frozen Build 5.11 verifier incorrectly required current-owner MQ4 to remain byte-identical to the frozen candidate. The verifier now validates immutable `source_bearing_commit` + freeze-commit source identity, while current-owner source match is informational; Q10's frozen EX4/settings/hash acceptance remains unchanged and independently verified.
- Isolated Strategy Tester: GBPUSD M15, 2026-08-01 through 2026-09-01, final rev006 only.
- Natural execution coverage: **14 opens / 14 outcomes**.
- P4 durable persistence: **14/14 opens DUR=Y; 14/14 outcomes DLOAD=Y and DMATCH=Y**.
- P10 displacement: **14/14 opens and outcomes present**.
- P7 density telemetry rows: **1494**; P8 stability rows: **2016**.
- P5 M5 semantic state stayed unresolved on all **523** frozen validated-decision observations.
- P11 runtime classes observed: **FIRST, NEW_JOURNEY**; no inferred CONTINUATION.
- Fatal-runtime/persistence failures: **0**.
- Build 5.13 execution trace is exact to Build 5.12 baseline across all 14 executions.
- Tester report fields are exact to Build 5.12 baseline: 14 trades and identical profit/drawdown metrics. Performance is descriptive only, not optimization evidence.

## Evidence
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/evidence_manifest_rev006.json`
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/targeted_regression_result.json`
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/final_runtime_analysis_rev006.json`
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/runtime_rev006_key_rows.log`
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/SMOKE_REV006_202608.html`
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/native_compile_rev006.log`
- `blueprint/audits/evidence/NMJE_V2_P4PLUS_20260925/harness_compile_rev006.log`

## Exit decision
The authorized P4+ current-owner rematerialization is complete for executable-safe shadow scope. P4/P6/P7/P8/P10/P11 are validated observer/research metadata only; P5 true-conflict remains HOLD because current P3 has no source-owned M5 signal semantics; P9 requires no code change. No Strategy-Core, risk, validation or execution authority was added.
