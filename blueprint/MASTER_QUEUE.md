# BBMA Active Master Queue

Reconciled: **2026-09-09**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`262ff66dfdeed2cd4a7ac20fb82c47136db59451`**

This file is the active queue. The pre-2026-09-09 historical queue is preserved byte-for-byte at `blueprint/archive/MASTER_QUEUE_pre_20260909.md`.

## Queue rules
- Resolve current state through `PROJECT_INSTRUCTIONS.md` Sections 17–20 before acting.
- GitHub live state outranks chat memory and historical queue text.
- `docs/references/SOURCE_INDEX.md` routes Strategy-Core evidence.
- Do not create a new trading rule merely to close a gap or improve past performance.
- No primary MT4 restart, trading enablement, or production activation is implied by queue progression.

## P0 — Immediate correctness / infrastructure blockers

### Q1 — Restore NMJE read-only authority
Issue: **#141**
PR: **#142**
Priority: **CRITICAL / ARCHITECTURE AUTHORITY**
Status: **SOURCE FIX + NATIVE VALIDATION PENDING G40**

Required next steps:
1. Reconnect G40 and re-read local `nmje-readonly-141` worktree before editing.
2. Preserve/finish unique Build **4.83** identity.
3. Remove NMJE relation-based execution rejection from the active preflight path while preserving N1/N2 observation/attribution telemetry.
4. Prove NMJE cannot create/reject/rank/execute under current policy.
5. Run targeted regression and native MetaEditor **0E0W**.
6. Push only exact verified source/evidence to PR #142.
7. Runtime validation must be attributable to the exact candidate before #141 closes.

Do not add a replacement nested filter or score.

### Q2 — Complete F7/C044 Build 4.82 infrastructure hardening
Issues: **#127 #132 #133 #138**
PR: **#140**
Priority: **CRITICAL / RUNTIME PROVENANCE + RESTART INTEGRITY**
Status: **REMOTE MODEL PASS / LOCAL SOURCE PATCH PENDING G40 RECONCILIATION**

Required next steps:
1. Reconnect G40 and preserve/re-read the existing uncommitted local v4.82 patch before any fetch/merge/edit that could overwrite it.
2. Reconcile local source against current PR #140 and current owner head.
3. Ensure `[F7-BUILD]` is emitted before initialization/recovery telemetry can be accepted.
4. Use frozen exact-ticket `info.open_time` for EXEC telemetry.
5. Make C044 lifecycle+replay persistence one verified generation: invalidate old commit first, clear/verify old payload, write/verify all new payload, publish commit marker last.
6. Fail frozen on legacy/unprovable/mixed/partial generations.
7. Run deterministic torn-prefix and injected writer-failure model/static regressions.
8. Native MetaEditor **0E0W**.
9. Push exact verified source/evidence to PR #140.
10. Physical/runtime acceptance remains separate; do not restart primary MT4 just to close static work.

### Q3 — Close exact C10 Build 4.81 broker-clock restart acceptance
Issues: **#122 #123**
PR: **#131** (with #125/#129/#130 retained as provenance/base lineage)
Priority: **HIGH / ISOLATED RUNTIME EVIDENCE**
Status: **SOURCE+STATIC+NATIVE PASS / FINAL RUNTIME GATE PENDING**

Required next steps after G40 reconnect:
1. Verify exact deployed MQ4/EX4/build/config/InstanceID=81 before accepting new evidence.
2. Keep `Authority=NONE`, `ExpertsTrades=false`, `MaxTradePerPair=0`, `MaxTotalTrade=0`.
3. Wait for one genuine fresh `ACTIVE`; do not synthesize a signal.
4. Perform same-isolated-terminal physical stop/restart with proper log flushing.
5. Require exact ACTIVE recovery plus `[C10][SHADOW_RECOVERY] Active=1` and exact-config `[C10][READY] ... Authority=NONE`.
6. Run hardened verifier.
7. Require zero malformed/duplicate target-domain rows, no ledger disable, no broker action and no `DEC_EXECUTED`.
8. Only then close #122/#123 / promote the C10 evidence state.

