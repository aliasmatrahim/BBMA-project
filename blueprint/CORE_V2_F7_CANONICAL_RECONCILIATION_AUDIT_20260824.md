# CORE-V2-F7 — Canonical Source / Governance Reconciliation Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: reconcile the completed F7 source findings into one canonical source/governance view without changing the frozen EA source  
Status: **SOURCE / GOVERNANCE RECONCILIATION COMPLETE — IMPLEMENTATION REMAINS DEFERRED**

## 1. Purpose

This audit consolidates the accepted F7 Path-A conclusions so the project has one authoritative source/governance interpretation before any later implementation work.

It does not change `blueprint/source/BBMA_EA.mq4`, does not create a new EA build, and does not invalidate the pending P3 runtime evidence.

## 2. Preflight basis

The reconciliation follows the project hierarchy:

`PROJECT_INSTRUCTIONS -> SOURCE_INDEX -> canonical Strategy Core -> original PDF evidence -> Finale evidence -> authenticated Home Course Workbook evidence -> F7 audit chain -> current contracts/code`

The current source hierarchy remains binding: implementation behavior does not outrank source evidence.

## 3. Accepted F7 source conclusions

### 3.1 Re-Entry exit model

For executable Re-Entry-owned trades, the source-supported management model is lifecycle-based rather than a universal static outer-BB target.

Accepted sequence:

`Re-Entry -> Momentum/CSM -> later Re-Entry -> Momentum/CSM -> ...`

If a valid Re-Entry is followed by no Momentum and structural reversal is confirmed, the position-management principle is TP/close.

### 3.2 Static outer-BB TP

The previous mappings:
- H1 Re-Entry -> H1 outer BB;
- REM -> H4 outer BB;
- RRE/REE -> D1 outer BB;

are **not proven as universal BBMA Strategy-Core broker TP rules** under strict Path A.

The fact that H1/H4/D1 are valid lifecycle-owner timeframes does not by itself prove the corresponding outer BB is a mandatory static TP.

### 3.3 Lifecycle owner timeframe

Accepted owner hierarchy:
- standalone H1 Re-Entry -> H1;
- REM -> H4 Re-Entry;
- RRE -> D1 Re-Entry;
- REE -> D1 Re-Entry.

Lower-timeframe supporting components do not become equal post-entry close owners of the higher-timeframe parent position.

### 3.4 Momentum success and re-arm

After same-direction Momentum succeeds, the source says to hold and wait for the next valid same-direction Re-Entry on the lifecycle-owner timeframe.

That later owner Re-Entry begins a new continuation-test phase for the already-open same-cycle position. A new full REM/RRE/REE combination is not required merely to continue managing the existing position.

### 3.5 Final old-cycle boundary

The project already accepts:

`opposite RAW Extreme = new-cycle candidate only`

`opposite REVERSAL-CONFIRMED Extreme = atomic old-cycle supersession`

F7 therefore treats an opposite reversal-confirmed Extreme on the lifecycle-owner timeframe as the final structural termination of the old directional lifecycle.

### 3.6 Protective hard SL

The exact current wick-based hard-stop implementation remains **EA_SAFETY**, not a universal BBMA Strategy-Core SL formula.

The Home Course/PDF evidence supports structural risk context but does not prove the exact mapped Re-Entry-candle wick plus one broker-point formula as a universal Oma Ally rule.

### 3.7 Risk:Reward

The source recognizes Risk:Reward qualitatively, but no universal numeric minimum RR is established for the lifecycle-managed Re-Entry model once the unproven static target is removed.

Therefore a numeric reward gate must not be represented as BBMA Core merely by deriving reward from the old outer-BB target.

## 4. D1 support gap

The active project currently has Extreme lifecycle support for M15/H1/H4 but not D1.

Because RRE/REE lifecycle ownership is D1 and the final old-cycle boundary is an opposite reversal-confirmed owner-timeframe Extreme, a future implementation needs D1 Extreme lifecycle support using the already accepted M08/F2 semantics.

This is a support-state requirement only. It does not authorize standalone D1 Extreme execution.

## 5. Module-level reconciliation boundary

At governance/responsibility level:
- M08/F2 remains Extreme maturity/cycle-boundary owner and would need D1 support;
- M10 remains Momentum/CSM owner;
- M12 remains Re-Entry owner;
- M13/M14/M15/M16 remain combination/selection/validity owners;
- M17 must no longer claim the old universal static outer-BB TP as Strategy Core for Re-Entry-owned trades;
- M22 remains execution-only and must not invent strategy targets;
- M23 remains the position-lifecycle/close owner;
- M24 remains restart/recovery owner;
- M20 emergency protection retains operational precedence;
- M19/M21 risk calculations remain conceptually based on downside exposure rather than a fabricated reward target.

This audit deliberately does not encode broker-operation or code-level execution steps.

## 6. F7 audit chain consolidated

The following records now form one completed source-decision chain:
- `CORE_V2_F7_M17_SLTP_PROVENANCE_AUDIT.md`;
- `CORE_V2_F7_WORKBOOK_AUTHENTICATION_AUDIT_20260824.md`;
- `CORE_V2_F7_WORKBOOK_RULE_RECONCILIATION_AUDIT_20260824.md`;
- `CORE_V2_F7_DETERMINISTIC_NO_MOMENTUM_EXIT_RESOLUTION_AUDIT_20260824.md`;
- `CORE_V2_F7_COMBINATION_LIFECYCLE_EXIT_OWNERSHIP_AUDIT_20260824.md`;
- `CORE_V2_F7_STATIC_TP_VS_LIFECYCLE_EXIT_COEXISTENCE_AUDIT_20260824.md`;
- `CORE_V2_F7_MINRR_PROTECTIVE_PAYLOAD_RESOLUTION_AUDIT_20260824.md`;
- `CORE_V2_F7_M23_M24_LIFECYCLE_STATE_RESTART_RECOVERY_AUDIT_20260824.md`;
- `CORE_V2_F7_POST_MOMENTUM_REARM_FINAL_EXIT_RESOLUTION_AUDIT_20260824.md`.

## 7. Current project status after reconciliation

Source/spec questions resolved by F7:
- lifecycle-based Re-Entry management principle;
- no-Momentum close principle;
- owner timeframe H1/H4/D1/D1;
- post-Momentum wait/re-arm principle;
- final opposite reversal-confirmed Extreme cycle boundary;
- old static outer-BB TP not Core-authorized;
- hard SL remains EA_SAFETY rather than universal Core;
- D1 Extreme lifecycle support required for RRE/REE future lifecycle handling.

Still pending:
- implementation changes after P3 runtime freeze;
- contract/code integration review at implementation time;
- new build identification and compile/runtime evidence for any future source change.

## 8. Runtime freeze

**NO EA SOURCE CHANGE.**

The current P3 runtime candidate remains frozen. Existing runtime evidence remains attributable to the same source/build.

## Final verdict

**CORE-V2-F7 SOURCE/GOVERNANCE STATUS: CLOSED ENOUGH FOR FUTURE ENGINEERING HANDOFF.**

The project now has a coherent Path-A source interpretation for Re-Entry-owned exits without promoting the old static outer-BB target or exact hard-stop engineering formula into BBMA Core.

Future implementation must preserve these source boundaries and must not silently reintroduce the rejected static-target assumptions as Oma Ally/Core rules.
