# BBMA Current Project State

Updated: **2026-09-23**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`e54bc1f8bacc9882c225aa5ac4b034380161e775`**

This file is the active current-state record. The pre-2026-09-09 historical `CURRENT.md` is preserved byte-for-byte at `blueprint/archive/CURRENT_pre_20260909.md`.

## Authority
- GitHub `aliasmatrahim/BBMA-project` is authoritative for live project state.
- Strategy/source semantics are routed through `docs/references/SOURCE_INDEX.md` and the accepted Core/source evidence chain.
- Canonical active EA path: `blueprint/source/BBMA_EA.mq4`.
- Canonical owner source: Build `5.11` / `V511_EVENT_DRIVEN_OBSERVER_20260922`; canonical normalized MQ4 SHA-256 `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`.
- Q7/Q8 Build 4.86 artifacts remain historical verified integration/regression evidence. Q10 is bound to the later exact Build 5.11 final integration candidate; this is still not a production-readiness claim.

## Current active workstreams / integrated state

### 1. NMJE read-only authority — Issue #141 / PR #142
Status: **IMPLEMENTATION MERGED / VERIFIED IN OWNER BUILD 4.83+**.
- PR #142 merged as `193735e2079936003e87bfd0db39ba6585757aa3`.
- NMJE remains observation-only: no create/reject/rank/execute authority under the active policy.
- Current Build 5.11 preserves the verified Q1 repair and attributable runtime proof.
- Issue-level tracking may remain open, but this implementation prerequisite no longer blocks Q7.

### 2. F7/C044 infrastructure hardening — Issues #127/#132/#133/#138 / PR #140
Status: **IMPLEMENTATION MERGED / VERIFIED IN OWNER BUILD 4.82+**.
- PR #140 merged as `30ac09675734da7bf4a23dae6b12faec8138f506`.
- Deterministic build identity, exact-ticket frozen open-time telemetry source path and generation-atomic C044 persistence are integrated.
- Deterministic C044 model, static/cross-module guards and native compile passed; current Build 5.11 preserves this lineage.
- Residual issue-level live exact-ticket/runtime observations remain separate and do not require recreating Q2 for Q7.

### 3. C10 Build 4.81 runtime closure — Issues #122/#123 / Draft PR #131
Status: **SOURCE/STATIC/NATIVE COMPILE PASS / FINAL BROKER-CLOCK RESTART GATE PENDING**.
- Exact BuildID: `4.81`.
- Source SHA-256: `5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57`.
- C10 SourceHash: `D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D`.
- Runtime config: `E376D23AA953085D`, InstanceID `81`, `ExpertsTrades=false`, zero trade caps, `Authority=NONE`.
- Fresh G40 recheck on 2026-09-23: isolated terminal PID `13064` remains alive and untouched. Exact InstanceID 81 checkpoint ledger is now `SEEN=91 / ACTIVE=0` (92 rows including header), SHA-256 `35262817B7271519F0CD8FAA9BF4DF56FE4BF7819012C635C1207984B576A909`, last write `2026-09-23T06:39:42+08:00`. This supersedes the older `58/0` count but does not change the gate. No restart or synthetic ACTIVE was performed.
- Classification remains **NOT RUNTIME VERIFIED / RUNTIME-ENVIRONMENT BLOCKED** until the exact natural gate is observable.
- Final gate: genuine fresh `ACTIVE` -> same isolated terminal physical stop/restart -> exact recovery -> hardened verifier PASS -> no malformed/duplicate rows, no ledger disable, zero broker actions.
- Build 4.80 or Strategy Tester evidence cannot substitute for this exact 4.81 gate.

