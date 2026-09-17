# Q5 — Standalone Extreme Execution Policy Decision

Date: 2026-09-17
Issue: #175
Owner baseline: `d1-owner-dev@0d8c8ac71aeb9947d48f89239f46a88c31981182`
Status: **RESOLVED — USER-APPROVED PROJECT EXECUTION POLICY**

## Decision scope

This decision closes only the remaining autonomous hard-SL mapping gate for standalone H1 Extreme execution under Entry Mode 2.

Accepted Strategy-Core maturity remains unchanged:

`RAW EXTREME -> REVERSAL-CONFIRMED -> RETEST/ENTRY-READY`

Only `RETEST/ENTRY-READY` is eligible as a standalone Extreme entry. RAW and reversal-only standalone Extreme remain non-executable.

## Locked structural wick window

The exact protective structural window is:

`RAW Extreme candle -> RETEST completion candle`, inclusive.

For BUY, the structural anchor is the lowest `Low` across that exact closed-candle window.

For SELL, the structural anchor is the highest `High` across that exact closed-candle window.
## Locked structural buffer

The project-approved structural buffer is exactly **3.0 pips** outside the structural wick anchor:

- BUY: `SL_structural = lowest Low - 3.0 pips`;
- SELL: `SL_structural = highest High + 3.0 pips`.

The primary source supports the Extreme-context concept of a stop a few pips beyond the relevant shadow/wick. The exact 3.0-pip value and lifecycle-window ownership are therefore classified as `PROJECT_EXECUTION_POLICY`, not universal Oma Ally Core.

## Broker normalization

Existing M17 broker normalization remains `EA_SAFETY`:

- BUY receives no additional spread buffer after the 3.0-pip structural buffer;
- SELL adds the frozen Ask-trigger spread normalization already owned by M17;
- final SL normalizes outward to broker tick size;
- StopLevel / FreezeLevel remain broker guards;
- `MaxSLPips` remains rejection-only and never clips or manufactures SL;
- `MinRRRatio` remains rejection-only and never manufactures TP.

## Execution scope

Standalone Extreme execution is limited to H1 under Entry Mode 2 and remains subject to the existing H4 immediate-owner boundary plus M11 D1 strategic gate.

M08 remains the Extreme lifecycle owner. M15 may only materialize an entry candidate from the exact mature owner state; M16 revalidates that identity; M17 resolves the approved SL/TP geometry. No detector is duplicated downstream.
## TP-Wajib execution mapping

Normal Extreme TP-Wajib remains source-authoritative: BUY targets the opposite MA5/MA10 High area first; SELL targets the opposite MA5/MA10 Low area first; Mid BB is farther context.

For deterministic initial broker TP in this H1 standalone scope, M17 maps that first area edge on the exact RETEST-completion H1 candle as:

- BUY: `min(MA5 High, MA10 High)`;
- SELL: `max(MA5 Low, MA10 Low)`.

This static zone-edge coordinate is an execution mapping preserving the source-owned TP-Wajib area; it is not a new Strategy-Core formula. A stale or wrong-side destination fails closed with no fallback.

## Rejected alternatives

No fixed 5-pip legacy stop, ATR stop, arbitrary swing lookback, MA10+allowance stop, RR-manufactured TP, Mid-BB fallback, raw-Extreme entry, or reversal-only standalone entry is authorized.

## Implementation gate

The decision gate is resolved. Production acceptance still requires test-first implementation, native MetaEditor 0E0W, targeted regression and attributable runtime/Strategy Tester evidence for BUY/SELL structural geometry before Issue #175 can close.
