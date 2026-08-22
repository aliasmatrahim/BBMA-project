# CORE-V2-F1 — MHV/MLV Canonical Lifecycle

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — LIFECYCLE + PARENT PROVENANCE + TP-WAJIB + PARENT MATURITY + LOSS-OF-MOMENTUM + TURNING-BODY FORMATION + IMMEDIATE BODY-FREEZE + RANGE-TOUCH RETEST + REM COMPONENT MATURITY USER APPROVED; SUPERSESSION DETAILS STILL PENDING**
Branch: `blueprint-dev`

## Decision 1 — MHV/MLV is one structural lifecycle
The project adopts **one canonical MHV/MLV lifecycle / owner-state model**, not independent one-candle detectors.

Canonical high-level lifecycle:

`PRIOR EXTREME / TP CONTEXT -> LOSS OF PRIOR MOMENTUM -> MHV/MLV FORMATION -> MARKED BODY/REFERENCE -> RETEST / ACTIVE SETUP -> VALID CONTINUATION OR VOID/SUPERSESSION`

Locked semantics:
- `MHV` and `MLV` are terminology aliases for the same loss-of-volume setup family unless stronger source evidence later distinguishes them;
- the setup may develop over multiple closed candles and therefore requires state/owner continuity;
- marked body/reference and retest belong to the same lifecycle;
- double/triple-top or bottom and H&S-like forms are morphology/examples, not mandatory universal formulas;
- source-valid close beyond the relevant outer BB voids MHV/MLV and returns authority to Momentum/CSM;
- MHV/MLV remains setup/context, not direct entry authority merely because the lifecycle is modeled explicitly;
- legacy `DetectMHV()`/MLV semantics must ultimately converge into one canonical owner-state result.

Classification: **DIRECT SOURCE STRUCTURAL CONCEPT + PROJECT STATE-MACHINE MAPPING**.

## Decision 2 — prior Extreme provenance is mandatory
A canonical MHV/MLV candidate requires a **prior source-valid Extreme in the same source timeframe / owner-cycle**.

Locked semantics:
- generic inside-BB consolidation, local double/triple morphology or loss of impulse is insufficient by itself;
- if no authoritative prior Extreme chain can be proved, resolve to `NO CANONICAL MHV/MLV OWNER`;
- a superseded/restarted cycle breaks the old provenance chain; an old Extreme cannot authorize unrelated later consolidations indefinitely.

Classification: **DIRECT SOURCE SEQUENCE + SOURCE-FAITHFUL PROJECT OWNER/PROVENANCE GUARD**.

## Decision 3 — normal TP-Wajib structural completion is mandatory before MHV formation
After the valid prior Extreme, price must actually reach the accepted normal TP-Wajib structural area before canonical MHV/MLV formation can begin.

Locked semantics:
- prior Extreme SELL -> opposite MA5/MA10 Low area;
- prior Extreme BUY -> opposite MA5/MA10 High area;
- Mid BB is farther/maximum context, not the canonical first TP prerequisite;
- TP-Wajib completion is a market-structure state, not broker/order status;
- no actual trade or broker TP-close is required;
- advanced Extreme without normal TP-Wajib remains `HOLD / UNCERTAIN` and cannot bypass this canonical rule.

Classification: **DIRECT SOURCE SEQUENCE + MINIMAL STRUCTURAL PROJECT MAPPING**.

## Decision 4 — minimum parent Extreme maturity is reversal-confirmed
The minimum F2 maturity for the prior-Extreme provenance link is **`REVERSAL-CONFIRMED EXTREME`**, together with Decision 3 TP-Wajib structural completion.

