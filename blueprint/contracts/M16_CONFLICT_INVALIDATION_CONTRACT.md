# M16 Conflict / Invalidation / Owner-Identity Contract

## Status
P0 Step 7 architecture contract for Module 16, reconciled 2026-08-24 with the D1 strategic-owner specification.

The BBMA source hierarchy governs strategy semantics. `Oma ally BBMA - AL.pdf` remains the primary operational reference. M11 now owns D1 strategic major-trend classification; M16 may verify its frozen identity but must not create a second trend formula.

## Source rule used in Step 7
The primary BBMA reference states that an Extreme requires reversal-candle confirmation and that Extremes are no longer valid in the presence of CSM regardless of MA5 being outside BB.

The original Step 7 contract therefore connected temporal CSM invalidation to Extreme validity. That ownership remains unchanged.

## Ownership
M16 is conflict / invalidation / exact-owner revalidation authority only.

M16 does not:
- detect a new BBMA strategy signal;
- compute D1 major trend independently;
- choose BUY versus SELL priority;
- choose SL/TP;
- calculate lot/risk;
- execute orders;
- close live broker positions merely because D1 becomes transitional.

Owner state remains:
- M08 -> Extreme detector/maturity source state;
- M09 -> persistent MHV/MLV lifecycle;
- M10 -> direction/Momentum producer;
- M11 -> D1 major-trend strategic owner;
- M12 -> persistent Re-Entry lifecycle;
- M16 -> final selected-decision component + strategic-owner revalidation before downstream execution.

## D1 strategic-owner revalidation
Any M15-created new-entry decision must carry a frozen M11 D1 owner snapshot/identity sufficient for M16 to verify that the decision still belongs to the same strategic state.

Conceptual required identity:
- D1 owner state;
- D1 owner direction;
- latest closed D1 candle time;
- D1 close;
- current closed-D1 MA50;
- previous closed-D1 MA50.

M16 must verify:
1. the frozen D1 state was `D1_OWNER_BUY_CONFIRMED` or `D1_OWNER_SELL_CONFIRMED`;
2. frozen owner direction equals `decision.Direction`;
3. the decision's D1 snapshot corresponds to the current M11-produced closed-D1 owner for the same processing context;
4. the owner has not become transition/unresolved before the decision proceeds downstream.

If the M11 owner is now `D1_TRANSITION`, `D1_OWNER_UNRESOLVED`, opposite direction, stale or identity-mismatched, M16 must invalidate/reject the created **new-entry decision** fail-closed.

M16 must not recompute price-vs-MA50 slope with its own independent Boolean logic. The sole strategy formula remains in M11.

## D1 gate is separate from component identity
The D1 major-trend owner is not inserted as another REM/RRE/REE structural component.

Exact signatures remain:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M16 must distinguish:
- D1 Re-Entry component validity; from
- D1 MA50 strategic-owner validity.

A valid D1 Re-Entry does not automatically prove the M11 strategic owner is confirmed in the same direction.

## Persistent Extreme owner-validity overlay
PairState currently stores independent H1/H4 BUY/SELL Extreme validity snapshots.

Original Step 7 behavior remains:
1. M08-originating source-valid Extreme may populate the appropriate slot;
2. M16 verifies exact current owner identity/structural validity and adds no fixed-age Strategy-Core TTL;
3. later same-timeframe closed source-valid CSM may invalidate the stored Extreme according to the source contract.

This does not turn M16 into an Extreme detector.

Future D1 Extreme lifecycle support required by the separate F7 lifecycle work remains a different implementation task and must not be confused with the D1 MA50 strategic-owner gate described here.

## CSM -> Extreme temporal invalidation
Operational encoding remains:
- CSM must be source-valid and closed;
- same timeframe as stored Extreme;
- later than the Extreme candle;
- no unsupported extra direction qualification is invented when the source sentence does not provide one.

## Structural invalidation is not age expiry
Extreme and Re-Entry Strategy-Core validity is structural. M16 must not mark an otherwise source-valid Extreme or Type 1/2/3/4 Re-Entry invalid merely because a generic project candle window elapsed.

`EXPIRED` may remain an enum/compatibility state for an explicitly owned non-Core expiry contract, but `MaxWaitBars_Extreme` and generic `MaxWaitBars_ReEntry` are not Strategy-Core death authority.

D1 transition/opposite-owner failure is a strategic-owner eligibility failure for a pending new-entry decision, not a generic time expiry.

