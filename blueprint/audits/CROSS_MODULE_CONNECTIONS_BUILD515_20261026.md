# Cross-module connection reconciliation — Build 5.15

Date: 2026-10-26  
Issue: #292  
Owner baseline: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15  
Scope: static producer/consumer and control-flow reconciliation. No EA source is changed by this document.

## Reading the edge ledger

The ledger records producer/consumer handoffs and control/helper calls from the exact Build 5.15 source snapshot. The accepted root graph and the current-owner lexical overlay are separate authorities. PR #295 merged at main commit 22b2e539a82eea768c53bd2a905dd958b6072324; the root graph remains pinned to d1-owner-dev@23def0919386263007ead1898b94637cc17f7f36, while current_owner_source_overlay is pinned to d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de and source blob 09de8b80fdaeeb2fd614de0a1826134e9a8b2411.

The accepted root graph retains its existing 28-module schema. The separate current-source overlay records all 29 source headers, including M11J, and 431 function definitions, 1,478 call occurrences, 502 cross-module call occurrences, 96 distinct module edges and 364 distinct function pairs. The separate config/bbma_field_access_inventory_build515.json covers 36 structs / 640 declared fields / 595 accessed fields and 338 struct-field pairs observed in multiple modules; 0 unresolved typed-member occurrences were reported within the scanner scope. PR #295 deterministic-tooling check passed on head a9e10ae474707f9de79bb7eb14b29f6f5f951a81.

These are lexical and type-level measurements. Repeated struct.field access across modules does not prove the same runtime object is shared. By-reference/copy aliases and call-side mutation are not fully resolved, and no dependency absence is inferred. Therefore consumer_edges and interprocedural read/write ownership remain PARTIAL.

Machine-readable detail is split between config/bbma_module_graph.json.current_owner_source_overlay and config/bbma_field_access_inventory_build515.json; the latter records direct reads, direct writes and nested traversals per module. M11J and M12N are represented in the current-source overlay and are not inserted into the accepted root graph schema.

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

### CP12 — Core §6 MHV/MLV owner path

- M27 refreshes the closed M15 source snapshot, updates both M08 M15 Extreme directions, then calls M09 for BUY MHV with the SELL Extreme parent and SELL MHV with the BUY Extreme parent. The accepted owner is source-timeframe M15 only.
- M09 statically maps the accepted lifecycle: reversal-confirmed parent → normal TP-Wajib → inside-BB loss-of-prior-momentum phase → body-edge accumulation and freeze on the first later close-away candle → later body retest or same-cycle direction takeover. Outer-BB / prior-direction Momentum invalidation applies before takeover; an opposite RAW Extreme is only a candidate until reversal confirmation supersedes the cycle. No generic expiry is applied.
- M13 exports the mature M15 MHV state. REM keeps the exact H4 RE + H1 Extreme + M15 MHV signature; formation-established/frozen body is sufficient, with no separate retest requirement. M14 keeps exact component/timeframe validation. M16 checks the persistent M15 direction, frozen body and formation candle identity.
- M12N reads the M15 MLV owner as a read-only overlay. Build 5.15 has no H4/H1 MHV state owner or H4_MHV_WATCH implementation. C039/C040 HTF observer/context behavior is documented but not implemented; those decisions explicitly do not authorize MQL4 changes by themselves. It is a separate scoped contract/task, not a canonical Core §6 M09 mismatch.
- CP12 is static only: no M09 contract, code, test, native compile, Strategy Tester or runtime was added/run. The CP07 Build 5.22 probe checks stale MLV component admission, not M09 lifecycle parity.
### CP13 — Core §7 eCSD/CSD direction handoff

