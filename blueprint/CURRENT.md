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
18. `blueprint/patches/0018-p0-step10-m19-risk-filter-accounting.patch`
19. `blueprint/patches/0019-p0-step11-m20-portfolio-gate-protection-ownership.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` was discovered during Step 3D to have been calculated from a partial reconstruction and remains withdrawn.

Last exact verified full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0019 currently have focused patch/contract verification only. A new full-chain SHA must only be claimed after exact materialization of the complete ordered patch chain.

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
- `blueprint/contracts/M19_RISK_FILTER_CONTRACT.md`
- `blueprint/contracts/M20_PORTFOLIO_PROTECTION_CONTRACT.md`
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

## Step 8B — BBMA SL / TP / Exit source resolution
Status: **APPROVED AT ARCHITECTURE CONTRACT LEVEL**

Provenance remains separated into `PDF_CORE`, `FORUM_SUPPORTED`, and `EA_SAFETY`.

Approved TP mapping:
- H1 Re-Entry BUY -> H1 TOP BB; SELL -> H1 LOW BB;
- REM BUY -> H4 TOP BB; SELL -> H4 LOW BB;
- RRE BUY -> D1 TOP BB; SELL -> D1 LOW BB;
- REE BUY -> D1 TOP BB; SELL -> D1 LOW BB.

No universal fixed-pip TP/SL is accepted as BBMA Core.

## Step 8C — approved M17 source resolver
Status: **COMPLETED AT ACTIVE-BLUEPRINT PATCH LEVEL**

Implemented by `blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`.

- final decision preserves the exact destination-producing Re-Entry component;
- H1/H4/D1 mapping is enforced for RE_ENTRY/REM/RRE/REE respectively;
- source candle must resolve exactly and be closed (`shift >= 1`);
- TP is read from approved source-timeframe TOP/LOW BB;
- hard SL uses exact source-candle wick plus one broker point as `EA_SAFETY` protection;
- unresolved/crossed/stale data fails closed;
- fixed-pip or RR-derived fallback is not introduced.

## Step 9 — M18 Signal Scoring / Label Authority
Status: **COMPLETED AT ACTIVE-BLUEPRINT PATCH + CONTRACT LEVEL**

- unsupported numeric BBMA quality weights removed;
- M18 is optional observability/display metadata only;
- `Score = 0`, `Level = LEVEL_NONE` for current execution architecture;
- no impact on entry, invalidation, SL/TP, risk, portfolio or execution.

## Step 10 — M19 Risk Engine
Status: **COMPLETED AT FILTER / ACCOUNTING CONTRACT LEVEL**

- spread unit handling repaired to true pips;
- drawdown separated from basket floating loss;
- total risk made prospective EA-wide and symbol-correct;
- stale/closed monitored entries excluded;
- unquantifiable risk fails closed;
- specific rejection reasons propagate correctly;
- M19 remains allow/reject only.

## Step 11 — M20 Portfolio Risk & Protection Engine
Status: **COMPLETED AT PORTFOLIO-GATE / PROTECTION-OWNERSHIP LEVEL**

Baseline defects repaired:
- `FinalPortfolioGuard()` checked prospective total trades and active pairs but omitted prospective `MaxTradePerPair` enforcement;
- it ignored `status.allowed` when the current portfolio was already beyond a hard limit;
- portfolio accounting relied on monitored entries without revalidating live EA magic ownership;
- `ManagePortfolio()` directly called `OrderClose()`, competing with M23 position-management ownership;
- `BasketProfitPercent` acted as a second TP policy and could close positions before the M17-approved BBMA destination.

Implemented by:
`blueprint/patches/0019-p0-step11-m20-portfolio-gate-protection-ownership.patch`

Patch commit:
`db18296e376a149d0238c116ef2c3c933ab00861`

Contract:
`blueprint/contracts/M20_PORTFOLIO_PROTECTION_CONTRACT.md`

Contract commit:
`641a216cfaa088627b4f0de4366d19850d886e60`

Locked M20 behavior:
- current portfolio counts only live, monitored, EA-owned orders whose live magic matches the configured pair magic;
- entry admission is prospective and atomic for `MaxActivePair`, `MaxTradePerPair`, and `MaxTotalTrade`;
- M20 may reject only with `REJ_PORTFOLIO_LIMIT_ATOMIC`; it cannot alter M15-M17 payload;
- basket-loss protection raises a latched `g_portfolio_emergency_close_requested` state;
- M23, not M20, owns broker close actions;
- the emergency request stays latched until all live EA-owned monitored positions are closed, allowing later-tick retry;
- `BasketProfitPercent` is compatibility/display-only and is not an execution trigger, preserving M17 BBMA TP authority;
- `ManagePortfolio()` is called before `ManagePositions()` so a newly tripped protection request can be acted on by M23 on the same tick.

### Downstream issue explicitly deferred
M23 still contains partial-close-at-1R and breakeven behavior plus direct TP close calls. Those are not silently accepted by Step 11; they are now flagged for the dedicated M23 lifecycle audit because they may conflict with the locked BBMA SL/TP policy and the project's no-extra-exit-management requirement.

### Verification boundary
The M20 baseline, both portfolio-gate call paths, `ManagePortfolio()` tick ordering, and all baseline `OrderClose()` locations were inspected. Patch 0019 and the M20 contract are stored on `blueprint-dev`. No full-chain compile/SHA is claimed yet.

## Next P0 action
**Step 12 — audit M21 Money Management.**

Required focus:
1. lot sizing must consume the final M17-approved Entry/SL distance without modifying it;
2. AutoLotPercent and FixedLot must be unit-correct across symbols and broker lot steps;
3. invalid/min/max/step cases must fail closed rather than clamp into unintended risk;
4. M21 must not use M18 score/level or signal type to change risk;
5. ensure the lot returned to M19/M20/M22 is deterministic from the frozen decision/risk snapshot.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
