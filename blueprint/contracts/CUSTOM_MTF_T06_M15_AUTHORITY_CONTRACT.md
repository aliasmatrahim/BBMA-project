# Custom MTF T06 — M15 Read-Only Authority Contract

Date: 2026-11-14  
Task: `T06-M15-READONLY-AUTHORITY-01`  
Status: **ENGINEERING MAPPING SET FOR READ-ONLY IMPLEMENTATION; VALIDATION HOLD**  
Authority: the user directed that the five open arbitration decisions be settled and a read-only M15 consumer be built. The policies below are engineering mappings for Custom MTF; they do not change BBMA source rules or canonical M15 behavior.

## 1. Decision cadence

- Consume only a committed, accepted `CustomEventBatch` with `eventCount > 0`.
- Produce at most one M15 authority receipt per resolved symbol and batch ticket.
- A result is selectable only when the T05 result is satisfied and its selected physical Trigger anchor is present in that result's fresh-anchor set and in the same batch's continuous closed-bar event.
- Re-observing a batch or reading a persistent Context does not create a new trigger. Persistent reservation/consumption is T07.
- This cadence applies only to the Custom path. Canonical M15 processing cadence and signatures remain unchanged.

## 2. M11 D1 strategic gate and direction conflict

- Require the same-symbol M11 `D1MajorTrendOwner` to be valid, confirmed BUY or SELL, and bound to the latest fully closed D1 candle supplied by the current source snapshot.
- `D1_TRANSITION`, `D1_OWNER_UNRESOLVED`, invalid/stale D1 identity, or a direction/state mismatch yields no selected receipt.
- Apply the M11 direction filter before arbitration. Candidates in the opposite direction are removed.
- If contradictory BUY and SELL candidates remain after the M11 filter, fail closed with no selection. Hedging configuration does not bypass this M15 new-entry gate.
- The full M11 owner snapshot is copied into the receipt for later M16 verification; T06 does not recompute the MA50 rule.

## 3. Candidate and slot arbitration

- Among D1-compatible satisfied results with valid fresh anchors, prefer the candidate whose selected physical Trigger event is latest.
- For equal event times, prefer timeframe order `D1 > H4 > H1 > M30 > M15 > M5 > M1`, then ascending signal string, then ascending opaque owner event ID.
- If same-direction results share the winning physical anchor, the lowest numeric slot ID is the primary attribution; all such slot IDs are retained as secondary matches. This is stable engineering bookkeeping, not BBMA quality ranking.
- Slot ID is considered only after physical anchor identity/time is resolved. No `CustomN_Priority` input is added.
- This rule chooses one selected receipt only. It does not reserve or consume any losing or alternative anchor; T07 consumes the original exact T05 snapshot together with the matching batch/config revision.

## 4. OR witness and fresh-anchor ordering

- Within a Context OR group, prefer the latest owner confirmation time; ties use the same high-to-low timeframe order, ascending signal string, then ascending event ID.
- Within a Trigger OR group and across simultaneous fresh Trigger groups, prefer the latest physical event time: `entryEventTime` when positive, otherwise the current closed `sourceBar`.
- Trigger ties use high-to-low timeframe order, ascending signal string, then ascending owner event ID.
- The selected fresh owner must be a Trigger component in the winning witness. Other fresh alternatives remain in `freshAnchors` for later T07 reservation.
- These are deterministic Custom MTF witness-selection mappings only. They do not change source detector formulas, owner lifecycles, signal maturity, or entry windows.

## 5. Read-only M15 receipt and M16 boundary

The new `CustomM15AuthorityReceipt` contains:

- resolved symbol, committed batch ticket/time, exact admitted configuration revision;
- selection state/reason, direction, primary slot, same-anchor matching slot IDs;
- selected anchor ID and the complete selected `CustomWitness`;
- frozen same-symbol M11 D1 owner snapshot;
- `m16RevalidationRequired=true` for a selection and `executionAuthority=false` always.

The receipt is not `BBMA_Decision`, does not call canonical M15 or M16, and does not invoke reservation, risk, SL/TP, OrderSend or trade lifecycle. A selected read-only receipt is not an executable candidate. M16 must later verify the exact witness and frozen M11 identity before downstream use.

## 6. Fail-closed owner boundaries

- Current semantic availability remains OFF. The consumer cannot select a T05 result while its view availability/entry gates remain false.
- RE/EXT/MOM receipts do not open owner availability.
- MHV/MLV formation remains setup-only, never a Trigger via this contract; SIG-06/T04-E owner-epoch/recovery remains a separate HOLD.
- CSA/CSAK fresh-event identity remains unresolved; neither may become a Trigger through this contract.
- Missing or mismatched signal/owner snapshot returns WAIT/no selection. No fallback signal, timeframe, current/live candle, prior direction or fabricated epoch is permitted.

## 7. Validation state

No compile, regression, static harness or runtime is performed in this milestone under the user's validation HOLD instruction. The implementation remains **NOT VERIFIED** until those checks are separately authorized and run with captured evidence.
