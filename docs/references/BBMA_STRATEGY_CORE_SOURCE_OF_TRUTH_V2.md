# BBMA Strategy Core — Source of Truth V2

## Status
**ACTIVE / AUTHORITATIVE FOR ACCEPTED BBMA STRATEGY-CORE RULES**

This document is the consolidated Strategy Core reference for the project after incorporating the accepted evidence from the two user-supplied PDF references, the BBMA Finale V01–V07 instructional transcript set, and the reconciled high-value findings from the authenticated Tier-B BBMA Home Course Workbook copy.

It is a **derived project specification**, not a claim of authorship or official publication provenance. It does not replace the original source files. Every material rule must remain traceable to the source digest, Finale evidence, or an explicit reconciliation decision that preserves source provenance.

`HOLD`, `UNCERTAIN`, personal workflow, risk-management and EA-management material are intentionally excluded from authoritative Core rules.

---

## 1. Source hierarchy

1. `PROJECT_INSTRUCTIONS.md` governs project scope and change control.
2. `Oma ally BBMA - AL.pdf` remains the **primary operational BBMA reference**.
3. `BBMA technique.pdf` remains the **secondary / historical corroborating reference**.
4. BBMA Finale V01–V07 is **supplemental instructional / clarification evidence**.
5. The 19-page `BBMA Home Course Workbook` copy reviewed under `CORE_V2_F7_WORKBOOK_AUTHENTICATION_AUDIT_20260824.md` is **TIER-B / STRONG-PROVENANCE, PRODUCT-LINKED SUPPLEMENTAL EVIDENCE**. It may strengthen or clarify a rule only through explicit reconciliation and does not outrank the primary PDF or silently become a Tier-A original.
6. `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` is the page-indexed PDF digest plus accepted Finale clarification pointers.
7. `docs/references/video/oma_ally_finale/BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md` governs unresolved Finale conflicts/holds.

No subtitle-only or workbook-only statement may silently weaken an established higher-precedence PDF-derived rule. If evidence conflicts, the conflict must be resolved explicitly before executable Core changes.

---

## 2. Indicator contract

BBMA Strategy Core uses:
- Bollinger Bands: period 20, deviation 2, shift 0, applied to Close.
- MA5 High.
- MA10 High.
- MA5 Low.
- MA10 Low.
- EMA/MA50 as the higher structural/trend/support-resistance reference described by the source.

Source basis: primary PDF page 1.

---

## 3. BBMA cycle

Authoritative operational sequence:

**Extreme → TP Wajib phase → MHV/MLV → direction signal (eCSD/CSD) → Re-Entry → CSM/Momentum → further Re-Entry opportunities → opposite Extreme / cycle restart**.

Rules:
- Extreme is a signal/context stage, not automatic proof of trend reversal.
- MHV/MLV is a setup/context stage.
- eCSD/CSD expresses direction/intent; raw detection is not direct execution authority.
- Re-Entry is the principal entry/setup zone in the taught cycle.
- Momentum/CSM may continue the move and create later Re-Entry opportunities.

Source basis: primary PDF page 2; Finale corroboration V01 00:57:06–00:59:17, V05 00:42:04–00:43:04, V06 00:06:09–00:08:49.

---

## 4. Bollinger Band state and Momentum / CSM

Authoritative rule:
- A close outside the relevant outer Bollinger Band is not sufficient by itself to classify directional momentum.
- Momentum/CSM context requires the outside close together with an expanding/directional Bollinger Band state.
- A close outside the outer BB while the BB is flat/horizontal is **not** treated as directional momentum under the accepted Core interpretation.

This is a corroborated rule, not a new post-Finale filter.

Source basis: historical PDF basic BBMA laws; Finale V02 00:13:51–00:18:07 and 00:24:44–00:26:18.
### 4.1 Mid-BB descriptive zones and slope context — non-executable clarification

Home Course terminology retained for completeness:
- area from Mid BB toward Top BB = `Buying Zone`;
- area from Mid BB toward Low BB = `Selling Zone`;
- Mid-BB slope up/down/horizontal is a same-timeframe descriptive trend guide.

Execution guard:
- zone membership is context only and is **not** standalone entry authority;
- Mid-BB slope alone is **not** a detector, entry filter, exit rule, TP/SL rule or timeframe-owner override;
- accepted eCSD/CSD, Re-Entry, Extreme, MHV/MLV, Momentum and exact REM/RRE/REE contracts remain unchanged.

Source/reconciliation basis: Home Course 19-page rows HC-P03-002 through HC-P03-007, constrained by `HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`.


---

## 5. Extreme

### 5.1 Normal Extreme lifecycle
Accepted normal/basic lifecycle:
1. Relevant MA5 or MA5/MA10 is outside the appropriate outer BB under the established strict Core detector rule.
2. A reversal-candle confirmation is required for the Extreme context.
3. Standalone Extreme entry is associated with a later retest; raw condition 1 alone is not entry authority.
4. Finale clarifies that the retest may span more than one candle.
5. A later outside-BB close / momentum context can void the Extreme context according to the source rules.

