# NMJE V2 P2 Counterfactual Equal-Candidate Shadow Attribution — 2026-09-25

Status: **VALIDATED / TESTER-ONLY SHADOW RESEARCH / P2 ORDERING HOLD REMAINS**

Issue: #101
Owner base: `d1-owner-dev@0034f31aced4e630d0b76ce64009a41078ba7cb3`

## 1. Objective

Build attributable counterfactual evidence for already-eligible equal-direction BBMA candidates without:
- changing M15 candidate ordering;
- rejecting or delaying the baseline decision;
- invoking risk approval for alternatives;
- sending duplicate orders;
- creating a second processing clock;
- inventing M5 semantics.

The research question is whether an alternative already-eligible candidate can be compared against the actually selected baseline candidate using common market exposure assumptions.

## 2. Build identity

- Build: `5.14`
- Build tag: `V514_NMJE_P2_COUNTERFACTUAL_SHADOW_20260925`
- Final source revision: `NMJE_P2_COUNTERFACTUAL_SHADOW_004_20260925`
- Final MQ4 SHA-256: `6C375BC36C5971097DE69B12586B1DD50F1445BE5E10D293A4D87CDCFC62C4EC`
- Production EX4 SHA-256: `DED8AB7B407DFF40E9CCCF5306AC224C970802F40FC36D896958A3CA916673A5`
- Tester-harness EX4 SHA-256: `DC8120885BBCE4CAACE7A266B15567DD642B489746FF72D9994A04D11F1B0ED7`
- Accepted Strategy-Core delta: **NONE**

## 3. Architecture

### 3.1 Capture boundary

On the sole closed-M15 processing cycle, P2 observes the already-valid candidate pool before `PriorityEngine_Atomic`.

It stores a tester-only, cycle-local pending set containing candidate identity and observer metadata only.

The canonical comparator remains untouched.

### 3.2 Baseline selection authority

`PriorityEngine_Atomic` and M16 run exactly as before.

Only after the real baseline order is successfully filled does the research overlay bind the pending alternatives to:
- the actual baseline ticket;
- actual baseline open time;
- actual baseline fill price.

No counterfactual candidate calls:
- `CheckRiskBeforeTrade`;
- `CalculateLotSize`;
- `FinalPortfolioGuard`;
- `ProcessEntry`;
- `OrderSend`;
- `OrderClose`.

### 3.3 Candidate-specific protective geometry

For each alternative, the overlay reuses the already-approved semantic source logic:
- standalone Re-Entry -> H1 Re-Entry;
- REM -> H4 Re-Entry;
- RRE/REE -> D1 Re-Entry;
- standalone Extreme -> H1 Extreme.

The common baseline fill price is an explicit **engineering research proxy**, not a Strategy-Core rule.

### 3.4 Paired outcome window

For candidates with resolved static SL/TP:
- only complete closed M1 bars after baseline fill and up to baseline close are examined;
- BUY uses Bid-history geometry;
- SELL uses frozen preflight spread as an explicit Ask-side engineering proxy;
- same-M1-bar SL+TP contact = `AMBIGUOUS_SAME_M1_BAR`;
- no tick-order assumption is invented.

Targetless lifecycle candidates remain `UNCOMPARABLE_TARGETLESS`.
No counterfactual TP/lifecycle exit is manufactured.

### 3.5 Identity dedup

The raw equal-eligible pool may contain metadata variants that collapse to the same executable research identity.

Final rev004 dedup is performed only after the actual baseline decision is known and after candidate-specific semantic SL/TP geometry is derived.

Execution-equivalent identity requires equality of:
- signal type;
- direction;
- sequence hash;
- anchor/start time;
- semantic SL/TP source type/timeframe/candle;
- resolved/targetless status;
- SL/TP geometry.

Geometry-distinct variants remain separate alternatives.

## 4. Runtime fix history

### rev001 / rev002
Exploratory runtime exposed four sets containing duplicate execution-equivalent Re-Entry rows.

Impact: duplicate research alternatives could over-count one executable identity.

Fix: selected-aware execution-geometry dedup; baseline-selected variant is evaluated first.

### rev003
Dedup succeeded, but three cycles collapsed to one unique candidate while `[Q9-P2-CF-OPEN]` had already been emitted.

