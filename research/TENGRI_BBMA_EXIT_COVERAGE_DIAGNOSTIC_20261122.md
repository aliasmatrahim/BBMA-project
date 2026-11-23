# Tengri + BBMA Hedge — exit coverage diagnostic

Date: 22 Nov 2026  
Status: **Completed — event-coverage diagnostic only; no new P&L replay**  
Branch: `research/tengri-bbma-hedge-replay-20261122`

## Question

The locked May 1–Nov 18 replay reported zero normal H1 Re-Entry exits for Types 1–4. This audit checks whether that came from missing events, signal timing, or the combined D1/H4/M15 approval gate.

## Method

Read-only audit of the existing locked replay result, its campaign records, and the Build 5.16 signal-event CSV on G40. No EA, entry rule, exit rule, cost, or locked performance result was changed or rerun.

For each closed campaign, the opening event was matched by symbol and type within five minutes before the recorded open. Any opposite-direction H1 Re-Entry candidate during the campaign was counted as pointing back toward the Tengri net direction. Candidate events were separated by the CSV's `d1_h4_m15_approved` flag. This flag is combined; it does not identify which individual gate rejected an event.

## Event-stream totals

| Type | Candidate rows | Approved | Not approved |
|---|---:|---:|---:|
| Type 1 | 74 | 42 | 32 |
| Type 2 | 0 | 0 | 0 |
| Type 3 | 81 | 41 | 40 |
| Type 4 | 127 | 71 | 56 |
| **Total** | **282** | **154** | **128** |

## Campaign-window findings

| Variant | Pair | Closed campaigns | Approved candidates back toward Tengri | Not-approved candidates back toward Tengri | Campaigns with at least one not-approved candidate |
|---|---|---:|---:|---:|---:|
| Type 1 | EURUSD | 4 | 0 | 9 | 3/4 |
| Type 1 | USDCHF | 4 | 0 | 11 | 3/4 |
| Type 3 | EURUSD | 4 | 0 | 9 | 3/4 |
| Type 3 | USDCHF | 4 | 0 | 4 | 2/4 |
| Type 4 | EURUSD | 5 | 0 | 10 | 4/5 |
| Type 4 | USDCHF | 5 | 0 | 3 | 1/5 |
| **Total** |  | **26** | **0** | **46 observations** | **16/26** |

The 46 observations represent 21 unique event hashes across campaign windows. Type 2 had no approved entry events and no campaigns. The locked replay's per-pair counters also show `exit_reentry_signals = 0` for every type; it ended with four Hedge campaigns still open.

## Interpretation

- The locked exit rule was not exercised because no approved, fresh H1 Re-Entry event toward the current Tengri direction occurred while a Hedge campaign was open.
- This is not evidence of stale-event blocking: the replay logged zero stale entry-signal blocks. The campaign-window cross-check independently found zero approved opposite-direction events.
- The combined approval gate is a plausible reason exits were absent: 21 unique unapproved candidates pointed back toward Tengri during exposure windows. The data does not say whether D1, H4, M15 arbitration, or another combined check rejected each candidate.
- This result does not establish that exiting on an unapproved candidate is profitable, safer, or preferable. It only shows that the locked normal exit rule had no coverage on this sample.

## Next valid test

Do not rerun or retune the May–Nov 18 locked P&L sample. For a new independent holdout, freeze entry rules and costs, then compare the locked exit against one declared alternative: exit on the first confirmed opposite-direction H1 Re-Entry candidate even when the D1/H4 entry-approval flag is false; retain the same Tengri-flat/net-side-flip safety close. Report Types 1–4 separately. If an independent Tengri path and matching quotes/ticks are unavailable, stop at event coverage and do not report performance.

This remains research-only. Build 5.16 versus 4.59 identity records, the Tengri ledger-to-executable crosswalk, reconciliation residuals, and broker margin/commission/swap/fill behavior remain unresolved. The installed G40 Hedge remains ADX/H4-based and does not consume BBMA events. No EA changes, live/forward trading, or merge occurred.
