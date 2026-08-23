# CORE-V2-F7 — M17 SL/TP Provenance Audit

Date: 2026-08-23  
Branch: `blueprint-dev`  
Scope owner: M17 initial SL/TP resolution / source governance  
Status: **AUDIT COMPLETE — PROVENANCE GAP CONFIRMED; NO EA CODE DEFECT IDENTIFIED**

## 1. Purpose

Resolve CV2-16 / CORE-V2-F7 by comparing the current executable M17 SL/TP policy against the project source hierarchy.

This is a source-governance audit. It does **not** change `blueprint/source/BBMA_EA.mq4` and does not disturb the frozen P3 runtime candidate.

Required comparison order:

`Original evidence -> Canonical Strategy Core -> M17 contracts -> current M17 code`

## 2. Source evidence established

### 2.1 Primary PDF — `Oma ally BBMA - AL.pdf`

The primary operational PDF explicitly supports:

- the BBMA cycle after an Extreme moving toward MA5/MA10 or Mid BB for mandatory profit taking;
- in the Extreme section, a stop statement that an SL can be placed a few pips above the highest shadow/wick;
- Re-Entry Type 1–4 entry/support/resistance/confluence semantics;
- REM/RRE/REE component/timeframe signatures and higher-timeframe alignment.

However, the PDF does **not** provide a complete universal deterministic initial SL/TP formula for all currently executable H1 Re-Entry, REM, RRE and REE decisions.

The Extreme-context wick-stop statement cannot be silently generalized into:

- every Re-Entry/REM/RRE/REE trade;
- the exact mapped Re-Entry source candle as the universal wick owner;
- a symmetric BUY/SELL formula for every executable setup;
- a one-broker-point buffer.

Those are project execution mappings unless stronger source evidence is established.

### 2.2 Secondary PDF — `BBMA technique.pdf`

The secondary PDF supports Bollinger Bands and Moving Averages as moving support/resistance and describes Re-Entry/Extreme/MHV structures. In the reviewed high-value sections it does not establish a deterministic universal executable H1 Re-Entry / REM / RRE / REE SL/TP resolver equivalent to current M17.

### 2.3 BBMA Finale V01–V07

Accepted Finale evidence gives a strong deterministic clarification for **normal Extreme TP Wajib**:

- Extreme SELL -> opposite MA5/MA10 Low area first;
- Extreme BUY -> opposite MA5/MA10 High area first;
- Mid BB is farther/maximum context.

This applies to the normal Extreme lifecycle and does not establish the current Re-Entry/REM/RRE/REE outer-BB TP mapping as universal Core.

V07 MA10 + allowance stop material is explicitly personal risk-management material and is rejected from universal Strategy Core.

### 2.4 Canonical Strategy Core V2

`docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` therefore establishes:

- normal Extreme TP-Wajib semantics;
- no accepted universal MA10+allowance stop rule;
- no complete universal executable H1 Re-Entry / REM / RRE / REE SL/TP contract equivalent to current M17.

### 2.5 Registered forum evidence

The registered source is the Forex Factory thread `BBMA strategy by Oma Ally` (thread 724759), classified `COMMUNITY / SUPPLEMENTAL / NON-AUTHORITATIVE`.

The current page-1 digest and systematic high-signal extraction do not contain a traceable post establishing the exact current M17 rules:

- H1 Re-Entry -> H1 outer BB TP;
- REM -> H4 outer BB TP;
- RRE/REE -> D1 outer BB TP;
- exact mapped Re-Entry source-candle wick +/- one broker point as hard SL.

Because the historical thread extraction is explicitly **not exhaustive page-by-page**, this is not proof that no such community statement ever existed. It does mean the current project evidence set is insufficient to cite the exact executable mapping as established by the registered forum source.

## 3. Current M17 contract/code behaviour

Current contracts and code agree with each other.

### TP mapping

- H1 `RE_ENTRY`: BUY -> H1 Top BB; SELL -> H1 Low BB.
- `REM`: BUY -> H4 Top BB; SELL -> H4 Low BB.
- `RRE`: BUY -> D1 Top BB; SELL -> D1 Low BB.
- `REE`: BUY -> D1 Top BB; SELL -> D1 Low BB.

The TP is resolved from the exact closed mapped Re-Entry source candle.

### Hard SL mapping

- BUY -> exact mapped Re-Entry source-candle Low minus one broker point.
- SELL -> exact mapped Re-Entry source-candle High plus one broker point.

### Safety behaviour

- wrong-side/crossed/stale/unresolved levels fail closed;
- no fixed-pip or RR-manufactured fallback exists;
- `MaxSLPips` and `MinRRRatio` are rejection filters only;
- broker StopLevel/FreezeLevel checks remain engineering constraints.