Source basis: primary PDF pages 5–6; Finale V04 00:27:23–00:31:55 and 00:37:27–00:40:53; V05 00:07:05–00:08:22.

### 5.2 Normal Extreme TP Wajib
Accepted clarification:
- Extreme SELL: the opposite MA5/MA10 Low area is the normal first TP-Wajib area.
- Extreme BUY: the opposite MA5/MA10 High area is the normal first TP-Wajib area.
- Mid BB is a farther/maximum context rather than replacing the opposite MA5/MA10 area as the normal first mandatory objective.

This refines the earlier broad digest wording “MA5/MA10 or Mid BB” without changing the overall Extreme cycle.

Source basis: primary PDF page 2 plus Finale V04 00:41:02–00:42:42 and V05 00:16:41–00:18:02.

### 5.3 Extreme edge-case closure
The former broad HOLD is closed by the 2026-08-26 source/forum/web reconciliation:
- **MA5 merely touching the outer BB is not equivalent to canonical Extreme.** The established Extreme condition requires the relevant MA extension outside the band. Touch/equality may be context only and cannot create Extreme/TP-Wajib/execution authority.
- **A reversal-direction candle that remains closed outside the relevant outer BB is not a universal valid-Extreme shortcut merely because it is inside MA5.** Accepted outside-close/Momentum invalidation retains precedence over maturity promotion.
- **Advanced repeated-Extreme behavior is a bounded MTF exception, not a blanket no-TP rule.** Later same-direction LTF Extremes may omit a fresh local TPW/local MHV cycle only when no opposite LTF Extreme intervenes and the immediate HTF independently owns a valid mature MHV/MLV or Re-Entry compatible with the sequence. The HTF state must be proven by its own owner; RAW LTF Extreme maturity cannot be bypassed.
- The bounded repeated-LTF exception does **not** apply to the current D1 `EXTREME_TPW` path because D1 is the top approved owner in the EA hierarchy and has no independently validated larger parent.

Authority:
- `blueprint/decisions/CORE_V2_RESIDUAL_HOLD_CLOSURE_DECISION_20260826.md`;
- `blueprint/decisions/ADVANCED_REPEATED_EXTREME_TPW_EXCEPTION_DECISION_20260826.md`.

### 5.4 Extreme maturity and deterministic reversal/retest lifecycle
**User-approved project Core decision:** an Extreme used as a component of executable REM/REE must be at least **reversal-confirmed**, while a standalone Extreme entry requires the later **retest/entry-ready** stage.

Maturity distinction:
- `RAW EXTREME` = strict MA5/MA10-outside-BB condition only. Not sufficient for executable REM/REE.
- `REVERSAL-CONFIRMED EXTREME` = raw Extreme plus accepted reversal confirmation. Eligible as an Extreme component of REM/REE.
- `RETEST/ENTRY-READY EXTREME` = reversal-confirmed Extreme plus the later accepted retest. Required for standalone Extreme entry eligibility.

Accepted deterministic mapping:
- reversal confirmation is evaluated on closed candles on the same source timeframe;
- SELL Extreme reversal direction: `Close < Open`;
- BUY Extreme reversal direction: `Close > Open`;
- the first qualifying closed reversal-direction candle promotes `RAW EXTREME -> REVERSAL-CONFIRMED`, provided accepted outside-BB/Momentum invalidation has not already voided the candidate;
- no mandatory previous-candle colour flip, named candlestick pattern, fixed two-/three-candle minimum, eCSD/CSD prerequisite, or universal close-back-inside-BB requirement is added;
- later same-direction candles may continue the reversal phase without delaying basic reversal-confirmed maturity;
- while the reversal phase continues, the provisional body reference may update; once retest starts, it freezes and must not drift;
- retest begins on the first later closed candle whose close moves back toward the original Extreme/reference relative to the previous close: SELL `CurrentClose > PreviousClose`; BUY `CurrentClose < PreviousClose`;
- the retest-start candle is the first retest-phase candle and is excluded from the completed reversal-phase anchor;
- for each reversal-phase candle, `BodyTop = max(Open,Close)` and `BodyBottom = min(Open,Close)`;
- frozen SELL body anchor = highest `BodyTop` across the completed reversal phase;
- frozen BUY body anchor = lowest `BodyBottom` across the completed reversal phase;
- wick `High/Low` is not the numeric body-anchor definition;
- relevant MA5 remains a source-supported alternate/confluent retest reference;
- standalone retest is completed by a valid price-range/wick interaction with the frozen body anchor **or** the relevant MA5 area; a universal additional close-side confirmation or named reversal pattern is not required;
- when body anchor and MA5 are separated, the **first valid interaction with either** completes the retest; there is no body-first/MA5-first hierarchy and no mandatory dual-touch;
- accepted outside-BB/Momentum invalidation has higher priority than maturity promotion or retest completion and results in `VOID`.

Consolidated lifecycle:

