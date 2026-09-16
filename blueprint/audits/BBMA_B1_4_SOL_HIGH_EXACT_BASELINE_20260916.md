ROADMAP ID: B1.4
MODEL: Sol High
TASK TYPE: EXACT BASELINE RECORDING / READ-ONLY PRE-DIAGNOSIS
PREDECESSOR: B1.3-P3 CLOSED/PASS at 1b8cbab892ae32afd4be93d5c0abda656f3561ab
LIVE OWNER: d1-owner-dev@ea4c48262c4bb058e375fb9a1b564fa132ba578b
GOVERNANCE/ORCHESTRATOR MAIN: main@11f7550e981e8c8b2206bf30f30d517c97bab909

# A. Purpose and boundary

B1.4 records the exact live baseline before B2 diagnosis.
It does not diagnose M01-M27/M12N, change Strategy Core, edit EA source, compile, run Strategy Tester, restart MT4, enable trading, merge implementation PRs, or promote unresolved evidence.
B1.3-P3 is reused as the verified predecessor; only material live deltas since that checkpoint are revalidated.

# B. Predecessor and workspace verification

- B1.3-P3 report gate: B1_4_EXACT_BASELINE_RECORDING_READY — PASS.
- B1.3-P3 savepoint commit: 1b8cbab892ae32afd4be93d5c0abda656f3561ab.
- B1.4 isolated branch: b1-4-sol-high-exact-baseline-savepoint-20260916.
- B1.4 worktree started clean from the exact predecessor commit.
- Primary historical checkout remains on the B1.3-P3 branch and retains three pre-existing untracked compile logs; they were not modified.
- Task Orchestrator tooling tree used for B1.4 matches merged main exactly: 64c5fe2b22aa5031e125f9a0938a7c15ace058b0.
# C. Live GitHub authority baseline

| Layer | Exact live identity | B1.4 classification |
|---|---|---|
| Implementation owner | d1-owner-dev@ea4c48262c4bb058e375fb9a1b564fa132ba578b | VERIFIED |
| Governance/tooling main | main@11f7550e981e8c8b2206bf30f30d517c97bab909 | VERIFIED |
| CURRENT.md | blob a4a9918a780fcd9a11c1ac04a61a4abfbddc8be5 | VERIFIED artifact; partially stale status text |
| MASTER_QUEUE.md | blob 8787ad515f3b34118a7fe582890a1512a72fc8b0 | VERIFIED active queue |
| SOURCE_INDEX.md | blob c6b7892d56152100a8153aba90b55476a320005f | VERIFIED source router |
| Canonical EA | blob 6e629128f37c3fd482dd49e275360503f73fee68 | VERIFIED unchanged |
| Strategy Core V2 | blob 923483602d89d775576e8def988958aff8f5fe75 | VERIFIED unchanged |

Delta from the B1.3-P3 owner reference 23def0919386263007ead1898b94637cc17f7f36 to current d1-owner-dev touches only:
- blueprint/CURRENT.md;
- blueprint/MASTER_QUEUE.md;
- docs/references/SOURCE_INDEX.md.

No delta exists in blueprint/source/BBMA_EA.mq4, blueprint/contracts, or BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md.
The live delta therefore changes governance/source-status documentation only and does not create a new Core/code baseline.
# D. Canonical EA / contract / Core baseline

Canonical EA remains:
- repository path: blueprint/source/BBMA_EA.mq4;
- Version 4.6.1 - F7 Re-Entry Lifecycle Integration;
- property version 4.61;
- SHA-256: 3BE02985A6A3DF9E001FB441BEED3B8F8DA2755C2ECE2F78B43879C6E635311C;
- Git blob: 6e629128f37c3fd482dd49e275360503f73fee68.

B1.3-P2 authority baseline is retained because the contract tree is unchanged:
- 25 tracked/readable contract artifacts;
- 22 active/locked contracts;
- M12N remains observation/read-only context;
- N2 remains research-only;
- N3 remains staging/inactive.

Strategy Core V2 remains unchanged at blob 923483602d89d775576e8def988958aff8f5fe75.
SOURCE_INDEX remains the mandatory source router. HOLD/UNCLEAR/PARTIAL evidence remains outside executable Core.
No standalone current singular Master Blueprint path/hash has become newly authoritative; the previously reconstructed archived blueprint remains historical-only evidence.
# E. Current governance and queue state

CURRENT.md is still anchored to its 2026-09-09 reconciliation header and old owner-head record 262ff66..., so those fields are STATUS_STALENESS versus live d1-owner-dev. Its source-transcription section was subsequently refreshed and must not be treated as uniformly stale.

