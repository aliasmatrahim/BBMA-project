# BBMA Current Project State

Updated: **2026-09-17**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`b4772efc7cac5a7e3061473a4c1a7c4c305b1835`**

This file is the active current-state record. The pre-2026-09-09 historical `CURRENT.md` is preserved byte-for-byte at `blueprint/archive/CURRENT_pre_20260909.md`.

## Authority
- GitHub `aliasmatrahim/BBMA-project` is authoritative for live project state.
- Strategy/source semantics are routed through `docs/references/SOURCE_INDEX.md` and the accepted Core/source evidence chain.
- Canonical active EA path: `blueprint/source/BBMA_EA.mq4`.
- Canonical owner source: Build `4.86` / `V486_STRUCTURAL_LIFETIME_20260917`; raw Git MQ4 SHA-256 `D737A25FD01D6BA879118479401B5E7969DF20F528E53E43515852C555DD3308`.
- Q7 freezes this exact Build 4.86 source as the integrated candidate under Issue #186; this is not a production-readiness claim.

## Current active workstreams / integrated state

### 1. NMJE read-only authority — Issue #141 / PR #142
Status: **IMPLEMENTATION MERGED / VERIFIED IN OWNER BUILD 4.83+**.
- PR #142 merged as `193735e2079936003e87bfd0db39ba6585757aa3`.
- NMJE remains observation-only: no create/reject/rank/execute authority under the active policy.
- Current Build 4.86 preserves the verified Q1 repair and attributable runtime proof.
- Issue-level tracking may remain open, but this implementation prerequisite no longer blocks Q7.

### 2. F7/C044 infrastructure hardening — Issues #127/#132/#133/#138 / PR #140
Status: **IMPLEMENTATION MERGED / VERIFIED IN OWNER BUILD 4.82+**.
- PR #140 merged as `30ac09675734da7bf4a23dae6b12faec8138f506`.
- Deterministic build identity, exact-ticket frozen open-time telemetry source path and generation-atomic C044 persistence are integrated.
- Deterministic C044 model, static/cross-module guards and native compile passed; current Build 4.86 preserves this lineage.
- Residual issue-level live exact-ticket/runtime observations remain separate and do not require recreating Q2 for Q7.

### 3. C10 Build 4.81 runtime closure — Issues #122/#123 / Draft PR #131
Status: **SOURCE/STATIC/NATIVE COMPILE PASS / FINAL BROKER-CLOCK RESTART GATE PENDING**.
- Exact BuildID: `4.81`.
- Source SHA-256: `5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57`.
- C10 SourceHash: `D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D`.
- Runtime config: `E376D23AA953085D`, InstanceID `81`, `ExpertsTrades=false`, zero trade caps, `Authority=NONE`.
- Last attributable pre-disconnect state: no final PASS/FAIL; checkpoint remained SEEN-only, no broker actions/ledger disable in reviewed target-domain evidence.
- Final gate: genuine fresh `ACTIVE` -> same isolated terminal physical stop/restart -> exact recovery -> hardened verifier PASS -> no malformed/duplicate rows, no ledger disable, zero broker actions.
- Build 4.80 or Strategy Tester evidence cannot substitute for this exact 4.81 gate.

### 4. Primary-15 source transcription / reconciliation
Status: **MECHANICAL TRANSCRIPTION COMPLETE / A4-A5 STRATEGY-CORE SEMANTIC BLOCKERS RESOLVED; TRANSCRIPT-QA RESIDUALS RETAINED**.
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
Rules:
- do not rerun completed manifests/chunks blindly;
- no transcript directly creates a production rule; reconcile through the Section 17 source hierarchy first;
- HOLD/PARTIAL/UNCLEAR evidence remains non-executable until explicit reconciliation.

### 5. Canonical historical-data environment — Issue #128
Status: **SYNTHETIC-V3 HST/TESTER GATES PASS / FULL NATIVE TICK ARCHIVE INCOMPLETE**.
- Pairs: EURUSD, GBPUSD, USDJPY.
- Target native window: 2006-09-01 through 2026-09-01 exclusive.
- Synthetic-v3 HST binary/cross-TF/full-history command-line tester gates have passed for the engineering profile.
- Synthetic profile remains engineering-only and is not tick-accurate.
- First native pilot EURUSD 2006-09 is COMPLETE: 720/720 valid expected hours, archive entries=720, archive SHA-256 `6e0975c7ca1454ba1056f8b189c0e21f639936683bfa4f115a87bd823cf21f79`.
- Last recorded orchestrator state had advanced to EURUSD 2006-10 using `BBMA_NATIVE_WORKERS=1` with a >120 GB free-space guard.
- Resume from the first incomplete verified pair-month only; do not redownload COMPLETE archive+SHA months.
- Final tick-accurate claims remain blocked until all 720 target pair-months and remaining provenance/session/deployment-mapping gates close.

### 6. Q7 integrated candidate freeze — Issue #186
Status: **VERIFIED / FROZEN**.
- Exact owner head `b4772efc7cac5a7e3061473a4c1a7c4c305b1835`; implementation parent `beef83f94d8177959c085a827f8a425119065d16`.
- Raw owner MQ4 bytes equal verified Build 4.86 bytes; no protected EA/Core/contract change exists after the implementation parent.
- Exact Build 4.86 EX4 SHA-256 remains `6A7116B26CDB7BA87B8CCC3415D2309BF414C32D274A66B4903D6E47FC93A5C6`.
- Freeze record: `blueprint/audits/Q7_BUILD486_INTEGRATED_CANDIDATE_FREEZE_20260917.md`.
- Q6 is sequenced next before Q8; Q3 continues independently in isolated shadow runtime.

## Current infrastructure blocker
Authorized G40 Remote Desktop Commander was reachable during the 2026-09-17 Q7 recovery. Active live-state work remains Q3 isolated runtime and Q6 archive resumption; all must re-read actual local state before mutation.

## Recently closed tracking/governance work
- stale v4.58 CI PR-gate bug #136 closed; workflow-only fix merged.
- D1 Package-B re-audit merged: current M11 -> M15 -> M16 is already integrated; old queue text describing it as unimplemented is historical/stale.
- project-governance drift #111 and live-status resolution #113 closed by documentation-only governance merge `262ff66...`.
- historical one-shot trigger issues/PRs and validation-only PRs that explicitly said `do not merge` were closed without deleting their branches/evidence.
- Issue #109 is deferred/reframed for the **final integration candidate**, not historical v4.59.

## Deferred / future work
- Issue #101 NMJE v2 / M5 accuracy hardening: do not resume until the current NMJE read-only baseline/authority conflict is closed and current owner lineage is re-established. M5 remains context/shadow-only unless a separately approved policy changes that.
- final automated broker/demo user-test programme (#109): run only after one exact final integration candidate is frozen and preceding native/historical/regression gates pass.
- older dashboard/observer preparation branches are historical staging. Re-audit against the then-current owner before any future materialization; do not merge an old frozen-candidate patch directly.

## Safety boundary
- No primary MT4 restart is authorized by this status record.
- Do not enable trading or lifecycle authority merely because static/native tests pass.
- PR #140 and #142 are already merged into the verified lineage; PR #131 remains gated by its exact C10 runtime acceptance.
- Do not invent a Strategy-Core rule to fill source uncertainty or improve historical profitability.
- Every EA source change requires a unique visible build identity and attributable native compile/runtime evidence.
