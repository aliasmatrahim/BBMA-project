# SIG06 MHV candidate invalidation implementation plan
Goal: prevent an invalidated pending Extreme candidate from installing a later MHV parent.
Spec: existing CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md and canonical ReadExtremeLifecycleInvalidation/TryAdvanceMHVSupersessionCandidate.
Architecture: one M09 engine and one shared candidate-clear helper; do not clear on generic MHV VOID because relevant outer sides differ.
- [ ] Native RED against frozen6.11: FORMATION/RETEST × BUY/SELL ×7TF; applicable Momentum must clear candidate and next reversal must not install its stale raw.
- [ ] Minimal shared M09 fix; unavailable data freezes owner; outer-only/non-Momentum invalidation preserves a valid candidate. Unique Build6.12 identity.
- [ ] Strict full EA/harness compile, native GREEN, source-readiness and M08/M09/canonical/recovery affected regressions, actual controller OFF/ON/frozen6.11 trace review. Existing specialized driver selection only; no new global checks inferred.
- [ ] Independent architecture/source regression review, bind hashes/RED/GREEN evidence and publish checkpoint in existing Draft PR303.
Original SIG06 session/epoch/full recovery gates remain HOLD; no later signal/activation/merge.
