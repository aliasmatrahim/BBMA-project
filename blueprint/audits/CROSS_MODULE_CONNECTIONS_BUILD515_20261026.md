# Cross-module connection reconciliation — Build 5.15

Date: 2026-10-26  
Issue: #292  
Owner baseline: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15  
Scope: static producer/consumer and control-flow reconciliation. No EA source is changed by this document.

## Reading the edge ledger

The ledger records producer/consumer handoffs and control/helper calls from the pinned source. The machine-readable graph now includes a lexical inventory of 431 detected function definitions, 96 cross-module call edges / 364 call pairs, 23 M01 input fields, 68 M01/M02 type declarations, and 37 M03 globals. It also adds the previously omitted M11J source module. These references do not fully classify nested field ownership or read/write direction; `consumer_edges` remains **PARTIAL**.

Machine-readable detail: `config/bbma_module_graph.json` under `connection_inventory` lists the exact caller/callee pairs, input readers, type users, global identifier references and D1 owner-field handoffs. Two legacy NMJE inputs have no readers and are explicitly marked inactive in the source.

D1O-01 is the approved project execution extension for M11J. The owner source writes PairState.d1_opportunity in M11J; M12N reads it as an observer overlay, while M15 builds the candidate and M16 revalidates its identity. The strategic D1 owner field remains a separate M11 producer/consumer path. No new rule or runtime claim is added.

## Main decision and execution path

1. M27 builds closed D1/H4/H1/M15 snapshots (plus M5 observer context); M06 supplies MA/BB values.
2. M27 updates the M11 D1 owner and M08/M09/M10/M12 owners for both directions, then runs M12N as read-only observer.
3. M13 collects owner snapshots and constructs REM/RRE/REE and other eligible candidates; M14 validates combinations.
4. M15 filters/selects the final new-entry decision; M16 revalidates the frozen decision and owner identities.
5. M17 resolves and validates SL/TP; M21 sizes; M19 applies risk; M20 applies portfolio protection; M22 performs execution.
6. M23 manages live positions on ticks; M24 restores persistent state during M26 initialization. M25 is dashboard-only. M18 has no caller found in the pinned execution path.

M27 runs portfolio and position management before the new closed-M15 scan on each tick. M23's C044 replay calls the canonical M08/M10/M12 state machines on private replay state; it does not own the canonical entry-state objects.

### CP11 — Extreme-specific owner path

- M06 supplies the frozen closed-candle OHLC/MA/BB snapshots. M27 invokes M08 on D1, M15, H1 and H4, resolves opposite mature-owner supersession, then exports reversal-confirmed H1/H4 state. The M15 lifecycle is the distinct M09 parent.
- M09 attaches only a reversal-confirmed M15 Extreme, then manages normal TP-Wajib and MHV/MLV progression. M12N observes the owner state after both directions update; it cannot create, reject or rank signals.
- M13/M14 consume immutable H1/H4 snapshots under the existing REM/RRE/REE signatures. Standalone H1 reaches M15 separately only at RETEST_READY with Mode 2 and active same-direction H4; M11 D1 and M16 exact-owner revalidation still apply.
- M17 resolves the Q5 H1 structural-wick stop and opposite-MA TP-Wajib mapping. The separate D1O path is an execution extension: `EnableD1TPWLifecycle=false`, M17 rejects that identity while disabled, and M23's D1 TPW close path is gated. No live D1 TPW lifecycle is claimed.
- CP11 is static-only. Focused maturity/TPW tests and runtime remain NOT VERIFIED; Strategy Tester remains NOT RUN.

## Module connection ledger

