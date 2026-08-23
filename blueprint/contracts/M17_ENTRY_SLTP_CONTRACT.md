# M17 Entry / Protective Payload Resolution & Validation Contract

## Status

**F7 CANONICAL CONTRACT — IMPLEMENTATION PENDING AFTER P3 RUNTIME FREEZE**

This contract supersedes the old Step 8C assumption that every executable Re-Entry-owned decision requires a positive static outer-BB TP.

The frozen P3 EA source still implements the historical Step 8C `SL + static TP` behavior and must not be changed until its pending runtime evidence closes. This file defines the **next implementation contract**, not a retroactive description of the frozen binary/source.

Canonical integration contract:
`blueprint/contracts/F7_REENTRY_LIFECYCLE_EXECUTION_CONTRACT.md`.

## Provenance boundary

Use these provenance classes explicitly:
- `STRATEGY_CORE` — accepted source-reconciled BBMA semantics;
- `EA_SAFETY` — deterministic broker/risk protection required for autonomous execution;
- `ENGINEERING` — persistence, normalization, recovery and broker mechanics.

The old universal Re-Entry outer-BB static TP mapping is **not Strategy Core under Path A** and must not be presented as `PDF_CORE`, `FORUM_SUPPORTED`, or Oma Ally authority.

The exact hard-stop formula remains **EA_SAFETY**:
- BUY -> exact owner Re-Entry source-candle LOW minus one broker point;
- SELL -> exact owner Re-Entry source-candle HIGH plus one broker point.

The primary source contains limited Extreme-context wick-stop guidance, but the exact owner-Re-Entry-candle mapping and one-point buffer remain project engineering protection, not a universal Core SL formula.

## 1. Covered executable decisions

All currently executable Strategy-Core decisions are Re-Entry-owned:
- standalone H1 `RE_ENTRY`;
- `REM`;
- `RRE`;
- `REE`.

Lifecycle owner mapping:
- standalone H1 Re-Entry -> H1 Re-Entry;
- REM -> H4 Re-Entry;
- RRE -> D1 Re-Entry;
- REE -> D1 Re-Entry.

The owner component identity must be preserved exactly from upstream validated components and must resolve to a fully closed source candle.

## 2. Future canonical payload

For these decisions M17 must produce/validate:

`EntryPrice = live execution reference`

`StopLoss = protective EA_SAFETY hard stop`

`TakeProfit = 0.0`

`ExitPolicy = REENTRY_LIFECYCLE`

`HasStaticTakeProfit = false`

`LifecycleOwnerType = SIGNAL_RE_ENTRY`

`LifecycleOwnerTimeframe = H1/H4/D1 according to the mapping above`

`OriginalOwnerReEntryCandleTime = exact validated owner Re-Entry confirmation candle`

No synthetic/static TP may be manufactured merely to satisfy legacy validators or RR calculation.

## 3. Source-component resolution

M17 must resolve the owner/protective source component by exact:
- component type = `SIGNAL_RE_ENTRY`;
- decision direction;
- expected owner timeframe;
- stored `CandleTime`;
- exact `iBarShift(..., exact=true)` mapping;
- resolved shift `>= 1`.

Missing/current-bar/stale/mismatched owner identity fails closed.

The old field names `HasSLTPSourceComponent` / `SLTPSourceComponent` may remain temporarily for compatibility, but their future semantic role must be narrowed to **protective/lifecycle owner component**, not proof of a static TP destination.

A future cleanup may rename them, but field renaming is not itself a Strategy-Core requirement.

## 4. Protective hard SL

For the exact closed owner Re-Entry candle:
- BUY anchor = candle LOW;
- SELL anchor = candle HIGH;
- BUY hard SL = `LOW - Point`;
- SELL hard SL = `HIGH + Point`.

Requirements:
- anchor must be valid and finite;
- `Point > 0`;
- BUY `SL < Entry`;
- SELL `SL > Entry`;
- positive SL distance;
- exact source candle must resolve; no arbitrary swing scan;
- no fixed-pip fallback;
- no RR-derived fallback.

`MaxSLPips` remains a project/EA-safety rejection cap only. It never manufactures a stop.

