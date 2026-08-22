# CORE-V2-F1 — MHV/MLV Canonical Lifecycle

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — STRUCTURAL LIFECYCLE MODEL USER APPROVED; CONTEXT/FORMATION/ANCHOR/RETEST DETAILS STILL PENDING**
Branch: `blueprint-dev`

## User-approved decision 1 — MHV/MLV is a structural lifecycle, not a one-candle detector
The project adopts **ONE CANONICAL MHV/MLV STRUCTURAL LIFECYCLE / OWNER-STATE MODEL**.

Accepted high-level lifecycle:

`PRIOR EXTREME / TP CONTEXT -> LOSS OF PRIOR MOMENTUM -> MHV/MLV FORMATION -> MARKED BODY/REFERENCE -> RETEST / ACTIVE SETUP -> VALID CONTINUATION OR VOID/SUPERSESSION`

Operational meaning:
- `MHV` and `MLV` remain terminology aliases for one setup family unless stronger source evidence later distinguishes them;
- MHV/MLV must not be represented as several independent Boolean detectors that can disagree about the same source-timeframe structure;
- the setup may develop over multiple closed candles and therefore requires state/owner continuity rather than a current-candle-only classification;
- the source-described marked body/reference and later retest belong to the same lifecycle and must not be replaced by a synthetic fixed-point neckline merely because the legacy detector currently uses one;
- double/triple-top or bottom and H&S-like shapes are permitted morphology/examples, not mandatory universal formulas;
- a source-valid close beyond the relevant outer Bollinger Band voids the MHV/MLV interpretation and returns authority to Momentum/CSM rather than allowing MHV to remain simultaneously valid;
- MHV/MLV remains a setup/context stage and does not become direct entry authority merely because its lifecycle is modeled explicitly;
- implementation must converge on one canonical owner-state result so legacy `DetectMHV()` and any MLV path cannot maintain contradictory semantics.

## Evidence classification
This decision is **DIRECT SOURCE STRUCTURAL CONCEPT + PROJECT STATE-MACHINE MAPPING**.

Source support:
- Finale V05 OA-F-V05-006 teaches MHV after Extreme + TP Wajib and describes loss of prior momentum;
- OA-F-V05-007 states that an outside-outer-BB close voids MHV and is treated as Momentum;
- OA-F-V05-008 teaches marked body/line plus retest structure and shows double/triple/H&S-like morphology;
- OA-F-V05-009 describes MHV as a setup / early new-trend stage rather than a direct entry signal.

The exact software state-machine names and transitions are project engineering semantics. They must preserve the source sequence and invalidation behavior and must not be presented as verbatim Oma Ally software rules.

## Rejected alternatives
- single-candle MHV/MLV detector as the complete source model;
- mandatory exact double/triple-top or bottom formula;
- mandatory H&S morphology;
- treating MHV as merely another name for Extreme reversal;
- keeping independent MHV and MLV detector families that can disagree for the same structure.

## Remaining specification before code
The structural lifecycle model is locked, but deterministic sub-rules still need one-by-one review before M09 is patched:
- whether a source-valid prior Extreme/TP-Wajib context is mandatory for every canonical MHV/MLV candidate or merely the normal taught sequence;
- what exact BBMA condition proves `LOSS OF PRIOR MOMENTUM` without inventing ATR/ADX/pip thresholds;
- how the marked highest/lowest body reference is owned and frozen;
- what constitutes the retest/active-setup interaction;
- lifecycle supersession/void rules beyond the explicit outer-BB close;
- migration/removal of legacy duplicate detector semantics after the canonical contract is complete.

No EA code change is authorized by this decision alone.
