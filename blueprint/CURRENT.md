# BBMA Current Project State

Updated: **2026-09-09**
Status owner: **`d1-owner-dev`**
Owner head at reconciliation: **`262ff66dfdeed2cd4a7ac20fb82c47136db59451`**

This file is the active current-state record. The pre-2026-09-09 historical `CURRENT.md` is preserved byte-for-byte at `blueprint/archive/CURRENT_pre_20260909.md`.

## Authority
- GitHub `aliasmatrahim/BBMA-project` is authoritative for live project state.
- Strategy/source semantics are routed through `docs/references/SOURCE_INDEX.md` and the accepted Core/source evidence chain.
- Canonical active EA path: `blueprint/source/BBMA_EA.mq4`.
- Canonical owner source at this reconciliation: `Version 4.6.1 - F7 Re-Entry Lifecycle Integration`, property `4.61`, Git blob `6e629128f37c3fd482dd49e275360503f73fee68`.
- The owner source is not a production-readiness claim. Runtime/source attribution and several acceptance gates remain open.

## Current blocking workstreams

### 1. NMJE execution-authority repair — Issue #141 / Draft PR #142
Status: **CONFIRMED AUTHORITY VIOLATION / SOURCE FIX PENDING G40 NATIVE VALIDATION**.
- Current v4.61 can reject M15/M16-valid Re-Entry decisions through `NMJE_PassExecutionGate()`.
- Active M12N/N3 contract requires NMJE to remain observation/read-only; execution policy is not authorized.
- Remote PR #142 contains authority audit + test-first guard only.
- Branch: `fix/nmje-readonly-authority-141`.
- Head at reconciliation: `8aea5000a98252fc80d2d4ea36582bec73ffd964`.
- Intended unique candidate build: **4.83**.
- Required closure: smallest execution-neutral source fix, preserve N1/N2 telemetry, static/cross-module proof, native MetaEditor **0E0W**, targeted regression, attributable runtime evidence.
- No replacement NMJE strategy rule is authorized.

### 2. F7/C044 infrastructure hardening — Issues #127/#132/#133/#138 / Draft PR #140
Status: **REMOTE MODEL/AUDIT READY / LOCAL SOURCE PATCH PENDING G40 RECONCILIATION**.
- Branch: `upgrade/f7-infra-postfreeze-20260909`.
- Head at reconciliation: `f0147f6a211be916f773b8e3152a85a42752235c`.
- Intended unique candidate build: **4.82**.
- Scope: deterministic `[F7-BUILD]`, exact-ticket EXEC open time, live-vs-canonical F7 provenance reconciliation, generation-atomic C044 checkpoint/replay persistence.
- Remote PR contains model/audit/test files only; no remote EA-source implementation is claimed.
- An uncommitted local v4.82 source patch was observed on G40 before disconnect and must be preserved/re-read rather than overwritten.
- Required closure: strengthened atomicity/static regression + native MetaEditor **0E0W** before source push; physical/runtime acceptance remains separate.

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
Status: **MECHANICAL TRANSCRIPTION COMPLETE / SEMANTIC RECONCILIATION REMAINS OPEN**.
Fresh Source Autonomy recheck on 2026-09-16 from live G40 manifests and completion markers:
- 63 existing Primary-15/Group-3 manifests inspected;
- 63/63 are mechanically complete; missing units = 0;
- Primary-15 videos 01-04 also have completed `AUDIO_RECHECK_CORRECTED` outputs from the same `faster-whisper` / `standard-large-v3-turbo-ct2` engine; absence of chunk-style manifests for those four does not authorize a blind rerun;
- Group-3 remains mechanically complete;
- `ASR-DRAFT` remains source/research evidence only and is never Core authority.
Reconciliation remains fail-closed:
- A4/A5 retains 9 adjudication records: 6 `UNCLEAR`, 3 `PARTIAL`, 0 `MATCH`;
- 4 active A3 overlaps remain blocked, 2 A3 records remain excluded, 6 audio-recheck-empty review rows remain pending, and W004 retains its duplicate conflict;
- a mechanical media recheck confirms the six audio-recheck-empty source files contain audio streams, but this does not resolve their semantic uncertainty.
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

## Current infrastructure blocker
Authorized G40 Remote Desktop Commander device is **offline** at this reconciliation. Last seen: `2026-09-09T02:23:57.054+00:00` (10:23:57 Malaysia). Auth token remains valid.

An hourly condition watcher is configured to resume the five G40-dependent workstreams above only when the device becomes available. It must re-read actual local state before mutation.

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
- Do not merge PR #140/#142/#131 until their own evidence gates close.
- Do not invent a Strategy-Core rule to fill source uncertainty or improve historical profitability.
- Every EA source change requires a unique visible build identity and attributable native compile/runtime evidence.
