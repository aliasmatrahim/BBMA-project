# C044 Step 1 — Targetless Payload Implementation Audit — 2026-08-26

Branch: `d1-owner-dev`

## Status
**IMPLEMENTED / STATIC INTEGRITY PASS / FAIL-SAFE FEATURE GATE OFF / NATIVE COMPILE PENDING**

## Scope
Stage the minimum M17/M22 plumbing required by the approved C044 targetless lifecycle architecture without enabling incomplete lifecycle execution.

## Implemented
- source build identifier advanced to `4.53 - C044 Targetless Payload Stage`;
- added internal locked `EnableC044Lifecycle=false` gate;
- added `BBMA_Decision.C044LifecycleManaged` payload classification;
- M17 can resolve the existing approved structural hard SL while producing `TP=0` only when the C044 gate is enabled;
- current static outer-BB TP path is preserved while the gate is OFF;
- M17 targetless validation accepts SL-only geometry, rejects `MinRRRatio>0`, and does not manufacture reward distance;
- M22 transport/pre-send guards can carry `TP=0` only when the decision is explicitly C044 lifecycle-managed;
- no M23 lifecycle close logic, M24 recovery semantics, entry eligibility, detector ownership, SL formula, lot sizing, risk percentage or emergency-close authority is changed in this step.

## Safety boundary
The C044 feature gate remains OFF because enabling targetless orders before M23/M24 lifecycle close and recovery are implemented would create live positions without the approved normal lifecycle exit. Current runtime behavior therefore remains the pre-C044 static-TP policy until the later atomic activation gate.

## Static checks
- exact pre-step source Git blob verified: `4ccd444a96a34b494653143a7560516a4147b5bc`;
- one C044 gate and one decision payload flag;
- targetless M17 path present;
- MinRR fail-closed rule present;
- M22 TP=0 transport path present;
- no new `OrderClose()` authority added;
- `git diff --check` required before commit.

## Next step
Implement immutable owner/lifecycle evidence + M23 C044 close latching and M24 restart reconstruction, then enable C044 only after cross-module static regression and native MetaEditor 0E0W.
