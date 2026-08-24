# BBMA Home Course — Full 19-Page Forensic Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Workbook: `333531988-BBMA-Home-Course.pdf`  
Workbook SHA-256: `b20b8de38d878fa192d0a2fb9d70aba15b59208b477a3cefe73936974a5c2ee7`  
Workbook provenance: **Tier B / Strong-Provenance Copy**  
Code comparison baseline: latest isolated D1 build on `d1-owner-dev`, commit `823393dcee453d9eda09e535440f8cda9ab6a134`, build `Version 4.5.1 - D1-05 Input Limit Guard`  
Status: **FULL 19/19 PAGE INVENTORY COMPLETE — SOURCE PROMOTION / CODE CHANGES NOT AUTOMATICALLY AUTHORIZED BY THIS AUDIT**

## 1. Purpose

Close the remaining source-expansion gap by reviewing the complete 19-page Home Course Workbook page-by-page instead of relying only on previously selected high-value findings.

Required flow applied here:

`Workbook page-by-page -> extraction -> classification -> PDF / Finale / forum cross-check -> conflict handling -> Core V2 comparison -> Blueprint/contracts comparison -> latest code comparison`

This audit does **not** silently promote every workbook sentence into Strategy Core. Workbook-only, qualitative, personal, ambiguous, or conflicting claims remain subordinate to the source hierarchy.

## 2. Source hierarchy used

1. `PROJECT_INSTRUCTIONS.md`.
2. `docs/references/SOURCE_INDEX.md`.
3. Primary operational source: `Oma ally BBMA - AL.pdf`.
4. Secondary/historical source: `BBMA technique.pdf`.
5. Finale V01-V07 synthesis and conflict register.
6. Forum evidence as community / supplemental / non-authoritative corroboration only.
7. Tier-B Home Course Workbook, reconciled rule-by-rule.
8. `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`.
9. Current contracts / Blueprint.
10. Latest isolated implementation on `d1-owner-dev` for code-gap status.

Forum review remains subordinate. The current forum index explicitly records **no forum-only Core changes**.

## 3. Classification legend

- **ALREADY APPLIED** — accepted in canonical Core/contracts and represented by the latest relevant implementation where implementation is required.
- **CORROBORATION** — strengthens an already accepted rule; no semantic change required.
- **NEW RULE / HOLD** — strategy-relevant workbook content not yet accepted as canonical; requires explicit higher-precedence reconciliation.
- **CONFLICT / HOLD** — wording conflicts with, weakens, or over-generalizes an accepted higher-precedence rule; do not encode literally.
- **NOT STRATEGY-CORE** — UI instructions, colours, personal money/risk/account workflow, news-specific practice, or qualitative teaching emphasis that does not belong in universal BBMA Strategy Core.
- **NEEDS CODE FIX** — source/Core status is already sufficiently resolved, but the latest code still does not implement the accepted behavior.

A row may carry two labels where appropriate, e.g. `CORROBORATION + NEEDS CODE FIX`.

## 4. Page-by-page forensic inventory

### Page 1 — Lesson 1: Bollinger Band setup / basic state

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P1-01 | Use EUR/USD chart. | NOT STRATEGY-CORE | Teaching/example instrument only; EA remains multi-pair. |
| P1-02 | Bollinger Bands is the first indicator. | CORROBORATION | BB is canonical indicator. |
| P1-03 | MT4 menu steps to insert BB. | NOT STRATEGY-CORE | Platform tutorial only. |
| P1-04 | Default BB visual colour / thickness. | NOT STRATEGY-CORE | Cosmetic only. |
| P1-05 | BB has Top, Low and Mid lines. | CORROBORATION | Canonical BB structure. |
| P1-06 | BB expands, contracts/flat/sideway and those states carry meaning. | ALREADY APPLIED | M07/F5 BB-state architecture exists; M10 uses directional/expansion context. |
| P1-07 | Expansion from flat indicates strong momentum. | CORROBORATION | Higher-precedence Finale/Core requires directional expansion plus outside close for executable Momentum. |
| P1-08 | BB is a boundary; candles normally remain inside. | CORROBORATION | General BBMA teaching context; not a literal hard invariant. |
| P1-09 | Normal candles play inside BB. | CORROBORATION | Context only. |
| P1-10 | Candle outside BB is abnormal / meaningful. | CORROBORATION | Meaning depends on BB state and cycle context. |
| P1-11 | Flat BB = no momentum / sideways. | ALREADY APPLIED | Canonical Core explicitly distinguishes flat BB from directional Momentum. |
| P1-12 | Greater BB expansion = stronger movement. | CORROBORATION | Qualitative strength statement; not encoded as a numeric score. |
| P1-13 | Two broad BB conditions: directional/vertical vs flat. | CORROBORATION | Canonical state distinction already represented. |

