# Approved Custom MTF queue — 2026-11-10

Active user sequence override2026-11-10: SIG-01 eCSD, SIG-02 CSA, SIG-03 CSAK/CSD, SIG-04 MOM and SIG-05 Extreme have bounded VERIFIED acceptances. Verify SIG-05 final publication before SIG-06 MHV. Finish one signal before another; do no unrelated task. All custom execution remains OFF.

Authority: user approved continuous execution with checkpoint after each task. This is a scoped workstream queue, not a replacement for the canonical MASTER_QUEUE. Source/branch authority and dependencies remain mandatory. Auto-entry/availability remain OFF; no merge or trading activation.

| Task | Scope / exit | Status at checkpoint |
|---|---|---|
| T04-A | Actual tick/timer handlers → M27 → observer → available producers → owner views; moving bars, no duplicate state, no custom-only canonical dispatch | VERIFIED for monitor fixture on GBPUSD M1/M5/M30, 2026-08-04 02:00–04:00 chart time, native12/12. No full seven-TF or execution claim. |
| T04-B | Source-proven weekend/session/DST gaps and cold-start reconstruction; never replay historical triggers as fresh entries | HOLD: missing history/session-boundary provenance and cold-start owner-epoch proof; no synthetic fill or assumed NONE. Contiguous anchored replay27/27 remains verified; Build6.03 read-only seven-TF weekend inventory still lacks authenticated historical session/owner-epoch proof. |
| T04-C | Canonical TF owner producers for custom-only symbols, isolated state, no canonical execution dispatch | VERIFIED requested-monitor wiring on Build6.00, native23/23; executable/recovered eligibility still depends on B and later authority gates. |
| T04-D | Shared MOM/CSA/CSAK mappings, no duplicate detectors | PARTIAL overall: eCSD6.07, CSA6.08 and CSAK/CSD6.09 predicate/read-only source acceptances VERIFIED; next serial MOM review. Custom trigger/selection/executable availability remains OFF and pending. |
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

2026-11-10 source/epoch retrieval: new V05 frame/candidate inventory records added; no source-discriminating candle or trusted M08/M09 historical epoch accepted. M11 epoch/Q10 validation snapshot excluded for wrong owner/build. B/D/E statuses unchanged; no dependency promotion. See CUSTOM_MTF_SOURCE_EPOCH_RETRIEVAL_20261110.md for exact next action.

Internet2026-11-10: primary researcher formula recovered (MidBB body cross plus MA close-side). Third-party implementation only; T04-D remains VERIFICATION REQUIRED, B/E recovery HOLD. Details in CUSTOM_MTF_INTERNET_DIRECTION_EVIDENCE_20261110.md.

2026-11-10 three-formula comparison completed in offline/source-review scope: current code matches locked F1; no founder-exclusive numeric open/equality decision. F2 event ambiguity and F1/F3 geometry/equality differences documented. T04-D/B/E/F statuses unchanged. See CUSTOM_MTF_THREE_FORMULA_CORE_COMPARISON_20261110.md for verified arithmetic and exact next action.

2026-11-10 USER DECISION supersedes earlier Open HOLD entries: Close-only direction accepted; no more Open source search. Implementation has not yet changed. Next eligible work is the shared canonical M10 patch and affected regression, then CSA/CSAK owner/materialization acceptance. B/E session/epoch recovery and F/T05 dependencies remain gated; all77 availability/auto-entry OFF.

SIG-01 acceptance2026-11-10: eCSD Close-only canonical source190 native/140 actual closed-history comparisons, native compile0/0,11 affected regressions, cloud76/76, full controller parity16 M15 cycles PASS. Current tested code3c14938; acceptance limits and initial RED in CUSTOM_MTF_ECSD_SIGNAL_ACCEPTANCE_20261110.md. Next eligible SIG-02 CSA after publication; CSD/CSAK still requires its own Close-only migration. No T04-D/F or execution availability promotion.

SIG-02 acceptance2026-11-10: native154/154 incl140 historical comparisons; actual controller210 CSA views,16 cycles/profile,12224-row OFF/ON/6.07 parity;14 native groups PASS; exact hash bindings verified. No new full-pytest claim. Next only SIG-03 CSAK/CSD after verified publication; historical Open investigation is superseded. No T04-F/execution promotion.

