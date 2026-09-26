# NMJE V2 Build 5.19 — Current-Candidate Lifecycle Hardening + Offline Discovery — 2026-09-26

Status: **IMPLEMENTED / NATIVE COMPILE PASS / PYTHON PASS / HOT-WINDOW A-B PASS / NATURAL ACTIONABLE DIVERGENCE NOT OBSERVED**

Issue: #101
Parent committed checkpoint: `5c0ddda9524093e015a084aec76e9c86f2c0e28e`

## Discovery findings

Build 5.17 first exposed stale N3 selection rows where both logged identities had already executed.

Build 5.18 excluded consumed candidates from the N3 arbitration set, but GBPUSD August 2026 showed a second lifecycle defect: the legacy canonical baseline had already executed, while N3 could still bypass that consumed baseline and select another unconsumed candidate. This changed one Re-Entry open from 12:00 OFF to 09:15 ON while retaining the same eventual ordered DecisionID set.

Classification: **CONFIRMED BUG — N3 MUST NOT BYPASS LEGACY DUPLICATE/LIFECYCLE OWNERSHIP**.

## Build 5.19 minimal fix

Build 5.19 adds `nmjeBaselineConsumed` and permits N3 arbitration only when:
- the legacy canonical baseline is itself unconsumed;
- at least two otherwise valid same-direction N3 candidates are unconsumed;
- all existing positive V1/M5 policy conditions hold.

If the legacy baseline is consumed, the existing M15 -> preflight duplicate/lifecycle path remains authoritative. NMJE does not rescue another candidate.

No detector, Core semantic, M16, risk/MM, SL/TP or broker-execution ownership changes.

## Build identity and compile

- Build `5.19`
- Tag `V519_NMJE_CURRENT_CANDIDATE_LIFECYCLE_20260926`
- Source rev `NMJE_CURRENT_CANDIDATE_LIFECYCLE_001_20260926`
- MQ4 SHA-256 `7AE7FA680132F42A4D4FDF13451FEA2CF704A26FE5FB616ACCA22A3C64F265C4`
- Native EX4 SHA-256 `246A2D30B5DBF793D536C5434DA457DF275829DC026E871B294D354DB7503EED`
- Harness EX4 SHA-256 `22F1525B04DB37B2B5BB6594ADED4E1F2041EB87F0AE299FD8C1B33EA8FB049E`
- Native production compile: **0 errors / 0 warnings**
- Native harness compile: **0 errors / 0 warnings**
- Python suite: **72/72 PASS**

## Recovered exact hot-window regression

EURUSD Feb 2026:
- executions: 20
- N3 changes: 0
- trace exact to stored OFF: True

EURUSD Jan 2026:
- executions: 34
- N3 changes: 0
- trace exact to stored OFF: True

GBPUSD Aug 2026:
- executions: 14
- N3 changes: 0
- trace exact to stored OFF: True

EURUSD Jul 2026 exact Build 5.19 A/B:
- OFF executions: 31
- ON executions: 31
- ON N3 changes: 0
- trace exact: True

All four are clean tester-complete sessions with zero targeted fatal runtime and zero duplicate DecisionID/ticket.

## Closure

All previously observed N3 hot windows now preserve the legacy execution trace and produce zero N3 winner-change after current-candidate lifecycle hardening.

Therefore the earlier Build 5.17/5.18 winner-change rows are classified as lifecycle artifacts, not acceptable proof of active policy quality.

Offline multi-pair/multi-period discovery is **PASS for lifecycle safety and A/B non-regression**.

A natural actionable N3 divergence among two or more current, unconsumed candidates was **NOT OBSERVED** in the bounded hot-window corpus. No synthetic substitute is created.

This remains separate from broker-connected demo-forward/restart/provenance/order-log validation.
