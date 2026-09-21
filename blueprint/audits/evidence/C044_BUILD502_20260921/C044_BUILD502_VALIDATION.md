# C044 Build5.02 Current-Owner Validation — 2026-09-21

## Scope

This branch reapplies the verified C044 fail-frozen recovery fix from stale PR #213 onto current owner head `2ce35026bb9ec2b30762a18ae85de0bc37a69b37` after M19 and D1TPW merged.

Build identity:
- Version: `5.02`
- BuildTag: `V502_C044_FAIL_FROZEN_RECOVERY_20260921`
- SourceRev: `C044_FAIL_FROZEN_RECOVERY_221_20260921`

No BBMA Strategy-Core, owner table, entry, ranking, M15/M16, SL/TP, risk/MM, or execution-policy change was introduced.

## Rebase result

The old commit applied with only three source conflicts:
- version header;
- property/build/source-revision identity;
- F7 build telemetry identity.

The C044 behavior change applied without a functional conflict. Current-owner M19 and D1TPW code remains preserved.

The D1TPW static feature guard was decoupled from the global build identity so it continues validating D1TPW atomicity after later legitimate builds.

## Deterministic and static verification

- C044 failed-load static guard: PASS.
- C044 transactional recovery model: PASS.
- C044 generation atomicity model: PASS — normal 145 ops / frozen 85 ops.
- Existing F7 source guard: PASS.
- D1TPW checkpoint atomicity static guard: PASS.
- D1TPW generation model: PASS — 12 failure points.
- M19 owned-risk aggregation model/static guards: PASS.
- Protected-body comparison against current owner Build5.01: PASS.
- `git diff --check`: PASS.

Protected bodies remained exact for F7 identity, SL/TP resolution, C044 reducer/advance/latch/close/initialization/writers, recovery, M15/M16, risk preflight, and broker execution. Only `LoadC044Checkpoint()` and build identity changed semantically.

## Native compilation

- Canonical MetaEditor compile: 0 errors, 0 warnings (844 ms).
- Tester adapter compile: 0 errors, 0 warnings (837 ms).

## Isolated offline regression

Profile: GBPUSD M15, Every Tick, 2026-08-01 through 2026-09-01.

- build marker: 1;
- initialization PASS: 1;
- initialization failures: 0;
- deinitialization reason 0: 1;
- mismatched-chart errors: 0;
- total trades: 14 / baseline 14;
- C044-managed observations: 497;
- targetless recovery-frozen events: 0;
- targeted fatal runtime faults: 0.

All protected trace sequences were exact-equal to the current M17.499 baseline:

| Marker | Baseline | Build5.02 | Exact |
|---|---:|---:|---|
| M15_COUNTS | 523 | 523 | yes |
| M15_SELECT | 523 | 523 | yes |
| M16_PASS | 523 | 523 | yes |
| DECISION_FINAL | 523 | 523 | yes |
| PREFLIGHT_PASS | 325 | 325 | yes |
| EXEC | 14 | 14 | yes |
| MOMENTUM_HOLD | 3 | 3 | yes |
| REENTRY_REARM | 0 | 0 | yes |
| EXIT_LATCHED | 10 | 10 | yes |
| CLOSE_SUCCESS | 10 | 10 | yes |
| LIFECYCLE_FROZEN | 0 | 0 | yes |

Global Variables:
- pre-run SHA256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6` (240 bytes);
- restored SHA256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6` (240 bytes).

## Artifact hashes

- Canonical MQ4: `DC1BD92C1BE2CB165502D7B0B288D68DC1372B9E3AB7BA846D2CFF0B9172C24B` (430685 bytes)
- Canonical EX4: `2A0BB78EB16BA9E2CFE7A665CC197F3B6502DB7AF32244C390AA80A7081899B2` (557500 bytes)
- Tester MQ4: `3D012DCFF7FAC063E531BEF15F74E4877718827EF6382DDEE2B53112E0DFA09D` (420062 bytes)
- Tester EX4: `C76610DA3F86C0298A8BBD3B5800449EAB25EF0148EE657F1BBAC4CCFFDAF9D6` (558502 bytes)
- Smoke report: `F609C57B0E32F3C2F76778245D8F49A21D35AD0559D52773819DF960549E1B48` (14203 bytes)
- Tester log delta: `E277F351D437083392EF76548284B45EC7D95437A0021796E246692731F1678B` (4260361 bytes)

## Boundary

This is source/code and isolated offline tester evidence only. No primary MT4 restart, broker demo/live runtime, production activation, or live-readiness claim was performed. Those remain in final Q.
