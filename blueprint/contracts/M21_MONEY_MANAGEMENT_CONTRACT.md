# M21 Money Management Contract

Status: **ACTIVE / LOCKED — compatible with M17-SLRANGE-01**.

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

## M17-SLRANGE-01 compatibility

M21 always sizes from the **final normalized hard SL produced by M17**.

For v4.52 this means the M17 input to M21 may already include:
- BUY: lowest Low across the exact source-owned Re-Entry lifecycle, minus one broker Point, with no spread buffer;
- SELL: highest High across the exact source-owned Re-Entry lifecycle, plus one broker Point and the approved rounded SELL spread buffer.

M21 applies **no second spread adjustment and no independent SL compensation**.

Consequences:
- if the final Entry-to-SL distance increases, AutoLot naturally decreases under the unchanged risk formula;
- if the final Entry-to-SL distance is unchanged, AutoLot is unchanged;
- FixedLot does not shrink automatically and therefore monetary risk may increase with a wider final SL.

This behavior is a consequence of the existing risk-distance formula, not a new lot-sizing strategy.

## FixedLot mode
`MMMode == 2` only.

`FixedLot` is explicit user intent and must already satisfy broker min/max/step constraints. M21 does not normalize or clamp it. Invalid FixedLot fails closed.

## Atomic snapshot rule
M21 uses the same frozen decision/snapshot pair that is subsequently checked by M19. `snapshot.EntryPrice` and `snapshot.StopLoss` must still match the M17-approved decision payload within broker-point tolerance.

M17 resolves and normalizes the final SL before that value is frozen into `snapshot.StopLoss` and before M21 sizing begins.

Live `AccountEquity()`, live `GetMaxLot()`, live `GetLotStep()`, and similar re-queries are not permitted inside the sizing calculation because they can make one decision produce different lots across ticks.

## Mode validation
Only modes 1 and 2 are valid. Unknown values may not fall through to FixedLot behavior.

Initialization must reject:
- invalid MMMode;
- non-positive AutoLotPercent in AutoLot mode;
- non-positive MaxAutoLot in AutoLot mode;
- non-positive FixedLot in FixedLot mode.

## Diagnostics boundary — P2-LOTDIAG-01

`REJ_INVALID_LOT` remains the downstream rejection enum. Observability may attach a reason tag and frozen-snapshot values **after** M21 has already failed, but diagnostics MUST NOT alter sizing or admission.

Approved diagnostic tags include at minimum:
- `BROKER_SNAPSHOT_INVALID`;
- `BELOW_MIN`;
- `ABOVE_MAX`;
- `STEP_MISMATCH`;
- `MAXAUTOLOT_BELOW_MIN`;
- `FIXEDLOT_INVALID`.

Additional explanatory tags may distinguish invalid decision payload, payload mismatch, invalid MM configuration, invalid SL distance/risk-per-lot/risk amount, unknown MMMode, or an otherwise-unclassified failure.

Diagnostic capture may include `rawLot`, normalized lot, `MinLot`, `MaxLot`, effective maximum lot, `LotStep`, `LotDigits`, `TickValue`, `TickSize_Price`, point size, SL distance, Entry, SL, frozen Equity, AutoLotPercent, MaxAutoLot, FixedLot and MMMode.

Hard guard: diagnostics consume only the already-frozen decision/snapshot and user inputs. They may not re-query live broker/account state, clamp/normalize a rejected trade into acceptance, change `CalculateLotSize()`, or replace `REJ_INVALID_LOT` with a new trading decision.

## Failure behavior
M21 returns `valid=false` and lot `0`. Downstream orchestration maps that to `REJ_INVALID_LOT`.

## Ownership boundary
M17 owns Entry/SL/TP and broker-side structural normalization.
M21 owns lot calculation only.
M19 owns prospective risk approval using the returned lot.
M20 owns portfolio admission/protection state.
M22 owns order execution.