`RAW EXTREME -> FIRST QUALIFYING REVERSAL-DIRECTION CLOSED CANDLE -> REVERSAL-CONFIRMED -> OPTIONAL REVERSAL CONTINUATION -> RETEST START / ANCHOR FREEZE -> FIRST VALID BODY-ANCHOR OR MA5 INTERACTION -> RETEST/ENTRY-READY`

Evidence classification:
- REM/REE component maturity = **SOURCE-INFERRED / STRONG HINT**;
- reversal-candle requirement and body/MA5 retest concepts = **DIRECT SOURCE / SOURCE-DERIVED**;
- exact Boolean direction, close-progression phase trigger, numeric candle-body edge, range-touch, and first-valid-reference rules = **MINIMAL DETERMINISTIC PROJECT MAPPING**, not verbatim Oma Ally formulas.

Reasoning basis:
- V04 separates raw Extreme, reversal confirmation and retest, and ties the retest to standalone Extreme entry;
- V04 permits retest to revisit a marked body/reference or relevant MA5 and gives outside-BB/Momentum behavior priority as invalidation;
- V05 teaches lower-timeframe Extreme/MHV/direction structures as supporting completion for higher-timeframe Re-Entry, supporting a distinction between MTF component maturity and standalone entry maturity.

Decision provenance: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`.

Implementation guard: implementation must reproduce this approved lifecycle without inventing arbitrary candle counts, named patterns, EMA/ATR/RSI filters, moving anchors, mandatory body+MA5 dual-touch, or an unsupported body-vs-MA5 priority hierarchy.

---

## 6. MHV / MLV

### 6.1 Terminology and role
`MHV` (Market Hilang Volume) and `MLV` are treated as source-terminology aliases for the same loss-of-volume setup family unless future source evidence explicitly distinguishes them.

Do not create two separate Strategy-Core setup types merely because the source documents use different abbreviations.

MHV/MLV remains a **setup/context structure**, not standalone direct execution authority.

### 6.2 Parent provenance and eligibility
Canonical MHV/MLV requires a prior source-valid Extreme in the **same source timeframe / owner-cycle**.

Accepted parent chain:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> NORMAL TP-WAJIB STRUCTURALLY COMPLETED -> ELIGIBLE MHV/MLV PARENT CONTEXT`

Rules:
- RAW Extreme alone is insufficient;
- the prior Extreme does not have to reach standalone `RETEST/ENTRY-READY` merely to provide MHV cycle provenance;
- normal TP-Wajib structural completion must actually occur before canonical MHV formation begins;
- prior Extreme SELL -> opposite MA5/MA10 Low area;
- prior Extreme BUY -> opposite MA5/MA10 High area;
- Mid BB remains farther/maximum context rather than the canonical first TP prerequisite;
- TP-Wajib completion is market-structure evidence, not broker/order status;
- the bounded repeated-LTF/valid-HTF exception does not manufacture a fresh same-timeframe MHV parent and does not weaken this canonical same-TF MHV provenance rule;
- a generic consolidation, local double/triple top/bottom or loss of impulse without a provable prior Extreme chain is not canonical MHV/MLV.

### 6.3 Loss-of-momentum state and concrete formation
After eligible parent context, `LOSS OF PRIOR MOMENTUM` is interpreted as a **developing post-TP structural failed-continuation state inside the relevant outer BB without source-valid Momentum/CSM continuation**.

Rules:
- one ordinary/non-Momentum candle is insufficient;
- absence of Momentum/CSM is necessary but not sufficient; a same-cycle post-TP structure must actually develop;
- `BB_FLAT`, ATR, ADX, fixed pip displacement, fixed body-size thresholds and fixed 2/3-candle minimums are not canonical proof.

Concrete deterministic formation mapping:
- prior Extreme SELL / bottom-side MHV:
  - `BodyBottom = min(Open,Close)`;
  - track the lowest `BodyBottom` across the active loss-of-momentum phase;
  - first later closed candle with `CurrentClose > PreviousClose` establishes MHV/MLV formation;
- prior Extreme BUY / top-side MHV:
  - `BodyTop = max(Open,Close)`;
  - track the highest `BodyTop` across the active loss-of-momentum phase;
  - first later closed candle with `CurrentClose < PreviousClose` establishes MHV/MLV formation;
- the move-away trigger candle is excluded from the accumulated body-extreme reference;
- wick `High/Low` is not substituted for the source-described marked body;
- no mandatory second touch, exact double/triple morphology, H&S, named candlestick pattern, eCSD/CSD, breakout or fixed candle count is required merely to establish initial formation.

### 6.4 Frozen marked body and retest
The marked body **freezes immediately when formation is established**.

Frozen reference:
- bottom-side MHV = lowest `BodyBottom` accumulated through the candle immediately before the move-away trigger;
- top-side MHV = highest `BodyTop` accumulated through the candle immediately before the move-away trigger.

Later candles cannot drag/recalculate the frozen reference merely because a new body extreme appears.

Retest completion:
- bottom-side MHV: a later source-timeframe candle with `Low <= FrozenMarkedBody`;
- top-side MHV: a later source-timeframe candle with `High >= FrozenMarkedBody`.

