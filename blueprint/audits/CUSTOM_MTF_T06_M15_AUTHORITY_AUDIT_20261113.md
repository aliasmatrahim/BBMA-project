# Custom MTF T06 — M15 Authority / Arbitration Contract Audit

Task: `T06-M15-AUTHORITY-ARBITRATION-CONTRACT-AUDIT-01`  
Date: 2026-11-13  
Branch: `feat/custom-mtf-v1-20261108`  
Base: `d1-owner-dev`  
Starting checkpoint: `f828ad79e396aec70923ad7f56382d9c805f1c69`  
Status: **FIVE ARBITRATION DECISIONS ADOPTED; READ-ONLY CONSUMER DRAFT IMPLEMENTED / NOT VERIFIED**  
Scope: read-only audit. No EA source or build identity changed.

## Findings

### Confirmed authority boundary

- The canonical Module 15 contract makes M15 the sole final new-entry authority. It filters candidates through the M11 D1 owner, rejects contradictory surviving directions, and selects among same-direction canonical candidates by latest component anchor, then latest sequence start, then deterministic sequence hash.
- The approved Custom MTF architecture decision preserves Module 15 as the only custom final authority and limits the clock exception to the future CUSTOM path. Canonical signatures and canonical cadence remain unchanged.
- M15 cannot re-detect source signals or transfer its decision to the parser, evaluator, risk manager, M12N, or execution layer.

These are authority constraints. They do not define the complete custom-slot arbitration policy.

### Current T05 receipt boundary

At the current Build 6.20 branch checkpoint, `DispatchCustomEvaluationSnapshot` stores a transient per-symbol diagnostic snapshot containing the symbol, observation time, committed batch ticket, exact configuration revision, and up to ten slot/direction results with satisfaction reason and witness.

The receipt is not a candidate queue or selected decision. No T06 consumer is connected. The evaluator requires current owner views and a fresh Trigger anchor; the current owner adapters keep execution/eligibility closed. All 77 semantic availability cells and custom auto-entry remain OFF.

Signal-specific limits carried into T06:

- RE has concrete subtype identity, but the owner availability/entry gates remain closed.
- EXT has a read-only retest-ready event mapping; it does not grant availability.
- MOM has a read-only per-closed-candle receipt, while its view remains recovery-only and execution-unavailable.
- MHV/MLV is a setup-formation receipt, not entry authority; Trigger use remains blocked and SIG-06/T04-E owner-epoch/recovery remains HOLD.
- CSA/CSAK predicate mapping is accepted, but fresh-event identity/consumption remains HOLD. Their Trigger paths must not become T06 candidates.

### Unresolved custom arbitration contract

The canonical M15 contract consumes M11/M12/M14 candidates with canonical signal types. It does not define how five Custom slots, custom formula witnesses, event-batch receipts, or custom attribution map into a single custom M15 decision.

The Custom MTF design document is marked **DRAFT FOR REVIEW**. Its details remain proposals, not a binding decision:

1. It proposes one final new-entry decision per symbol/event batch.
2. It proposes a `CustomN_Priority` followed by slot ID for selecting a primary slot, but the live input reference and current source expose no such priority input.
3. It proposes blocking both custom directions when they compete in a batch; the canonical M15 contract instead applies the D1 filter first and fails closed only if contradictory directions remain.
4. It proposes choosing among simultaneous fresh anchors by later confirmation time and then canonical TF/signal/owner-ID order.

The current `CustomEvaluator.mqh` does not implement that proposed anchor order: it selects OR components by event-ID string order and uses `CustomEarlierIdentity` (earlier confirmation first) for the fresh replacement. Because the design is still draft, this is a **contract mismatch requiring an adopted ruling**, not a claim that an approved rule was violated.

The M15→M16 custom payload is also not defined. M16 requires the exact selected components and frozen M11 D1 identity; the current transient T05 diagnostic snapshot has no selected-decision type or approved custom-witness revalidation interface. T04-B/E recovery and owner availability remain unverified, so a current D1/H4 owner identity cannot be assumed for every custom-only symbol.

## Classification

- **CONFIRMED:** Module 15 remains sole final custom decision authority; canonical processing/signatures remain unchanged.
- **HOLD / UNRESOLVED:** custom event-batch decision cadence, same-direction slot winner/attribution, conflicting-direction behavior, OR/fresh-anchor tie-break, and the exact M15→M16 custom decision payload.
- **DEPENDENCY HOLD:** all 77 owner-availability cells remain OFF; CSA/CSAK fresh-event semantics remain unresolved; MHV/MLV is not an entry Trigger; SIG-06/T04-E source epoch/recovery remains HOLD.
- **NO IMPLEMENTATION:** creating a winner/tie-break or adapting the canonical M15 candidate sorter to custom slots now would choose semantics absent from an accepted contract. No T06 consumer was added.

## Exact decisions required to unblock T06 implementation

