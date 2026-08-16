# M21 Money Management Contract

Status: LOCKED for the P0 architecture-repair cycle.

## Role
M21 is a sizing-only module. It consumes a fully validated M15–M17 decision plus the frozen `RiskValidationSnapshot` and returns either one broker-valid lot size or failure.

M21 MUST NOT:
- create, change, widen, tighten, normalize, or replace Entry, SL, or TP;
- change signal type or direction;
- consume M18 score/level/SignalMode as a risk multiplier or gate;
- query a later account/broker state and mix it with the frozen risk snapshot;
- clamp an invalid FixedLot or below-minimum AutoLot into a different trade size.

## AutoLot mode
`MMMode == 1` only.

The approved formula is:

`risk_amount = snapshot.Equity * AutoLotPercent / 100`

`risk_per_lot = abs(decision.EntryPrice - decision.StopLoss) * snapshot.TickValue / snapshot.TickSize_Price`

`raw_lot = risk_amount / risk_per_lot`

The lot is rounded DOWN to `snapshot.LotStep`. Rounding up is forbidden because it can exceed the requested risk percentage.

The resulting lot must satisfy all of:
- `lot >= snapshot.MinLot`;
- `lot <= snapshot.MaxLot`;
- `lot <= MaxAutoLot`;
- exact broker lot-step validity under the frozen snapshot.

If the risk-based lot is below minimum lot, above the effective maximum, cannot be quantified, or the snapshot is invalid, M21 fails closed. It does not force min lot or silently cap an oversized lot.

`MaxAutoLot` applies only to AutoLot mode.

## FixedLot mode
`MMMode == 2` only.

`FixedLot` is explicit user intent and must already satisfy broker min/max/step constraints. M21 does not normalize or clamp it. Invalid FixedLot fails closed.

## Atomic snapshot rule
M21 uses the same frozen decision/snapshot pair that is subsequently checked by M19. `snapshot.EntryPrice` and `snapshot.StopLoss` must still match the M17-approved decision payload within broker-point tolerance.

Live `AccountEquity()`, live `GetMaxLot()`, live `GetLotStep()`, and similar re-queries are not permitted inside the sizing calculation because they can make one decision produce different lots across ticks.

## Mode validation
Only modes 1 and 2 are valid. Unknown values may not fall through to FixedLot behavior.

Initialization must reject:
- invalid MMMode;
- non-positive AutoLotPercent in AutoLot mode;
- non-positive MaxAutoLot in AutoLot mode;
- non-positive FixedLot in FixedLot mode.

## Failure behavior
M21 returns `valid=false` and lot `0`. Downstream orchestration maps that to `REJ_INVALID_LOT`.

## Ownership boundary
M17 owns Entry/SL/TP.
M21 owns lot calculation only.
M19 owns prospective risk approval using the returned lot.
M20 owns portfolio admission/protection state.
M22 owns order execution.
