# CORE-V2-F1 — Canonical MHV/MLV Lifecycle Implementation Audit

Date: 2026-08-22
Status: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**
Branch: `blueprint-dev`

## Scope
Implements the resolved `CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md` contract in M09 and executable REM ownership paths. F2 remains the Extreme maturity authority used for same-timeframe M15 parent provenance. F3 Type-1 and F4 H4 parent-owner semantics are not changed by this patch.

## Removed legacy divergence
- Removed the independent one-candle `DetectMHV()` path.
- Removed synthetic fixed-pip double-top/double-bottom candidate logic, generated neckline confirmation and `MaxWaitBars_MLV` strategy expiry.
- MHV and MLV now resolve from one canonical `MLVData` owner lifecycle; `SIGNAL_MHV` is only an alias export of that owner, while REM consumes the same canonical owner identity as `SIGNAL_MLV`.

## Implemented lifecycle
`REVERSAL-CONFIRMED SAME-TF EXTREME -> NORMAL TP-WAJIB COMPLETE -> POST-TP LOSS OF PRIOR MOMENTUM -> MOST-EXTREME BODY -> FIRST CLOSED MOVE AWAY -> FORMATION ESTABLISHED + BODY FROZEN -> OPTIONAL LATER BODY RETEST -> SAME-CYCLE eCSD/CSD DIRECTION TAKEOVER -> HISTORICAL PROVENANCE UNTIL OPPOSITE REVERSAL-CONFIRMED EXTREME SUPERSESSION`.

### Parent and TP provenance
- M15 BUY MHV uses a prior reversal-confirmed M15 SELL Extreme; M15 SELL MHV mirrors from a prior reversal-confirmed M15 BUY Extreme.
- RAW Extreme cannot parent MHV.
- TP-Wajib is structural market evidence, not broker-order state: prior SELL Extreme reaches current opposite MA5/MA10 Low area; prior BUY Extreme reaches current opposite MA5/MA10 High area.
- The TP-completion candle only records TP completion; the later loss-of-momentum structure must develop separately.

### Loss / formation / marked body
- Loss-of-momentum starts only inside the relevant outer BB without source-valid continuation CSM.
- One ordinary candle does not itself establish MHV: a provisional body is first accumulated, then a later closed move-away establishes formation.
- BUY/bottom MHV tracks lowest `min(Open,Close)` and establishes on first later `Close > PreviousClose`.
- SELL/top MHV tracks highest `max(Open,Close)` and establishes on first later `Close < PreviousClose`.
- Move-away trigger candle is excluded from body accumulation and the marked body freezes immediately at formation.

### Retest / direction progression
- Later BUY MHV retest completes on `Low <= FrozenMarkedBody`; SELL on `High >= FrozenMarkedBody`.
- Retest is not required merely for REM component maturity.
- Same-cycle eCSD/CSD on a later closed candle advances ownership to `MLV_DIRECTION_TAKEN`; it does not void completed MHV provenance.
- Once direction takes ownership, the MHV outer-BB/Momentum invalidation window is closed.

### Invalidation and supersession
- While loss/formation/retest is the active stage, relevant outer-BB continuation / prior-direction CSM has priority and resolves the setup to `MLV_VOID`.
- No generic candle/session/day TTL exists for canonical MHV validity.
- A later opposite-cycle RAW Extreme is candidate-only. It cannot erase the old MHV.
- Only the subsequent reversal-confirmation candle atomically installs the new M15 Extreme parent and resolves old MHV provenance to `MLV_SUPERSEDED`.
- Superseded/void MHV cannot satisfy new REM ownership.

## REM maturity contract
`IsCombinationMLVReady()` and M16 owner validation accept only canonical formation-established-or-later states with a frozen marked body and exact formation-candle identity. The exact REM signature remains `H4 Re-Entry + H1 Extreme + M15 MHV/MLV`.

## Static regression invariants
- no `DetectMHV()` or legacy `DetectMLV_State()` remains;
- no synthetic MHV neckline/double-top/double-bottom rule remains;
- no `MLV_CANDIDATE`, `MLV_CONFIRMED`, `MLV_EXPIRED` legacy state remains;
- no MHV `ExpiryCandleTime` strategy TTL remains;
- M15 F2 Extreme lifecycle owners exist for both directions;
- canonical BUY/SELL MHV lifecycle call sites and alias exports are unique;
- exact REM signature remains unchanged;
- full-source brace/parenthesis/bracket lexical sanity passes.

## Remaining verification
1. Native MetaEditor compile must report **0 errors / 0 warnings**.
2. Runtime traces should cover: parent RAW rejection; parent reversal confirmation; TP-Wajib completion; continued Momentum delaying loss state; loss-state invalidation; multi-candle body accumulation; move-away/freeze; formation export into REM; later retest; eCSD/CSD takeover; RAW supersession candidate without handover; reversal-confirmed atomic supersession; stale REM rejection after supersession.
3. F3/F4 implementation must preserve this canonical MHV owner and F2 provenance.

Decision provenance: `blueprint/decisions/CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md`.
