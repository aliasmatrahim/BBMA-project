# BBMA Master Blueprint Development Status

## Current branch
`blueprint-dev`

## Source of truth
GitHub `aliasmatrahim/BBMA-project` is authoritative for the active Master Blueprint. Notion is supporting documentation only.

BBMA strategy semantics are governed by the user-supplied references indexed under `docs/references/`. If active blueprint logic conflicts with a supported BBMA source rule, blueprint/code must be repaired rather than the source being reinterpreted to fit the code.

## Immutable baseline
Source: `Master Blueprint 2.0.txt`

Verified baseline SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

The exact baseline is stored as deterministic gzip+base64 chunks under `blueprint/archive/`.

## Current revision — ordered patch chain
1. `blueprint/patches/0001-fix-m25-complexity-limiter.patch`
2. `blueprint/patches/0002-p0-step1-bbshape-extreme-contract.patch`
3. `blueprint/patches/0003-p0-step2-mlv-persistence-lifecycle.patch`
4. `blueprint/patches/0004-p0-step2b-mlv-void-transition-contract.patch`
5. `blueprint/patches/0005-p0-step3-reentry-persistence-lifecycle.patch`
6. `blueprint/patches/0006-p0-step3b-reentry-source-alignment.patch`
7. `blueprint/patches/0007-p0-step3c-m06-ma-source-alignment.patch`
8. `blueprint/patches/0008-p0-step3d-m08-extreme-source-alignment.patch`
9. `blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`
10. `blueprint/patches/0010-p0-step4a-m13-combination-collector-source-alignment.patch`
11. `blueprint/patches/0011-p0-step4b-m27-signal-owner-routing.patch`
12. `blueprint/patches/0012-p0-step5-m14-combination-validation.patch`
13. `blueprint/patches/0013-p0-step6-m15-final-authority-atomic-entry-mode.patch`
14. `blueprint/patches/0014-p0-step7-m16-owner-aware-invalidation.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` was discovered during Step 3D to have been calculated from a partial reconstruction and remains withdrawn.

Last previously verified exact full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0014 have focused verification records in their contracts. A new full-chain SHA must only be claimed after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`
- `blueprint/contracts/M14_COMBINATION_VALIDATION_CONTRACT.md`
- `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`
- `blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Step 1 — BB Shape → Extreme contract
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

M07 owns BB-shape classification; BB shape is auxiliary Extreme context and no fabricated state is substituted when classification is disabled.

## Step 2 — M09 MLV persistence/lifecycle
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

Persistent BUY/SELL MLV slots, M09 lifecycle ownership, confirmed chronology/expiry and downstream immutable snapshots are established.

## Step 3 / 3B — M12 Re-Entry persistence + BBMA source alignment
Status: **COMPLETED AT M12 CONTRACT LEVEL**

Persistent H1/H4/D1 x BUY/SELL state is established. Type 1–4 contracts are source-aligned; only confirmed Re-Entry may be exported downstream.

## Step 3C — M06 MA producer source alignment
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

MA5/10 High/Low use source-specific LWMA High/Low production; EMA50 uses EMA Close.

## Step 3D — M08 Extreme source alignment
Status: **COMPLETED AT RAW EXTREME SIGNAL CONTRACT LEVEL; TEMPORAL VALIDITY NOW CONNECTED BY STEP 7**

BUY/SELL MA-side mapping, outer-BB rule and VOID-on-close-outside behavior are source-aligned. Raw Extreme is not standalone execution authority. Step 7 now supplies the persistent validity overlay and later-CSM invalidation path while M08 remains the detector.

## Step 3E — M10 CSM / CSD / eCSD source alignment
Status: **COMPLETED AT SIGNAL-PRODUCER CONTRACT LEVEL**

Legacy unsourced CSM formula was removed; CSM follows directional outer-BB momentum context. eCSD and CSD use source-aligned crossing contracts; same-candle CSD-over-eCSD precedence is handled by M13.

## Step 4 — M13 Combination Engine / collector contract
Status: **COMPLETED AT COLLECTOR / COMBINATION CONTRACT LEVEL**

Source-locked project rows:
- REM = H4 Re-Entry + H1 Extreme + M15 confirmed MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M13 is collector/assembler only and does not detect, mutate lifecycle, rank or choose SL/TP.

## Step 5 — M14 REM/RRE/REE validation
Status: **COMPLETED AT VALIDATE-ONLY CONTRACT LEVEL**

M14 validates exact combination identity/type/timeframe/direction, populates validated component identity, removes unrelated legacy sequence signatures and does not invent strict chronology, priority tier or SL/TP source.

