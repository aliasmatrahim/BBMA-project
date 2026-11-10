# Signal-by-signal acceptance — 2026-11-10

User instruction: finish one signal before moving to the next; do no unrelated task. The active task is SIG-01, canonical eCSD / MA5-MA10 early-direction predicate. Shared-consumer regression is part of SIG-01, not development of another signal. Base328d33a0dd4824f4ff3dcb2a2b2823a69e12bc9b / Draft PR303 / feat/custom-mtf-v1-20261108.

## SIG-01 eCSD — IN PROGRESS, until evidence bundle passes

Spec: M10_DIRECTION_CLOSE_ONLY_USER_DECISION_20261110.md. BUY Close above MA5High and MA10High; SELL Close below MA5Low and MA10Low. Open is not read by this predicate. Relevant equality is rejected. Shift0/negative is rejected. M06 readiness still owns complete valid data, and raw direction is not execution authority.

Acceptance checklist:
- [x] Actual extracted baseline detector fails a valid Close-beyond-MAs case solely due Open (RED observed).
- [x] Small canonical eCSD patch and reusable close-pair helper; unique Build6.07 identity.
- [x] Nine protected CSD/MOM/owner/consumer function bodies unchanged. Caller signatures unchanged. No duplicate detector or M15 updater.
- [x] Cloud regression76/76 after change; runner/helper py_compile/diff checks.
- [x] Initial native full EA/harness strict compile0 errors/0 warnings and176 fixture/delegation checks; extended final190-check harness pending.
- [ ] Final native eCSD harness: synthetic BUY/SELL/Open/equality/readiness cases, seven-TF140 actual closed-history comparisons, D1/M11/M12 consumer delegation/identity, no orders.
- [ ] Affected source/native regression all pass and exact source/include/harness/binary hashes bound.
- [ ] Actual M27/ProcessPair monitor OFF/ON parity bound to final source; intended old/new differences against frozen6.06 reviewed. Orders remain disabled/captured.
- [ ] Evidence, branch/commit/checkpoint/Draft PR saved and verified before next signal.

This task does not add an eCSD input token to the approved11-signal custom grammar, alias the user's MidBB CSA to eCSD, activate custom admission, certify arbitrary history/session recovery or claim profitability.

The current helper migration is intentionally per signal: legacy CSD still uses its historical body-span code and will be addressed only in its own task. Thus Build6.07 is an intermediate signal migration, not full M10 Close-only acceptance or release-ready. Current same-candle precedence Momentum > CSD > eCSD remains in untouched consumers. Earlier same-signal observations can now qualify on more source candles; no new first-cross/colour/TTL filter is added, and later custom identity/admission gates remain OFF.

## Queue after SIG-01 acceptance

SIG-02 CSA (user MidBB direction) -> SIG-03 CSAK/CSD (MA pair+MidBB) -> MOM -> Extreme -> MHV -> MLV -> Re-Entry. MHV/MLV remain one canonical M09 engine with alias-specific acceptance, never duplicate detectors. Previously VERIFIED signal work is reused and only affected/unverified criteria are checked. Do not start a later signal if SIG-01 is PARTIAL/HOLD.

No unrelated queue task, merge, deployment or trading activation. All77 semantic availability cells/custom auto-entry OFF. Native/market-history scope limitations must be retained rather than promoted to universal seven-TF or execution acceptance.