### 4. Primary-15 source transcription / reconciliation
Status: **MECHANICAL TRANSCRIPTION COMPLETE / A4-A5 SEMANTIC BLOCKERS RESOLVED / G40-WIDE STRICT SOURCE RECONCILIATION COMPLETE; EXPLICIT NON_CORE/HOLD BOUNDARIES RETAINED**.
Fresh Source Autonomy recheck on 2026-09-16 from live G40 manifests and completion markers:
- 63 existing Primary-15/Group-3 manifests inspected;
- 63/63 are mechanically complete; missing units = 0;
- Primary-15 videos 01-04 also have completed `AUDIO_RECHECK_CORRECTED` outputs from the same `faster-whisper` / `standard-large-v3-turbo-ct2` engine; absence of chunk-style manifests for those four does not authorize a blind rerun;
- Group-3 remains mechanically complete;
- `ASR-DRAFT` remains source/research evidence only and is never Core authority.
Q5 A4/A5 semantic reconciliation is fail-closed under `blueprint/audits/BBMA_Q5_A4A5_SEMANTIC_RESOLUTION_20260916.md`:
- the 9 retained rows resolve to 6 `CORROBORATION_ONLY` + 3 `REJECTED`; Strategy-Core semantic `UNCLEAR`/`PARTIAL` = 0, `SOURCE_CONFLICT` = 0 and `ACCEPTED_CORE` = 0;
- the historical 4 A3 blocked overlaps, 2 excluded A3 records, 6 audio-recheck-empty review rows and W004 duplicate conflict remain preserved as provenance/transcript-QA states only, not Strategy-Core blockers;
- exact-wording uncertainty remains for five bounded transcript fragments and must not be normalized into source text without materially better evidence;
- the six audio-recheck-empty source files contain audio streams, and local Finale V07 media is now recovered in the source-audit workspace; neither fact creates new Core authority.
Strict G40-wide closure on 2026-09-25 additionally inventories/routes the forum archive, extra-deep discovery queue, local Tier-A-priority/direct-Oma-labelled intake, Roohi external-practitioner set and Tier-C derivative taxonomy. Momentum `-nMZUF1Bx0k` and Personal Meeting Room `hqzptZ9uRmg` are now mechanically covered and semantically adjudicated with targeted large-model/visual evidence where material. Result: **PASS WITH EXPLICIT NON_CORE/HOLD BOUNDARIES; ACCEPTED CORE DELTA NONE**. Closure: `blueprint/audits/G40_FINAL_RECONCILIATION_CLOSURE_20260925.md`.
Rules:
- do not rerun completed manifests/chunks blindly;
- no transcript directly creates a production rule; reconcile through the Section 17 source hierarchy first;
- HOLD/PARTIAL/UNCLEAR evidence remains non-executable until explicit reconciliation.

### 5. GBPUSD historical engineering profile / Q6 closure — Issue #128
Status: **Q6 STOPPED BY USER / ISSUE #128 CLOSED NOT PLANNED / GBPUSD ENGINEERING PROFILE VERIFIED**.
- User decision on 2026-09-20 stops the full three-pair Dukascopy-native Q6 archive. It must not auto-resume without a new explicit instruction.
- Live G40 acquisition processes were stopped and rechecked; local range state is `STOPPED_BY_USER`. Existing verified native progress (17/720 pair-months) and partial artifacts are retained as historical evidence only.
- The separate GBPUSD-only native archive is **not** complete: `0/240` native-only months under `native_archive_gbpusd_progress.json`. This native-only objective is not required for the retained engineering tester profile and is no longer active.
- GBPUSD Jetta/raw-tick range is COMPLETE: `240/240` months, pending=0.
- GBPUSD derived-v9 artifact integrity is PASS: 252 files, 19,254,140 checked rows, 0 errors.
- GBPUSD derived-v9 cross-timeframe reconciliation M1 -> M5 -> M15 -> H1 -> H4/D1 is PASS with 0 errors.
- Full GBPUSD 2006-09 through 2026-08 native/Jetta tick-to-derived M1 reconciliation v3 is PASS: 240 months, failedMonthCount=0.
- All six installed GBPUSD HST files were freshly SHA-256 reverified on 2026-09-20 and exactly match the Q8 evidence manifest.
- Build 4.86 EX4 and the Q8 tester harness EX4 were also freshly hash-matched to the Q8 evidence manifest.
- Q8 Build 4.86 GBPUSD engineering historical regression remains VERIFIED / COMPLETE.
- Classification: **READY FOR ISOLATED ENGINEERING STRATEGY TESTER USE / NOT FINAL TICK-ACCURATE / NOT DEPLOYMENT-BROKER CANONICAL**.
- No EA Strategy-Core/code change is implied by this scope decision.

