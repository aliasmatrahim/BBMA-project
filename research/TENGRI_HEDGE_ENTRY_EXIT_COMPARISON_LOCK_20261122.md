# Tengri Hedge Entry/Exit Comparison — Research Lock

Date: 22 Nov 2026  
Status: **Protocol locked; comparative run in progress**  
Branch: `research/tengri-bbma-hedge-replay-20261122`

## Objective

Compare the installed H4 Mid-BB + ADX(14)>25 + DI Hedge trigger with fixed, sourceable combinations that may improve entry timing and reversal exit timing. The target is an insurance overlay for a Tengri basket already under adverse pressure, not a standalone BBMA strategy. Results are exploratory on a previously studied window; they cannot establish a production winner or be called out-of-sample.

## Candidates fixed before the new comparison

### Entry variants

| ID | Entry condition |
|---|---|
| E0 — Installed control | Closed H4 close on Hedge side of Mid-BB(20,2), ADX(14)>25, DI aligned with Hedge side. |
| E1 — ADX context + BBMA | Keep E0's H4 context active; trigger on a confirmed H1 Build 5.16 Re-Entry event in the Hedge direction (Type 1–4 separately). Do not accept a stale or candidate event. |
| E2 — Structure + retest | Confirm H4 and H1 swing breaks in the Hedge direction; enter only after an M15 retest of the broken level and a closed M15 continuation candle. |
| E3 — Hybrid | Require E0's H4 Mid-BB/ADX/DI context plus H1 directional structure; use the same M15 retest/continuation trigger as E2. |

Build 5.16's currently pinned M12 Re-Entry producer is H1-only; M15 Re-Entry is not assumed. E2/E3 use price structure on M15, not an unverified BBMA M15 Re-Entry event.

### Exit variants

| ID | Exit condition |
|---|---|
| X0 — Installed control | Closed H4 Mid-BB recross against the Hedge; immediate safety close if Tengri net exposure is flat or changes direction. |
| X1 — Structure recovery | Closed H1 swing break back toward current Tengri net direction, confirmed by an M15 close/continuation in that direction; same immediate safety close. No D1/H4 trend-owner gate is imposed on exits. |
| X2 — BBMA recovery | Closed M15 CSAK back toward Tengri direction (close beyond Mid-BB and MA5 High/Low on the appropriate side), plus H1 swing break confirmation; same immediate safety close. This uses the user's clarified CSAK close rule and is a research definition, not a currently implemented Hedge event. |

For entry timing, first replay E0–E3 with the common X0 exit. For exit timing, compare X0–X2 using the predeclared E2 and E3 entries. E1 Type 1–4 stays separately reported under X0; it must not be merged into a single favorable type. A second pass may measure X2 only after its signal formula receives a source-level/event audit; do not call it validated BBMA if that audit fails.

## Shared execution and risk rules

- Same frozen Tengri ledger, HFM Demo4 quote/tick archive, period 1 May–18 Nov 2026, and 4,000 USC anchor.
- Same-symbol Hedge opposite Tengri net exposure only; require at least six Tengri orders on the net side; target 25% of net lots, rounded down. Hedge P&L does not resize later frozen Tengri orders.
- Closed bars only. Entries use the first fresh quote at or after signal confirmation; no look-ahead or stale-signal carry. H4 context can persist only while its closed-bar condition remains active.
- Same actual Bid/Ask execution, entry spread cap 3 pips, 1 pip/lot/action base Hedge cost, and +1 pip/lot/action stress. Do not deduct spread twice.
- One active Hedge campaign per symbol; no Hedge martingale/grid. Trim only if Tengri exposure falls. Include open Hedge mark-to-market at cutoff.
- Report per pair and combined account: campaigns/tickets, eligible/blocked signals, expectancy, PF, realized and floating Hedge P&L, combined floating and equity drawdown, costs, exits by reason, and holding duration.
- Record entry delay from first qualifying close and exit delay from first qualifying reversal event. These quantify timing; higher P&L alone does not prove greater signal precision.

## Limits and decision rule

- The current installed EA remains ADX/H4 and does not consume BBMA events. This work is offline research only: no EA activation, live/forward orders, or Tengri modifications.
- The release identity conflict (source Build 5.16 vs `EA_RELEASE_IDENTITY.json` Build 4.59), ledger-to-Tengri-executable crosswalk, full path-dependent lot feedback, margin/stop-out, broker commission/swap, and fill failure remain open validation issues.
- Previous structure and Type 1–4 results used related but not identical execution/exit models. Treat them as hypotheses, not directly ranked winners.
- Do not tune thresholds or choose a winner on this May–November sample. If one candidate survives this fixed comparison, require a separately identified untouched period and margin/fill model before considering any implementation.
