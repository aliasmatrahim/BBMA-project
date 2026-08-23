# CORE-V2-F7 — Path A Strict Core Provenance Decision

Date: 2026-08-23  
Branch: `blueprint-dev`  
Status: **PATH A SELECTED / STRICT CORE PROVENANCE REQUIRED**

## Decision

The project selects **Path A — Strict Core-only provenance** for M17 executable SL/TP governance.

The current M17 resolver may continue to be used as the frozen P3 runtime candidate for plumbing/runtime evidence, but its complete H1 Re-Entry / REM / RRE / REE SL/TP mapping is **not production-certified as BBMA Strategy Core** until stronger source evidence is established.

No non-Core rule may be relabelled as BBMA Core merely to close this gap.

## Source decision basis

### Primary operational PDF
`Oma ally BBMA - AL.pdf` explicitly establishes:

- normal Extreme TP-Wajib movement toward the opposite MA5/MA10 area or Mid BB;
- Extreme retest/entry context;
- an Extreme-context statement that SL may be placed a few pips beyond the highest shadow/wick;
- Re-Entry Type 1–4 structure and multi-timeframe context.

It does **not** establish a universal deterministic formula equivalent to the current M17 policy for all executable H1 Re-Entry, REM, RRE and REE trades.

### Secondary PDF
`BBMA technique.pdf` establishes BB/MA support-resistance and BBMA Re-Entry structure, but the retained source does not establish the current exact M17 H1/H4/D1 outer-BB TP mapping or exact source-candle wick +/- one broker point hard-SL formula as universal Core.

### Finale V01–V07
Accepted Finale evidence strongly resolves normal Extreme TP Wajib, but does not establish the current executable Re-Entry/REM/RRE/REE outer-BB TP mapping as universal Core.

V07 MA10 + allowance stop material remains personal risk-management material and is not promoted into Strategy Core.

### Registered forum evidence
The retained Forex Factory evidence is supplemental/non-authoritative and does not currently contain traceable evidence for the exact current M17 mapping.

### External source hunt performed on 2026-08-23
A wider web search found several derivative/community BBMA documents that repeatedly describe Re-Entry profit-taking in **state/lifecycle terms** rather than as the current fixed mapped outer-BB destination. Examples include descriptions equivalent to:

- after Re-Entry, if Momentum/CSM appears, the move may continue and another Re-Entry can follow;
- if Re-Entry is followed by failure to produce Momentum, profit should be taken / the setup may rotate;
- some derivative material identifies TP on opposing direction/structure rather than a universal H1/H4/D1 outer-BB resolver.

These are useful research leads, but their provenance is not strong enough to become strict Core authority. They therefore **must not be encoded as replacement rules** under Path A without stronger authentication/reconciliation.

## Current implementation classification

### TP
Current mapping:

- H1 Re-Entry -> H1 Top/Low BB;
- REM -> H4 Top/Low BB;
- RRE -> D1 Top/Low BB;
- REE -> D1 Top/Low BB.

Status under Path A: **UNRESOLVED CORE PROVENANCE / NOT PRODUCTION-CERTIFIED AS BBMA CORE**.

### Hard SL
Current mapping:

- BUY -> exact mapped Re-Entry source-candle Low minus one broker point;
- SELL -> exact mapped Re-Entry source-candle High plus one broker point.

Status under Path A: **EA_SAFETY / NOT UNIVERSAL BBMA CORE**.

The primary PDF's Extreme-context wick-stop statement is insufficient to universalize this exact Re-Entry/REM/RRE/REE formula.

## Production gate

Before the project may claim the executable M17 SL/TP policy is fully BBMA/Oma Ally Core-derived, stronger evidence must establish the rule at sufficient specificity for autonomous execution.

Required evidence must resolve, at minimum:

1. **Re-Entry TP ownership:** what exact source-owned event/level terminates or targets a valid H1 Re-Entry;
2. **REM/RRE/REE TP ownership:** whether the higher-timeframe Re-Entry component supplies the exit target, and if so exactly how;
3. **Re-Entry hard-SL ownership:** what exact source structure invalidates the setup before/after execution;
4. whether SL is a static broker level, a lifecycle invalidation rule, or both;
5. whether TP is a static price level, a Momentum/no-Momentum lifecycle event, or a combination;
6. how the same rules scale across H1/H4/D1 and combination setups without inventing unsupported symmetry.

If the evidence does not resolve these items deterministically, the item remains `HOLD/UNRESOLVED` and no replacement BBMA rule is invented.

## Runtime freeze policy

Path A does **not** authorize changing `blueprint/source/BBMA_EA.mq4` while the current P3 runtime evidence B–D is pending.

Reason:

- runtime evidence must remain attributable to the already compiled/tested candidate;
- a documentation/source-governance decision is not itself a code defect;
- changing SL/TP now would invalidate attribution of the current runtime candidate.

If/when stronger source evidence authorizes a different M17 rule, it becomes a **new patch/build** subject to the mandatory build identifier, native compile, static regression, source-purity audit, and fresh runtime validation.

## Relationship to F7 audit

Parent audit:
`blueprint/CORE_V2_F7_M17_SLTP_PROVENANCE_AUDIT.md`

That audit remains valid:

- no current M17 implementation mismatch against its existing contract was found;
- provenance gap is real;
- current executable formula cannot be certified as fully BBMA Strategy Core from retained canonical evidence.

This decision resolves the governance choice by selecting **Path A**.

## Final state

**CORE-V2-F7 Path A state:**

- governance decision: **CLOSED — PATH A SELECTED**;
- strict SL/TP source provenance: **OPEN / UNRESOLVED**;
- production BBMA-Core certification for current M17 executable SL/TP: **BLOCKED**;
- P3 frozen runtime candidate: **PRESERVED**;
- EA source change now: **NO**;
- next source action: obtain/authenticate stronger Oma Ally/BBMA source evidence specifically for Re-Entry/REM/RRE/REE SL/TP lifecycle and destination ownership.
