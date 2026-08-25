# BBMA Home Course 19-Page — Canonical Dedup + Core V2 Mapping Gate

Status: NEXT GATE COMPLETE — FORENSIC MAPPING / PROMOTION HOLDS IDENTIFIED
Date: 2026-08-25
Source ledger: `HOME_COURSE_19P_ATOMIC_LEDGER_20260825.md`
Target: `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`

## Method

The 189 provenance rows are retained in the atomic ledger. This gate collapses literal repetitions/restatements into canonical semantic rule families without deleting provenance. NON_CORE material is excluded from the coverage denominator. HOLD/ambiguous source claims remain applicable evidence but are not counted as covered merely because a related concept exists in Core V2.

A coverage number is publishable only when every canonical applicable rule family has a deterministic Core-V2 mapping. This gate completes the semantic-family mapping and identifies the remaining row-level normalization needed for a mechanically reproducible numerator/denominator.

## Canonical mapping results

### COVERED by Core V2

1. BB20/2 indicator contract and outer/Mid-BB structure.
2. MA5 High/Low, MA10 High/Low LWMA contracts.
3. EMA/MA50 Close structural/trend reference.
4. BB state matters; directional/expanding BB is required for accepted directional Momentum/CSM.
5. Outside-outer-BB close in accepted directional BB context = Momentum/CSM.
6. Horizontal-BB outside close is not silently treated as directional Momentum.
7. Extreme is signal/context rather than raw direct execution authority.
8. Strict Extreme MA-outside-BB structural basis.
9. Extreme reversal-confirmation lifecycle.
10. Extreme later retest / standalone entry-ready lifecycle.
11. Extreme normal TP-Wajib structure, with Core V2's refined opposite-MA5/10 first objective and Mid-BB farther context.
12. MHV/MLV follows valid prior Extreme provenance and normal TP-Wajib structural completion.
13. MHV failed-continuation/loss-of-momentum formation family.
14. MHV marked-body reference and later retest concept.
15. MHV is setup/context, not standalone execution authority.
16. Early/weak direction versus strong direction distinction (eCSD/CSD).
17. Re-Entry is principal entry/setup zone; do not execute simply because Candle Arah exists.
18. Re-Entry MA5/MA10 structural contact/non-exceedance family.
19. Powerful Re-Entry MA5+MA10+Mid-BB confluence.
20. Most-powerful Re-Entry confluence including MA50.
21. Source-supported minimum-three-candle Re-Entry wording.
22. First-candle confirmation / later entry wording is represented in the accepted Re-Entry lifecycle constraints rather than raw first-touch execution.
23. Direction/Momentum -> Re-Entry cycle progression.
24. Momentum -> further Re-Entry progression.
25. Sideways/ranging -> Re-Entry structural family.
26. MTF interpretation and higher-timeframe structural ownership/scaling.
27. Lower-TF setups should align with accepted higher-TF direction/owner context.
28. REM/RRE/REE exact approved signatures preserve the accepted MTF entry architecture.
29. Opposite Extreme / new-cycle supersession is represented in Core V2 lifecycle.
30. Canonical overall cycle: Extreme -> TP Wajib -> MHV/MLV -> direction -> Re-Entry -> Momentum -> Re-Entry -> opposite Extreme/restart.

### PARTIAL — Core V2 has the concept but Workbook is more explicit

P1. **Mid-BB named zones:** Workbook names Mid->Top `Buying Zone` and Mid->Low `Selling Zone`; Core V2 uses Mid BB structurally but does not canonicalize these names as an execution contract.

P2. **Mid-BB slope as same-TF trend guide:** structurally compatible but not exposed as a standalone canonical rule.

P3. **Direction-strength ladder:** Core V2 has eCSD/CSD, but Workbook's full weak -> strong -> MA50 strongest ladder is not separately canonicalized.

P4. **MA50/D1 major-trend wording:** Core V2 has higher structural/trend reference and explicit owner contracts, but Workbook's broad `major trend = MA50, minimum D1` wording is stronger and broader.

P5. **Lower-TF replay during three-candle Re-Entry:** Core V2 preserves MTF scaling and approved signatures but does not authorize every Workbook lower-TF replay/add-on instruction.

P6. **Sideways on larger TF creates a fresh smaller-TF setup:** structural idea is present, but Workbook wording is broader than executable approved signatures.

P7. **Candle Arah outer-BB destination:** cycle/direction intent exists, but Core V2 does not encode a universal deterministic outer-BB destination promise.

