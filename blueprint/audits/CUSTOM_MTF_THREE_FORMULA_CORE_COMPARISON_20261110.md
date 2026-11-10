# Three-formula comparison against founder/Core evidence — 2026-11-10

Task C/T04-D. Branch feat/custom-mtf-v1-20261108, base a149da67d578c19a94d12f6e0d14bd8d9ea8f865. Source Build6.06 LF SHA0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e. No EA/include/test changes, alias admission, merge or activation. Publication SHA in Draft PR303.

This comparison concerns strong-direction/CSD versus candidate CSAK mechanics. It does not automatically map the user's independent MidBB CSA label to eCSD. Formula labels F1/F2/F3 below correspond to arithmetic keys A/B/C; they are not a new choice replacing the user's C+1 source-verification authorization.

## Exact predicates

O=open, C=close of the same valid closed source candle. M=MidBB; H5/H10=MA High pair; L5/L10=MA Low pair at that source bar. Valid positive data/readiness is assumed for the numerical comparison, not bypassed in the EA.

| Formula | BUY | SELL |
|---|---|---|
| F1 / A: current locked all-line body span | O <= min(M,H5,H10), C > max(M,H5,H10) | O >= max(M,L5,L10), C < min(M,L5,L10) |
| F2 / B: bare close-side interpretation | C > max(M,H5,H10) | C < min(M,L5,L10) |
| F3 / C: published Mid-only open crossing | O < M, C > max(M,H5,H10) | O > M, C < min(M,L5,L10) |

F2 deliberately contains no unannounced colour, previous-close, first-cross or dedup rule. Adding one would create a fourth predicate to be specified separately. An aligned-colour requirement alone still permits repeated aligned continuation bars. None of these equations alone grants entry authority.

## Source comparison

| Evidence retrieved under SOURCE_INDEX | Explicit support | What it does not settle |
|---|---|---|
| Primary PDF page8 | eCSD crosses MA5/10; CSD additionally crosses MidBB; MidBB conveys stronger intent | Numeric open inequalities, equality handling and whether one body must span every line |
| Accepted Core V2 section7 | Retains MA-pair and MidBB crossing plus signal-only role | Does not provide a standalone numeric open/equality/event formula |
| Original V05 subtitles33:54-34:17 and extracted OA-F-V05-011 | Close beyond MA5/10 High or Low plus MidBB identifies strong direction | Open-side geometry is not explicit in these statements |
| Original V06 subtitles20:07-20:18 / OA-F-V06-004 | Close beyond MA5/10 and MidBB; raw SRT has noisy words already recorded by extraction | No deterministic open comparison can be inferred from the noisy wording |
| Registered Tier-B Workbook Lesson9 | Corroborates the required close side | No explicit numerical open restriction recovered; existing provenance ceiling unchanged |
| Locked M10 source contract | F1 is the chosen deterministic body-span engineering interpretation, explicitly not verbatim Oma Ally wording | A project choice is not independent founder proof that F2/F3 must be rejected |
| Current DetectCSD plus shared helper | Implements F1 exactly, including inclusive open equality | Correct implementation of its contract does not resolve the source ambiguity |
| Marlina/SEMMAU researcher implementation, printedp179 | Explicit F3 equations | Does not establish founder authority or modify Core; no independent MA-open constraint is coded |

Research source: https://publikasi.uyelindo.ac.id/index.php/semmau/article/download/236/205/570 . Founder/PDF attribution and original-source provenance limits remain as in SOURCE_INDEX; this audit does not independently authenticate authorship or overrule accepted contracts. Existing frames did not resolve a labelled open-side counterexample.

## Reproducible numerical witnesses

Hypothetical geometry only, not recorded market OHLC or proof of profitability. SELL mirrors are in result.json.

