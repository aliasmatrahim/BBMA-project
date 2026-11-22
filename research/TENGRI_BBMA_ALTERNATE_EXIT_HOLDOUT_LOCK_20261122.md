# Tengri + BBMA Hedge — alternate exit holdout lock

Date locked: 22 Nov 2026  
Status: **PRE-REGISTERED — before calculating holdout P&L**  
Branch: `research/tengri-bbma-hedge-replay-20261122`

## Purpose

Evaluate one alternative Hedge exit on a non-overlapping historical holdout. The previously locked May 1–Nov 18 sample is closed to further performance selection. No parameter sweep or same-sample retuning is allowed.

## Holdout window

- **2026-04-06 00:00 through 2026-05-01 00:00 UTC**, including the last available quote before the end time.
- This is a pre-window holdout relative to the May–Nov locked replay. It was selected from date coverage only; no April strategy P&L or signal counts were examined when selecting it.
- G40 has quote files for EURUSD and USDCHF on all 19 weekdays in the interval (plus the archived Sunday market sessions). The frozen Tengri ledger begins on Apr 6 and has no earlier opened positions. Final data-quality and time-alignment gates remain to be checked.
- First account contribution is recorded as **3,578 USC at 2026-04-06 14:28:20**, immediately before the first Tengri orders. Treat it as initial capital; subsequent external cash flows within the window remain flows. Report absolute USC results and percent returns against this anchor.
- If tick coverage, event export, or ledger time alignment fails for either symbol, mark the holdout **INVALID** and do not report performance.

## Frozen entry rules

Run each BBMA H1 Re-Entry Type 1, 2, 3, and 4 independently for EURUSD and USDCHF. Keep the existing locked entry rules unchanged:

- Entry event must be closed-candle, source-confirmed, and pass the D1/H4/M15 entry-approval path.
- Hedge opposes same-symbol current Tengri net exposure.
- Require at least six Tengri orders on the net side.
- Target 25% of net lots, rounded down to the 0.01-lot step.
- Entry spread cap: 3 pips. Use the first valid quote at or after the first M15 decision row following the confirmed H1 event.
- No cross-pair hedge. Trim to target as Tengri net exposure shrinks.

## Single alternate exit

- Close the open same-symbol Hedge at the first source-confirmed, closed H1 Re-Entry Type 1–4 candidate whose direction is back toward the **current** Tengri net direction.
- For this exit only, do not require the D1/H4/M15 entry-approval flag. The exit closes existing Hedge exposure and cannot open or add a position.
- The event must still be a confirmed H1 Re-Entry from the pinned Build 5.16 source; do not use candidate/unconfirmed lifecycle states.
- Execute at the first valid HFM quote at or after its first M15 decision row.
- Keep the locked safety close: close immediately if Tengri becomes flat or its net direction changes so that the Hedge is no longer opposite. Safety close takes precedence if it occurs on the same event/quote.
- All Types 1–4 use this same alternate exit.

The existing event CSV stores only a combined `d1_h4_m15_approved` flag. This lock therefore bypasses that combined entry-approval flag for exit candidates; it cannot isolate D1/H4 from M15 rejection reason.

## Costs and reporting

Keep the prior cost model exactly:

- Execute entries and exits on actual Bid/Ask quotes.
- Base added cost: 1 pip per lot per Hedge action.
- Stress added cost: 2 pips per lot per Hedge action.
- Entry spread cap remains 3 pips; no new spread, lot, or layer settings.

Report per Type, pair, and combined:

- Hedge and account net P&L, including mark-to-market of open Hedge positions;
- closed campaigns, wins/losses, expectancy, and profit factor;
- maximum flow-adjusted equity drawdown and worst combined floating P&L;
- action counts and modeled costs, with stress result;
- end-open exposure and any invalid/missing data.

Use the frozen Tengri order stream; Hedge P&L does not feed back into subsequent Tengri lots. Margin/stop-out, broker-specific commission/swap, rejected/partial fills, and ledger-to-executable provenance remain limitations. Results are conditional historical overlay research, not production EA performance.

## Integrity gates before performance replay

1. Pin/hash the exact Build 5.16 source and test executable used for the April event export.
2. Export all source-confirmed April H1 Re-Entry candidates, retaining the approval flag for entry gating only.
3. Verify HFM quote-file counts, ordering, Bid/Ask validity, and timestamp alignment for both pairs over the full window.
4. Verify D1/H4/H1/M15 warm-up spans April 6 and owner state is reconstructed without look-ahead.
5. Verify the frozen Tengri order timeline, first contribution anchor, and end-of-window open positions.
6. Run the single locked comparison once. If any gate fails, stop at the diagnostic and do not substitute a different period after seeing performance.

No EA source changes, production activation, live/forward orders, or merge are included.
