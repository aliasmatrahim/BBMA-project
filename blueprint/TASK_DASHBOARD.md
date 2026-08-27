# BBMA Project Task Dashboard

Updated: 2026-08-27
Status source: `blueprint/MASTER_QUEUE.md` + `blueprint/queue/*.md` + current NMJE staging work
Purpose: one compact dashboard for what is DONE, ACTIVE, BLOCKED, KIV, and QUEUED. Detailed semantics remain authoritative in the underlying queue/audit/contract files.

## Legend
- ✅ DONE / PASS — completed at the stated evidence level.
- 🟡 ACTIVE — work in progress or evidence collection currently active.
- 🟠 READY / WAITING — prepared but waiting for a dependency, CI, runtime evidence or timing gate.
- 🔴 BLOCKED — cannot safely progress until the stated blocker is cleared.
- ⏸ KIV — deliberately parked; do not implement yet.
- ⚪ QUEUED — pending according to the planned execution order.

## Current project headline
- P0 Architecture Repair: ✅ COMPLETE at locked patch/contract level.
- P1 Integration / canonicalization: ✅ COMPLETE / PASS at recorded level.
- P2 functional/cross-module audit series: ✅ RECORDED through Step 18; exact item status stays in each record.
- P3 Runtime Validation: 🟡 ACTIVE. Preserve current runtime candidate/evidence attribution before source changes on the runtime lineage.
- BBMA Strategy Core / D1 / NMJE: 🟡 ACTIVE through isolated staging and documentation work; no production NMJE execution policy is active.

## Active / highest-priority work

### 1. P3 frozen runtime evidence
Status: 🟡 ACTIVE
Priority: CRITICAL
Action:
- keep the currently running/frozen runtime candidate attributable to its existing source/build;
- collect open-order/runtime evidence required by the active P3 closure checklist;
- do not opportunistically patch the runtime branch while that evidence is being collected.
Dependency: broker/live MT4 runtime evidence.

### 2. NMJE dependency hardening / N3 staging
Status: 🟡 ACTIVE ON ISOLATED STAGING BRANCH
Priority: CRITICAL
Queue record: `blueprint/queue/NMJE_N3_HARDENING_IMPROVEMENTS_20260827.md`
Staging branch: `nmje-n3-hardening-dev`
Staging PR: `#97 NMJE N3 hardening staging` — DRAFT / NO MERGE / NO ACTIVATION.
Completed staging work already recorded:
- dependency audits DEP-A01 through DEP-A09;
- N1/N1.1 observer audit;
- N2 shadow-evidence audit;
- N3 pre-enforcement contract draft;
- M09 single-writer hardening design/materialization path;
- canonical event identity / ParentEventID / JourneyID provenance;
- M15 shadow freeze + M16 shadow revalidation only;
- replay/recovery fail-closed regression gates;
- cross-module authority regression gate;
- identity-domain separation regression gate.
Current staging blocker/finding:
- D1 owner EventID needs stable owner-epoch identity rather than daily snapshot identity;
- Step-5 D1 owner epoch materialization is prepared but latest GitHub Actions runs are failing before executable job steps, so source materialization/compile cannot yet be trusted as completed.
Next safe chain when CI/runner is healthy:
1. materialize D1 owner epoch anchor;
2. run static identity/authority/recovery tests;
3. native MT4 MetaEditor 0E0W;
4. PR diff/regression closure;
5. remain DRAFT until runtime evidence and any required strategy-policy approval are available.

### 3. D1 strategic-owner path
Status: 🟠 SPEC/CONTRACT RESOLVED; CURRENT SOURCE LINEAGES DIFFER BY BRANCH
Priority: CRITICAL / STRATEGY CORRECTNESS
Canonical queue source: `blueprint/MASTER_QUEUE.md`
Related KIV record: `blueprint/queue/KIV_HOME_COURSE_D1_MAJOR_TREND_TRANSITION.md`
Current rule set already reconciled in project records:
- D1 closed-candle MA50 owner = strategic authority;
- H4 = immediate structural/setup parent;
- BUY confirmed = Close > MA50 and MA50 rising;
- SELL confirmed = Close < MA50 and MA50 falling;
- otherwise valid disagreement/flat/equality = TRANSITION;
- invalid history = UNRESOLVED;
- new entries block on TRANSITION/UNRESOLVED.
Current engineering focus for NMJE: stable D1 owner epoch/provenance without changing the BBMA owner formula.

## Runtime traces still pending

### 4. CORE-V2-F1 M09 MHV/MLV lifecycle
Status: 🟠 STATIC PASS / NATIVE 0E0W RECORDED — RUNTIME TRACE PENDING
Need: lifecycle trace including parent Extreme, TP-Wajib completion, failed continuation, frozen body, retest, same-cycle progression and opposite mature Extreme supersession.

### 5. CORE-V2-F2 Extreme maturity
Status: 🟠 STATIC PASS / NATIVE 0E0W RECORDED — RUNTIME TRACE PENDING
Need: RAW -> REVERSAL-CONFIRMED -> RETEST/ENTRY-READY and supersession traces.