### Page 2 — Flat vs directional BB behavior

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P2-14 | Flat BB and directional BB must be interpreted differently. | ALREADY APPLIED | Directly aligned with Core V2 Momentum semantics. |
| P2-15a | Flat BB, wick pierces Top and closes inside -> price expected toward Mid BB. | NEW RULE / HOLD | Contextual mean-reversion teaching; not currently an executable universal entry/TP rule. Needs primary/Finale chart-specific reconciliation before any code use. |
| P2-15b | Flat BB, wick pierces Low and closes inside -> price expected toward Mid BB. | NEW RULE / HOLD | Symmetric contextual rule; same HOLD. |
| P2-15c | Flat BB, body/wick outside and close outside -> move at least toward Mid BB. | CONFLICT / HOLD | Literal wording is directionally ambiguous and cannot override canonical rule that flat-BB outside close is **not directional Momentum**. |
| P2-15d | Wick does not pass outer BB -> price expected toward Mid BB. | NEW RULE / HOLD | Too broad / insufficient deterministic context. |
| P2-16a | Directional BB, wick pierces outer band and closes inside -> price continues current direction. | NEW RULE / HOLD | Plausible instructional context but not a currently accepted universal Boolean. |
| P2-16b | Directional BB, body/wick closes outside -> price continues current direction. | CORROBORATION | Compatible with Momentum only when canonical directional/expansion requirements are satisfied. |
| P2-17 | Any candle close outside BB is Momentum. | CONFLICT / HOLD | **Do not encode literally.** Current Core requires outside close **plus expanding/directional BB**; flat-BB outside close is not directional Momentum. |
| P2-18 | Flat BB width 10-20 pips predicts a large breakout. | CONFLICT / HOLD | Exact pip threshold is not established in higher-precedence Core and would introduce a volatility-style threshold. Not authorized. |
| P2-19 | Refer to multiple timeframes. | CORROBORATION | Strongly supported by primary PDF, Finale and forum. |
| P2-20 | Outside close in directional BB: follow direction, do not fight it. | CORROBORATION | Directional Momentum principle, subject to canonical state/owner gates. |
| P2-21 | Every outside close on directional BB has a lower-TF Re-Entry. | NEW RULE / HOLD | Strong MTF teaching but absolute `every` wording is not accepted as a guaranteed executable rule. |

### Page 3 — Mid BB

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P3-22a | Mid BB is SMA20. | CORROBORATION | Mathematically consistent with BB20 middle band. |
| P3-22b | Mid-to-Top BB = buying zone. | CORROBORATION / CONTEXT | Primary PDF says price above Mid BB is uptrend context; do not create a buy entry from zone alone. |
| P3-22c | In buying zone, look for buy opportunities. | CONFLICT / HOLD if treated as entry gate | Higher-timeframe owner and BBMA setup requirements remain mandatory; Mid-zone alone cannot authorize entry. |
| P3-22d | Crossing Mid BB from buy zone enters sell zone. | CORROBORATION | Mid BB is directional/support-resistance context. |
| P3-22e | In sell zone, look for sell opportunities. | CONFLICT / HOLD if treated as entry gate | Same guard: zone alone is not an executable setup. |
| P3-22f | Mid BB slope is a guide to current-TF trend. | CORROBORATION | Useful context; D1 strategic authority remains MA50 price-side + slope, not Mid-BB override. |

### Page 4 — MA5 High / Low

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P4-01/04 | MA5 High/Low settings: period 5, LWMA, High/Low, visual colours. | CORROBORATION + NOT STRATEGY-CORE cosmetic | Period/method/price source are Core; colours/thickness are not strategy. |
| P4-05 | Observe MA/candle relation during down move. | CORROBORATION | Primary PDF contains MA arrangement. |
| P4-06 | During decline, candle is below sloping MA5 High. | CORROBORATION | Trend structure context. |
| P4-07 | MA5 Low lies through/above candle body during decline. | CORROBORATION | Broadly matches primary PDF arrangement. |
| P4-08 | BB overlay reveals Momentum as outside-BB close. | CONFLICT / HOLD if outside close alone | Must retain directional/expanding-BB requirement. |
| P4-09 | Close outside MA5 Low while falling is also Momentum. | CONFLICT / HOLD | MA5 close alone is not the canonical M10 Momentum detector. |
| P4-10 | Outside BB + outside MA5 Low + MA5 Low hugging Low BB = very strong Momentum. | NEW RULE / HOLD as strength grading | May be useful confluence teaching, but no canonical numeric/quality gate exists. Do not alter M10 without explicit reconciliation. |

### Page 5 — MA10 High / Candle Arah

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P5-01 | MA10 High settings: period 10, LWMA, High. | CORROBORATION | Canonical indicator contract. |
| P5-02 | During decline MA10 High is far above price. | CORROBORATION | Descriptive context. |
| P5-03 | Price will not rise until it closes above MA10 High. | CONFLICT / HOLD | Pedagogical absolute; not a universal executable law. |
| P5-04 | First close above MA10 = Candle Arah. | CONFLICT / HOLD as exact detector | Current eCSD/CSD requires relevant MA5/MA10 crossing structure, not MA10-only shortcut. |
| P5-05 | Close above MA10 but not Mid BB = weak direction. | CORROBORATION / CLARIFICATION | Consistent with early-direction vs strong CSD distinction, but MA5/MA10 pair remains canonical. |
| P5-06 | Close above Mid BB and MA10 = strong direction. | CORROBORATION / CLARIFICATION | CSD intent requires MA5/MA10 + Mid BB; do not weaken to MA10-only. |

### Page 6 — MA10 Low / MA ordering

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P6-01 | MA10 Low settings: period 10, LWMA, Low. | CORROBORATION | Canonical indicator contract. |
| P6-02 | MA5/10 High/Low arrangement differs in rise vs fall. | CORROBORATION | Primary PDF. |
| P6-03 | During fall candles are below High-side MAs. | CORROBORATION | Primary PDF. |
| P6-04 | During fall MA10 High is above MA5 High. | CORROBORATION | Primary PDF. |
| P6-05 | During fall MA10 Low is above MA5 Low. | CORROBORATION | Primary PDF. |

