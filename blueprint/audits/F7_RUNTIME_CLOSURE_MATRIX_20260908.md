# F7 Runtime Closure Matrix — 2026-09-08

Status: **STATIC PATHS PRESENT / PARTIAL RUNTIME EVIDENCE / NOT FULLY RUNTIME VERIFIED**.

| F7 path | Canonical v4.61 static state | Runtime evidence currently attributable | Status |
| --- | --- | --- | --- |
| initial owner Re-Entry -> `MOMENTUM_PENDING` | implemented | historical execution/recovery observations exist but build attribution is qualified by #127/#133 | PARTIAL |
| same-direction CSM -> `WAIT_NEXT_REENTRY` | `DetectCSM` -> checkpoint -> `MOMENTUM_HOLD` telemetry | none harvested | PENDING |
| later same-direction owner Re-Entry -> re-arm | same canonical M12 replay state; owner/epoch reset -> `MOMENTUM_PENDING`; `REENTRY_REARM` | none harvested | PENDING |
| opposite CSM while pending | canonical M10 `DetectCSM` opposite direction -> `C044_EXIT_OPPOSITE_CSM` latch | none harvested | PENDING |
| failed Momentum / reverse confirmation | CSM precedence first, then reverse-colour confirmation -> `C044_EXIT_FAILED_MOMENTUM` | one `EXIT_LATCHED` + matching `CLOSE_SUCCESS` observed | OBSERVED / provenance-limited |
| opposite reversal-confirmed owner-TF Extreme | canonical M08 replay lifecycle; checked before ordinary lifecycle state -> `C044_EXIT_CYCLE_SUPERSEDED` | none harvested | PENDING |
| chronological missed-candle replay | oldest-to-newest exact owner-TF history; freezes on missing/invalid cursor | `RECOVERY_RESTORED` observed twice; exact full restart matrix not complete | PARTIAL |
| M20 emergency precedence | `ManagePortfolio()` before `ManagePositions()`; emergency close branch before F7 normal close | no focused F7+M20 runtime case harvested | PENDING |
| M23 full close / no partial-BE-trailing | F7 latched close is full `OrderClose`; normal unsupported management absent | failed-Momentum full-close observation exists | PARTIAL |
| duplicate-close prevention | already-closed ticket clears checkpoint; registry compaction removes closed row | no focused same-ticket repeated-latch/restart runtime proof | PENDING |
| torn checkpoint/replay write | current save protocol is not generation-atomic | no runtime occurrence required to establish static defect | **CONFIRMED BUG — separate audit** |

## Static ownership findings
- F7 does not reimplement Extreme/Re-Entry formulas; replay calls canonical M08/M12 state machines.
- canonical CSM classification has precedence over weaker reverse-colour confirmation.
- opposite mature Extreme supersession is evaluated before ordinary hold/pending state handling.
- F7 close authority remains M23-side and M20 emergency handling remains earlier in `ManagePositions()`.

## New blocker found by static audit
`SaveC044ReplaySeed()` publishes `V=1` before overwriting replay payload, and C044 lifecycle metadata is also overwritten in place without a cross-payload generation commit. An interruption can leave a mixed previous/current checkpoint that still has every expected key. See `F7_C044_RESTART_ATOMICITY_AUDIT_20260908.md`.

Therefore a future F7 runtime PASS must not be promoted to restart-complete until this persistence atomicity defect is fixed in a new post-freeze build and torn-write regression passes.

## Boundary
No new BBMA semantics are inferred by this matrix. Missing runtime rows remain PENDING rather than being synthesized from static code.
