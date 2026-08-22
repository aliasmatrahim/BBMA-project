# BBMA Strategy Core — Source of Truth V2

## Status
**ACTIVE / AUTHORITATIVE FOR ACCEPTED BBMA STRATEGY-CORE RULES**

This document is the consolidated Strategy Core reference for the project after incorporating the accepted evidence from the two user-supplied PDF references and the BBMA Finale V01–V07 instructional transcript set.

It is a **derived project specification**, not a claim of authorship or official publication provenance. It does not replace the original source files. Every material rule must remain traceable to the source digest or Finale evidence.

`HOLD`, `UNCERTAIN`, personal workflow, risk-management and EA-management material are intentionally excluded from authoritative Core rules.

---

## 1. Source hierarchy

1. `PROJECT_INSTRUCTIONS.md` governs project scope and change control.
2. `Oma ally BBMA - AL.pdf` remains the **primary operational BBMA reference**.
3. `BBMA technique.pdf` remains the **secondary / historical corroborating reference**.
4. BBMA Finale V01–V07 is **supplemental instructional / clarification evidence**.
5. `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` is the page-indexed PDF digest plus accepted Finale clarification pointers.
6. `docs/references/video/oma_ally_finale/BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md` governs unresolved Finale conflicts/holds.

No subtitle-only statement may silently weaken an established PDF-derived rule. If evidence conflicts, the stricter established Core rule remains active until explicit resolution.

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

### 5.3 Extreme rules that remain HOLD
The following are **not authoritative Core rules yet**:
- MA5 merely touching the outer BB as equivalent to the established outside-BB Extreme condition.
- A reversal candle remaining outside BB but inside MA5 as a universal acceptance rule.
- Advanced / higher-timeframe Extreme exceptions without the normal TP-Wajib behaviour.

These remain governed by `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`.

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
- advanced Extreme without normal TP Wajib remains `HOLD / UNCERTAIN` and cannot bypass this canonical rule;
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

### 8.6 First-candle validation / second-candle entry wording
Finale repeatedly uses the teaching phrase “first Re-Entry candle validates; second candle is entry.” This is **accepted as a semantic/timing clarification to verify**, not as authorization to insert an additional full-candle delay.

The project’s closed-candle architecture may already implement the intended semantics by validating after the first candle closes and executing during the next candle. Exact runtime mapping must be verified before any code change.

Status: **CLARIFY / VERIFY — not a new Core timing rule yet**.

Source basis: Finale V06 00:30:46–00:31:06 and 00:52:48–00:56:27.

---

## 9. Multi-timeframe relationship

Accepted Core interpretation:
- BBMA must be read across related timeframes.
- A higher-timeframe Re-Entry may be completed/read through lower-timeframe signal/setup structures.
- An opposite-looking lower-timeframe direction signal must not automatically be treated as an independent reversal when it is structurally part of the higher-timeframe Re-Entry context.
- The structural principle scales across related chains such as D1/H4/H1, H4/H1/M15, H1/M15/M5 and M15/M5/M1, but project execution contracts use only explicitly approved timeframe signatures.

Source basis: primary PDF page 10 and pages 12–13; Finale V05 00:34:48–00:36:37 and 00:46:16–00:53:55; V06 00:26:57–00:29:02.

### 9.1 Standalone H1 Re-Entry higher-timeframe parent contract
**User-approved project Core decision:** standalone H1 Re-Entry uses **H4 as the immediate higher-timeframe parent/context owner** in the approved intraday chain.

Accepted contract:
- H1 standalone Re-Entry cannot be treated as autonomous from H4 BBMA context.
- D1 remains broader structural context but is not a universal mandatory hard gate for every standalone H1 Re-Entry.
- H4 compatibility is based on an **active authoritative BBMA directional/cycle owner**, not a single current H4 candle, EMA50-only reading, Mid-BB-only reading, score, or generic trend filter.
- Raw H4 Extreme and raw H4 MHV/MLV are pre-direction context and do not by themselves establish directional ownership.
- H4 directional ownership is inherited across one same-direction cycle: a valid direction signal establishes/advances the owner; same-direction Re-Entry and CSM/Momentum inherit/continue that owner.
- A valid H4 `eCSD` is sufficient to establish H4 directional ownership for parent compatibility; later same-direction CSD/Re-Entry/CSM may strengthen/advance the same owner but are not mandatory prerequisites.
- eCSD remains directional context only; it does not become direct trade-entry authority.
- A source-valid opposite H4 `eCSD`, `CSD`, or `CSM/Momentum` causes **atomic owner handover**: the old owner is superseded and the new opposite owner becomes authoritative on the closed-candle transition.
- Simultaneous authoritative H4 BUY and SELL owners are not allowed.
- An ordinary neutral H4 candle does not erase an inherited owner that remains structurally valid.
- If H4 is truly **`NO_OWNER`**, standalone H1 Re-Entry execution is blocked until a compatible authoritative H4 owner exists. No silent fallback to D1, MA50/Mid BB, candle color, generic price position, or absence of an opposite signal is permitted.
- H4 owner lifetime is **purely structural with no generic fixed candle/time/day/session expiry**.

