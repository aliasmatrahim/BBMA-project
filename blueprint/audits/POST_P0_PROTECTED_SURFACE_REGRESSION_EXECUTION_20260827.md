# Post-P0 Protected-Surface Regression Execution — 2026-08-27

Status: **IP-05 STATIC PROTECTED-SURFACE PASS / FULL MATRIX INCOMPLETE UNTIL IP-07 COMPILE**  
Integration branch: `p0-v459-postpass-integration-20260827`  
Canonical base: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`  
Source-bearing integration commit: `aa74898ead8725f78141924f8bcb1725f0c113ca`  
Integrated source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`  
Build: `Version 4.5.9 - P0 Execution Identity Persistence Fix` / property `4.59`

## 1. Predecessor gate

P0 authenticated HFM demo runtime predecessor is PASS. Repository evidence:

`blueprint/audits/P0_EXEC_ID_RUNTIME_PASS_RECORD_20260827.md`

Observed qualifying ticket `484701907` (`CHFJPY SELL`) reported fresh `Persist=PASS Local=Y`, survived a full same-installation MT4/EA restart as `REC_IDENTITY_HASH_ONLY`, and no second live ticket for execution hash `7AADB1796BF36399` was observed.

## 2. Integration-lineage check

Fresh canonical base remained exactly `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`; no intervening canonical commit had to be reconciled.

A fresh branch was created from that exact base and only the reviewed P0 source blob was applied. Compare `5a1e778... -> aa74898...` shows one changed file only:

- `blueprint/source/BBMA_EA.mq4`
- additions: 240
- deletions: 34
- total changed lines: 274

No P0 one-shot workflow, trigger token, patch helper or temporary validation plumbing was imported.

## 3. Diff-hunk classification

All source diff hunks fall into approved P0 scope:

| Area | Classification | Result |
|---|---|---|
| Header / property version v4.58 -> v4.59 | `P0_REQUIRED` | PASS |
| Durable terminal execution-identity helpers | `P0_REQUIRED` | PASS |
| `RebuildExecutionHistory()` local-first identity | `P0_REQUIRED` | PASS |
| `CreateOrderComment()` compact `BBMA|H:<16hex>` | `P0_REQUIRED` | PASS |
| Error 128 retryable -> ambiguous | `P0_REQUIRED` | PASS |
| `FindExistingExecutionTicket()` local-first lookup | `P0_REQUIRED` | PASS |
| `ProcessEntry()` durable write/verification + EXEC_ID telemetry | `P0_REQUIRED` | PASS |
| `RecoverExistingOrders()` local-first recovery / hash-only state | `P0_REQUIRED` | PASS |
| Dashboard/init build identity v4.59 | `P0_REQUIRED` | PASS |
| Any strategy/MM/risk/lifecycle/input change outside P0 | `UNAUTHORIZED` | **NONE FOUND** |

## 4. Protected-surface results

The prepared matrix `POST_P0_PROTECTED_SURFACE_REGRESSION_MATRIX_20260826.md` was applied to the exact integrated candidate.

