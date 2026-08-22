# F7-R — SL/TP Evidence & Reasoning Reconstruction Audit

Date: 2026-08-22
Status: EVIDENCE RECONSTRUCTED / PROVENANCE CLARIFIED / NO CODE CHANGE
Scope: reconstruct the reasoning chain behind current M17 SL/TP policy using accepted PDF evidence, Finale V01–V07, project contracts, and corroborating BBMA forum evidence. This audit does not change `.mq4` logic by itself.

## 1. Why this audit exists
The current M17 contract correctly separates `PDF_CORE`, `FORUM_SUPPORTED`, and `EA_SAFETY`, but a later project summary over-compressed the TP provenance as merely forum-derived. The historical design decision was broader: PDF/Core defines BBMA structure and destination semantics, Finale supplies MTF/context clarification, forum material corroborates practical Re-Entry destination and protective-stop usage, and the EA converts those semantics into one deterministic autonomous execution policy.

This audit reconstructs that chain without falsely upgrading any rule to verbatim PDF language.

## 2. Evidence hierarchy
1. `Oma ally BBMA - AL.pdf` — primary operational BBMA reference.
2. `BBMA technique.pdf` — secondary/historical corroboration.
3. BBMA Finale V01–V07 — supplemental instructional clarification and MTF/context evidence.
4. BBMA/Oma Ally forum notes and practitioner explanations — corroborating evidence, not primary-source override.
5. EA engineering — deterministic broker protection only; cannot be represented as Oma Ally strategy semantics.

## 3. Reconstructed reasoning chain

### 3.1 Strategy structure before exit mapping
Accepted Core establishes:
- BBMA operates as a cycle, not isolated indicator touches;
- Extreme has explicit TP-Wajib structure toward the opposite MA5/MA10 area, with farther BB context;
- eCSD/CSD establishes direction/context rather than direct execution;
- Re-Entry is a principal entry/setup zone after direction;
- higher-timeframe setup ownership matters and lower-timeframe structures may complete/confirm higher-timeframe intent;
- REM/RRE/REE preserve an explicit validated Re-Entry component at a specific source timeframe.

Therefore an autonomous exit resolver should preserve the timeframe/owner of the validated Re-Entry rather than manufacture an unrelated fixed-pip or generic RR target.

### 3.2 TP destination reasoning
Current M17 mapping:
- standalone H1 `RE_ENTRY`: BUY -> H1 TOP BB; SELL -> H1 LOW BB;
- `REM`: BUY -> H4 TOP BB; SELL -> H4 LOW BB;
- `RRE`: BUY -> D1 TOP BB; SELL -> D1 LOW BB;
- `REE`: BUY -> D1 TOP BB; SELL -> D1 LOW BB.

Reasoning:
1. The decision payload already identifies the validated Re-Entry component and its exact timeframe.
2. BBMA uses outer-BB destinations as structural price objectives in the taught framework; Extreme TP-Wajib semantics prove that exits are structural rather than arbitrary pip targets, although they do not by themselves prove the exact Re-Entry mapping above.
3. Finale MTF teaching reinforces that an overshot/lower-TF Re-Entry may be seeking a higher-timeframe Re-Entry/structure; therefore target ownership must follow the validated higher-TF setup rather than the chart on which execution happens.
4. Forum evidence attributed to BBMA/Oma Ally notes/practice explicitly corroborates holding a validated higher-TF Re-Entry toward that timeframe's directional outer BB. Example discussed in the forum: when Daily Re-Entry becomes valid, hold toward Top BB Daily or H4.
5. M17 therefore resolves the directional outer BB on the exact closed source-component candle/timeframe. If that target is already crossed or on the wrong side of entry, the trade fails closed.

### 3.3 Correct TP provenance classification
The mapping is NOT accurately described as `PDF_CORE` verbatim and is also too reductive to describe its reasoning as `forum only`.

Final classification:
- structural destination principle: `BBMA_CORE_DERIVED`;
- higher-timeframe/source-owner selection: `CORE + FINALE MTF DERIVED`;
- exact Re-Entry -> directional outer-BB practical mapping: `CORROBORATED / FORUM_SUPPORTED`;
- exact executable resolver and fail-closed geometry: `PROJECT DETERMINISTIC MAPPING / EA_ENGINEERING`.