## Decision component identity
`ValidatedSequenceCandidate` / `BBMA_Decision` component identity remains the basis for exact selected-setup verification.

M16 validates the exact selected components rather than inferring validity from generic decision timestamps.

## Owner-aware component validation
### Re-Entry component
Valid only when the matching H1/H4/D1 M12 slot remains:
- confirmed;
- valid;
- same direction/timeframe;
- same confirmation-candle identity;
- still source-valid under the M12 structural owner contract; no generic fixed-age TTL is added by M16.

### MHV/MLV component
Valid only when the matching M09 owner state remains at the required maturity/identity for the selected decision.

### Extreme component
For REM/REE component use, the matching owner snapshot must remain source-valid, same type/direction/timeframe/candle identity, and not structurally invalidated/superseded.

For standalone H1 Extreme under Issue #175, M16 revalidates the exact M08 lifecycle rather than treating a reversal-confirmed component snapshot as entry-ready. Required identity is `EXT_MAT_RETEST_READY`, `IsValid == true`, matching H1 direction, valid `RawCandleTime <= RetestCompletionCandleTime`, and exact `RetestCompletionCandleTime == decision component CandleTime`.

M16 does not detect or promote Extreme maturity; it only verifies the owner state selected by M15. If one required structural component is no longer owner-valid, the selected Extreme/Re-Entry/REM/RRE/REE decision cannot proceed.

## D1 transition is not a live-position exit
M16's D1 revalidation applies to **not-yet-executed new-entry decisions**.

It must not directly close a live broker position because D1 moves to transition/opposite major-trend state. Existing positions remain owned by M23/M24 lifecycle plus protective/emergency controls under their own contracts.

## Opposite direction conflict
M15 is the final direction authority and applies the D1 strategic filter first.

If contradictory eligible directions still reach M16 despite one confirmed D1 owner, treat that as an upstream identity/invariant failure and invalidate the decision. M16 does not invent a winner.

## Broker guard
Broker readiness is not M16 strategy invalidation ownership and remains downstream.

## Scope guard
M16 does not own:
- D1 owner production;
- candidate direction filtering/selection;
- M11 MA50 calculations;
- standalone Extreme execution;
- SL/TP;
- risk/portfolio semantics;
- broker execution/recovery;
- live-position strategy close.

## Current owner implementation status — reconciled 2026-10-26
The previous implementation-gap statement is superseded for static status by owner Build 5.15 at `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`.

- M16 consumes a decision created by M15 and revalidates the frozen M11 D1 snapshot before downstream execution.
- M16 does not reproduce the D1 price/MA50 slope formula.
- D1 transition or identity failure blocks the pending entry; it does not create a live-position close rule.

Classification: **STATIC IMPLEMENTATION PRESENT / COMBINED REGRESSION PARTIAL / RUNTIME NOT VERIFIED**.

## Historical implementation record
Patch:
`blueprint/patches/0014-p0-step7-m16-owner-aware-invalidation.patch`

Patch commit:
`b7a4c255d19bdfb92323a9e4ba86bb0ce15aa9c9`

Focused patch SHA-256:
`d333b64594eb563c3013776e36d3ab967041be471f7b45206fb73d466adc034a`

Do not merge to `main` until the current source/spec/runtime gates are reconciled and explicitly approved.

## D1-02 implementation record — `d1-owner-dev`
The 2026-08-24 D1 owner revalidation is implemented on isolated `d1-owner-dev` as build `Version 4.5.1 - D1-02 M15-M16 Strategic Gate`.

- M16 verifies the frozen M15 D1 snapshot against the current M11-produced owner identity.
- Transition/unresolved/opposite/stale/identity mismatch fails closed before structural component revalidation.
- M16 does not duplicate the D1 price-vs-MA50 slope formula.
- D1 strategic failure invalidates only a pending new-entry decision; it is not a live-position close rule.
- Native MT4 MetaEditor: **0 errors / 0 warnings**.
- `blueprint-dev` remains unchanged pending explicit integration approval.

## D1-03 atomic snapshot ownership overlay
M16 continues to revalidate D1 before structural component freshness, but the comparison now uses only the current M11-owned atomic D1 snapshot. It no longer compares frozen decision identity against split raw `d1_data` / PairState MA mirror fields. No D1 trend formula is duplicated and no live-position exit authority is added.
