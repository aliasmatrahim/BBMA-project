# BBMA Master Blueprint Development Status

## Current branch
`blueprint-dev`

## Baseline
Source: `Master Blueprint 2.0.txt`

Immutable archive is stored as verified deterministic gzip+base64 chunks:

- `blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part01a`
- `blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part01b`
- `blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part02`
- `blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part03`
- `blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part04`
- `blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part05`

Verified encoded length: `32224` characters.

Original source SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

To reconstruct the exact baseline locally from the repository root:

```bash
cat \
  blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part01a \
  blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part01b \
  blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part02 \
  blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part03 \
  blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part04 \
  blueprint/archive/MASTER_BLUEPRINT_2.0_BASELINE.txt.gz.b64.part05 \
  | base64 -d | gzip -d > MASTER_BLUEPRINT_2.0_BASELINE.txt
```

Then verify:

```bash
sha256sum MASTER_BLUEPRINT_2.0_BASELINE.txt
```

Expected SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

## Current revision
Apply patches in order:

1. `blueprint/patches/0001-fix-m25-complexity-limiter.patch`
2. `blueprint/patches/0002-p0-step1-bbshape-extreme-contract.patch`

Expected working-source SHA-256 after patches 0001 + 0002:
`039b586a3868b7bb39d4ab18275106092548711910a181229e6637260cc21e46`

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

## P0 Architecture Repair

### Step 1 — BB Shape → Extreme contract
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

Problem repaired:
- M13 previously forced H1 `BollingerBand.State = BB_NONE` before calling M08.
- M27 previously forced H4 `BollingerBand.State = BB_NONE` before calling M08.
- `PairState.prev_bollinger` was declared and read but never populated, so M07 could not classify H1 state reliably.

Architecture after repair:
- **M06** supplies the frozen closed-candle `TimeframeData` and current Bollinger values.
- **M07** is the sole owner of BB shape classification. `BuildBBShapeState()` builds the current/previous closed-candle BB pair and assigns the current state.
- **M08** remains a detector/consumer. Its existing Extreme trading-rule conditions are not changed by this step.
- **M13** remains collect-only. It receives the already classified H1 band and does not create or reinterpret BB state.
- **M27** remains orchestrator-only. It invokes M07 for H1/H4, stores the H1 snapshot in `PairState`, and routes the classified bands to downstream consumers.

Closed-candle rule:
- `BuildBBShapeState()` rejects invalid/open data and requires `barIndex >= 1`.
- The current BB values come from the frozen `TimeframeData` snapshot.
- The previous BB is calculated from the immediately preceding closed candle (`barIndex + 1`).

Scope guard:
- No Extreme definition, direction rule, MA rule, sequence rule, SL/TP rule, risk rule, or execution rule is altered in Step 1.
- `EnableBBShapeEngine == false` leaves the routed BB bands unclassified (`BB_NONE`), so M08 does not receive a fabricated substitute state.

Verification performed:
- All `CollectAllSignals()` call/signature references were reconciled.
- H1 and H4 no longer receive hard-coded `BB_NONE` in the Extreme path.
- `prev_bollinger` now has a defined producer and meaning.
- Structural delimiter balance of the working blueprint remains intact after the patch.

### Next P0 step
**Step 2 — M09 MLV persistence/lifecycle.**

Target: remove the current per-cycle zeroing problem so `MLV_CANDIDATE → MLV_CONFIRMED/MLV_VOID/expiry` can persist across M15 processing cycles without moving lifecycle authority out of M09.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
