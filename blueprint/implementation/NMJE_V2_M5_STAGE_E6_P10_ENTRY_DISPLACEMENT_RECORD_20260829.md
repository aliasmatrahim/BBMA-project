# NMJE v2 / M5 Stage-E6 P10 Entry-Displacement Record — 2026-08-29

## Scope

Measure entry displacement for research after a trade has already been sent and
the exact broker ticket has been selected. P10 does not add an entry-distance
filter, delay, rejection, score, candidate input, or execution authority.

## Frozen price chain

- Source confirmation price: exact confirmed Re-Entry lifecycle selected by
  the P9 semantic source.
- Validation entry price: frozen broker-side entry used by M17/risk preflight.
- Broker execution price: exact `OrderOpenPrice()` from the selected ticket.
- Structural anchor: exact source-owned Re-Entry lifecycle anchor used by M17.

Directional price movement is emitted in pips for source-confirmation to
validation, validation to execution, and structural-anchor to execution.
Positive values mean movement farther in the trade direction.

## Classification

- `FLAT`: validation-to-execution movement is within half a broker point.
- `FAVORABLE`: the broker fill improved against the trade direction.
- `ADVERSE`: the broker fill extended in the trade direction.
- `UNRESOLVED`: exact source, broker fill, point, or pip identity is unavailable.

The classification is descriptive only and carries no threshold beyond the
half-point equality tolerance.

## Durability and recovery

- P10 fields persist under the existing execution hash/ticket/open-time identity.
- Attribution storage version 2 adds P10 keys while version-1 P4-P8 records stay
  readable with displacement marked unresolved.
- Missing/corrupt P10 attribution never changes trade recovery, lifecycle,
  eligibility, risk, execution, management, or closed-order handling.
- Exact closed-order outcomes emit the persisted price chain, directional pip
  deltas, classification, and realized net result.

## Authority boundary

- Existing execution-deviation safety remains unchanged and authoritative.
- M15 remains the sole final-decision clock; M22 remains OrderSend owner.
- NMJE execution authority, D1TPW, and C044 remain disabled.
- No W1, M30, primary M1, ATR, volatility, or non-BBMA logic is introduced.
- PR remains draft; no activation or merge authorization.

## Build and evidence

- Header: `Version 4.6.9 - NMJE v2 Entry Displacement Telemetry`
- Property: `4.69`
- Full N3 and M5 Stage A-E6 regression/static suite PASS.
- Python compile and N3 static guard PASS.
- Native MT4 MetaEditor: `Result: 0 errors, 0 warnings, 426 msec elapsed`;
  EX4 refreshed at 581,216 bytes.