Impact: 3 OPEN rows had no corresponding OUT row.

Fix: active set is committed and OPEN telemetry is emitted only when final unique `active.Count >= 2`.

### rev004
Final runtime closure passed all pairing, dedup and authority checks.

## 5. Static / compile validation

- `git diff --check`: PASS.
- Targeted P2 counterfactual regression: **PASS**.
- Protected functions byte-normalized exact to owner Build 5.13:
  - `CompareCanonicalCandidates`;
  - `PriorityEngine_Atomic`;
  - `InvalidationEngine_Atomic`;
  - `CheckRiskBeforeTrade`;
  - `IsSignalAllowed`;
  - `ResolveExecutionReferencePrice`;
  - `ResolveSelectedSLTPSourceComponent`;
  - `IsApprovedSLTPSourceComponent`;
  - `SendOrderWithRetry`;
  - `RunEntryPreflightAndExecute`.
- Broker primitive counts unchanged: `OrderSend=1 / OrderClose=3`.
- Production MetaEditor compile: **0 errors / 0 warnings**.
- Tester harness compile: **0 errors / 0 warnings**.
- Full repository Python suite: **72/72 PASS**. Initial run exposed a test-extractor fragility in `test_q5_standalone_extreme_175.py`: the helper matched the new pre-definition call to `ResolveApprovedInitialSLTP` instead of the function definition. The extractor was tightened to definition syntax; canonical M17/SLTP source code remained byte-identical under the protected-function regression.

## 6. Final rev004 Strategy Tester evidence

Environment:
- GBPUSD
- M15
- 2026-08-01 through 2026-09-01
- baseline execution path unchanged

Observed:
- raw equal-eligibility cycles: **200**;
- executed counterfactual sets after baseline fill + final dedup: **3**;
- counterfactual OPEN rows: **9**;
- counterfactual OUT rows: **9**;
- selected rows: **3**;
- alternative rows: **6**;
- execution-equivalent duplicate sets: **0**;
- OPEN/OUT pairing errors: **0**;
- candidate-ID pairing errors: **0**;
- selected baseline geometry match: **3/3**;
- M5 semantic-resolved rows: **0**;
- capacity skips: **0**;
- fatal runtime errors: **0**.

Outcome coverage:
- alternative static-SL/TP comparable windows: **1**;
- alternative `UNCOMPARABLE_TARGETLESS`: **4**;
- alternative `UNCOMPARABLE_SLTP_UNRESOLVED`: **1**;
- the one comparable alternative remained `UNRESOLVED_AT_BASELINE_CLOSE`.

Authority regression:
- canonical executions: **14**;
- Build 5.13 baseline executions: **14**;
- exact execution trace equality: **PASS**;
- tester report trade/performance fields equal Build 5.13: **PASS**.

## 7. Research conclusion

The infrastructure now provides attributable equal-candidate counterfactual shadow records without changing live strategy behavior or creating duplicate trades.

However this August sample does **not** justify active P2 ordering:
- only 3 real baseline fills had at least 2 unique execution-distinct candidates;
- only 1 alternative had a static-SL/TP window that could be meaningfully evaluated;
- 4 alternatives were targetless and correctly left uncomparable;
- 1 alternative had unresolved SL/TP;
- no M5 semantic discrimination exists.

Therefore:
**P2 active coherence tie-break remains HOLD / NON-EXECUTABLE.**

Future P2 policy research may reuse this attribution layer, but any targetless alternative comparison requires a separately validated lifecycle-replay methodology; it must not be invented inside this patch.

## 8. Evidence

- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/evidence_manifest_rev004.json`
- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/targeted_regression_result.json`
- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/final_runtime_analysis_rev004.json`
- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/runtime_rev004_key_rows.log`
- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/execution_trace_514_rev004.txt`
- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/native_compile_rev004.log`
- `blueprint/audits/evidence/NMJE_V2_P2_COUNTERFACTUAL_20260925/harness_compile_rev004.log`

## 9. Exit decision

Counterfactual equal-candidate shadow attribution is complete for the current research-safe scope.

Classification:
- implementation: **VALIDATED RESEARCH OVERLAY**;
- strategy authority: **NONE**;
- P2 ordering: **HOLD**;
- M5 execution authority: **NONE**;
- Strategy-Core delta: **NONE**.
