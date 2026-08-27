# NMJE Dependency Hardening Audit — DEP-A05 M10 Direction/Momentum State

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Baseline verdict
M10 provides deterministic CSM/CSD/eCSD predicates and is acceptable as upstream BBMA direction/momentum evidence, but for N3 it should remain an owner-signal producer consumed by M08/M09/M12/M11J rather than becoming an independent NMJE scoring layer.

## Strengths observed
- CSM is closed-candle directional BB expansion + outside-BB close.
- CSD uses candle-body crossing of MA5, MA10 and Mid BB in the requested direction.
- eCSD uses candle-body crossing of MA5 and MA10.
- predicates are directional and reject invalid inputs.
- no RSI/MACD/ADX/session/news/score additions are present.

## Hardening findings before N3

### DEP-A05-F1 — M10 should expose canonical event identity/epoch where needed
The predicates currently return booleans. M12 and other owners infer current owner transitions from those booleans and current candle metadata.
Action: where N3 provenance requires it, expose/freeze event metadata (type, direction, timeframe, candle time) at the consuming canonical owner, not via a second NMJE detector.

### DEP-A05-F2 — Avoid duplicate Momentum semantics
M08 invalidation contains accepted Momentum logic equivalent to directional BB expansion/outside close, while M10 also owns DetectCSM(). This duplication can drift.
Action: audit whether M08 should consume the canonical M10/owner-facing Momentum predicate or whether both remain intentionally identical under one locked helper. N3 itself must not implement a third copy.

### DEP-A05-F3 — Event-vs-state distinction
CSM/CSD/eCSD are event predicates, not persistent strategic-owner states by themselves.
Action: NMJE should consume their effects through canonical lifecycle owners (M08/M09/M12/H4/D1 opportunity) or explicit event provenance; it must not treat an isolated boolean from a later scan as a permanent journey owner.

### DEP-A05-F4 — Same-candle precedence must remain deterministic
When multiple accepted predicates can be true on the same closed candle, downstream owner modules must have explicit precedence/ownership transfer. M12 already gives exact Type3/4 precursors priority over generic Type1.
Action: preserve owner-module precedence and reason-code it; NMJE must observe the resolved owner outcome rather than arbitrate between M10 events.

### DEP-A05-F5 — Replay equivalence
Because M10 is deterministic from closed OHLC/MA/BB data, replay risk is low, but owner modules that consume its events must prove the same event ordering after restart/missed processing.
Action: include CSM/eCSD/CSD event sequences in the deterministic replay library.

## N3 readiness
- Deterministic closed-candle predicates: PASS
- BBMA-pure: PASS
- Suitable as direct N3 scoring/filter layer: NO
- Suitable as canonical upstream event evidence: YES
- Duplicate semantic risk with M08 Momentum helper: HARDEN/AUDIT
- Replay risk at predicate level: LOW; owner-consumption replay still pending

## Timing
Documentation-only now. Resolve semantic dedup/single-owner behaviour before N3 enforcement, without changing BBMA definitions.

## Next
DEP-A06 — M27 orchestration/synchronization-barrier audit.
