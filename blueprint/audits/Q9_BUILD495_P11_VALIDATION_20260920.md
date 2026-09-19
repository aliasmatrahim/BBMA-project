# Q9 Build 4.95 P11 Validation — 2026-09-20

> **SUPERSEDED FOR P11 LINEAGE SEMANTICS.** Build 4.96 / decision A replaces the 4.95 higher-owner-root mapping with strict canonical ParentEventID/JourneyID semantics. Retain this file as historical evidence only.

Status: **STATIC/MODEL/PERSISTENCE/NATIVE COMPILE/STRATEGY TESTER AUTHORITY REGRESSION PASS**

P11 FIRST and NEW_JOURNEY natural runtime branches are **BOUNDED-UNEXERCISED** in the verified August GBPUSD safety window.
Durable ticket-bound P11 persistence is also runtime-unexercised because zero-trade caps prevent successful fills.

## Identity

- Version: `4.95`
- BuildTag: `V495_Q9_P11_LINEAGE_REFINEMENT_20260920`
- SourceRev: `Q9_P11_LINEAGE_REFINEMENT_101_20260920`
- canonical MQ4 SHA-256:
  `F8E9DD081BF660820F72467D45558C1A5D8F6B95FC0512F0A6DBE96334E6C52D`
- canonical short-path EX4 SHA-256:
  `44C74D8FADD57439E2E0F2D398C17DCAF89B1D4CE4C8AF8078CF9BEFABA65607`
  size 676434
- exact runtime-name MQ4 equals canonical bytes.
- runtime-name EX4 SHA-256:
  `E8D342F8FB7BCC97B82E8C2D4AFBADEBEAD17B5F871840DB2DA478E46D36734F`
  size 676324
- tester adapter MQ4 SHA-256:
  `DDE545F8AD26ADCDAAD5729925D2806235BACF1CC07F4F6B209828C5D6931713`
- tester EX4 SHA-256:
  `4A346372D51F9010606D42FA4AA1B51981959F229E6E15D1D4159D90F4CB7D2B`
  size 676934

## Static / model / inherited regression

PASS:
- P11 lineage refinement model;
- P11 persistence model;
- P11 static authority firewall;
- inherited P10 entry-displacement model/static;
- P8 provenance stability model/static;
- P7 structural density model/static;
- P6 maturity model/static;
- P5 conflict refinement;
- P4 attribution/persistence;
- P2/P3 shadow;
- P1 epoch model;
- NMJE read-only authority;
- M12N orchestration;
- D1O execution identity;
- N3 activation firewall;
- `git diff --check`.

Historical P1 current-owner static remains intentionally excluded because it hard-codes obsolete owner/build assumptions already superseded by later Q9 stages.

## Protected authority comparison

P10 -> P11 exact body equality PASS for:
- `BuildPossibleCombinations` = `68b2a7c875522ef5`
- `ValidateSequence` = `c077d62a2beb1d89`
- `BuildConfirmedReEntryCandidate` = `57dd94202cc8f09f`
- `BuildStandaloneExtremeCandidate` = `cd04028f76c4365f`
- `BuildD1OpportunityCandidate` = `091ac1b343c7c6f4`
- `CompareCanonicalCandidates` = `da7fb006a6c598f3`
- `PriorityEngine_Atomic` = `f3c3622f5a02298d`
- `InvalidationEngine_Atomic` = `1adf558f43cde2e3`
- `ResolveExecutionReferencePrice` = `bfb381ef6af1e416`
- `ResolveApprovedInitialSLTP` = `667719357edc1613`
- `CheckRiskBeforeTrade` = `dfe90dbd0fa5d42b`
- `RunEntryPreflightAndExecute` = `0c4fd16b9b241070`
- `IsSignalAllowed` = `b009d798cac7b320`
- `SendOrderWithRetry` = `09cb33800c8ae6e8`

## Native compile

MetaEditor:
- canonical short-path: 0 errors / 0 warnings / 1059 ms;
- runtime-name: 0 errors / 0 warnings / 1194 ms;
- tester adapter: 0 errors / 0 warnings / 1114 ms.