Evidence classification: the requirement for higher-timeframe reading/alignment is a **DIRECT SOURCE PRINCIPLE**. H4-as-immediate-parent and the deterministic owner/inheritance/handover/no-owner/lifetime encoding are **SOURCE-INFERRED / STRONG HINT** based on the explicit H4/H1/M15 chain, source direction/setup separation and Finale parent/child teaching.

Decision provenance: `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`.

### 9.2 Restart/recovery preservation of the H4 owner
Restart/recovery mechanics are **EA ENGINEERING POLICY**, not an Oma Ally strategy rule, but they must preserve Section 9.1 semantics.

Approved recovery contract:
- persisted owner state is only a verified checkpoint/cache, not unquestioned source of truth;
- after restart, replay closed H4 history chronologically after the checkpoint using the same owner/invalidation/handover state machine;
- if checkpoint provenance cannot be verified, rebuild from available closed H4 history;
- if available history cannot prove an authoritative owner chain, resolve to `NO_OWNER` and block standalone H1 execution;
- the recovered H4 owner should equal the owner that uninterrupted closed-candle runtime would have produced.

This recovery mechanism must never invent direction from a current snapshot or unsupported fallback.

---

## 10. REM / RRE / REE exact signatures

The authoritative project signatures remain PDF-derived:
- **REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV**.
- **RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme**.
- **REE = D1 Re-Entry + H4 Extreme + H1 Extreme**.

All three components must be interpreted consistently with their own source-defined validity and direction contracts. Finale corroborates the higher-to-lower timeframe principle but does not provide sufficient transcript-only chart detail to redefine these signatures.

Additional maturity rules:
- every Extreme component in executable REM/REE must be at least reversal-confirmed;
- retest/standalone-entry readiness is not required merely because the Extreme is serving as an MTF combination component;
- the M15 MHV/MLV component in REM must be at least `FORMATION ESTABLISHED + FROZEN MARKED BODY`;
- M15 MHV/MLV retest completion is not mandatory merely to satisfy the REM component signature;
- a void/superseded or old-cycle historical-only M15 MHV/MLV cannot satisfy a new/current REM decision.

Source basis: primary PDF pages 12–13; Finale treated as corroboration plus the approved deterministic maturity decisions recorded in `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md` and `blueprint/decisions/CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md`.

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

## 13. Post-Finale Core delta

Relative to the pre-Finale project Core, the accepted material is predominantly **clarification/corroboration**, not strategy replacement.

Accepted material changes the project knowledge in these specific ways:
- clarifies that normal Extreme retest can span multiple candles and raw MA-outside condition is not entry authority;
- refines normal Extreme TP Wajib toward the opposite MA5/MA10 area as the first mandatory objective, with Mid BB as farther context;
- standardizes MHV/MLV as terminology aliases rather than separate setup types;
- closes the deterministic MHV/MLV lifecycle: mandatory reversal-confirmed prior Extreme provenance, normal TP-Wajib completion, structural loss-of-momentum, most-extreme body + first move-away formation, immediate frozen marked body, range-touch retest, REM component maturity, stage-bounded invalidation, same-cycle direction progression and opposite reversal-confirmed Extreme atomic cycle supersession;
- keeps double/triple and H&S-like MHV morphology as supported examples rather than mandatory universal formulas;
- strengthens the existing expanding-BB requirement for Momentum/CSM;
- strengthens the interpretation that eCSD/CSD is direction information and Re-Entry is the entry setup;
- clarifies higher-timeframe ownership/context of lower-timeframe signals;
- records the first-validation-candle / second-entry-candle phrase as a timing semantic that still requires runtime mapping;
- closes the user-approved Extreme maturity/reversal/retest lifecycle: reversal-confirmed is sufficient for REM/REE components; standalone Extreme requires later body-or-MA5 retest; deterministic reversal direction, phase transition, frozen body anchor, first-valid-reference retest and invalidation precedence are specified;
- closes the Type 1 structural-ranging contract, including prior BBMA-state proof, structural invalidation and no fixed minimum/expiry count;
- closes the standalone H1 Re-Entry H4-parent contract, including inherited H4 owner semantics, eCSD owner authority, atomic opposite handover, no-owner block and structural owner lifetime;
- records verified checkpoint + deterministic replay as engineering-only restart/recovery policy to preserve the H4 owner contract.

The unresolved Extreme exceptions and personal/workflow material remain outside authoritative Core.