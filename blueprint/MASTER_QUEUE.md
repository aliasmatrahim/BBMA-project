# BBMA Active Master Queue

Reconciled: **2026-09-16**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`efe9ede3211ef306d74bb3ce566ed9b3677e3163`**

This file is the active queue. The pre-2026-09-09 historical queue is preserved byte-for-byte at `blueprint/archive/MASTER_QUEUE_pre_20260909.md`.

## Queue rules
- Resolve current state through `PROJECT_INSTRUCTIONS.md` Sections 17–20 before acting.
- GitHub live state outranks chat memory and historical queue text.
- `docs/references/SOURCE_INDEX.md` routes Strategy-Core evidence.
- Do not create a new trading rule merely to close a gap or improve past performance.
- No primary MT4 restart, trading enablement, or production activation is implied by queue progression.

## Execution order / dependency path
Stable Q IDs are preserved. The active dependency order is:
- **Source evidence:** Q4 -> Q5
- **Core / architecture:** Q1 -> Q2
- **Parallel validation / data:** Q3 + Q6
- **Integration / final acceptance:** Q7 -> Q8 -> Q10
- **Deferred / future:** Q9 + Q11

Q3 and Q6 may progress in parallel when their runtime/data conditions are available. Q7 remains blocked until Q1/Q2 and materially relevant Q5 reconciliation are sufficiently closed.

## Stage A - Source evidence / reconciliation

### Q4 — Primary-15 same-engine transcription
Priority: **HIGH / SOURCE EVIDENCE**
Status: **COMPLETE / DO NOT RERUN**

Fresh Source Autonomy recheck on 2026-09-16 from live G40 manifests and `.done` markers:
- 63 existing Primary-15/Group-3 manifests inspected;
- 63/63 mechanically COMPLETE;
- missing units = 0;
- Primary-15 videos 01-04 also have completed `AUDIO_RECHECK_CORRECTED` outputs from the same `faster-whisper` / `standard-large-v3-turbo-ct2` engine;
- `ASR-DRAFT` remains non-Core and cannot create executable Strategy-Core authority.

Closure handling:
1. Do not rerun completed manifests/chunks blindly.
2. Preserve original audio/video, raw ASR and corrected evidence as separate provenance layers.
3. Any future re-transcription requires new evidence that a specific source unit is mechanically missing or invalid.
4. Continue semantic work under Q5; mechanical completion is not reconciliation or Core acceptance.

### Q5 — Reconcile completed source evidence against current Core/code
Priority: **HIGH / SOURCE RECONCILIATION**
Status: **IN PROGRESS / HOLD-AWARE**

Current retained unresolved state:
- A4/A5 adjudication: 9 records = 6 `UNCLEAR`, 3 `PARTIAL`, 0 `MATCH`;
- 4 active A3 overlaps remain blocked;
- 2 A3 records remain excluded;
- 6 `AUDIO_RECHECK_EMPTY` review rows remain pending; source-media recheck confirms audio streams exist, but empty/invalid recheck text does not resolve semantic uncertainty;
- W004 remains duplicate-conflict / pending review.

Scope:
- Extreme/MHV/MLV/Re-Entry/CSA-CSAK/Momentum/F7 timing/lifecycle;
- mainframe -> subframe chronology;
- SL/TP provenance and any remaining HOLD/CONFLICT items.

Rules:
- no rule addition merely because an evidence gap exists;
- source contradiction remains HOLD until resolved;
- compare Evidence -> Core -> Contract -> Code -> Test evidence;
- production change requires a separately authorized minimal fix;
- HOLD/PARTIAL/UNCLEAR evidence remains non-executable.

## Stage B - Core / architecture correctness

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

## Stage C - Parallel runtime validation / historical data

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

## Stage D - Integration / regression / final acceptance

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

### Q10 — Final automated broker/demo acceptance
Issue: **#109**
Status: **DEFERRED UNTIL FINAL INTEGRATION CANDIDATE**

Do not run the historical v4.59 R1–R6 runner as if it were the final programme. Resolve and freeze the exact final candidate, then generate/run the candidate-specific demo acceptance matrix with fail-closed demo identity and evidence packaging.

## Stage E - Deferred / future

### Q9 — NMJE v2 M5 accuracy hardening
Issue: **#101**
PR: **#126 retained as future replacement staging/evidence**
Status: **DEFERRED UNTIL CURRENT NMJE BASELINE IS CLEAN**

Do not resume old PR #102 lineage; it is historical evidence and has been closed. Rebase/re-audit future work against the then-current owner. M5 remains lower-TF context/shadow/refinement and cannot become an independent clock/create/reject/execute authority without a separate explicit policy decision.

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
G40 was reachable during the 2026-09-16 queue reconciliation. Future work must still re-read actual local process/worktree/manifest state before any mutation.

G40-dependent active workstreams that require live-state recovery are **Q1, Q2, Q3 and Q6**. Q4 is mechanically complete and must not be re-added to the resume list without new evidence that a specific source unit is missing or invalid.

No destructive reset, blind recreation, automatic MT4 restart, or trading enablement is authorized by this queue.