- Source/Core §7 defines eCSD as the early MA5/MA10 direction cross, CSD as the stronger MA5/MA10 plus Mid-BB cross, and both as direction signals rather than entry setups. M10's closed-body spanning formula and directional High/Low MA pairing remain explicit engineering mappings, not verbatim PDF formulas.
- M10 `DetectECSD`, `DetectCSD` and `DetectCSM` supply the signal predicates. M12 `DetectReEntryDirectionOwnerSignal` resolves same-candle precedence as CSM > CSD > eCSD; Type 3 uses CSM and Type 4 uses CSD as candidate precursors, with the later source-specific MA retrace required for confirmation. eCSD is direction ownership/context, not a Re-Entry.
- M13 `CollectSignalSnapshots` suppresses a same-direction eCSD when CSD has the same candle time. M27's H4 owner classifier uses CSM > CSD > eCSD. Its M15 inputs are selected from the exact latest-closed snapshot; M09 independently requires valid, closed data before consuming same-direction CSD/eCSD for MHV direction takeover. Raw CSD/eCSD is not assembled as a standalone M13/M15 entry candidate.
- M11J's approved D1O-01 D1 CSD family is an opportunity context only: the D1 source candle must be closed, direction must align with the ready D1 strategic owner, and a fresh confirmed LTF Re-Entry must follow activation. D1 eCSD logging uses the inclusive raw MA-pair predicate and remains watch-only, even if CSD also matches. The resulting candidate is `SIGNAL_RE_ENTRY`; M15 is still final authority and M16 is fail-closed.
- The old M10 contract instruction that M13 still needed to decide CSD/eCSD precedence was stale and is corrected in CP13. Owner Build 5.15 still carries the separately recorded M06 incomplete-history defect; its Build 5.20 repair is candidate-scoped, so the CP13 mapping does not certify incomplete-input signals. M08's local CSM-equivalent invalidation maps statically to M10 geometry but is not a direct M10 call; focused helper parity/runtime remains NOT VERIFIED. CP13 is static only; no tests, compile, Tester or broker runtime ran.
### CP14 — Core §8 Re-Entry owner and D1O-01 timing handoff

- Core §8, the PDF-derived index, Finale V05/V06 and M12 contract define the Re-Entry zone, close-side validity, Type2's MA5/MA10/Mid-BB confluence for at least three candles, Type3 CSM then later MA5/MA50 retrace, and Type4 CSD then later MA5/MA10 retrace. Type1 remains structural/range evidence without an invented count or expiry. IsNear < 2 points and the exact Type1 predicate are engineering mappings.
- Build 5.15 M12 keeps one direction/timeframe owner. When empty, TryStartSpecificReEntry() tries Type3→Type4→Type2 before Type1. reviewed sources do not assign overlap precedence and code does not prove mutual exclusion. CP16 records the approved project policy to keep the existing Type3→Type4→Type2→Type1 empty-owner order. The policy is not a source rule and does not claim an observed overlap; owner code remains unchanged.
- M11J D1O-01 consumes D1 EntryCandle as ActivationTime and requires fresh LTF Re-Entry readiness strictly after activation. This is limited to the approved D1 opportunity freshness gate; the ordinary M27→M15/M16→M22 path has no extra full-candle timer.
- M27 feeds closed D1/H4/H1/M15 owners; M13/M14 form/check exact signatures; M15 makes the final candidate decision; M16 revalidates identity; M17/risk/M22 remain downstream. Static trace only: no tests, compile, Tester or broker runtime were run in CP14.

### CP15 — direct primary PDF overlap check (2026-10-27)

- The supplied primary PDF pages 9–10 were read as text and rendered for visual inspection. Its SHA-256 `3e6065dd97c20951bd8af96bc81b81ca138800184be6fc4740a32aa4ab0a9c9c` matches the primary PDF hash recorded in SOURCE_INDEX.
- Page 10 lists the separate Type2, Type3 and Type4 formations and retraces but does not set overlap precedence, a tie-break, or mutual exclusivity. Page 9 defines Type1 range context; it does not add Type2/3/4 arbitration.
- This direct evidence confirms the M12 arbitration gap is not resolved by the primary PDF. Current Type3→Type4→Type2 ordering remains implementation behavior only; preserve it unchanged pending an explicit project policy. No code/test/compile/Tester/runtime changed or ran.

## Module connection ledger

