# P2 Step 15 — Order Execution / Broker Constraints / Normalization Audit

Status: FAIL — Fix A required

## Scope
Cross-module audit of M17 SL/TP resolution + validation, M21 lot sizing, M22 order execution, and broker digit/step constraints.

## Finding
The resolved protective/target prices are not normalized to broker price precision before they are sent to `OrderSend()`.

`ResolveApprovedInitialSLTP()` assigns:
- structural SL from source wick ± one broker point;
- TP directly from `iBands()` output.

Those values then pass through `ValidateSLTP()` and later M22 forwards `decision.StopLoss` / `decision.TakeProfit` directly into `OrderSend()`.

Lot sizing is already broker-step aware via the frozen snapshot, but SL/TP price quantization is not. Indicator-derived double values (especially the Bollinger destination) can carry precision beyond the symbol's executable digits/tick grid, leading to avoidable broker error 130 / invalid stops or inconsistent execution behavior.

## Required Fix A
Add broker-executable price normalization at the M17 source-resolution boundary, before risk sizing and validation:
- quantize SL and TP using the frozen snapshot symbol precision;
- preserve strategy geometry (no fixed-pip replacement, no RR-derived target);
- apply direction-safe SL rounding so normalization cannot weaken the protective side;
- validate directional geometry and StopLevel after normalization;
- M22 remains a dumb executor and must not repair prices at send time.

No BBMA signal-selection logic changes are permitted.