1. Confirm whether custom M15 arbitration runs once per accepted closed-TF event batch, and whether at most one decision is allowed per symbol/batch.
2. Choose an approved deterministic policy for multiple same-direction matching slots and their primary attribution. If configurable priority is intended, add it explicitly to the input/identity contract.
3. Confirm custom opposite-direction handling and its order relative to the M11 D1 strategic gate.
4. Choose one canonical OR-witness/fresh-anchor ordering and align T05 before T06 consumes it.
5. Define the frozen custom decision fields M16 must revalidate, including exact source witness, symbol, batch/config revision, direction and M11 D1 owner identity; preserve unavailable behavior where the required owner is missing.

After these decisions are recorded, implement the smallest T06 consumer. Keep custom availability and auto-entry OFF, do not bypass M16/T07, and do not change canonical standalone H1 Extreme policy.

## Evidence reviewed

- `docs/references/SOURCE_INDEX.md` and `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
- `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md` on `d1-owner-dev`
- `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`, `M13_COMBINATION_COLLECTOR_CONTRACT.md`, and `M16_CONFLICT_INVALIDATION_CONTRACT.md` on `d1-owner-dev`
- `blueprint/decisions/CUSTOM_MTF_V1_ARCHITECTURE_DECISION.md`
- `docs/superpowers/specs/2026-11-07-custom-mtf-autoentry-design.md`
- `blueprint/contracts/CUSTOM_MTF_CLOSED_BAR_OBSERVATION_CONTRACT.md` and `CUSTOM_MTF_T05_DRAFT_INTERFACE.md`
- Current `CustomClock.mqh`, `CustomEvaluator.mqh`, and `CustomDispatch.mqh` at the starting checkpoint
- `blueprint/runtime/custom_mtf/task_queue.md`, `progress.md`, and `USER_INPUT_REFERENCE.md`
- Live PR #303 is open, Draft, unmerged; its head matched the starting branch checkpoint.

## Validation and next action

No compile, regression, static harness, or runtime command was run under the user's validation HOLD instruction. This documentation audit is not implementation verification.

Exact next action: record the five arbitration/interface decisions above in an approved T06 contract, then implement the read-only M15 consumer only after the required signal/owner inputs are accepted. Until then T06 is **AUDIT COMPLETE / IMPLEMENTATION HOLD**, not complete.


## User-directed arbitration decisions and implementation update — 2026-11-14

The user's next instruction adopts the five custom arbitration mappings in `blueprint/contracts/CUSTOM_MTF_T06_M15_AUTHORITY_CONTRACT.md`. These are engineering mappings for the Custom MTF path; they do not change BBMA source rules or canonical M15 behavior.

1. **Cadence:** at most one read-only receipt per resolved symbol and committed nonempty batch. Persistent reservation/consumption stays in T07.
2. **D1 and conflict:** require the same-pair confirmed current M11 D1 owner; filter direction before arbitration; unresolved/stale/transition owner blocks. Only contradictory directions surviving that filter fail closed. Hedging does not bypass the gate.
3. **Slot/attribution:** latest physical fresh trigger event wins; ties use D1→H4→H1→M30→M15→M5→M1, signal ascending, owner event ID ascending. Same-anchor slots all remain attributed; lowest numeric slot is primary bookkeeping, with no quality rank or configurable priority.
4. **OR/fresh-anchor order:** Context OR uses latest confirmation; Trigger OR and cross-candidate ordering use latest physical event (`entryEventTime`, else closed source bar), followed by the same deterministic tie order. Alternative anchors remain in the witness for T07.
5. **M15→M16 payload:** carry symbol, batch/time, exact config revision, direction, primary and matching slots, selected anchor, full witness, and frozen M11 D1 owner identity; M16 revalidation is required and execution authority is always false.

Implementation is present as a separate read-only consumer, connected after successful T05 dispatch. It does not invoke canonical M15, M16, T07, risk, OrderSend or trade lifecycle. D1 filtering happens before candidate validation/arbitration. The evaluator's OR comparator now follows the adopted deterministic ordering. Build identity is 6.21.

Code commits: comparator `342ab25a414b17647d720e637db1ac9ad934c76f`; consumer validation `bae2db09c5ea8321fc61a1bceb75a72107073265`; EA wiring/build identity `b76eec7609cf72bd029b7fc489170fdde38ae7c7`.

All 77 semantic availability cells and custom auto-entry remain OFF. MHV/MLV remains setup-only; CSA/CSAK fresh-event identity remains HOLD; SIG-06/T04-E owner-epoch/recovery remains HOLD. No compile, regression, static harness or runtime was run under the standing validation HOLD. This remains **DRAFT / HOLD / NOT VERIFIED**, with no merge or trading activation.

Exact next action: preserve this implementation checkpoint and wait for the validation gate to reopen; then run strict compile, targeted M15/T05 arbitration regressions and scheduler runtime evidence before deciding whether T06 can advance. Reassess upstream availability and T04-B/E plus M16/T07 dependencies at that point.
