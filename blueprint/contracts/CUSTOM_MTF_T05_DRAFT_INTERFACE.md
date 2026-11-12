# T05 evaluator draft interface

Status HOLD / NOT VERIFIED. User authorized coding with tests deferred on 2026-11-12. Source baseline `bfbd41b57740b762e3bdf610d7ef5a85026eb8b2` on `feat/custom-mtf-v1-20261108`.

## Draft implementation

`blueprint/source/custom_mtf/CustomEvaluator.mqh` contains `EvaluateCustomSlotSnapshot`, consuming existing parsed slot formulas, a closed event batch, an immutable owner frame and owner-supplied fresh event IDs. The extra frame and fresh-ID parameters make the current producer boundary explicit. The planned batch-only wrapper remains pending producer integration.

The function evaluates OR alternatives within each parsed group and AND across groups, enforces direction and current-frame identity, and publishes a witness only after Context and Trigger both succeed. Trigger components require owner entry eligibility and window state. At least one component must have an owner-declared fresh identity in a continuous batch event. Closed-bar advancement alone does not declare an owner identity fresh.

The draft selects OR components deterministically by physical owner event ID. It selects a fresh anchor using confirmation time, timeframe, concrete signal and owner ID, replaces that group's selected alternative if needed, and retains all matching simultaneous fresh identities for the future reservation consumer. It introduces no source detector, structural TTL or component-time ordering requirement.

RE wildcard matching requires an explicit RE1–RE4 view. Existing RE event identities are treated as opaque. `CustomWitnessContainsSource` only searches the selected components for later SL/TP source validation.

## Integration still required

- A producer must supply authenticated fresh owner IDs after replay/cold-start restrictions and exact physical identity checks. This list must never be populated solely from changed candle timestamps.
- Bind the slot symbol scope and validated configuration revision before evaluation. Map the existing owner frame into concrete RE subtype views where needed.
- Preserve unavailable owner rows. Current custom execution availability stays closed, including MOM/CSA/CSAK read-only views.
- Resolve the final wrapper and scheduler call through the approved T04/T06 owner interfaces. The draft header has no EA caller or include in `BBMA_EA.mq4`.
- T08 must reject an unusable fixed SL/TP source for the selected witness. Exit-source selection among alternative satisfying witnesses remains pending the exit configuration interface.
- Native compile, witness harness, regression, scheduler/runtime wiring and T05 acceptance remain pending. No test or compile was run in this change at the user's request.

Include this header only after the canonical types required by `CustomOwners.mqh` are declared. The module has a unique draft revision. The EA build identity is unchanged because the EA source is unchanged.