### 6. Q7 integrated candidate freeze — Issue #186
Status: **VERIFIED / FROZEN**.
- Exact owner head `b4772efc7cac5a7e3061473a4c1a7c4c305b1835`; implementation parent `beef83f94d8177959c085a827f8a425119065d16`.
- Raw owner MQ4 bytes equal verified Build 4.86 bytes; no protected EA/Core/contract change exists after the implementation parent.
- Exact Build 4.86 EX4 SHA-256 remains `6A7116B26CDB7BA87B8CCC3415D2309BF414C32D274A66B4903D6E47FC93A5C6`.
- Freeze record: `blueprint/audits/Q7_BUILD486_INTEGRATED_CANDIDATE_FREEZE_20260917.md`.
- Q8 scoped GBPUSD engineering regression is complete under Issue #188; Q6 native acquisition was stopped/closed on 2026-09-20 and Q3 continues independently.

### 7. Q8 Build 4.86 GBPUSD engineering historical regression — Issue #188
Status: **VERIFIED / COMPLETE — ENGINEERING HISTORICAL EVIDENCE ONLY**.
- Scope: GBPUSD only; 2024, 2025 H1, 2025 H2 and 2026 YTD through 2026-09-01 exclusive.
- Exact Build 4.86 source/binary identity and all six installed GBPUSD HST identities were freshly reverified.
- Offline Strategy Tester required a test-only three-guard environment adapter; invariant audit proves no Strategy-Core/risk/execution/lifecycle semantic delta.
- Native harness compile: 0 errors / 0 warnings; all four matrix periods and the August-2026 smoke passed mechanism/runtime acceptance.
- Deep matrix: 1,045 executions, zero duplicate executed DecisionIDs/tickets, zero execution-order/closed-candle chronology defects and zero targeted fatal runtime faults.
- Audit: `blueprint/audits/Q8_BUILD486_GBPUSD_ENGINEERING_HISTORICAL_REGRESSION_20260918.md`.
- This remains engineering historical evidence and is not a profitability or production-readiness claim. The former Issue #128 native final-authority programme was later stopped by user decision and closed not planned on 2026-09-20.

## Current infrastructure blocker
Authorized G40 Remote Desktop Commander is reachable. Q3 isolated Build 4.81 runtime remains separate/environment-blocked on primary PID 13064. Q10 Phase-L now uses the merged `Q10_20PAIR_R2_20260923` MetaQuotes-Demo profile on one dedicated terminal: 20 broker-supported fixed-ID pairs are monitored, `MaxActivePair=1`, and all other approved risk/MM/execution settings remain unchanged. Do not conflate or restart the Q3 terminal. Q9 P11 remains a verified scoped Draft research branch with no production activation. Q6 native acquisition was stopped by explicit user decision on 2026-09-20 and must not auto-resume.

## Recently closed tracking/governance work
- stale v4.58 CI PR-gate bug #136 closed; workflow-only fix merged.
- D1 Package-B re-audit merged: current M11 -> M15 -> M16 is already integrated; old queue text describing it as unimplemented is historical/stale.
- project-governance drift #111 and live-status resolution #113 closed by documentation-only governance merge `262ff66...`.
- historical one-shot trigger issues/PRs and validation-only PRs that explicitly said `do not merge` were closed without deleting their branches/evidence.
- Issue #109 is active on exact Build 5.11 under hybrid tester-first / MetaQuotes-Demo-last acceptance. The older R3-only status is superseded by the 2026-09-24 exact-R2 runtime checkpoint. Formal local Phase-L state is now **R3 PASS / R4 PASS / R5 INCOMPLETE / R6 NOT PROMOTED**. R5 mandatory live/reconfirm PASS cases are `R5-00/R5-01/R5-11/R5-12/R5-13/R5-20`; the only mandatory blockers are **R5-14** (natural server blank/replaced broker comment) and **R5-16** (natural safe retryable OrderSend error 135/138/146), with no mandatory R5 FAIL. USDCHF ticket `1629172566` / hash `CA000D516825BB44` survived a guarded graceful restart as the same persisted identity with `Monitored=1`; no duplicate ticket was observed. Exact candidate/source/EX4/settings identity is unchanged. Evidence: `blueprint/audits/Q10_PHASE_L_R5_LIVE_STATE_20260924.md`.