Price-range/wick interaction is sufficient for the project deterministic retest mapping. No universal body-close-at-line, extra close-away confirmation, named reversal pattern, mandatory double/triple touch or eCSD/CSD prerequisite is added merely to complete retest.

The formation-establishing move-away candle cannot simultaneously count as the later retest candle.

`RETEST COMPLETE / ACTIVE MHV SETUP` remains setup/context maturity only and does not become standalone direct entry authority.

### 6.5 M15 MHV/MLV maturity inside REM
The exact REM signature remains:

`H4 Re-Entry + H1 Extreme + M15 MHV/MLV`

Minimum M15 MHV/MLV maturity for REM is:

`MHV/MLV FORMATION ESTABLISHED + FROZEN MARKED BODY`

Rules:
- eligible parent context, pending loss-of-momentum or unfrozen provisional formation is insufficient;
- later MHV `RETEST COMPLETE` is **not mandatory merely to satisfy the REM component**;
- no eCSD/CSD, second retest, double/triple morphology, fixed wait or broker execution event is added as an extra REM requirement;
- a void/superseded M15 MHV/MLV cannot satisfy REM.

This is a **SOURCE-INFERRED COMPONENT-MATURITY MAPPING** over the PDF-explicit REM signature.

### 6.6 Stage-bounded invalidation and same-cycle progression
While MHV/MLV is still the pending/current authoritative stage, source-valid outside-outer-BB close / Momentum/CSM can void the MHV interpretation.

Rules:
- invalidation has priority if the same candle/structure also satisfies a competing MHV promotion/retest event;
- source-valid same-cycle `eCSD` or `CSD` is the normal next direction stage and does **not** retroactively void an already-completed MHV/MLV;
- once valid same-cycle eCSD/CSD structurally takes direction ownership, the active MHV invalidation window closes;
- later same-cycle Re-Entry and CSM/Momentum are normal cycle progression and cannot retroactively convert completed MHV provenance into `VOID`;
- distinguish **current active stage ownership** from **completed structural provenance**: direction may become active while completed MHV/MLV remains immutable same-cycle history;
- the frozen marked body remains frozen;
- no fixed candle/session/day expiry or generic “new signal erases old setup” rule is added.

Canonical stage progression:

`MHV PENDING / FORMATION / ACTIVE MHV -> SAME-CYCLE eCSD/CSD DIRECTION TAKEOVER -> RE-ENTRY -> SAME-CYCLE CSM/MOMENTUM`

### 6.7 New-cycle supersession
An opposite `RAW EXTREME` is a **new-cycle candidate only**. It does not by itself erase the current cycle or completed MHV provenance.

The old cycle is atomically superseded when the opposite Extreme reaches the F2 minimum maturity:

`OPPOSITE REVERSAL-CONFIRMED EXTREME`

At that closed-candle transition:
- old-cycle MHV/MLV provenance and its frozen marked-body reference become historical-only;
- they can no longer satisfy new REM construction, current-cycle validation, inherited setup authority or future MHV retest authority;
- superseded provenance may remain in diagnostics/history;
- standalone opposite Extreme `RETEST/ENTRY-READY` maturity is not required merely for the cycle boundary;
- if the opposite RAW Extreme becomes VOID before reversal confirmation, the old cycle is not superseded by that failed candidate;
- opposite eCSD/CSD alone does not replace this explicit F1 cycle-restart event;
- no fixed candle count, timer, session/day reset or generic age expiry is used.

Canonical lifecycle:

`REVERSAL-CONFIRMED PRIOR EXTREME -> TP-WAJIB COMPLETE -> LOSS OF PRIOR MOMENTUM -> MOST-EXTREME BODY -> FIRST CLOSED MOVE AWAY -> MHV/MLV FORMATION + FROZEN BODY -> OPTIONAL RETEST -> SAME-CYCLE DIRECTION -> RE-ENTRY / CSM CONTINUATION -> OPPOSITE RAW EXTREME CANDIDATE -> OPPOSITE REVERSAL-CONFIRMED EXTREME -> ATOMIC OLD-CYCLE SUPERSESSION`

### 6.8 Morphology and evidence classification
- Double/triple top or bottom morphology is supported.
- H&S-like morphology shown in Finale is an example, not a mandatory condition.
- Highest/lowest body marking and retest are source-supported structural concepts.
- Exact software states, body-edge formulas, close-to-close turning predicate, immediate freeze, range-touch retest, REM component threshold, stage-bounded invalidation and atomic cycle supersession are **project deterministic mappings**, not verbatim Oma Ally Boolean formulas.

Source basis: primary PDF pages 2 and 7–8; historical PDF pages 31–34; primary PDF pages 12–13 for REM; Finale V05 00:18:07–00:28:12, OA-F-V05-006 to OA-F-V05-019, and V01 00:59:18–01:00:05.

Decision provenance: `blueprint/decisions/CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md`.

Implementation guard: M09 must ultimately use one canonical lifecycle/owner result. Independent legacy `DetectMHV()`/MLV semantics, synthetic fixed-point necklines, moving anchors, fixed-N expiry and generic consolidation heuristics must not override this resolved contract.

