# M16 Conflict / Invalidation / Owner-Aware Freshness Contract

## Status
P0 Step 7 architecture contract for Module 16, with M27 routing support and decision-payload support from M15.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference.

## Source rule used in Step 7
The primary BBMA reference states that an Extreme requires reversal-candle confirmation and that **Extremes are no longer valid in the presence of CSM regardless of the position of MA5 outside BB**.

Step 7 therefore connects a temporal CSM invalidation path to Extreme validity. M08 remains the raw Extreme detector; M16 owns the later validity/invalidation overlay.

## Ownership
M16 is conflict/invalidation/freshness authority only.

M16 does not:
- detect a new BBMA strategy signal;
- choose BUY versus SELL priority;
- choose SL/TP;
- calculate lot/risk;
- execute orders.

Owner state remains:
- M09 -> persistent MLV lifecycle;
- M12 -> persistent Re-Entry lifecycle;
- M08 -> raw Extreme detection semantics;
- M16 -> persistent validity overlay for detected Extreme plus final component invalidation checks.

## Persistent Extreme validity overlay
PairState now stores independent H1/H4 x BUY/SELL Extreme validity snapshots:
- `extreme_h1_buy_state`;
- `extreme_h1_sell_state`;
- `extreme_h4_buy_state`;
- `extreme_h4_sell_state`.

A new M08-detected Extreme may populate/replace the matching slot. M16 then applies:
1. timeframe-aware project expiry using `MaxWaitBars_Extreme * timeframe * 60`;
2. later CSM invalidation.

This does not turn M16 into an Extreme detector. The slot can only originate from an M08-valid Extreme snapshot.

## CSM -> Extreme temporal invalidation
Operational encoding for the source sentence is:
- CSM must be a source-valid CLOSED CSM from M10;
- CSM must be on the **same timeframe** as the stored Extreme;
- CSM candle time must be later than the Extreme candle time;
- the source sentence does not qualify the invalidation by CSM direction, so no additional same-direction requirement is invented.

M27 builds H1/H4 CSM-presence snapshots by checking the source-aligned M10 CSM detector before the BUY/SELL candidate loop, then passes that temporal evidence to M16's Extreme validity overlay.

This same-timeframe/later-closed-candle mapping is an engineering translation of the source rule, not a verbatim algorithm from the PDF.

## Expiry is not invalidation
Step 7 explicitly separates:
- `EXPIRED` -> owner/project time window ended;
- `INVALIDATED` -> owner state no longer matches or a strategy invalidation such as later CSM removed the Extreme.

An Extreme invalidated by CSM must not be mislabeled as time-expired.

## Decision component identity
`ValidatedSequenceCandidate` now carries explicit `ComponentCount`.

M15 forwards the selected candidate payload into `BBMA_Decision`:
- `ComponentCount`;
- `Components[3]`;
- `CandidateExpiry` when explicitly supplied by the owner.

This allows M16 to validate the exact component identity chosen by M15 rather than infer validity from `decision.CandleTime` or `CycleStartTime`.

## Owner-aware component validation
Before a created decision can become `DEC_VALIDATED`, M16 checks every selected component against the current owner state.

### Re-Entry component
Valid only when the matching H1/H4/D1 + BUY/SELL M12 slot is still:
- `RE_STATE_CONFIRMED`;
- `IsValid == true`;
- same direction/timeframe;
- same `ConfirmationCandle` as the decision component;
- not past explicit `ExpiryCandleTime`.

### MLV component
Valid only when the matching M15 + BUY/SELL M09 slot is still:
- `MLV_CONFIRMED`;
- `IsValid == true`;
- same direction;
- same `ConfirmationCandleTime` as the decision component;
- not past explicit `ExpiryCandleTime`.

### Extreme component
Valid only when the matching persistent M16 H1/H4 + BUY/SELL slot is:
- still `Valid`;
- same type/direction/timeframe/candle identity;
- not past the timeframe-aware Extreme project expiry;
- not invalidated by a later same-timeframe CSM.

If one required component is no longer owner-valid, the assembled Re-Entry/REM/RRE/REE decision cannot proceed.

## Removal of legacy generic expiry
M16 no longer expires a decision using:
- `decision.CandleTime + MaxWaitBars_Global * 900`;
- `decision.CycleStartTime + MaxWaitBars_Global * 900`.

The old generic helpers that assumed one universal M15/global time basis for Signal/MLV/Re-Entry are removed from the M16 path.

Freshness now comes from the real owner state and timeframe.

## Opposite direction conflict
Step 6 already resolves simultaneous eligible BUY + SELL conservatively by producing **no created trade decision**.

M16 preserves that architecture. If a direction conflict ever reaches M16 together with a created decision, M16 invalidates it; M16 does not invent a winner.

## Broker guard removed from M16
The old `g_broker_initialized` rejection inside M16 is removed because broker readiness is not BBMA signal invalidation ownership. Broker/risk/execution readiness remains downstream.

## Scope guard / remaining blockers
Step 7 does not certify or repair:
- standalone Extreme reversal-candle + retest entry lifecycle;
- M17 entry-price / SL / TP source resolution;
- M17 direction-aware stop/TP validation;
- risk/portfolio semantics;
- execution/recovery logic.

The next P0 target is M17.

## Implementation record
Patch:
`blueprint/patches/0014-p0-step7-m16-owner-aware-invalidation.patch`

Patch commit:
`b7a4c255d19bdfb92323a9e4ba86bb0ce15aa9c9`

Focused patch SHA-256:
`d333b64594eb563c3013776e36d3ab967041be471f7b45206fb73d466adc034a`

## Verification
Focused post-Step6 verification:
- patch dry-run/apply: clean;
- applied output exact-match to generated Step 7 target;
- braces: 502 / 502;
- parentheses: 1538 / 1538;
- brackets: 353 / 353;
- legacy generic decision/cycle expiry formulas absent from M16;
- legacy generic `IsExpired_Signal`, `IsExpired_MLV`, `IsExpired_ReEntry` helpers absent from the active focused region;
- decision component payload forwarding present;
- owner snapshot validator present;
- persistent H1/H4 Extreme validity overlay present;
- later same-timeframe CSM invalidation path present;
- M16 call receives explicit `pairIndex` instead of inferring PairState from broker symbol text.

This remains focused verification. A new complete full-chain working-source SHA is not claimed until the entire ordered patch chain is exactly materialized in one source file.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