MASTER_QUEUE.md was reconciled on 2026-09-16. Its recorded reconciliation head efe9ede... is one merge behind current owner head because PR #166 subsequently reordered the queue. The queue content itself is current at blob 8787ad51....

Current dependency order is:
Q4 -> Q5 -> Q1 -> Q2 -> Q3 + Q6 -> Q7 -> Q8 -> Q10 -> Q9 + Q11.

Current Q statuses:
- Q4 COMPLETE / DO NOT RERUN.
- Q5 IN PROGRESS / HOLD-AWARE.
- Q1 SOURCE FIX + NATIVE VALIDATION PENDING G40.
- Q2 REMOTE MODEL PASS / LOCAL SOURCE PATCH PENDING G40 RECONCILIATION.
- Q3 SOURCE+STATIC+NATIVE PASS / FINAL RUNTIME GATE PENDING.
- Q6 SYNTHETIC-V3 TESTER GATES PASS / NATIVE ARCHIVE INCOMPLETE.
- Q7 NOT YET AUTHORIZED.
- Q8 PENDING.
- Q10 DEFERRED UNTIL FINAL INTEGRATION CANDIDATE.
- Q9 DEFERRED UNTIL CURRENT NMJE BASELINE IS CLEAN.
- Q11 DEFERRED / RE-AUDIT REQUIRED.
# F. Active workstream baseline

## F1. Q1 NMJE read-only authority
- Draft PR #142 remains OPEN / DRAFT / NO MERGE.
- Head: 89f970ad5239a6303e31471a8a75ec3d3477d7f6.
- Persisted PR evidence records Build 4.83 source fix, targeted tests and native MetaEditor 0E0W.
- Runtime remains NOT VERIFIED; no canonical activation is implied.

## F2. Q2 F7/C044 Build 4.82 hardening
- Draft PR #140 remains OPEN / DRAFT / NO MERGE.
- Head: 73680bfcf087b35d87807f3ebf2ada1a69676240.
- Persisted PR evidence records Build 4.82, native 0E0W, targeted guards and deterministic C044 model PASS.
- Physical/runtime acceptance remains separate and NOT VERIFIED.

## F3. Q3 C10 Build 4.81 runtime closure
- Draft PR #131 remains OPEN / DRAFT.
- Head: 93328149b6830ed7ff000451aa8590d7ec044b35.
- Static/model/native compile evidence remains bounded PASS.
- Exact broker-clock ACTIVE -> same-terminal physical restart/recovery gate remains PENDING.
- Current B1.4 process snapshot found no terminal.exe or metaeditor.exe, so no active runtime attempt is inferred from process state.
## F4. Q4/Q5 source evidence
- Q4 mechanical source processing is canonical COMPLETE / DO NOT RERUN.
- Current queue records 63/63 Primary-15/Group-3 manifests mechanically complete with missing units = 0.
- ASR-DRAFT remains non-Core and cannot create executable Strategy-Core authority.
- A5 closure remains ACCEPTED WITH PENDING ITEMS, not semantic closure.
- Retained unresolved state: 9 A4/A5 decisions = 6 UNCLEAR + 3 PARTIAL + 0 MATCH; 4 blocked A3 overlaps; 2 excluded A3 records; 6 audio-recheck-empty queue records; W004 duplicate conflict.
- No genuine approved-Core source conflict was established for those nine decisions; unresolved content remains outside execution.

Source Autonomy is available on governance main at 11f7550e981e8c8b2206bf30f30d517c97bab909 and remains bounded/read-only for manifest planning unless an explicit native resume command is separately authorized.

Local snapshot limitation:
- D:\BBMA\Workspace\source-autonomy-live-evidence\SOURCE_RECON_SCAN_20260916.json currently hashes to 1FDCADB614C27BACD473C8B189FF8AE9861060548D8CFE28E66A8C8DEBD32479.
- The previously recorded 0837... identity could not be reproduced and no second copy was found under D:\BBMA.
- Therefore the 0837... identity is NOT_PROVABLE and is not used as B1.4 authority.
- Canonical Q4/Q5 state is instead anchored to merged queue/source governance plus the retained A5 closure evidence.

## F5. Q6 historical data
- Issue #128 remains OPEN.
- Scope remains EURUSD, GBPUSD, USDJPY; full native raw-tick archive is required before final tick-accurate canonical claims.
- MASTER_QUEUE status remains NATIVE ARCHIVE INCOMPLETE.
- B1.4 does not restart or advance historical-data workers.
- D: free space at the B1.4 snapshot is approximately 401.66 GB, above the existing >120 GB fail-closed guard.
# G. Exact claim classification

