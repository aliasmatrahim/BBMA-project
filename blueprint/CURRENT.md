# BBMA Master Blueprint Development Status

## Current branch
`blueprint-dev`

## Source of truth
GitHub `aliasmatrahim/BBMA-project` is authoritative for the active Master Blueprint. Notion is supporting documentation only.

BBMA strategy semantics are governed by the user-supplied source references indexed under `docs/references/`. If active blueprint logic conflicts with a supported BBMA source rule, the blueprint/code must be repaired rather than the source being reinterpreted to fit the code.

## Immutable baseline
Source: `Master Blueprint 2.0.txt`

Verified baseline SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

The exact baseline is stored as deterministic gzip+base64 chunks under `blueprint/archive/`.

## Current revision
Apply patches in order:

1. `blueprint/patches/0001-fix-m25-complexity-limiter.patch`
2. `blueprint/patches/0002-p0-step1-bbshape-extreme-contract.patch`
3. `blueprint/patches/0003-p0-step2-mlv-persistence-lifecycle.patch`
4. `blueprint/patches/0004-p0-step2b-mlv-void-transition-contract.patch`
5. `blueprint/patches/0005-p0-step3-reentry-persistence-lifecycle.patch`
6. `blueprint/patches/0006-p0-step3b-reentry-source-alignment.patch`
7. `blueprint/patches/0007-p0-step3c-m06-ma-source-alignment.patch`

Reconstructed working-source SHA-256 after patches 0001–0007:
`274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy is LOCKED for the current blueprint-development cycle.

- M01 BEGINNER
- M02 BEGINNER
- M03 INTERMEDIATE
- M04 INTERMEDIATE
- M05 INTERMEDIATE
- M06 INTERMEDIATE
- M07 INTERMEDIATE
- M08 INTERMEDIATE
- M09 INTERMEDIATE+
- M10 INTERMEDIATE
- M11 BEGINNER
- M12 INTERMEDIATE+
- M13 INTERMEDIATE+
- M14 EXPERT-RESTRICTED
- M15 EXPERT-RESTRICTED
- M16 EXPERT-RESTRICTED
- M17 INTERMEDIATE
- M18 INTERMEDIATE
- M19 EXPERT-RESTRICTED
- M20 EXPERT-RESTRICTED
- M21 INTERMEDIATE+
- M22 EXPERT
- M23 EXPERT-RESTRICTED
- M24 EXPERT
- M25 BEGINNER
- M26 INTERMEDIATE
- M27 EXPERT-RESTRICTED

# P0 Architecture Repair

## Step 1 — BB Shape → Extreme contract
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

- M06 supplies frozen closed-candle market data.
- M07 solely classifies BB shape/state.
- M08 consumes classified BB state.
- M13 remains collect-only for this contract.
- M27 remains orchestrator-only for this contract.

## Step 2 — M09 MLV persistence/lifecycle
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

- `PairState` owns independent persistent BUY/SELL MLV slots.
- M09 solely mutates MLV lifecycle.
- M27 selects the correct state slot and passes a cycle snapshot downstream.
- M13 no longer mutates MLV lifecycle.
- Lifecycle: `NONE → CANDIDATE → CONFIRMED → EXPIRED`, plus explicit `VOID` invalidation interface.
- Sequence chronology uses the MLV confirmation candle.

## Step 3 — M12 Re-Entry persistence/lifecycle
Status: **COMPLETED AT STATE-OWNERSHIP LEVEL**

Patch 0005 established persistent H1/H4/D1 × BUY/SELL Re-Entry state, M12 as sole lifecycle owner, M13 as snapshot consumer, M27 as lifecycle router, timeframe-aware expiry, and confirmed-only Re-Entry export.

## Step 3B — M12 Re-Entry BBMA source alignment
Status: **COMPLETED AT M12 CONTRACT LEVEL / UPSTREAM DEPENDENCIES REMAIN**

Source-aligned repairs:
- Type 1 uses MA5/10 Low for BUY and MA5/10 High for SELL rather than the old EMA50-near/cross shortcut.
- Type 2 uses MA5/10 + MID BB collision; MA50 confluence marks the strongest form; persistent state represents the minimum 3-candle contract.
- Type 3 uses CSM as precursor and requires a later retrace to MA5/MA50.
- Type 4 uses CSD as precursor and requires a later retrace to the relevant MA5/10 cluster.
- only confirmed Re-Entry may be exported downstream.

Operational interpretation remains explicitly documented in `M12_REENTRY_SOURCE_CONTRACT.md`; source gaps are not presented as verbatim Oma Ally rules.

## Step 3C — M06 BBMA MA producer source alignment
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

Source basis:
- primary reference page 1 distinguishes MA5 High, MA10 High, MA5 Low, MA10 Low and Exponential MA50;
- secondary MT4 setup diagrams on pages 11–14 show MA5/10 as Linear Weighted applied to High/Low and MA50 as Exponential applied to Close.

### Repaired
- Removed the incorrect use of close-price `SMA()` as producer for all four MA5/10 lines.
- Added M06 source-specific `BBMAHighMA()` using `MODE_LWMA + PRICE_HIGH`.
- Added M06 source-specific `BBMALowMA()` using `MODE_LWMA + PRICE_LOW`.
- `CalculateAllMA()` now produces distinct source-correct High/Low MA5/10 values.
- Replaced the custom reverse-chronology EMA recurrence with MT4 `iMA(... MODE_EMA, PRICE_CLOSE ...)`.
- `GetDataForTimeframe()` reuses the same frozen EMA50 value instead of recomputing it separately.
- Existing previous-candle MA5 lookups now use M06 High/Low helpers rather than close-price SMA.
- Removed an existing hardcoded `PERIOD_H1` from previous-MA retrieval; the lookup now follows `data.timeframe`.

### Verification
- Patch 0007 dry-runs and applies cleanly to the reconstructed post-Step3B source.
- Applied output exactly matches the generated Step3C working source.
- braces 508/508, parentheses 1473/1473, brackets 330/330.
- remaining `SMA(...MA5/10...)` bypass calls: 0.
- working-source SHA-256 after 0007: `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`.

### Scope guard / newly exposed downstream blocker
Step 3C does not change strategy meaning in M08/M09/M10. After the producer repair, an existing M08 Extreme consumer mismatch remains visible: the active consumer path maps BUY to MA5 High and SELL to MA5 Low. The BBMA source-side law associates BUY with the Low MA side and SELL with the High MA side. This must be reconciled in M08 itself rather than hidden inside M06.

M10 CSM/CSD/eCSD source alignment also remains required because M12 Type 3/4 depends on M10-owned precursor signals.

## Next P0 action
**Step 3D — audit and source-align M08 Extreme direction/MA contract before trusting Extreme as an M13 combination component.**

After M08, audit M10 CSM/CSD/eCSD source alignment, then continue to M13/M14 combination/sequence repair.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
