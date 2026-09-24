# BBMA Active Master Queue

Reconciled: **2026-09-23**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`e54bc1f8bacc9882c225aa5ac4b034380161e775`**

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
- **Parallel validation / research:** Q3 + Q9 (Q6 stopped/closed; GBPUSD engineering profile retained)
- **Integration / final acceptance:** Q7 -> Q8 -> Q10
- **Deferred / future:** Q11

Q3 remains a separate isolated runtime-validation workstream and is environment-blocked at `SEEN=91 / ACTIVE=0` on the exact InstanceID 81 ledger; do not disturb its primary PID 13064. Q9 P1-P11 remains verified scoped Draft research with no activation, while the subsequent Issue #101 downstream sequence (D1TPW -> C044 -> D1/D1O -> M17 -> TradeLock/risk/execution -> N1/N2/N3 -> M25 -> Observer -> cross-module -> final integration) is already completed and must not be requeued. Q6 remains stopped/closed. Q7/Q8 historical gates are complete. **Q10 Phase L R5 is the highest-priority active final-acceptance task. R3 and R4 are formally PASS; R5 remains the first incomplete stage.**

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
Status: **COMPLETE / G40-WIDE STRICT RECONCILIATION PASS / TRANSCRIPT-QA + NON_CORE/HOLD BOUNDARIES NON-BLOCKING**

Current semantic state after Issue #169 / PR #170 and full Q5 Issue #176 closure:
- 9 retained records = 6 `CORROBORATION_ONLY` + 3 `REJECTED`; Strategy-Core semantic `UNCLEAR`/`PARTIAL` = 0;
- no row is promoted to `ACCEPTED_CORE`, no source conflict is created and no detector/filter/timing authority is added;
- 4 historical A3 blocked overlaps, 2 excluded A3 records, 6 `AUDIO_RECHECK_EMPTY` rows and W004 duplicate-conflict remain retained as provenance/transcript-QA residuals only;
- five exact-wording fragments remain uncertain and non-executable pending materially better evidence;
- these transcript-QA residuals do not block accepted Core semantics or authorize production changes;
- Issue #180 / PR #183 is closed unmerged because current owner Build 4.86 already contains the shared MA5/MA10 close-side guard before Type-3 confirmation, so a Type-3-local patch would duplicate canonical logic.
- 2026-09-25 strict G40-wide source audit is complete: all discovered U1-U6 families now have route/dedup/evidence/authority dispositions; Momentum and Personal Meeting Room media blockers are reconciled; accepted Core delta = `NONE`; news-specific/personal/derivative/ambiguous material remains explicitly NON_CORE/HOLD.
- Final closure: `blueprint/audits/G40_FINAL_RECONCILIATION_CLOSURE_20260925.md`.

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

Fresh 2026-09-23 read-only ledger checkpoint: `SEEN=91 / ACTIVE=0`; ledger SHA-256 `35262817B7271519F0CD8FAA9BF4DF56FE4BF7819012C635C1207984B576A909`. The higher `SEEN` count does not satisfy the restart gate; `ACTIVE=0` still forbids progression to stop/restart recovery validation.

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

### Q6 — Canonical Dukascopy-native 3-pair archive
Issue: **#128 — CLOSED / NOT PLANNED**
Priority: **STOPPED**
Status: **STOPPED BY USER 2026-09-20 / DO NOT AUTO-RESUME**

Final active-state handling:
1. Full EURUSD/GBPUSD/USDJPY native acquisition is no longer an active project requirement.
2. Live G40 runner/downloader processes were stopped and rechecked; local range progress is `STOPPED_BY_USER`.
3. Preserve the verified 17/720 native pair-months and any partial artifacts as historical evidence; do not delete or silently promote them.
4. The separate GBPUSD native-only archive remains 0/240 and is not being pursued.
5. For isolated historical tester work, use the already-verified GBPUSD engineering profile:
   - Jetta/raw-tick range 240/240 COMPLETE;
   - derived-v9 artifact integrity PASS;
   - cross-TF reconciliation PASS;
   - full 2006-09..2026-08 tick-to-derived reconciliation PASS;
   - six installed GBPUSD HST identities hash-match Q8 evidence;
   - Q8 Build 4.86 engineering regression VERIFIED / COMPLETE.
6. Evidence classification remains **ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE / NOT DEPLOYMENT-BROKER CANONICAL**.
7. A future native-archive restart requires a new explicit user instruction.


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
- Q8 scoped GBPUSD engineering regression is complete; Q6 native acquisition is stopped/closed and Q10 remains separately gated.

### Q8 — Regression/backtest programme
Issue: **#188**
Priority: **AFTER Q7 FROZEN CANDIDATE + VERIFIED GBPUSD ENGINEERING HISTORICAL PROFILE**
Status: **VERIFIED / COMPLETE — GBPUSD ENGINEERING HISTORICAL EVIDENCE**

