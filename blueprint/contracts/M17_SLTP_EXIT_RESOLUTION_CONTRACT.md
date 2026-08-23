# M17 SL / TP / Exit Resolution Contract

## Status
P0 Step 8B architecture decision is **APPROVED** and P0 Step 8C is **IMPLEMENTED AT ACTIVE-BLUEPRINT PATCH LEVEL**.

This contract separates:
1. **PDF_CORE** — rules explicitly supported by the user-supplied Oma Ally / BBMA PDFs;
2. **FORUM_SUPPORTED** — rules strongly supported by the BBMA Oma Ally ForexFactory community thread but not promoted to PDF-core authority;
3. **EA_SAFETY** — deterministic engineering/risk rules required for autonomous execution and explicitly labelled as project management logic rather than BBMA strategy semantics.

No FORUM_SUPPORTED or EA_SAFETY rule may be described in code, comments, documentation or UI as an explicit Oma Ally PDF rule.

---

## 1. Source precedence
When sources conflict, use this order:
1. user-supplied BBMA / Oma Ally PDF references;
2. approved BBMA source contracts already locked in the project;
3. ForexFactory BBMA Strategy by Oma Ally thread as supporting evidence only;
4. project engineering / risk controls.

A lower-priority source may not silently override a higher-priority BBMA rule.

---

## 2. Core exit principle
The project rejects a universal fixed-pip TP or fixed-pip SL as BBMA strategy semantics.

Approved principle:
> A BBMA trade targets the next structurally relevant BBMA destination, while loss control is based on structural invalidation plus an explicit protective hard-stop mechanism.

`MaxSLPips` and `MinRRRatio` remain rejection filters only. They do not manufacture the strategy SL or TP.

---

## 3. TP provenance and destination rules
### 3.1 Extreme / TPW context
Classification: **FORUM_SUPPORTED**.

After a valid Extreme + reversal/confirmation context, the first short BBMA destination may be the opposing MA5/10 area commonly described by the community as TPW. Raw Extreme is not a direct executable path under the current M15 contract, so this remains context only.

### 3.2 Confirmed H1 Re-Entry
Classification: **FORUM_SUPPORTED**.
- BUY destination = H1 TOP BB;
- SELL destination = H1 LOW BB.

### 3.3 REM
Classification: **FORUM_SUPPORTED + PROJECT MAPPING**.
REM identity:
- H4 Re-Entry;
- H1 Extreme;
- M15 confirmed MLV.

The H4 Re-Entry is the destination-producing component:
- BUY -> H4 TOP BB;
- SELL -> H4 LOW BB.

### 3.4 RRE
Classification: **FORUM_SUPPORTED + PROJECT MAPPING**.
RRE identity:
- D1 Re-Entry;
- H4 Re-Entry;
- H1 Extreme.

The highest-timeframe valid Re-Entry component is the destination source:
- BUY -> D1 TOP BB;
- SELL -> D1 LOW BB.

### 3.5 REE
Classification: **FORUM_SUPPORTED + PROJECT MAPPING**.
REE identity:
- D1 Re-Entry;
- H4 Extreme;
- H1 Extreme.

The D1 Re-Entry is the destination source:
- BUY -> D1 TOP BB;
- SELL -> D1 LOW BB.

### 3.6 Higher-timeframe continuation
Classification: **FORUM_SUPPORTED**.

The current project has no TP2/TP3. Step 8C therefore implements only the initially resolved single destination. Any later extension requires a separate lifecycle contract.

---

## 4. Protective SL rule
Classification: **EA_SAFETY informed by FORUM_SUPPORTED structural practice**.

The BBMA PDFs do not provide a complete universal deterministic hard-SL formula for every currently executable setup. Autonomous execution nevertheless requires a broker-side protective stop.

For Step 8C, the deterministic source-owned structural anchor is narrowed to the exact closed Re-Entry source candle selected by the approved mapping:
- BUY anchor = source-candle LOW;
- SELL anchor = source-candle HIGH.

The broker hard stop is placed one broker point beyond that wick:
- BUY -> `LOW - Point`;
- SELL -> `HIGH + Point`.

The one-point buffer is **EA_SAFETY** only and must not be presented as an Oma Ally PDF rule.

