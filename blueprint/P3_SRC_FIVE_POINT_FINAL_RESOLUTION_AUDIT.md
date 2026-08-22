# P3-SRC — Five-Point BBMA Source Uncertainty Final Resolution Audit

Date: 2026-08-22
Branch target: `blueprint-dev`
Scope: source-governance resolution only. No `.mq4` strategy logic change is authorized by this record alone.

## Evidence hierarchy
1. User-supplied `Oma ally BBMA - AL.pdf` — primary operational reference.
2. User-supplied `BBMA technique.pdf` — secondary/historical corroboration.
3. BBMA Finale V01–V07 — supplemental instructional clarification.
4. Public web/forum material — corroborating evidence only unless provenance can be established as primary Oma Ally material.
5. Project deterministic mappings — allowed only where human/chart-based source concepts require machine-state encoding; must be explicitly labelled as project mapping, never as verbatim Oma Ally formula.

## Resolution summary

| Point | Topic | Final status | Executable decision |
|---|---|---|---|
| U-01 | Advanced/MTF Extreme without normal TP Wajib | RESOLVED BY SCOPE BOUNDARY | No universal no-TP-Wajib Extreme exception enters Core. Normal Extreme retains TP-Wajib semantics. A lower-TF Extreme embedded as a component of a higher-TF setup does not automatically create an independent broker TP action; component semantics and position-exit semantics are separate. |
| U-02 | MA5 touch-only Extreme | RESOLVED | Strict RAW Extreme detector requires relevant MA5/MA10 outside the outer BB. Touch-only remains non-Core / optional community interpretation and cannot satisfy executable Extreme authority. |
| U-03 | Reversal candle outside BB but inside MA5 | RESOLVED | `close back inside BB` is not a universal hard prerequisite. Reversal confirmation follows the approved F2 lifecycle; outside-BB directional Momentum/CSM invalidation has priority. No blanket `outside BB + inside MA5 = valid` shortcut is introduced. |
| U-04 | Deterministic state-machine mappings not verbatim in source | RESOLVED BY GOVERNANCE | Keep minimal deterministic mappings where required, but classify them explicitly as PROJECT DETERMINISTIC MAPPING. Each must preserve a direct/source-derived concept, be fail-closed, avoid invented indicators/thresholds, and remain replaceable if stronger source evidence appears. |
| U-05 | M17 SL/TP provenance | RESOLVED BY PROVENANCE SEPARATION | Do not call current executable SL/TP wholly `PDF_CORE`. Re-Entry/combination TP mapping remains `FORUM_SUPPORTED` project execution policy; hard SL remains `EA_SAFETY` informed by structural practice. This is acceptable for autonomous EA execution only when the documentation preserves this provenance boundary. |

---

## U-01 — Advanced / MTF Extreme without normal TP Wajib

### Internal evidence
- Primary PDF digest defines normal cycle `Extreme -> TP Wajib -> MHV/MLV` and normal Extreme TP toward the opposite MA5/MA10 area.
- Finale V04/V05 mentions advanced or MTF contexts in which the normal TP-Wajib action is not taken, but does not provide a deterministic universal classifier for a new standalone Extreme class.
- Existing Core V2 already requires normal TP-Wajib structural completion for the canonical MHV parent chain.

### External corroboration
Public BBMA teaching material repeatedly presents normal Extreme as MA outside BB -> reversal -> retest/entry -> TP Wajib at opposite MA5/MA10, with Mid BB as farther context. Public forum material also distinguishes basic/intermediate/advanced BBMA and warns that advanced treatment is additional structure rather than a replacement for basic rules.

### Resolution
The ambiguity came from mixing **signal-component semantics** with **broker-position TP actions**.

Locked interpretation:
- For a standalone normal Extreme trade, TP-Wajib semantics remain active.
- An Extreme used only as a lower-timeframe component inside a higher-timeframe Re-Entry/combination does not automatically create a separate broker trade requiring its own independent TP event.
- This does **not** mean `Extreme has no TP Wajib`; it means a non-executed component is not itself a separate position.
- No universal advanced/no-TP standalone Extreme detector is authorized until a deterministic primary-source classifier exists.

Result: source ambiguity is closed for the current executable Core without inventing an advanced rule.

---

## U-02 — MA5 touch-only Extreme

### Internal evidence
- Primary PDF digest: relevant MA must be outside the corresponding outer BB.
- Core V2 strict RAW Extreme already uses the outside-BB rule.
- Finale V05 says touch may sometimes be treated as Extreme while clearly outside is the better form; this was previously a conflict.

### External corroboration
Multiple public BBMA references consistently describe Extreme as MA5 outside the BB. Community tools sometimes offer `touch` as an optional user filter, which confirms that touch is a looser interpretation rather than the canonical strict rule.

### Resolution
For deterministic EA authority:
- `outside` is mandatory for RAW Extreme.
- `touch-only` cannot promote a candidate to RAW Extreme.
- Touch can be retained only as non-authoritative observability/research metadata if ever needed; it must not affect entry authority.

Result: RESOLVED.

