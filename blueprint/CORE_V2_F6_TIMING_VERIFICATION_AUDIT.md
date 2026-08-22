# CORE-V2-F6 — Re-Entry Validation-Candle / Entry-Candle Timing Verification

Date: 2026-08-22
Status: **STATIC TIMING VERIFIED / METADATA CORRECTED — NO EXTRA ENTRY DELAY ADDED; NATIVE METAEDITOR + RUNTIME ORDER-TIME TRACE STILL REQUIRED**
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

## Metadata correction
`ReEntryData.EntryCandle` previously equalled `ConfirmationCandle`, which was misleading even though runtime execution timing was already next-candle. F6 changes **metadata only**:
- `ConfirmationCandle = data.candle_time`;
- `EntryCandle = data.candle_time + source timeframe seconds`.

`EntryCandle` is not consumed by strategy eligibility or execution authority elsewhere, so this correction does not alter signal qualification, ordering, SL/TP, lot, risk or OrderSend timing.

## Classification
- first validation / second entry wording: **DIRECT FINALE CLARIFICATION**;
- proof that current architecture already satisfies it: **PROJECT STATIC EXECUTION-MAPPING VERIFICATION**;
- EntryCandle timestamp correction: **OBSERVABILITY/METADATA REPAIR ONLY**.

## Remaining verification
1. Native MetaEditor compile: **0 errors / 0 warnings** for integrated F1-F6 source.
2. Runtime trace must record at least one Re-Entry where `ConfirmationCandle < OrderOpenTime()` and `OrderOpenTime()` falls inside the immediately following source-TF candle.
3. Do not add an extra full-candle delay unless runtime evidence contradicts this mapping.

Source basis: `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` F-07 and `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-11.