| ID | Claim | Classification | Action |
|---|---|---|---|
| B14-C01 | d1-owner-dev is the implementation owner at ea4c482... | MATCH | PRESERVE |
| B14-C02 | main is governance/tooling authority at 11f7550... | MATCH | PRESERVE |
| B14-C03 | Canonical EA blob/source identity is unchanged from B1.3 | MATCH | PRESERVE |
| B14-C04 | Contract tree and Strategy Core V2 are unchanged from B1.3 | MATCH | PRESERVE |
| B14-C05 | CURRENT header/head represent current live owner state | STATUS_STALENESS | Use live refs, do not rewrite in B1.4 |
| B14-C06 | MASTER_QUEUE recorded owner head equals current live owner head | STATUS_STALENESS | Queue content retained; live owner ref wins |
| B14-C07 | Q4 requires more transcription | NO FIX / STALE ROUTE | DO NOT RERUN |
| B14-C08 | Q5 unresolved evidence can create executable rules | HOLD-UNRESOLVED | Prohibited |
| B14-C09 | Source snapshot SHA 0837... is current/verifiable | NOT_PROVABLE | Do not use as authority |
| B14-C10 | PR #142 is runtime/canonical accepted | NOT_PROVABLE | Runtime and merge gates remain open |
| B14-C11 | PR #140 is runtime/canonical accepted | NOT_PROVABLE | Runtime and merge gates remain open |
| B14-C12 | PR #131 final broker-clock recovery is closed | NOT_PROVABLE | Exact physical runtime gate remains open |
| B14-C13 | Full 3-pair native archive is complete | NOT_PROVABLE | Q6 remains incomplete |
| B14-C14 | Integrated candidate/release readiness exists | NOT_PROVABLE | Q7/Q8/Q10 remain gated |
| B14-C15 | Q1 queue wording still says source fix/native validation pending, while PR #142 records committed source + native 0E0W | STATUS_STALENESS | Treat source/native as persisted PASS; runtime remains pending |
| B14-C16 | Q2 queue wording still says local source patch pending, while PR #140 records committed Build 4.82 + targeted tests/native 0E0W | STATUS_STALENESS | Treat source/static/native as persisted PASS; physical/runtime remains pending |

No new approved-Core, architecture or production-safety conflict was created by B1.4.
# H. PASS / FAIL / NOT RUN

| Gate | Result |
|---|---|
| B1.3-P3 predecessor integrity | PASS |
| Live d1-owner-dev/main ref recovery | PASS |
| Owner delta scope verification | PASS — governance/source-status docs only |
| Canonical EA identity continuity | PASS |
| Contract/Core identity continuity | PASS |
| Current queue/status extraction | PASS |
| Active PR status refresh | PASS |
| Source HOLD retention | PASS |
| Runtime/process observation | PASS — no terminal/metaeditor observed |
| Local snapshot 0837... provenance | FAIL / NOT_PROVABLE; excluded from authority |
| EA compile/static/test/tester execution by B1.4 | NOT RUN |
| MT4 restart/deployment/trading enablement | NOT RUN |
| Strategy-Core diagnosis B2 | NOT RUN |
| Release readiness/profitability | NOT RUN / NOT CLAIMED |

# I. B1 closure and next safe step

Decision: B1_EXACT_BASELINE_RECORDED — PASS, subject to report/hash/commit verification.

The B1 preflight sequence is now materially complete once this report is integrity-verified and saved as a report-only continuation artifact.
No unresolved item above is silently resolved by baseline recording.

Next roadmap step: B2 — Strategy-Core gap audit M01-M27 + M12N, beginning B2.1 M01-M05.
Roadmap owner for B phase is Astra High; XHigh is reserved only for genuine architecture or production-safety conflict.
Source Autonomy must be used automatically for any source/evidence retrieval in B2.
B2 must classify mismatch before fix and must not implement fixes during B phase.

# Mandatory conclusion

B1.4 EXACT BASELINE RECORDED
B1 PRE-DIAGNOSIS PREFLIGHT BASELINE COMPLETE
CANONICAL EA CONTRACT AND CORE IDENTITIES UNCHANGED
LIVE GOVERNANCE DELTAS RECORDED WITHOUT PROMOTING THEM TO STRATEGY SEMANTICS
Q4 COMPLETE / DO NOT RERUN
ALL A5 HOLD UNCLEAR PARTIAL BLOCKED EXCLUDED DUPLICATE AND PENDING STATES RETAINED
NO EA CORE CONTRACT EXECUTION RISK OR PRODUCTION LOGIC CHANGED
COMPILE TESTER RUNTIME RESTART DEPLOYMENT AND TRADING ENABLEMENT NOT RUN
B2.1 M01-M05 STRATEGY-CORE GAP AUDIT IS NEXT, WITH ASTRA HIGH MODEL ROUTE
