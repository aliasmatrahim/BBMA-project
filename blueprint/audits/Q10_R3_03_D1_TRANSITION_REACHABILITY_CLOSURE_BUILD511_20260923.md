# Q10 R3-03 D1_TRANSITION Reachability Closure — Build 5.11 — 2026-09-23

Issues: #248, #109  
Baseline owner: `d1-owner-dev@a162a2b3d8c7337e1347f7d8f8f0b2f469c34618`  
Scoped branch: `fix/r3-03-d1-transition-reachability`  
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Result

**R3-03 = PASS / DETERMINISTIC_BY_CONSTRUCTION.**

Classification: **SOURCE/CONTRACT/ACCEPTANCE RECONCILIATION / NO EA SOURCE CHANGE / NO NEW BBMA RULE**.

The prior HOLD was valid while the project expected a naturally observable non-equality `D1_TRANSITION`. Source/contract reconciliation now proves that expectation was incompatible with the canonical immediate EMA50(Close) formula.

## Source reconciliation

The source chain supports MA50/EMA50 as the trend reference, D1 as the scoped strategic owner, and the descriptive relationship of price side plus MA50 direction. The source does not specify a software transition state, alternate MA type, multi-day slope lookback, tolerance band, ATR/pip threshold, or frozen previous direction.

The Home Course ledger explicitly records MA50 as period 50, Exponential, applied Close.

For canonical EMA(Close):

`EMA_t - EMA_(t-1) = alpha * (Close_t - EMA_(t-1))`

and

`Close_t - EMA_t = (1-alpha) * (Close_t - EMA_(t-1))`.

For `0 < alpha < 1`, both expressions have the same sign. Therefore a non-equality same-bar price/immediate-slope disagreement is not reachable.

The old examples “price above EMA50 while immediate EMA50 falls” and “price below EMA50 while immediate EMA50 rises” are specification artifacts, not observable states under the canonical formula.

## Contract correction

The D1 strategic-owner hierarchy is unchanged.

- BUY/SELL owner semantics remain as currently implemented.
- `D1_OWNER_UNRESOLVED` remains invalid/missing-history fail-closed state.
- `D1_TRANSITION` remains a fail-closed software state with `DIR_NONE`.
- Natural valid transition under the immediate EMA mapping is limited to equality/flat degeneracy and need not occur in finite broker history.
- No H4/LTF fallback is allowed.
- No live-position close authority is created.
- No new EMA/lookback/tolerance/confirmation rule is introduced.

The current M11 conjunction is retained because it is behaviorally equivalent to same-bar price-side classification for non-equality EMA(Close) data. Changing EA source would create unnecessary churn without changing reachable behavior.

## Q10 acceptance correction

R3-03 remains mandatory, but evidence mode is now deterministic by construction.

Required proof:
1. exact canonical Build 5.11 source identity;
2. EMA50 period 50;
3. `MODE_EMA` + `PRICE_CLOSE`;
4. immediate previous closed-D1 EMA comparison;
5. canonical BUY/SELL conjunctions intact;
6. transition fallback assigns `DIR_NONE`;
7. strategic execution readiness accepts only confirmed BUY/SELL;
8. no historical contradictory selection.

Natural non-equality transition occurrence is not required.

## Validation evidence

Exact canonical MQ4 SHA-256:
`50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`.

Updated hybrid analyzer on the existing four-period exact Build 5.11 evidence:
- R3-03: **PASS**;
- evidence mode: `DETERMINISTIC_BY_CONSTRUCTION`;
- natural transition observations: `0`;
- contradictory selections: `0`;
- all eight source/reachability/fail-closed checks: **PASS**;
- analyzer summary: `34 PASS / 23 INCOMPLETE / 0 FAIL` before reuse of the later targeted Phase-H closure supplements;
- analyzer output SHA-256: `FF241886F084B141EE5028A91609C30A6003BAD6CF0B593E6CAF292C65023EB3`.

Python regression on the scoped branch:
- `py -3.12 -m pytest -q`;
- **59 passed**.

No Strategy Tester rerun was performed. Existing exact Build 5.11 hash-addressed historical logs were reused.

## Phase-H consequence

The authoritative previous combined checkpoint was:
- 55 PASS;
- 2 INCOMPLETE;
- 0 FAIL;
- mandatory HOLD: R3-03;
- conditional INCOMPLETE: R5-19.

Applying only this reconciled R3-03 result gives:
- **56 PASS**;
- **1 INCOMPLETE**;
- **0 FAIL**;
- mandatory HOLD: none;
- conditional INCOMPLETE: R5-19 only.

This is an **allowed Phase-H completion state** under the existing matrix exception for unsafe emergency-precedence evidence. Phase L MetaQuotes-Demo is therefore eligible after integration of this reconciliation.

## Regression / release impact

- EA `.mq4`: unchanged.
- Build/tag: unchanged at Build 5.11.
- Native MQL4 compile: not required by this patch because EA source bytes are unchanged.
- Strategy Tester rerun: not required and not justified.
- Runtime behavior: unchanged.
- Strategy Core execution authority: unchanged.
- Q10 acceptance/tooling/documentation: corrected.

Evidence:
- `blueprint/audits/evidence/Q10_R3_03_RECONCILIATION_20260923/R3_03_RECONCILIATION.json`;
- `blueprint/audits/evidence/Q10_R3_03_RECONCILIATION_20260923/COMBINED_STATUS_V4.json`;
- `blueprint/decisions/R3_03_D1_TRANSITION_REACHABILITY_RECONCILIATION_20260923.md`.

## Final classification

**NO EA FIX. CONTRACT/ACCEPTANCE FIX REQUIRED AND VALIDATED.**

R3-03 is no longer a source/reachability HOLD. Phase L must still wait for this scoped reconciliation to be integrated into the owner branch.