---

## 7. Direction signal — eCSD / CSD

### 7.1 eCSD / early direction
Relevant MA5/MA10 pair is crossed without the stronger Mid-BB cross.

### 7.2 CSD / stronger direction
Relevant MA5/MA10 pair and Mid BB are crossed.

### 7.3 Execution meaning
- eCSD/CSD expresses direction/intent.
- Raw direction-candle detection is not direct entry authority.
- The normal cycle waits for the applicable Re-Entry structure.

Source basis: primary PDF pages 7–8; Finale V05 00:28:41–00:36:51 and V06 00:17:07–00:20:18.

---

## 8. Re-Entry

### 8.1 General role
- Re-Entry follows a valid directional/momentum context and is the actual setup/entry zone in the normal taught cycle.
- MA5 is the principal retest area; MA10 confluence strengthens the structure.
- A Re-Entry candle may penetrate MA5, but the accepted structure does not allow a close that clears through the relevant MA5/MA10 cluster against the intended setup direction.

Finale mainly corroborates the existing close-side validity already present in the project contracts.

Source basis: primary PDF pages 9–10; Finale V05 00:37:25–00:41:16.

### 8.2 Type 1
Accepted source/project interpretation:
- Re-Entry Type 1 forms after a prior rise/fall followed by a sideways/ranging phase.
- Type 1 must not be reduced to an arbitrary MA5/MA10 touch alone.
- The project interprets the ranging phase structurally: prior directional movement has occurred, active momentum has paused/ended, price consolidates/retraces rather than continuing impulsively, and the relevant MA5/MA10 cluster begins acting as support/resistance.
- `BB_FLAT`/horizontal BB may support the ranging interpretation but is not by itself a universal mandatory Type 1 condition.
- There is **no fixed minimum candle count** for Type 1 ranging. Structural completion, not an invented 2-candle/3-candle threshold, governs maturity.
- A qualifying prior rise/fall must be evidenced by a source-valid BBMA direction/momentum state (`eCSD`, `CSD`, or `CSM/Momentum`) under its own source contract; generic EMA/ATR/pip displacement is not a substitute.
- Transition into Type 1 ranging is owner/state based: prior valid direction/momentum → active momentum ceases/pauses → retrace/consolidation toward the relevant MA5/MA10 cluster. One non-CSM candle by itself is insufficient proof of ranging.
- SELL context: MA5/10 High acts as resistance; sell Re-Entry is considered when price finds the relevant cluster and the validating candle remains/closes on the permitted SELL side.
- BUY context: MA5/10 Low acts as support; buy Re-Entry is considered when price finds the relevant cluster and the validating candle remains/closes on the permitted BUY side.
- A pending Type 1 is structurally invalidated/reset/reclassified when the relevant MA5/MA10 close-side fails, same-direction Momentum/CSM resumes and ends the old ranging phase, opposite source-valid direction/momentum supersedes the old context, or an exact Type 3/Type 4 structure becomes the correct setup owner.
- Type 1 owner lifetime is **structural, not timer-based**. There is no generic fixed candle expiry; owner age may be logged but does not determine validity.
- Exact Type 3 (`CSM -> MA5/MA50 retrace`) and Type 4 (`CSD -> MA5/10 retrace`) structures retain their own ownership and must not be relabelled as generic Type 1.

Source basis: primary PDF page 9; Finale supporting context V01/V02/V03/V05/V06. The structural-ranging, prior-owner, transition and invalidation interpretations are **SOURCE-INFERRED / STRONG HINT** around the PDF-explicit rise/fall + sideways/ranging requirement. The no-fixed-candle/no-fixed-expiry rules are source-faithful project specifications because the source provides no universal numeric Type 1 threshold.

Decision provenance: `blueprint/decisions/CORE_V2_F3_TYPE1_CONTEXT_DECISION.md`.

Implementation guard: the Type 1 strategy specification is resolved, but M12 still requires implementation/audit against the approved owner/state contract. Do not introduce RSI/ADX/ATR/fixed-pip/timer heuristics as disguised Core rules.

### 8.3 Type 2 — Powerful Re-Entry
- MA5/MA10 and Mid BB meet/collide.
- MA50 confluence strengthens the setup further.
- Minimum duration: three candles on the relevant timeframe.

Source basis: primary PDF page 10; Finale V06 00:20:20–00:22:13 and 00:32:41–00:33:31.

### 8.4 Type 3 — CSM Re-Entry
- CSM forms first.
- Price then reverses/retraces toward MA5 or MA50 for the Re-Entry setup.

Source basis: primary PDF page 10.

### 8.5 Type 4 — CSD Re-Entry
- CSD forms first.
- Price then gyrates/retraces toward MA5/MA10.
- Direction follows the relevant MA5/MA10 High/Low context described by the source.

Source basis: primary PDF page 10.

### 8.6 Validation-candle / immediately-following live-candle timing
The teaching phrase “first Re-Entry candle validates; second candle is entry” is now **closed at semantic/project-mapping level**.

