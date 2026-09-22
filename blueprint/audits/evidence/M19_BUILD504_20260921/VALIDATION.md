# M19 Build 5.04 validation
Completed validation: 2026-09-22 UTC. Build identity retains task start date20260921.
Issue101 F01 only; user selected option1. Baseline d1-owner-dev@f48a74e9d87c8c7ae2ac5b9f0ac6cf28e87391fd (Build5.03).
PR217/219/220/221/222 remain VERIFIED and are not recreated.
## Fix and scope
CalculateTotalRisk now selects each monitored ticket once, rejects selection failure with valid=false, then applies the unchanged pair/registry magic/live magic ownership predicate.
Existing selected closed/foreign rows still excluded. Risk formula, thresholds, TradeLock, M20/M21/M22/M24, M17, D1TPW, C044, D1O and strategy ownership unchanged.
The shared boolean ownership helper remains unchanged; copying its small predicate inside M19 avoids a second silent selection failure and any change to other callers.
Source-wide protected comparison permits only CalculateTotalRisk and five build identity fields.
TradeLock source conflict and cross-decision execution ambiguity remain HOLD; no new policy was implemented.
## Verified checkpoints
- TDD actual source-body broker-stub probe: RED3 failures -> GREEN0, ten cases (PROBE_TDD.log).
- M19 static and existing ownership model: PASS.
- Complete pytest collection:22 PASS (PYTEST.log).
- Thirteen targeted scripts: PASS, including M17/M19/D1O/D1TPW/C044/F7 checks.
- D1O static identity initially rejected new Build504 header; exact503-or504 identity tuple added, semantic assertions unchanged; RED and final logs retained.
- Complete protected-source comparison: PASS (PROTECTED.log).
- Native MetaEditor:0 errors/0 warnings (native_metaeditor.log).
- Exact three-transform tester adapter: PASS; MetaEditor0 errors/0 warnings (tester_adapter_metaeditor.log).
- Offline MT4 GBPUSD M15 EveryTick Aug1-Sep1 2026, spread20: PASS,14 trades,0 chart mismatches,0 fatal scan matches.
- Exact baseline503/candidate504 traces:523 M15/M16/final decisions;325 preflight;14 execution;3 momentum hold;10 lifecycle exit/close.
- Exact Global Variables restoration:240 bytes; SHA256 DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6 before/after; byte equality and existence verified.
- Primary MT4 PID13064 unchanged; isolated tester PID16580 exited0.
## Source/artifact identity
Candidate LF SHA256 C8E0987393FDB3D1063A1072FB767BD8509C3E7DB48CE30BA31B5595ED587F9F.
Native Windows MQ4 SHA256 7D1E8D270729BD90AE737A314741D100DF5DE6F69A5CC10566255A793F21EA9D.
Native EX4 SHA256 A3884751D1AFD5B04CBDD7906968A642ABA5783A203988A2C4E752F041B52DE9.
All adapter/source/artifact hashes: COMPILE_MANIFEST.json and SMOKE_ARTIFACTS.json.
G40 raw smoke evidence: D:/BBMA/MT4_TesterRunner_OfflineDiag/evidence/M19_504_101_20260922.
Reusable compile/helpers: D:/BBMA/Compile/M19_504_101. Task worktree: D:/BBMA/Workspace/m19-selection-failclosed-101.
## Limitations and remaining scope
The historical smoke does not inject broker selection failure; that path is covered by source-extracted host tests. No broker live/demo claim.
No primary restart, trading enablement or production activation. Broker runtime/live-readiness remain final Q.
Independent review and exact-head PR/merge checks recorded separately; Issue101 remains open for deferred findings.
