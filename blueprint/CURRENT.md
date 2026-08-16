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

Last fully verified full working-source SHA-256 through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patch 0006 was structural/dry-run verified against the reconstructed post-0005 M12 state. A refreshed full-source SHA will be recorded when the materialized current working source is generated.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
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

Patch 0005 established:
- persistent H1/H4/D1 × BUY/SELL Re-Entry slots in `PairState`;
- M12 as sole Re-Entry lifecycle mutation owner;
- M13 as Re-Entry snapshot consumer;
- M27 as lifecycle router/orchestrator;
- timeframe-aware expiry;
- confirmed-only Re-Entry export downstream.

## Step 3B — M12 Re-Entry BBMA source alignment
Status: **COMPLETED AT M12 CONTRACT LEVEL / UPSTREAM DEPENDENCIES REMAIN**

Primary source basis: `Oma ally BBMA - AL.pdf`, especially pages 9–10. Secondary corroboration: `BBMA technique.pdf`, especially the BUY-on-MA5/10-Low / SELL-on-MA5/10-High law.

### Source-aligned repairs
- **Type 1:** removed the old EMA50-near + EMA50-cross logic. Type 1 now uses the relevant MA5/10 entry cluster: BUY on MA5/10 Low support context, SELL on MA5/10 High resistance context.
- **Type 2:** removed the old BB-width / close-outside-BB detector. Candidate now comes from MA5/10 + MID BB collision; MA50 collision marks the strongest form. Minimum 3-candle requirement is represented in persistent state.
- **Type 3:** CSM alone is no longer a valid Re-Entry. CSM starts a candidate; a later retrace to MA5 or MA50 confirms it.
- **Type 4:** CSD alone is no longer a valid Re-Entry. CSD starts a candidate; a later retrace to MA5/10 confirms it.
- Re-Entry snapshot MA mapping is corrected so BUY stores MA5/10 Low and SELL stores MA5/10 High.
- H1/H4/D1 state advances only on a new closed candle of its own timeframe even though M15 remains the sole orchestration clock.
- Only confirmed Re-Entry remains exportable as `SIGNAL_RE_ENTRY`.

### Explicit operational interpretation
The source states that Type 2 occurs for a minimum of 3 candles per timeframe but does not define an algorithmic counter. Step 3B explicitly encodes this as **three distinct consecutive closed candles maintaining MA5/10 + MID BB confluence**. This is an implementation interpretation, not a claimed verbatim Oma Ally rule.

`IsNear()` is used only as the existing numerical representation of line collision because the source provides no pip/point collision tolerance. That tolerance is not treated as a BBMA strategy rule.

### Verification performed
- Patch 0006 dry-runs and applies cleanly against the reconstructed post-0005 M12 state.
- Structural braces, parentheses and brackets remain balanced in the reconstructed Step 3B state.
- Old Type 1 EMA50 confirmation function is removed from the Step 3B reconstruction.
- Old Type 2 BB-width detector is removed.
- Type 3 and Type 4 no longer become valid from their precursor signal alone.
- Type-specific lifecycle state is persistent and confirmed-only export remains intact.

### Remaining upstream blockers before M12 can be trusted numerically in production
1. **M06 MA producer:** MA5/10 High/Low production must be source-correct. M12 now depends directly on those four values.
2. **M10 CSM/CSD producer:** Type 3 and Type 4 depend on M10-owned precursor definitions. M12 does not redefine them; M10 source alignment must be audited separately.
3. **Higher-timeframe trend alignment:** the reference instructs multi-timeframe/higher-timeframe trend confirmation. This belongs to the later final entry-eligibility/priority contract and is not silently invented inside M12.

## Next P0 action
**Step 3C — repair and lock the M06 MA5/10 High/Low producer against the BBMA source before proceeding downstream.**

After M06, audit the M10 CSM/CSD producer dependency, then continue to M13/M14 combination/sequence repair.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
