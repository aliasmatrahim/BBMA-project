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
15. `blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`
16. `blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`
17. `blueprint/patches/0017-p0-step9-m18-label-only-scoring-authority.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` was discovered during Step 3D to have been calculated from a partial reconstruction and remains withdrawn.

Last exact verified full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0017 currently have focused patch/contract verification only. A new full-chain SHA must only be claimed after exact materialization of the complete ordered patch chain.

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
- `blueprint/contracts/M17_ENTRY_SLTP_CONTRACT.md`
- `blueprint/contracts/M17_SLTP_EXIT_RESOLUTION_CONTRACT.md`
- `blueprint/contracts/M18_SIGNAL_SCORING_LABEL_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Steps 1–3E — BBMA source alignment foundations
Status: **COMPLETED AT THEIR LOCKED CONTRACT LEVELS**

- M07 BB-shape ownership repaired.
- M09 MLV persistence/lifecycle repaired.
- M12 Re-Entry persistence and Type 1–4 source alignment repaired.
- M06 MA5/10 High/Low producer corrected to BBMA LWMA High/Low semantics.
- M08 Extreme source contract repaired.
- M10 CSM/CSD/eCSD source contracts repaired.

## Step 4 — M13 Combination Engine
Status: **COMPLETED AT COLLECTOR / COMBINATION CONTRACT LEVEL**

Source-locked project rows:
- REM = H4 Re-Entry + H1 Extreme + M15 confirmed MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M13 is collector/assembler only.

## Step 5 — M14 Validation
Status: **COMPLETED AT VALIDATE-ONLY CONTRACT LEVEL**

M14 validates exact REM/RRE/REE identity, timeframe and direction; populates component payload; no invented chronology, priority or SL/TP source.

## Step 6 — M15 Final Signal Authority
Status: **COMPLETED AT FINAL-AUTHORITY CONTRACT LEVEL**

- `EntryMode 1 = RE_ENTRY_ONLY` -> confirmed H1 Re-Entry only.
- `EntryMode 2 = ALL_VALIDATED_BBMA_ENTRIES` -> confirmed H1 Re-Entry + validated REM/RRE/REE.
- raw Extreme/MLV/CSD/eCSD/CSM cannot directly execute.
- BUY and SELL are resolved atomically; unresolved opposite validated directions -> no trade.
- no arbitrary REM/RRE/REE quality ranking.

## Step 7 — M16 Conflict / Invalidation
Status: **COMPLETED AT CONFLICT / INVALIDATION CONTRACT LEVEL**

- decision components are revalidated against their real owner state;
- generic M15-based expiry assumptions removed;
- persistent H1/H4 Extreme validity overlay added;
- later same-timeframe source-valid CSM invalidates stored Extreme;
- M16 remains invalidation-only.

## Step 8 — M17 Entry / SL / TP engineering guard
Status: **COMPLETED AT ENGINEERING GUARD LEVEL**

- BUY execution reference uses ASK; SELL uses BID.
- direction-aware geometry enforced: BUY `SL < Entry < TP`, SELL `TP < Entry < SL`.
- MaxSL conversion uses the project pip-price helper; `MaxSLPips` is a rejection cap only.
- `MinRRRatio` is a rejection filter only and does not manufacture TP.
- StopLevel/FreezeLevel are direction-aware.
- unresolved source payload fails closed with `REJ_SLTP_UNRESOLVED`.

Patch:
`blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

## Step 8B — BBMA SL / TP / Exit source resolution
Status: **APPROVED AT ARCHITECTURE CONTRACT LEVEL**

Provenance remains separated into:
- `PDF_CORE`;
- `FORUM_SUPPORTED`;
- `EA_SAFETY`.

Approved TP mapping:
- H1 Re-Entry BUY -> H1 TOP BB; SELL -> H1 LOW BB;
- REM BUY -> H4 TOP BB; SELL -> H4 LOW BB;
- RRE BUY -> D1 TOP BB; SELL -> D1 LOW BB;
- REE BUY -> D1 TOP BB; SELL -> D1 LOW BB.