| Module | Main output / control | Consumers or next handoff | Current gap/status |
|---|---|---|---|
| M01 Header & Inputs | Runtime inputs and modes | M26 validates; readers enumerated in the machine graph | 23 inputs mapped; two legacy NMJE flags are explicitly inactive and unread; no runtime input replay here |
| M02 Enums & Structs | Shared signal, state, candidate and decision types | Modules listed in the machine graph type inventory | 68 M01/M02 declarations mapped to references; nested-field ownership remains partial |
| M03 Global Variables | PairState, owner states, monitored trades, observer state | Modules listed in the machine graph global inventory | 37 global identifiers mapped to referencing modules; read/write ownership remains partial |
| M04 Symbol & Market Data | Candle, quote, symbol and broker properties | Direct function callers enumerated in the machine graph | Call sites mapped; shared field-level read/write ownership remains partial |
| M05 Utility Functions | Pair lookup, time, hashes, logging, normalization | Direct function callers enumerated in the machine graph | Call sites mapped; shared helper/state ownership remains partial |
| M06 BBMA Data Engine | Closed-candle OHLC, MA and BB values | M07–M12, M17, M23–M24, M27 | **Owner bug confirmed:** incomplete history can yield biased indicators/valid snapshots; candidate repair is only in Draft PR #293 |
| M07 BB Shape Engine | BB shape / flat state | M27 builds H1/H4 shape snapshots; current source has no downstream BB-state reader | CP10 adds a source/ownership contract; output remains auxiliary/write-only and does not gate M10 CSM |
| M08 Extreme Detector | RAW signal plus persistent maturity, invalidation, supersession and retest lifecycle | M09 M15 parent; M12N observer; M13 combination snapshots; M15 standalone H1; M16 exact identity; M17 SL/TP source; M23 private replay; M27 orchestration | CP11 maps Core §5. RAW is not an entry; M08-local invalidation is not a direct M10 call. Standalone H1 requires RETEST_READY/Mode 2/H4 plus M11 D1 gate. Focused test/runtime remain NOT VERIFIED |
| M09 MHV/MLV Lifecycle | Reversal-confirmed M15 parent Extreme, normal TP-Wajib, loss/formation, body mark, retest and invalidation | M12N, M13, M16, M27 | CP11 verifies the M08 parent edge; Core §6/M09 full owner-gap reconciliation remains next. No standalone M09 contract is linked |
| M10 CSM/CSD/eCSD | Direction and momentum evidence | M12, M12N, M13, M23 replay, M27 | Core §4 signal geometry is statically mapped; M12 Type-3 consumption is present; all-case test/runtime trace remains NOT VERIFIED |
| M11 Trend Functions | Atomic closed-D1 major-trend owner | M11J, M12, M12N, M15, M16, M27 | Static implementation present; D1 owner field handoff is inventoried; runtime remains unverified |
| M11J D1 Opportunity Journey | D1 opportunity family/cycle state; D1 Extreme requires reversal-confirmed maturity and active normal TP-Wajib | M12N overlay, M15 candidate construction, M16 revalidation, M23 TPW lifecycle, M27 update | D1O is a project extension. Dedicated D1 TPW lifecycle gate is OFF; M17 rejects D1TPW identity while OFF. Runtime remains unverified |
| M12 Re-Entry Engine | Persistent Re-Entry owner states and confirmed signal | M12N, M13, M15, M17, M23 replay, M27 | Invalid refresh preserves prior state; admission impact still requires reproduction |
| M12N Nested MTF Journey | Read-only lineage and journey context | M11J D1 opportunity overlay; M13; M15/M22/M23 telemetry; M27 observer update | No create/reject/rank/execute authority |
| M13 Combination Engine | Collected component sets and candidates | M14; M27 orchestration | Candidate/test assignment coverage partial |
| M14 Sequence Engine | Validated REM/RRE/REE candidates | M15; M27 orchestration | Full signature regression matrix absent |
| M15 Priority Engine | Sole final new-entry decision; Mode-2 standalone H1 Extreme candidate only from exact M08 RETEST_READY plus active same-direction H4 | M16, M17; M27 orchestration | Core §5 static gate mapped. M11 D1 authority and source-freshness checks also apply; combined/runtime proof partial |
| M16 Conflict & Invalidation | Revalidates frozen component and owner identity; standalone Extreme must match exact M08 H1 RETEST_READY completion candle | M17; M27 orchestration | Core §5 identity path mapped. Candidate freshness repair in PR #293 remains separate from owner; runtime incomplete |
| M17 SL/TP Validation | Standalone H1 Extreme: Q5 structural-wick SL window and opposite-MA TPW area-edge mapping; D1 TPW identity is fail-closed while gate OFF | M21, M19, M22 preflight; M23 TPW lifecycle when enabled | Static mapping confirmed. SELL spread normalization and full broker runtime remain open; D1 lifecycle is not activated |
| M18 Signal Scoring | Label-only score | No caller found in pinned source | Confirm whether any display/telemetry consumer is intended |
| M19 Risk Engine | Risk approval/rejection | M22; M24 recovery helpers | No signal authority |
| M20 Portfolio Protection | Portfolio gate and protection request | M22, M23, M27 tick path | Broker-connected protection path not revalidated |
| M21 Money Management | Frozen lot-size result | M19, M22 | Broker lot/tick-value runtime matrix remains separate |
| M22 Order Execution | Approved order side effects and execution identity | M23, M24, M27 preflight call | No runtime/order/SL/TP acceptance in this audit |
| M23 Position Management | Tick-driven close/position lifecycle; private M08 replay for C044 and separate gated D1 TPW close | M24 recovery; M27 tick path | CP11 confirms D1 TPW lifecycle gate is OFF; C044 uses private owner snapshots; no runtime rerun |
| M24 Recovery Engine | Reconstructed execution, risk and lifecycle state | M19–M23, M26 initialization, M27 owner/H4 helpers | Restart/provenance runtime remains unverified |
| M25 Dashboard | Read-only display snapshot | M27 refresh | Preserve display-only boundary |
| M26 Initialization & Cleanup | Input validation, initialization and recovery dispatch | M24 recovery; platform lifecycle | No new startup/restart runtime evidence |
| M27 Main Controller | Closed D1/M15/H1/H4 M08 lifecycle updates, M15 parent M09 update, M12N observer, M13/M14 assembly, M15 candidates, M16 decision and M17 handoff | Entry point / M22 preflight and lifecycle tick path | CP11 order statically traced; orchestration runtime remains unverified |

