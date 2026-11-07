# CORE-V2-F6 — Re-Entry Validation-Candle / Entry-Candle Timing Verification

Date: 2026-08-22 (Build 5.15 baseline; see Issue #300 addendum)
Status: **HISTORICAL BASELINE — UPDATED BY BUILD 5.16 ADDENDUM BELOW**
Baseline branch: `blueprint-dev`

## Question

Finale teaches: first Re-Entry candle validates; the second candle is the entry candle. The Core audit required proof before adding any delay.

## Static execution-path proof (baseline)

The integrated EA structurally implemented the intended timing:
1. `GetLatestClosedCandleTime()` only returns a candle after its full timeframe duration has elapsed.
2. M27 processes a pair only when a new **closed M15 candle** becomes available.
3. H1/H4/D1 Re-Entry detection therefore consumes closed source-TF data; `ConfirmReEntryState()` records that closed candle as `ConfirmationCandle`.
4. After M13/M14/M15/M16 validation, the same M27 pass may call `RunEntryPreflightAndExecute()` immediately.
5. M22 ultimately calls `OrderSend()` at the current live broker price. Because the validation candle is already closed, that live execution necessarily occurs in the immediately following source-TF candle (subject to normal processing/broker delay).

Therefore the closed-candle architecture maps the source wording as:
`FIRST CLOSED RE CANDLE = VALIDATION -> IMMEDIATELY FOLLOWING LIVE CANDLE = ENTRY WINDOW`.

Adding another mandatory full-candle wait would create a third-candle execution and would be an unsupported extra delay.

## Metadata correction (Build 5.15 baseline)

In the Build 5.15 snapshot audited at the time:
- `ConfirmationCandle = data.candle_time`;
- `EntryCandle = data.candle_time + source timeframe seconds`.

At that snapshot, `EntryCandle` was not consumed by candidate eligibility or execution authority, so the change was metadata-only. That statement describes the historical Build 5.15 state and is superseded by the Issue #300 Build 5.16 addendum below.

## Classification

- first validation / second entry wording: **DIRECT FINALE CLARIFICATION**;
- closed-candle timing mapping: **PROJECT STATIC EXECUTION-MAPPING VERIFICATION**;
- Build 5.15 `EntryCandle` timestamp: **METADATA ONLY AT THAT BASELINE**.

## Build 5.15 baseline verification (historical)

The baseline runtime trace identified a late standalone Re-Entry admission. See the Build 5.16 addendum for the isolated before/after eligibility result. The baseline run was an isolated Strategy Tester run; no live orders were placed.

## Issue #300 — Build 5.16 EntryCandle eligibility gate

Branch: `fix/m12-entry-candle-window-20261107`

### Confirmed issue and minimum patch

Build 5.15 admitted a confirmed standalone Re-Entry later than its recorded entry candle when the H4 owner eventually aligned. In the GBPUSD M15 August 2026 baseline, the H1 confirmation at 06:00 produced an expected entry window of 07:00–08:00, but the order opened at 12:00.

Build 5.16 limits confirmed standalone Re-Entry candidate eligibility to the recorded source-TF `EntryCandle`:
- the candidate must have a valid `EntryCandle`;
- the currently open source-TF candle, `iTime(pair, reEntry.Timeframe, 0)`, must equal `EntryCandle`;
- otherwise the candidate is not built.

This does not mutate or expire the structural M12 Re-Entry state. Its validity and lifecycle remain governed by source-defined structural invalidation and ownership transfer; `candidate.Expiry` remains zero and no generic M12 TTL is introduced. If the entry candle passes without eligibility, that confirmation cannot create a later standalone entry candidate, even while the structural state remains valid.

### Verification evidence

- Python suite: `blueprint/tests` — **73 passed**.
- MetaEditor 5.0.0.2425: canonical Build 5.16 and isolated TESTENV adapter — **0 errors, 0 warnings**.
- Isolated MT4 Strategy Tester Build 1492: GBPUSD M15, August 2026, Model 0 from available M1 history, fixed spread 20; **7 trades**. The 7 baseline timely entries were retained; the late 14 Aug 12:00 trade was excluded.
- Positive-window control: the H1 Re-Entry confirmed 13 Aug 00:00 was admitted at 01:00–01:45 while H4 remained active and SELL-aligned; no later admission appeared after that EntryCandle passed.
- For the late case, the log contains no `[P3M1][RE_ADMIT]` for the 14 Aug 06:00 confirmation. The structural Re-Entry remained `Valid=Y` through 20:45, including after H4 aligned, and still did not become a late entry.
- HST history hashes were unchanged by the run.

### Limits

Model 0 was synthesized from available M1 data, not raw tick-by-tick Bid/Ask history. This isolated test verifies the eligibility timing change only; it is not live-runtime verification and does not support a profitability conclusion.

Source basis: `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` F-07 and `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-11.
