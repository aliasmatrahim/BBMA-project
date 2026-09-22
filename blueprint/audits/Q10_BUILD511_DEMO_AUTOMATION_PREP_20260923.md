# Q10 Build 5.11 HFM Demo Automation Preparation

Date: 2026-09-23
Issue: #109
Owner baseline: `d1-owner-dev@78ddbd771853681de6628032701eea7231e05d61`
Frozen candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Result

**TOOLING READY / BROKER RUNTIME BLOCKED AT AUTH.**

The final integration candidate exists, so Issue #109 is now eligible for candidate-specific automation materialization. This change does not modify the BBMA EA source, Strategy Core, risk/MM, execution, lifecycle, recovery, dashboard or telemetry authority.

Current G40 does not contain attributable authenticated HFM demo-account evidence or a dedicated HFM demo terminal. Therefore no broker/demo acceptance stage was executed. Formal Q10 remains `BLOCKED / AUTH`.

## Candidate binding

The runner binds to the frozen final candidate:

- freeze commit: `78ddbd771853681de6628032701eea7231e05d61`;
- source-bearing commit: `c1da06ea15e6cc31d097765043fba26899090b7e`;
- canonical MQ4 SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`;
- native EX4 SHA-256: `CFF8DA584C91AE177CA26E1C47518AA585A67F0E16C99295F932670E8CDEC6E1`;
- approved final-integration settings SHA-256: `37BC585EB3AB5A73914FEC3C532023636D4FACCD7D3AAAF20B774269CF92DA70`.

The runner verifies:
- normalized current source hash;
- required Build 5.11 markers;
- exact source at the freeze commit;
- zero EA-source diff after the freeze commit.

Actual fail-closed rehearsal against the current worktree returned candidate identity **PASS**.

## Demo-only identity gate

Added `Q10_DEMO_IDENTITY_PROBE.mq4`:

- read-only;
- logs no account number;
- no credential handling;
- zero `OrderSend`, `OrderClose`, `OrderModify`, or `OrderDelete` call sites;
- emits demo/connected/trade-allowed/server/company/terminal-build only;
- native MetaEditor compile: **0 errors / 0 warnings**;
- MQ4 SHA-256: `97DA0293B048D6D1CADACDB0659A9A54CD61D4BA3062E7C0F4ADEDF116EB1DE6`;
- EX4 SHA-256: `C69F5AF156AE5A3E31379F6413123B38ECF6124B56E140FCEC0422403304F8CD`.

Probe launch generation forces `ExpertsTrades=false`.

Runtime stage generation remains blocked until probe evidence positively proves:
- `Demo=Y`;
- `Connected=Y`;
- server/company identifies HFM / HF Markets / HotForex.

A live-account marker produces `BLOCKED`, never PASS.

## Dedicated terminal / credentials policy

The runner:
- requires a dedicated `terminal.exe`;
- refuses the declared primary terminal path;
- requires the exact candidate EX4 and settings to reside under the dedicated terminal root;
- checks native EX4/settings hashes before runtime config generation;
- never writes `Login=` or `Password=` to generated configs;
- never creates accounts or bypasses broker/MT4 authentication.

Current environment scan found no HFM/HFMarkets/HotForex demo terminal. Primary MT4 PID 13064 was preserved.

## Current candidate-specific stage order

Formal AUTO order:

`AUTH -> R3 -> R4 -> R5 -> R6 -> COMPLETE`

R3-R6 remain based on the accepted broker-runtime matrix, rebound to current Build 5.11 semantics.

Current source bindings recorded in the matrix:
- M15 = sole processing clock;
- Strategy Core = closed candle;
- M12N = observation/read-only;
- N3 execution policy = NONE;
- TradeLock:
  - `LOCK_OFF=0`;
  - `LOCK_SAME_DIRECTION=1` allows same-direction additions on an already-owned pair and rejects opposite direction;
  - `LOCK_ONE_POSITION=2` blocks another exact-owned position on the pair.

No historical v4.59 source/build identity is accepted by the Q10 runner.

## Resumable state / formal promotion

State vocabulary is restricted to:
- `PASS`;
- `FAIL`;
- `INCOMPLETE`;
- `BLOCKED`.

The state file persists stage results/evidence references.

Formal stage selection rules:
- AUTH not PASS -> `BLOCKED / AUTH`;
- a stage FAIL blocks later formal promotion;
- first non-PASS stage is the next formal stage;
- COMPLETE requires all formal stages PASS.

Later-stage evidence can still be collected opportunistically, but formal progression cannot skip the predecessor order.

## Collector / analyzer

Collector:
- binds bundle to candidate source/build and demo-evidence hash;
- records raw-log hash;
- extracts stage-relevant markers;
- redacts `Account=<digits>` and `Login=<digits>` from committed excerpts.

Analyzer:
- uses explicit case assertions against the candidate-specific R3-R6 matrix;
- marker presence alone cannot create PASS;
- unknown case IDs fail closed;
- any FAIL makes the stage FAIL;
- missing mandatory PASS remains INCOMPLETE;
- conditional cases may remain INCOMPLETE only where the source matrix explicitly permits practical/safety incompleteness.

## Offline validation

- `py_compile`: PASS;
- Q10 targeted pytest: **11/11 PASS**;
- full repository pytest: **33/33 PASS**;
- `git diff --check`: PASS;
- EA source diff from frozen Build 5.11 candidate: **0**;
- probe native compile: **0E0W**.

Actual fail-closed rehearsal:

- candidate identity: **PASS**;
- demo evidence: **BLOCKED**;
- reason: `DEMO_LOG_MISSING`;
- next formal stage: `AUTH`.

This is the required behavior for the current G40 environment.

## Files

Tool:
`blueprint/tools/q10_demo_acceptance.py`

Candidate manifest:
`blueprint/runtime/q10_demo_acceptance/FINAL_BUILD511_CANDIDATE.json`

Stage matrix:
`blueprint/runtime/q10_demo_acceptance/FINAL_BUILD511_STAGE_MATRIX.json`

Read-only probe:
`blueprint/runtime/q10_demo_acceptance/Q10_DEMO_IDENTITY_PROBE.mq4`

Runbook:
`blueprint/runtime/q10_demo_acceptance/README.md`

Evidence:
`blueprint/audits/evidence/Q10_TOOLING_BUILD511_20260923/`

## Classification

**ENGINEERING IMPROVEMENT — Q10 automation tooling**
Candidate-specific demo acceptance tooling is ready and validated offline.

**NO FIX — EA / Strategy Core**
No EA source change is justified or performed.

**BLOCKED — HFM demo runtime acceptance**
No attributable authenticated HFM demo terminal/account evidence exists on G40.

## Genuine next gate

The next action requires a dedicated MT4 terminal already authenticated to an **HFM demo account**. Once that exists, the read-only probe can establish demo identity without credentials and Q10 can resume automatically from AUTH -> R3.

Do not use a live account.
