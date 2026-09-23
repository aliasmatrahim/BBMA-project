# BBMA Active Master Queue

Reconciled: **2026-09-20**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`f69492c85792f1e42624f7c796b4265335a38886`**

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

Q3 remains the active isolated runtime-validation workstream but is currently environment-blocked at `SEEN=58 / ACTIVE=0`. Q9 P1-P11 is verified in the scoped Draft research lineage with strict canonical JourneyID semantics; no Q9 activation or merge is authorized. The next eligible downstream re-audit from Issue #101 is D1TPW lifecycle. Q6 was stopped by explicit user decision on 2026-09-20 and Issue #128 is closed as not planned; do not auto-resume native acquisition. Q7 is frozen, GBPUSD Q8 is complete, and Q10 remains separately gated.

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
Status: **ACTIVE / PHASE H HISTORICAL COVERAGE; PHASE L LIVE RECONFIRMATION LAST**

The exact Build 5.11 candidate is frozen. Per explicit user decision on 2026-09-23, use both exact-candidate historical Strategy Tester evidence and MetaQuotes-Demo runtime evidence: historical tester first for deterministic/rare-scenario coverage, then live demo last for broker/runtime reconfirmation. Do not use the historical v4.59 runner or relabel engineering historical evidence as broker evidence. Evidence authority is defined by `blueprint/runtime/q10_demo_acceptance/FINAL_BUILD511_HYBRID_EVIDENCE_POLICY.json`. Current Phase H checkpoint: **55 PASS / 2 INCOMPLETE / 0 FAIL**. All currently safe non-HOLD Phase-H work is exhausted. R3-03 remains HOLD-UNRESOLVED under Issue #248 because fail-closed source behavior is proven but the acceptance-required observable transition scenario is not reachable/observed under the current immediate-EMA mapping. R5-19 remains conditional safe-only/INCOMPLETE; do not manufacture an emergency loss merely to force PASS. Phase L MetaQuotes-Demo remains last and is not yet formally allowed because mandatory R3-03 remains HOLD. R5-14 and R5-16 remain LIVE_ONLY broker-behavior cases. Current audit: `blueprint/audits/Q10_PHASE_H_GAP_CLOSURE_BUILD511_20260923.md`.

## Stage E - Deferred / future

### Q9 — NMJE v2 M5 accuracy hardening
Issue: **#101**
Scoped lineage: **Draft PRs #192-#205**
Priority: **HIGH / SHADOW-RESEARCH CORRECTNESS**
Status: **P1-P11 VERIFIED / CONTRACT STABILIZED / NO ACTIVATION**

Current state:
1. Do not rerun P1-P10; their exact scoped evidence remains reusable.
2. P11 decision A is locked as strict canonical JourneyID semantics.
3. Accepted P11: PR #205 head `0f80addc9080e726b8e6bb26a34094ae41ac3256`, Build `4.96`, source SHA-256 `B08CBDEFED1B1A6B6F0B9CADC3CA53B25BD3F98334E7E797A51D765F53E0C148`.
4. Build 4.95 lineage semantics are superseded; ParentEventID/JourneyID transition = NEW_JOURNEY, unchanged canonical root = FIRST, and CONTINUATION remains unproven without a separate source-owned continuation-event identity.
5. Static/model/persistence + native compile + deterministic GBPUSD tester authority regression PASS; broker actions=0.
6. Preserve canonical owner Build 4.86 unchanged. PR #205 stays Draft: no merge, no production activation, no P2 ordering activation, no M5 execution authority.
7. Next downstream sequence from Issue #101 is now eligible, in order:
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
