# CORE-V2-F4 — Higher-Timeframe Context for Standalone H1 Re-Entry

Date: 2026-08-22  
Reconciled: 2026-08-24  
Status: **REOPENED BY STRONGER HOME-COURSE EVIDENCE / D1 STRATEGIC GATE ADDED AT SPECIFICATION LEVEL / IMPLEMENTATION PENDING**  
Branch: `blueprint-dev`

## Reconciliation notice
The original 2026-08-22 F4 decision correctly established H4 as the **immediate structural/setup parent** for standalone H1 Re-Entry, but its statement that D1 was only broader context and not a universal hard gate is superseded by stronger Home Course + primary-PDF reconciliation.

The canonical hierarchy is now:

`D1 MAJOR-TREND STRATEGIC OWNER -> H4 IMMEDIATE STRUCTURAL/SETUP PARENT -> H1 RE-ENTRY -> M15/lower-TF completion where applicable`

The H4 owner model remains valid. What changes is that **H4 is no longer sufficient by itself to authorize a new standalone H1 trade** when D1 is opposite, transitional or unresolved.

Decision provenance:
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`;
- `blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`.

---

## 1. D1 strategic owner — mandatory new-entry gate
For new standalone H1 Re-Entry execution, D1 is the strategic directional authority.

Accepted D1 states are produced only from fully closed D1 data:
- BUY confirmed: `Close1 > MA50_1` AND `MA50_1 > MA50_2`;
- SELL confirmed: `Close1 < MA50_1` AND `MA50_1 < MA50_2`;
- otherwise-valid disagreement/flat/equality = `D1_TRANSITION`;
- missing/invalid history = `D1_OWNER_UNRESOLVED`.

Execution meaning:
- confirmed BUY permits only BUY-direction candidates, subject to H4/H1 and all other gates;
- confirmed SELL permits only SELL-direction candidates;
- `D1_TRANSITION` blocks all new strategy entries;
- `D1_OWNER_UNRESOLVED` blocks all new strategy entries.

The previous confirmed D1 direction may remain as historical/diagnostic provenance during transition but is not current execution authority.

Evidence classification:
- D1/MA50 major-trend authority = **DIRECT SOURCE / STRONGLY CORROBORATED**;
- price-side + MA50-slope agreement = **DIRECT PRIMARY-PDF RULE**;
- explicit transition/unresolved states + fail-closed blocking = **MINIMAL DETERMINISTIC PROJECT MAPPING**.

---

## 2. H4 remains the immediate structural/setup parent
For standalone H1 Re-Entry, H4 remains the immediate parent/context owner in the approved intraday chain.

Accepted principle:

`D1 strategic direction -> H4 BBMA structural owner -> H1 Re-Entry`

Operational meaning:
- H1 Re-Entry is not autonomous from H4;
- H4 must provide a compatible authoritative BBMA directional/cycle owner;
- H4 does not replace or override D1 strategic authority;
- D1 is not an `OR` fallback for missing H4 ownership;
- this decision does not convert standalone H1 Re-Entry into a REM/RRE/REE combination.

---

## 3. H4 compatibility = authoritative BBMA cycle/directional state
H4 compatibility is based on an **active authoritative BBMA directional/cycle owner**, not one current H4 candle or a generic indicator snapshot.

Accepted interpretation:
- H4 context persists structurally across a valid same-direction BBMA cycle;
- raw H4 Extreme alone is not directional authority;
- raw H4 MHV/MLV alone is not directional authority;
- Mid-BB/MA50 position is not by itself the H4 owner;
- ordinary neutral H4 candles do not automatically erase a surviving owner.

Evidence classification: **SOURCE-INFERRED / STRONG HINT** built on direct MTF principles and source separation between setup, direction, Re-Entry and Momentum stages.

---

## 4. Inherited H4 directional cycle owner
Canonical H4 lifecycle:

`H4 DIRECTION SIGNAL -> H4 RE-ENTRY -> H4 CSM/MOMENTUM -> FURTHER SAME-CYCLE RE-ENTRY`

Rules:
- a source-valid H4 direction signal establishes/advances ownership;
- later same-direction Re-Entry and CSM/Momentum inherit/continue the same owner;
- same-direction continuation does not require a fresh eCSD/CSD on every H4 candle;
- raw Extreme/MHV remain pre-direction context only;
- owner age alone does not end ownership.

---

## 5. Valid H4 eCSD may establish H4 ownership
A source-valid H4 `eCSD` is sufficient to establish H4 directional ownership for same-direction standalone H1 parent compatibility.

Later same-direction `CSD`, Re-Entry and `CSM/Momentum` strengthen/advance/inherit the same owner but are not prerequisites merely to establish owner direction.

H4 eCSD remains directional context only; it does not itself become a direct entry.

---

## 6. Atomic opposite-direction H4 handover
Canonical transition:

`OLD H4 OWNER -> VALID OPPOSITE H4 eCSD/CSD/CSM -> OLD OWNER SUPERSEDED -> NEW H4 OWNER ACTIVE`

Rules:
- opposite source-valid eCSD/CSD/CSM may atomically hand over H4 directional ownership at the closed-candle transition;
- simultaneous authoritative H4 BUY and SELL owners are not allowed;
- ordinary opposite-colour candles, raw Extreme, raw MHV/MLV or MA touches do not create the handover by themselves.

This H4 handover does **not** bypass the D1 strategic gate. A newly opposite H4 owner remains non-executable if D1 is still confirmed in the other direction or is transitional/unresolved.

---

## 7. Neutral candle versus true H4 NO_OWNER
Accepted distinction:

`NEUTRAL H4 CANDLE + VALID INHERITED OWNER -> OWNER REMAINS`

but

`TRUE H4 NO_OWNER -> STANDALONE H1 RE-ENTRY BLOCKED`

No silent fallback is allowed from H4 `NO_OWNER` to:
- D1 alone;
- H4 MA50/Mid BB;
- candle colour;
- current price position;
- absence of an opposite signal.

The final standalone H1 entry therefore requires **both**:
1. confirmed same-direction D1 strategic owner; and
2. active same-direction H4 structural owner.

---

## 8. Structural H4 owner lifetime
H4 owner lifetime remains purely structural.

There is no generic:
- 3/5/10-candle expiry;
- 24-hour expiry;
- daily/session reset;
- forced periodic eCSD/CSD refresh.

Owner age may be logged for diagnostics but cannot become a BBMA validity filter.

---

## 9. H4 restart/recovery
The prior verified-checkpoint + deterministic closed-H4 replay contract remains unchanged as **EA engineering policy**:

`RESTART -> VERIFY CHECKPOINT -> REPLAY CLOSED H4 CHRONOLOGICALLY -> RECONSTRUCT OWNER`

If checkpoint/history cannot prove H4 ownership, resolve to `H4 NO_OWNER` and block standalone H1 execution.

The recovered H4 owner must equal the owner the same state machine would have produced without restart.

D1 recovery is separate: current D1 strategic owner is deterministically rebuilt from the latest two closed D1 MA50 observations and latest closed D1 close. D1 transition/unresolved remains blocked.

---

## 10. Consolidated standalone H1 Re-Entry contract
A standalone H1 Re-Entry is eligible for final new-entry consideration only when:
1. D1 strategic owner is confirmed BUY or SELL;
2. D1 direction equals the H1 Re-Entry direction;
3. H4 has an active authoritative directional/cycle owner;
4. H4 owner direction equals the H1 Re-Entry direction;
5. H4 owner has not been structurally superseded;
6. H4 is not `NO_OWNER` / recovery-unresolved;
7. D1 is not `D1_TRANSITION` / `D1_OWNER_UNRESOLVED`;
8. the H1 Re-Entry itself is source-valid under M12;
9. all downstream M15/M16/risk/execution gates subsequently pass.

There is:
- no H1-only bypass;
- no `H4 OR D1` rule;
- no H4-only execution against D1;
- no D1-only execution when H4 has no owner;
- no EMA50-only H4 substitute;
- no raw Extreme/MHV-only H4 owner;
- no simultaneous H4 BUY/SELL owners;
- no generic fixed H4 owner expiry;
- no freeze of an old D1 owner as execution authority during D1 transition.

---

## 11. Relationship to REM/RRE/REE
This F4 reconciliation does not modify exact component signatures:
- REM remains `H4 Re-Entry + H1 Extreme + M15 MHV/MLV`;
- RRE remains `D1 Re-Entry + H4 Re-Entry + H1 Extreme`;
- REE remains `D1 Re-Entry + H4 Extreme + H1 Extreme`.

D1 major-trend ownership is a separate strategic execution gate, not a fourth REM component.

A D1 Re-Entry component in RRE/REE does not silently substitute for D1 MA50 strategic-owner confirmation.

---

## 12. Existing live positions
`D1_TRANSITION` is not an ordinary broker-close rule.

This F4 decision governs **new-entry context** only. Existing live-position closure remains owned by the separately approved lifecycle/SL/emergency contracts.

---

## Rejected alternatives
- H1-only execution with no higher-timeframe context;
- H4-only authorization against a confirmed opposite D1 owner;
- retaining old D1 BUY/SELL as executable authority during `D1_TRANSITION`;
- immediate D1 direction flip from price-side cross alone while MA50 slope still disagrees;
- `H4 OR D1` alignment;
- D1-only fallback when H4 is `NO_OWNER`;
- H4 EMA50-only/current-candle-only direction;
- raw H4 Extreme/MHV ownership;
- simultaneous H4 BUY and SELL owners;
- fixed H4 owner expiry;
- fixed multi-day D1 confirmation delay;
- trusting persisted H4 owner blindly after restart;
- inferring either H4 or D1 direction from an unsupported current snapshot.

## Implementation guard
This reconciled record is the canonical F4 specification.

The active EA still reflects the older H4-only standalone-H1 execution gate, so F4 is **not implementation-complete relative to this stronger source reconciliation**.

No EA source change is authorized by this documentation update while the current P3 runtime candidate remains frozen. Future implementation must update the appropriate M11/M15/M16 interfaces, use a new unique left-aligned build identifier, and receive fresh compile/runtime verification.
