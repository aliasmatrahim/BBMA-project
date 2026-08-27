# Development, Verification & Release History

## Purpose

This document is the dedicated engineering-history section for the BBMA EA project.

It is intentionally separate from the strategy-rule documentation. The BBMA/Oma Ally strategy source of truth, trading rules and module contracts remain in their own strategy/reference/contract documents. This file records **how the EA was engineered, corrected, verified, compiled, runtime-tested, integrated and released**.

Use this section for developer/audit traceability, not as a substitute for BBMA trading-rule authority.

---

## 1. What is recorded here

Engineering work is classified into the following categories:

1. **Logic / architecture correction** — ownership, state-flow, timing, lifecycle, recovery, risk/execution boundaries or strategy-source alignment.
2. **MT4 source implementation** — actual changes to `blueprint/source/BBMA_EA.mq4` when a proven defect or approved design change requires code.
3. **Static audit / regression** — evidence that the change did not unintentionally alter protected BBMA Core, SL/TP, MM, risk, lifecycle or execution surfaces.
4. **Native MetaEditor compilation** — exact-source compile evidence and 0 errors / 0 warnings gates.
5. **Broker/runtime validation** — authenticated MT4 demo evidence, including order creation, recovery, lifecycle behavior and duplicate protection.
6. **Integration / canonicalization** — promotion of a reviewed candidate into the canonical development branch without importing temporary test plumbing.
7. **Release identity / freeze** — exact source blob, MQ4/EX4 hashes, build/version, default gates and freeze boundary.
8. **Issue / defect closure** — the defect, root cause, implementation, test evidence and final closure state.

---

## 2. Architecture and implementation history

The project progressed through multiple engineering layers rather than treating every step as a fresh trading-strategy rewrite.

Earlier P0/P1/P2/P3, Core V2, D1/D1O, C044, N1/N2/N3 and related audit records remain in `blueprint/`, `blueprint/audits/`, `blueprint/contracts/`, `blueprint/decisions/`, `blueprint/gap_closure/` and `docs/references/`.

Important principle:

> A development step may result in a code patch, a contract/architecture correction, a verification-only PASS, a runtime evidence requirement, or a deliberate decision to leave already-correct code unchanged.

Therefore a numbered project step does **not** automatically mean new MT4 trading logic was added.

---

## 3. P0 execution-identity defect — v4.59

### 3.1 Defect

Issue #94 demonstrated that an oversized MT4 broker `OrderComment()` could be stripped by the HFM server. The older execution identity depended too heavily on that broker comment, creating restart/recovery and duplicate-reconciliation risk.

### 3.2 MT4 source fix

Build:
`Version 4.5.9 - P0 Execution Identity Persistence Fix`

Property:
`#property version "4.59"`

Implemented engineering changes included:

- compact broker comment `BBMA|H:<16hex>`;
- terminal-side durable execution identity using GlobalVariables keyed/cross-validated by execution hash, ticket, magic, open time and direction;
- local persistence as the primary duplicate/history/recovery identity source;
- broker comment retained only as secondary/fallback/migration evidence;
- recovery does not claim normal identity when durable persistence actually failed;
- MT4 error 128 treated as ambiguous/fail-closed rather than blindly retryable.

No intended BBMA signal, SL/TP, MM or risk semantic change was introduced by this P0 fix.

### 3.3 Compile and regression evidence

- exact source native MetaEditor compile: **0 errors / 0 warnings**;
- protected-surface regression: **PS-01..PS-30 PASS**;
- v4.59 tooling/selftests/native profile matrix: **PASS**.

### 3.4 HFM broker-runtime acceptance

Fresh EA-created HFM demo order:

- ticket: `484701907`
- pair: `CHFJPY`
- direction: `SELL`
- execution hash: `7AADB1796BF36399`
- immediate persistence: `Persist=PASS Local=Y`
- compact broker hash found and matched

After a full restart of the same MT4 installation, the exact ticket was recovered as accepted `REC_IDENTITY_HASH_ONLY / EXECUTION_HASH_ONLY`, and no duplicate live order for the same execution identity was observed.

Result: **P0 broker-runtime PASS**.

Issue #94 was subsequently closed as `completed` after canonical promotion verification.

---

## 4. Post-P0 integration sequence — IP-01 to IP-12

The IP sequence exists to ensure a runtime-proven fix becomes canonical without contaminating the production source with temporary diagnostic/test plumbing.

