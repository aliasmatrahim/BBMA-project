# Approved Custom MTF queue — 2026-11-10

Authority: user approved continuous execution with checkpoint after each task. This is a scoped workstream queue, not a replacement for the canonical MASTER_QUEUE. Source/branch authority and dependencies remain mandatory. Auto-entry/availability remain OFF; no merge or trading activation.

| Task | Scope / exit | Status at checkpoint |
|---|---|---|
| T04-A | Actual tick/timer handlers → M27 → observer → available producers → owner views; moving bars, no duplicate state, no custom-only canonical dispatch | VERIFIED for monitor fixture on GBPUSD M1/M5/M30, 2026-08-04 02:00–04:00 chart time, native12/12. No full seven-TF or execution claim. |
| T04-B | Source-proven weekend/session/DST gaps and cold-start reconstruction; never replay historical triggers as fresh entries | HOLD: missing history/session-boundary provenance and cold-start owner-epoch proof; no synthetic fill or assumed NONE. Contiguous anchored replay27/27 remains verified; Build6.03 read-only seven-TF weekend inventory still lacks authenticated historical session/owner-epoch proof. |
| T04-C | Canonical TF owner producers for custom-only symbols, isolated state, no canonical execution dispatch | VERIFIED requested-monitor wiring on Build6.00, native23/23; executable/recovered eligibility still depends on B and later authority gates. |
| T04-D | Shared MOM/CSA/CSAK mappings, no duplicate detectors | PARTIAL: Build6.01 MOM/CSM shared snapshot/native55/55 and integration12/12 VERIFIED; CSA/CSAK exact alias/admission mapping still verification required. |
| T04-E | MHV/MLV on source-accepted TFs through the same M09 owner | PARTIAL: E/4 pre-freeze transaction/controller mechanics VERIFIED on exact6.06: native61/61, actual ProcessPair seeded D1/H4/H1 handovers3/3, monitor ON/OFF full-trace parity16 cycles/profile, affected regressions/startup PASS. Natural formation/session/cold-start reconstruction and source-epoch admission remain HOLD; all semantic/executable availability OFF. |
| T04-F | Integrated T04 acceptance, entry-window/isolation/reinit/regression, per-row availability evidence | BLOCKED by remaining B–E/gates. |
| T05 | Context/Trigger AND/OR evaluator and concrete witness | PENDING after required T04 owner/eligibility interfaces pass. |
| T06 | M15 final authority and arbitration | PENDING. |
| T07 | Physical dedup, reservation and retry | PENDING. |
| T08 | Exit profiles / frozen TradePlan | PENDING. |
| T09 | Sizing / exposure / hedging | PENDING. |
| T10 | Execution / recovery / lifecycle | PENDING. |
| T11 | Labels / monitor / attribution | PENDING. |
| T12 | Integrated acceptance / documentation / handoff | PENDING. |

Do not redo VERIFIED work. If a task is HOLD, continue only an independent eligible portion; do not silently bypass that dependency at acceptance. Every task records source commit, evidence, remaining work and exact next action in progress.md and the Draft PR.

Follow-up evidence: `CUSTOM_MTF_REMAINING_GATE_REVIEW_20261109.md`; four G40 provenance metadata records hashed, native M10 characterization141/141, fresh full EA/harness compile0/0 and cloud regression73/73. These subtasks do not close B/D/E or advance F. Next required inputs are same-feed historical session/owner epoch and exact CSA/CSAK mapping; guarded canonical parent handover remains unchanged.

C+1 follow-up: user selected source-example verification and pre-freeze M09 integration. Build6.06 is a WIP candidate: cloud2/2 targeted (12 transaction-fixture checks),75/75 full suite; native compile/runtime NOT VERIFIED because G40 offline. Source-review evidence still does not distinguish the exact open-side requirement. T04-E/4 native harness prepared, not passed; no B/D/E/F or downstream acceptance status is promoted. Exact next action is native6.06 compile/controller parity plus original V05/V06 chart-frame review.


2026-11-10 superseding native checkpoint: see CUSTOM_MTF_E4_NATIVE_ACCEPTANCE_20261110.md, native606_evidence.json and both controller606 manifests. The earlier offline/WIP native status above is historical. B/D/E overall remain unresolved; F/T05+ stay blocked. C source frames corroborate close-side wording but do not decide open-side mapping. Exact next action: source-discriminating CSA/CSAK example plus same-feed historical session/UTC and trusted owner-epoch evidence, then targeted recovery validation. No merge/activation.

2026-11-10 refresh: final published-harness cloud suite75/75 PASS after workspace recovery; six full traces/five JPEGs rebound, four interrupted addenda reconciled. Source unchanged. V05_2062 timestamp corrected to34:22 (six seconds after routed window). No B/D/E/F availability promotion. See progress.md latest reconciliation.