### Page 7 — MA50

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P7-01 | EMA50 settings: period 50, Exponential, Close. | CORROBORATION | Canonical indicator contract. |
| P7-02 | MA50 shows trend. | ALREADY APPLIED | D1 strategic-owner architecture now implemented on isolated D1 branch. |
| P7-03 | Downtrend: candles below MA50 and Mid BB. | CORROBORATION | Primary PDF supports price-side trend context. |
| P7-04 | MA5/10 lines under MA50 in downtrend. | CORROBORATION / CONTEXT | Not used as separate mandatory D1 gate. |
| P7-05 | MA5/10 cross Mid BB before MA50. | NEW RULE / HOLD | Sequence is descriptive; no universal deterministic owner transition should be inferred without stronger evidence. |

### Page 8 — Signal/setup basics

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P8-01 | MA cannot be outside BB; MA outside BB indicates Extreme. | CORROBORATION | Strict outside-BB Extreme rule retained; touch-only exception excluded. |
| P8-02 | Extreme is a signal, not a setup. | ALREADY APPLIED | Core/Finale and execution architecture agree. |
| P8-03 | Extreme is early indication that movement may be ending. | CORROBORATION | Primary PDF. |
| P8-04a/b | Candle normally should not close outside BB; outside close signals Momentum. | CONFLICT / HOLD if outside close alone | Must include expanding/directional BB context. |
| P8-04c | Momentum marks beginning of market strength. | CORROBORATION | Directional continuation context. |
| P8-05/08 | BB controls/frames movement; Top/Low BB act as continuation/termination boundaries. | CORROBORATION / CONTEXT | Structural teaching, not direct broker-exit formula. |
| P8-09 | Outside-BB close means Momentum continues. | CONFLICT / HOLD if state ignored | Retain M10 canonical state requirements. |
| P8-10 | No outside close = no Momentum. | CORROBORATION | Necessary but not sufficient for any exit decision. |
| P8-11 | No Momentum = market reverses. | CONFLICT / HOLD as universal rule | F7 reconciliation accepts only **post-valid-Re-Entry + structural reversal** lifecycle meaning; not any non-Momentum candle. |
| P8-12 | Mid BB separates rise/fall. | CORROBORATION | Primary PDF trend/SR context. |
| P8-13 | Change confirmed at Mid BB. | CORROBORATION / CONTEXT | CSD uses Mid BB crossing. |
| P8-14 | Break Mid BB, retest, fail to recross -> direction changes. | NEW RULE / HOLD | Potential structure rule, but not yet a canonical standalone transition detector. |

### Page 9 — Extreme lifecycle

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P9-01/02 | Extreme occurs when setup violates BBMA normal condition / MA5 outside BB. | CORROBORATION | Strict outside-BB raw Extreme retained. |
| P9-03a | MA5 outside BB. | ALREADY APPLIED | M08/F2 raw Extreme. |
| P9-03b | Reversal candle required. | ALREADY APPLIED | F2 reversal-confirmed maturity. |
| P9-03c | Retest candle is entry stage. | ALREADY APPLIED at lifecycle/spec level | Standalone Extreme requires retest/entry-ready; standalone execution remains intentionally withheld from active EntryMode. |
| P9-04 | Mark reversal candle body / highest-volume reference. | ALREADY APPLIED via deterministic body-anchor mapping | Project uses candle body, not literal volume indicator. |
| P9-05 | Wait for retest of marked body for entry. | ALREADY APPLIED at F2 lifecycle level | Body/MA5 retest resolution is accepted deterministic mapping. |
| P9-06 | Extreme entry must TP at MA5/MA10, farthest Mid BB. | CORROBORATION / CLARIFIED | Core V2 refines normal first TP-Wajib to opposite MA5/10; Mid BB is farther context. Standalone Extreme is currently non-executable. |

### Page 10 — MHV

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P10-01 | MHV = Market Hilang Volume. | CORROBORATION | MHV/MLV resolved as aliases. |
| P10-02a | MHV candle fails to close beyond relevant outer BB. | ALREADY APPLIED | F1/M09 lifecycle uses no source-valid Momentum continuation. |
| P10-02b | Reversal candle is important to terminate prior move. | ALREADY APPLIED / SOURCE-DERIVED | F1 deterministic formation includes move-away/failed continuation structure. |
| P10-02c | Retest of marked body is entry context. | ALREADY APPLIED at MHV lifecycle level | Frozen marked body/retest implemented; MHV itself remains setup/context, not raw direct-entry authority. |
| P10-02d | MHV occurs after Extreme. | ALREADY APPLIED | Same-TF prior Extreme/TP provenance required. |
| P10-03 | MHV TP is negotiable; next candle outside BB = allow Momentum, inside BB = close because reversal expected. | CORROBORATION + NEEDS CODE FIX / QUALIFICATION | The MHV-specific continuation/failure idea is source-supported, but literal one-candle universal closure must not leak into generic Re-Entry lifecycle. Current M23 does not implement the reconciled lifecycle exit. |
| P10-04 | MHV -> direction -> Re-Entry -> no Momentum => TP mandatory. | CORROBORATION + NEEDS CODE FIX | Accepted F7 lifecycle principle; deterministic source-resolved implementation remains absent in D1-05. |

### Page 11 — Candle direction

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P11-01a | Close past MA5/MA10 = early/weak direction if Mid BB not crossed. | ALREADY APPLIED | eCSD semantics. |
| P11-01b | Close past MA5/MA10 + Mid BB = strong direction. | ALREADY APPLIED | CSD semantics. |
| P11-02 | Marked volume/body + MA5 High retest is a strong entry area. | CORROBORATION | Body/MA5 retest confluence exists in source; avoid quality-score gating. |
| P11-03 | Close below MA5/10 + Mid BB ends prior rise / confirms fall. | CORROBORATION | Strong direction/CSD intent. |
| P11-04 | Strong direction reaches Low BB without Momentum -> do not TP yet. | ALREADY RECONCILED GUARD | Accepted boundary: if expected Re-Entry has not occurred yet, absence of Momentum is not a close trigger; hold/wait for Re-Entry. |
| P11-05 | Strong direction must be followed by Re-Entry. | CORROBORATION | Core cycle. Absolute wording is teaching expectation, not guarantee. |

