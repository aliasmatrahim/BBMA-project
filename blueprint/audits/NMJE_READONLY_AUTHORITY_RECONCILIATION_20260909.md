# NMJE Read-Only Authority Reconciliation — 2026-09-09

Status: **CONFIRMED AUTHORITY VIOLATION / SOURCE FIX PENDING NATIVE-COMPILE ENVIRONMENT**.

Issue: #141.

## Preflight
- owner: `d1-owner-dev` @ `c3318c20970b9c4413b75b46e01976a6e511bf92`;
- canonical EA: `blueprint/source/BBMA_EA.mq4` v4.61;
- router: `docs/references/SOURCE_INDEX.md`;
- accepted Core remains `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- relevant NMJE contracts: M12N read-only contract + N3 execution-intelligence staging contract.

## Contract result
The N3 contract is explicit: execution status is `INACTIVE — NO NMJE EXECUTION POLICY` until real forward evidence, an exact dated strategy proposal, explicit approval, protected-surface review, native compile and runtime activation review.

The N3 staging closure and N1–N3 RC freeze also state that no N3 execution gate was added and execution policy remained `NONE / INACTIVE / NOT YET AUTHORIZED`.

## Current-source mismatch
Commit `97e07de784e49b20c8fa31b7a364430849d4637b` introduced `BlockNMJEConflict=true`, `BlockNMJEBuilding=true`, `NMJE_PassExecutionGate()` and `REJ_NMJE_RELATION` under v4.60 profitability hardening.

Current v4.61 retains that gate. An M15/M16-valid `SIGNAL_RE_ENTRY` can therefore be rejected by an observation/staging relation.

The preceding `NMJE_7LOSS_DEEP_DIAGNOSIS_20260904.md` had correctly classified such a filter as a strategy-policy change and did not itself authorize executable promotion. No later dated NMJE activation decision is present in the live decision tree.

## Smallest repair boundary
The future source patch should restore execution-neutral NMJE behavior while retaining observation/attribution telemetry. It must not add a replacement nested rule, score, risk modifier or duplicate authority.

Protected surfaces:
- M15 final selection;
- M16 owner/component revalidation;
- D1 strategic/D1 opportunity authority;
- M17 SL/TP;
- M19/M20/M21 risk/MM;
- M22 OrderSend;
- M23/M24 lifecycle/recovery;
- F7 lifecycle semantics.

## Validation gate
Do not claim fixed until:
1. exact source change is isolated on this branch;
2. static/cross-module proof shows NMJE cannot create/reject/rank/execute;
3. observation/N2 telemetry remains intact;
4. native MetaEditor compile is 0 errors / 0 warnings;
5. targeted regression proves identical M15/M16 decisions are no longer rejected by NMJE relation;
6. runtime evidence is attributable to the exact candidate build.

The authorized `g40` development machine is currently offline, therefore MQL4 mutation/compile evidence is intentionally deferred rather than guessed. No primary MT4 restart, merge or activation is authorized.