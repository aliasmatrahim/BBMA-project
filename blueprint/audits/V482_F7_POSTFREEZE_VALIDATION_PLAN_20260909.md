# Build 4.82 F7 Post-Freeze Validation Plan — 2026-09-09

Status: **SCOPED / SOURCE CHANGE LOCAL-PENDING / NO RUNTIME CLAIM**.

Refs: #127, #132, #133, #138.

## Required source corrections before commit
1. `[F7-BUILD]` must emit before `InitializeEA()` so recovery/startup telemetry cannot precede build identity.
2. C044 committed-generation save must invalidate the old commit first, clear old lifecycle/replay payload, verify clearing, write one new generation, verify every required payload key, then publish the commit marker last.
3. Legacy V1 replay/checkpoint must not be silently accepted as generation-atomic evidence; unprovable recovery fails frozen.

## Deterministic gates
- every interrupted write prefix with a prior complete generation must load INVALID/fail-frozen;
- only the final committed generation may load valid;
- mixed old/new generation must never load valid;
- repeated load of one committed generation must be equivalent;
- missing/corrupt generation or payload must fail frozen;
- F7 hold/re-arm/failed-Momentum/opposite-CSM/opposite-Extreme semantics unchanged.

## Architecture/static gates
- M15 remains sole final new-entry authority;
- M20 lifecycle precedence remains before M23 and strategy scan;
- M22 remains normal OrderSend owner;
- M23 remains normal full-close owner;
- F7 telemetry remains observability only;
- prospective telemetry emits only after successful exact-ticket execution;
- EXEC OrderOpen telemetry uses frozen exact-ticket `info.open_time`;
- NMJE/C10 gain no execution authority;
- current M11 -> M15 -> M16 D1 owner implementation is inherited unchanged.

## Compile/runtime boundary
Native MetaEditor 0 errors / 0 warnings is mandatory before Package A is called stable. Physical/live runtime remains NOT RUNTIME VERIFIED until the later combined candidate gate. No primary MT4 reload is authorized by this plan.