Canonical mapping:
- the source-timeframe Re-Entry validation candle must be fully closed;
- after that closed candle confirms the Re-Entry, execution may become eligible during the **immediately following live source-timeframe candle**, subject to the normal M15/final-authority and downstream validation gates;
- no extra full source-timeframe candle must close merely to reinterpret the teaching phrase;
- `EntryCandle` observability metadata refers to the immediately following source-TF candle and must not duplicate `ConfirmationCandle`.

This is consistent with `CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md`. Remaining broker `OrderOpenTime()` traces are runtime evidence, not a Strategy-Core semantic HOLD.

Evidence classification:
- first-validating / next-entry-candle teaching = **SOURCE-SUPPORTED**;
- exact closed-candle autonomous-EA timing = **PROJECT DETERMINISTIC MAPPING / ENGINEERING**.

---

## 9. Multi-timeframe relationship and strategic hierarchy

Accepted Core interpretation:
- BBMA must be read across related timeframes.
- A higher-timeframe Re-Entry may be completed/read through lower-timeframe signal/setup structures.
- An opposite-looking lower-timeframe direction signal must not automatically be treated as an independent reversal when it is structurally part of the higher-timeframe Re-Entry context.
- The structural principle scales across related chains such as D1/H4/H1, H4/H1/M15, H1/M15/M5 and M15/M5/M1, but project execution contracts use only explicitly approved timeframe signatures.

Canonical project hierarchy after Home Course reconciliation:

`D1 MAJOR-TREND STRATEGIC OWNER -> H4 STRUCTURAL/SETUP PARENT -> H1 SIGNAL/RE-ENTRY -> M15 FINE/ADDITIONAL EXECUTION STRUCTURE`

Source basis: primary PDF page 1, page 10 and pages 12–13; Finale V05 00:34:48–00:36:37 and 00:46:16–00:53:55; V06 00:26:57–00:29:02; reconciled Home Course D1/MA50 evidence.

### 9.1 D1 major-trend strategic owner
D1 is the strategic major-trend authority for new-entry direction.

The accepted deterministic owner uses only fully closed D1 data:
- BUY confirmed when `Close1 > MA50_1` **and** `MA50_1 > MA50_2`;
- SELL confirmed when `Close1 < MA50_1` **and** `MA50_1 < MA50_2`.

Where:
- `Close1` = latest fully closed D1 close;
- `MA50_1` = MA50 on that same closed D1 candle;
- `MA50_2` = MA50 on the immediately previous fully closed D1 candle.

Evidence classification:
- D1/MA50 major-trend authority = **DIRECT SOURCE / STRONGLY CORROBORATED**;
- the source wording “price above + MA50 ascending” / “price below + MA50 descending” = **DIRECT PRIMARY-PDF DESCRIPTIVE TREND RULE**;
- the immediate adjacent-bar slope comparison `MA50_1` versus `MA50_2` = **PROJECT ENGINEERING MAPPING**.

For the accepted EMA50 applied to Close, the immediate slope comparison is algebraically coupled to the same-bar price side for every non-equality observation. Therefore the two conjuncts above are not independent market conditions. The existing M11 conjunction may remain as a source-facing deterministic expression, but it must not be interpreted as creating an independently observable non-equality transition zone.

Decision provenance:
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`;
- `blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- `blueprint/decisions/R3_03_D1_TRANSITION_REACHABILITY_RECONCILIATION_20260923.md`;
- `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`.

### 9.2 D1 transition / unresolved state
The software state `D1_TRANSITION` remains a fail-closed project state for otherwise-valid closed-D1 inputs that are neither confirmed BUY nor confirmed SELL.

Under the current **EMA50 / PRICE_CLOSE / immediate adjacent-bar** mapping:
- `Close1 > MA50_1` implies `MA50_1 > MA50_2`;
- `Close1 < MA50_1` implies `MA50_1 < MA50_2`;
- therefore “close above MA50 while immediate EMA50 falls” and “close below MA50 while immediate EMA50 rises” are not reachable non-equality states;
- a naturally reachable valid `D1_TRANSITION` is limited to equality/flat degeneracy permitted by exact input arithmetic and may be absent in finite broker history.

If the required closed-D1/MA50 history is missing or invalid, state = `D1_OWNER_UNRESOLVED`.

Execution meaning is unchanged:
- `D1_TRANSITION` -> **block all new strategy entries**;
- `D1_OWNER_UNRESOLVED` -> **block all new strategy entries**;
- the last confirmed D1 direction may remain historical/diagnostic only and does not stay active as new-entry authority.

No fixed two-/three-day confirmation, alternate MA type, longer slope lookback, ATR/pip buffer, score, RSI/ADX, session, news or timer is introduced merely to manufacture a wider transition state.

The explicit transition/unresolved software state and fail-closed blocking are **MINIMAL DETERMINISTIC PROJECT MAPPINGS**, not claimed as verbatim Oma Ally software instructions. R3-03 validation may prove transition safety **deterministically by construction**; natural observation of a mathematically unreachable non-equality transition is not required.