MetaEditor process exit code was 1 while compiler log reported 0E/0W; compiler result + produced EX4 identity are the accepted compile evidence.

## Tester adapter firewall

Diff against canonical: 46 lines.
Only the same three previously verified environment-only deltas are present:
1. tester symbol fallback in `FindActualSymbol()`;
2. `IsTerminalConnected()` allows `IsTesting()`;
3. skip `EventSetTimer(1)` under `IsTesting()`.

No Strategy-Core/risk/execution/lifecycle delta is present.

## Strategy Tester

Pair/TF: GBPUSD M15.
Window: 2026-08-01 through 2026-09-01.
Model: 0.
Spread: 20.
Safety profile:
- `MaxTradePerPair=0`;
- `MaxTotalTrade=0`;
- `MaxActivePair=1`;
- `InstanceID=95`.

Run A:
- `EXITED=True`
- `FORCED=False`
- tester bytes: 6,592,054

Run B:
- `EXITED=True`
- `FORCED=False`
- tester bytes: 6,592,054

After dropping only the wall-clock tester performance summary:
- normalized A lines: 26,188
- normalized B lines: 26,188
- exact equality: PASS
- SHA-256 both:
  `D705BDB6C8208EA9D484EC8369BE71066137C54219004F077E6BE45B4BC33C60`

Each run processed 2016 tick events / 2016 bars / 3017 bar states.

## P10 -> P11 authority regression

Exact equality:
- M15_COUNTS: 523 / 523
- M15_SELECT: 523 / 523
- M15_CONFLICT: 0 / 0
- M16_PASS: 523 / 523
- M16_REJECT: 0 / 0
- M16_OWNER_REJECT: 0 / 0
- DECISION_FINAL: 523 / 523
- D1O M15 block: 0 / 0
- D1O M16 reject: 0 / 0

Aggregate authority trace:
- P10: 2,092 lines
- P11: 2,092 lines
- exact equality: PASS
- SHA-256 both:
  `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`

Broker-action markers:
- P10=0
- P11A=0
- P11B=0

Runtime error scan: none.

## P11 lineage runtime coverage

Final fixed A/B each emitted 2016 P11 lineage rows.

Run A classes:
- FIRST: 0
- CONTINUATION: 2016
- NEW_JOURNEY: 0
- UNRESOLVED: 0
- NONE: 0

The bounded August window therefore naturally exercises CONTINUATION only.

Classification:
- CONTINUATION: **RUNTIME VERIFIED**
- FIRST: **BOUNDED-UNEXERCISED / VERIFICATION REQUIRED for natural occurrence**
- NEW_JOURNEY: **BOUNDED-UNEXERCISED / VERIFICATION REQUIRED for natural occurrence**

No synthetic transition was introduced.

## Confirmed runtime defect and correction

Pre-fix A/B produced one startup `NEW_JOURNEY` row with no previous canonical root.

Cause:
non-empty string comparison was insufficient to prove a prior canonical EventID.

Fix:
all current/previous lineage roots must satisfy exact canonical 16-character identity before they can create root transition semantics.

Post-fix:
- phantom startup transition = 0;
- deterministic A/B remains exact;
- authority trace remains exact P10/P11;
- protected executable bodies remain unchanged.

## Persistence coverage

Focused P11 persistence model PASS.
Static save/load/clear contract PASS.

Because the safety profile has zero broker execution, ticket-bound durable P11 persistence is not naturally exercised in Strategy Tester.
Classification: **BOUNDED-UNEXERCISED for natural ticket persistence**.

Pre-P11 records remain backward-readable when P11 keys are absent.

## Environment restoration

OfflineDiag GlobalVariables backup SHA-256:
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`

Restored GlobalVariables SHA-256:
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`

Q3 isolated terminal PID 13064 was not restarted or modified.
Live Q6 progress is now `STOPPED_BY_USER` at 17/720 PASS with an explicit do-not-auto-resume note. P11 did not restart or duplicate Q6.

## Result

**P11 implementation + authority-preservation exit gate: VERIFIED.**

FIRST / NEW_JOURNEY natural runtime occurrence and ticket-bound persistence remain separately bounded-unexercised.
No merge / no production activation.