---

## U-03 — Reversal candle location relative to BB / MA5

### Internal evidence
- Primary PDF requires a reversal candle but does not establish a universal hard `must close inside BB` Boolean.
- Finale V04 says inside BB is preferable.
- Finale V05 describes a nuanced case where a reversal can still be meaningful outside BB but inside the relevant MA5, provided it has not become continuing Momentum.
- Core V2 F2 already gives outside-BB/Momentum invalidation priority and deliberately does not add a universal close-back-inside-BB requirement.

### External corroboration
Public teaching summaries consistently require `reverse candle` plus later retest, while outside-BB closes associated with continuing momentum invalidate the reversal/Extreme context. They do not consistently state that every reversal candle must close inside BB.

### Resolution
- Remove the uncertainty by separating **preference** from **hard validity**.
- `inside BB` = preferred/stronger visual teaching condition, not universal Boolean gate.
- `outside BB but inside MA5` = contextual possibility, not automatic acceptance rule.
- Authoritative machine rule remains F2 reversal direction + structural lifecycle, with Momentum/outside-BB invalidation priority.

Result: RESOLVED without broadening the detector arbitrarily.

---

## U-04 — Project deterministic mappings

### Problem
Oma Ally material is chart/context teaching, not a complete formal specification. EA implementation therefore needs deterministic state transitions for concepts such as reversal maturity, body anchors, retest start/completion, owner handover and cycle supersession.

### Resolution rule
A project deterministic mapping is valid only if all conditions hold:
1. It encodes a concept directly stated or strongly source-derived from the accepted Core.
2. It adds no external trading indicator or unsupported filter.
3. It uses no arbitrary pip, ATR, RSI, ADX, score, fixed candle-count or timeout threshold unless separately source-authorized.
4. It is fail-closed when provenance/state cannot be proven.
5. It is explicitly documented as `PROJECT DETERMINISTIC MAPPING`, not as a verbatim Oma Ally formula.
6. It is covered by static/runtime invariants and may be replaced if stronger source evidence becomes available.

Existing F1-F4 mappings satisfy this governance model at the recorded static-audit level. Runtime traces remain evidence work, not source uncertainty.

Result: RESOLVED BY GOVERNANCE.

---

## U-05 — M17 SL/TP provenance

### Internal evidence
The current M17 contract already distinguishes:
- `PDF_CORE`;
- `FORUM_SUPPORTED`;
- `EA_SAFETY`.

Current executable mapping:
- standalone H1 Re-Entry TP -> H1 directional outer BB;
- REM TP -> H4 directional outer BB;
- RRE/REE TP -> D1 directional outer BB;
- hard SL -> exact source Re-Entry candle wick plus one broker point.

The project primary PDF gives explicit TP-Wajib semantics for Extreme, but does not establish the current complete Re-Entry/REM/RRE/REE hard-SL/TP mapping as universal PDF Core.

### External corroboration
Forum practitioners describing BBMA/Oma Ally use higher-timeframe Re-Entry destination BBs as TP areas and suggest previous/source-timeframe wick/high-low as classic protective SL. Other forum posts explicitly state that basic BBMA material contains limited trade-management detail. Therefore this evidence corroborates the current execution policy but does not upgrade it to primary-source Core.

### Resolution
- Current M17 execution policy is acceptable **with provenance separation**.
- Do not claim `100% PDF Core SL/TP` for Re-Entry/REM/RRE/REE.
- TP mapping remains `FORUM_SUPPORTED`.
- Hard SL remains `EA_SAFETY`, structurally informed, and its one-point buffer is pure broker engineering.
- `MinRR`, `MaxSL`, StopLevel/FreezeLevel remain EA safety/rejection policies, not BBMA semantics.
- Strategy compliance claims must therefore distinguish `BBMA signal/setup compliance` from `autonomous execution protection policy`.

Result: RESOLVED. F7 source-governance decision can be closed; no code change is required solely from this resolution.

---

## Final confidence classification

### Source/Core semantics
HIGH confidence for current executable basic/intermediate Core:
- cycle;
- strict Extreme;
- reversal/retest lifecycle;
- normal TP-Wajib concept;
- MHV/MLV lifecycle;
- eCSD/CSD direction semantics;
- Re-Entry Type 1-4;
- higher-timeframe context;
- REM/RRE/REE signatures.

### Explicitly outside `official Core` claims
- touch-only Extreme;
- universal advanced/no-TP standalone Extreme exception;
- personal H4 workflow;
- personal/sample win-rate claims;
- current hard-SL engineering rule;
- forum-derived outer-BB TP mapping as if it were explicit PDF language.

### Remaining work is runtime evidence, not source ambiguity
- F1-F6 lifecycle traces;
- P3-M1 Mode 1 runtime trace;
- opposite-direction pair integrity runtime trace;
- P3 Step 5 recovery/execution identity closure.

## Closure statement
All five requested source uncertainties are now resolved for the project's executable governance. Where the underlying teaching material remains intrinsically contextual, the resolution is a conservative scope/provenance boundary rather than an invented trading rule.