No universal fixed-pip TP/SL is accepted as BBMA Core.

## Step 8C — approved M17 source resolver
Status: **COMPLETED AT ACTIVE-BLUEPRINT PATCH LEVEL**

Implemented by:
`blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`

Patch commit:
`2afeee76806f4b1c4e56f829fd7c8d42403a1450`

Contract updates:
- `blueprint/contracts/M17_ENTRY_SLTP_CONTRACT.md` — commit `ce785c942eddcd3f6c3b131b6e961411ddde60e7`;
- `blueprint/contracts/M17_SLTP_EXIT_RESOLUTION_CONTRACT.md` — commit `89e56feede6a8f268ce9cbb65e09fa9a492fd533`.

Step 8C behavior:
- final decision now preserves the exact destination-producing Re-Entry component;
- H1/H4/D1 mapping is enforced for RE_ENTRY/REM/RRE/REE respectively;
- source candle must resolve exactly and be closed (`shift >= 1`);
- TP is read from the approved source-timeframe TOP/LOW BB;
- hard SL uses the exact source-candle wick plus one broker point as explicit `EA_SAFETY` protection;
- crossed/stale/missing/invalid source data fails closed with `REJ_SLTP_UNRESOLVED`;
- fixed-pip or RR-derived fallback is not introduced;
- opposite-CSM dynamic broker close remains disabled pending downstream lifecycle audit.

## Step 9 — M18 Signal Scoring / Label Authority
Status: **COMPLETED AT ACTIVE-BLUEPRINT PATCH + CONTRACT LEVEL**

Baseline finding:
- M18 was labelled `LABEL ONLY` but used arbitrary numeric weights;
- it awarded unconditional `BBShape:10` and `MultiTF:5` points;
- the weights were not established BBMA/Oma Ally source rules;
- the pre-Step6 orchestration scored raw `extreme/mlv/reEntry` snapshots instead of the atomic final M15 decision.

Step 6 had already removed M18 scoring from the active final-authority path. Step 9 now makes the M18 implementation itself match that architecture.

Implemented by:
`blueprint/patches/0017-p0-step9-m18-label-only-scoring-authority.patch`

Patch commit:
`de3db83c82aeb8371b4c06e8c11ae58dcd982362`

Contract:
`blueprint/contracts/M18_SIGNAL_SCORING_LABEL_CONTRACT.md`

Contract commit:
`1009901feffe507fe71d11761832a23fba933bef`

Locked M18 behavior:
- optional observability/display metadata only;
- `Score = 0`, `Level = LEVEL_NONE` for current execution architecture;
- no REM/RRE/REE or signal-type quality ranking;
- no effect on M15 direction/entry authority;
- no effect on M16 invalidation;
- no effect on M17 Entry/SL/TP payload;
- no effect on lot sizing, risk approval, portfolio checks or execution;
- `SignalMode`, `ScoreDisplayThresholdManual` and `EnableSignalScoring` cannot act as hidden trading filters.

### Verification boundary
The original M18 baseline was checked directly from the archived `Master Blueprint 2.0.txt`. The only old score-field writer was the M18 helper itself, and the only active orchestration scoring call was already removed by Step 6. Step 9 removes the unsupported weights and raw-signal mutation path.

No new full-chain working-source SHA is claimed until the complete patch chain is exactly materialized and compiled.

## Next P0 action
**Step 10 — audit M19 Risk Engine as a filter-only module.**

Required focus:
1. M19 may reject a fully formed M15–M17 decision but must not recreate strategy direction or SL/TP;
2. verify spread, drawdown, basket-loss and total-risk calculations use coherent account/EA ownership and units;
3. verify decision rejection reason maps to the actual failed risk rule rather than collapsing all failures into `REJ_TOTAL_RISK`;
4. verify risk snapshot timing and live-order accounting do not violate the closed-candle strategy clock while still using live broker/account state where required;
5. verify M19 does not consume M18 score/level/SignalMode as a trading filter.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