- Frozen lineage: Build `4.86` / `V486_STRUCTURAL_LIFETIME_20260917`.
- Scope executed: GBPUSD only; 2024, 2025 H1, 2025 H2, 2026 YTD through 2026-09-01 exclusive, plus bounded August-2026 smoke.
- Exact candidate MQ4/EX4 identity and six GBPUSD HST identities were freshly reverified before continuation.
- Offline tester used a separately hashed three-guard tester-only adapter; invariant verification proves no Strategy-Core/risk/execution/lifecycle semantic delta.
- Native harness compile 0E0W; every matrix run passed init/deinit, M15 chronology, M16->preflight->execution ordering, lifecycle coverage, duplicate/order and fatal-runtime checks.
- Performance results are descriptive only; no optimization/filter/rule was introduced.
- Evidence remains `ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE`.
- Audit: `blueprint/audits/Q8_BUILD486_GBPUSD_ENGINEERING_HISTORICAL_REGRESSION_20260918.md`.
- Q6 native archive work was later stopped/closed on 2026-09-20; Q10 final broker/demo acceptance remains separately gated.

### Q10 — Hybrid historical coverage + final MetaQuotes-Demo acceptance
Issue: **#109**
Status: **ACTIVE / PHASE L LIVE RECONFIRMATION / R3 NATURAL D1O RESTART GATE**

The exact Build 5.11 source/EX4 candidate is frozen. Phase H remains **56 PASS / 1 conditional INCOMPLETE / 0 FAIL**; R5-19 is the approved safe-only conditional case and must not be manufactured. PR #265 merged the final-live `Q10_20PAIR_R2_20260923` settings revision: the only functional settings delta is PairList expansion from GBPUSD to 20 MetaQuotes-Demo-supported fixed-ID FX pairs, with `MaxActivePair=1` and all other approved risk/MM/execution settings unchanged. Read-only broker smoke passed 20/20 resolution/specification plus PairID/Magic isolation. V2 stage evidence binds exact EX4 + settings SHA, so legacy GBPUSD-only Phase-L bundles cannot be combined into R2 evidence. Formal exact-R2 Phase-L state is now `R3 = PASS`, `R4 = PASS`, `R5 = INCOMPLETE`, and `R6 = NOT PROMOTED`. R5 live/reconfirm PASS cases are `R5-00/R5-01/R5-11/R5-12/R5-13/R5-20`; the only mandatory blockers are **R5-14** (natural server blank/replaced broker comment) and **R5-16** (natural safe retryable OrderSend error 135/138/146), with no mandatory R5 FAIL. The dedicated exact-R2 terminal remains running; neither broker condition may be synthesized. R6 cannot be formally promoted until R5 passes. Current runtime audit: `blueprint/audits/Q10_PHASE_L_R5_LIVE_STATE_20260924.md`.

## Stage E - Deferred / future

### Q9 — NMJE v2 M5 accuracy hardening
Issue: **#101**
Scoped lineage: **Draft PRs #192-#205**
Priority: **HIGH / SHADOW-RESEARCH CORRECTNESS**
Status: **V1↔V2 CURRENT-OWNER RECONCILIATION COMPLETE / P1 INTEGRATED / P2-P11 RESEARCH-ONLY / NO ACTIVATION**

Current state:
1. Do not rerun P1-P10; their exact scoped evidence remains reusable.
2. P11 decision A is locked as strict canonical JourneyID semantics.
3. Accepted P11: PR #205 head `0f80addc9080e726b8e6bb26a34094ae41ac3256`, Build `4.96`, source SHA-256 `B08CBDEFED1B1A6B6F0B9CADC3CA53B25BD3F98334E7E797A51D765F53E0C148`.
4. Build 4.95 lineage semantics are superseded; ParentEventID/JourneyID transition = NEW_JOURNEY, unchanged canonical root = FIRST, and CONTINUATION remains unproven without a separate source-owned continuation-event identity.
5. Static/model/persistence + native compile + deterministic GBPUSD tester authority regression PASS; broker actions=0.
6. Current owner Build 5.11 already contains the P1 provenance identity substrate. PR #205 is retained as verified historical research provenance only and must **not** be direct-merged: live compare shows it 164 commits behind current owner. Any resumed P2-P8/P10/P11 work must be rematerialized from the then-current owner; P2 ordering remains HOLD and M5 remains shadow-only.
7. Current-owner reconciliation audit: `blueprint/audits/NMJE_V1_V2_CURRENT_OWNER_IMPLEMENTATION_RECONCILIATION_20260925.md`; current-owner code fix = `NONE`, accepted Core delta = `NONE`.
8. Issue #101 downstream sequence is **COMPLETED through final integration**; the following list is retained as completed order and must not be requeued without new evidence:
   - D1TPW lifecycle re-audit;
   - C044 lifecycle;
   - D1/D1O identity & dedup;
   - M17 validation/SL geometry;
   - TradeLock/cumulative risk/execution ambiguity;
   - N1/N2/N3 end-to-end provenance/firewall;
   - M25 dashboard materialization;
   - Observer finalization;
   - M01-M27 + M12N cross-module audit;
   - final integration candidate/tests/backtest;
   - final MetaQuotes-Demo runtime acceptance last (Issue #109; user-selected demo provider, 2026-09-23).
8. Old PR #102/#126 lineage remains historical/staging evidence only; do not merge it directly.

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

G40-dependent live process state is **Q3** (watcher/isolated terminal preserved; environment-blocked). Q9 P11 is now verified and pushed to its scoped Draft branch; do not merge/activate it through this queue. Q6 native acquisition is stopped/closed and must not auto-resume. Q1/Q2 are already integrated and Q7 is frozen; do not recreate them. Q4 is mechanically complete and must not be re-added without new evidence.

No destructive reset, blind recreation, automatic MT4 restart, or trading enablement is authorized by this queue.