| Module | Main output / control | Consumers or next handoff | Current gap/status |
|---|---|---|---|
| M01 Header & Inputs | Runtime inputs and modes | M26 validates; readers enumerated in the machine graph | 23 inputs mapped; two legacy NMJE flags are explicitly inactive and unread; no runtime input replay here |
| M02 Enums & Structs | Shared signal, state, candidate and decision types | Modules listed in the accepted graph and current-source overlay | 338 cross-module typed struct-field pairs are inventoried separately; interprocedural ownership remains partial |
| M03 Global Variables | PairState, owner states, monitored trades, observer state | Modules listed in the machine graph global inventory | 37 global identifiers mapped to referencing modules; read/write ownership remains partial |
| M04 Symbol & Market Data | Candle, quote, symbol and broker properties | Direct function callers enumerated in the machine graph | Call sites mapped; shared field-level read/write ownership remains partial |
| M05 Utility Functions | Pair lookup, time, hashes, logging, normalization | Direct function callers enumerated in the machine graph | Call sites mapped; shared helper/state ownership remains partial |
| M06 BBMA Data Engine | Closed-candle OHLC, MA and BB values | M07–M12, M17, M23–M24, M27 | **Owner bug confirmed:** incomplete history can yield biased indicators/valid snapshots; candidate repair is only in Draft PR #293 |
| M07 BB Shape Engine | BB shape / flat state | M27 builds H1/H4 shape snapshots; current source has no downstream BB-state reader | CP10 adds a source/ownership contract; output remains auxiliary/write-only and does not gate M10 CSM |
| M08 Extreme Detector | RAW signal plus persistent maturity, invalidation, supersession and retest lifecycle | M09 M15 parent; M12N observer; M13 combination snapshots; M15 standalone H1; M16 exact identity; M17 SL/TP source; M23 private replay; M27 orchestration | CP11 maps Core §5. RAW is not an entry; M08-local invalidation is not a direct M10 call. Standalone H1 requires RETEST_READY/Mode 2/H4 plus M11 D1 gate. Focused test/runtime remain NOT VERIFIED |
| M09 MHV/MLV Lifecycle | Reversal-confirmed M15 parent Extreme → normal TP-Wajib → post-TP loss/formation → frozen body, retest, invalidation and opposite-cycle supersession | M12N, M13/M14, M16, M27 | CP12 maps accepted Core §6 statically; no direct M15 lifecycle mismatch found. No standalone M09 contract is linked; HTF observer extensions C039/C040 are absent from this owner. Parity/runtime remain NOT VERIFIED |
| M10 CSM/CSD/eCSD | Closed-candle direction and Momentum predicates | M08 local invalidation parity; M12 Type1/3/4; M12N read-only; M13 same-candle precedence; M27 H4 owner/M15 snapshots; M11J D1 CSD context | CP13 maps Core §7; body-cross formula is an engineering interpretation. M12 priority is CSM > CSD > eCSD; M13 suppresses same-candle duplicate eCSD. Focused tests/runtime remain NOT VERIFIED |
| M11 Trend Functions | Atomic closed-D1 major-trend owner | M11J, M12, M12N, M15, M16, M27 | Static implementation present; D1 owner field handoff is inventoried; runtime remains unverified |
| M11J D1 Opportunity Journey | D1 CSD/Re-Entry/Momentum opportunity context; separate gated D1 Extreme-TPW journey | M12N overlay; M15 fresh-LTF-RE candidate construction/final authority; M16 revalidation; M23 TPW lifecycle; M27 update | D1O-01: D1 CSD is context aligned with D1 strategic owner and requires fresh LTF Re-Entry; EntryCandle sets ActivationTime; eCSD watch-only. CP18 Build 5.23 M15/M16 require a confirmed D1 owner for D1_OPP_EXTREME_TPW; transition/unresolved block, while counter-direction with a confirmed owner retains the existing H4/H1 prerequisites. D1 TPW gate remains OFF. Runtime unverified |
| M12 Re-Entry Engine | Persistent Type1/2/3/4 Re-Entry owners; M10 signal classification | M12N, M13, M15, M17, M23 replay, M27 | CP13 maps M10 precedence and Type3/4 later-retrace confirmation. CP14 maps Core §8; CP15 verified that sources set no Type2/3/4 overlap priority. CP16 records the approved project policy to preserve Type3→Type4→Type2→Type1 on an empty owner; this matches Build 5.15 and is not a source rule. Build 5.22 candidate freshness repair remains unmerged; owner unchanged; runtime open |
| M12N Nested MTF Journey | Read-only lineage and journey context; M15 MLV overlay | M11J D1 opportunity overlay; M13; M15/M22/M23 telemetry; M27 observer update | No create/reject/rank/execute authority. Build 5.15 has no H4/H1 MHV watch/context state; C039/C040 implementation requires a separate scoped contract/task |
| M13 Combination Engine | Collects REM/RRE/REE and per-cycle direction snapshots; REM includes mature M15 MLV | M14; M27 orchestration | CP12 maps REM maturity; CP13 verifies same-direction/same-candle CSD suppresses duplicate eCSD. Candidate regression/runtime coverage remains partial |
| M14 Sequence Engine | Validates exact REM/RRE/REE component/timeframe signatures | M15; M27 orchestration | CP12 maps REM's M15 MLV component to Core §6; full signature regression matrix absent |
| M15 Priority Engine | Sole final new-entry decision; Mode-2 standalone H1 Extreme candidate only from exact M08 RETEST_READY plus active same-direction H4 | M16, M17; M27 orchestration | Core §5 static gate mapped. M11 D1 authority and source-freshness checks also apply; combined/runtime proof partial |
| M16 Conflict & Invalidation | Revalidates frozen component and owner identity; MLV must match exact M15 direction, formation candle and frozen body | M17; M27 orchestration | CP12 maps Core §6 MLV identity; candidate freshness repair in PR #293 remains separate/unmerged from owner; runtime incomplete |
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
| M27 Main Controller | Closed D1/M15/H1/H4 M08/M10/M12 updates; M11J opportunity; M12N observer; M13/M14; M15/M16 and M17 handoff | Entry point / M22 preflight and lifecycle tick path | CP11–CP13 static order traced: M08 M15 precedes M09; M27 M15 direction snapshots feed M09/M13; D1 CSD opportunity remains LTF-Re-Entry-only. Orchestration runtime unverified |

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



