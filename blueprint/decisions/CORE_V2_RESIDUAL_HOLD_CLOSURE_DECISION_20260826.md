# Core V2 Residual HOLD Closure Decision — 2026-08-26

Branch: `d1-owner-dev`
Status: **APPROVED / RESIDUAL CORE AMBIGUITIES CLOSED / NO EA SOURCE CHANGE BY THIS RECORD**

## Purpose

Close residual `HOLD / CLARIFY / VERIFY` wording that remains in `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` outside the 49-family ledger after the 2026-08-26 full Core research/rebaseline.

## R1 — MA5 merely touching outer BB as Extreme

**Decision: REJECT AS UNIVERSAL EXTREME CONDITION.**

Accepted canonical Extreme remains an actual MA extension **outside** the relevant outer Bollinger Band under the M08/Core contract.

A mere touch/equality with Top/Low BB:
- may be observed as boundary interaction;
- does not by itself create `SIGNAL_EXTREME`;
- cannot bypass reversal/maturity requirements;
- cannot create TP-Wajib or execution authority.

Reason: primary/source-aligned Extreme definition consistently uses MA outside the band. Broader touch wording is insufficient to weaken the stricter established definition.

Tag: `[REJECTED-FROM-CURRENT-CORE]` for `touch == Extreme`.

## R2 — reversal candle remains closed outside BB but inside MA5

**Decision: REJECT AS UNIVERSAL VALID-EXTREME ACCEPTANCE RULE.**

Canonical priority remains:
- source-valid outside-BB close / Momentum invalidation has precedence over Extreme maturity promotion;
- a reversal-direction candle cannot universally rescue an Extreme lifecycle if the accepted outside-close invalidation is already present;
- no generic `inside MA5` exception overrides that invalidation.

This does not forbid a future narrowly evidenced advanced structure, but no current Core detector or maturity owner may use `reversal candle outside BB but inside MA5` as a universal valid shortcut.

Tag: `[REJECTED-FROM-CURRENT-CORE]`.

## R3 — Re-Entry validation candle / entry candle timing

**Decision: CLOSED / SEMANTIC MAPPING VERIFIED.**

Canonical project timing:
- source-timeframe Re-Entry validation uses a fully closed source candle;
- once that candle has closed and the Re-Entry is confirmed, execution may be eligible during the **immediately following live source-timeframe candle** subject to the normal M15/final-authority and downstream gates;
- no additional full source candle must close merely because teaching language says `first candle validates / second candle entry`;
- `EntryCandle` metadata points to the immediately following source-TF candle and must not duplicate the confirmation candle.

This matches the already completed F6 static timing verification. Remaining live `OrderOpenTime()` traces are runtime evidence only and do not keep the Strategy-Core semantic timing unresolved.

Tag: source teaching `[BBMA-SOURCE-CONSISTENT]`; exact closed-candle/autonomous-EA mapping `[PROJECT-EXTENSION][ENGINEERING-ONLY]`.

## R4 — residual SL/TP wording

Unresolved universal broker-SL/TP formulas are not left as undefined Core obligations. They are now explicitly classified:
- normal Extreme TP-Wajib = Core;
- D1 `EXTREME_TPW` lifecycle semantic owner = D1 Extreme, with targetless broker mapping as project engineering;
- Re-Entry structural-range hard SL = `EA_SAFETY / PROJECT EXECUTION NORMALIZATION`, not universal BBMA Core;
- generic Re-Entry static outer-BB broker TP = historical/project policy, not universal Core;
- C044 post-Re-Entry continuation/failure principle = accepted lifecycle source principle, with conservative deterministic implementation mapping separately labelled project policy.

Therefore lack of a universal source-proven broker formula is a **provenance classification**, not an unresolved Core semantic gap.

## Final verdict

After this record plus the 49-family rebaseline and advanced repeated-Extreme decision:

**UNRESOLVED BBMA CORE SEMANTIC HOLD COUNT = 0.**

This does not activate any gated lifecycle feature and does not convert context-only/rejected material into execution authority.
