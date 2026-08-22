# CORE-V2-F1 — MHV/MLV Canonical Lifecycle

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — STRUCTURAL LIFECYCLE + MANDATORY PRIOR EXTREME + TP-WAJIB COMPLETION USER APPROVED; EXTREME MATURITY/LOSS-OF-MOMENTUM/ANCHOR/RETEST DETAILS STILL PENDING**
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

### Evidence classification
This decision is **DIRECT SOURCE STRUCTURAL CONCEPT + PROJECT STATE-MACHINE MAPPING**.

Source support:
- Finale V05 OA-F-V05-006 teaches MHV after Extreme + TP Wajib and describes loss of prior momentum;
- OA-F-V05-007 states that an outside-outer-BB close voids MHV and is treated as Momentum;
- OA-F-V05-008 teaches marked body/line plus retest structure and shows double/triple/H&S-like morphology;
- OA-F-V05-009 describes MHV as a setup / early new-trend stage rather than a direct entry signal.

The exact software state-machine names and transitions are project engineering semantics. They must preserve the source sequence and invalidation behavior and must not be presented as verbatim Oma Ally software rules.

## User-approved decision 2 — canonical MHV/MLV requires prior Extreme context
The project adopts **A PRIOR SOURCE-VALID EXTREME IN THE SAME SOURCE-TIMEFRAME / OWNER-CYCLE AS A MANDATORY PRECONDITION FOR A CANONICAL MHV/MLV CANDIDATE**.

Accepted operational rule:
- a generic inside-BB consolidation, loss of impulse, or local double/triple-top/bottom is not sufficient by itself to create a canonical MHV/MLV owner;
- the MHV/MLV lifecycle must be traceable to a prior Extreme context belonging to the same structural cycle on that source timeframe;
- if no such prior Extreme can be established from the authoritative closed-candle lifecycle/history, the result is `NO CANONICAL MHV/MLV OWNER` rather than inferring MHV from morphology alone;
- a new/opposite cycle that supersedes the relevant prior Extreme also breaks the old provenance chain; the old Extreme cannot be reused indefinitely to authorize unrelated later consolidations;
- this decision does **not yet decide** the minimum F2 Extreme maturity required for the provenance link. That remains a separate focused review.

### Evidence classification
This decision is **DIRECT SOURCE SEQUENCE + SOURCE-FAITHFUL PROJECT OWNER/PROVENANCE GUARD**.

Source support:
- Finale V05 OA-F-V05-006 explicitly teaches MHV after Extreme + TP Wajib;
- the accepted BBMA cycle also places MHV/MLV after the Extreme / TP phase rather than as a generic standalone consolidation setup.

The same-timeframe / same-owner-cycle provenance requirement is the project's deterministic state-management encoding of that source sequence and is not claimed as verbatim software wording from Oma Ally.

## User-approved decision 3 — normal TP-Wajib structural move must complete before MHV/MLV formation
The project adopts **NORMAL TP-WAJIB STRUCTURAL COMPLETION AS A MANDATORY PRECONDITION BEFORE CANONICAL MHV/MLV FORMATION MAY BEGIN**.

Accepted operational rule:
- after a valid prior Extreme exists, price must first reach the accepted normal TP-Wajib structural area for that Extreme before the lifecycle may advance into MHV/MLV formation;
- for a prior Extreme SELL, normal TP-Wajib completion is price reaching the opposite MA5/MA10 Low area under the accepted Extreme contract;
- for a prior Extreme BUY, normal TP-Wajib completion is price reaching the opposite MA5/MA10 High area;
- Mid BB remains farther/maximum context and does not replace the normal first TP-Wajib area as the canonical prerequisite;
- `TP-Wajib completed` is a **market-structure state**, not an execution/broker state: no actual EA order, filled position, or broker TP-close event is required to prove the structural sequence;
- a mere configured TP level, unfilled target, or assumption that price was “likely headed there” is insufficient; the authoritative closed-candle/price history must show the accepted target area was actually reached;
- the advanced-Extreme-without-normal-TP-Wajib exception remains `HOLD / UNCERTAIN` and cannot be used to bypass this canonical rule;
- this decision still does **not** decide whether the prior Extreme must be merely reversal-confirmed or fully standalone retest/entry-ready before it can serve as the MHV/MLV parent. That is intentionally separated into the next review.

### Evidence classification
This decision is **DIRECT SOURCE SEQUENCE + MINIMAL STRUCTURAL PROJECT MAPPING**.

Source support:
- Finale V05 OA-F-V05-006 explicitly teaches MHV after `Extreme + TP Wajib`;
- Finale V04/V05 define the normal Extreme TP-Wajib objective around the opposite MA5/MA10 area, with Mid BB as a farther/maximum possibility;
- the source describes a market sequence, not a requirement that a broker-side trade must have existed.

The software state `TP-WAJIB STRUCTURALLY COMPLETED` is therefore a deterministic project representation of the source-described market progression, not an order-management event.

## Rejected alternatives
- single-candle MHV/MLV detector as the complete source model;
- mandatory exact double/triple-top or bottom formula;
- mandatory H&S morphology;
- treating MHV as merely another name for Extreme reversal;
- keeping independent MHV and MLV detector families that can disagree for the same structure;
- treating prior Extreme as merely preferred rather than required for the canonical MHV/MLV lifecycle;
- allowing any generic loss-of-momentum/consolidation to become MHV without a provable prior Extreme owner-chain;
- allowing canonical MHV/MLV formation before the normal TP-Wajib structural area has been reached;
- treating Mid BB as the sole/universal TP-Wajib prerequisite;
- requiring a real broker order to have closed at TP before market structure may progress;
- using the unresolved advanced-Extreme/no-TP-Wajib exception to bypass the canonical normal-cycle rule.

## Remaining specification before code
The structural lifecycle, mandatory prior-Extreme provenance and mandatory TP-Wajib completion are locked, but deterministic sub-rules still need one-by-one review before M09 is patched:
- define the minimum F2 Extreme maturity required for the prior-Extreme provenance link;
- define what exact BBMA condition proves `LOSS OF PRIOR MOMENTUM` without inventing ATR/ADX/pip thresholds;
- define how the marked highest/lowest body reference is owned and frozen;
- define what constitutes the retest/active-setup interaction;
- define lifecycle supersession/void rules beyond the explicit outer-BB close;
- migrate/remove legacy duplicate detector semantics after the canonical contract is complete.

No EA code change is authorized by these decisions alone.