### Page 12 — Re-Entry, first half

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P12-01 | Re-Entry is additional/second entry after MHV retest entry. | CORROBORATION / CONTEXT | Project treats Re-Entry as principal executable setup; no mandatory lot-layer numbering is encoded. |
| P12-02/03 | Re-Entry candle should not close through MA5/MA10; MA5/10 + Mid BB confluence is strong. | ALREADY APPLIED | M12 close-side conditions and Type 2 confluence. |
| P12-04 | MA5/10 + Mid BB Re-Entry yields minimum 3 candles of movement per TF. | CORROBORATION **ONLY FOR TYPE 2** | Primary PDF explicitly attaches minimum three candles to Powerful Re-Entry/Type 2. Do not universalize to every Re-Entry. |
| P12-05 | Direction/Momentum is followed by Re-Entry. | CORROBORATION | Core lifecycle. |
| P12-06 | MA5/10 + Mid BB Re-Entry merits larger lot. | NOT STRATEGY-CORE | Position sizing preference; no source-owned lot multiplier. |
| P12-07 | Falls lead to sideways; sideways forms Re-Entry. | CORROBORATION | Primary PDF Re-Entry forms after rise/fall and sideways. |
| P12-08 | Understand small-lot vs large-lot entry points. | NOT STRATEGY-CORE | Money-management guidance. |
| P12-09 | When Extreme appears, TP. | CONFLICT / HOLD as universal wording | Normal Extreme TP-Wajib is contextual to prior Extreme position/cycle; not an unconditional command to close every position. |
| P12-10 | Re-Entry close should not pass MA5/MA10. | ALREADY APPLIED | M12 confirmation rule. |
| P12-11 | Wait for defined entry location. | CORROBORATION | Re-Entry/setup discipline. |
| P12-12 | Do not enter on direction candle itself. | ALREADY APPLIED | eCSD/CSD are signals, not direct entry authority. |
| P12-13 | Direction candle is a market-change signal. | ALREADY APPLIED | M10 signal role. |
| P12-14 | Enter at Re-Entry setup. | ALREADY APPLIED | EntryMode design. |
| P12-15 | MA5/MA10/Mid BB confluence gives minimum 3 candles movement. | CORROBORATION ONLY FOR TYPE 2 | Same scope guard as P12-04. |
| P12-16 | This is a large-lot / 3-candle location. | NOT STRATEGY-CORE for lot sizing; CORROBORATION for Type 2 duration | Do not encode lot-size claims. |

### Page 13 — Re-Entry, MTF / destination teaching

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P13-17 | H1 3 candles = 3h; H4 3 candles = 12h. | CORROBORATION | Arithmetic expression of Type 2 duration. |
| P13-18 | H4 Type-2 window should contain lower-TF entries. | NEW RULE / HOLD as mandatory requirement | MTF completion concept is supported, but `must` within that exact window is not part of current exact REM/RRE/REE signatures. |
| P13-19 | Find lower-TF setups aligned with higher-TF direction. | CORROBORATION | Strong MTF principle. |
| P13-20 | Within one H4 candle, seek lower-TF add-on entry. | NEW RULE / HOLD / PERSONAL EXECUTION DETAIL | Not universal Core timing. |
| P13-21 | Within 12h / three H4 candles there must be lower-TF entry setup. | NEW RULE / HOLD | Do not add mandatory timer. |
| P13-22 | H4 sell Momentum -> move to lower TF for sell entry. | CORROBORATION | MTF alignment concept, subject to exact source-owned setup validity. |
| P13-23 | In higher-TF sell, every lower-TF rise is sell. | CONFLICT / HOLD as absolute | Lower-TF retracement still needs valid BBMA setup; `every` retracement cannot authorize entry. |
| P13-24 | D1 sell setup -> lower-TF retracements are sell opportunities. | CORROBORATION with setup guard | Consistent with D1 strategic direction, but lower-TF setup is still mandatory. |
| P13-25 | Re-Entry is the best entry because direction is confirmed. | CORROBORATION / QUALITATIVE | No quality score needed. |
| P13-26 | Follow major trend. | ALREADY APPLIED | D1 strategic owner gate implemented on `d1-owner-dev`. |
| P13-27 | Direction candle destination is Top/Low BB. | CONFLICT / HOLD if used as universal static TP | F7 explicitly rejects universal outer-BB broker TP mapping. Keep as contextual destination teaching only. |
| P13-28 | Retracement direction candle destination is Top BB. | CONFLICT / HOLD as universal static target | Same F7 boundary. |
| P13-29 | Strong direction -> Re-Entry -> outer-BB destination; if no Momentum wait for reverse confirmation/retest. | CORROBORATION / CONTEXT | Lifecycle idea accepted; static target not universal. Exact close trigger already reconciled separately. |
| P13-30 | Retracement dies when direction resumes with major trend. | CORROBORATION | Direction-owner context. |
| P13-31 | Re-Entry must not close past MA5/MA10/Mid BB. | CONFLICT / CLARIFY | Current source contract treats Type 2 Mid-BB confluence distinctly; do not impose Mid-BB close-side condition on all Re-Entry types without exact type context. |
| P13-32 | In downtrend, strong D1 up-direction candle targets Top BB. | CONFLICT / HOLD as universal target | Contextual countertrend destination, not static TP rule. |
| P13-33 | At D1 Top BB, inspect lower TF for continuation/termination setup. | CORROBORATION | MTF analysis principle. |
| P13-34 | MA5/10 + Mid BB confluence gives high-quality entry. | CORROBORATION | Type 2 Powerful Re-Entry. |

