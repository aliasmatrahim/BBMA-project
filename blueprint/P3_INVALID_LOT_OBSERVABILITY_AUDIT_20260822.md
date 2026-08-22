# P3 — REJ_INVALID_LOT Observability Audit

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **DEFECT CONFIRMED / FIX DESIGN READY / SOURCE CHANGE DEFERRED TO PRESERVE CURRENT RUNTIME CANDIDATE**

## Finding
M21 currently returns `valid=false` / `0` from multiple distinct lot-sizing failure branches. M27 then collapses all of them into the single rejection `REJ_INVALID_LOT`.

This is not a sizing-logic defect by itself, but it materially weakens runtime diagnosis because the log cannot distinguish broker-spec failure, below-min lot, effective max-lot failure, step mismatch, fixed-lot invalidity, or malformed frozen snapshot/payload.

## Distinct failure classes visible in current source
The current `CalculateLotSize()` path can fail for at least:
1. invalid decision/pair/Entry/SL payload;
2. invalid broker snapshot (`Point`, `TickSize`, `TickValue`, `LotStep`, `MinLot`, `MaxLot`, `LotDigits`, `Equity`);
3. frozen payload mismatch between decision and risk snapshot;
4. invalid AutoLot configuration (`AutoLotPercent`, `MaxAutoLot`);
5. non-positive SL distance;
6. non-positive risk-per-lot;
7. non-positive risk amount;
8. normalized auto lot below broker `MinLot`;
9. effective max lot (`min(BrokerMaxLot, MaxAutoLot)`) below `MinLot`;
10. normalized auto lot above effective max lot;
11. auto lot step mismatch;
12. fixed lot non-positive / below min / above max;
13. fixed lot step mismatch;
14. unsupported `MMMode`.

## Minimal fix design
Keep `REJ_INVALID_LOT` as the trading rejection. Add observability-only reason metadata/logging so sizing semantics do not change.

Minimum fields to log on failure:
- `Pair`, `MMMode`;
- `rawLot`, `normalizedLot` where available;
- `MinLot`, `MaxLot`, `LotStep`, `LotDigits`;
- `TickValue`, `TickSize_Price`, `Point`;
- SL distance;
- effective max lot;
- `FixedLot`, `AutoLotPercent`, `MaxAutoLot` as relevant;
- compact reason tag.

Recommended reason tags:
- `BROKER_SNAPSHOT_INVALID`
- `PAYLOAD_INVALID`
- `PAYLOAD_MISMATCH`
- `AUTO_CONFIG_INVALID`
- `SL_DISTANCE_INVALID`
- `RISK_PER_LOT_INVALID`
- `RISK_AMOUNT_INVALID`
- `BELOW_MIN`
- `MAXAUTOLOT_BELOW_MIN`
- `ABOVE_MAX`
- `STEP_MISMATCH`
- `FIXEDLOT_INVALID`
- `MMMODE_INVALID`

## Change-control decision
Do **not** modify the current EA source before P3 Step 5 Tests B–D are captured, because the current build already has native 0E0W + runtime initialization PASS + Test A PASS. A source-only observability patch now would create a new runtime candidate and force a fresh compile/deploy evidence chain.

The fix is ready to implement immediately after the current Step 5 candidate is closed or if the user explicitly chooses to supersede that candidate.