P8. **MA5 relationship as Momentum strength context:** Core V2 does not elevate `outside MA5` / `MA5 hugging BB` into separate Momentum validity tiers.

### MISSING / HOLD — must not be silently promoted

H1. **Horizontal-BB three-condition behavioral table:** wick outside/close inside, body+wick outside/close outside, near-boundary wick -> Mid-BB reversion expectations. Core V2 only locks the accepted non-directional-Momentum interpretation; the complete table is not canonical.

H2. **Absolute horizontal-BB width 10–20 pip breakout claim.** Instrument/precision dependence and absolute prediction make this unsuitable for silent Core promotion.

H3. **MA5-close Momentum definition / very-strong Momentum class.** Could be strength/context rather than validity; requires evidence reconciliation.

H4. **Universal D1 precedence over H4 (`D1 buy, H4 sell -> follow D1`).** Potentially conflicts with the project's explicit timeframe owner contract; strategy decision required if intended to alter execution ownership.

H5. **Double H1 Extreme -> H4 MHV inference.** Not currently a canonical deterministic detector.

H6. **Valid H4 MHV -> enter each H1 Extreme without waiting for H1 MHV.** Would expand execution authority and therefore requires explicit reconciliation/approval.

H7. **Valid H4 MHV means no further H1 MHV.** Absolute source wording is not canonical.

H8. **Strong direction reaches outer BB without Re-Entry and without Momentum -> hold until Re-Entry.** This is an execution/TP exception and is not silently promotable.

H9. **Direction -> Re-Entry -> no Momentum => mandatory close because market reverses.** Lifecycle concept is source-backed, but deterministic exit authority is not currently canonical.

H10. **MHV -> direction -> outer BB before Re-Entry -> no TP / wait for Re-Entry.** Same execution-management hold as H8.

H11. **Countertrend Candle Arah has guaranteed opposite outer-BB destination.** Predictive wording requires scope/evidence reconciliation.

H12. **Today's D1 close determines tomorrow's movement.** Directional context may be useful but absolute prediction is not canonical software law.

H13. **Extrem Magic: MA5 and MA10 both outside BB.** Workbook presents it as rare special structure; no accepted universal detector/authority exists in Core V2.

## NON_CORE exclusions

Excluded from denominator: MT4 menu instructions, colors/thickness cosmetics, example EURUSD choice, `lot besar`/small-vs-large-lot language, news-event entry instructions, account splitting/growth/withdrawal workflow, emotional-trading/account-purpose material, and guaranteed/marketing-style wording when it cannot be converted into deterministic source-supported Core behavior.

## Coverage gate result

The semantic mapping is now complete enough to state the key conclusion but **not yet to publish a defensible exact percentage**: the atomic ledger contains 189 provenance rows, while multiple rows are duplicates/restatements and several rows mix applicable and NON_CORE clauses. A mechanically reproducible denominator requires one final normalization pass assigning every HC-Pxx-xxx row to a canonical rule ID and `duplicate_of` pointer.

Therefore no invented `x/y` is published here.

What is already proven:
- Core V2 covers the large majority of the Workbook's executable BBMA skeleton.
- Eight material families are only partially represented.
- Thirteen material claims remain MISSING/HOLD and cannot silently change strategy.
- The most consequential unresolved items are D1-vs-H4 execution precedence, Double-Extreme->higher-TF-MHV inference, higher-TF-MHV lower-TF execution shortcut, and the post-direction/post-Re-Entry hold/TP rules.

## Promotion decision

**Do not promote Core V2 to V3 yet.**

Safe V2.x documentation clarifications may eventually include named Mid-BB zones and clearer direction-strength/MA50 context if corroborated, because these can be descriptive without changing execution authority.

Any change involving H4/D1 owner precedence, new MTF detector inference, lower-TF direct-entry shortcuts, or TP/hold behavior is a material strategy change and remains HOLD for explicit user decision after cross-source reconciliation.

## Next mechanical gate

Create `HOME_COURSE_19P_CANONICAL_ROW_MAP_20260825.md` with one record for every one of the 189 provenance rows:

`source_row | canonical_rule_id | duplicate_of | applicability | core_v2_section | status | note`

Then compute exact unique applicable canonical denominator and exact COVERED/PARTIAL/MISSING/HOLD counts. PARTIAL must not be counted as fully covered unless a separate weighted metric is explicitly defined.