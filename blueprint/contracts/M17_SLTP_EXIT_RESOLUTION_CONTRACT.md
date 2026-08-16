# M17 SL / TP / Exit Resolution Contract

## Status
P0 Step 8B — **APPROVED AT ARCHITECTURE CONTRACT LEVEL**.

This contract resolves the previously open BBMA SL/TP source gap by separating:

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

After a valid Extreme + reversal/confirmation context, the first short BBMA destination may be the opposing MA5/10 area commonly described by the community as TPW (Take Profit Wajib).

This is not a direct executable entry path under the current M15 contract because raw Extreme is not executable. It is therefore retained as lifecycle/context information only unless a future approved entry contract changes that.

### 3.2 Confirmed H1 Re-Entry
Classification: **FORUM_SUPPORTED**.

For an executable confirmed H1 Re-Entry:
- BUY destination = H1 TOP BB;
- SELL destination = H1 LOW BB.

The target level is resolved from closed-candle BB data belonging to the setup timeframe.

### 3.3 REM
Classification: **FORUM_SUPPORTED + PROJECT MAPPING**.

REM identity is:
- H4 Re-Entry;
- H1 Extreme;
- M15 confirmed MLV.

The H4 Re-Entry is the primary destination-producing component.

Therefore:
- REM BUY destination = H4 TOP BB;
- REM SELL destination = H4 LOW BB.

### 3.4 RRE
Classification: **FORUM_SUPPORTED + PROJECT MAPPING**.

RRE identity is:
- D1 Re-Entry;
- H4 Re-Entry;
- H1 Extreme.

The highest-timeframe valid Re-Entry component is the destination-producing component.

Therefore:
- RRE BUY destination = D1 TOP BB;
- RRE SELL destination = D1 LOW BB.

### 3.5 REE
Classification: **FORUM_SUPPORTED + PROJECT MAPPING**.

REE identity is:
- D1 Re-Entry;
- H4 Extreme;
- H1 Extreme.

The D1 Re-Entry is the destination-producing component.

Therefore:
- REE BUY destination = D1 TOP BB;
- REE SELL destination = D1 LOW BB.

### 3.6 Higher-timeframe continuation
Classification: **FORUM_SUPPORTED**.

If price reaches or breaks the current destination and a valid same-direction momentum/CSM continuation is confirmed with BB expansion, a position may be eligible for a future higher-timeframe destination extension.

However, the current project explicitly has **no TP2/TP3**. Therefore Step 8B does not introduce multi-target execution.

For the current architecture, the initially resolved destination remains the single TP unless a later separately approved lifecycle contract changes that rule.

---

## 4. Protective SL rule

Classification: **EA_SAFETY informed by FORUM_SUPPORTED structural practice**.

The BBMA PDFs do not provide a complete universal deterministic hard-SL formula for every currently executable setup. Autonomous execution nevertheless requires a broker-side protective stop.

Approved hard-stop rule:

### BUY
Place the hard SL below the most recent structurally relevant confirmed swing-low / lowest wick that belongs to the executable decision's source setup.

### SELL
Place the hard SL above the most recent structurally relevant confirmed swing-high / highest wick that belongs to the executable decision's source setup.

The structural anchor must be derived from closed candles only.

A small broker-normalized safety buffer may be added beyond the wick. The buffer is an **EA_SAFETY** implementation detail and must not be presented as an Oma Ally rule.

The structural anchor must come from the selected decision payload or from an explicitly owned upstream source component. M17 may validate and normalize the resolved level but may not invent an unrelated swing range.

If no unambiguous structural anchor is available, resolution fails closed with `REJ_SLTP_UNRESOLVED`.

---

## 5. Dynamic BBMA invalidation / cut-loss

Classification: **FORUM_SUPPORTED**.

In addition to the broker hard SL, a live position may become invalid before the hard stop when a confirmed opposite-direction CSM/momentum condition with BB expansion invalidates the active BBMA thesis.

This is a **trade-lifecycle exit**, not the initial hard-SL price builder.

Ownership requirement:
- M17 resolves/validates initial SL/TP only;
- M23/M24 lifecycle ownership must be audited before dynamic invalidation-close logic is enabled;
- M16 signal invalidation must not directly close broker positions unless the blueprint explicitly routes that state to the lifecycle owner.

No lifecycle module may recreate detector logic independently; it must consume owner-produced confirmed signal state.

---

## 6. Deterministic TP resolver mapping

For current M15 executable decision types:

| Final decision type | Destination source | BUY TP | SELL TP |
|---|---|---|---|
| H1 RE_ENTRY | H1 Re-Entry | H1 TOP BB | H1 LOW BB |
| REM | H4 Re-Entry | H4 TOP BB | H4 LOW BB |
| RRE | D1 Re-Entry | D1 TOP BB | D1 LOW BB |
| REE | D1 Re-Entry | D1 TOP BB | D1 LOW BB |

The destination must be resolved from the closed-candle snapshot corresponding to the source component validated by M14/M15/M16.

M17 must not recalculate a different signal or silently substitute another timeframe.

---

## 7. Geometry and rejection rules

After source resolution, M17 must retain the Step 8 validation rules:

- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`;
- `MaxSLPips` may reject an excessively distant structural SL;
- `MinRRRatio` may reject a resolved pair with insufficient reward-to-risk;
- broker StopLevel/FreezeLevel rules must remain direction-aware;
- invalid, stale, inverted or unresolved levels fail closed.

If the resolved BB destination is already crossed or lies on the wrong side of the execution reference at decision time, do not manufacture a replacement TP. Reject the decision as unresolved/stale for execution.

---

## 8. Ownership

### Upstream owners
M06/M07 provide MA/BB data.
M08/M09/M10/M12 provide their owned BBMA signals/states.
M13 assembles REM/RRE/REE.
M14 validates exact combination identity/components.
M15 selects the final executable decision.
M16 revalidates owner-state validity/invalidation.

### M17 owns
- selecting the approved TP destination mapping for the already-selected decision;
- resolving the TP level from the validated source snapshot;
- consuming a source-owned structural SL anchor;
- normalizing the broker execution reference;
- validating direction geometry;
- applying MaxSL/MinRR/broker rejection filters;
- failing closed when resolution is ambiguous.

### M17 does not own
- BBMA detection;
- signal confirmation;
- combination invention;
- lifecycle close decisions after execution;
- trailing stop;
- TP2/TP3;
- arbitrary fixed-pip SL/TP manufacture.

---

## 9. Required implementation follow-up

Step 8B is an architecture/source decision, not yet the final implementation patch.

Before execution can be certified, the blueprint implementation must be patched so that:

1. each executable decision carries the exact destination-producing source component/timeframe;
2. an unambiguous closed-candle structural SL anchor is available in the decision payload;
3. M17 resolves TP using the table in Section 6;
4. M17 resolves/validates the hard SL without inventing a new strategy signal;
5. stale/invalid destination and missing-anchor cases remain fail-closed;
6. M23/M24 lifecycle ownership is audited separately before opposite-CSM dynamic cut-loss is enabled.

This implementation follow-up is designated **P0 Step 8C**.

---

## 10. Project decision

The user approved the Step 8B research finding that:
- fixed-pip TP/SL must not be represented as BBMA Core;
- TP should follow BBMA destination structure;
- structural hard SL and dynamic opposite-signal invalidation must be explicitly provenance-labelled;
- community-supported rules must remain distinguishable from PDF-confirmed BBMA rules.

Accordingly, this contract is authoritative for the next M17 blueprint repair on `blueprint-dev`.