| BUY situation | M / H5 / H10 | O -> C | F1 | F2 | F3 |
|---|---|---|---|---|---|
| All required lines crossed | 100 / 102 / 104 | 99 -> 105 | YES | YES | YES |
| Open already beyond both MAs, before Mid | 100 / 98 / 99 | 99.5 -> 101 | NO | YES | YES |
| Open already beyond Mid, closes above MAs | 100 / 102 / 104 | 101 -> 105 | NO | YES | NO |
| Aligned continuation above all lines | 100 / 102 / 104 | 105 -> 106 | NO | YES | NO |
| Opposite-colour body remains above all lines | 100 / 102 / 104 | 106 -> 105 | NO | YES | NO |
| Open exactly at Mid | 100 / 102 / 104 | 100 -> 105 | YES | YES | NO |
| Open exactly at a required MA | 100 / 98 / 99 | 98 -> 101 | YES | YES | YES |
| Close exactly at highest required line | 100 / 102 / 104 | 99 -> 104 | NO | NO | NO |

Important geometry result: when BUY High MAs are both at/above MidBB (SELL Low MAs both at/below MidBB), F1 and F3 agree except O==Mid equality. Differences therefore depend on line arrangement and equality, not merely the chosen label. F1 and F3 are both subsets of F2; F1 is not an unconditional subset of F3 because of inclusive open equality. No claim about real-market prevalence follows from the synthetic grid counts.

## Signal versus zone versus event

All three require the same close-side destination. F2 alone can identify a continuing zone, including opposite-colour candles, and cannot determine which occurrence is the new direction event. F1/F3 encode within-body crossing but still do not settle entire lifecycle/dedup, same-cycle identity, later strengthening or reuse as combination context. These remain separate owner/evaluator decisions. A raw signal is not Re-Entry, risk approval or execution authority.

## Findings and ruling

- VERIFICATION REQUIRED: no retrieved founder/Core statement resolves the exclusive numeric open/equality choice. The stronger shared evidence is the required close beyond all relevant lines.
- NO FIX: current DetectCSD matches its locked F1 contract. No confirmed implementation bug is established by this comparison.
- ENGINEERING ASSESSMENT: F3 is a useful candidate for source adjudication because it explicitly tests MidBB transition without requiring each MA-open cross. This is a candidate rationale, not a source acceptance or instruction to replace F1.
- F2 is incomplete as a new-event detector without a separate justified event rule; do not add colour/first-cross/TTL rules silently to make it appear complete.
- Keep F1 executable mapping unchanged. CSA/CSAK alias/event admission stays unresolved; all77 custom availability cells and auto-entry OFF. T04-D PARTIAL, B/E epoch/session HOLD, F/T05 dependencies unchanged.

## Actual validation

`python blueprint/audits/evidence/CUSTOM_MTF_THREE_FORMULAS_20261110/compare.py`:16 explicit BUY/SELL witnesses PASS;33,614 hypothetical geometry cases PASS; actual extracted DetectCSD/helper code, compiled as host C++ with platform I/O stubs, matches F1 on33,614 cases. Final host compile has no warnings. Initial audit-adapter misleading-indentation warning was corrected; EA source unchanged.

`python blueprint/tests/custom_mtf/test_m10_shared_pair.py`: existing targeted shared-helper regression driver PASS,19,683 C++ cases. An initial pytest invocation on that module collected no tests (exit5); it is a top-level executable driver, so the proper direct Python command was used. No pytest test-count claim is made from that invocation.

Audit script py_compile and git diff --check PASS. These are offline numeric/source checks, not native MQL4 compile, full runtime, market backtest or source-authority validation. Prior exact-source native compile and full cloud75/75 remain historical and were not duplicated.

## Exact next action

Resolve the remaining source decision narrowly: a labelled candle where its open is beyond a required MA but before MidBB, an open-equals-Mid case, and first-direction versus later-strengthening classification. An explicit decision must reconcile PDF/Core, original teaching and the locked engineering contract before any detector change. Owner-epoch acquisition remains independent and cannot be satisfied by these numerical witnesses. Do not search/re-extract already reviewed frames as if new evidence, or advance T04-F/T05 by treating the arithmetic PASS as founder-rule proof.
