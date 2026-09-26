# NMJE V2 Build 5.17 — A/B + Multi-Pair Runtime Checkpoint — 2026-09-26

Status: **STRATEGY TESTER A/B PASS / MULTI-PAIR REGRESSION PASS / DEMO ACTIVE ATTACH PARTIAL / RESTART-PROVENANCE BROKER GATE PENDING**

Issue: #101
Branch head before this evidence checkpoint: `4244b4c8bdc2ae36ca16c7b298cb0a209f6d1c8d`
Build: `5.17 / V517_NMJE_ACTIVE_SELECTION_POLICY_20260926`
MQ4 SHA-256: `B28E8C7F493D96899A681397FECE14876EFAAF7F73435274E5A3EA6E33394F9F`

## Recovered execution state

The interrupted runtime task did not require P2/P5/N3 implementation or compile work to be repeated.

Already VERIFIED before runtime continuation:
- P2/P5 policy closure;
- N3 default-OFF active-selection implementation;
- native MetaEditor 0 errors / 0 warnings;
- targeted regression PASS;
- repository Python suite 72/72 PASS;
- specialized GitHub NMJE invariant run #21 SUCCESS.

Recovered local evidence proves the Strategy Tester A/B and multi-pair runs had already completed after the interruption.

## Strategy Tester A/B

Exact GBPUSD M15 window: 2026-08-01 through 2026-09-01.

OFF:
- 14 executions;
- policy marker 0;
- duplicate DecisionID 0;
- duplicate ticket 0;
- fatal runtime faults 0.

ON:
- 14 executions;
- policy marker present;
- duplicate DecisionID 0;
- duplicate ticket 0;
- fatal runtime faults 0.

OFF and ON execution traces are exact-equal for this period.

Classification: **PASS — NON-REGRESSION**.

## Multi-pair active-policy regression

Validated ON runs:
- EURUSD Jan 2026: 34 executions;
- EURUSD Aug 2026: 26 executions;
- GBPUSD Jan 2026 R2: 34 executions;
- USDJPY Jan 2026 R2: 42 executions;
- USDJPY Aug 2026 R2: 16 executions;
- GBPUSD Aug 2026 A/B-ON: 14 executions.

Across the full seven-run matrix:
- total executions: 180;
- reconstructed active-evaluation cycles: 419;
- duplicate DecisionIDs: 0;
- duplicate tickets: 0;
- fatal runtime faults: 0;
- all runs mechanical PASS.

Observed N3 winner changes: **0**.

This means the matrix verifies active-policy evaluation and non-regression, but it does not provide a historical divergent-winner example. No synthetic winner change was manufactured.

Classification: **PASS — MULTI-PAIR SAFETY/REGRESSION; DIVERGENT-SELECTION EXAMPLE NOT OBSERVED**.

## Demo-forward active-policy state

Dedicated terminal only:
`D:\BBMA\MT4_Q5_180_Demo`

Q3 PID 13064 and Q10 PID 2336 remain separate and untouched.

Build 5.17 was loaded successfully three times after Build 5.16 shutdown:
- 05:39:09 — active Build 5.17 loaded, StrategyID 93 / InstanceID 95;
- 05:42:44 — active Build 5.17 loaded, StrategyID 93 / InstanceID 95;
- 05:46:42 — clean active Build 5.17 loaded, StrategyID 96 / InstanceID 96.

Current recovered dedicated PID: `15356`.
Current config:
`config\nmje_v2_517_active_demo_clean.ini`
Current preset:
`NMJE_V2_517_ACTIVE_DEMO_CLEAN_20PAIR.set`
`EnableNMJEForwardEvidence=true`
`EnableNMJESelectionPolicy=true`
`MaxActivePair=1`.

However, after the 05:38 Build 5.16 shutdown, the terminal log contains no fresh MetaQuotes-Demo login marker for the Build 5.17 launches and the EA log has no Build 5.17 `EA initialized successfully` marker, `[F7-BUILD]` marker, or `[N3-NMJE-POLICY]` marker after the latest load.

No initialization failure, fatal runtime fault, broker order, or attributable active-policy outcome is evidenced either.

Classification: **VERIFICATION REQUIRED / BROKER-CONNECTIVITY-INITIALIZATION ENVIRONMENT GATE**.

The current dedicated Build 5.17 terminal is intentionally left running. Do not restart it merely to repeat the same weekend connectivity condition.

## Restart / provenance / order-log gate

Not yet accepted because a restart acceptance cycle requires a fully initialized active-policy demo session.

Already supported by tester evidence:
- no duplicate DecisionID/ticket;
- no fatal runtime fault;
- one broker execution owner remains unchanged;
- active selection does not alter risk/MM/execution surfaces.

Still required from the demo environment:
1. fresh Build 5.17 successful initialization with active-policy marker;
2. broker-connected active-policy decision/execution or attributable monitored trade state;
3. graceful stop/restart of the same dedicated Build 5.17 instance;
4. durable identity/provenance recovery;
5. no duplicate order/DecisionID, persistence failure or ownership ambiguity after restart;
6. attributable order/log outcome validation.

Because the terminal has not reached item 1 after the latest weekend restart attempts, items 2-6 cannot be forced safely.

## Exit state

- Strategy Tester A/B: **PASS**.
- Multi-pair regression: **PASS**.
- Active-policy historical divergent winner: **NOT OBSERVED / NO SYNTHETIC SUBSTITUTE**.
- Demo Build 5.17 binary/config attach: **OBSERVED**.
- Demo active-policy initialization: **VERIFICATION REQUIRED**.
- Demo broker-connected outcome: **VERIFICATION REQUIRED**.
- Restart/provenance/order-log: **BLOCKED BY THE SAME DEMO INITIALIZATION/CONNECTIVITY GATE**.
- Release readiness: **NOT CLAIMED**.
