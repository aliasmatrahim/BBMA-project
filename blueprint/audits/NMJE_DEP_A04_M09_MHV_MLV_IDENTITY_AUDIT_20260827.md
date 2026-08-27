# NMJE Dependency Hardening Audit — DEP-A04 M09 MHV/MLV Lifecycle Identity

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Baseline verdict
M09 is materially aligned with the locked F1/F2 lifecycle and is suitable for NMJE N1/N2 observation, but needs identity/replay hardening before N3 enforcement.

## Strengths observed
- MHV/MLV is a stateful lifecycle, not a one-candle detector.
- Parent requires a reversal-confirmed M15 Extreme.
- Normal TP-Wajib is completed before loss-of-momentum development.
- Formation freezes the most-extreme body reference; the move-away candle is excluded from the frozen body.
- Retest uses later price interaction with the frozen marked body.
- Same-cycle eCSD/CSD may take direction ownership without retroactively deleting completed MHV provenance.
- Opposite RAW Extreme is only a supersession candidate; the old MHV is superseded only after the opposite Extreme reaches reversal-confirmed maturity.
- No fixed lifecycle timer is introduced.

## Hardening findings before N3

### DEP-A04-F1 — Stable MHV CycleID/EventID
Current identity is represented by parent raw/confirmation times plus MHV confirmation/body fields, but there is no explicit immutable cycle identifier for NMJE/recovery.
Action: derive/freeze a canonical read-only MHV CycleID from pair + M15 + MHV direction + parent Extreme identity + formation anchor. Do not add a quality score.

### DEP-A04-F2 — Parent identity should be canonical, not timestamp-only
ParentConfirmationCandleTime is strong provenance, but N3 should bind to the canonical parent Extreme EventID once DEP-A03 identity hardening exists.
Action: M09 consumes/records M08 parent identity; M09 must not reconstruct an independent Extreme formula.

### DEP-A04-F3 — Terminal-state monotonicity
VOID/SUPERSEDED are present and explicit. N3 recovery must prove an old terminal cycle cannot resurrect from stale state when a newer parent has already taken ownership.
Action: add monotonic cycle/epoch checks and replay tests; a newer canonical parent creates a new cycle identity.

### DEP-A04-F4 — Supersession helper writes the parent Extreme
InstallMHVSupersessionParent() directly constructs a reversal-confirmed Extreme parent during M09 supersession handling. This is architecturally sensitive because M08 is supposed to be the canonical Extreme owner/single writer.
Action: before N3, audit/refactor ownership so M09 requests/observes the M08 canonical opposite Extreme transition rather than becoming a second canonical Extreme writer. Preserve current source semantics; do not invent a new BBMA rule.

### DEP-A04-F5 — Replay/recovery equivalence not yet proven
M09 depends on mutable fields such as ParentConfirmationCandleTime, TPWajibCandleTime, StartCandleTime, ProvisionalBodyAnchor, FrozenMarkedBody, PreviousClose and supersession candidate state.
Action: deterministic replay suite must prove uninterrupted and restarted histories produce identical lifecycle state/body/parent identity; otherwise NMJE lineage becomes UNRESOLVED for new-entry use.

### DEP-A04-F6 — MHV maturity distinction must remain intact
NMJE may observe PARENT_READY/TP_COMPLETE/LOSS_DEVELOPING as BUILDING context, but only source-approved mature states may satisfy executable combination requirements.
Action: N3 cannot promote pre-formation MHV because nesting is aligned.

## N3 readiness
- Canonical lifecycle: PASS
- Closed-candle/stateful processing: PASS
- Frozen formation body: PASS
- Parent provenance: PASS/PARTIAL
- Single-writer authority: HARDEN (M09 parent-install helper)
- Stable immutable cycle identity: HARDEN
- Restart/replay equivalence: NOT YET PROVEN
- Safe for N1/N2 observation: YES
- Safe for N3 enforcement today: NO

## Timing
Documentation-only now. Implement after current runtime evidence is preserved and before mandatory N3 enforcement.

## Next
DEP-A05 — M10 direction/Momentum/eCSD/CSD/CSM state audit.
