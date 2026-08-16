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
10. `blueprint/patches/0010-p0-step4a-m13-combination-collector-source-alignment.patch`
11. `blueprint/patches/0011-p0-step4b-m27-signal-owner-routing.patch`

## Full-source SHA verification status
The previously recorded SHA-256
`274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`
was discovered during Step 3D to have been calculated from a **partial reconstruction**, not the complete patch chain 0001–0007. It remains withdrawn as a full-working-source SHA.

Last previously verified exact full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0011 have focused structural/hunk verification records in their contracts. A new full-chain SHA must be generated only after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`
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
- CSD-over-eCSD collector precedence is now handled by Step 4.
- temporal CSM invalidation of an already-existing Extreme remains an M08/M16 lifecycle integration item.

Patch: `blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`.
Contract: `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`.

## Step 4 — M13 Combination Engine / collector contract
Status: **COMPLETED AT COLLECTOR / COMBINATION CONTRACT LEVEL**

Primary source basis: `Oma ally BBMA - AL.pdf`, pages 12–13.

### Source-locked combinations for project timeframes
- REM = H4 Re-Entry + H1 Extreme + M15 confirmed MLV.
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

These are the D1/H4/H1/M15 rows supported by the project. M13 does not invent alternative components or substitute timeframes.

### Pure collector repair
- Removed all strategy detector/state-engine calls from M13.
- M27 now orchestrates M08/M09/M10/M12 owner calls once and passes immutable per-cycle snapshots to M13.
- `CollectSignalSnapshots()` copies owner outputs only.
- Same-candle CSD suppresses eCSD as an independent collected confirmation, preventing one candle from being double-counted.

### Combination identity
- `ComponentIdentity` now stores `Timeframe`.
- `ComponentSet` now stores `CombinationType` and `ComponentCount`.
- sequence hash identity now includes combination type and each component timeframe.
- REM uses MLV `ConfirmationCandleTime`, not candidate/start time.

### Ownership guard
M13 no longer chooses `SLTPSource`. Combination candidates leave `SLTPSource = SIGNAL_NONE`; later owning validation/SLTP architecture must resolve that separately.

### M27 routing correction
Numeric H1/H4/M15 BB snapshots are routed from frozen data even when optional BB-shape classification is disabled. This prevents disabling BB shape from accidentally zeroing the TOP/LOW BB values required by M08 Extreme detection.

### Temporal interpretation guard
The PDF describes REM/RRE/REE as three setups forming across three different timeframes. M13 assembles coexisting components and does **not** impose an artificial `Comp1 < Comp2 < Comp3` chronology. Direction consistency, coexistence/expiry windows and final validation belong downstream.

Patches:
- `blueprint/patches/0010-p0-step4a-m13-combination-collector-source-alignment.patch`
- `blueprint/patches/0011-p0-step4b-m27-signal-owner-routing.patch`

Contract: `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`.

### Verification
- 0010 and 0011 dry-run/apply sequentially: clean.
- sequential applied output exactly matches the generated Step 4 target in focused reconstruction.
- braces 489/489, parentheses 1454/1454, brackets 339/339.
- M13 strategy detector/state-mutator calls: 0.
- old `CollectAllSignals()` calls: 0.
- REM/RRE/REE each have explicit combination identity and timeframe-stamped components.

No new full-chain working-source SHA is claimed from this focused reconstruction.

## Next P0 action
**Step 5 — audit and repair M14 validation against the source-defined REM/RRE/REE combination contract.**

Priorities for Step 5:
1. remove the current unrelated reversal/continuation/major-reversal signatures that do not validate M13 REM/RRE/REE correctly;
2. validate `CombinationType`, exact component signature, three distinct expected timeframes and direction consistency;
3. replace the inappropriate strict chronological `Comp1 < Comp2 < Comp3` requirement with a source-compatible coexistence/expiry contract;
4. populate `ValidatedSequenceCandidate.Components[3]` completely because M15 consumes them;
5. keep M14 validate-only — no detection, lifecycle mutation, priority selection or execution authority.

After M14, continue to M15 final signal authority and atomic BUY/SELL resolution.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
