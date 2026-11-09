# Approved Custom MTF queue — 2026-11-09

Authority: user approved continuous execution with checkpoint after each task. This is a scoped workstream queue, not a replacement for the canonical MASTER_QUEUE. Source/branch authority and dependencies remain mandatory. Auto-entry/availability remain OFF; no merge or trading activation.

| Task | Scope / exit | Status at checkpoint |
|---|---|---|
| T04-A | Actual tick/timer handlers → M27 → observer → available producers → owner views; moving bars, no duplicate state, no custom-only canonical dispatch | VERIFIED for monitor fixture on GBPUSD M1/M5/M30, 2026-08-04 02:00–04:00 chart time, native12/12. No full seven-TF or execution claim. |
| T04-B | Source-proven weekend/session/DST gaps and cold-start reconstruction; never replay historical triggers as fresh entries | HOLD: missing history/session-boundary provenance and cold-start owner-epoch proof; no synthetic fill or assumed NONE. Contiguous anchored replay27/27 remains verified; Build6.03 read-only seven-TF weekend inventory still lacks authenticated historical session/owner-epoch proof. |
| T04-C | Canonical TF owner producers for custom-only symbols, isolated state, no canonical execution dispatch | VERIFIED requested-monitor wiring on Build6.00, native23/23; executable/recovered eligibility still depends on B and later authority gates. |
| T04-D | Shared MOM/CSA/CSAK mappings, no duplicate detectors | PARTIAL: Build6.01 MOM/CSM shared snapshot/native55/55 and integration12/12 VERIFIED; CSA/CSAK exact alias/admission mapping still verification required. |
| T04-E | MHV/MLV on source-accepted TFs through the same M09 owner | PARTIAL: E/1 foundation and E/2 monitor pipeline VERIFIED through Build6.03 (wiring52/52, seven-TF anchored replay57/57, moving integration12/12). NEXT E/3 canonical higher-TF M09 pre-freeze parent-ownership integration. Extra semantic/executable admission remains OFF; full source epoch/session acceptance pending. |
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
