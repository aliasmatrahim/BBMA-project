# BBMA Work Session Log

Purpose: technical audit trail for BBMA Professional EA development. This log distinguishes work performed in normal Chat vs Work mode and provides a traceable handoff for later verification.

## Rules

- Record only meaningful project changes, validation events, or audit checkpoints.
- `MODE` must be `CHAT` or `WORK`.
- Link each entry to a Git commit/hash or local Git state whenever available.
- Do not mark a change `VERIFIED` from memory alone; verification must come from actual compile/runtime/log/code evidence.
- Forward-runtime evidence must identify the active MT4 Data Folder/log path and exact build/marker.
- For NMJE v4.5.9, only evidence explicitly traceable to `BBMA_EA_V459_NMJE_FORWARD` is valid. Ignore C10, Strategy Tester, old builds, and unrelated historical evidence.
- A genuine NMJE outcome is usable only when `[N1-NMJE]` -> `[N2-NMJE-DEC]` -> `[N2-NMJE-OUT]` can be correlated by `DID/DIDH`, pair/symbol, and identity consistently.

## Permanent Session-Logging Workflow

This workflow applies to all future BBMA technical work.

1. At the start of a meaningful task, classify the execution source as `CHAT` or `WORK`.
2. Before changing source/config/architecture, capture the best available baseline: branch + commit/HEAD and local dirty state when accessible.
3. Record an entry whenever work produces a meaningful code/config/architecture change, compile result, runtime result, validation result, regression finding, or audit checkpoint.
4. Small explanations, status questions, or discussions that do not change project state do not require an entry.
5. Every entry must identify the affected scope/modules and distinguish implementation from validation.
6. A code change performed in `CHAT` remains `PENDING` until it is verified by evidence. When `WORK` later audits it, add a new `WORK` verification entry rather than rewriting its origin.
7. Never relabel work originally performed in `CHAT` as `WORK`, or vice versa. Verification mode and implementation mode are separate facts.
8. Where available, use Git commit/hash as the primary technical anchor. If changes are still local/uncommitted, record branch/HEAD + dirty/local-diff state instead.
9. Runtime/MT4 evidence must record the verified active Data Folder/log path and exact build/marker; stale or unrelated logs are invalid evidence.
10. Before a build is treated as locked/production-ready, all meaningful `CHAT` deltas since the last known-good `WORK` baseline must be audited and classified `VERIFIED`, `FAILED`, `PENDING`, or `SUPERSEDED`.

### Identification Rule

- `ORIGIN MODE` = where the implementation/change was actually performed.
- `VERIFY MODE` = where that change was later audited/validated.
- A change may therefore be `ORIGIN MODE: CHAT` and later `VERIFY MODE: WORK`.
- Git history + Desktop Commander local state + this log together form the audit trail. Memory alone is not sufficient evidence.

## Status Values

- `PENDING` — work/evidence exists but verification is incomplete.
- `VERIFIED` — independently checked and accepted.
- `FAILED` — validation failed or a confirmed defect exists.
- `SUPERSEDED` — replaced by a newer implementation/evidence set.

## Entry Template

```text
DATE/TIME:
ORIGIN MODE: CHAT | WORK
VERIFY MODE: CHAT | WORK | NONE
SCOPE/MODULES:
BASELINE/COMMIT:
LOCAL STATE:
CHANGE/ACTION:
REASON:
COMPILE STATUS:
RUNTIME STATUS:
VALIDATION STATUS: PENDING | VERIFIED | FAILED | SUPERSEDED
EVIDENCE:
ISSUE/RISK:
NEXT GATE:
```

---

## 2026-09-04 — Chat-mode continuation checkpoint

DATE/TIME: 2026-09-04 (Malaysia time)
ORIGIN MODE: CHAT
VERIFY MODE: NONE
SCOPE/MODULES: BBMA Professional EA v4.5.9; NMJE forward-runtime validation and project continuation
BASELINE/COMMIT: To be resolved from Git/local history during next Work-mode audit
LOCAL STATE: Must be compared against the last known-good pre-Chat baseline using Desktop Commander + Git history
CHANGE/ACTION: Established formal Chat-vs-Work audit logging and continued forward-validation tracking without treating pending NMJE evidence as verified
REASON: Work quota unavailable; development may continue in normal Chat while preserving a later independent Work-mode audit boundary
COMPILE STATUS: Not asserted by this log entry
RUNTIME STATUS: MT4 previously confirmed active; `BBMA_EA_V459_NMJE_FORWARD` loaded. Current forward evidence remains incomplete until a genuine outcome chain is captured and correlated
VALIDATION STATUS: PENDING
EVIDENCE: Active MT4 instance/log path must be re-confirmed at each runtime check. Required chain: `[N1-NMJE]` -> `[N2-NMJE-DEC]` -> `[N2-NMJE-OUT]`, consistent `DID/DIDH` + pair/symbol + `BBMA_EA_V459_NMJE_FORWARD`
ISSUE/RISK: Do not mix old C10/Strategy Tester/build evidence with current v4.5.9 forward evidence. Do not infer "no new outcome" without reading the current active MQL4 log
NEXT GATE: When Work mode is available, resolve the exact last known-good baseline, audit all Chat-mode deltas using Desktop Commander + GitHub, then classify each delta as VERIFIED/FAILED/PENDING before locking the build