### Page 14 — Major trend / advanced MTF Extreme-MHV claims

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P14-35 | Strong direction reaches Low BB before Re-Entry, even without Momentum -> hold because Re-Entry still expected. | ALREADY APPLIED at source-contract level / NEEDS lifecycle code coverage only if tied to open-position management | This guard is accepted in F7 reconciliation. |
| P14-36 | Extreme against major trend is weak. | CORROBORATION / QUALITATIVE | D1 strategic direction now filters new entries; no numeric quality score. |
| P14-37 | Major trend is MA50. | ALREADY APPLIED | D1 strategic owner. |
| P14-38 | Price above MA50 = major-trend Buy. | CORROBORATION **with qualification** | Canonical D1 owner also requires MA50 slope agreement; price-side alone is insufficient during transition. |
| P14-39 | Every MA5/MA10 Low is Re-Entry Buy in major uptrend. | CONFLICT / HOLD as absolute | Re-Entry validity requires proper lifecycle/context and close-side confirmation, not every touch. |
| P14-40/41 | Repeated same-side Extremes without opposite Extreme imply higher-TF structure. | NEW RULE / HOLD | Useful MTF diagnostic, but no canonical deterministic mapping yet. |
| P14-42 | Double H1 Extreme corresponds to H4 MHV. | NEW RULE / HOLD | Not in accepted exact contracts; chart-dependent teaching needs explicit source reconciliation. |
| P14-43 | If higher-TF MHV complete, lower-TF Extreme can be entered immediately without lower-TF MHV. | CONFLICT / HOLD | This resembles advanced MTF Extreme exceptions already excluded from executable Core under CF-04; do not bypass F2 maturity/entry rules. |
| P14-44 | Two H1 sell Extremes imply H4 MHV. | NEW RULE / HOLD | Same as P14-42. |
| P14-45 | Valid H4 MHV means no further H1 MHV. | NEW RULE / HOLD | Not established in higher-precedence canonical rules. |
| P14-46 | MA50 functions best from Daily minimum. | CORROBORATION | Strong support for D1 strategic owner. |
| P14-47 | H4 is not major-trend owner. | ALREADY APPLIED | D1 overrides H4 strategically; H4 remains structural parent. |
| P14-48 | Daily candle owns daily movement. | CORROBORATION | Supports D1 owner timeframe. |
| P14-49 | D1 Buy vs H4 Sell -> follow D1. | ALREADY APPLIED | Central D1 reconciliation; implemented in D1-02/D1-03 chain. |
| P14-50 | D1 sell Momentum means that day's market strength is sell. | CORROBORATION / CONTEXT | Does not replace D1 MA50 owner formula. |
| P14-51 | Today's D1 close determines tomorrow's movement. | CONFLICT / HOLD if literal | Pedagogical directional guidance, not deterministic guarantee. |

### Page 15 — Re-Entry summary notes

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P15-52a | Direction must be followed by Re-Entry. | CORROBORATION | Core cycle expectation. |
| P15-52b | Falls lead to sideways; wait at Mid-BB confluence. | CORROBORATION / CONTEXT | Re-Entry after move/sideways is canonical; Mid-BB confluence corresponds especially to Type 2. |
| P15-52c | Sideways forms Re-Entry. | CORROBORATION | Primary PDF. |
| P15-52d | Direction occurs during Re-Entry formation. | NEW RULE / HOLD as universal ordering | Wording ambiguous; do not change current detector sequencing without stronger context. |

### Page 16 — Momentum / news / timing / Extreme Magic

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P16-01 | Direction -> Re-Entry -> Momentum. | ALREADY APPLIED at Core level | Canonical cycle. |
| P16-02 | Momentum -> another Re-Entry. | ALREADY APPLIED at Core level / NEEDS lifecycle code | F7 re-arm principle accepted; D1-05 position lifecycle does not yet implement WAIT_NEXT_REENTRY/re-arm. |
| P16-03 | Direction -> Re-Entry -> no Momentum -> close; market reverses. | ALREADY ACCEPTED Core principle + NEEDS CODE FIX | F7 accepted semantic lifecycle; current code still uses static TP/MinRR and lacks lifecycle close state. |
| P16-04 | Direction -> no Re-Entry yet -> hold and wait. | ALREADY ACCEPTED guard + NEEDS CODE FIX where lifecycle-managed position is concerned | Must not be replaced with fixed no-Momentum timer. |
| P16-05 | Momentum characteristic: close beyond outer BB. | CONFLICT / HOLD if used alone | Existing directional/expanding BB requirement remains mandatory. |
| P16-06 | Big news creates Momentum. | NOT STRATEGY-CORE | Project governance excludes news filters/rules from trading logic. |
| P16-07 | After Momentum candle closes, next candle may be entry if lower TF aligns. | NEW RULE / HOLD | General MTF teaching; current F6 timing rule applies to Re-Entry validation, not a universal post-Momentum next-candle entry. |
| P16-08 | Can enter every candle during news. | NOT STRATEGY-CORE / REJECT | Not compatible with project strategy governance; no news-driven entry expansion. |
| P16-09 | News aligned with major trend. | NOT STRATEGY-CORE | Context only; no news filter. |
| P16-10 | Daily/Weekly downtrend overrides countertrend news rise. | NOT STRATEGY-CORE | News-specific practice excluded; D1 trend ownership remains independently canonical. |
| P16-11 | If news follows major trend, enter second candle after Momentum. | NOT STRATEGY-CORE / HOLD | News-specific and not universal. |
| P16-12 | Strong H1 Type-2 Re-Entry gives three-candle window; inspect M5 on candles 2/3. | NEW RULE / HOLD for exact M5 timing | General MTF fractal idea is corroborated, but current D1/H4/H1/M15 architecture must not silently add M5 processing. |
| P16-13 | `Extreme Magic`: MA5 and MA10 both outside BB, rare after long sideways. | NEW RULE / HOLD | Variant/terminology not accepted as separate executable Extreme class. |
| P16-14a/b | Re-Entry first candle validates; second candle is entry. | ALREADY APPLIED at static timing semantics | F6 resolves closed validation candle -> immediately following live candle; runtime trace remains evidence task, not source conflict. |
| P16-15 | Direction crossing Mid BB, MA5, MA10 and MA50 is extremely strong. | CORROBORATION / QUALITATIVE | Confluence strength only; D1 strategic authority must not be replaced by lower-TF MA50 crossing score. |

