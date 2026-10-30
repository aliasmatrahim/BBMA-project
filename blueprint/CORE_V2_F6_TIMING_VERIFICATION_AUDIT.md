# CORE-V2-F6 — Re-Entry Validation-Candle / Entry-Candle Timing Verification

Date: 2026-08-22
Status: **STATIC ORDINARY-ENTRY TIMING MAPPED / D1O-01 ACTIVATION USE VERIFIED; NO EXTRA ORDINARY ENTRY DELAY; NATIVE + RUNTIME TRACE REQUIRED**
Branch: `blueprint-dev`

## Question
Finale teaches: first Re-Entry candle validates; the second candle is the entry candle. The Core audit required proof before adding any delay.

## Static execution-path proof
The integrated EA already implements the intended timing structurally:
1. `GetLatestClosedCandleTime()` only returns a candle after its full timeframe duration has elapsed.
2. M27 processes a pair only when a new **closed M15 candle** becomes available.
3. H1/H4/D1 Re-Entry detection therefore consumes closed source-TF data; `ConfirmReEntryState()` records that closed candle as `ConfirmationCandle`.
4. After M13/M14/M15/M16 validation, the same M27 pass may call `RunEntryPreflightAndExecute()` immediately.
5. M22 ultimately calls `OrderSend()` at the current live broker price. Because the validation candle is already closed, that live execution necessarily occurs in the immediately following source-TF candle (subject to normal processing/broker delay).

Therefore the existing closed-candle architecture already maps the source wording as:
`FIRST CLOSED RE CANDLE = VALIDATION -> IMMEDIATELY FOLLOWING LIVE CANDLE = ENTRY WINDOW`.

Adding another mandatory full-candle wait would create a third-candle execution and would be an unsupported extra delay.

## EntryCandle timestamp correction
`ReEntryData.EntryCandle` previously equalled `ConfirmationCandle`, which was misleading even though ordinary order timing is already next-candle after closed-source processing. F6 corrects the source-timeframe timestamp:
- `ConfirmationCandle = data.candle_time`;
- `EntryCandle = data.candle_time + source timeframe seconds`.

`EntryCandle` is not a general broker-order timestamp and does not schedule the normal standalone Re-Entry order. **CP14 correction:** the approved M11J D1O-01 path does consume it for D1 Re-Entry opportunity eligibility. When a confirmed D1 Re-Entry installs that opportunity, `UpdateD1OpportunityJourney()` uses `d1RE.EntryCandle` as `ActivationTime`; `BuildD1OpportunityCandidate()` then requires confirmed H1/M15 Re-Entry readiness to be strictly later than activation. The corrected timestamp therefore sets the D1O freshness boundary, consistent with D1O-01's post-activation rule. The previous statement that it was unused by all strategy eligibility was overbroad. This does not add a later full-candle wait to the normal M12/M15 broker-order path.

## CP14 current-owner correction — D1O-01 consumes EntryCandle (2026-10-26)

The Build 5.15 owner code confirms the downstream use: `UpdateD1OpportunityJourney()` sets the D1 RE activation boundary from `EntryCandle` (with the existing source-duration fallback), while `IsFreshOpportunityReEntry()` compares each lower-timeframe RE ready time strictly against that boundary. This affects only the approved D1 opportunity freshness gate. M15 remains final authority, M16 revalidates, and the ordinary order path still uses live broker price after closed-candle processing.

## Classification
- first validation / second entry wording: **DIRECT FINALE CLARIFICATION**;
- proof that current architecture already satisfies it: **PROJECT STATIC EXECUTION-MAPPING VERIFICATION**;
- EntryCandle timestamp correction: **OBSERVABILITY + approved D1O activation-boundary mapping; not a broker-order delay**.

## Remaining verification
1. Native MetaEditor compile: **0 errors / 0 warnings** for integrated F1-F6 source.
2. Runtime trace must record at least one Re-Entry where `ConfirmationCandle < OrderOpenTime()` and `OrderOpenTime()` falls inside the immediately following source-TF candle.
3. Do not add an extra full-candle delay unless runtime evidence contradicts this mapping.

Source basis: `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` F-07 and `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-11.