| ID | Result | Evidence summary |
|---|---|---|
| PS-01 M06-M12 detectors | PASS | no diff hunk in detector/state semantics |
| PS-02 M12N/NMJE | PASS | no diff; no execution authority introduced |
| PS-03 M13 collector | PASS | no diff |
| PS-04 M14 validator | PASS | no diff |
| PS-05 M15 final authority | PASS | no diff/bypass introduced |
| PS-06 M16 invalidation | PASS | no diff |
| PS-07 D1 strategic owner | PASS | no diff |
| PS-08 D1 Opportunity | PASS | no family/direction/eligibility diff; persistence transport only downstream |
| PS-09 RE/REM/RRE/REE | PASS | no family/composition/priority diff |
| PS-10 M17 SL/TP | PASS | no SL anchor, spread buffer, TP mapping, MinRR or targetless-classification strategy drift |
| PS-11 M21 MM | PASS | no lot formula/cap/MM-mode diff |
| PS-12 M19 risk | PASS | no risk admission diff |
| PS-13 M20 portfolio/emergency | PASS | no portfolio/emergency semantic diff |
| PS-14 M22 normal payload | PASS | payload geometry unchanged; compact comment/identity handling only |
| PS-15 M22 retry policy | PASS | error 128 removed from retryable set and added to ambiguous set |
| PS-16 M22 duplicate protection | PASS | local-first persisted-ticket lookup present; predecessor runtime showed no duplicate |
| PS-17 M23 lifecycle semantics | PASS | no lifecycle event/close semantic diff; default gates remain OFF |
| PS-18 M24 recovery ownership | PASS | local durable identity first; broker comment fallback; no strategy authority fabricated |
| PS-19 C044 gate | PASS | `EnableC044Lifecycle=false` |
| PS-20 D1TPW gate | PASS | `EnableD1TPWLifecycle=false` |
| PS-21 N3 firewall | PASS | no N3 source diff or execution-authority activation in P0 delta |
| PS-22 Inputs/defaults | PASS | no unrelated input/default diff |
| PS-23 Magic identity | PASS | no StrategyID/InstanceID/pair magic formula diff |
| PS-24 Closed-candle timing | PASS | no processing-clock/current-bar shortcut diff |
| PS-25 Trade registry | PASS | successful-order ownership remains; identity state is additive/fail-closed |
| PS-26 Broker comment authority | PASS | broker comment no longer sole authority |
| PS-27 Legacy compatibility | PASS | full-comment parser remains fallback/migration support; validated local identity is preferred |
| PS-28 Build identity | PASS (source/runtime strings) | header/property/dashboard/init are synchronized to v4.59 |
| PS-29 Compile cleanliness | **PENDING IP-07** | requires official MetaEditor compile of exact integrated source |
| PS-30 Runtime attribution / EX4 identity | **PENDING IP-07** | requires exact integrated compile log + EX4 SHA-256 |

## 5. Focused execution-path review

Required chain:

`M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22 -> M24`, with M23 lifecycle sanity.

Static result:

1. M15 decision authority/timing: unchanged.
2. M16 invalidation: unchanged.
3. M17 SL/TP geometry/classification: unchanged.
4. M21 lot sizing: unchanged.
5. M19 trade-risk admission: unchanged.
6. M20 portfolio/emergency authority: unchanged.
7. M22 order payload remains decision-owned; P0 changes only compact comment, durable identity, duplicate lookup and ambiguous-send handling.
8. M24 recovery/history becomes local-identity-first without adding strategy authority.
9. M23 lifecycle semantics are untouched and both staged gates remain OFF.

No discrepancy appears before the allowed M22/M24 P0 identity boundary.

## 6. Identity-specific checks

| Check | Result |
|---|---|
| PR-ID-01 compact comment | PASS |
| PR-ID-02 durable local write + flush | PASS |
| PR-ID-03 ticket/magic/open-time/direction + reverse hash cross-validation | PASS |
| PR-ID-04 local-first duplicate lookup | PASS |
| PR-ID-05 local-first recovery/history | PASS |
| PR-ID-06 blank/mutated broker-comment tolerance | PASS by architecture; runtime predecessor also demonstrated durable recovery |
| PR-ID-07 no false normal state when durable write fails | PASS |
| PR-ID-08 error 128 ambiguous/fail-closed | PASS |

## 7. Static IP-05 verdict

**PASS — no unauthorized protected-surface semantic drift found.**

This permits IP-06 exact identity capture and IP-07 official compile.

The complete PS-01..PS-30 matrix is intentionally **not yet declared fully closed** because PS-29 and PS-30 are compile/artifact gates. They must be completed only with official MetaEditor 0E0W evidence and exact EX4 attribution from IP-07.

No update to `d1-owner-dev`, no merge to `main`, no lifecycle gate activation and no Issue #94 closure is authorized by this static report.
