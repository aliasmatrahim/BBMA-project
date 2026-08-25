# Targeted SL/TP Implementation Audit — 2026-08-26

**Branch audited:** `d1-owner-dev`  
**EA build audited:** `Version 4.5.6 - C044 Deterministic Replay Stage`  
**Scope:** Strategy-derived initial SL/TP and lifecycle exit behaviour; M17 ownership and downstream implications.

## Verdict

**REPAIR / SOURCE-RESOLUTION REQUIRED. Do not declare current SL/TP source-locked.**

The current M17 implementation is materially safer than the legacy fixed-pip/RR builder because it no longer manufactures an RR-derived destination and it resolves a structural source component. However, the latest source set does **not** support claiming that the current generic Re-Entry-owned structural SL + static outer-BB TP is the final BBMA SL/TP contract.

Most importantly, `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` still explicitly says that unresolved SL/TP provenance issues remain outside authoritative Core. Therefore code cannot outrank that unresolved source status.

## Evidence reviewed

### Primary operational PDF — `Oma ally BBMA - AL.pdf`

- BBMA cycle states that an Extreme entry has mandatory profit taking as price moves to MA5/MA10 or Mid BB.
- Extreme section states that SL can be placed a few pips above the highest shadow/wick.
- Re-Entry sections define Types 1–4 and their MA/BB context but do not provide an equally explicit universal broker-SL formula for every Re-Entry/REM/RRE/REE entry.

### Home Course Workbook

- Extreme entry: TP is mandatory at MA5/MA10; Mid BB is the farthest destination / no-compromise context.
- MHV: TP is not universally fixed at MA5/10 or Low/Top BB; the next candle / momentum state changes whether the position is held or closed.
- After direction + Re-Entry: if Momentum fails, close/TP because market is expected to reverse; if Momentum appears, wait for the next Re-Entry.
- Direction without Re-Entry may be held while waiting for Re-Entry.

This is lifecycle-sensitive exit behaviour, not one universal static initial TP rule.

### Canonical Core V2

- Extreme normal TP-Wajib is explicitly reconciled: SELL -> opposite MA5/MA10 Low area; BUY -> opposite MA5/MA10 High area; Mid BB is farther/maximum context.
- Core V2 also explicitly records that still-unresolved SL/TP provenance issues remain outside authoritative Core.

## Current implementation observed

### M17 source ownership

`IsApprovedSLTPSourceComponent()` accepts only a `SIGNAL_RE_ENTRY` component as SL/TP source:

- standalone RE -> H1 (or H1/M15 for D1 Opportunity cluster),
- REM -> H4,
- RRE/REE -> D1.

### Current SL

`ResolveApprovedInitialSLTP()` resolves the exact M12 Re-Entry lifecycle and scans the closed source-owned window `StartCandleTime..ConfirmationCandle`:

- BUY: lowest low in the lifecycle window,
- SELL: highest high in the lifecycle window,
- adds one `Point` structural safety buffer,
- SELL additionally adds a rounded spread buffer,
- normalizes outward to tick size.

This is deterministic and broker-safe, but the exact generic Re-Entry lifecycle-window SL formula is a project mapping whose BBMA-source provenance is not yet closed.

### Current TP when C044 lifecycle is OFF (default)

`ResolveApprovedBBDestination()` sets:

- BUY -> source-timeframe `TOP_BB`,
- SELL -> source-timeframe `LOW_BB`.

Therefore current static initial TP for RE/REM/RRE/REE is an outer-BB destination based on the selected Re-Entry source component.

### Current TP when C044 lifecycle is ON

Initial TP is set to `0.0` and lifecycle management is expected downstream. The source itself states C044 remains fail-safe gated OFF until M23/M24 close/restart lifecycle support is complete and verified.

## Findings

### SLTP-01 — HIGH — D1 `EXTREME_TPW` opportunity is not TP-Wajib-owned in M17

The D1 Opportunity engine contains an explicit `D1_OPP_EXTREME_TPW` family, but the resulting candidate is represented as a Re-Entry execution cluster and M17 accepts only the selected Re-Entry component as SL/TP owner.

With C044 OFF, M17 therefore resolves a static outer-BB destination from the Re-Entry component instead of the source-reconciled Extreme TP-Wajib area.

This is a direct semantic mismatch risk because Core V2 already has an explicit normal Extreme TP-Wajib contract: opposite MA5/MA10 first; Mid BB only farther/maximum context.

**Status:** repair required, but exact D1-opportunity destination ownership must be reconciled with the D1O contract before editing code.

### SLTP-02 — HIGH — Generic static outer-BB TP is not sufficient to represent latest lifecycle exit evidence

Current non-C044 execution gives RE/REM/RRE/REE one static outer-BB TP.

Home Course evidence is lifecycle-dependent:

- after Re-Entry, no Momentum -> TP/close,
- Momentum -> continue and wait for next Re-Entry,
- direction without Re-Entry may be held until Re-Entry,
- MHV exits are conditional rather than one universal fixed target.

Therefore a static outer-BB TP may be a useful provisional destination, but it cannot be called the complete latest BBMA exit contract.

**Status:** source/contract reconciliation required; likely M23/M24 lifecycle responsibility, not an M17-only patch.

### SLTP-03 — MEDIUM/HIGH — Generic Re-Entry SL provenance remains unresolved

Primary PDF gives an explicit Extreme-context statement: SL can be a few pips beyond the highest wick/shadow. It does not, in the reviewed source, establish the current universal formula of `ReEntry lifecycle window extreme +/- 1 Point`, plus SELL spread buffer, for every RE/REM/RRE/REE source.

The current formula is technically deterministic and broker-aware, but Core V2 itself says unresolved SL/TP provenance remains outside authoritative Core.

**Status:** HOLD / source-resolution required before claiming BBMA-canonical SL. Do not replace it with a different guessed numeric rule.

### SLTP-04 — MEDIUM — `MinRRRatio` and `MaxSLPips` are safety filters, not BBMA destination generators

Current code correctly does not use MinRR to manufacture TP. `MinRRRatio > 0` only rejects insufficient RR; `MaxSLPips` only rejects an excessive resolved SL. This separation should be preserved.

**Status:** keep.

### SLTP-05 — KEEP — broker stop/freeze validation is implementation safety, not Strategy-Core reinterpretation

StopLevel/FreezeLevel checks, tick-size normalization, directional Bid/Ask geometry and fail-closed rejection are broker/execution safeguards. They should not be confused with the BBMA semantic source of SL/TP.

**Status:** keep.

## Required next sequence

1. Resolve the source contract separately for:
   - Extreme/TP-Wajib,
   - MHV live-position exit,
   - Re-Entry / Momentum continuation and failed-Momentum exit,
   - REM/RRE/REE destination ownership,
   - D1 Opportunity `EXTREME_TPW` destination ownership,
   - protective SL provenance per executable family.
2. Cross-check PDF + Finale V01–V07 + Home Course + relevant forum evidence.
3. Update Core V2 only for rules that become accepted/reconciled.
4. Update M17/M23/M24 contracts so initial protective SL, optional broker TP, and lifecycle close authority are separated explicitly.
5. Patch code only after the source contract is deterministic.
6. Apply new build/patch identifier, compile, static regression and runtime validation.

## Audit conclusion

**Current M17 is not legacy fixed-pip/RR logic, but SL/TP is not fully updated to the latest BBMA source set.**

The clearest actionable defect is the mismatch between `D1_OPP_EXTREME_TPW` semantics and M17's Re-Entry-owned static outer-BB destination. The broader generic SL and lifecycle TP/close rules require source reconciliation first; inventing a replacement now would violate project governance.