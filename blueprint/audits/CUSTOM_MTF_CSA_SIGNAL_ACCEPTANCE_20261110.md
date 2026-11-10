# SIG-02 CSA acceptance — 2026-11-10

Status: VERIFIED for bounded read-only M10 MidBB source, observer materialization and native/controller evidence below. Execution/trigger admission and integrated T04 remain pending.

Base fb4779b92ddff09f3b913c00701305b37ac8e363; branch feat/custom-mtf-v1-20261108; Draft PR #303.
Build 6.08 / V608_CSA_MIDBB_SOURCE_20261110 / CSA_MIDBB_SOURCE_001_20261110.
Source LF SHA256 f317317f2ba7145990b66340aea6022a385e464e72da4e01be2d71f1c12e7e9c. Publication commit is recorded in PR #303.

## Accepted behavior

M10_DIRECTION_CLOSE_ONLY_USER_DECISION_20261110.md governs: valid closed Close > MidBB for BUY, Close < MidBB for SELL. Equality is a readable false signal. Open/MA pair/previous cross/colour/BB expansion are not CSA criteria. This is the accepted user mapping, not a newly authenticated founder quotation. Legacy eCSD stays MA-only and is never renamed CSA.

One M10 classifier and snapshot own the rule. Shared closed-input/fingerprint machinery reuses MOM's current finalized band when its current 20 inputs match; CSA requires only its own 20-bar current band, not MOM's 21-bar previous-band dependency. Current/historical cache slots are separate and symbol-specific; history revisions invalidate numeric reuse. Unready, nonfinite/nonpositive, unordered or changing input is unavailable. Shift0/negative rejects. No extra lifecycle, TTL, detector, candidate or execution owner is introduced.

Requested observer snapshots project direction and symbol/TF/source-candle identity. Repeated reads keep identity. False direction has no confirmation/event ID. First observation primes without emitting historical trigger; failed readiness aborts without consuming the batch. Every CSA view remains recoveryOnly=true, entryWindowOpen=false, entryEligible=false and executionAvailable=false. These IDs describe observations; physical trade dedup/trigger reservation remains T05–T07 work.

## Verified evidence

| Check | Evidence |
|---|---|
| Native full EA and final CSA harness | 0 errors / 0 warnings |
| CSA native | 154/154 PASS across M1/M5/M15/M30/H1/H4/D1 |
| Actual history | 140 directional comparisons (10 closed bars × two directions × seven TF); M30 declared derived OHLC fixture |
| Native regression | eCSD190, MOM55, MHV-TF238, M09producer52/replay57, canonical47, observer4, observer-M09 4, producer22, recovery27, higher23, flow12, prefreeze61 PASS |
| Actual controller | OnTick/OnTimer → M27 → ProcessPair, GBPUSD Aug4 2026 02:00–06:00 chart time, M1 delivery/model2, canonical M15 clock |
| CSA materialization in controller | 210 views across15 frames validated against closed iClose/iMA; context-only flags checked |
| Full scalar parity | OFF/ON/frozen6.07 traces each12,224 rows over16 M15 cycles; identical, old/new differences0 |
| Orders | Valid decisions0, captured attempts0, no orders in all three profiles |
| Cloud targeted | 5 test functions plus module import assertions, actual extracted host-C++ classifiers/transaction fixtures and all custom Python py_compile PASS |
| Architecture | 10 protected functions byte-identical to6.07, including DetectCSD/ECSD/CSM, MOM classifier/snapshot, D1 owner, canonical M09 transaction, ProcessPair, OnTickMain and position management |
| Final integrity | G40 verifier11780 exit0;14 manifests, source/include/final harness/16 unique source-binary bindings and3 complete traces verified |

Full pytest was not rerun in this resumed cloud environment because pytest is unavailable. No new77/77 claim is made. Prior verified eCSD evidence is retained; affected native regression was already executed and recovered rather than duplicated.

## Retained native test failure

Initial CSA harness passed147 and failed7 identical false-direction assertions. Diagnostics showed readable=true, valid=false, confirmation0 and event length0; MQL4 ZeroMemory string comparison to literal empty returned false. Replace the assertion with StringLen(eventId)==0. No production predicate changed; final harness hash cdaa7dbc6f758694b432dffa2a533dd3880bd2253d6e577bc1fc1c76082b852b is bound to154/154. The original RED manifest remains in csa608_native_evidence.json. Controller harness also verifies false-direction identity by length.

The resumed verification recovered already-completed native/controller artifacts, checked actual processes, recomputed exact bindings and archived full traces. No primary-terminal restart or duplicate native run was needed.

## Limits and next signal

M30 remains the declared complete-bucket fixture. The seven-TF source checks do not authenticate market/session completeness. Timer delivery is harness-driven; arbitrary cold-start structural epoch, wall-clock timers, positive entry, multi-symbol broker execution and profitability are not proved. All77 semantic availability cells and custom auto-entry stay OFF.

SIG-01 eCSD is reused. SIG-02 CSA source/context is complete in this scope. SIG-03 CSAK/CSD is next, after this publication is verified. CSD deliberately retains historical Open/body logic until that task; overall T04-D/F and later custom-trigger/selection/risk/execution gates remain incomplete. No merge or deployment.
