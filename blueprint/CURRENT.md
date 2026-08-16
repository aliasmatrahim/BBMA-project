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
3. `blueprint/patches/0003-p0-step2-mlv-persistence-lifecycle.patch`
4. `blueprint/patches/0004-p0-step2b-mlv-void-transition-contract.patch`

Expected working-source SHA-256 after patches 0001–0004:
`5e83938613aa3304f5cd4e1241e0dc3fee5f8a52ea5b8d71b5b8fadca779094f`

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

Architecture after repair:
- **M06** supplies frozen closed-candle `TimeframeData` and current Bollinger values.
- **M07** is the sole owner of BB shape classification.
- **M08** remains detector/consumer only.
- **M13** remains collect-only and receives classified H1 BB state.
- **M27** remains orchestrator-only and routes H1/H4 classified band snapshots.

Scope guard: no Extreme definition, direction rule, MA rule, sequence rule, SL/TP rule, risk rule, or execution rule was changed by Step 1.

### Step 2 — M09 MLV persistence/lifecycle
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

Problems repaired:
- `MLVData` was previously a local object inside the BUY/SELL loop and was zeroed every processing cycle, making `MLV_CANDIDATE → MLV_CONFIRMED` persistence impossible.
- One non-directional detector could prefer a SELL DoubleTop before a BUY DoubleBottom when both were inspected in the same state object.
- M13 was mutating MLV lifecycle even though it is a collect-only module.
- MLV validity used a hardcoded `10 * 900` expiry instead of `MaxWaitBars_MLV`.
- M13 used the MLV candidate start candle as the sequence component time even though MLV becomes usable only after confirmation.
- `MLV_VOID` existed in the enum but there was no defined state-transition interface.

Architecture after repair:
- `PairState` owns two persistent slots: `mlv_buy_state` and `mlv_sell_state`.
- M09 is the sole owner of MLV state mutation.
- M27 only chooses the pair+direction slot, invokes one M09 update on the frozen closed M15 snapshot, then copies an immutable cycle snapshot downstream.
- M13 consumes the MLV snapshot and no longer calls the MLV state engine.
- State lifecycle is now explicitly `MLV_NONE → MLV_CANDIDATE → MLV_CONFIRMED → MLV_EXPIRED`, with `MLV_VOID` available for explicit external invalidation.
- `MarkMLVVoid()` is the state-mutation interface for future M16 invalidation. Step 2 deliberately does not invent a price-based VOID rule because the source blueprint does not define one.
- Terminal `VOID/EXPIRED` state is retained for one completed processing candle, then the pair+direction slot is released for a new independent MLV pattern.
- Candidate creation and confirmation cannot occur on the same closed candle.
- `ExpiryCandleTime` is derived from `StartCandleTime + MaxWaitBars_MLV × timeframe` and is the authoritative time-based expiry field.
- A confirmed MLV is valid only while `State == MLV_CONFIRMED`, `IsValid == true`, and the expiry has not passed.
- REM sequence chronology now uses `m15_mlv.ConfirmationCandleTime` for the MLV component; candidate start time remains available as the overall pattern start metadata.

Scope guard:
- Existing DoubleTop/DoubleBottom comparison logic, tolerance (`point * 10`) and confirmation neckline offset (`point * 5`) are preserved.
- No new BBMA trading condition was invented.
- No MLV VOID price rule was invented; external invalidation criteria remain for the later M16 repair.
- Restart persistence is not claimed here; recovery across EA restart belongs to the later recovery/state-reconstruction scope.

Verification performed:
- Old `DetectMLV_State(... timeframe, shift)` call contract is removed from the working revision.
- M13 no longer mutates MLV state.
- BUY and SELL persistent state slots are both present and initialized.
- `ConfirmationCandleTime` is used for the MLV sequence component.
- Hardcoded `10 * 900` MLV validity expiry is removed.
- `MLV_EXPIRED` and `MarkMLVVoid()` are present.
- Structural braces and parentheses remain balanced in the reconstructed working source.

### Next P0 step
**Step 3 — M12 Re-Entry persistence/lifecycle.**

Target: make Re-Entry candidate/confirmation/expiry state persistent and authoritative, remove the current detector-immediately-valid shortcut, and preserve M13 as collect-only.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