M17 does not scan an unrelated swing window. If the exact source candle cannot be resolved, the trade fails closed with `REJ_SLTP_UNRESOLVED`.

---

## 5. Dynamic BBMA invalidation / cut-loss
Classification: **FORUM_SUPPORTED**.

A live position may later become invalid before the protective hard SL when an opposite confirmed CSM/momentum condition with BB expansion invalidates the active BBMA thesis.

This is a trade-lifecycle exit, not the initial SL-price builder.

Ownership requirement remains:
- M17 resolves/validates initial SL/TP only;
- M23/M24 lifecycle ownership must be audited before dynamic invalidation-close logic is enabled;
- M16 signal invalidation must not directly close broker positions unless the blueprint explicitly routes that state to the lifecycle owner.

Step 8C does **not** enable this dynamic broker close path.

---

## 6. Deterministic TP resolver mapping
For current M15 executable decision types:

| Final decision type | Destination source | BUY TP | SELL TP |
|---|---|---|---|
| H1 RE_ENTRY | H1 Re-Entry | H1 TOP BB | H1 LOW BB |
| REM | H4 Re-Entry | H4 TOP BB | H4 LOW BB |
| RRE | D1 Re-Entry | D1 TOP BB | D1 LOW BB |
| REE | D1 Re-Entry | D1 TOP BB | D1 LOW BB |

Step 8C preserves the destination-producing source component in the decision payload and resolves the destination from the exact closed candle identified by that component.

M17 must not substitute another timeframe or manufacture a fixed-pip/RR-derived target.

---

## 7. Closed-candle identity guard
The source component is accepted only when:
- type = `SIGNAL_RE_ENTRY`;
- direction = final decision direction;
- timeframe exactly matches the mapping above;
- `CandleTime` resolves exactly on the same timeframe;
- resolved shift is `>= 1`.

A current-bar, stale, missing or mismatched source fails closed.

---

## 8. Geometry and rejection rules
After source resolution:
- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`;
- `MaxSLPips` may reject an excessively distant structural SL;
- `MinRRRatio` may reject a resolved pair with insufficient reward-to-risk;
- broker StopLevel/FreezeLevel rules remain direction-aware;
- invalid, stale, inverted or unresolved levels fail closed.

If the resolved BB destination is already crossed or lies on the wrong side of the execution reference at decision time, no replacement TP is created; resolution fails closed.

---

## 9. Ownership
### Upstream owners
M06/M07 provide MA/BB data.
M08/M09/M10/M12 provide their owned BBMA signals/states.
M13 assembles REM/RRE/REE.
M14 validates exact combination identity/components.
M15 selects the final executable decision and preserves the approved source component identity.
M16 revalidates owner-state validity/invalidation.

### M17 owns
- validation of the approved TP source mapping for the already-selected decision;
- exact closed-source-candle lookup;
- BB destination resolution on the mapped timeframe;
- structural hard-SL resolution from the exact source candle wick;
- broker execution-reference normalization;
- direction geometry validation;
- MaxSL/MinRR/broker rejection filters;
- fail-closed behavior when resolution is ambiguous or stale.

### M17 does not own
- BBMA detection;
- signal confirmation;
- combination invention;
- lifecycle close decisions after execution;
- trailing stop;
- TP2/TP3;
- arbitrary fixed-pip SL/TP manufacture.

---

## 10. Step 8C implementation record
Active-blueprint patch:
`blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`

Patch commit:
`2afeee76806f4b1c4e56f829fd7c8d42403a1450`

M17 implementation contract update commit:
`ce785c942eddcd3f6c3b131b6e961411ddde60e7`

Implemented behavior:
1. decision payload carries the exact destination-producing Re-Entry component/timeframe;
2. source candle identity must resolve exactly and be closed;
3. TP comes from the mapped source-timeframe TOP/LOW BB;
4. hard SL comes from the exact mapped Re-Entry source candle wick plus one broker point;
5. stale/crossed/missing/invalid payload remains fail-closed with `REJ_SLTP_UNRESOLVED`;
6. dynamic opposite-CSM lifecycle closure remains disabled pending M23/M24 audit.

This completes the Step 8B -> Step 8C architecture-to-implementation transition at patch level.

A new full-chain working-source SHA is not claimed until the entire ordered patch chain is exactly materialized and verified as one source.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