### Page 17 — Summary

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P17-01a-c | Extreme = MA5 outside BB + reversal candle + retest entry. | ALREADY APPLIED at lifecycle/spec level | F2 maturity chain. |
| P17-02 | Extreme is early sign movement may end. | CORROBORATION | Primary PDF. |
| P17-03 | Extreme TP Wajib at MA5/MA10 or Mid BB. | CORROBORATION / CLARIFIED | Opposite MA5/10 is normal first mandatory area; Mid BB farther context. |
| P17-04a-d | MHV: fail outer-BB close, reversal, mark body, retest marked body/MA5 High. | ALREADY APPLIED | F1 MHV lifecycle and frozen-body retest semantics. |
| P17-05 | Early direction = close beyond MA5/10; may revisit Top BB / prior marked area. | ALREADY APPLIED for eCSD; destination part CONTEXT/HOLD | No static target inference. |
| P17-06 | Strong direction = MA5/10 + Mid BB; direction followed by Re-Entry. | ALREADY APPLIED | CSD + cycle. |
| P17-07a | Re-Entry at Mid BB has strong significance. | CORROBORATION | Type 2 context. |
| P17-07b/c | MA5/10 + Mid BB + MA50 is strongest Re-Entry / no compromise. | ALREADY APPLIED for Type 2 confluence semantics | Do not translate qualitative certainty into scoring/guarantee. |
| P17-08 | Momentum = outside-BB close; Momentum followed by Re-Entry. | PARTIAL CONFLICT + ALREADY APPLIED lifecycle | Outside close requires directional/expanding BB; re-entry continuation is accepted. |
| P17-09 | Re-Entry after Momentum. | ALREADY APPLIED at Core level / NEEDS lifecycle code | Re-arm not yet implemented in D1-05. |
| P17-10 | Lower TF forms repeated copy of cycle. | CORROBORATION | MTF/fractal teaching, no arbitrary new TF required. |
| P17-11 | Extreme -> MHV -> direction -> Re-Entry -> Momentum -> Re-Entry is recurring main cycle. | ALREADY APPLIED at Core level | Strongly corroborated by primary PDF/Finale/forum sequence framing. |

### Page 18 — Lifecycle summary / exit behavior

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P18-12 | Extreme -> TP Wajib -> MHV -> direction -> Re-Entry -> Momentum -> Re-Entry. | ALREADY APPLIED at Core level | Canonical sequence. |
| P18-13 | Re-Entry without Momentum leads to rotation. | ALREADY ACCEPTED semantic principle + NEEDS CODE FIX | F7 lifecycle. |
| P18-14 | Momentum leads to another Re-Entry continuation. | ALREADY ACCEPTED + NEEDS CODE FIX | Post-Momentum re-arm lifecycle absent in D1-05. |
| P18-15 | Direction without Re-Entry -> hold until Re-Entry. | ALREADY ACCEPTED guard + NEEDS CODE FIX for lifecycle-managed position state | No fixed timer. |
| P18-16/17 | MHV -> strong direction reaches Low BB before Re-Entry -> do not TP; wait for Re-Entry. | ALREADY ACCEPTED guard | Prevents over-broad `no Momentum => close`. |
| P18-18a | If Momentum appears, wait for Re-Entry. | ALREADY ACCEPTED + NEEDS CODE FIX | Re-arm state absent. |
| P18-18b | If no Momentum, market will rise `100%`. | CONFLICT / REJECT LITERAL GUARANTEE | CF-11: qualitative certainty must never be encoded as guaranteed outcome. |
| P18-19 | Strong direction to Low BB before Re-Entry -> no TP, Re-Entry is still expected. | ALREADY ACCEPTED guard | Same as P18-16/17. |
| P18-20 | After Re-Entry, Momentum is expected. | CORROBORATION | Core lifecycle. |
| P18-21 | At Momentum, wait for Re-Entry again. | ALREADY ACCEPTED + NEEDS CODE FIX | Lifecycle re-arm. |
| P18-22 | MHV -> direction -> Re-Entry -> no Momentum -> TP. | ALREADY ACCEPTED + NEEDS CODE FIX | Direct F7 source basis. |
| P18-23 | Two different outcomes can occur from same MHV setup depending on Momentum. | CORROBORATION | Lifecycle branch semantics. |
| P18-24 | Full cycle repeats from Extreme through further Re-Entry. | ALREADY APPLIED at Core level | Cycle. |
| P18-25 | Sideways forms Re-Entry. | CORROBORATION | Primary PDF. |
| P18-26 | Higher-TF sideways produces lower-TF setup. | CORROBORATION / CONTEXT | MTF principle; not a guaranteed every-candle entry rule. |

### Page 19 — Account / psychology workflow