### CP16 — M12 overlap policy decision (2026-10-27)

- The requester approved retaining the existing empty-owner order Type3→Type4→Type2→Type1 as deterministic project policy. The direct primary PDF finding remains unchanged: no source assigns this priority.
- Build 5.15 owner code already follows the selected order. This decision changes documentation/governance only; it does not establish predicate mutual exclusion or an observed market overlap.
- M12's project-policy gate is closed. Next eligible static audit: accepted Core §9 multi-timeframe relationship and strategic hierarchy through M11/M11J/M12/M12N/M13/M14/M15/M16/M27.
- No owner/EA code, tests, compile, Strategy Tester, broker runtime or trade changed/ran. Qualified G40 history remains NOT VERIFIED; PR #293 remains draft/unmerged and DO NOT MERGE.


## CP17 — accepted Core §9 MTF relationship / strategic hierarchy (2026-10-27)

Static baseline: accepted Core V2 blob 3c450d7157db6b7a6bf53549f645bb75c88371e5 at main; Build 5.15 owner blob 09de8b80fdaeeb2fd614de0a1826134e9a8b2411 at d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de.

- M27 builds closed D1/H4/H1/M15 snapshots, updates M11 D1 and the recovered H4 directional owner before M06–M12 owner processing, and calls M12N after both direction passes. M12N summarizes D1/H4/H1/M15 relations only; its contract bars creation/rejection/ranking and requires M15 to ignore nested relation for final eligibility.
- M11 uses closed D1 Close1 and current/previous closed MA50 values. Invalid/missing inputs become D1_OWNER_UNRESOLVED; valid but unconfirmed values become D1_TRANSITION. M15 admits ordinary candidates only under a confirmed same-direction D1 owner, freezes that identity, and M16 revalidates it.
- H4 recovery begins unresolved and requires verified checkpoint/replay provenance; runtime updates require completed recovery and a valid new closed H4 snapshot. Neutral H4 candles preserve the structural owner; ambiguous opposite events clear it. Standalone H1 Re-Entry requires active same-direction H4 plus confirmed same-direction D1.
- M13/M14 assemble/validate only the exact REM, RRE and REE signatures. M12N metadata does not add a component or replace a timeframe. M5 data is observed for a shadow layer only; no M1 executable path is present in the approved D1/H4/H1/M15 universe.
- **Open policy discrepancy:** Core §9.2 and M15 contract say D1_TRANSITION blocks all new entries. D1O-01 authorizes D1_OPP_EXTREME_TPW to oppose the strategic owner with H4 + fresh H1 gates, but does not explicitly authorize D1_TRANSITION. Build 5.15 M15's special D1O-TPW authority branch accepts any valid D1 state except UNRESOLVED, thus also accepts TRANSITION. The M17 D1 TPW feature flag is false; ResolveApprovedInitialSLTP rejects that identity before downstream risk/order execution. Keep this lifecycle gate OFF until the transition exception is explicitly resolved and required runtime gates pass.
- Result: the Core §9 hierarchy maps statically, but closure is PARTIAL at the D1 transition / D1O-TPW boundary. No code, Core source, tests, compile, Strategy Tester, broker runtime or trade changed/ran. C039/C040 H4/H1 MHV observer coverage remains a separate extension gap.