---

## 2026-09-04 — Permanent Chat/Work identification workflow enabled

DATE/TIME: 2026-09-04 (Malaysia time)
ORIGIN MODE: CHAT
VERIFY MODE: NONE
SCOPE/MODULES: Project-wide development process
BASELINE/COMMIT: Workflow documentation commit created from current `main`
LOCAL STATE: Repository-side process update only; no EA source logic changed
CHANGE/ACTION: Made Chat-vs-Work origin tracking a permanent BBMA workflow. Added separate `ORIGIN MODE` and `VERIFY MODE` so later Work audits do not erase the fact that a change originated in Chat.
REASON: Ensure all meaningful project work can later be attributed and audited accurately across Chat and Work modes.
COMPILE STATUS: Not applicable; documentation-only change
RUNTIME STATUS: Not applicable
VALIDATION STATUS: VERIFIED
EVIDENCE: `docs/WORK_SESSION_LOG.md` workflow rules and Git commit history
ISSUE/RISK: None introduced to EA runtime/source code
NEXT GATE: Apply this classification to every future meaningful BBMA technical change or validation checkpoint

---

## 2026-09-04 — P2 invalid-lot diagnostics static audit checkpoint

DATE/TIME: 2026-09-04 (Malaysia time)
ORIGIN MODE: CHAT
VERIFY MODE: CHAT
SCOPE/MODULES: P2 observability; M21 Money Management; `REJ_INVALID_LOT` diagnostics
BASELINE/COMMIT: `d1-owner-dev`, source blob SHA `dc83e62748c93171d89a312e9f7a53c06d97e261`
LOCAL STATE: GitHub authoritative branch inspected; no EA source change performed in this checkpoint
CHANGE/ACTION: Audited the queued `REJ_INVALID_LOT` diagnostics item without running tests or modifying EA logic. Confirmed `DiagnoseInvalidLotReason()` and `PrintInvalidLotDiagnostic()` already exist and are called on the failed `CalculateLotSize()` path before the decision is marked `REJ_INVALID_LOT`.
REASON: User requested continuation using detailed non-test steps while preserving the frozen runtime candidate.
COMPILE STATUS: Not rerun; source not modified
RUNTIME STATUS: Not run by this checkpoint
VALIDATION STATUS: PENDING
EVIDENCE: `blueprint/source/BBMA_EA.mq4` on `d1-owner-dev`; M21 contains observability-only reason classification and `RunEntryPreflightAndExecute()` invokes it on lot failure
ISSUE/RISK: `blueprint/MASTER_QUEUE.md` still lists P2 `REJ_INVALID_LOT diagnostics` as `QUEUED`, so project tracking is stale relative to the current source. Runtime/compile closure is intentionally not claimed.
NEXT GATE: Reconcile the queue/status record for this item, then continue with the next non-test audit item while leaving the frozen EA runtime candidate unchanged.

---

## 2026-09-04 — P2 dashboard active-trade count static audit checkpoint

DATE/TIME: 2026-09-04 (Malaysia time)
ORIGIN MODE: CHAT
VERIFY MODE: CHAT
SCOPE/MODULES: P2 UI/observability; M25 dashboard active-trade count refresh
BASELINE/COMMIT: `d1-owner-dev`, source blob SHA `dc83e62748c93171d89a312e9f7a53c06d97e261`; audit record commit `b399b3bb88d8ba14f43f98505b934f293ee75569`
LOCAL STATE: GitHub authoritative branch inspected; no EA `.mq4` source change performed
CHANGE/ACTION: Confirmed `P2-DASHCOUNT-01` is already present. M25 derives the displayed trade count from the live broker order pool using `OrdersTotal()` + `OrderSelect(..., MODE_TRADES)` + `IsExactEAOwnedSelectedOrder()`, rather than `g_monitored_count`. `RefreshDashboardLiveTradeCount()` rebuilds the snapshot when the broker-derived count changes, and `OnTimer()` invokes the refresh path.
REASON: Continue the non-test queue while preserving the currently frozen runtime candidate.
COMPILE STATUS: Not rerun; EA source unchanged
RUNTIME STATUS: Not run by this checkpoint
VALIDATION STATUS: PENDING
EVIDENCE: `blueprint/source/BBMA_EA.mq4` M25 and `blueprint/audits/P2_DASHCOUNT_STATIC_AUDIT_20260904.md`
ISSUE/RISK: `blueprint/MASTER_QUEUE.md` still lists dashboard active-trade count refresh as `QUEUED`; that tracking status is stale relative to current source. Runtime display behavior is not claimed as verified.
NEXT GATE: Reconcile stale tracking metadata later; continue with another non-test/read-only item that does not alter the frozen EA runtime candidate.

---

## Work-mode return audit checklist

1. Identify the last known-good commit/state before normal Chat continuation.
2. Use Desktop Commander to inspect the actual local clone: `git status`, branch, HEAD, log, and diff.
3. Compare local state and GitHub history against the baseline.
4. Audit only the Chat-mode delta for new compile, runtime, architecture, cross-module, lifecycle/state, duplication, and regression issues.
5. Re-check pending forward-validation evidence from the active MT4 Data Folder and MQL4 logs.
6. Report only new meaningful findings as `ISSUE -> IMPACT -> FIX`.
7. Do not modify code until the user confirms fixes after the audit.