Result: **no implementation mismatch against the current M17 contract is identified.**

## 4. Audit findings

### F7-01 — No M17 code defect against its current contract

Classification: **NO IMPLEMENTATION DEFECT**.

The current M17 code faithfully implements the current M17 contracts.

### F7-02 — Executable outer-BB TP is not certified as PDF/Core

Classification: **SOURCE-GOVERNANCE / PROVENANCE GAP**.

The exact H1/H4/D1 outer-BB TP mapping is not established by the primary PDF, secondary PDF, accepted Finale Core, or canonical Strategy Core V2 as a universal executable rule for H1 Re-Entry/REM/RRE/REE.

It must not be described as `PDF_CORE` or as fully source-owned BBMA Strategy Core.

### F7-03 — Current `FORUM_SUPPORTED` TP label is not traceable enough

Classification: **DOCUMENTATION / PROVENANCE DEFECT**.

The registered forum evidence currently retained by the project does not contain the exact post/evidence needed to support the current outer-BB mapping. Until exact provenance is captured and reconciled, `FORUM_SUPPORTED` is stronger than the presently traceable evidence permits.

Recommended neutral classification if behaviour is retained:

`PROJECT_EXECUTION_POLICY / COMMUNITY-CORROBORATED-PENDING-TRACE`

Do not upgrade this to Strategy Core solely from generic BB/MA support-resistance reasoning.

### F7-04 — Hard SL is EA safety, not universal BBMA Core

Classification: **EA_SAFETY / SOURCE BOUNDARY**.

The primary PDF contains an Extreme-context wick-stop statement, so structural wick protection is not foreign to the source material. But current M17's exact Re-Entry source-candle wick owner plus one-point buffer is a deterministic engineering mapping beyond the universal source wording.

The one-point buffer is unequivocally engineering/broker protection.

Recommended classification:

`EA_SAFETY`, with a note that structural wick protection has limited source context from the primary PDF's Extreme section.

Do not call the full current formula `PDF_CORE`.

### F7-05 — Dynamic opposite-CSM/BB-expansion cut-loss remains outside enabled Core execution

Classification: **SUPPLEMENTAL / LIFECYCLE POLICY — NOT ENABLED**.

No change is authorized here. M17 remains initial SL/TP owner only; any dynamic live-position invalidation belongs to M23/M24 lifecycle governance and requires its own source/ownership audit.

## 5. F7 resolution state

The audit resolves the **classification question**, but it does not manufacture missing Strategy-Core evidence.

Therefore:

- **F7 audit:** COMPLETE.
- **Current M17 implementation:** contract-compliant.
- **Full BBMA-Core provenance claim for executable H1 Re-Entry / REM / RRE / REE SL/TP:** **NOT PROVEN**.
- **EA code change required now:** NO.
- **P3 frozen runtime candidate:** PRESERVE.

## 6. Production-governance choices

Before final production sign-off, the project must explicitly choose one of these paths.

### Path A — Strict Core-only provenance

Require stronger source evidence before claiming or locking the executable M17 TP/SL mapping as BBMA Strategy Core. Until then the provenance claim remains `HOLD/UNRESOLVED` even though the current implementation may continue runtime validation.

No replacement trading rule may be invented merely to close the gap.

### Path B — Explicit project execution policy

Retain the current deterministic M17 levels as a non-Core autonomous-execution policy, with exact provenance labels:

- outer-BB TP mapping -> `PROJECT_EXECUTION_POLICY` unless/until exact community evidence is captured;
- hard source-candle wick +/- Point -> `EA_SAFETY`;
- `MaxSLPips`, `MinRRRatio`, StopLevel/FreezeLevel -> EA risk/broker guards.

Under Path B, documentation/UI must never claim that these full formulas are explicit Oma Ally PDF/Core rules.

## 7. Recommended next action

Do **not** modify `BBMA_EA.mq4` while P3 runtime evidence B-D is pending.

Recommended documentation-only follow-up after this audit:

1. reconcile M17 contract provenance labels so unsupported `FORUM_SUPPORTED` wording is not stronger than retained evidence;
2. record the chosen Path A or Path B as an explicit project decision;
3. update `CURRENT.md` / `MASTER_QUEUE.md` during the next state-reconciliation pass;
4. if stronger source evidence is later found, reopen F7 and trace the exact source before changing strategy behaviour.

## 8. Final verdict

**CORE-V2-F7 verdict: PROVENANCE GAP CONFIRMED; NO CURRENT M17 IMPLEMENTATION BUG.**

The present resolver is deterministic and internally coherent, but its complete executable H1 Re-Entry / REM / RRE / REE SL/TP formula cannot currently be certified as fully BBMA Strategy Core from the retained canonical evidence set.