Canonical parent chain:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> TP-WAJIB STRUCTURALLY COMPLETED -> ELIGIBLE MHV/MLV PARENT CONTEXT`

Locked semantics:
- RAW Extreme with no reversal confirmation is insufficient;
- standalone `RETEST/ENTRY-READY` maturity is not required merely for downstream MHV/MLV provenance;
- no actual Extreme trade needs to have been executed;
- void/superseded Extreme cannot remain a parent.

Classification: **DIRECT SOURCE EXTREME-REVERSAL REQUIREMENT + SOURCE-INFERRED SEPARATION OF ENTRY MATURITY FROM MHV CYCLE PROVENANCE**.

## Decision 5 — loss of prior momentum is a structural failed-continuation state
After eligible parent context, `LOSS OF PRIOR MOMENTUM` means a **developing post-TP structure inside the relevant outer BB that fails to produce source-valid Momentum/CSM continuation**.

Locked semantics:
- one ordinary/non-Momentum candle is insufficient;
- absence of Momentum/CSM is necessary but not sufficient; a same-cycle structure must actually develop;
- `BB_FLAT`, ATR, ADX, fixed pip displacement, fixed body-size percentages and fixed 2/3-candle minimums are not canonical proof;
- if source-valid outer-BB close / Momentum/CSM appears before formation matures, pending MHV/MLV is void/superseded.

Classification: **DIRECT SOURCE LOSS-OF-MOMENTUM + OUTER-BB/MOMENTUM INVALIDATION PRINCIPLE, WITH SOURCE-INFERRED STRUCTURAL STATE MAPPING**.

## Decision 6 — most-extreme body + first closed move-away establishes formation
Concrete MHV/MLV formation is established by the **most-extreme candle-body reference during the loss-of-momentum phase followed by the first closed move away from that side**.

For lifecycle descending from prior Extreme SELL (bottom-side MHV/MLV):
- `BodyBottom = min(Open, Close)`;
- track lowest `BodyBottom` across the active loss-of-momentum phase;
- first later closed candle with `CurrentClose > PreviousClose` establishes `MHV/MLV FORMATION ESTABLISHED`.

For lifecycle descending from prior Extreme BUY (top-side MHV/MLV):
- `BodyTop = max(Open, Close)`;
- track highest `BodyTop` across the active loss-of-momentum phase;
- first later closed candle with `CurrentClose < PreviousClose` establishes `MHV/MLV FORMATION ESTABLISHED`.

Additional rules:
- move-away trigger candle is excluded from accumulated body-extreme reference;
- wick `High/Low` is not substituted for the marked body;
- no mandatory second touch, exact double/triple morphology, H&S, named candlestick pattern, eCSD/CSD, previous-high/low breakout or fixed candle count is required merely to establish initial formation;
- outer-BB/Momentum invalidation has priority.

Classification: **DIRECT SOURCE BODY-MARKING / RETEST CONCEPT + MINIMAL STRUCTURAL TURNING-POINT PROJECT MAPPING**.

## Decision 7 — marked body freezes immediately when formation is established
The project adopts **IMMEDIATE FREEZE OF THE MARKED HIGHEST/LOWEST BODY REFERENCE AT THE SAME CLOSED-CANDLE TRANSITION THAT ESTABLISHES MHV/MLV FORMATION**.

Locked operational rule:
- once Decision 6 first closed move-away establishes MHV/MLV formation, the accumulated body extreme from the completed formation segment becomes the **frozen marked-body reference**;
- prior Extreme SELL / bottom-side MHV: freeze the lowest `BodyBottom` accumulated through the candle immediately preceding the move-away trigger;
- prior Extreme BUY / top-side MHV: freeze the highest `BodyTop` accumulated through the candle immediately preceding the move-away trigger;
- all later candles are evaluated against that frozen reference and must not move it merely because price creates a later body extreme;
- the move-away trigger candle itself does not redefine the frozen reference;
- later price action that creates another body extreme must be classified by later lifecycle rules as retest, continuation, invalidation/supersession or a new formation/cycle; it must not silently drag the existing anchor;
- no fixed-N waiting period, eCSD/CSD prerequisite, wick substitution or moving-neckline/chasing behavior is added;
- source-valid outer-BB/Momentum invalidation remains higher priority and can void/supersede the lifecycle.

Canonical transition:

`LOSS OF MOMENTUM -> BODY EXTREME -> FIRST CLOSED MOVE AWAY -> MHV/MLV FORMATION ESTABLISHED + MARKED BODY FROZEN -> WAIT FOR RETEST / LATER LIFECYCLE EVENT`

Classification: **DIRECT SOURCE MARKED-BODY / RETEST CONCEPT + MINIMAL FIXED-REFERENCE PROJECT MAPPING**.

## Decision 8 — range/wick interaction with the frozen marked body completes MHV/MLV retest
The project adopts **FIRST VALID PRICE-RANGE INTERACTION WITH THE FROZEN MARKED BODY AS THE MINIMUM DETERMINISTIC RETEST-COMPLETION RULE**.

Locked operational rule:
- retest evaluation begins only after Decision 6 has established the MHV/MLV formation and Decision 7 has frozen its marked-body reference;
- for a bottom-side MHV/MLV descending from prior Extreme SELL, retest is completed when a later source-timeframe candle satisfies `Low <= FrozenMarkedBody`;
- for a top-side MHV/MLV descending from prior Extreme BUY, retest is completed when a later source-timeframe candle satisfies `High >= FrozenMarkedBody`;
- price-range/wick interaction is sufficient to prove that price has returned to the source-marked reference; the candle is evaluated on the project closed-candle processing clock, but no universal requirement is added for the candle body to close exactly at the marked line;
- no universal extra close-away confirmation, engulfing/pin-bar/named pattern, mandatory second/third touch, exact double/triple morphology, or eCSD/CSD prerequisite is added merely to complete the MHV/MLV retest;
- the formation-establishing move-away candle cannot simultaneously count as a later retest candle; retest requires subsequent price action after the frozen reference exists;
- the frozen reference remains unchanged during and after the retest;
- accepted source-valid outside-outer-BB close / Momentum/CSM invalidation has priority. If the same candle/structure satisfies the project invalidation contract, the lifecycle resolves to `VOID/SUPERSEDED`, not `RETEST COMPLETE`;
- `RETEST COMPLETE / ACTIVE MHV SETUP` is a setup/context maturity state only. It does **not** make MHV/MLV a standalone trade-entry authority.

Canonical transition:

`MHV/MLV FORMATION ESTABLISHED + FROZEN MARKED BODY -> LATER RANGE/WICK INTERACTION WITH FROZEN BODY -> RETEST COMPLETE / ACTIVE MHV SETUP`

Classification: **DIRECT SOURCE MARKED-BODY / RETEST CONCEPT + MINIMAL RANGE-INTERACTION PROJECT MAPPING**.

## Decision 9 — M15 MHV/MLV used inside REM requires formation-established maturity, not retest completion
The project adopts **`MHV/MLV FORMATION ESTABLISHED + FROZEN MARKED BODY` AS THE MINIMUM MATURITY REQUIRED WHEN M15 MHV/MLV SERVES AS THE MLV/MHV COMPONENT OF REM**.

Locked operational rule:
- exact REM signature remains `H4 Re-Entry + H1 Extreme + M15 MHV/MLV` under the authoritative PDF-derived contract;
- the M15 component is not valid while it is only an eligible parent context, a pending loss-of-momentum state, or an unfrozen provisional formation;
- once Decision 6 establishes the M15 MHV/MLV formation and Decision 7 freezes its marked body, the M15 component is structurally mature enough to satisfy the MHV/MLV leg of REM, provided it has not been voided/superseded;
- Decision 8 `RETEST COMPLETE / ACTIVE MHV SETUP` is a later maturity state and is **not mandatory merely for M15 MHV/MLV to serve as the REM component**;
- this preserves the separation between **component maturity** and later standalone/setup maturity, analogous to the already-approved F2 rule where an Extreme component may be usable before standalone Extreme entry-readiness;
- no eCSD/CSD, second retest, double/triple morphology, fixed waiting period, or broker execution event is added as an extra REM requirement;
- if the M15 MHV/MLV is `VOID/SUPERSEDED` under the canonical lifecycle before the REM decision is consumed, the M15 leg is invalid and REM must not treat that stale component as valid;
- this decision does not redefine H4 Re-Entry or H1 Extreme maturity; those remain governed by their own locked contracts.

Canonical REM component condition:

`H4 VALID RE + H1 REVERSAL-CONFIRMED EXTREME + M15 MHV/MLV FORMATION ESTABLISHED WITH FROZEN BODY -> REM COMPONENT SET COMPLETE`, subject to normal M14/M15/M16 validation and invalidation authority.

Classification: **DIRECT SOURCE REM SIGNATURE + SOURCE-INFERRED COMPONENT-MATURITY MAPPING**.

## Source support for Decisions 1–9
- primary PDF digest pages 2 and 7–8: MLV normally follows Extreme/TP phase, highest/lowest body is marked because price may retest, MLV may show double/triple morphology, and outside-BB close voids the setup;
- primary PDF digest pages 12–13: REM is the exact multi-timeframe family `H4 Re-Entry + H1 Extreme + M15 MLV/MHV`;
- Finale V05 OA-F-V05-006 to OA-F-V05-009: MHV follows Extreme + TP Wajib, represents loss of prior momentum, must remain inside relevant outer BB, uses marked body/line plus retest structure, and is a setup stage;
- Finale V05 OA-F-V05-017 and OA-F-V05-019 reinforce the higher/lower-timeframe setup-family relationship while leaving the exact REM signature governed by the PDF.

The exact software states, body-edge formulas, close-to-close turning predicates, immediate freeze transition, range-interaction retest predicates, and REM component-maturity threshold are project-level deterministic encodings of the source concepts and are not claimed as verbatim Oma Ally Boolean formulas.

## Rejected alternatives
- one-candle detector as the complete MHV/MLV model;
- generic consolidation without prior Extreme provenance;
- MHV formation before normal TP-Wajib completion;
- RAW Extreme as sufficient parent;
- requiring standalone Extreme retest/entry-ready state merely for MHV provenance;
- first non-Momentum candle as sufficient loss-of-momentum proof;
- `BB_FLAT`, ATR, ADX, fixed pip/body-size or fixed-N heuristics as canonical proof;
- first post-TP candle as marked body without a structural move-away;
- mandatory second touch/double/triple/H&S before initial formation;
- waiting for eCSD/CSD before recognizing formation;
- keeping the marked body moving after formation is established;
- wick High/Low as replacement for the source-described body reference;
- fixed 2/3-candle delay before freezing the reference;
- requiring candle-body close exactly at/across the frozen marked body to count as retest;
- requiring a named reversal candle or additional close-away confirmation after touch merely to complete the retest;
- requiring double/triple retest morphology or eCSD/CSD to mature the retest;
- allowing a merely pending loss-of-momentum state to satisfy the M15 MHV/MLV leg of REM;
- requiring M15 MHV/MLV `RETEST COMPLETE` merely to satisfy the REM component signature.

## Remaining specification before code
The lifecycle, parent provenance, TP-Wajib prerequisite, parent maturity, loss-of-momentum state, turning-body formation predicate, immediate frozen-reference policy, range-touch retest contract and REM component-maturity threshold are locked. Remaining one-by-one review before M09 patching:
- define lifecycle supersession/void rules beyond the explicit outer-BB/Momentum invalidation;
- migrate/remove legacy duplicate detector semantics after the canonical contract is complete.

No EA code change is authorized by these decisions alone.