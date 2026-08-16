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
12. `blueprint/patches/0012-p0-step5-m14-combination-validation.patch`

## Full-source SHA verification status
The previously recorded SHA-256
`274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`
was discovered during Step 3D to have been calculated from a **partial reconstruction**, not the complete patch chain 0001–0007. It remains withdrawn as a full-working-source SHA.

Last previously verified exact full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0012 have focused structural/hunk verification records in their contracts. A new full-chain SHA must be generated only after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`
- `blueprint/contracts/M14_COMBINATION_VALIDATION_CONTRACT.md`
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

M10 precursor production for Type 3/4 is source-aligned by Step 3E.

## Step 3C — M06 BBMA MA producer source alignment
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

- MA5/10 High/Low are source-specific LWMA High/Low producers.
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

Step 3E provides a source-aligned CSM producer. However, the source rule that a later CSM invalidates an existing Extreme is temporal. M08 currently detects raw per-candle Extreme and does not own a persistent Extreme lifecycle. That later invalidation must be connected through the appropriate lifecycle/invalidation owner.

Contract: `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`.

## Step 3E — M10 CSM / CSD / eCSD source alignment
Status: **COMPLETED AT SIGNAL-PRODUCER CONTRACT LEVEL**

Primary source basis: `Oma ally BBMA - AL.pdf`, especially pages 2, 5 and 8. Secondary operational corroboration: `BBMA technique.pdf`, especially pages 18–19.

### Repaired — CSM
- Removed the unsourced rule requiring exactly three same-colour candles.
- Removed the unsourced `body > 70% of three-candle average body` test.
- CSM follows the supplied BBMA momentum law: directional candle close outside TOP/LOW BB in vertical/expanding BB context.
- Operational `BB vertical` encoding uses increasing BB width plus MID/outer BB movement in the momentum direction, with no arbitrary percentage threshold.

### Repaired — eCSD / CSD
- eCSD requires the closed candle to cross MA5/10 from open to close.
- CSD requires the candle to cross MA5/10 **and MID BB**.
- same-candle CSD-over-eCSD collector precedence is handled by Step 4.

Contract: `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`.

## Step 4 — M13 Combination Engine / collector contract
Status: **COMPLETED AT COLLECTOR / COMBINATION CONTRACT LEVEL**

Primary source basis: `Oma ally BBMA - AL.pdf`, pages 12–13.

### Source-locked project combinations
- REM = H4 Re-Entry + H1 Extreme + M15 confirmed MLV.
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

### Collector repair
- Removed all strategy detector/state-engine calls from M13.
- M27 orchestrates M08/M09/M10/M12 owner calls once and passes immutable per-cycle snapshots to M13.
- same-candle CSD suppresses eCSD as an independent collected confirmation.
- `ComponentIdentity` stores timeframe.
- `ComponentSet` stores `CombinationType` and `ComponentCount`.
- REM uses MLV `ConfirmationCandleTime`.
- M13 leaves `SLTPSource = SIGNAL_NONE`.
- M13 does not impose artificial component chronology.

Patches:
- `blueprint/patches/0010-p0-step4a-m13-combination-collector-source-alignment.patch`
- `blueprint/patches/0011-p0-step4b-m27-signal-owner-routing.patch`

Contract: `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`.

## Step 5 — M14 REM/RRE/REE validation contract
Status: **COMPLETED AT VALIDATE-ONLY CONTRACT LEVEL**

Primary source basis: `Oma ally BBMA - AL.pdf`, pages 12–13.

### Repaired
- Removed the unrelated legacy `Extreme -> MLV/MHV -> CSD` reversal signature.
- Removed the unrelated `CSD -> Re-Entry -> REM` continuation signature.
- Removed the unrelated `REE/RRE -> CSD -> Re-Entry` major-reversal signature.
- Removed universal strict chronology `Comp1 < Comp2 < Comp3`.
- M14 now validates the exact REM/RRE/REE component type + timeframe signatures created by M13.
- `ComponentCount == 3`, non-zero component identity and direction consistency are mandatory.
- `ValidatedSequenceCandidate.Components[0..2]` are now populated completely.
- `candidate.SequenceType` is the actual `SIGNAL_REM`, `SIGNAL_RRE`, or `SIGNAL_REE`.

### Ownership guard
M14 remains validate-only:
- `PriorityTier = TIER_NONE` because the supplied PDF does not define a REM/RRE/REE ranking policy;
- `SLTPSource = SIGNAL_NONE` because the combination pages do not define an M14-owned SL/TP source;
- no detector, lifecycle mutation, final entry selection, risk or execution authority is added.

### Temporal guard
M14 treats the combination as coexisting owner-valid snapshots in the current M15 processing cycle. It does not invent chronological ordering between D1/H4/H1/M15 candle times.

The current generic candidate-expiry construction downstream is **not certified** by Step 5. Owner-aware freshness/expiry remains an M15/M16 integration item.

Patch: `blueprint/patches/0012-p0-step5-m14-combination-validation.patch`.
Contract: `blueprint/contracts/M14_COMBINATION_VALIDATION_CONTRACT.md`.

### Verification
Focused post-Step4 patch verification passed:
- dry-run/apply clean;
- braces 488/488;
- parentheses 1457/1457;
- brackets 342/342;
- legacy strict chronology validator absent;
- exact REM/RRE/REE signature checks present;
- `candidate.Components[0..2]` populated.

No new full-chain working-source SHA is claimed from this focused verification.

## Next P0 action
**Step 6 — audit and repair M15 Final Signal Authority / atomic direction resolution.**

Priorities for Step 6:
1. stop M27 from running independent final authority once for BUY and once for SELL; M15 must see both directions before choosing a final outcome;
2. define safe M15 treatment of validated REM/RRE/REE now that M14 intentionally leaves `PriorityTier = TIER_NONE`;
3. enforce the locked Entry Mode contract: `RE_ENTRY_ONLY` versus `ALL_VALIDATED_BBMA_ENTRIES`;
4. repair candidate freshness/expiry so it is not derived from `Comp1` with a generic M15 multiplier;
5. use the now-populated `candidate.Components[]` consistently when creating the final decision;
6. keep raw detector validity from becoming execution authority;
7. leave SL/TP source resolution to the proper downstream contract rather than inventing it in M15.

After M15, continue to M16 conflict/invalidation integration, including temporal CSM invalidation of an existing Extreme.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