For compatibility with the existing three-class M17 contract, the executable TP may continue to carry the coarse label `FORUM_SUPPORTED`, but documentation MUST retain the richer reasoning chain above. `FORUM_SUPPORTED` means the exact executable target is not explicit PDF text; it does not mean the decision was derived from forum evidence alone.

## 4. SL reasoning reconstruction
Current hard SL:
- BUY -> exact closed Re-Entry source candle LOW minus one broker point;
- SELL -> exact closed Re-Entry source candle HIGH plus one broker point.

Evidence/reasoning:
1. BBMA source material is primarily setup/structure teaching and does not provide a complete universal broker-hard-SL formula for every executable Re-Entry/REM/RRE/REE case.
2. Forum BBMA practitioners explicitly describe a classic/protective SL below the previous low/high or source-timeframe candle wick when a trader wants a hard stop.
3. The EA must have deterministic broker-side protection for autonomous operation; therefore the structural wick of the exact validated source candle is chosen instead of an arbitrary swing scan.
4. One broker point beyond the wick is purely execution engineering and has no BBMA semantic claim.
5. `MaxSLPips`, `MinRRRatio`, StopLevel and FreezeLevel remain rejection/broker-safety policy only and never manufacture a replacement SL/TP.

Final classification:
- structural wick idea: `FORUM_CORROBORATED STRUCTURAL PRACTICE`;
- mandatory broker hard stop for autonomous EA: `EA_SAFETY`;
- exact source-candle selection: `PROJECT DETERMINISTIC MAPPING` preserving source ownership;
- +/- one Point buffer: `BROKER_ENGINEERING`.

## 5. What PDF / Finale do and do not prove
### Strongly supported
- structural/cycle-based BBMA interpretation;
- direction before Re-Entry;
- Re-Entry as setup/entry zone;
- higher-timeframe ownership/context;
- BB/MA structural objectives rather than arbitrary fixed-pip semantics;
- exact source component must not be silently replaced by an unrelated timeframe.

### Not claimed as explicit PDF formula
- every Re-Entry must always TP at directional outer BB;
- REM/RRE/REE exact TP table as verbatim Oma Ally PDF text;
- hard SL must always be source-candle wick;
- one-point SL buffer;
- MinRR/MaxSL rejection thresholds.

This boundary prevents both under-crediting the evidence chain and overstating provenance.

## 6. Forum corroboration rechecked
Fresh public search reconfirmed the relevant BBMA forum evidence:
- Re-Entry is taken after direction and retracement to MA High/Low, not immediately on CSD/CSM;
- a Daily Re-Entry example is described as valid after confirmation and held toward Top BB Daily or H4;
- classic SL, if used, is suggested below/above the previous low/high of the entry/source timeframe, e.g. H1 previous-low candle wick;
- forum-translated BBMA Oma Ally SSS notes state first candle validates Re-Entry and second candle is entry, reinforcing the source-candle/owner separation already used by F6/M17.

These posts are corroboration and do not override the PDFs or Finale.

## 7. Decision on current M17
### TP
KEEP current mapping. No evidence found in this reconstruction justifies replacing it with fixed pips, generic RR, nearest BB on execution timeframe, or another arbitrary target.

### SL
KEEP current protective hard-SL policy. It remains autonomous-EA safety, not an official Oma Ally universal SL formula.

### Provenance
REPAIR documentation wording only: current TP is evidence-triangulated and Core/Finale-derived in reasoning, with the exact practical outer-BB mapping forum-corroborated. Current hard SL remains EA safety with forum-corroborated structural anchoring.

## 8. Compliance statement
A correct project claim is:

> BBMA signal/setup semantics are governed by the accepted PDF + Finale Core. M17 preserves the validated Re-Entry source/timeframe and applies an evidence-triangulated structural TP policy whose exact outer-BB mapping is forum-corroborated, plus a deterministic EA-safety hard SL based on the exact source candle wick. Broker buffers and risk rejection filters are engineering policy, not Oma Ally rules.

An incorrect claim is:

> The entire current M17 SL/TP formula is explicitly written in the Oma Ally PDF.

Another incorrect claim is:

> The current TP came only from a random forum rule.

## 9. Outcome
- F7-R: PASS — reasoning reconstructed.
- Current M17 logic: NO CHANGE REQUIRED from provenance reconstruction.
- TP provenance: strengthened from an over-simplified `forum only` description to an evidence-triangulated layered classification.
- SL provenance: remains deliberately separated as EA safety / structural practice.
- Runtime geometry and order-time verification remain implementation evidence work, not source-governance uncertainty.