| Step | Purpose | Final status |
|---|---|---|
| IP-01 | Freeze/fresh-check canonical development base | PASS |
| IP-02 | Create isolated post-P0 integration branch | PASS |
| IP-03 | Integrate reviewed production P0 source delta only | PASS |
| IP-04 | Classify changed files / exclude temporary plumbing | PASS |
| IP-05 | Run protected-surface regression | PASS |
| IP-06 | Lock exact source/build identity | PASS |
| IP-07 | Official exact-source MetaEditor compile | PASS — 0E0W |
| IP-08 | Rebaseline v4.59 runtime tooling / native matrix | PASS |
| IP-09 | Reconcile documentation, evidence and release identity | PASS |
| IP-10 | Promote reviewed candidate to `d1-owner-dev` and re-verify | PASS |
| IP-11 | Record canonical closure and close Issue #94 | PASS |
| IP-12 | Freeze canonical identity and hand off R1 | PASS |

### 4.1 Canonical v4.59 identity frozen at IP-12

- canonical source-bearing promotion commit: `4373e55b3baca7c99a3ca643cb5fa97629be09b7`
- source Git blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- repository/LF MQ4 SHA-256: `07a69ccfca19e19d71c95ca891c66d953343261276d7722107624ce974830843`
- Windows compile-checkout MQ4 SHA-256: `0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e`
- accepted EX4 SHA-256: `89821c5b1ae2d7c28a6cad7569cb2ced0e45090d0897451e0f61e0b46eb8944c`
- canonical baseline: `EnableD1TPWLifecycle=false`
- canonical baseline: `EnableC044Lifecycle=false`
- N3: non-execution-authority / firewalled

The LF and CRLF MQ4 SHA values represent line-ending materialization only and resolve to the same Git blob.

---

## 5. Runtime validation programme — R1 to R6

The formal runtime programme is sequential and evidence-driven:

`R1 -> R2 -> R3 -> R4 -> R5 -> R6`

Current state at the IP-12 freeze:

| Stage | Scope | Cases | Status |
|---|---|---:|---|
| R1 | D1 Extreme TP-Wajib lifecycle | 17 | INCOMPLETE / RELEASED FOR COLLECTION |
| R2 | C044 failed-Momentum lifecycle | 27 | BLOCKED by R1 |
| R3 | D1 owner + D1O identity/dedup | 16 | BLOCKED by R2 |
| R4 | Validation timing + M17 live SL geometry | 17 | BLOCKED by R3 |
| R5 | TradeLock + cumulative risk + P3/ambiguity | 21 | BLOCKED by R4 |
| R6 | N1/N2 forward identity/outcome + N3 firewall | 17 | BLOCKED by R5 |

No stage is marked PASS without attributable broker/demo evidence meeting its detailed matrix.

### R1 test boundary

R1 uses a **test-only** v4.59 profile:

- D1TPW ON
- C044 OFF
- authenticated HFM demo/broker session
- canonical production baseline remains D1TPW OFF / C044 OFF
- hosted/disconnected MT4 smoke is never accepted as broker-runtime PASS

During R1 evidence attribution, no opportunistic production EA source edits are permitted. A source change requires a concrete runtime defect or separately approved strategy/architecture decision followed by revalidation.

---

## 6. Release and evidence records

Key v4.59 records include:

- `blueprint/audits/P0_EXEC_ID_RUNTIME_PASS_RECORD_20260827.md`
- `blueprint/audits/P0_POST_PASS_INTEGRATION_EXECUTION_WORKSHEET_20260827.md`
- `blueprint/audits/P0_V459_POSTPASS_INTEGRATION_CLOSURE_AUDIT_20260827.md`
- `blueprint/audits/P0_V459_IP10_CANONICAL_PROMOTION_VERIFICATION_20260827.md`
- `blueprint/audits/P0_V459_IP12_CANONICAL_FREEZE_R1_HANDOFF_20260827.md`
- `blueprint/audits/POST_P0_PROTECTED_SURFACE_REGRESSION_EXECUTION_20260827.md`
- `blueprint/audits/POST_P0_CANONICAL_FREEZE_RELEASE_CHECKLIST_20260827.md`
- `blueprint/audits/MASTER_R1_R6_RUNTIME_EVIDENCE_INDEX_20260827.md`
- `blueprint/source/EA_RELEASE_IDENTITY.json`

These records are the developer/audit trail. Strategy rules remain governed by the dedicated BBMA/Oma Ally source-of-truth/reference and module-contract documents.

---

## 7. Maintenance rule for this section

Future engineering milestones should be appended here when they materially affect the EA development/release story, including:

- source fixes;
- architecture corrections;
- runtime-discovered defects;
- compile/regression closures;
- canonical promotions;
- formal R1-R6 stage closures;
- production release/freeze milestones.

Do not use this history section to silently introduce or reinterpret BBMA trading rules. Any strategy-semantic change must remain traceable to its approved source/decision/contract authority.
