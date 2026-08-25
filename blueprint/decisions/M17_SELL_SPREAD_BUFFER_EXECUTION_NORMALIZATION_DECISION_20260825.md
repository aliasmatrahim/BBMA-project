# M17 SELL Spread-Buffer Execution Normalization Decision — 2026-08-25

Status: **SUPERSEDED / HISTORICAL ONLY / DO NOT IMPLEMENT INDEPENDENTLY**

Superseded by:
`blueprint/decisions/M17_REENTRY_STRUCTURAL_RANGE_SL_EXECUTION_NORMALIZATION_DECISION_20260825.md`

## Historical purpose
This record originally locked SELL-only spread-buffer normalization while keeping the old exact-confirmation-candle wick anchor unchanged.

The user subsequently approved a broader and more coherent hard-SL model for the next source update:
- BUY and SELL structural anchors now come from the full validated M12 Re-Entry lifecycle window from `StartCandleTime` through `ConfirmationCandle`, inclusive;
- BUY uses the lowest Low in that structural window and receives no spread buffer;
- SELL uses the highest High in that structural window and then receives the already-approved rounded frozen spread buffer;
- AutoLot sizes from the final hard SL so configured risk percentage is preserved subject to broker lot constraints.

## Preserved historical rule incorporated into successor
The SELL spread-buffer rule itself remains approved and is carried forward unchanged into the successor decision:

`SpreadBufferPips = max(2.0, ceil(CurrentSpreadPips))`

with the spread frozen from the same entry/preflight `RiskValidationSnapshot` and `MaxSpreadPips` remaining an entry rejection filter rather than an SL buffer.

## Governance
- Do not implement this file as a standalone patch.
- Use only the successor decision as the active engineering contract.
- This file remains solely to preserve decision history and why the queue changed.