`D1_TRANSITION` is not by itself a live-position broker-close rule.

### 9.3 Standalone H1 Re-Entry H4 parent contract
Standalone H1 Re-Entry uses **H4 as the immediate structural/setup parent**, but H4 is subordinate to D1 strategic direction.

Accepted contract:
- H1 standalone Re-Entry cannot be autonomous from H4 BBMA context;
- H4 compatibility is based on an active authoritative BBMA directional/cycle owner, not one H4 candle, H4 MA50-only reading, Mid-BB-only reading, score or generic trend filter;
- raw H4 Extreme/MHV are pre-direction context and do not establish H4 directional ownership;
- H4 directional ownership is inherited across a same-direction cycle: valid direction signal establishes/advances owner; same-direction Re-Entry and CSM/Momentum inherit/continue it;
- valid H4 eCSD is sufficient to establish H4 directional ownership for parent compatibility;
- opposite valid H4 eCSD/CSD/CSM causes atomic H4 owner handover;
- simultaneous H4 BUY and SELL owners are not allowed;
- neutral H4 candles do not erase a surviving owner;
- true H4 `NO_OWNER` blocks standalone H1 Re-Entry;
- H4 owner lifetime is structural with no generic time/candle/session expiry;
- D1 cannot substitute for missing H4 ownership, and H4 cannot override an opposite/transition/unresolved D1 owner.

Therefore final standalone H1 higher-timeframe alignment requires **both**:
1. confirmed same-direction D1 strategic owner; and
2. active same-direction H4 structural owner.

Evidence classification: H4 MTF/owner semantics remain **DIRECT SOURCE PRINCIPLE + SOURCE-INFERRED / STRONG HINT**, while D1 strategic authority is governed by Sections 9.1–9.2.

Decision provenance: reconciled `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`.

### 9.4 Restart/recovery preservation
H4 owner restart/recovery remains **EA ENGINEERING POLICY**:
- verified checkpoint/cache only;
- deterministic chronological closed-H4 replay;
- insufficient provenance -> `NO_OWNER` and block standalone H1 execution.

D1 current strategic state does not require a persisted owner checkpoint merely for safe new-entry gating. It can be rebuilt from the latest two closed D1 MA50 observations plus the latest closed D1 close. Missing/invalid inputs -> `D1_OWNER_UNRESOLVED` -> block new entries.

Neither H4 nor D1 recovery may invent direction from a current candle snapshot or unsupported fallback.

---

## 10. REM / RRE / REE exact signatures and D1 strategic gate

The authoritative project signatures remain PDF-derived and unchanged:
- **REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV**.
- **RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme**.
- **REE = D1 Re-Entry + H4 Extreme + H1 Extreme**.

All three components must be interpreted consistently with their own source-defined validity and direction contracts. Finale corroborates the higher-to-lower timeframe principle but does not redefine these signatures.

Additional maturity rules remain:
- every Extreme component in executable REM/REE must be at least reversal-confirmed;
- retest/standalone-entry readiness is not required merely because the Extreme serves as an MTF combination component;
- M15 MHV/MLV inside REM must be at least `FORMATION ESTABLISHED + FROZEN MARKED BODY`;
- M15 MHV/MLV retest completion is not mandatory merely to satisfy REM;
- void/superseded old-cycle MHV/MLV cannot satisfy a current REM decision.

### D1 strategic gate does not alter signatures
D1 major trend is a **separate final new-entry strategic-direction gate**:
- REM does not acquire a fourth D1 component;
- RRE/REE D1 Re-Entry components remain setup/component identity, not substitutes for D1 MA50 strategic-owner confirmation;
- a structurally valid REM/RRE/REE may remain observable while non-executable if D1 owner is opposite, `D1_TRANSITION`, or `D1_OWNER_UNRESOLVED`;
- final executable direction must agree with a confirmed M11 D1 strategic owner.

Source basis: primary PDF pages 1 and 12–13; Finale corroboration; Home Course D1/MA50 reconciliation; F1/F2 component-maturity decisions.

---

## 11. Material explicitly excluded from universal Strategy Core

Do not promote the following into BBMA Strategy Core without stronger source evidence and explicit project approval:
- personal H4-only workflow/preference;
- sample win-rate statistics;
- personal risk %, leverage, lot sizing or portfolio/account-management rules;
- personal MA10 + allowance stop methodology as a universal BBMA SL rule;
- psychology/money-management teaching;
- literal guarantees from qualitative phrases such as “pasti”, “100%” or “paling selamat”;
- EA implementation mechanisms such as trade lock, scheduler, dashboard, logging, broker handling, portfolio cap or execution plumbing.
### 11.1 Home Course / 49-family completeness boundary — fully classified

The historical 2026-08-25 revalidation recorded `28 COVERED + 10 PARTIAL/mixed + 11 MISSING/HOLD`. Subsequent dated source decisions supersede that count as the current gap status.

