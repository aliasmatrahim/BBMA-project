# Q9 NMJE V2 P2 — Equal-Eligibility Coherence Tie-Break Policy / Evidence Adjudication — 2026-09-25

Status: **DECIDED / COHERENCE METADATA SUPPORTED / ORDERING HOLD / NON-EXECUTABLE / NO EA CODE CHANGE**

Issue: #101  
Base: `d1-owner-dev@444949c06cdb3310ba15070c97b860bef85a080f`

## 1. Scope

This decision adjudicates whether NMJE journey-coherence metadata may become an active deterministic tie-break when two or more already-eligible same-direction BBMA candidates compete on one M15 processing cycle.

This decision does not change:
- canonical candidate eligibility;
- D1 strategic authority;
- REM/RRE/REE signatures;
- M15 sole final-decision ownership;
- M16 revalidation;
- semantic SL/TP ownership;
- risk/MM;
- broker execution.

## 2. Source route used

Mandatory source/evidence route was followed:
- `docs/references/SOURCE_INDEX.md`;
- accepted `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- primary PDF pages 12-13 for REM/RRE/REE + higher-TF trend alignment;
- Finale V05/V06 MTF evidence and reconciliation;
- authenticated Home Course MTF/major-trend evidence;
- G40-wide reconciliation closure;
- active M12N/M15/M16 contracts;
- current Build 5.13 source;
- Build 5.12/5.13 targeted regression and Strategy Tester evidence;
- historical Stage-C P2/P3 contract as provenance only.

## 3. Source findings

### 3.1 Journey coherence / MTF alignment is source-supported context

Primary PDF pages 12-13 define REM/RRE/REE as three-timeframe setups and explicitly require higher-timeframe trend/alignment context.

Finale V05/V06 strongly corroborate:
- higher-timeframe Re-Entry read through lower-timeframe supporting structures;
- related timeframe chains;
- lower-TF activity must be interpreted inside higher-TF context;
- mixed-direction shortcut teaching exists, but the reconciled hard-coding status remains HOLD.

Home Course likewise supports higher-TF direction and lower-TF continuation/retracement reading.

Therefore:
**journey coherence is legitimate BBMA context/metadata.**

### 3.2 Source does not define a deterministic candidate ordering

No accepted primary/Core source defines a universal ordering such as:
- `ALIGNED > SUPPORTING > BUILDING > CONFLICT > UNRESOLVED`; or
- REM > RRE > REE; or
- Re-Entry > Extreme > REM/RRE/REE for simultaneous already-eligible candidates.

The primary PDF defines valid setup families and higher-TF alignment, not an arbitration comparator between simultaneous valid candidate identities.

Finale qualitative wording that Re-Entry is safer/best does not define a deterministic simultaneous-candidate comparator and is not sufficient to override the active M15 no-arbitrary-ranking contract.

Therefore:
**an active P2 coherence ordering is not directly source-owned.**

## 4. Active M15 authority boundary

Current M15 explicitly states:
- no invented REM/RRE/REE superiority;
- same-direction multiple candidates are canonicalized only for stable identity/bookkeeping;
- comparator order is latest component anchor -> latest sequence start -> deterministic sequence hash;
- this ordering must not be represented as setup quality superiority.

P2 activation would alter this boundary.

A coherence-based winner can change:
- selected `SignalType`;
- selected `SequenceHash`;
- frozen component identity;
- semantic SL/TP source.

Current SL/TP source differs by selected family:
- standalone Re-Entry -> H1 Re-Entry;
- REM -> H4 Re-Entry;
- RRE/REE -> D1 Re-Entry;
- standalone Extreme -> H1 Extreme.

Therefore P2 ordering is not harmless metadata even if trade count stays constant. It can change trade identity and protective geometry.

Classification: **STRATEGY-SELECTION POLICY CHANGE**.

## 5. Current P2 runtime evidence

Exact Build 5.12 rev003 Strategy Tester segment:
- log: `D:\BBMA\MT4_TesterRunner_OfflineDiag\tester\logs\20260925.log`;
- Build 5.12 rev003 starts at log line 19071;
- next Build marker begins at line 38136;
- exact rev003 P2 segment = lines 19071..38135.

Observed:
- **200 equal-eligibility M15 cycles**;
- **472 candidate telemetry rows**;
- eligible-candidate count distribution:
  - 134 cycles with 2 eligible candidates;
  - 62 cycles with 3;
  - 2 cycles with 4;
  - 2 cycles with 5.

Candidate rows include Re-Entry, Extreme, REM and RRE examples.

However the rev003 P2 telemetry has no discriminative coherence evidence:
- all observed rows in the exact rev003 segment had `ParentMatch=Y`;
- all had `M5Present=Y`;
- P3 M5 is snapshot-only and has no source-owned semantic state;
- therefore M5 presence cannot distinguish candidate quality/coherence.

This proves that simultaneous eligibility occurs in practice, but it does **not** prove which candidate should win.

## 6. Outcome-attribution limitation

Current P4 durable attribution freezes the **selected** canonical decision/trade after validation and joins that selected identity to the realized closed-trade outcome.

It does not produce a source-valid counterfactual closed-trade outcome for every unselected equal-eligible candidate.

Therefore the current evidence cannot answer:
“Would selecting candidate B instead of the canonical candidate A have improved accuracy?”

Current 14-trade rev006 outcome evidence is valid for the executed baseline path only. It is not evidence for a P2 comparator.

## 7. P2 policy decision

### Supported now
P2 may remain:
- equal-eligibility detector;
- read-only journey-coherence metadata;
- shadow telemetry;
- candidate-set observability;
- research attribution context.

### Not authorized now
P2 may not:
- reorder candidates;
- assign priority/score;
- change `CompareCanonicalCandidates`;
- change `PriorityEngine_Atomic`;
- select a different `SignalType`/SLTP source;
- reject/delay a sole valid candidate;
- use M5 snapshot presence as quality;
- infer a full five-timeframe coherence state while M5 semantic ownership is absent.

Classification:
**P2 ORDERING = HOLD / UNRESOLVED / NON-EXECUTABLE.**

## 8. Release criteria for any future active P2 tie-break

P2 ordering may leave HOLD only when all are satisfied:

1. **Deterministic policy**
   - an explicit project decision defines the exact comparator semantics;
   - no hidden numeric score/voting system is introduced;
   - treatment of `ALIGNED/SUPPORTING/BUILDING/CONFLICT/UNRESOLVED` is explicit.

2. **Semantic inputs are authoritative**
   - every relation used by the comparator comes from canonical owner state;
   - if M5 participates, M5 semantic owner coverage must first exist under canonical M08/M09/M10/M12 ownership;
   - raw OHLC/M5 presence alone is insufficient.

3. **Attributable shadow evidence**
   - equal-eligible alternatives are frozen with stable candidate identity;
   - the research method can compare candidate-selection consequences without sending duplicate live orders;
   - evidence is not inferred merely from the realized outcome of the currently selected candidate.

4. **Cross-module impact is explicitly validated**
   - selected signal family;
   - semantic SL/TP source;
   - M16 revalidation;
   - risk geometry;
   - duplicate/DecisionID behavior;
   - restart/recovery;
   - trade count and timing.

5. **Separate activation authorization**
   - because active P2 changes strategy selection, activation requires explicit strategy-policy approval plus static/native/regression/runtime evidence.

## 9. Current implementation disposition

Current Build 5.13 P2 implementation:
- records equal-eligibility telemetry only;
- does not write order/score/reject state;
- does not touch protected comparator, M16, risk, SL/TP or execution functions.

This remains correct.

Classification: **NO FIX**.

No Build bump, native compile or Strategy Tester rerun is required because this adjudication changes no EA source bytes.

## 10. Final P2 status

- BBMA MTF/journey coherence concept: **SOURCE-SUPPORTED**.
- Equal-eligibility observability: **VALIDATED SHADOW METADATA**.
- Deterministic active coherence comparator: **NOT SOURCE-DEFINED**.
- Current runtime discriminatory evidence: **INSUFFICIENT**.
- Active P2 ordering: **HOLD / NON-EXECUTABLE**.
- M15 sole final authority: **UNCHANGED**.
- Accepted Strategy-Core delta: **NONE**.
- Current EA code fix: **NONE**.
