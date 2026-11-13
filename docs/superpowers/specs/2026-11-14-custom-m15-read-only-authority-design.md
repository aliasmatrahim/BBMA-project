# Custom MTF M15 Read-Only Authority — Design

## Intent

Consume the current T05 diagnostic receipt through a Custom M15 authority boundary, select at most one read-only receipt for a resolved symbol and accepted closed-timeframe batch, and preserve the existing M11 D1 gate. This fills T06's missing consumer without activating custom entries.

## Goals

- Make all five T06 arbitration decisions explicit and reproducible.
- Preserve exact symbol, batch, configuration, source-witness, and D1-owner identity.
- Leave canonical M15 cadence/signatures, signal detectors, M16, T07 reservations, risk and execution untouched.
- Keep all 77 semantic availability cells and custom auto-entry OFF.

## Non-goals

- No BBMA signal formula or lifecycle change.
- No M16 consumer, persistent dedup/reservation, trade plan, risk, order or position lifecycle.
- No availability/owner promotion or merge/activation.
- No compile/regression/static/runtime validation in this milestone; prior user direction leaves validation HOLD.

## Approaches

1. **Reuse canonical `BBMA_Decision` and canonical M15 selection.** Rejected: the current canonical pipeline accepts its M11/M12/M14 candidate types; custom formulas/witnesses are not those candidates. Reusing it would alter canonical behavior or require an unapproved conversion.
2. **Select directly inside T05 dispatch.** Rejected: dispatch produces diagnostic results; choosing there would bypass the explicit M15 final-authority boundary.
3. **Add a separate pure Custom M15 consumer after a committed T05 snapshot.** Chosen: it consumes the exact batch/snapshot/config plus same-pair M11 owner and returns an immutable read-only authority receipt. It does not call M16 or execution.

## Decisions

The five selected policies and their exact ordering are normative for this read-only milestone in [the T06 contract](../../blueprint/contracts/CUSTOM_MTF_T06_M15_AUTHORITY_CONTRACT.md):

1. One output per committed nonempty Custom event batch and resolved symbol; candidate needs a fresh physical Trigger event in that batch.
2. Filter through current valid M11 D1 owner first; stale/unresolved/transition blocks, and any contradictory post-filter state fails closed.
3. Choose the latest physical fresh event; then D1→H4→H1→M30→M15→M5→M1, ascending signal, ascending owner ID. Same-anchor same-direction slots use the lowest slot ID as primary and retain all same-anchor matches for attribution.
4. Context OR prefers latest confirmation. Trigger OR/fresh anchors prefer latest physical event (`entryEventTime`, else `sourceBar`), then the same deterministic tie-break.
5. Freeze the exact selected witness, batch/config identity, slot attribution, and full M11 snapshot in a receipt with execution authority permanently false and M16 revalidation required.

These are engineering mappings, not new source-derived BBMA rules. Their trade-plan implications remain subject to T08; the selection is not executable.

## Architecture and files

- `CustomEvaluator.mqh`: use the selected deterministic OR/fresh-anchor ordering.
- `CustomM15Authority.mqh`: pure read-only consumer and receipt; validates batch, config, witness and M11 owner.
- `BBMA_EA.mq4`: include the consumer after T05 types, clear one transient receipt per symbol, call it only after the committed batch and successful T05 dispatch, and assign a unique Build 6.21 identity.
- T05 interface, queue and progress: point to the policy and state that selection remains non-executable/NOT VERIFIED.

## Risks and safeguards

- Stale D1 owner: compare its source candle to the latest fully closed D1 identity from the same resolved symbol; return WAIT on mismatch.
- Duplicate or stale T05 data: match symbol, ticket, observation time, exact config revision, witness fields and fresh-anchor identity before selection.
- Several slot plans on the same anchor: choose lower slot ID only for same-anchor attribution and preserve all matching IDs; later T08 must consume the recorded primary slot.
- Unsupported signal freshness: the receipt validator still requires an explicit fresh anchor; it does not loosen CSA/CSAK or MHV/MLV restrictions.
- M15 output mistaken for an order: `executionAuthority=false`; no `OrderSend`, M16, T07, M17, M21 or lifecycle call exists in this consumer.

## Success evidence for this milestone

- Source and contract are read back at the final immutable commit.
- The consumer is connected only after successful T05 dispatch and the same committed batch.
- Unique Build 6.21/source revision is reflected in header and build log identity.
- Tests/compile/runtime remain explicitly NOT RUN; therefore this is an implementation draft, not a verified T06 acceptance.