## CP18 — D1 TPW transition policy and candidate M15/M16 gate (2026-10-27)

- Project policy now resolves the CP17 ambiguity: D1_TRANSITION and D1_OWNER_UNRESOLVED block D1_OPP_EXTREME_TPW at both M15 candidate admission and M16 decision revalidation.
- The existing D1O-01 counter-direction extension remains available against a confirmed D1 owner when its existing aligned/recovered H4 and fresh confirmed H1 Re-Entry prerequisites hold. No D1 direction-equality rule was added for the TPW family.
- Candidate Build 5.23 uses the existing M11 confirmed-owner execution helper at both gates. M11 owner production, accepted Core, component signatures and M17 lifecycle behavior are unchanged; EnableD1TPWLifecycle remains OFF.
- Five focused portable regression scripts passed (four new exact-source unittest methods); exact Git-blob strict MetaEditor compile passed with 0 errors / 0 warnings. See build523 regression/native logs and manifest.
- Strategy Tester, qualified-history validation and broker/runtime were NOT RUN / NOT VERIFIED. The owner remains Build 5.15; PR #293 remains draft, open, unmerged and DO NOT MERGE.

## CP19 — accepted Core §10 exact MTF signatures and maturity (2026-10-27)

- The accepted signatures map through M13 collection and M14 exact component/timeframe/direction validation: REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV; RRE = D1/H4 Re-Entry + H1 Extreme; REE = D1 Re-Entry + H4/H1 Extreme.
- Component maturity is owned separately: M08 Extreme must be reversal-confirmed for REM/REE but does not need standalone RETEST_READY; M09 M15 MHV/MLV must reach formation-established plus frozen marked body for REM, with no retest prerequisite and no void/superseded cycle reuse.
- M11 remains the D1 strategic-owner producer. M15/M16 gate executable direction independently from signature validity; D1 Re-Entry is a component identity, not a substitute for M11 owner confirmation. M12N remains observational. M27 preserves the closed-snapshot → owner/candidate → M15 → M16 → downstream sequence.
- CP11/CP12/CP14/CP17 already provide the owner-source maturity/signature traces; CP18 resolves the separate D1O-TPW transition gate. CP19 reconciles Core §10 against those verified records without repeating their tests or compile and finds no new mismatch.
- Static mapping only. Qualified G40 history remains NOT VERIFIED; Strategy Tester and broker/runtime remain NOT RUN. C039/C040 stays a separate scoped extension gap.

## CP20 — Core §11 scope and non-Core boundary (2026-10-27)

- Accepted Core §11 excludes personal H4-only workflow, sample win-rate claims, personal risk/leverage/lot/portfolio, personal MA10-plus-allowance stop methodology, psychology, literal guarantees, and EA mechanisms such as lock/scheduler/dashboard/logging/broker/execution plumbing.
- Current Core authority says the Home Course denominator is 49/49 classified with zero unresolved Core semantic holds. This is semantic classification coverage, not a claim that 49 families are executable or runtime verified.
- Cross-module interpretation: M17 SL/TP, M18 label-only score, M19 risk, M20 portfolio, M21 sizing, M22 order side effects, M23 lifecycle, M24 recovery, M25 display, M26 initialization and M27 orchestration remain project implementation layers. Their authority is governed by project contracts and accepted mappings; they do not add universal BBMA signal rules.
- C039/C040/C041 remain bounded context; C044 remains separately gated. D1O-01 remains a labelled project extension. No new code or Core promotion was made in CP20.
- No new source-to-Core gap found. CP20 reuses the Q5 rebaseline and dated closure decisions; no tests, compile, Strategy Tester or broker runtime ran. Full rule-to-runtime and nested-field ownership remain PARTIAL.