Build 4.80 or Strategy Tester evidence cannot substitute for exact 4.81 runtime closure.

## P1 — Autonomous source-library infrastructure

### Q3A — Build autonomous source-library lifecycle and reconciliation control plane
Issue: **#152**
Depends on: **PR #149 Task Orchestrator Contract + PR #151 autonomous engineering infrastructure**
Priority: **HIGH / PARALLEL-SAFE SOURCE INFRASTRUCTURE**
Status: **AUTHORIZED / P1 IMPLEMENTATION STARTING**

Purpose: state-driven source maintenance, provenance/HOLD preservation, lower repeated scans/context, no transfer of Strategy-Core authority.

Processing phase: `DISCOVERED -> INGESTED -> INTEGRITY_VERIFIED -> PROVENANCE_CLASSIFIED -> EXTRACTED -> RECONCILIATION_PENDING -> RECONCILED -> REGISTERED`.

Semantic disposition: `UNREVIEWED | MATCH | CORROBORATION_ONLY | PARTIAL | UNCLEAR | SOURCE_CONFLICT | ACCEPTED_CORE | REJECTED`.

Priority order: registry/invariants/idempotent SHA ingestion -> discovery/provenance -> reconciliation/no-promotion guard -> Evidence-DAG Core impact -> bounded SOURCE_INDEX/register updater -> failure-first dashboard/context pack -> G40 Primary-15/Group-3/media adapters -> end-to-end evidence package.

Hard gates: no new rule/entry/exit/filter/SL/TP/lifecycle authority; HOLD/PARTIAL/UNCLEAR/SOURCE_CONFLICT/REJECTED remain non-executable; ACCEPTED_CORE requires explicit accepted authority; originals/corrected/derived stay separate; zero-result search is not absence; no automatic merge/deploy/restart/trading.

Execution lane: initial deterministic tooling may run parallel to Q1-Q3, must reuse PR #151 primitives, and semantic adjudication still follows `SOURCE_INDEX -> routed evidence -> accepted Core -> contracts/decisions`.

## P1 — Source corpus completion / reconciliation

### Q4 — Finish Primary-15 same-engine transcription
Priority: **HIGH / SOURCE EVIDENCE**
Status: **LOCAL RESUME PENDING G40**

At reconnect, re-read manifests first. Last observed state only:
- 05–09 complete;
- 10 partial (2/10 chunks observed);
- 11 pending;
- 12–15 complete;
- 01–04 queued for same-engine re-transcription where required;
- Group-3 BBMATV corpus complete at last rescan.

Required handling:
1. Resume only missing chunks/videos.
2. Preserve original audio/video and transcript provenance.
3. Produce corrected technical transcript separately from raw ASR where needed.
4. Reconcile evidence into MATCH/PARTIAL/MISSING/CONFLICT before any Strategy-Core proposal.
5. Do not modify production rules directly from ASR output.

### Q5 — Reconcile completed source evidence against current Core/code
Priority: **HIGH AFTER RELEVANT TRANSCRIPTS**
Status: **PENDING**

Scope:
- Extreme/MHV/MLV/Re-Entry/CSA-CSAK/Momentum/F7 timing/lifecycle;
- mainframe -> subframe chronology;
- SL/TP provenance and any remaining HOLD/CONFLICT items.

Rules:
- no rule addition merely because an evidence gap exists;
- source contradiction remains HOLD until resolved;
- compare Evidence -> Core -> Contract -> Code -> Test evidence;
- production change requires a separately authorized minimal fix.

## P1 — Historical/backtest environment

### Q6 — Complete canonical Dukascopy-native 3-pair archive
Issue: **#128**
Priority: **HIGH / LONG-RUNNING DATA PROVENANCE**
Status: **SYNTHETIC-V3 TESTER GATES PASS / NATIVE ARCHIVE INCOMPLETE**

Current verified milestone:
- EURUSD 2006-09 COMPLETE 720/720;
- archive SHA-256 `6e0975c7ca1454ba1056f8b189c0e21f639936683bfa4f115a87bd823cf21f79`;
- last recorded orchestrator position: EURUSD 2006-10;
- worker policy: `BBMA_NATIVE_WORKERS=1` while Primary-15 ASR is active;
- free-space fail-closed guard: >120 GB.

