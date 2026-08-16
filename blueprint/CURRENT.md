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
8. `blueprint/patches/0008-p0-step3d-m08-extreme-source-alignment.patch`

## Full-source SHA verification status
The previously recorded SHA-256
`274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`
was discovered during Step 3D to have been calculated from a **partial reconstruction**, not the complete patch chain 0001–0007. It is therefore **withdrawn as a full-working-source SHA**.

Last previously verified exact full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0008 have focused structural/hunk verification records in their contracts. A new full-chain SHA must be generated only after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

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

M07 remains the BB-shape classifier. After later source alignment in Step 3D, BB shape is auxiliary Extreme context/classification and is no longer a universal gate for whether an Extreme signal exists.

## Step 2 — M09 MLV persistence/lifecycle
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

`PairState` owns independent persistent BUY/SELL MLV slots; M09 owns lifecycle mutation; M13 consumes snapshots; M27 routes state; confirmed chronology and expiry are explicit.

## Step 3 — M12 Re-Entry persistence/lifecycle
Status: **COMPLETED AT STATE-OWNERSHIP LEVEL**

Patch 0005 established persistent H1/H4/D1 × BUY/SELL Re-Entry state, M12 as sole lifecycle owner, M13 as snapshot consumer, M27 as lifecycle router, timeframe-aware expiry, and confirmed-only Re-Entry export.

## Step 3B — M12 Re-Entry BBMA source alignment
Status: **COMPLETED AT M12 CONTRACT LEVEL / M10 DEPENDENCY REMAINS**

- Type 1 uses MA5/10 Low for BUY and MA5/10 High for SELL.
- Type 2 uses MA5/10 + MID BB collision with the documented minimum-candle operational encoding.
- Type 3 uses CSM as precursor then retrace to MA5/MA50.
- Type 4 uses CSD as precursor then retrace to MA5/10.
- Only confirmed Re-Entry may be exported downstream.

M10 CSM/CSD source alignment remains required for Type 3/4 trust.

## Step 3C — M06 BBMA MA producer source alignment
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

- MA5/10 High/Low are now source-specific LWMA High/Low producers.
- EMA50 uses MT4 EMA applied to Close.
- Generic close SMA no longer produces BBMA MA5/10.
- previous-MA retrieval follows the same M06 producer and snapshot timeframe.

Contract: `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`.

## Step 3D — M08 Extreme source alignment
Status: **COMPLETED AT EXTREME SIGNAL CONTRACT LEVEL / M10 CSM INVALIDATION DEPENDENCY REMAINS**

Primary source basis: `Oma ally BBMA - AL.pdf`, pages 5–6. Secondary corroboration: `BBMA technique.pdf`, page 28.

### Repaired
- SELL Extreme now uses MA5/10 High outside TOP BB.
- BUY Extreme now uses MA5/10 Low outside LOW BB.
- Supports the source wording that MA5 alone or MA5/10 may be outside the relevant BB.
- A relevant candle close outside the outer BB rejects/voids the Extreme signal.
- Removed the non-source 10% outer-BB proximity gate.
- Removed the non-source MA5 slope/previous-MA gate.
- Removed mandatory `BB_EXPANDING || BB_SQUEEZE` as a universal Extreme prerequisite.
- BB shape remains auxiliary classification context only.

### Signal vs entry guard
`DetectExtreme()` now represents a BBMA **signal**, not automatic execution authority.

The source additionally requires reversal-candle confirmation and identifies the retest candle as the standalone Extreme point of entry. The supplied references do not define a sufficiently deterministic universal reversal-candle algorithm to encode without interpretation, so Step 3D does not invent one.

This is consistent with the locked Entry Mode contract: raw detector validity alone is not enough to execute a trade.

### Remaining dependency
The primary source says Extreme becomes invalid in the presence of CSM. M08 does not own CSM; M10 does. Because M10 is still unaudited, Step 3D does not hard-wire an unaudited CSM producer into M08. This source rule must be connected after M10 source alignment.

Patch: `blueprint/patches/0008-p0-step3d-m08-extreme-source-alignment.patch`.
Contract: `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`.

## Next P0 action
**Step 3E — audit and source-align M10 CSM / CSD / eCSD.**

This is now the next blocker because:
1. M12 Type 3 depends on CSM;
2. M12 Type 4 depends on CSD;
3. M08 Extreme invalidation depends on CSM;
4. M13 must not consume incorrect precursor signals when REM/RRE/REE are repaired.

After M10, continue to M13/M14 combination/sequence repair.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
