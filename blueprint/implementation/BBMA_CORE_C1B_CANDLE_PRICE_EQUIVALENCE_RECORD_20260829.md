# BBMA Core C1-B Candle-Price Equivalence Record — 2026-08-29

## Scope

Extend C1-A with deterministic closed-candle numeric examples bound to the
existing build-4.71 MQL4 predicates. This is audit-only verification. It does
not change EA source, detector geometry, opportunity frequency, authority,
risk, execution, or lifecycle behavior.

Branch and PR boundary:

- branch: `bbma-core-truth-table-dev`;
- draft PR: `#104`;
- base remains `d1-tpw-checkpoint-hardening-dev`;
- no change targets `main`;
- no activation or merge authorization.

## Fixture coverage

The 59 explicit expected-result cases cover both BUY and SELL plus equality
and wrong-direction boundaries for:

- RAW Extreme outside-BB MA predicates;
- reversal direction;
- directional candle-body level crossing;
- expanding/directional/outside-BB CSM;
- CSD versus eCSD MID-BB distinction;
- Re-Entry MA-cluster and MA5/MA50 touch;
- Type-1 full-cluster close-side failure and structural retrace;
- Extreme retest start, frozen-body interaction, and MA5 interaction;
- MHV TP-Wajib completion, inside-BB/non-CSM loss phase, move-away, and
  frozen-marked-body retest.

Strict comparisons (`>`, `<`) and inclusive interactions (`>=`, `<=`) are
tested at equality boundaries. Undefined direction remains fail closed.

## Verification

- `BBMA_CORE_CANDLE_PRICE_EQUIVALENCE=PASS cases=59`
- `BBMA_CORE_CANDLE_PRICE_SOURCE_STATIC=PASS`
- C1-A truth table/source guards: PASS
- complete N3/NMJE/D1TPW/core regression target: PASS
- Python compileall target: PASS
- EA source SHA-256 remains
  `c6a87f613495547ee3cf52a8fe041ae6f9a63396075c0c755a7475b9f488a7bb`
- native MetaEditor is not rerun because `.mq4` remains unchanged.

## Evidence boundary

The Python model mirrors and statically locks the source predicates; it does
not execute compiled MQL4. Native Strategy Tester/runtime equivalence and
historical performance remain C3 evidence. This record cannot authorize NMJE
execution, D1TPW, C044, KIV risk features, demo/live use, merge, or release.

