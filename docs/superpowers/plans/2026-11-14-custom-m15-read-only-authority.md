# Custom MTF M15 Read-Only Authority Implementation Plan

> **For agentic workers:** Inline implementation in the existing feature branch; preserve the user's validation HOLD. Do not merge or activate trading.

**Goal:** Consume one committed T05 snapshot with a fail-closed, read-only Custom M15 selection receipt.

**Architecture:** Keep canonical M15 unchanged. A separate pure MQL4 consumer validates the exact batch, config revision, selected witness, fresh anchor, and same-pair M11 D1 snapshot, then records one immutable receipt with execution disabled.

**Tech Stack:** MQL4 `#property strict`; existing custom_mtf headers and GitHub branch `feat/custom-mtf-v1-20261108`.

**Spec:** `docs/superpowers/specs/2026-11-14-custom-m15-read-only-authority-design.md`

## Global Constraints

- Use latest closed bars and existing owner snapshots only.
- Preserve canonical M15 signatures/cadence and canonical standalone H1 Extreme policy.
- Never invent or promote signal-owner availability; all 77 cells remain OFF.
- MHV/MLV is setup-only here; CSA/CSAK freshness remains HOLD.
- Do not call M16, T07, M17, M21, OrderSend or trade lifecycle from this consumer.
- No compile, regression, static harness or runtime command during this user-directed validation HOLD.

## Review Focus

- Stale or wrong-symbol D1 owner snapshot must block the receipt.
- Old batch ticket/config revision/witness must never be selected.
- An anchor must be a fresh Trigger component of the selected witness and the same continuous batch.
- Equal-timeframe/equal-event arbitration must be independent of source frame order.
- Multiple matching slots must preserve attribution while choosing a stable primary only for a shared physical anchor.

---

### Task 1: Bind deterministic witness ordering

**Files:**
- Modify: `blueprint/source/custom_mtf/CustomEvaluator.mqh`
- Modify: `blueprint/contracts/CUSTOM_MTF_T05_DRAFT_INTERFACE.md`

**Interfaces:**
- Consumes: `CustomOwnerView`, current `CustomWitness`, explicit `freshOwnerIds`.
- Produces: deterministic OR witness; latest confirmation for Context; latest physical event for Trigger; tie order D1→H4→H1→M30→M15→M5→M1, signal ascending, event ID ascending.

- [ ] Record a pre-code snapshot of the current ascending/earliest comparator in the progress ledger.
- [ ] Replace it with the contract comparator; do not change formulas or availability.
- [ ] Validation remains deferred; make no compiler/test claim.

### Task 2: Implement and wire the read-only M15 consumer

**Files:**
- Create: `blueprint/source/custom_mtf/CustomM15Authority.mqh`
- Modify: `blueprint/source/BBMA_EA.mq4`
- Modify: `blueprint/contracts/CUSTOM_MTF_T05_DRAFT_INTERFACE.md`
- Modify: `blueprint/runtime/custom_mtf/task_queue.md`
- Modify: `blueprint/runtime/custom_mtf/progress.md`

**Interfaces:**
- Consumes: `CustomEvaluationSnapshot`, committed `CustomEventBatch` / `CustomClockState`, exact admitted config revision, latest closed D1 identity, and the same pair's `D1MajorTrendOwner`.
- Produces: one transient `CustomM15AuthorityReceipt`, carrying the primary slot, same-anchor matching slots, selected witness/fresh anchors and frozen D1 owner. `executionAuthority` is always false.

- [ ] Validate config and batch bindings before scanning successful results.
- [ ] Apply the confirmed M11 D1 filter; block stale/unresolved/transition D1; fail closed if opposite directions remain.
- [ ] Select the latest fresh anchor; use the contract's stable ties; collapse only same-direction same-anchor slots to the lowest slot ID and retain attribution.
- [ ] Call only after committed T05 dispatch; clear the previous receipt at the start of each observation.
- [ ] Set unique Build 6.21 and source revision tags in the EA header/property/build log.
- [ ] Do not run compile/regression/static/runtime; record all as NOT RUN / NOT VERIFIED.
- [ ] Read back the source, contract, interface, queue and progress from the final immutable SHA.

### Task 3: Checkpoint Draft PR

**Files:**
- Modify: PR #303 body and progress record.

- [ ] Record task ID, branch, final source/checkpoint SHA, evidence, validation HOLD, remaining dependencies and exact next action.
- [ ] Confirm PR remains Draft/open/unmerged; do not merge or activate.

