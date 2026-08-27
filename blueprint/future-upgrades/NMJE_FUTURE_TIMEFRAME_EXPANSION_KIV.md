# NMJE Future Timeframe Expansion — KIV

Status: **PARKED / FUTURE UPGRADE / DO NOT IMPLEMENT NOW**

Activation gate: **Only revisit after the current NMJE/N3 is considered mature/perfect and its runtime validation is closed.**

Purpose: keep future timeframe-expansion ideas separate from the current production/core workstream so they cannot accidentally alter current BBMA/NMJE behaviour.

## Current canonical chain remains unchanged

`D1 -> H4 -> H1 -> M15`

No W1, M30 or M5 authority is approved by this record.

## Future proposal A — W1

Candidate role: **Macro Context / observation layer**.

Principles:
- W1 must not automatically become a universal hard gate.
- Source reconciliation is required before assigning W1 authority over D1.
- Initial implementation should be observation/shadow-only.
- Measure whether W1 provides useful information before allowing it to alter entry decisions.

## Future proposal B — M5

Candidate role: **Execution Refinement / Additional Entry child layer**.

Principles:
- M5 must not independently overthrow D1/H4/H1 ownership.
- Prefer activation only after an eligible higher-timeframe BBMA setup already exists.
- Candidate uses include entry refinement and source-valid signal-based additional Re-Entry/pyramiding.
- Initial implementation should be observation/shadow-only.

## Future proposal C — M30 readiness

M30 is intentionally not required in the first expansion, but the architecture should be designed so it can be added later without another major refactor.

Candidate role:
`H1 setup -> M30 intermediate development -> M15 completion/entry -> M5 execution refinement`

Important:
- M30 must not silently alter canonical source-defined combination signatures such as REM/RRE/REE.
- It may provide nested/intermediate information without becoming a mandatory component unless later source/architecture evidence justifies that role.

## Required architecture preparation before any expansion

1. Close current NMJE/N3 runtime validation first.
2. Lock explicit role/authority/permissions for every timeframe before coding.
3. Generalize NMJE away from scattered fixed four-timeframe assumptions toward a configurable hierarchy/node model.
4. Each timeframe node should be able to define at minimum:
   - timeframe;
   - parent;
   - child;
   - role;
   - owner authority;
   - allowed signals/states;
   - handover permission;
   - closed-candle state/cache.
5. Preserve strict state isolation between timeframe nodes.
6. Define deterministic cross-TF conflict/handover rules before execution authority is granted.
7. Audit new-bar synchronization, caching and performance for 20-pair operation before enabling additional streams.
8. Add new TFs first in **shadow/observation mode**: calculate/log them but do not allow them to open, block or close trades.
9. Compare shadow decisions against the canonical engine before granting limited authority.

## Candidate long-term hierarchy (concept only)

Possible future structure:

`W1 -> D1 -> H4 -> H1 -> M30 -> M15 -> M5`

This is an engineering concept, **not a locked Oma Ally canonical hierarchy**.

Suggested functional layers:
- W1: macro context
- D1: major trend authority
- H4: immediate structural parent
- H1: main setup
- M30: optional intermediate/bridge context
- M15: completion/entry
- M5: execution refinement/additional entry

## Core design principle

The goal is **not to maximize the number of timeframes**. The goal is for NMJE to understand nested BBMA cycles: parent vs child, owner vs retracement, confirmation vs opposition, and the evidence required for an actual owner handover.

A lower-timeframe opposite signal must not automatically overthrow its higher-timeframe parent. Expansion should improve structural resolution without creating all-timeframe-alignment paralysis or conflicting equal-authority signals.

## Rollout concept when eventually activated

Phase 1: architecture/hierarchy-readiness audit.

Phase 2: W1/M5 shadow mode; keep canonical trading decisions unchanged.

Phase 3: evaluate runtime information gain and false/conflicting states.

Phase 4: grant only narrowly defined authority where justified.

Phase 5: add M30 later through the generalized hierarchy if it demonstrates useful information gain.

## Explicit KIV constraint

Until the activation gate is met:
- do not modify current EA code for W1/M5/M30;
- do not change current REM/RRE/REE signatures because of these proposals;
- do not make W1 a D1 hard gate;
- do not make M5/M30 standalone strategic owners;
- do not mix this future-upgrade work with current runtime/NMJE stabilization fixes.