SIG-03 CSAK/CSD IN_PROGRESS: Build6.09 rev002; actual extracted baseline RED rejects Close-beyond-all due Open. Canonical Close-only detector and shared M10 CSAK source/context now native211/211 and182/182, compile0E0W. Native regression/controller driver5580 is running; no final acceptance or next-signal promotion. Initial rev001 compile had2 array-initialization warnings, corrected explicitly in rev002 before native passes. All77 availability/entry OFF.

SIG-03 FINAL acceptance2026-11-10 supersedes IN_PROGRESS entry above: Build6.09 rev002 canonical211/211, final context189/189, characterization141/141,17 native groups, strict0E0W, actual controller420 combined CSA/CSAK views,16 cycles/12224 rows per case, OFF/ON exact parity. Frozen6.08 differs296 intended owner/M12 Type4 rows, Decision differences0; zero attempts.19 bindings and3 traces verified6212 exit0; independent source review no material defect, High-only revision test passed7TF. Final acceptance CUSTOM_MTF_CSAK_SIGNAL_ACCEPTANCE_20261110.md. Next only SIG-04 MOM after publication verification. All77 availability/auto-entry OFF; no merge/deployment.

SIG-04 MOM IN_PROGRESS / CONFIRMED BUG: native6.09 missing required Close9 gives ready=false/raw=true; partial BB arithmetic escaped readiness. Valid-data native72 and1400 iBands comparisons/controller630 views passed but do not close this failure. Scope includes unavailable-vs-no-Momentum propagation before M09/M11/M12/C044/M27 cursor/state mutations. Source repair not yet applied at this checkpoint. Plan docs/superpowers/plans/2026-11-10-sig04-momentum-readiness.md. No Extreme/later signal until SIG-04 closes. All77 availability/entry OFF.

SIG-04 code checkpoint: Build6.10 rev003 / LF SHA ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae. Actual native unavailable-source/cursor/owner/freeze/retry suite167/167 and strict full EA/harness0E0W. Includes native RED1/159, missing-H4-retry RED164/1 and checkpoint/atomicity RED165/2 before fixes. Current driver4376 affected regression/controller RUNNING; full SIG-04 remains IN_PROGRESS. Do not duplicate processes or start next signal.


SIG-04 FINAL acceptance2026-11-10 supersedes IN_PROGRESS entries: Build6.10 rev003 / source ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae; native72 plus167, all18 groups and strict0E0W;20 bindings verified9520 exit0. Actual controller630 combined views/16 cycles/12224 rows per case, OFF/ON/6.09 identical, zero decisions/attempts. Readiness/owner/recovery/atomicity REDs and initial incomplete synthetic fixture retained. See CUSTOM_MTF_MOM_SIGNAL_ACCEPTANCE_20261110.md, mom610_final_summary.json and full gzip archive/traces. Source unchanged from0da5720; only fixture prerequisites updated. Next only SIG-05 Extreme after verified publication. No session/epoch/T04-F/custom execution/merge/deployment promotion.


SIG-05 Extreme IN_PROGRESS: Build6.11 rev003 / LF SHA a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb. Native source RED8/14 exposed duplicated partial-data Momentum and owner VOID; first repair22/22. Native reviewed Extreme-handover expansion106/35 RED, including7 actual M09 source-revision escapes, now guarded with availability propagation to all3 callers. Driver8896 current source141/lifecycle716 +18 native groups/controller baseline610 RUNNING. Do not duplicate or start MHV. Plan/ext611_checkpoint.json carry remaining work. All77 availability/auto-entry OFF.


SIG-05 FINAL supersedes IN_PROGRESS: Build6.11 rev003, source a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb. Native141 source/handover +716 valid lifecycle/history,19 specialized groups (21 current total), frozen6.10 lifecycle716, strict0E0W. Controller180 EXT+630 M10 views/15 frames,16 cycles/12224 rows per profile, OFF/ON/6.10 exact parity; zero decisions/attempts.23 bindings plus separate baseline harness and3 full traces verified12828 exit0. Full manifest/RED archive ext611_evidence.json.gz; acceptance CUSTOM_MTF_EXTREME_SIGNAL_ACCEPTANCE_20261110.md. Next only SIG-06 MHV after publication verification. No session/epoch/T04-F/entry/merge/deployment promotion.
