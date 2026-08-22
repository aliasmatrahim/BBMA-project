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

### 5.4 Extreme maturity when used inside REM / REE
**User-approved project Core decision:** an Extreme used as a component of an executable REM or REE must be at least **reversal-confirmed**.

Maturity distinction:
- `RAW EXTREME` = strict MA5/MA10-outside-BB condition only. Not sufficient for executable REM/REE.
- `REVERSAL-CONFIRMED EXTREME` = raw Extreme plus source-valid reversal confirmation. Eligible as an Extreme component of REM/REE.
- `RETEST / ENTRY-READY EXTREME` = reversal-confirmed Extreme plus the later retest. Required for standalone Extreme entry eligibility.

Evidence classification: **SOURCE-INFERRED / STRONG HINT**, not a verbatim Oma Ally statement specifically defining REM/REE component maturity.

Reasoning basis:
- V04 separates raw Extreme, reversal confirmation and retest, and ties the retest to standalone Extreme entry.
- V05 teaches lower-timeframe Extreme/MHV/direction structures as supporting completion for higher-timeframe Re-Entry, indicating that supporting MTF Extreme context is not identical to standalone Extreme entry maturity.

Decision provenance: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`.

Implementation guard: this decision does **not** authorize inventing a reversal-candle algorithm. A deterministic source-faithful reversal-confirmation contract must still be specified before patching M08/M13/M14/M15 behavior.

---

## 6. MHV / MLV

### 6.1 Terminology
`MHV` (Market Hilang Volume) and `MLV` are treated as source-terminology aliases for the same loss-of-volume setup family unless future source evidence explicitly distinguishes them.

Do not create two separate Strategy-Core setup types merely because the source documents use different abbreviations.

### 6.2 Structural rule
- MHV/MLV normally forms after Extreme / TP phase in the BBMA cycle.
- It represents loss of prior momentum/volume.
- It becomes invalid/void when price breaks and closes outside the relevant outer BB.
- Highest/lowest candle body or equivalent marked reference is used for possible retest context.
- Double/triple top or bottom morphology is supported.
- H&S-like morphology shown in Finale is an example, not a mandatory condition.
- MHV/MLV is a setup/context structure, not a raw execution signal by itself.

Source basis: primary PDF pages 7–8; historical PDF pages 31–34; Finale V05 00:18:07–00:28:12 and V01 00:59:18–01:00:05.

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
- SELL context: MA5/10 High acts as resistance; sell Re-Entry is considered when price finds the relevant cluster and the validating candle remains/closes on the permitted SELL side.
- BUY context: MA5/10 Low acts as support; buy Re-Entry is considered when price finds the relevant cluster and the validating candle remains/closes on the permitted BUY side.

Source basis: primary PDF page 9; Finale supporting context V01/V02/V03/V05/V06. The structural-ranging interpretation is **SOURCE-INFERRED / STRONG HINT** around the PDF-explicit sideways/ranging requirement. The no-fixed-candle rule is a source-faithful project specification because the source provides no universal Type 1 candle count.

Decision provenance: `blueprint/decisions/CORE_V2_F3_TYPE1_CONTEXT_DECISION.md`.

Implementation guard: a deterministic BBMA-state predicate for prior movement, momentum pause, consolidation/retrace and invalidation still requires specification before M12 is patched. Do not introduce RSI/ADX/ATR/fixed-pip thresholds as disguised Core rules.

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

---

## 10. REM / RRE / REE exact signatures

The authoritative project signatures remain PDF-derived:
- **REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV**.
- **RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme**.
- **REE = D1 Re-Entry + H4 Extreme + H1 Extreme**.

All three components must be interpreted consistently with their own source-defined validity and direction contracts. Finale corroborates the higher-to-lower timeframe principle but does not provide sufficient transcript-only chart detail to redefine these signatures.

Additional maturity rule from Section 5.4:
- every Extreme component in executable REM/REE must be at least reversal-confirmed;
- retest/standalone-entry readiness is not required merely because the Extreme is serving as an MTF combination component.

Source basis: primary PDF pages 12–13; Finale treated as corroboration plus the user-approved source-inferred maturity decision recorded in `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`.

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
- enriches MHV/MLV retest/morphology interpretation without making H&S mandatory;
- strengthens the existing expanding-BB requirement for Momentum/CSM;
- strengthens the interpretation that eCSD/CSD is direction information and Re-Entry is the entry setup;
- clarifies higher-timeframe ownership/context of lower-timeframe signals;
- records the first-validation-candle / second-entry-candle phrase as a timing semantic that still requires runtime mapping;
- adds the user-approved source-inferred maturity distinction that REM/REE Extreme components must be reversal-confirmed, while standalone Extreme entry still requires the later retest;
- adds the user-approved Type 1 structural-ranging interpretation and explicitly rejects inventing a fixed Type 1 minimum candle count.

The unresolved Extreme exceptions and personal/workflow material remain outside authoritative Core.