## Evidence and unresolved gates

- The source signatures retained are REM = H4 RE + H1 Extreme + M15 MHV/MLV; RRE = D1/H4 RE + H1 Extreme; REE = D1 RE + H4/H1 Extreme.
- M06 repair exists in Draft PR #293 / Build 5.20; owner baseline remains Build 5.15.
- Finding B is **VERIFICATION REQUIRED**: reproduce an actual unreadable H1/H4 refresh through candidate construction, M15, M16 and downstream gates. Do not add generic age expiry.
- The full accepted-Core rule denominator, global regression assignment, qualified data gate, and M01–M27/M11J/M12N runtime trace remain **PARTIAL / NOT VERIFIED**.
- This document records a static owner snapshot; it adds no BBMA rule and makes no profitability or production-readiness claim.

## Candidate-branch delta — Build 5.21 / CP06 (2026-10-26)

The owner inventory above remains pinned to Build 5.15. Draft PR #293 adds this separately verified candidate handoff:

| Producer / source | Consumer / gate | Required link | Result |
|---|---|---|---|
| M27 `BuildTimeframeSnapshot` + M06 `GetDataForTimeframe` | M15 `IsCurrentClosedSourceSnapshot` | Valid, closed data timeframe and candle time must equal the latest closed processing-snapshot candle | Invalid H1/H4 refresh is rejected for new entry |
| M12 Re-Entry owner + M24 H4 directional owner | M15 `IsCandidateSourceSnapshotReady` / `PriorityEngine_Atomic` | Exact current source snapshot; H1 standalone candidates retain the active, same-direction H4 dependency | Candidate excluded before M15 direction counts/selection |
| M15-created decision + persistent M12 owner | M16 `IsDecisionSourceSnapshotReady` / `ValidateDecisionOwnerSnapshot` | Repeat current snapshot and required H4-owner check before `DEC_VALIDATED` | Forced stale decision fails closed |
| M16 validated decision | M27 preflight dispatch -> M17 -> M19 -> M20 -> M22 | Existing order remains; no new execution authority | Dispatch chain checked statically; no preflight/order runtime executed |

A failed read does not reset M12/H4 state or create age expiry. The exact-source portable probe confirms invalid-H1/H4 rejection and a valid-data control. Build 5.21 native compilation, qualified Strategy Tester and broker runtime remain NOT TESTED; owner Build 5.15 is unchanged.

This candidate delta does not complete the full consumer-field graph or the M01–M27/M11J/M12N audit.


## Candidate-branch delta — Build 5.22 / CP07 (2026-10-27)

The Build 5.15 owner inventory above remains pinned and unchanged. Draft PR #293 adds a source-readiness gate for every component in the frozen candidate/decision:

| Producer / source | Consumer / gate | Required link | Result |
|---|---|---|---|
| M08 Extreme / M09 MHV-MLV / M12 Re-Entry owner snapshots | M15 `IsCandidateSourceSnapshotReady` | Every component timeframe must have valid, closed data equal to the latest closed processing snapshot | Stale H1 Extreme, H4 Extreme or M15 MLV is excluded before M15 selection |
| M15 frozen component identities | M16 `IsDecisionSourceSnapshotReady` + `ValidateDecisionOwnerSnapshot` | Repeat source readiness for every component, then preserve existing owner identity validation | Forced stale decision cannot reach `DEC_VALIDATED` |
| M16 validated decision | M27 preflight -> M17 -> risk/portfolio -> M22 | Existing call order and authority remain unchanged | Portable gate probe stops before broker APIs; runtime not exercised |

Owners remain persistent through unreadable refreshes. Build 5.22 adds no expiry or signal/ranking semantics. Native strict compile and Strategy Tester are NOT TESTED; full audit remains PARTIAL.


## Candidate-branch delta — CP10 Core §4 BB-state / Momentum trace (2026-10-27)

The Build 5.15 owner remains unchanged. This static trace adds no signal, priority or execution rule:

- M06 supplies closed BB values. M27 invokes M07 `BuildBBShapeState` for H1/H4; `DetectBBState` writes the enum snapshot, but the pinned source contains no downstream BB-state reader. M07 is auxiliary, not an M10 gate.
- M10 `DetectCSM` independently requires a closed outside-band candle, increased BB width and same-direction Mid/relevant outer-band movement. M12 consumes it as a Type-3 precursor and direction-owner signal; M27 owns the closed-candle call order.
- M08's persistent Extreme lifecycle checks `IsExtremeLifecycleInvalidation` before maturity promotion. That calls the M08-local `IsExtremeMomentumInvalidation`, whose valid-data geometry mirrors the M10 CSM predicate; it is a local calculation, not a direct M10 call.
- The stale M08/M10 contract statements are reconciled. Static trace is VERIFIED; focused M08/M10 helper parity and attributable runtime remain NOT VERIFIED. M07's 0.9/1.1 classifications and one-point tolerance are engineering labels, not BBMA rules.