Required next steps:
1. Re-read manifests/process state on G40.
2. Reuse every COMPLETE verified month; resume first incomplete pair-month only.
3. Validate exact expected hourly artifact count, payload validity, manifest completeness, tar entry count and archive SHA for each month.
4. Retry only missing/transient-failure hours; never accept invalid payload silently.
5. Continue through all 720 target pair-months.
6. Resolve remaining provenance/session/deployment broker-time engineering mapping.
7. Only then permit final tick-accurate canonical historical claims.

Synthetic-v3 remains engineering-only; its tick volume normalization cannot become native tick authority.

## P2 — Integration after blockers

### Q7 — Build one integrated candidate from verified current workstreams
Priority: **HIGH AFTER Q1/Q2 + REQUIRED SOURCE RECONCILIATION**
Status: **NOT YET AUTHORIZED**

Before integration:
- Q1 NMJE read-only correction must be verified;
- Q2 F7 infrastructure candidate must be verified;
- D1 M11 -> M15 -> M16 is already integrated; do not duplicate it;
- reconcile any source evidence that materially changes candidate semantics;
- preserve M15/M16/M17/M19/M20/M21/M22/M23/M24 ownership boundaries.

Integrated candidate requires unique build identity, protected-surface/static regression, native MetaEditor 0E0W, deterministic tests and attributable historical/runtime validation.

### Q8 — Regression/backtest programme
Priority: **AFTER EXACT INTEGRATION CANDIDATE + USABLE HISTORICAL PROFILE**
Status: **PENDING**

Use isolated/canonical historical environment. Separate mechanism correctness from profitability claims. Any proposed accuracy filter/policy must start as evidence/shadow work and requires explicit Strategy-Core authorization before reducing valid trade opportunity.

## P3 — Deferred/future

### Q9 — NMJE v2 M5 accuracy hardening
Issue: **#101**
PR: **#126 retained as future replacement staging/evidence**
Status: **DEFERRED UNTIL CURRENT NMJE BASELINE IS CLEAN**

Do not resume old PR #102 lineage; it is historical evidence and has been closed. Rebase/re-audit future work against the then-current owner. M5 remains lower-TF context/shadow/refinement and cannot become an independent clock/create/reject/execute authority without a separate explicit policy decision.

### Q10 — Final automated broker/demo acceptance
Issue: **#109**
Status: **DEFERRED UNTIL FINAL INTEGRATION CANDIDATE**

Do not run the historical v4.59 R1–R6 runner as if it were the final programme. Resolve and freeze the exact final candidate, then generate/run the candidate-specific demo acceptance matrix with fail-closed demo identity and evidence packaging.

### Q11 — Dashboard / observer future materialization
Status: **DEFERRED / RE-AUDIT REQUIRED**

Older dashboard/observer PRs were prepared against historical frozen candidates. Do not directly merge their source transforms into the current owner. When sequenced, re-audit the desired display/observer behavior against current source/ownership, rematerialize the smallest display/observer-only patch, and run native/runtime acceptance as applicable.

## Closed / do not requeue without new evidence
- D1 M11 strategic owner -> M15 strategic filter/frozen snapshot -> M16 exact snapshot revalidation: **already integrated**; post-freeze re-audit found no new code fix required.
- stale v4.58 automatic PR probe #136: closed by workflow-only fix.
- governance drift #111 and live-status authority #113: closed by documentation-only merge.
- historical one-shot/dispatcher/validation-only PRs explicitly marked `do not merge`: closed; branches/evidence remain available as provenance.
- historical v4.59 demo runner is not a current release path.

## G40 resume policy
Current G40 device is offline at this reconciliation, auth token valid. An hourly condition watcher is enabled. When G40 reconnects it must first re-read local process/worktree/manifests and then resume Q1/Q2/Q3/Q4/Q6 from exact actual state. No destructive reset or blind recreation is permitted.