Current authority:
- `docs/references/BBMA_CORE_49_FAMILY_CLOSURE_REBASELINE_20260826.md`;
- `blueprint/decisions/CORE_REMAINING_GAPS_CLOSURE_DECISION_20260826.md`;
- `blueprint/decisions/CORE_V2_RESIDUAL_HOLD_CLOSURE_DECISION_20260826.md`;
- `blueprint/decisions/ADVANCED_REPEATED_EXTREME_TPW_EXCEPTION_DECISION_20260826.md`.

Current result: **49/49 Home Course families explicitly classified and 0 unresolved Core semantic HOLDs.**

“Closed” does not mean “directly executable.” Each former non-full family now terminates in one explicit category:
- accepted Core;
- accepted bounded/source-consistent context only;
- bounded advanced MTF interpretation;
- deterministic project/engineering mapping with provenance label;
- or rejected from current universal Core.

Important bounded outcomes:
- horizontal-BB rejection/compression, zones, Mid-BB slope and MA5-strength wording remain context/annotation unless an existing canonical setup owns execution;
- C018 Mid-BB break/retest/failure-to-recross is direction-confirmation context, not a standalone CSD detector;
- C024 MHV Momentum/no-Momentum behavior is a lifecycle principle, without inventing a new MHV direct-entry path;
- C034 Candle Arah Top/Low-BB destination is structural context, not a guaranteed universal resting broker TP;
- C035 pre-Re-Entry outer-BB hold is bounded to the pre-ReEntry stage;
- C038 D1 precedence is scoped strategic ownership, not an unconditional raw D1-vs-H4 shortcut;
- C039/C040/C041 repeated-Extreme/HTF-MHV relationships are bounded nested context and never manufacture HTF confirmation or suppress genuine LTF detectors;
- C042 prior-day D1 is strategic prior/context, not deterministic next-day prediction;
- C044 post-Re-Entry failed-Momentum is accepted as lifecycle source principle, while its exact automated outer-test/latch/recovery machinery is labelled project mapping and remains feature-gated pending broker validation;
- C048 Extreme Magic is a strength subtype, not independent execution authority;
- repeated same-direction LTF Extreme may omit a fresh local TPW/local MHV cycle only under the separately accepted bounded valid-HTF MHV/RE condition; D1 is excluded in the current hierarchy.

No historical HOLD/rejected wording may silently re-enter execution after this closure rebaseline.


---

## 12. Change-control rule

Any future Strategy-Core change must be classified before acceptance:
- **KEEP** — already supported; no Core change.
- **CLARIFY** — makes an existing rule more precise without changing its semantic contract.
- **ADD** — genuinely new, source-supported Core rule.
- **CORRECT** — existing Core interpretation proven wrong and replaced by stronger source evidence.
- **HOLD / UNCERTAIN** — insufficient or conflicting evidence; no Core change.
- **REJECT FROM CORE** — personal, non-universal, implementation-only or unsupported material.

No `HOLD`, `UNCERTAIN` or `REJECT` item is allowed to enter executable Strategy Core silently.

---

## 13. Post-source-reconciliation Core delta

Relative to the earlier Core, accepted material now includes these specific clarifications/corrections:
- normal Extreme retest can span multiple candles and raw MA-outside condition is not entry authority;
- normal Extreme TP Wajib is refined toward the opposite MA5/MA10 area first, with Mid BB as farther context;
- MHV/MLV terminology and deterministic lifecycle are consolidated;
- expanding-BB requirement for Momentum/CSM is strengthened;
- eCSD/CSD remains direction information while Re-Entry is the setup;
- first-validation-candle / second-entry-candle wording remains a timing semantic subject to runtime mapping;
- Extreme maturity/reversal/retest lifecycle, Type 1 structural-ranging contract and H4 inherited owner semantics are closed at specification level;
- **D1 is now explicitly the strategic major-trend authority for new-entry direction**;
- **H4 remains the immediate structural/setup parent but cannot override D1**;
- **standalone H1 final higher-timeframe alignment now requires same-direction confirmed D1 strategic owner + same-direction active H4 owner**;
- **`D1_TRANSITION` / `D1_OWNER_UNRESOLVED` block new entries rather than freezing the previous D1 owner as executable authority**;
- **REM/RRE/REE signatures remain unchanged; D1 strategic gating is separate from component identity**;
- H4 restart uses verified checkpoint + deterministic replay as engineering policy; D1 current strategic state is rebuilt from closed-D1 price/MA50 history;
- the 49-family Home Course completeness set is fully classified with no unresolved Core semantic HOLD;
- residual Extreme touch/outside-reversal ambiguities are closed by rejection of unsupported universal shortcuts;
- the repeated-LTF Extreme / valid-HTF MHV-or-ReEntry exception is accepted only in bounded MTF scope and does not apply to D1 in the current hierarchy;
- Re-Entry validation-candle / immediately-following live-candle timing is closed at semantic/project-mapping level;
- SL/TP items without universal BBMA broker formulas are explicitly classified as Core, lifecycle principle, context, or project/EA-safety mapping rather than left as undefined Core obligations.

**Current unresolved BBMA Core semantic HOLD count: 0.**
