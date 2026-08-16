# BBMA Master Blueprint Development Status

## Current branch
`blueprint-dev`

## Source of truth
GitHub `aliasmatrahim/BBMA-project` is authoritative for the active Master Blueprint. Notion is supporting documentation only.

## Immutable baseline
Source: `Master Blueprint 2.0.txt`

Verified baseline SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

The exact baseline is stored as deterministic gzip+base64 chunks under:
`blueprint/archive/`

Reconstruction order:
1. `MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part01a`
2. `MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part01b`
3. `MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part02`
4. `MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part03`
5. `MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part04`
6. `MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part05`

## Current revision
Apply patches in order:

1. `blueprint/patches/0001-fix-m25-complexity-limiter.patch`
2. `blueprint/patches/0002-p0-step1-bbshape-extreme-contract.patch`
3. `blueprint/patches/0003-p0-step2-mlv-persistence-lifecycle.patch`
4. `blueprint/patches/0004-p0-step2b-mlv-void-transition-contract.patch`
5. `blueprint/patches/0005-p0-step3-reentry-persistence-lifecycle.patch`

Expected working-source SHA-256 after patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

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

Architecture:
- M06 supplies frozen closed-candle market data.
- M07 solely classifies BB shape/state.
- M08 consumes classified BB state.
- M13 remains collect-only.
- M27 remains orchestrator-only.

No Extreme trading rule, direction rule, SL/TP rule, risk rule or execution rule was changed by this step.

## Step 2 — M09 MLV persistence/lifecycle
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

Architecture:
- `PairState` owns independent persistent BUY/SELL MLV slots.
- M09 solely mutates MLV lifecycle.
- M27 selects the correct state slot and passes a cycle snapshot downstream.
- M13 no longer mutates MLV lifecycle.
- Lifecycle: `NONE → CANDIDATE → CONFIRMED → EXPIRED`, plus explicit `VOID` invalidation interface.
- Candidate cannot confirm on its creation candle.
- `ExpiryCandleTime` is authoritative.
- Sequence chronology uses MLV confirmation candle, not candidate start candle.

## Step 3 — M12 Re-Entry persistence/lifecycle
Status: **PARTIALLY COMPLETED / SAFE ARCHITECTURE GUARD APPLIED**

### Repaired
- Re-Entry is no longer a local object that is recreated/zeroed as lifecycle authority every M15 processing cycle.
- `PairState` now owns persistent Re-Entry state for H1/H4/D1 independently for BUY and SELL.
- M12 is the sole owner of Re-Entry lifecycle mutation.
- M13 remains collect-only and receives an immutable H1 Re-Entry snapshot.
- M27 only routes frozen H1/H4/D1 data into M12 and exports confirmed H4/D1 Re-Entry signals for combinations.
- Direct `DetectReEntry_Master(...) → Valid=true` shortcuts in M13/M27 are removed.
- Type 1 now follows an explicit persistent lifecycle: `NONE → CANDIDATE → CONFIRMED → EXPIRED` using the confirmation rule already present in the active Master Blueprint.
- Candidate and confirmation must occur on different closed candles.
- Re-Entry expiry is timeframe-aware via `ExpiryCandleTime = StartCandleTime + MaxWaitBars_ReEntry × timeframe`.
- Only `RE_STATE_CONFIRMED && IsValid` may be exported as `SIGNAL_RE_ENTRY`.

### Safety quarantine
Type 2, Type 3 and Type 4 are currently **not execution-eligible** in the authoritative lifecycle. They are deliberately quarantined until their BBMA contract is reconciled. This prevents an incomplete or contradictory detector from becoming a valid combination component.

### Source conflict discovered
The active Master Blueprint defines detector code for Type 2–4 but does not define their confirmation lifecycle. A prior project reference, `PSCODE BBMA CORE V1.0.txt`, states BBMA/PDF-derived semantics that do not match the current detector implementations:

- Type 2: MA5/10 + MID BB collision, strongest when MA50 also meets; minimum 3 candles per timeframe.
- Type 3: CSM occurs, then price retraces/reverses to MA5 or MA50.
- Type 4: CSD occurs, then price gyrates/retraces toward MA5/10.

The current Master Blueprint Type 2–4 detectors therefore require a deliberate source-alignment repair before they can be re-enabled. The historical reference is supporting evidence only; GitHub remains authoritative after the repair is explicitly incorporated.

### Verification
- Patch 0005 applies cleanly to the Step 2 working source.
- Old direct-valid H4/D1 Re-Entry paths are removed.
- Re-Entry state slots exist for H1/H4/D1 × BUY/SELL.
- Only confirmed states are exported downstream.
- Structural braces, parentheses and brackets remain balanced.
- Working-source SHA-256 is `9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`.

## Next P0 action
**Step 3B — reconcile and lock Re-Entry Type 2–4 BBMA contracts before proceeding to M13/M14.**

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
