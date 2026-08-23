# Decision — D1 Major-Trend Owner / D1_TRANSITION

Date: 2026-08-24  
Branch: `blueprint-dev`  
Status: **RESOLVED AT STRATEGY / SPECIFICATION LEVEL — IMPLEMENTATION DEFERRED; NO EA SOURCE CHANGE**

## 1. Purpose

Resolve the previously open `D1_TRANSITION` question created by the Home Course reconciliation:

> When the latest closed D1 candle and the D1 MA50 slope no longer agree on one clear major-trend direction, should the EA freeze the last confirmed D1 owner for new entries, or block new entries until a new D1 owner is confirmed?

This decision also defines the minimum deterministic D1 major-trend owner classification needed later by standalone H1 Re-Entry, REM, RRE, REE, and D1-owned lifecycle work.

This is documentation/specification only. `blueprint/source/BBMA_EA.mq4` remains unchanged while the active P3 runtime candidate is frozen.

---

## 2. Mandatory source + GitHub preflight

Applied project order:

`PROJECT_INSTRUCTIONS -> SOURCE_INDEX -> canonical Core -> primary/secondary PDFs -> Finale -> retained forum evidence -> prior Home Course reconciliation -> current contracts/code`

Relevant live records checked:
- `PROJECT_INSTRUCTIONS.md`;
- `docs/references/SOURCE_INDEX.md`;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- `docs/references/video/oma_ally_finale/BBMA_FINALE_MASTER_RULE_INDEX.md`;
- `docs/references/original/forum/forexfactory_bbma_strategy_by_oma_ally/DEEP_EXTRACTION_REGISTER.md`;
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`;
- active `blueprint/source/BBMA_EA.mq4`;
- current `blueprint/CURRENT.md` and `blueprint/MASTER_QUEUE.md`.

No retained Finale/forum evidence was found that supplies a stronger deterministic D1 transition algorithm than the PDF/Home Course MA50 evidence. Therefore no lower-precedence source overrides the resolution below.

---

## 3. Source-derived D1 / MA50 findings

### 3.1 D1 is the project major-trend authority

The Home Course evidence states that:
- major trend is MA50;
- MA50 functions properly from at least Daily/D1;
- H4 does not carry the major trend;
- if D1 says BUY while H4 says SELL, follow D1;
- the closed Daily candle governs the next day's directional reading.

The primary operational PDF independently says:
- confirm trend using MA50 on the Daily chart;
- price above MA50 is uptrend context;
- price below MA50 is downtrend context;
- when price is above MA50 and MA50 is ascending, trend is bull;
- when price is below MA50 and MA50 is descending, trend is bear;
- MA50 acts as support/resistance and a break/interaction around MA50 can signal reversal/continuation context.

Therefore D1 major-trend authority is source-supported and is distinct from the H4 immediate setup-parent role.

### 3.2 Source does not define a software transition state

The sources do not explicitly define what an EA should do when:
- D1 close is above MA50 but MA50 is flat/falling;
- D1 close is below MA50 but MA50 is flat/rising;
- D1 closes exactly at MA50;
- a first D1 close crosses MA50 while the MA50 slope still points in the previous direction.

That ambiguity requires a minimal deterministic project mapping. It must not silently become an invented reversal rule.

---

## 4. Canonical D1 owner states

The future specification shall use four conceptual states:

- `D1_OWNER_BUY_CONFIRMED`
- `D1_OWNER_SELL_CONFIRMED`
- `D1_TRANSITION`
- `D1_OWNER_UNRESOLVED` — missing/invalid closed-D1 history only

The state is evaluated only from **fully closed D1 candles**.

For the latest closed D1 candle:

- `Close1` = latest closed D1 close;
- `MA50_1` = EMA50 on that same closed D1 candle;
- `MA50_2` = EMA50 on the immediately previous closed D1 candle.

### D1 BUY confirmed

`Close1 > MA50_1` **AND** `MA50_1 > MA50_2`

### D1 SELL confirmed

`Close1 < MA50_1` **AND** `MA50_1 < MA50_2`

### D1_TRANSITION

With otherwise valid closed-D1 data, any state that is neither confirmed BUY nor confirmed SELL is `D1_TRANSITION`, including:
- close above MA50 while MA50 is flat/falling;
- close below MA50 while MA50 is flat/rising;
- close at MA50;
- MA50 flat;
- first cross to the opposite side while the MA50 slope still points in the previous direction.

No ATR, pip buffer, fixed percentage distance, score, RSI/ADX, session, news, or fixed-N-day confirmation rule is introduced.

Classification:
- D1/MA50 major-trend concept = **DIRECT SOURCE**;
- price-side + MA50-slope agreement = **DIRECT PRIMARY-PDF RULE**;
- explicit software state `D1_TRANSITION` = **MINIMAL DETERMINISTIC PROJECT MAPPING**.

---

## 5. D1_TRANSITION execution decision

### Decision

**BLOCK NEW STRATEGY ENTRIES UNTIL A CONFIRMED D1 OWNER EXISTS.**

Do **not** freeze the last confirmed D1 direction as active execution authority during `D1_TRANSITION`.

Reason:
- freezing an old BUY owner after a closed D1 has moved below MA50 would contradict the new D1 price-side evidence;
- immediately flipping to SELL while MA50 is still rising would contradict the MA50-slope evidence;
- the source does not authorize H4 to resolve that D1 ambiguity;
- project governance requires fail-closed handling when BBMA semantics are genuinely ambiguous.

The last confirmed D1 direction may be retained only as historical/diagnostic provenance. It is **not** allowed to authorize a new trade while current state is `D1_TRANSITION`.

### Consequence

While `D1_TRANSITION`:
- detectors continue to run;
- Re-Entry/REM/RRE/REE candidates may still be observed/recorded;
- no candidate may acquire final new-entry execution authority;
- H4 cannot override the transition;
- no new counter-D1 or same-old-D1 order is opened merely by inheriting the previous owner.

This blocking rule is **project fail-closed execution mapping**, not claimed verbatim Oma Ally wording.

---

## 6. Owner handover / re-confirmation

No fixed two-day/three-day confirmation is added.

The first fully closed D1 candle that satisfies one of the confirmed conditions is sufficient to restore execution authority:

- transition -> `Close1 > MA50_1` and rising MA50 -> `D1_OWNER_BUY_CONFIRMED`;
- transition -> `Close1 < MA50_1` and falling MA50 -> `D1_OWNER_SELL_CONFIRMED`.

If this direction differs from the last confirmed owner, that closed-D1 transition is the atomic major-trend owner handover.

The source statement that today's D1 close determines tomorrow's movement supports using the next completed D1 evidence rather than inventing an extra full-candle delay.

---

## 7. Relationship to H4, standalone H1 Re-Entry and REM

The prior reconciliation remains valid:

`D1 major-trend authority -> H4 immediate setup parent -> H1 signal/completion -> M15 fine/additional entry`

### Standalone H1 Re-Entry

Future final eligibility requires both:
1. valid compatible H4 directional owner; and
2. confirmed D1 major-trend owner in the same execution direction.

A valid H4 owner by itself cannot authorize an H1 Re-Entry against a confirmed opposite D1 owner or during `D1_TRANSITION`.

### REM

REM's source signature remains unchanged:

`H4 Re-Entry + H1 Extreme + M15 MHV/MLV`

D1 is **not** added as a fourth REM component. It is a separate strategic-direction execution gate.

A structurally valid REM may therefore exist while non-executable because:
- D1 owner is opposite; or
- D1 is in transition/unresolved.

M13/M14 must not rewrite the REM signature merely to express this gate.

---

## 8. Relationship to RRE / REE

The signatures remain:
- `RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme`;
- `REE = D1 Re-Entry + H4 Extreme + H1 Extreme`.

Their D1 Re-Entry component does not silently replace the D1 MA50 major-trend owner.

Future final execution eligibility requires:
- valid exact RRE/REE component signature;
- D1 major-trend owner confirmed;
- combination direction compatible with that confirmed D1 owner.

If D1 is `D1_TRANSITION`, the combination may remain structurally observable but is not executable yet.

This preserves the distinction between:
- D1 Re-Entry = setup/component state; and
- D1 MA50 = major-trend strategic authority.

---

## 9. Existing live positions during D1_TRANSITION

`D1_TRANSITION` is **not** by itself a broker close rule.

Existing live positions remain governed by their already-approved position lifecycle, protective SL, and M20 emergency protection.

Do not auto-close an existing position solely because the D1 MA50 state becomes transitional.

Reason:
- MA50 transition indicates uncertainty/change in strategic trend context;
- it is not identical to the already accepted BBMA cycle-supersession event such as an opposite reversal-confirmed Extreme on the relevant lifecycle-owner timeframe;
- entry authority and live-position exit authority remain separate architectural responsibilities.

---

## 10. Recovery / restart mapping

No persistent D1 owner checkpoint is required merely to make new-entry gating safe.

On restart, the current D1 major-trend state can be deterministically rebuilt from:
- latest closed D1 candle;
- latest closed D1 MA50;
- immediately previous closed D1 MA50.

If the latest state is transitional, execution remains blocked. The historical last-confirmed direction may be reconstructed only if needed for diagnostics; it is not required for current execution authority.

If the required two closed-D1 MA50 values are unavailable/invalid:

`D1_OWNER_UNRESOLVED -> BLOCK NEW ENTRIES`

No H4/current-candle fallback is permitted.

---

## 11. Current implementation comparison

### Gap A — current `TimeframeData.trend` is incomplete for D1 owner semantics

The active EA currently sets `data.trend` only from the candle close relative to EMA50:
- above -> `1.0`;
- below -> `-1.0`;
- equal -> `0`.

It does not include MA50 slope in that trend value.

Therefore it cannot distinguish a confirmed D1 owner from `D1_TRANSITION` as resolved here.

### Gap B — Module 11 has no implemented D1 major-trend owner state

The active source contains the `MODULE 11: TREND FUNCTIONS` section marker but no dedicated D1 major-trend owner lifecycle/state implementation.

### Gap C — standalone H1 Re-Entry currently gates only on H4 owner

The active `BuildConfirmedReEntryCandidate()` explicitly requires a compatible H4 owner and states that no D1/EMA fallback is used.

That was correct under the older F4 decision but is now incomplete after the stronger Home Course D1-major-trend reconciliation.

### Gap D — REM final eligibility has no separate D1 major-trend gate

The source-locked REM signature must remain unchanged, but the final execution path still needs a separate D1 strategic-direction eligibility check.

### Gap E — RRE/REE need explicit D1-owner compatibility

Their D1 Re-Entry component is structural identity, not proof that the MA50 major-trend owner is confirmed in the same direction.

These are **specification/implementation gaps exposed by stronger source reconciliation**, not evidence that the original PDF signatures themselves are wrong.

---

## 12. Future module ownership

Recommended ownership without duplicate strategy authority:

### M11 — D1 major-trend producer
Owns the deterministic closed-D1 classification:
- BUY confirmed;
- SELL confirmed;
- TRANSITION;
- UNRESOLVED.

M11 does not select trades.

### M13/M14
Keep exact REM/RRE/REE component construction/validation unchanged. They do not add D1 as a fourth REM component.

### M15 — final new-entry strategic gate
Consumes the M11 D1 owner and blocks final new-entry authority when:
- owner is transition/unresolved; or
- candidate direction disagrees with confirmed D1 owner.

### M16
May revalidate the frozen D1-owner identity/freshness as part of existing downstream validity checking, but must not independently invent a second D1 trend formula.

### M23/M24
Do not use `D1_TRANSITION` as an invented ordinary close rule. Existing position lifecycle remains separately governed.

---

## 13. Canonical transition table

| Latest closed D1 state | Result | New-entry authority |
|---|---|---|
| Close > MA50 and MA50 rising | D1 BUY CONFIRMED | BUY-direction candidates only, subject to all other BBMA gates |
| Close < MA50 and MA50 falling | D1 SELL CONFIRMED | SELL-direction candidates only, subject to all other BBMA gates |
| Close > MA50 but MA50 flat/falling | D1_TRANSITION | BLOCK |
| Close < MA50 but MA50 flat/rising | D1_TRANSITION | BLOCK |
| Close == MA50 | D1_TRANSITION | BLOCK |
| D1/MA50 history invalid or incomplete | D1_OWNER_UNRESOLVED | BLOCK |

No fixed timer or extra confirmation candle is added.

---

## 14. Decision verdict

`D1_TRANSITION` is now **RESOLVED**:

> When D1 price-side and MA50 slope do not agree on a confirmed major-trend direction, preserve the old direction only as historical provenance and **block all new strategy entries** until a later fully closed D1 candle confirms BUY or SELL by price-side + MA50-slope agreement.

This is the most source-faithful fail-closed mapping and prevents H4 from overriding an unresolved D1 major-trend transition.

## 15. Implementation status

**NOT IMPLEMENTED.**

No EA source, header/build identifier, runtime candidate, M17/M22/M23/M24 behavior, or broker behavior is changed by this decision.

Future implementation must first reconcile the canonical Core/F4 contracts and then patch M11/M15/M16 with a new unique build identifier and fresh compile/runtime evidence after the current P3 freeze is released.
