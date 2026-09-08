# Post-Freeze Accelerated Upgrade Plan — 2026-09-09

Status: **AUTHORIZED / SCOPED DEVELOPMENT ONLY / NO CANONICAL PROMOTION YET**.

## Package A — Infrastructure / F7
Scope is restricted to confirmed engineering defects and provenance gaps:
- #127 deterministic `[F7-BUILD]` initialization identity;
- #132 EXEC telemetry uses the exact frozen new-ticket open time;
- #133 reconcile live v4.61 delta, retaining only authorized observability/lifecycle-housekeeping placement;
- #138 make C044 replay seed + lifecycle metadata one fail-closed committed generation.

No BBMA Strategy-Core detector, candidate, risk/MM, normal OrderSend or new lifecycle semantics may be added.

## Package B — D1 Strategy-Core
Implement only accepted contracts:
- M11 sole D1 major-trend owner from fully closed D1 `Close1`, `MA50_1`, `MA50_2`;
- M15 consumes M11 and applies D1 strategic direction before atomic surviving-direction selection;
- M16 verifies the frozen M11 identity/state and does not duplicate the MA50 formula.

Exact REM/RRE/REE signatures remain unchanged. `D1_TRANSITION` and `D1_OWNER_UNRESOLVED` block new entries only.

## Fast validation model
Each package receives targeted deterministic/static tests and native MetaEditor compile before integration. Multi-day natural-runtime waiting is deferred to the integrated candidate unless the event appears naturally in the background.

After both packages are stable, create one integrated candidate with a unique build identity, then run one combined static/compile/Strategy Tester/runtime/regression gate.

No merge or primary MT4 reload is authorized by this plan.