| ID | Workbook statement | Classification | Reconciliation / project status |
|---|---|---|---|
| P19-27a-k | Example: grow RM/500 account, split accounts, move profit to main account, separate scalping/swing accounts, withdrawal workflow. | NOT STRATEGY-CORE | Personal account/money-management workflow. Must not alter BBMA signal, setup, risk engine or execution contracts. |

## 5. Cross-source findings after all 19 pages

### HC-F01 — Momentum wording is repeatedly over-broad in the Workbook

Workbook pages 2, 4, 8, 16 and 17 often shorten Momentum to `candle close outside BB`.

Higher-precedence reconciliation is already stronger:

`outside outer-BB close + expanding/directional BB = directional Momentum/CSM`

and:

`outside close while BB is flat/horizontal != directional Momentum`.

**Decision:** Workbook shorthand is **CORROBORATING PEDAGOGY WITH REQUIRED QUALIFICATION**, not authority to weaken M10.

### HC-F02 — Extreme lifecycle is strongly and repeatedly corroborated

Pages 8, 9 and 17 independently repeat:

`MA5 outside BB -> reversal confirmation -> retest -> entry context`.

Primary PDF and Finale support the same lifecycle, and F2 already provides deterministic maturity mapping.

**Decision:** **ALREADY APPLIED / NO NEW SEMANTIC FIX REQUIRED.**

### HC-F03 — MHV/MLV provenance, body marking and retest are strongly corroborated

Pages 10 and 17 support:

- after Extreme;
- failed continuation/no valid outside-BB Momentum;
- reversal/move-away structure;
- body marking;
- retest.

This aligns with F1.

**Decision:** **ALREADY APPLIED in current source branch for detector/state semantics.**

### HC-F04 — Re-Entry Type 2 three-candle rule is not universal to every Re-Entry

Workbook wording sometimes sounds universal, but the primary PDF explicitly attaches the three-candle minimum to `Powerful Re-Entry` / Type 2.

**Decision:** retain current Type-2 scope. **Do not add a three-candle minimum to all Re-Entry types.**

### HC-F05 — First validation candle / next live candle entry is already source-resolved

Page 16 repeats first-candle validation / second-candle entry.

F6 already reconciles this to:

`closed source-TF validation candle -> execution may occur during the immediately following live source-TF candle`.

**Decision:** **ALREADY APPLIED statically; runtime timestamp trace remains verification, not a source-rule gap.**

### HC-F06 — D1 / MA50 major-trend hierarchy is strongly corroborated

Pages 14-16 contain the strongest Workbook material:

- MA50 as major trend;
- Daily as minimum strategic owner;
- D1 overrides conflicting H4;
- lower-TF opportunities should align with higher-TF direction.

The primary PDF additionally supplies the MA50-slope requirement, preventing the Workbook's simplified `price above MA50 = Buy` statement from being used alone.

Canonical owner remains:

- BUY: closed D1 `Close1 > MA50_1` and `MA50_1 > MA50_2`;
- SELL: closed D1 `Close1 < MA50_1` and `MA50_1 < MA50_2`;
- otherwise valid disagreement/flat = `D1_TRANSITION`;
- transition/unresolved blocks new strategy entry.

**Decision:** **ALREADY APPLIED on isolated `d1-owner-dev` D1-05 lineage.**

### HC-F07 — Advanced MTF Extreme/MHV shortcuts remain unresolved/excluded

Workbook page 14 claims include:

- repeated H1 Extremes implying H4 MHV;
- completed H4 MHV allowing lower-TF Extreme entry without lower-TF MHV;
- valid H4 MHV suppressing later H1 MHV.

These are not sufficiently established in the primary PDF/Core and overlap with the already excluded advanced-MTF Extreme exception class.

**Decision:** **HOLD / DO NOT IMPLEMENT.**

### HC-F08 — Workbook strongly supports lifecycle-managed Re-Entry positions, not universal static outer-BB TP

Pages 10, 11, 13, 16-18 distinguish:

`Direction -> no Re-Entry yet -> HOLD / wait`

from:

`Valid Re-Entry -> Momentum -> HOLD / later Re-Entry`

and:

`Valid Re-Entry -> no Momentum + reversal/rotation -> TP/CLOSE`.

This is already accepted by F7.

The Workbook also uses Top/Low BB as directional destination teaching, but does not prove the old universal broker mapping:

- H1 RE -> H1 outer BB;
- REM -> H4 outer BB;
- RRE/REE -> D1 outer BB.

**Decision:** lifecycle model is accepted; old universal static TP mapping remains non-Core.

### HC-F09 — Current D1-05 code still conflicts with accepted F7 exit/risk governance

Latest D1-05 source still contains:

- initial TP resolution through `ResolveApprovedBBDestination(...)`;
- a mandatory positive normalized TP in initial SL/TP resolution;
- `MinRRRatio` numeric gate using `tpDistance / slDistance`;
- no post-entry `WAIT_NEXT_REENTRY` / owner-timeframe Re-Entry -> Momentum/no-Momentum lifecycle state in M23.

F7 canonical reconciliation already concluded:

- universal outer-BB TP mapping is not proven Core;
- numeric minimum RR is not established as universal Core for lifecycle-managed Re-Entry positions;
- protective hard SL remains EA_SAFETY;
- lifecycle ownership belongs downstream in M23/M24 once implemented.

**Classification:** **NEEDS CODE FIX — HIGH PRIORITY AFTER THIS SOURCE AUDIT / UNDER NORMAL CHANGE CONTROL.**

### HC-F10 — News, lot-size and account-management statements are intentionally excluded

