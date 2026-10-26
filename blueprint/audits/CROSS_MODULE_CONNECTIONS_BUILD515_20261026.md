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

## Module connection ledger

| Module | Main output / control | Consumers or next handoff | Current gap/status |
|---|---|---|---|
| M01 Header & Inputs | Runtime inputs and modes | M26 validates; readers enumerated in the machine graph | 23 inputs mapped; two legacy NMJE flags are explicitly inactive and unread; no runtime input replay here |
| M02 Enums & Structs | Shared signal, state, candidate and decision types | Modules listed in the machine graph type inventory | 68 M01/M02 declarations mapped to references; nested-field ownership remains partial |
| M03 Global Variables | PairState, owner states, monitored trades, observer state | Modules listed in the machine graph global inventory | 37 global identifiers mapped to referencing modules; read/write ownership remains partial |
| M04 Symbol & Market Data | Candle, quote, symbol and broker properties | Direct function callers enumerated in the machine graph | Call sites mapped; shared field-level read/write ownership remains partial |
| M05 Utility Functions | Pair lookup, time, hashes, logging, normalization | Direct function callers enumerated in the machine graph | Call sites mapped; shared helper/state ownership remains partial |
| M06 BBMA Data Engine | Closed-candle OHLC, MA and BB values | M07–M12, M17, M23–M24, M27 | **Owner bug confirmed:** incomplete history can yield biased indicators/valid snapshots; candidate repair is only in Draft PR #293 |
| M07 BB Shape Engine | BB shape / flat state | M27 builds shape state | Direct consumer edge was missing from the old graph; standalone M07 contract still absent |
| M08 Extreme Detector | Extreme maturity, validity and lifecycle snapshots | M09, M12N, M13, M16, M23 replay, M27 | Old gap-register claims are stale; runtime lifecycle trace still open |
| M09 MHV/MLV Lifecycle | Parent Extreme, TP-Wajib, loss, body mark, retest, invalidation | M12N, M13, M16, M27 | No standalone M09 contract; old graph incorrectly cited the D1 TPW contract |
| M10 CSM/CSD/eCSD | Direction and momentum evidence | M12, M12N, M13, M23 replay, M27 | All-case runtime trace not verified |
| M11 Trend Functions | Atomic closed-D1 major-trend owner | M11J, M12, M12N, M15, M16, M27 | Static implementation present; D1 owner field handoff is inventoried; runtime remains unverified |
| M11J D1 Opportunity Journey | D1 opportunity family/cycle state from the approved D1O-01 extension | M12N overlay, M15 candidate construction, M16 revalidation, M23 TPW completion check, M27 update | Source module was omitted from older maps; now included. D1O-01 is mapped; no standalone module contract is linked here. Test/runtime status remains partial/unverified |
| M12 Re-Entry Engine | Persistent Re-Entry owner states and confirmed signal | M12N, M13, M15, M17, M23 replay, M27 | Invalid refresh preserves prior state; admission impact still requires reproduction |
| M12N Nested MTF Journey | Read-only lineage and journey context | M11J D1 opportunity overlay; M13; M15/M22/M23 telemetry; M27 observer update | No create/reject/rank/execute authority |
| M13 Combination Engine | Collected component sets and candidates | M14; M27 orchestration | Candidate/test assignment coverage partial |
| M14 Sequence Engine | Validated REM/RRE/REE candidates | M15; M27 orchestration | Full signature regression matrix absent |
| M15 Priority Engine | Sole final new-entry decision | M16, M17; M27 orchestration | D1 gate exists statically; combined/runtime proof partial |
| M16 Conflict & Invalidation | Revalidated or rejected selected decision | M17; M27 orchestration | M12 stale-refresh path still unproven |
| M17 SL/TP Validation | Approved execution geometry and source component | M21, M19, M22 preflight | SELL spread normalization and full broker runtime remain open |
| M18 Signal Scoring | Label-only score | No caller found in pinned source | Confirm whether any display/telemetry consumer is intended |
| M19 Risk Engine | Risk approval/rejection | M22; M24 recovery helpers | No signal authority |
| M20 Portfolio Protection | Portfolio gate and protection request | M22, M23, M27 tick path | Broker-connected protection path not revalidated |
| M21 Money Management | Frozen lot-size result | M19, M22 | Broker lot/tick-value runtime matrix remains separate |
| M22 Order Execution | Approved order side effects and execution identity | M23, M24, M27 preflight call | No runtime/order/SL/TP acceptance in this audit |
| M23 Position Management | Tick-driven position lifecycle and close actions | M24 recovery; M27 tick path | C044 replay uses private owner snapshots |
| M24 Recovery Engine | Reconstructed execution, risk and lifecycle state | M19–M23, M26 initialization, M27 owner/H4 helpers | Restart/provenance runtime remains unverified |
| M25 Dashboard | Read-only display snapshot | M27 refresh | Preserve display-only boundary |
| M26 Initialization & Cleanup | Input validation, initialization and recovery dispatch | M24 recovery; platform lifecycle | No new startup/restart runtime evidence |
| M27 Main Controller | Snapshot clock, owner updates, candidate handoffs and lifecycle orchestration | Entry point; no downstream consumer | Direct function edges are now inventoried; orchestration runtime remains unverified |

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