## 5. No-static-TP validation

For explicit `REENTRY_LIFECYCLE` payloads:
- `TakeProfit == 0.0` is valid and required;
- `HasStaticTakeProfit == false` is required;
- positive TP is an inconsistent payload and must fail closed;
- negative TP is invalid;
- no TP direction-geometry test is performed;
- no TP StopLevel/FreezeLevel test is performed;
- no destination-staleness/crossed-target test is performed;
- M17 must not call the historical outer-BB destination resolver for these decisions.

A zero TP **without** explicit lifecycle/no-static-TP identity remains unresolved/invalid and must not be silently accepted.

## 6. MinRR

`MinRRRatio` is **structurally inactive/bypassed** for standalone H1 Re-Entry, REM, RRE and REE under Path A.

Reason:
- there is no source-proven deterministic reward distance at entry;
- the historical RR value depended on the now-rejected universal static outer-BB TP;
- manufacturing an estimated lifecycle reward would create hidden non-Core strategy logic.

These trades must not emit `REJ_INVALID_RR` merely because static TP is absent.

Do not depend on the user manually setting `MinRRRatio=0`.

## 7. Broker geometry

Execution reference remains engineering-only:
- BUY = live ASK;
- SELL = live BID.

For lifecycle payloads validate only:
- valid direction;
- valid live EntryPrice;
- valid exact owner/protective source identity;
- non-zero protective SL;
- BUY `SL < Entry`;
- SELL `SL > Entry`;
- positive SL distance;
- broker normalization / SL StopLevel requirements;
- `MaxSLPips` safety cap.

FreezeLevel behavior remains broker-mechanics only and must not create a strategy target.

## 8. Lifecycle ownership handoff

M17 does not decide post-entry Momentum/no-Momentum exits.

It must hand downstream enough immutable identity for:
- original owner Re-Entry candle;
- owner timeframe;
- direction;
- cycle provenance;
- explicit lifecycle/no-static-TP exit policy.

Post-entry lifecycle belongs to M23/M24 and is governed by:
`blueprint/contracts/F7_REENTRY_LIFECYCLE_EXECUTION_CONTRACT.md`.

## 9. Fail-closed cases

M17 rejects when:
- owner Re-Entry component is absent/ambiguous;
- type/timeframe/direction does not match the approved owner mapping;
- owner candle does not resolve exactly to a closed bar;
- protective wick anchor is invalid;
- hard SL is on the wrong side / zero distance;
- broker SL geometry fails;
- `MaxSLPips` fails;
- exit-policy/static-TP fields contradict each other.

Use the closest existing rejection code during implementation or add a narrowly scoped payload-policy rejection enum if needed. Do not map targetless lifecycle mode to `REJ_INVALID_TP` merely because TP is zero by design.

## 10. Historical Step 8C behavior

Historical Step 8C mapped:
- H1 RE -> H1 outer BB TP;
- REM -> H4 outer BB TP;
- RRE/REE -> D1 outer BB TP.

F7 source reconciliation found that those outer-BB destinations are not sufficiently proven as universal Re-Entry broker TP rules under strict Path A. They remain historical implementation context only.

The owner **timeframe hierarchy** H1/H4/D1 remains valid for lifecycle ownership, but that does not revive the old static TP formula.

## 11. Ownership guard

M17 owns:
- execution-reference normalization;
- exact owner/protective component validation;
- protective hard-SL resolution;
- lifecycle/no-static-TP payload consistency;
- SL broker geometry;
- `MaxSLPips` safety rejection;
- structural MinRR bypass for lifecycle-managed current executable types.

M17 does not own:
- BBMA detection;
- Re-Entry confirmation;
- REM/RRE/REE assembly;
- final decision selection;
- lot sizing;
- portfolio risk;
- broker send;
- post-entry lifecycle reduction/close;
- trailing stop, breakeven, partial close, TP2 or TP3.

## 12. Implementation gate

No EA code change is authorized by this documentation update while P3 runtime evidence remains open.

After freeze closure, implementation must follow the canonical F7 contract, assign a new unique left-aligned build/header identifier, compile at 0 errors/0 warnings, and run fresh targetless-lifecycle runtime validation.
