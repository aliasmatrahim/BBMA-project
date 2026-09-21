# D1TPW Build5.01 Validation — 2026-09-21

## Scope

PR #220 rebases the D1TPW generation-atomic lifecycle checkpoint persistence onto owner head after M19 merge. Build identity is V5.01 / source revision D1TPW_CHECKPOINT_ATOMICITY_220_20260921. No strategy/filter changes and no production activation.

## Verification

- D1TPW generation model: PASS (failure_points=12).
- Static identity/atomicity test: PASS.
- Native canonical compile: 0 errors, 0 warnings (956 ms).
- Tester adapter compile: 0 errors, 0 warnings (989 ms).
- Isolated GBPUSD M15 Every-Tick smoke: completed; report generated.
- Runtime fatal/array/zero-divide markers: 0.
- D1TPW managed runtime events: 0 (gate remains OFF).
- Global Variables pre-run SHA256: DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6 (240 bytes).
- Global Variables restored SHA256: DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6 (240 bytes).

## Protected comparator

Against the current M17.499 GBPUSD M15 baseline, all protected marker counts were exact-equal:

| Marker | Baseline | D1TPW | Equal |
|---|---:|---:|---|
| M15_COUNTS | 523 | 523 | yes |
| M15_SELECT | 523 | 523 | yes |
| M16_PASS | 523 | 523 | yes |
| DECISION_FINAL | 523 | 523 | yes |
| PREFLIGHT_PASS | 325 | 325 | yes |
| EXEC | 14 | 14 | yes |
| MOMENTUM_HOLD | 3 | 3 | yes |
| EXIT_LATCHED | 10 | 10 | yes |
| CLOSE_SUCCESS | 10 | 10 | yes |

## Artifact hashes

- Canonical MQ4: 65B24166B6D4E72E32B4B10F53DF844FE9D53DF1FA9412B12532F3A3E39C9D61 (430589 bytes)
- Canonical EX4: 1DE6B4A35359DBECD4E50676A5BED9AE676757039473FEAD8C96E513CD1E8650 (556554 bytes)
- Tester adapter MQ4: A2C3327F0C98F58679714819067D2C5CAE3115DD4867CEAD2A731A99268C8B91 (419971 bytes)
- Tester adapter EX4: 4E4B8C949FB2CBFD5BBB20E8C55EB64C91703798EE05BC54692848E12E4D1D44 (557676 bytes)
- Smoke report: 9711574F2B964331A86C588A36680E4CD5FDC7338B9D9FFDE6AE01F2DB792A21 (14206 bytes)
- Tester log delta: E23F2DBAB639397B348BB3BA4707A77DE6F05413CF6FF239A1F89A541770C423 (4278948 bytes)

## Gate

This evidence validates code and isolated tester behavior only. Production primary MT4, live broker, and strategy activation remain untouched.
