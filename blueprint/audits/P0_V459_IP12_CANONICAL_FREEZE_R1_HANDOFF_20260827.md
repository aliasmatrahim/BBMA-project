# P0 v4.59 IP-12 Canonical Freeze / R1 Handoff

Date: 2026-08-27  
Canonical branch: `d1-owner-dev`  
Status: **CANONICAL FROZEN / R1 RELEASED AS INCOMPLETE**

## 1. Preconditions

The ordered predecessor gates are complete:

- P0 broker-runtime acceptance: **PASS**.
- IP-01..IP-09 integration, regression, compile, tooling and documentation gates: **PASS**.
- IP-10 canonical development-branch promotion: **PASS** through PR #95.
- IP-11 Issue #94 canonical closure: **PASS**; Issue #94 is closed as `completed`.

This record is a freeze/handoff boundary. It does not change BBMA strategy semantics and does not activate any lifecycle gate in the canonical production baseline.

## 2. Frozen source/build identity

Canonical source-bearing promotion commit:
`4373e55b3baca7c99a3ca643cb5fa97629be09b7`

IP-10 post-promotion verification head:
`5674d2bcc097a025d35859a40250060fc1d70d99`

Canonical source:
`blueprint/source/BBMA_EA.mq4`

Frozen identity:

- build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- property version: `4.59`
- Git blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- repository/LF MQ4 SHA-256: `07a69ccfca19e19d71c95ca891c66d953343261276d7722107624ce974830843`
- Windows compile-checkout MQ4 SHA-256: `0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e`
- accepted EX4 SHA-256: `89821c5b1ae2d7c28a6cad7569cb2ced0e45090d0897451e0f61e0b46eb8944c`
- official exact-source MetaEditor integration compile: **0 errors / 0 warnings**
- v4.59 runtime tooling/native matrix: **PASS**

The two MQ4 SHA-256 values represent repository LF bytes versus the Windows CRLF compile checkout. They resolve to the same Git blob and do not represent a source-semantic difference.

## 3. Canonical default-gate freeze

The canonical baseline remains:

- `EnableD1TPWLifecycle=false`
- `EnableC044Lifecycle=false`
- N3 remains non-execution-authority / firewalled

IP-12 does **not** switch either lifecycle gate ON in `blueprint/source/BBMA_EA.mq4`.

## 4. P0 closure identity

Accepted HFM demo runtime evidence remains attributable to:

- ticket `484701907`
- pair `CHFJPY`
- direction `SELL`
- execution hash `7AADB1796BF36399`
- immediate persistence `Persist=PASS Local=Y`
- same-installation full MT4 restart recovered the same ticket as accepted `REC_IDENTITY_HASH_ONLY / EXECUTION_HASH_ONLY`
- no duplicate live ticket for the same execution identity was observed

Issue #94 was closed as `completed` on 2026-08-27 after the final IP-11 canonical verification comment.

## 5. Freeze rule during R1 attribution

While R1 broker-runtime evidence is being collected:

**No opportunistic EA-source edit is allowed on the frozen canonical source.**

A source patch is permitted only when:

1. a concrete attributable runtime defect is demonstrated; or
2. a separately approved strategy/architecture decision authorizes a change.

Documentation, evidence indexing and test-package preparation may continue provided they do not mutate canonical trading semantics.

## 6. R1 handoff

R1 is now formally released from the P0/IP-10/IP-11 blocker, but its status is **INCOMPLETE**, not PASS.

Scope:
`R1 — D1 Extreme TP-Wajib lifecycle`

Mandatory tracker:
`blueprint/audits/MASTER_R1_R6_RUNTIME_EVIDENCE_INDEX_20260827.md`

Detailed authority:
`R1_D1_TPW_BROKER_RUNTIME_TEST_MATRIX_PREP_20260826.md`

R1 test-package rules:

- exact v4.59 frozen source lineage only
- authenticated HFM demo/broker session required
- test-only profile: **D1TPW ON / C044 OFF**
- canonical production baseline remains **D1TPW OFF / C044 OFF**
- `MinRRRatio=0` where the targetless D1 TP-Wajib acceptance case requires it
- hosted/disconnected MT4 smoke can support environment/tooling checks but can never be promoted to broker-runtime PASS
- all 17 R1 cases (`R1-00..R1-16`) remain evidence-driven; no narrative or static inference can mark them PASS

## 7. Downstream stage boundary

Current formal stage ordering is:

`R1 -> R2 -> R3 -> R4 -> R5 -> R6`

- R1: `INCOMPLETE / RELEASED FOR COLLECTION`
- R2-R6: `BLOCKED` by predecessor ordering

No downstream stage is promoted by this freeze record.

## 8. Main branch boundary

`main` is not advanced by IP-12. Canonical development and runtime attribution continue from `d1-owner-dev` under the frozen identity above.

## 9. Verdict

**IP-12 PASS — CANONICAL FROZEN / R1 RELEASED AS INCOMPLETE.**

The next executable project activity is R1 authenticated broker-runtime evidence collection. Any source defect discovered during R1 must be handled through a separately attributable fix/revalidation cycle before R1 can close.