## Step 6 — M15 Final Signal Authority / Entry Mode / atomic direction
Status: **COMPLETED AT FINAL-AUTHORITY CONTRACT LEVEL**

- `EntryMode 1 = RE_ENTRY_ONLY` -> confirmed H1 Re-Entry only.
- `EntryMode 2 = ALL_VALIDATED_BBMA_ENTRIES` -> confirmed H1 Re-Entry + validated REM/RRE/REE.
- raw Extreme/MLV/CSD/eCSD/CSM cannot directly execute.
- BUY and SELL candidates are pooled before one atomic M15 pass.
- simultaneous eligible BUY and SELL -> no created trade decision; no arbitrary winner.
- `SignalMode` quality-tier gating is removed from M15 authority.
- no REM/RRE/REE superiority ranking is invented.

Patch: `blueprint/patches/0013-p0-step6-m15-final-authority-atomic-entry-mode.patch`.
Contract: `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`.

## Step 7 — M16 conflict / invalidation / owner-aware freshness
Status: **COMPLETED AT CONFLICT / INVALIDATION CONTRACT LEVEL**

Primary BBMA source rule connected in this step: an Extreme is no longer valid in the presence of CSM.

### Persistent Extreme validity overlay
M08 remains the raw detector. M16 now owns H1/H4 x BUY/SELL persistent Extreme validity snapshots for temporal invalidation/expiry:
- `extreme_h1_buy_state`;
- `extreme_h1_sell_state`;
- `extreme_h4_buy_state`;
- `extreme_h4_sell_state`.

A later source-valid CLOSED CSM on the same timeframe invalidates the stored Extreme. The source does not qualify this invalidation by CSM direction, so Step 7 does not invent a same-direction requirement. This same-timeframe/later-candle mapping is explicitly an engineering translation of the source sentence.

### Owner-aware decision validation
M15 now forwards explicit selected component identity into `BBMA_Decision` through `ComponentCount`, `Components[3]` and explicit `CandidateExpiry` when an owner supplies it.

M16 checks every selected component against its actual owner state before allowing `DEC_VALIDATED`:
- Re-Entry -> matching M12 H1/H4/D1 + direction slot, confirmed/valid/same confirmation candle/not expired;
- MLV -> matching M09 M15 + direction slot, confirmed/valid/same confirmation candle/not expired;
- Extreme -> matching M16 H1/H4 + direction persistent validity slot, same identity/not expired/not invalidated by later CSM.

If any required component is no longer owner-valid, the assembled decision cannot proceed.

### Legacy generic expiry removed
M16 no longer uses:
- `decision.CandleTime + MaxWaitBars_Global * 900`;
- `decision.CycleStartTime + MaxWaitBars_Global * 900`.

Legacy generic Signal/MLV/Re-Entry expiry helpers are removed from the active M16 path. Expiry and strategy invalidation are treated separately.

### Ownership cleanup
- broker initialization rejection removed from M16 because broker readiness is not strategy invalidation ownership;
- unresolved opposite direction remains no-trade; M16 never invents a winner;
- M16 remains conflict/invalidation-only and does not own SL/TP, risk, priority or execution.

Patch:
`blueprint/patches/0014-p0-step7-m16-owner-aware-invalidation.patch`

Contract:
`blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md`

Focused patch SHA-256:
`d333b64594eb563c3013776e36d3ab967041be471f7b45206fb73d466adc034a`

### Focused verification
- dry-run/apply clean and exact generated target match;
- braces 502/502;
- parentheses 1538/1538;
- brackets 353/353;
- old generic decision/cycle expiry formulas absent;
- owner snapshot validator present;
- persistent H1/H4 Extreme validity overlay present;
- temporal later-CSM invalidation present;
- explicit pairIndex routing into M16 present.

No new full-chain working-source SHA is claimed from this focused verification.

## Next P0 action
**Step 8 — M17 entry / SL / TP contract and direction-aware validation.**

Priorities:
1. resolve where `EntryPrice`, `StopLoss`, `TakeProfit` and `StopLossPoints` are actually built for each final eligible entry type;
2. replace absolute-distance-only validation with direction-aware BUY/SELL SL/TP geometry;
3. correct MaxSL pip/point conversion;
4. make StopLevel/FreezeLevel validation execution-side aware rather than always using BID;
5. preserve BBMA-source SL/TP semantics where explicitly stated; if the PDF does not specify a deterministic rule for an entry type, mark it unresolved rather than inventing one;
6. keep M17 validation/resolution separate from risk sizing and order execution.

After M17, continue to scoring/risk/portfolio/execution blockers in dependency order.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