Workbook news entries, larger-lot claims, account splitting, profit-transfer and withdrawal workflow are not Strategy-Core authority.

**Decision:** **NOT STRATEGY-CORE.** No EA strategy change.

### HC-F11 — No forum-only rule changes the audit result

The retained Forex Factory evidence corroborates sequence/state framing, MTF reasoning and some timeframe-code terminology, but the forum index explicitly finds no forum-only Core rule worth promoting.

**Decision:** forum remains supporting evidence only.

## 6. Required follow-up register

### A. Already closed / no new strategy change required

- BB/MA indicator settings.
- BB flat vs directional semantic distinction.
- canonical expanding/directional Momentum requirement.
- Extreme raw -> reversal-confirmed -> retest lifecycle.
- normal Extreme TP-Wajib interpretation.
- MHV/MLV alias, parent provenance, frozen body and retest.
- eCSD/CSD signal role.
- Re-Entry as actual setup/entry zone.
- Type 2 MA5/10 + Mid BB / MA50 confluence and three-candle minimum.
- first-validation-candle / immediately-following-live-candle timing interpretation.
- D1 strategic owner over H4 structural parent.
- exact REM/RRE/REE signatures remain unchanged.

### B. Source HOLD / do not encode

1. Flat-BB exact `10-20 pip -> big breakout` rule.
2. Any outside-BB close = Momentum without BB-state qualification.
3. MA5-only / MA10-only simplified Momentum or direction detector shortcuts.
4. Mid-BB buying/selling zone as a direct entry trigger.
5. Universal `no Momentum -> reverse` detached from lifecycle stage.
6. Mandatory lower-TF entry within one H4 candle / exactly three H4 candles.
7. `every lower-TF retracement` is automatically an entry.
8. Direction-candle outer BB destination as universal static broker TP.
9. repeated H1 Extreme -> deterministic H4 MHV shortcut.
10. completed H4 MHV -> lower-TF Extreme direct entry shortcut.
11. valid H4 MHV -> no later H1 MHV.
12. `Extreme Magic` as a new executable class.
13. literal `100%`, `pasti`, `no compromise` guarantees.
14. news-driven entry rules.

### C. Accepted Core but latest code still needs repair

1. **F7 lifecycle position management** — owner-timeframe Re-Entry -> Momentum/no-Momentum -> later Re-Entry/re-arm -> final opposite reversal-confirmed Extreme.
2. **Static TP removal/reclassification** — do not present outer-BB static destination as universal Core broker TP for Re-Entry-owned trades.
3. **MinRR gate reconciliation** — current `MinRRRatio` depends on the unproven static reward target and should not remain a universal BBMA Core admission rule once lifecycle-managed TP is implemented.
4. **M22/M23/M24 payload/recovery adjustments** required by the lifecycle model, including targetless/lifecycle-managed positions where appropriate.
5. **D1 Extreme lifecycle support** for D1-owned RRE/REE final-cycle termination, without authorizing standalone D1 Extreme entry.

These were already identified by F7; the full Workbook audit **strengthens rather than overturns** them.

## 7. Coverage statement

This audit reviewed **all 19 pages** of the supplied Workbook.

Coverage rule used:
- every numbered lesson statement was inventoried;
- strategy-relevant sub-items were separately classified;
- purely cosmetic sub-items such as colour/thickness were grouped with their owning indicator-setting row rather than falsely treated as independent trading rules;
- page 19 account-management sub-items were grouped because all are non-Strategy-Core personal workflow.

Therefore the project can now make the narrower evidence-backed claim:

> **100% of the strategy-relevant textual content in the supplied 19-page Workbook has been inventoried and classified against the current source hierarchy.**

This does **not** mean every Workbook sentence was promoted into Core. It means every relevant textual rule was accounted for as accepted/corroborating, unresolved/conflicting, non-Core, or implementation-gap material.

## 8. What is still not proven by this audit

- Tier-A authentication of the Workbook binary.
- Universal validity of Workbook-only advanced MTF shortcuts.
- Exact chart-image-only rules that cannot be reconstructed from the Workbook text alone.
- Universal fixed outer-BB TP for Re-Entry/REM/RRE/REE.
- Universal numeric minimum RR.
- Exact source-owned hard-SL formula.
- News-based entry logic.
- Lot-sizing multipliers from qualitative `lot besar/kecil` teaching.

## 9. Engineering recommendation

Do **not** change Core for every Workbook shorthand.

The next engineering priority exposed by the full audit is still F7 implementation alignment, specifically:

`lifecycle-managed Re-Entry exits + removal of unproven universal static TP/RR assumptions`,

while preserving:

- D1 strategic owner;
- H4 structural parent;
- F1-F6 detector/lifecycle semantics;
- exact REM/RRE/REE signatures;
- existing risk/emergency protections that are explicitly EA_SAFETY rather than mislabelled as BBMA Core.

Any source patch must receive a new unique left-aligned build identifier and native MetaEditor 0E0W before runtime verification.

## 10. Final verdict

**HOME-COURSE FULL 19-PAGE FORENSIC AUDIT: COMPLETE.**

The earlier statement that only high-value Workbook findings had been reconciled is no longer sufficient to describe the evidence work. The project now has a page-by-page inventory covering the full supplied Workbook text.

The audit finds three broad outcomes:

1. **Most foundational BBMA teaching is corroboration of already accepted PDF/Finale/Core semantics.**
2. **A meaningful set of Workbook-only absolutes/advanced MTF shortcuts remains HOLD and must not be encoded.**
3. **The largest accepted-but-unimplemented gap remains F7 lifecycle exit management and the related static-TP / numeric-MinRR assumptions in the current EA.**

No EA source was changed by this forensic audit.