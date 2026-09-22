# N2 Build 5.07 F07 Closed-Outcome Provenance Validation

Date: 2026-09-22
Issue: #229 / downstream #101 N1/N2/N3 provenance-firewall
Base: `d1-owner-dev@49206bc1fd148c4faf6f34e733b95e6e9e4f2bf1` / Build 5.06
Source-bearing commit: `292c684e8a26dbb8d6e4c19858a88a2e5da22fd9`
Candidate: Build 5.07 / `V507_N2_F07_CLOSED_OUTCOME_BRIDGE_20260922`

## Classification
**CONFIRMED BUG -> SCOPED FIX VERIFIED OFFLINE.**

A broker order that materialized and closed before F07 ambiguity reconciliation was identity-adopted and tombstoned, but never entered the monitored registry. Therefore the normal compaction hook could not emit `[N2-NMJE-OUT]` for that realized trade.

## Smallest repair
- preserve pair/hash/optional same-session DecisionID/magic before successful F07 HOLD cleanup;
- only for `isOpen == false`, construct an ephemeral `TradeInfo` telemetry view;
- call the existing `NMJE_PrintClosedOutcomeShadow()` after HOLD cleanup;
- reuse the exact closed order already selected and identity-validated by `AdoptAmbiguousExecutionTicket()`;
- do not create a monitored row, resend, retry, close, modify or otherwise alter broker state;
- open-order ambiguity adoption remains unchanged.

## Static / regression
- targeted pre-fix test: RED on missing closed-outcome bridge;
- targeted Build 5.07 bridge test: PASS;
- Build 5.06 protected bodies: 27/27 exact PASS; only `ReconcileExecutionAmbiguityHold()` plus build identity intentionally differ;
- F07 ambiguity model/static: PASS;
- full pytest: 22 passed;
- `git diff --check`: PASS;
- NMJE read-only execution firewall and M12N orchestration tests remain included in the full suite.

## Native compile identity
- worktree/native MQ4 SHA-256: `0A1C2B77613B5CDC7BCC4CA34D019005CEBEBBB34B6099233DA18CA85A1BC017`;
- native EX4 SHA-256: `86BFDA1977BE4F1CC0472B08C772C7CF8FDB767007D899D25D6D6F200C1C6120`;
- native MetaEditor: **0 errors / 0 warnings**;
- exact three-transform tester adapter invariant: PASS;
- tester adapter MetaEditor: **0 errors / 0 warnings**;
- targeted closed-reconcile harness MetaEditor: **0 errors / 0 warnings**.

## Normal-path EveryTick regression
GBPUSD M15, 2026-08-01 through 2026-09-01, isolated tester.
Build 5.07 is exact-equal to VERIFIED Build 5.06 for 11 trace families:
M15 counts/selects, M16 pass, final decision, preflight pass, execution,
F7 momentum/exit/close telemetry, N2 validated-decision telemetry and N2 closed-outcome telemetry.
Counts include 523 final decisions, 325 preflight passes, 14 executions, 523 N2 decisions and 14 N2 outcomes.
Total trades = 14, mismatched-chart errors = 0, fatal runtime markers = 0.
No F07 ambiguity event occurred in this normal-path run.

## Targeted closed-reconcile runtime
A tester-only harness waited until a normal EA-owned trade was closed and compacted, then seeded one exact closed-history F07 identity before the real reconciliation call.
Observed:
- `[N2-F07-TEST][SEEDED_CLOSED]` = 1;
- F07 HOLD cleared with `Open=N` = 1;
- `[N2-NMJE-OUT] ... DID=- DIDH=<hash> ... REC=REC_AMBIGUOUS_EXECUTION_FROZEN` = 1;
- seed failure = 0;
- total trades = 14;
- mismatched-chart errors = 0; fatal runtime markers = 0.
This proves runtime reachability/output of the repaired closed branch. It is not a claim of spontaneous live-broker ambiguity reproduction.

## Runtime isolation
Both tester runs restored `gvariables.dat` exactly to 240 bytes, SHA-256
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.
Primary MT4 PID 13064 remained the sole terminal after the runs; no restart or production activation occurred.

## Evidence-helper incident
The first normal run used an unmatched report-path replacement and overwrote the local Build 5.06 NORMAL_R3 HTML report.
The Build 5.07 report was preserved under its correct N2 evidence directory and the mislabeled Build 5.06 path was removed fail-closed.
The authoritative Build 5.06 tester log and repository `NORMAL_R3_ANALYSIS.json` remained intact and were used for regression.
See `RUNTIME_HELPER_CONTAMINATION_NOTICE.txt`.

## Boundary
No BBMA Strategy-Core rule, M15/M16 authority, risk/MM, TradeLock policy, M17, M22 broker-send behavior, M23/M24 lifecycle behavior, or N3 activation policy is changed.
Live/demo spontaneous late-fill ambiguity remains final acceptance evidence; it is **NOT LIVE BROKER VERIFIED** here.
