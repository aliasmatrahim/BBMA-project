# NMJE Dependency Hardening Audit — DEP-A01 M11 D1 Owner

Date: 2026-08-27
Status: **AUDIT COMPLETE / SOURCE PATCH DEFERRED WHILE RUNTIME CANDIDATE IS ACTIVE**
Scope: M11 D1 strategic-owner producer only, with downstream/NMJE interface observations where directly relevant.

## Baseline
- Canonical contract: `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`.
- Active source baseline inspected: `d1-owner-dev`, `blueprint/source/BBMA_EA.mq4`, Version 4.5.9.
- This audit is documentation-only and does not alter the running EA source.

## Verdict
**M11 is now materially implemented and the core owner formula matches the canonical D1 contract.**

The old contract text saying the EA has no dedicated M11 D1 owner is stale relative to the current source and must be reconciled later as documentation drift, not treated as a current code gap.

## Confirmed alignment

### A01-01 — Dedicated canonical owner exists — PASS
Current `PairState` contains `D1MajorTrendOwner d1_major_trend_owner`, and M11 exposes `UpdateD1MajorTrendOwner()` as the producer.

### A01-02 — Closed-D1 only — PASS
M11 rejects invalid/non-closed/non-D1 snapshots and resolves them to `D1_OWNER_UNRESOLVED`.

### A01-03 — BUY rule — PASS
Current implementation:
`Close1 > MA50_1 && MA50_1 > MA50_2` -> `D1_OWNER_BUY_CONFIRMED` / `DIR_BUY`.
This matches the canonical contract.

### A01-04 — SELL rule — PASS
Current implementation:
`Close1 < MA50_1 && MA50_1 < MA50_2` -> `D1_OWNER_SELL_CONFIRMED` / `DIR_SELL`.
This matches the canonical contract.

### A01-05 — Transition semantics — PASS
Any otherwise-valid closed-D1 state that is neither confirmed BUY nor confirmed SELL becomes `D1_TRANSITION` with `DIR_NONE`.
This correctly covers price/slope disagreement, flat MA50 and equality cases without inventing extra delay or score.

### A01-06 — Unresolved semantics — PASS
Missing/invalid required closed-D1 inputs resolve fail-closed to `D1_OWNER_UNRESOLVED` and `DIR_NONE`.

### A01-07 — Atomic direction handover semantics — PASS AT FORMULA LEVEL
The first later closed D1 snapshot satisfying the opposite confirmed formula replaces current owner direction directly. No fixed 2-day/3-day confirmation delay is added.

### A01-08 — Restart determinism — PASS AT FORMULA LEVEL
M11 recomputes the owner from closed D1 data rather than requiring last-known direction fallback. This is consistent with the canonical restart contract.

### A01-09 — Authority boundary — PASS
M11 produces strategic owner state only. D1 opportunity/lifecycle code is separate (`MODULE 11J`), and M11 itself does not execute orders or become a live-position close authority.

## Hardening findings

### DEP-A01-H1 — Closed-D1 snapshot atomicity for MA50_2 — VERIFY / HARDEN BEFORE N2->N3 PROMOTION
Priority: **HIGH FOR NMJE RELIABILITY, NOT A CURRENT FORMULA BUG**

Current M11 takes:
- `Close1` and `MA50_1` from the existing `state.d1_data` snapshot;
- `MA50_2` through a separate live `EMA(pair, PERIOD_D1, EMA50_PERIOD, state.d1_data.barIndex + 1)` read.

This is mathematically aligned, but the two MA50 observations are not visibly carried in one already-frozen D1 owner input snapshot. If broker history refreshes between owner input reads, a hybrid snapshot is theoretically possible.

Required hardening direction after runtime freeze:
- verify existing market-data snapshot/atomicity guarantees cover this call path; or
- freeze `MA50_2` together with the same closed-D1 snapshot/epoch used for `Close1` and `MA50_1`;
- do not add smoothing, delay, tolerance, score or a new BBMA rule.

Do not patch merely from this audit until the current runtime candidate/evidence attribution is released.

### DEP-A01-H2 — Stable owner identity metadata for NMJE — QUEUED FOR DEPENDENCY SCHEMA HARDENING
Priority: **HIGH FOR N2/N3 ATTRIBUTION**

Current owner already carries `SourceCandleTime`, state, direction, MA50 values and validity. For future NMJE lineage, add/derive a deterministic owner identity/epoch only if needed to distinguish owner cycles and prove supersession/replay.

Constraints:
- identity is engineering provenance only;
- no confidence score or freshness TTL;
- SourceCandleTime remains the canonical closed-D1 anchor;
- M11 remains the sole writer of underlying D1 owner state.

### DEP-A01-H3 — Documentation status drift — FIX DOCUMENTATION AFTER ACTIVE RUNTIME ATTRIBUTION IS PRESERVED
Priority: **MEDIUM / GOVERNANCE**

`M11_D1_MAJOR_TREND_OWNER_CONTRACT.md` still says implementation is pending and that active EA has no dedicated M11 owner. Current 4.5.9 source disproves that historical statement.

Required later synchronization:
- change contract implementation status to reflect implemented/current verification state;
- update Master Queue/CURRENT where they still list the pre-implementation M11 gap;
- preserve historical decision records instead of rewriting their chronology.

## Complexity limiter assessment
Current M11 `LEVEL: BEGINNER` is acceptable for the producer formula because the correct implementation is intentionally direct and deterministic. Safety criticality alone is not a reason to increase implementation complexity. If owner epoch/recovery schema later becomes materially stateful, reassess only that added state-management portion.

## No-fix findings
No evidence from this audit supports adding:
- extra D1 confirmation days;
- MA50 tolerance/pip buffers;
- scoring/weighted timeframe voting;
- RSI/MACD/ADX/volatility/session/news filters;
- H4 fallback when D1 is transition/unresolved;
- live-position close authority inside M11.

## Closure status
DEP-A01 M11 audit: **COMPLETE**.

Current disposition:
- core M11 formula/owner states: **PASS**;
- snapshot atomicity of `MA50_2`: **VERIFY/HARDEN LATER**;
- NMJE owner identity metadata: **QUEUE FOR N2/N3 DEPENDENCY SCHEMA**;
- stale documentation: **RECONCILE LATER**;
- EA source modification now: **NO — preserve active runtime candidate**.

## Next dependency audit
Proceed to **DEP-A02 — M12 Re-Entry owner/lifecycle hardening audit** against the latest source and canonical F3/F6/F7 decisions/contracts, documentation-only unless an explicit runtime-freeze release authorizes a source patch.