## CP21 — Nested typed-field inventory (2026-10-27)

- The authoritative Build 5.15 source is d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de, blob 09de8b80fdaeeb2fd614de0a1826134e9a8b2411.
- Main graph correction is merged at 22b2e539a82eea768c53bd2a905dd958b6072324: accepted graph authority remains unchanged; the current-source overlay and typed field inventory are separate artifacts.
- CP21 adds a complete typed-member inventory for the scanner scope. It does not complete object-identity, by-reference/copy alias or call-side mutation ownership; consumer_edges remains PARTIAL_INTERPROCEDURAL.
- No EA/Core semantics, owner source, tests, compile, Strategy Tester or broker runtime changed/ran in CP21. Qualified G40 history remains NOT VERIFIED; Strategy Tester and runtime remain NOT RUN.

## CP22 — Cross-module reference identity and mutation map (2026-10-27)

- PR #296 merged at main@7fb1cfdbb0fb2d7e30fe75e382e176199199416f. The exact PR head fe021e2b424b1e2866fe328be618f0de86a28e3a passed deterministic-tooling.
- Machine inventory: config/bbma_reference_identity_inventory_build515.json, blob a4a159631e6021598a000d454abca9b5f9979ab1. Accepted root graph authority remains 23def0919386263007ead1898b94637cc17f7f36; current source overlay remains owner Build 5.15 commit 459c0588e625d7f7630f0fb5612b7f04fda496de / source blob 09de8b80fdaeeb2fd614de0a1826134e9a8b2411.
- Parser counts again match the accepted source overlay: 431 functions, 1,478 calls, 502 cross-module call occurrences, 96 module edges and 364 function pairs. The inventory resolves 317 cross-module struct-by-reference call arguments into 90 global subobjects, 69 forwarded references (51 whole-param / 18 nested-member), 151 local objects and 7 local copies.
- Interprocedural propagation records 344 origin associations across those 317 callsites, with zero unresolved, unbound or cyclic rows. Nineteen callsites have multiple origins because the same helper is reached with different local/global or timeframe/direction objects; identity is therefore PARTIAL_CONTEXT_INSENSITIVE, not one object per function.
- Static parameter-write tracing finds 122 callsite parameters with direct/transitive write paths and 195 with no detected parameter write path. All 317 target parameters are mutable references; “no detected write” is not a const/read-only guarantee and does not cover opaque builtin or direct global side effects.
- Canonical owner path: M27 passes g_pair_states[pairIndex] and nested timeframe/lifecycle/re-entry subobjects to M06/M08/M09/M11/M12. M11 writes the D1 owner; M08/M09/M12 update their respective persistent state paths. M27 passes the same PairState root to M13/M12N/M15; no PairState parameter write paths were detected through those observer/final-gate calls. M16 D1 snapshot helpers pass a local PairState copy loaded from the global array.
- C044 helper paths are separate from PairState: replay fields can resolve either to a local counterfactual TradeInfo copy or to g_monitored_trades[i] during trade lifecycle handling. The field path stays within c044_replay_* state.
- No EA/Core source, tests, compile, Strategy Tester, broker runtime, terminal restart or trading activation changed/ran in CP22. G40 device is online, but process/terminal state was not inspected. The last Q10 R5 runtime artifact dated 2026-09-24 lists R5-14 and R5-16 as natural broker-event blockers; current runtime is not reconfirmed here.
- Next implementation hardening: qualify proven read-only reference parameters as const and compile the exact candidate on G40 before accepting that guard. Keep Q10 R5/R6 gates unchanged; do not manufacture broker conditions.
