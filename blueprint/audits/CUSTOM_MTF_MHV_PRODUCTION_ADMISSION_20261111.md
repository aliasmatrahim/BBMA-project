# SIG06 MHV — actual production gap admission, 2026-11-11

Status: **bounded production fail-frozen validation PASS; full SIG06 PARTIAL/HOLD**.
Base b9f200861a865ab90a909a1897e4a70dc06a68c5; feat/custom-mtf-v1-20261108; Draft PR303.
Production Build6.11 remains unchanged, LF SHA256 a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb.

## Finding: NO FIX for current continuity rejection

Actual ReplayCustomAuxOwnerSource rejects a non-nominal candle interval with WAIT_REPLAY_HISTORY_CONTINUITY.
Its staged copy must not leak earlier work in the same failed chunk. RefreshCustomRequestedOwners must set recoveryRequired even for an owner previously not held, preserve canonical structural/data state and prevent MHV view admission.
No accepted same-feed production calendar/owner-epoch evidence has been added. Rejection is the current required conservative behaviour; no production calendar shortcut or reset is introduced.

## Fresh native evidence

CustomMHVProductionAdmissionHarness includes exact production source and calls real replay, router, canonical storage and view functions. It introduces no price/calendar/API overrides.
Reuses the exact existing H4/D1 v7 snapshots, checked against prior manifest SHA; no restart proofs or historical downloads repeated.
Six existing fixture weekend boundaries × zero/two-bar prefixes × initially-held/previously-unheld owners =24 cases.
Native340/340 assertions PASS; terminal PID6904 exit0. Driver8456 exit0. Strict harness compile0 errors/0 warnings.

Checks cover:
- complete frozen snapshot identity and exact actual closed input;
- the two-bar continuous control advances and matches all102 M08/M09 fields of the prior frozen snapshot;
- direct production replay rejects the actual gap;
- all structural fields in SameOwners (M08/M09 and initialized M12), all TimeframeData fields and recovery metadata remain unchanged after direct refusal;
- retry is idempotent;
- actual router target is the current latest closed candle, not the historical test boundary;
- catch-up from the historical source snapshot meets the same first gap, activates/retains recoveryRequired and stores no partial owner/data updates;
- BUY and SELL MHV views return WAIT_OWNER_RECOVERY, unreadable, no eventId, entry eligibility/window or execution availability;
- zero orders, original7 HST hashes and both snapshots unchanged.

H4 boundary1777665600→1777852800; current router target1785528000.
D1 boundaries1761264000→1761523200,1761868800→1762128000,1762473600→1762732800,1763078400→1763337600,1763683200→1763942400; current router target1785456000.
Epoch integers are synthetic chart-time labels, not authenticated broker UTC.
M12 begins initialized, not from a mature historical M12 snapshot; this is not new M12 signal acceptance.

## Retained initial diagnostic failure

V1 strict compile passed but native148 PASS/12 FAIL: only actual_router_holds failed because the fixture passed an old boundary timestamp to a router contract requiring latest==GetLatestClosedCandleTime.
Direct replay rollback/retry checks already passed. Corrected test target to actual current latest; did not change expected continuity rejection, production source or owner state.
V2 additionally covers initiallyHeld=false and true after independent review identified the previous coverage limit. Initial native rows, source, binary, compile log and config remain in archive initial_invalid_router_target/.
This is a test-fixture correction, not a production bug/fix.

## Review and limits

Independent review: no material diagnostic defect; actual latest-target contract and previously-unheld coverage verified by source review.
Native results were subsequently read from G40; reviewer assertions alone are not used as runtime evidence.
No new fix required in this fail-frozen scope.
The prior242 bounded successful-restart assertions/168 reloaded source bars remain a separate evidence set; these340 negative-admission checks are not counted as successful gap recovery.

Full SIG06 remains HOLD:
1. Accepted same-feed historical boundary/session authority for production admission.
2. Source-proven owner epoch beyond the bounded four-initial-state stress hypotheses.
3. Successful full-owner continuous/recovered comparison through actual production admission across an accepted non-nominal boundary.

The source router/Core/F1 specification is resolved; missing runtime recovery authority is not an unresolved MHV formula or Open-price decision.
No original exit was waived. All77 custom availability and auto-entry OFF. No SIG07/MLV/Re-Entry, unrelated task, merge or deployment.

Evidence: mhv611_production_admission_20261111.json and mhv611_production_admission_20261111.zip.
Archive SHA256 ec6049c513eed9c44861aaf43caa59768d996cf1e2293729ef5049b16506ada2;271289 bytes.
