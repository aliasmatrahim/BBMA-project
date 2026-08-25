# D1O Rebaseline After Workbook Audit

Date: 2026-08-25
Baseline branch: `d1-owner-dev`
Baseline commit: `80ea1bbbd49e3546ac89dc0334835a8ecab117ec`

## Decision

Do not merge the stale/diverged `d1o-canonical-dedup-native-compile` validation branch into the current owner branch.

The validation branch has historical D1O tooling/gates but diverged materially from the current owner baseline. The current owner branch also contains the completed Home Course forensic audit and safe Core V2.x clarification work.

## Safe continuation contract

1. Treat current `d1-owner-dev` as sole implementation baseline.
2. Re-apply only the D1O-07 canonical LTF dedup behavior required by the locked clarification, against current source layout.
3. Preserve the safe Core V2.x documentation clarifications; they have no executable behavior impact.
4. Do not import historical validation-branch files wholesale.
5. Re-run static, native compile, and runtime/telemetry validation on the newly materialized current-baseline patch.
6. Any mismatch that would change BBMA strategy/execution authority remains a strategy decision gate; technical compatibility fixes are autonomous.

## Strategy invariants

- Fresh LTF Re-Entry owns executable opportunity identity.
- D1 cycle/family changes are attribution context and must not manufacture a duplicate executable opportunity while the same fresh LTF identity remains active.
- Approved REM/RRE/REE signatures and D1/H4/H1/M15 ownership remain unchanged.
- Workbook-derived safe clarifications do not authorize new detector, entry, TP, hold, or timeframe-owner behavior.

Status: REBASELINE LOCKED — READY FOR CURRENT-BASELINE MATERIALIZATION.
