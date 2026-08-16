# M18 Signal Scoring / Label Contract

## Status
P0 Step 9 — **COMPLETED AT ARCHITECTURE CONTRACT LEVEL**.

M18 is retained only as optional observability / display metadata. It is not a BBMA strategy authority and must never participate in entry selection, direction resolution, signal validation, SL/TP resolution, risk approval or execution.

## Finding
The legacy M18 function was labelled `SIGNAL SCORING ENGINE (LABEL ONLY)` but still manufactured a numeric quality score from arbitrary weights and unconditional bonuses, including unconditional `BBShape:10` and `MultiTF:5` points.

Those values are not established BBMA/Oma Ally source rules. They also conflict architecturally with the locked M15 contract, which explicitly removed arbitrary SAFE/NORMAL/AGGRESSIVE score/tier gating and does not define REM/RRE/REE quality superiority.

The old orchestration call also scored raw detector/state snapshots (`extreme`, `mlv`, `reEntry`) rather than the final atomic M15 decision. Step 6 already removed that active call from the final decision path. Step 9 makes the M18 implementation consistent with that architecture.

## Locked ownership
M18 MAY:
- expose a human-readable label for the final selected decision;
- expose source type / direction / timeframe identity for dashboard or diagnostics;
- return neutral compatibility score fields when old structs/UI still expect them.

M18 MUST NOT:
- set or change `BBMA_Decision.Valid`;
- set or change `DecisionState` or `RejectionReason`;
- select BUY vs SELL;
- rank or prefer RE_ENTRY, REM, RRE or REE;
- alter `PriorityTier`;
- create or modify EntryPrice, StopLoss or TakeProfit;
- affect `MaxSLPips`, `MinRRRatio`, lot size, portfolio limits or any risk result;
- turn a raw Extreme/MLV/CSD/eCSD/CSM into an executable signal;
- recreate M08/M09/M10/M12/M13/M14/M15/M16/M17 logic.

## Numeric score policy
For the current architecture, numeric quality scoring is **neutralized**:
- `Score = 0`;
- `Level = LEVEL_NONE`.

No artificial A+/A/B/C/D grade is generated for execution candidates.

This avoids claiming an unsupported BBMA quality hierarchy while preserving compatibility with existing `SignalScoreResult` / `Signal.Score` / `Signal.Level` fields if UI code still references them.

## Label metadata
When a valid final decision is supplied, M18 may emit a non-authoritative text label containing only facts already owned upstream, for example:
- final `SignalType`;
- final `Direction`;
- validated source timeframe where available.

The label is descriptive only. It is not a confidence score.

## Input compatibility
`SignalMode`, `ScoreDisplayThresholdManual` and `EnableSignalScoring` are not trading-authority inputs.

- `SignalMode` remains deprecated for M15 entry authority.
- `ScoreDisplayThresholdManual` is display/compatibility-only and must never block a trade.
- `EnableSignalScoring` controls optional M18 label metadata only and must never alter a decision state.

## Downstream boundary
M19 begins the risk-filter layer after M17 has resolved/validated the approved SL/TP payload.

M19–M24 must consume the already-selected decision. They may reject or safely execute/manage it according to their explicit ownership, but they must not consult M18 numeric score/grade as a hidden strategy filter.

## Verification requirement
Before Master Blueprint lock, downstream audit must confirm there is no active reference in M19–M24 that uses M18 `Score`, `Level`, `SignalMode` or `ScoreDisplayThresholdManual` to gate, rank or mutate a trade.

## Project decision
M18 remains in the 27-module architecture for observability compatibility, but **quality scoring has zero trading authority** and unsupported arbitrary weights are removed.