### 6. CORE-V2-F3 Re-Entry Type 1 context
Status: 🟠 STATIC PASS / NATIVE 0E0W RECORDED — RUNTIME TRACE PENDING
Need: owner -> structural ranging/retrace -> MA-cluster interaction -> confirmation / invalidation traces.

### 7. CORE-V2-F5 BB flat classification
Status: 🟠 CODE + STATIC PASS / NATIVE 0E0W RECORDED — RUNTIME TRACE PENDING

### 8. CORE-V2-F6 Re-Entry timing
Status: 🟠 STATIC TIMING PASS / METADATA REPAIRED / NATIVE 0E0W RECORDED — RUNTIME ORDER-TIME TRACE PENDING
Need: prove validation on closed source candle and execution eligibility in the immediately following live source-TF candle.

### 9. Opposite-direction / same-pair cycle integrity
Status: 🟠 FIX IMPLEMENTED / STATIC PASS / NATIVE 0E0W RECORDED — RUNTIME TRACE PENDING
Need: focused runtime proof of lock/ownership behavior on the active build lineage.

### 10. Sequential cumulative risk-budget admission
Status: 🟠 STATIC PASS — RUNTIME MULTI-DECISION TRACE PENDING
No strategy/risk formula change unless runtime evidence exposes a defect.

## Architecture / lifecycle work queued after the current evidence gates

### 11. CORE-V2-F7 SL/TP + lifecycle architecture
Status: ⚪ QUEUED / SOURCE-LIFECYCLE SEMANTICS RESOLVED
Priority: HIGH
Do after current runtime attribution is preserved and before final production lock.
Focus:
- remove reliance on unsupported universal outer-BB TP assumptions where the canonical lifecycle says otherwise;
- keep hard SL provenance as EA_SAFETY where applicable;
- reconcile M17 + M23/M24 lifecycle ownership and restart behavior;
- compile/static/runtime verify after implementation.

### 12. Cross-module authority audit
Status: ⚪ QUEUED
Priority: HIGH / ARCHITECTURE INTEGRITY
Queue record: `blueprint/queue/CROSS_MODULE_AUTHORITY_AUDIT_20260827.md`
Timing: after D1 owner path + NMJE N3 + SL/TP lifecycle architecture are stable, before final production-lock/regression sign-off.
Scope: verify one owner/one writer across M11, M12, M12N, M13, M14, M15, M16, M17, M22, M23, M24 and M27.

### 13. P3-M1 Mode 1 Official BBMA Compliance re-audit
Status: ⚪ QUEUED / REOPENED AFTER D1 RECONCILIATION
Priority: CRITICAL STRATEGY GATE
Run after the D1 strategic-owner path used by the candidate is stable and verified.

## Observability / UI queue

### 14. REJ_INVALID_LOT diagnostics
Status: ⚪ QUEUED
Priority: MEDIUM
Observability only. Add reason-code visibility for M21 failures such as BELOW_MIN, ABOVE_MAX, STEP_MISMATCH, BROKER_SNAPSHOT_INVALID, MAXAUTOLOT_BELOW_MIN and FIXEDLOT_INVALID. Do not change lot-sizing semantics.

### 15. Dashboard active-trade count refresh
Status: ⚪ QUEUED
Priority: MEDIUM
Audit M25 display source and open-order/monitored compaction so displayed active count comes from current exact-owned open positions, not stale lifecycle state. No strategy change.

## KIV

### 16. Home Course D1 Major Trend / Transition KIV record
Status: ⏸ KIV RECORD RETAINED
Record: `blueprint/queue/KIV_HOME_COURSE_D1_MAJOR_TREND_TRANSITION.md`
Note: later project records have reconciled/implemented portions of the D1 owner path on newer lineages, so this KIV file is historical protection context and must be re-read against latest source before any future D1/H4 semantic change.

## Locked execution order from here
1. Preserve/complete active P3 runtime evidence on the frozen runtime candidate.
2. In parallel, continue only isolated/documentation/static-safe NMJE staging work.
3. When GitHub Actions is healthy, close the D1 owner epoch identity gap on `nmje-n3-hardening-dev` and re-run all N3 static/native gates.
4. Do not merge/activate N3 until real N2/runtime evidence and required policy gates are satisfied.
5. Implement/verify the queued F7 SL/TP lifecycle architecture at its correct post-freeze timing.
6. Run the cross-module authority audit.
7. Re-run P3-M1 and required Core/runtime regression gates.
8. Finish remaining runtime traces.
9. Address observability/UI items.
10. Final production-lock only after compile, static, replay/recovery and runtime evidence are all green.

## Governance
- `blueprint/MASTER_QUEUE.md` remains the canonical detailed queue.
- Files under `blueprint/queue/` hold dedicated queued/KIV work packages.
- This dashboard is a concise status view; it must not override a newer decision/contract/audit.
- No confidence scoring, timeframe voting, AI/ML filter, win-rate gate, RSI/MACD/Stochastic/ADX/news/correlation filter or unsupported BBMA rule may enter through queue implementation.
- NMJE remains context/lineage infrastructure unless a separately approved, source-backed execution policy explicitly changes that boundary.
