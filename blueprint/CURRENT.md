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
9. `blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`

## Full-source SHA verification status
The previously recorded SHA-256
`274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`
was discovered during Step 3D to have been calculated from a **partial reconstruction**, not the complete patch chain 0001–0007. It remains withdrawn as a full-working-source SHA.

Last previously verified exact full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0009 have focused structural/hunk verification records in their contracts. A new full-chain SHA must be generated only after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`
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
Status: **COMPLETED AT M12 CONTRACT LEVEL**

- Type 1 uses MA5/10 Low for BUY and MA5/10 High for SELL.
- Type 2 uses MA5/10 + MID BB collision with the documented minimum-candle operational encoding.
- Type 3 uses CSM as precursor then retrace to MA5/MA50.
- Type 4 uses CSD as precursor then retrace to MA5/10.
- Only confirmed Re-Entry may be exported downstream.

M10 precursor production for Type 3/4 is now source-aligned by Step 3E.

## Step 3C — M06 BBMA MA producer source alignment
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

- MA5/10 High/Low are now source-specific LWMA High/Low producers.
- EMA50 uses MT4 EMA applied to Close.
- Generic close SMA no longer produces BBMA MA5/10.
- previous-MA retrieval follows the same M06 producer and snapshot timeframe.

Contract: `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`.

## Step 3D — M08 Extreme source alignment
Status: **COMPLETED AT EXTREME SIGNAL CONTRACT LEVEL / TEMPORAL CSM INVALIDATION CONNECTION REMAINS**

- SELL Extreme uses MA5/10 High outside TOP BB.
- BUY Extreme uses MA5/10 Low outside LOW BB.
- relevant candle close outside the outer BB rejects/voids the current Extreme signal.
- non-source 10% proximity, MA5 slope and mandatory BB-state gates were removed.
- raw Extreme remains a signal, not standalone execution authority.

Step 3E now provides a source-aligned CSM producer. However, the source rule that a later CSM invalidates an existing Extreme is temporal. M08 currently detects raw per-candle Extreme and does not own a persistent Extreme lifecycle. That later invalidation must be connected through the appropriate lifecycle/invalidation owner rather than being falsely represented as solved by a same-candle check.

Contract: `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`.

## Step 3E — M10 CSM / CSD / eCSD source alignment
Status: **COMPLETED AT SIGNAL-PRODUCER CONTRACT LEVEL**

Primary source basis: `Oma ally BBMA - AL.pdf`, especially pages 2, 5 and 8. Secondary operational corroboration: `BBMA technique.pdf`, especially pages 18–19.

### Repaired — CSM
- Removed the unsourced rule requiring exactly three same-colour candles.
- Removed the unsourced `body > 70% of three-candle average body` test.
- CSM now follows the supplied BBMA momentum law: directional candle close outside TOP/LOW BB in vertical/expanding BB context.
- Operational `BB vertical` encoding uses increasing BB width plus MID/outer BB movement in the momentum direction, with no arbitrary percentage threshold.

### Repaired — eCSD
- eCSD no longer means merely `close already beyond MA5/10`.
- It now requires the closed candle to cross MA5/10 from open to close.
- BUY uses the directional High MA pair; SELL uses the directional Low MA pair as an explicitly documented implementation interpretation.

### Repaired — CSD
- CSD now requires the candle to cross MA5/10 **and MID BB**.
- MID BB crossing remains the distinction showing stronger/real directional intent.

### Explicit implementation interpretation
The source says `crosses` but does not specify wick-vs-body coding semantics. Step 3E encodes a cross as the **closed candle body** spanning the level from open to close; wick-only touches do not count.

The source phrase `BB vertical` is encoded deterministically as widening BB plus MID/relevant outer band moving in the momentum direction. This is engineering translation, not claimed verbatim source wording.

### Downstream consequences
- M12 Type 3 now consumes source-aligned CSM.
- M12 Type 4 now consumes source-aligned CSD.
- M13 must later resolve collector precedence so a full CSD candle is not incorrectly double-counted as a separate eCSD confirmation merely because it also crosses MA5/10.
- temporal CSM invalidation of an already-existing Extreme remains an M08/M16 lifecycle integration item.

Patch: `blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`.
Contract: `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`.

### Verification
Focused patch dry-run and apply passed with exact output match. Structural delimiters remain balanced in the focused reconstruction. The old three-candle/70%-body CSM formula is absent.

## Next P0 action
**Step 4 — audit and source-align M13 Combination Engine / collector contract before M14.**

Priorities for Step 4:
1. make M13 a true collector only;
2. enforce CSD-over-eCSD collector precedence on the same candle;
3. build REM/RRE/REE only from source-valid immutable components;
4. reconcile M13 component/timeframe construction against the PDF before M14 sequence validation;
5. do not allow raw detector validity to become execution authority.

After M13, continue to M14 sequence repair and then M15 final entry authority.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
