# M10 direction: Close-only user decision — 2026-11-10

Status: ACCEPTED USER SEMANTIC DECISION. Implementation pending; not native/runtime verified against this new decision.
Task: C / T04-D. Branch feat/custom-mtf-v1-20261108. Base6a9964ece8da5f36cada0c2587ce1c4ba42a6f64. Recorded at the user's explicit request; publication SHA in Draft PR303.

## Authority and resolved meaning

The user explicitly clarified that candle Open is unimportant to CSA/direction classification; the important condition is the closed price beyond the relevant MA, MidBB, or both. The user subsequently requested that this information be saved. This is the project's user-directed semantic reconciliation, not a claim that a new authenticated founder quote was discovered.

Use a valid completed source candle and the corresponding finalized indicator values:

| Direction condition | BUY | SELL |
|---|---|---|
| Relevant MA pair | Close > MA5High and Close > MA10High | Close < MA5Low and Close < MA10Low |
| MidBB direction | Close > MidBB | Close < MidBB |
| Relevant MA pair plus MidBB | Both BUY conditions above | Both SELL conditions above |

Open is not a direction-admission condition. Do not require body spanning any line, Open on the opposite side, a candle-colour condition derived from Open, or a previous-bar cross merely to reintroduce the rejected Open restriction. Close equal to a required line does not pass that strict beyond-line condition; existing close-side strictness is retained, not a new Open-equality gate.

Keep product nomenclature traceable: user MidBB CSA must not silently alias MA-only legacy eCSD; strong MA+Mid correspondence with CSD/CSAK remains subject to shared materialization/wiring checks. Teaching material can use CSA as a broader umbrella with early/strong subtypes. Naming alone is not a source conflict.

## Scope and preserved ownership

This decision applies to direction predicates, not all candle-body calculations in the EA. Existing source-defined Extreme/MHV marked-body anchors and other unrelated uses of Open are not removed. It does not change MOM expanding/directional BB rules, Re-Entry structure/timing, M09 lifecycle, frozen parent ownership, M15 authority, risk or execution.

Signal identity/dedup, Context versus Trigger and entry eligibility belong to their existing owners/queue gates. Do not count a repeated matching observation as a fresh executable event simply because this predicate passes. No new generic TTL, first-event reset or expiry rule is defined here. Raw direction remains a signal, not standalone order authority.

## Superseded decision boundary

The open-side ambiguity from earlier three-formula/source audits is RESOLVED BY USER. Do not reopen it, seek further Open counterexamples, or retain it as a source HOLD. The old all-line body-span interpretation is superseded as the required direction target. The paper's Mid-only Open restriction is likewise not the accepted target.

Earlier audits and arithmetic results remain historical evidence of the old implementation. Their native/cloud PASS does not prove compliance with this newly accepted target. Current Build6.06 source SHA0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e still reads Open in DetectCSD/DetectECSD and uses body-cross predicates. This is a CONFIRMED IMPLEMENTATION GAP relative to this decision; no source patch or new compile/runtime result is claimed by this documentation checkpoint.

## Remaining signal work and exact next action

1. Apply the smallest shared canonical M10 close-side change and update affected consumers/tests; do not add a parallel detector. Bump build identity, native compile, targeted M10/M11/M12/M09/M27 regression and actual owner/controller validation before implementation acceptance.
2. Bind CSA/CSAK source views and signal identities to that shared owner, then verify Context/Trigger materialization and duplicate handling without inventing Open/TTL rules.
3. MHV/MLV: authenticated same-feed session history and actual structural M08/M09 cycle-origin epoch remain missing for full gap/cold-start recovery. Seeded handovers and unrelated M11 epochs do not close this gate.
4. Re-Entry: accepted EntryCandle timing needs actual custom-TF runtime acceptance; structural validity is not generic TTL and does not itself grant a late entry.
5. Complete the per-signal/per-TF acceptance matrix and integrated T04-F only after dependencies pass. Monitor wiring is not executable availability.

These are implementation/runtime evidence gaps, not a request for the user to re-decide Open. No other new signal-definition conflict is established by this checkpoint. All77 custom semantic availability cells and custom auto-entry remain OFF. No merge, deployment or trading activation.
