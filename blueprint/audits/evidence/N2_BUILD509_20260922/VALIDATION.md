# N2 Build 5.09 F07 Open DecisionID Provenance Validation

Date: 2026-09-22
Issue: #233 / downstream #101 N1/N2/N3 provenance-firewall
Base: `d1-owner-dev@a4cd2363c5f9d3fe9655177d41056a7f3fdfcecb` / Build 5.08
Source-bearing commit: `83df7f14b625799e4cdc376490da9b6b0c883341`
Candidate: Build 5.09 / `V509_N2_F07_OPEN_DECISIONID_20260922`

## Classification
**CONFIRMED N2/F07 PROVENANCE BUG -> SCOPED FIX VERIFIED OFFLINE.**

Build 5.08 validated an exact same-session F07 open execution but then discarded the still-known full DecisionID when materializing the monitored TradeInfo. The later N2 closed outcome therefore degraded unnecessarily to hash-only attribution.

## Smallest repair
- F07 open adoption copies only the already-owned `g_execution_ambiguity.DecisionID` into `TradeInfo.decision_id`;
- no DecisionID is reconstructed or guessed;
- restart/minimal persistent context remains hash-only because the full DecisionID is not persisted or loaded;
- no Strategy-Core, candidate, M15/M16/M17, risk/MM, TradeLock, M22 send/retry, M23 lifecycle or M24 recovery semantics are changed.

## TDD / static / cross-module
- exact Build 5.08 baseline: RED — open adoption contains `info.decision_id = ""` and lacks the carry marker;
- Build 5.09 targeted guard: PASS;
- protected Build 5.08 bodies: 25/25 exact PASS;
- prior N2 closed-before-reconcile bridge: PASS;
- F07 model/static: PASS;
- N1 P1 static + epoch model: PASS;
- NMJE read-only authority + M12N ordering: PASS;
- full pytest: 22/22 PASS;
- `git diff --check`: PASS;
- production `OrderSend()` count remains one;
- N3 execution activation markers remain absent.

## Compile identity
- source/native MQ4 SHA-256: `4DB2A8A84051489AB9FFDA513287FCD9D43B234E2F6EA58D776B5BBB1609E273`;
- native EX4 SHA-256: `5860523512DAB667EB49174A226C5859A5C97971EBFFCFEE8ADCB49ACDF4CE9E`;
- native MetaEditor: **0 errors / 0 warnings**;
- exact three-transform tester adapter SHA-256: `264FBDE51D14C6641C3878B415B38CAEE1BDEF4403449B8E9C6F7B9454BD73D8`;
- tester adapter EX4 SHA-256: `948ADDFA851C9C159878D7580A455D19F0809507C88CC2E31A799EF8AAB5DC8E`;
- tester adapter MetaEditor: **0 errors / 0 warnings**;
- targeted open and hash-only harnesses also compile **0 errors / 0 warnings**.

## Normal-path EveryTick regression
GBPUSD M15, 2026-08-01 through 2026-09-01, isolated tester.
Build 5.09 is byte-exact to VERIFIED Build 5.08 across 11 trace families:
- M15_COUNTS 523;
- M15_SELECT 523;
- M16_PASS 523;
- DECISION_FINAL 523;
- PREFLIGHT_PASS 325;
- EXEC 14;
- F7 MOMENTUM_HOLD 3;
- F7 EXIT_LATCHED 10;
- F7 CLOSE_SUCCESS 10;
- N2-NMJE-DEC 523;
- N2-NMJE-OUT 14.
Fatal runtime markers = 0; mismatched chart errors = 0.

## Targeted same-session open reconciliation
Tester-only harness seeds one persistent F07 HOLD immediately after a real successful execution and invokes the production reconciler while the order is still open.
Observed:
- seed = 1;
- reconcile PASS = 1;
- F07 HOLD cleared with `Open=Y` = 1;
- eventual closed outcome retains exact full DID + matching DIDH = 1;
- recovery marker = `REC_AMBIGUOUS_EXECUTION_FROZEN`;
- fatal runtime markers = 0.
Concrete outcome:
`[N2-NMJE-OUT] PAIR=GBPUSD TICKET=1 DID=GBPUSD|2026.08.10~13:00|1|7|6365325817470039 DIDH=9837A0C7AF77EECA NET=-0.78000000 CLOSE=1786375801 REC=REC_AMBIGUOUS_EXECUTION_FROZEN`.

## Hash-only regression
A second tester-only harness emulates post-restart minimal context by clearing only the non-persisted in-memory DecisionID while retaining the exact persisted execution hash before the same open reconciliation.
Observed matching outcome:
`[N2-NMJE-OUT] PAIR=GBPUSD TICKET=1 DID=- DIDH=9837A0C7AF77EECA NET=-0.78000000 CLOSE=1786375801 REC=REC_AMBIGUOUS_EXECUTION_FROZEN`.
This is a targeted hash-only simulation, not a physical terminal restart. It proves the candidate does not fabricate a full DecisionID when the in-memory value is unavailable.

## Runtime isolation
All three tester runs restored `gvariables.dat` exactly to 240 bytes, SHA-256
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.
Primary MT4 PID 13064 remained the sole terminal after every run.

## Boundary
No production activation, primary MT4 restart, live/demo broker ambiguity reproduction or live-readiness claim.
Raw tester logs remain on G40 and are identified by `RUNTIME_MANIFEST.json`.
