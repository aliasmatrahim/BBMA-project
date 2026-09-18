# BBMA Active Master Queue

Reconciled: **2026-09-18**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`6be2eef1495e2d896e121f5c1846ab3cd14e0f12`**

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

Q3 and Q6 may progress in parallel when their runtime/data conditions are available. Q7 is frozen and the scoped GBPUSD Q8 engineering regression is now complete under Issue #188. Q6 native final-authority residuals remain open under Issue #128; Q3 remains parallel and Q10 remains separately gated.

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
Status: **COMPLETE FOR Q7 / TRANSCRIPT-QA RESIDUALS NON-BLOCKING**

Current semantic state after Issue #169 / PR #170 and full Q5 Issue #176 closure:
- 9 retained records = 6 `CORROBORATION_ONLY` + 3 `REJECTED`; Strategy-Core semantic `UNCLEAR`/`PARTIAL` = 0;
- no row is promoted to `ACCEPTED_CORE`, no source conflict is created and no detector/filter/timing authority is added;
- 4 historical A3 blocked overlaps, 2 excluded A3 records, 6 `AUDIO_RECHECK_EMPTY` rows and W004 duplicate-conflict remain retained as provenance/transcript-QA residuals only;
- five exact-wording fragments remain uncertain and non-executable pending materially better evidence;
- these transcript-QA residuals do not block accepted Core semantics or authorize production changes;
- Issue #180 / PR #183 is closed unmerged because current owner Build 4.86 already contains the shared MA5/MA10 close-side guard before Type-3 confirmation, so a Type-3-local patch would duplicate canonical logic.

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
Status: **IMPLEMENTATION MERGED / VERIFIED IN OWNER BUILD 4.83+**

- PR #142 merged as `193735e2079936003e87bfd0db39ba6585757aa3`.
- NMJE execution rejection authority is removed; observation/telemetry remains.
- Current Build 4.86 preserves Q1 and exact attributable runtime evidence.
- Issue-level tracking may remain open; do not recreate or reapply the repair.

### Q2 — Complete F7/C044 Build 4.82 infrastructure hardening
Issues: **#127 #132 #133 #138**
PR: **#140**
Priority: **CRITICAL / RUNTIME PROVENANCE + RESTART INTEGRITY**
Status: **IMPLEMENTATION MERGED / VERIFIED IN OWNER BUILD 4.82+**

- PR #140 merged as `30ac09675734da7bf4a23dae6b12faec8138f506`.
- Deterministic `[F7-BUILD]`, frozen exact-ticket open-time telemetry source path and generation-atomic C044 persistence are integrated.
- C044 deterministic model, static/cross-module guards, native 0E0W and isolated broker startup attribution passed.
- Residual live exact-ticket/runtime observations remain issue-level acceptance evidence; do not recreate Q2.

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
Issue: **#186**
Priority: **HIGH / INTEGRATION FREEZE**
Status: **VERIFIED / FROZEN — BUILD 4.86**

- Exact owner head at freeze: `b4772efc7cac5a7e3061473a4c1a7c4c305b1835`.
- Implementation parent: `beef83f94d8177959c085a827f8a425119065d16`.
- Raw Git MQ4 SHA-256: `D737A25FD01D6BA879118479401B5E7969DF20F528E53E43515852C555DD3308`.
- Verified EX4 SHA-256: `6A7116B26CDB7BA87B8CCC3415D2309BF414C32D274A66B4903D6E47FC93A5C6`.
- Q1/Q2/#175/#174/#173 lineage is integrated; post-Build-4.86 owner change is governance-only.
- Exact-source compile/regression/deterministic/cross-module/runtime evidence is reused; no new EA build or duplicate integration is justified.
- Freeze record: `blueprint/audits/Q7_BUILD486_INTEGRATED_CANDIDATE_FREEZE_20260917.md`.
- Q8 scoped GBPUSD engineering regression is complete; Q6 native final-authority residuals remain open and Q10 remains separately gated.

### Q8 — Regression/backtest programme
Issue: **#188**
Priority: **AFTER Q7 FROZEN CANDIDATE + Q6 USABLE HISTORICAL PROFILE**
Status: **VERIFIED / COMPLETE — GBPUSD ENGINEERING HISTORICAL EVIDENCE**

- Frozen lineage: Build `4.86` / `V486_STRUCTURAL_LIFETIME_20260917`.
- Scope executed: GBPUSD only; 2024, 2025 H1, 2025 H2, 2026 YTD through 2026-09-01 exclusive, plus bounded August-2026 smoke.
- Exact candidate MQ4/EX4 identity and six GBPUSD HST identities were freshly reverified before continuation.
- Offline tester used a separately hashed three-guard tester-only adapter; invariant verification proves no Strategy-Core/risk/execution/lifecycle semantic delta.
- Native harness compile 0E0W; every matrix run passed init/deinit, M15 chronology, M16->preflight->execution ordering, lifecycle coverage, duplicate/order and fatal-runtime checks.
- Performance results are descriptive only; no optimization/filter/rule was introduced.
- Evidence remains `ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE`.
- Audit: `blueprint/audits/Q8_BUILD486_GBPUSD_ENGINEERING_HISTORICAL_REGRESSION_20260918.md`.
- Q6 native archive/provenance and Q10 final broker/demo acceptance remain separate gates.

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
G40 was reachable during the 2026-09-17 Q7 reconciliation. Future work must still re-read actual local process/worktree/manifest state before any mutation.

G40-dependent active workstreams that require live-state recovery are **Q3 and Q6**. Q1/Q2 are already integrated and Q7 is frozen; do not recreate them. Q4 is mechanically complete and must not be re-added to the resume list without new evidence that a specific source unit is missing or invalid.

No destructive reset, blind recreation, automatic MT4 restart, or trading enablement is authorized by this queue.
