# P0 v4.59 IP-10 Canonical Promotion Verification

Date: 2026-08-27  
Target branch: `d1-owner-dev`  
Status: **IP-10 PASS / IP-11 PENDING**

## 1. Promotion boundary

Reviewed integration candidate:
- branch: `p0-v459-postpass-integration-20260827`
- reviewed head: `307571027a75b3697e162b555213f5e956cd96d7`
- candidate tree: `b1618eca763f84d6f157fc99c0a8f6d72e8fdb1b`

Fresh canonical base immediately before promotion:
- `d1-owner-dev`: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`
- compare state: candidate ahead 19, behind 0
- merge base: exact canonical base above

Promotion:
- PR: `#95` — `IP-10: promote reviewed P0 v4.59 candidate to d1-owner-dev`
- merge commit: `4373e55b3baca7c99a3ca643cb5fa97629be09b7`
- merge commit tree: `b1618eca763f84d6f157fc99c0a8f6d72e8fdb1b`
- merge tree is identical to the reviewed candidate tree.

## 2. Exact canonical source verification after merge

Re-fetched directly from `d1-owner-dev` after PR #95 merge:
- path: `blueprint/source/BBMA_EA.mq4`
- Git blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- repository/LF SHA-256: `07a69ccfca19e19d71c95ca891c66d953343261276d7722107624ce974830843`
- Windows compile-checkout SHA-256: `0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e`
- build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- `#property version "4.59"`
- `EnableC044Lifecycle=false`
- `EnableD1TPWLifecycle=false`

The two MQ4 byte hashes differ only by repository LF vs Windows checkout CRLF. Git blob identity is unchanged.

## 3. Accepted predecessor evidence

Promotion relies on already-closed predecessor gates:
- P0 authenticated HFM fresh-order / restart / no-duplicate runtime acceptance: PASS.
- protected-surface regression PS-01..PS-30: PASS.
- exact official MetaEditor integration compile: 0 errors / 0 warnings.
- accepted EX4 SHA-256: `89821c5b1ae2d7c28a6cad7569cb2ced0e45090d0897451e0f61e0b46eb8944c`.
- v4.59 runtime tooling rebaseline and native matrix: PASS.
- IP-09 documentation/release reconciliation: PASS.

## 4. Scope preservation

Verified boundaries:
- `main` is not advanced by IP-10.
- no lifecycle gate is enabled in canonical baseline.
- no N3 execution authority is activated.
- no new BBMA strategy, SL/TP, MM, risk or lifecycle semantic patch is introduced by IP-10.
- Issue #94 remains OPEN intentionally until IP-11.

## 5. Release identity metadata

`blueprint/source/EA_RELEASE_IDENTITY.json` is updated documentation-only after promotion to record:
- canonical promotion PR `#95`;
- source-bearing promotion merge commit `4373e55b3baca7c99a3ca643cb5fa97629be09b7`;
- status `IP10_CANONICAL_PROMOTION_PASS_IP11_PENDING`.

This metadata update does not alter `BBMA_EA.mq4` or the accepted EX4 identity.

## 6. Verdict

**IP-10 PASS.**

The reviewed P0 v4.59 candidate is now the canonical development-branch source on `d1-owner-dev`, with exact source/build/default-gate identity re-verified after promotion.

Next authorized step: **IP-11 — record canonical verification on Issue #94 and close the issue.**

`main` remains untouched. R1 formal broker evidence collection still waits IP-11 closure and IP-12 canonical freeze/handoff.