### 8. Q9 NMJE v2 / M5 accuracy hardening — Issue #101
Status: **BUILD 5.12 P2/P3 SHADOW REMATERIALIZATION VALIDATED / P2 ORDERING HOLD / M5 EXECUTION AUTHORITY NONE**.
- Q9 P1-P11 Draft/scoped research lineage #192-#205 remains non-activated against canonical owner Build 5.11; NMJE remains observation-only and M5 remains closed-candle context/shadow only. Subsequent Issue #101 downstream production-owner audits/fixes through Build 5.11 were completed separately and must not be requeued.
- User decision A locks strict canonical JourneyID semantics for P11.
- Accepted P11 head: PR #205 commit `0f80addc9080e726b8e6bb26a34094ae41ac3256`, Build `4.96` / `V496_Q9_P11_STRICT_JOURNEY_LINEAGE_20260920`, MQ4 SHA-256 `B08CBDEFED1B1A6B6F0B9CADC3CA53B25BD3F98334E7E797A51D765F53E0C148`.
- ParentEventID/JourneyID transition is NEW_JOURNEY; unchanged canonical root is FIRST; CONTINUATION is not inferred without a distinct source-owned continuation-event identity.
- Legacy Build 4.95 higher-owner-root semantics are superseded; durable 4.95 CONTINUATION loads fail-closed as UNRESOLVED under 4.96.
- Exact P10/P11 authority trace remains 2,092/2,092 equal; final tester lineage per run: FIRST=1988, NEW_JOURNEY=28, CONTINUATION=0; broker actions=0.
- Canonical/runtime/tester native MetaEditor compile = 0 errors / 0 warnings.
- PR #205 remains Draft provenance only: **DO NOT DIRECT-MERGE / NO PRODUCTION ACTIVATION / NO P2 ACTIVATION / NO M5 EXECUTION AUTHORITY**.
- 2026-09-25 V1↔V2 current-owner reconciliation against Build 5.11: P1 identity substrate is already integrated/equivalent; P2-P8/P10/P11 remain bounded research/shadow concepts. PR #205 is 164 commits behind live owner and must be rematerialized from current owner if research resumes. Current-owner code fix = `NONE`. Audit: `blueprint/audits/NMJE_V1_V2_CURRENT_OWNER_IMPLEMENTATION_RECONCILIATION_20260925.md`.
- Fresh current-owner P2/P3 rematerialization is validated as Build `5.12` / `V512_NMJE_P2P3_SHADOW_20260925`, source rev `NMJE_P2P3_SHADOW_003_20260925`, source SHA-256 `D80FA8D1A11A1FBAFFEC1F2E3FFF029DBAAB96BB58D89C29EDEBC25830379D1E`, EX4 SHA-256 `DECCE17D2BAC0694A9A25C4C66C7828DE520D7EFBA4A977FF6703C5B4EECD252`. Native compile 0E/0W, targeted regression PASS and isolated GBPUSD M15 Strategy Tester runtime/order coverage PASS. P2 remains telemetry-only; P3 remains latest-closed-M5 shadow context only. Audit: `blueprint/audits/NMJE_V2_P2_P3_CURRENT_OWNER_REMATERIALIZATION_20260925.md`.
- Legacy N2/N3 v4.58 workflows are historical manual-dispatch checks pinned to immutable v4.58 revisions; they no longer gate/misroute current-owner EA PRs.
- Issue #101 downstream production-owner sequence is completed through final integration; do not requeue D1TPW/C044/D1O/M17/TradeLock-risk/N1-N2-N3/M25/Observer/cross-module work without new evidence.

## Deferred / future work
- final automated broker/demo user-test programme (#109): **ACTIVE** on exact frozen Build 5.11 with merged 20-pair R2 profile. The dedicated terminal is collecting fresh R2 R3 evidence; the rare gating event remains natural D1O restart continuity (`R3-12`).
- older dashboard/observer preparation branches are historical staging. Re-audit against the then-current owner before any future materialization; do not merge an old frozen-candidate patch directly.

## Safety boundary
- No primary MT4 restart is authorized by this status record.
- Do not enable trading or lifecycle authority merely because static/native tests pass.
- PR #140 and #142 are already merged into the verified lineage; PR #131 remains gated by its exact C10 runtime acceptance.
- Do not invent a Strategy-Core rule to fill source uncertainty or improve historical profitability.
- Every EA source change requires a unique visible build identity and attributable native compile/runtime evidence.
