# CORE-V2-F1 — MHV/MLV Canonical Lifecycle

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — DECISIONS 1–11 USER APPROVED; FINAL SAME-CYCLE PROVENANCE TERMINATION/SUPERSESSION EVENT STILL PENDING**
Branch: `blueprint-dev`

## Decision 1 — MHV/MLV is one structural lifecycle
The project adopts **one canonical MHV/MLV lifecycle / owner-state model**, not independent one-candle detectors.

Canonical high-level lifecycle:

`PRIOR EXTREME / TP CONTEXT -> LOSS OF PRIOR MOMENTUM -> MHV/MLV FORMATION -> MARKED BODY/REFERENCE -> RETEST / ACTIVE SETUP -> DIRECTION / CONTINUATION OR VOID/SUPERSESSION`

Locked semantics:
- `MHV` and `MLV` are terminology aliases for the same loss-of-volume setup family unless stronger source evidence later distinguishes them;
- setup may develop across multiple closed candles and requires state/owner continuity;
- marked body/reference and later retest belong to the same lifecycle;
- double/triple top/bottom and H&S-like shapes are permitted morphology/examples, not mandatory formulas;
- MHV/MLV remains setup/context and is not direct entry authority;
- legacy duplicate `DetectMHV()`/MLV semantics must ultimately converge into one canonical owner-state result.

Classification: **DIRECT SOURCE STRUCTURAL CONCEPT + PROJECT STATE-MACHINE MAPPING**.

## Decision 2 — prior Extreme provenance is mandatory
A canonical MHV/MLV candidate requires a **prior source-valid Extreme in the same source timeframe / owner-cycle**.

Locked semantics:
- generic inside-BB consolidation, local morphology or loss of impulse is insufficient by itself;
- if no authoritative prior Extreme chain can be proved, resolve to `NO CANONICAL MHV/MLV OWNER`;
- a superseded/restarted cycle breaks the old provenance chain; an old Extreme cannot authorize unrelated later consolidations indefinitely.

Classification: **DIRECT SOURCE SEQUENCE + SOURCE-FAITHFUL PROJECT OWNER/PROVENANCE GUARD**.

## Decision 3 — normal TP-Wajib structural completion is mandatory before MHV formation
After the valid prior Extreme, price must actually reach the accepted normal TP-Wajib structural area before canonical MHV/MLV formation can begin.

Locked semantics:
- prior Extreme SELL -> opposite MA5/MA10 Low area;
- prior Extreme BUY -> opposite MA5/MA10 High area;
- Mid BB is farther/maximum context, not the canonical first TP prerequisite;
- TP-Wajib completion is market-structure evidence, not broker/order status;
- advanced Extreme without normal TP-Wajib remains `HOLD / UNCERTAIN` and cannot bypass this canonical rule.

Classification: **DIRECT SOURCE SEQUENCE + MINIMAL STRUCTURAL PROJECT MAPPING**.

## Decision 4 — minimum parent Extreme maturity is reversal-confirmed
Minimum parent maturity is **`REVERSAL-CONFIRMED EXTREME`**, together with Decision 3 TP-Wajib completion.

Canonical parent chain:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> TP-WAJIB STRUCTURALLY COMPLETED -> ELIGIBLE MHV/MLV PARENT CONTEXT`

Locked semantics:
- RAW Extreme alone is insufficient;
- standalone `RETEST/ENTRY-READY` maturity is not required merely for downstream MHV provenance;
- no actual Extreme trade must exist;
- void/superseded Extreme cannot remain a parent.

Classification: **DIRECT SOURCE EXTREME-REVERSAL REQUIREMENT + SOURCE-INFERRED ENTRY-MATURITY-vs-CYCLE-PROVENANCE SEPARATION**.

## Decision 5 — loss of prior momentum is a structural failed-continuation state
After eligible parent context, `LOSS OF PRIOR MOMENTUM` means a **developing post-TP structure inside the relevant outer BB that fails to produce source-valid Momentum/CSM continuation**.

Locked semantics:
- one ordinary/non-Momentum candle is insufficient;
- absence of Momentum/CSM is necessary but not sufficient; a same-cycle structure must actually develop;
- `BB_FLAT`, ATR, ADX, fixed pip/body-size thresholds and fixed 2/3-candle minimums are not canonical proof;
- if source-valid outer-BB close / Momentum/CSM appears while MHV formation is pending under its valid invalidation window, the pending interpretation is void/superseded.

Classification: **DIRECT SOURCE LOSS-OF-MOMENTUM + OUTER-BB/MOMENTUM INVALIDATION PRINCIPLE, WITH SOURCE-INFERRED STRUCTURAL STATE MAPPING**.

## Decision 6 — most-extreme body + first closed move-away establishes formation
Concrete MHV/MLV formation is established by the **most-extreme candle-body reference during the active loss-of-momentum phase followed by the first closed move away from that side**.

Prior Extreme SELL / bottom-side MHV:
- `BodyBottom = min(Open, Close)`;
- track lowest `BodyBottom`;
- first later closed candle with `CurrentClose > PreviousClose` establishes formation.

Prior Extreme BUY / top-side MHV:
- `BodyTop = max(Open, Close)`;
- track highest `BodyTop`;
- first later closed candle with `CurrentClose < PreviousClose` establishes formation.

Additional rules:
- move-away trigger candle is excluded from accumulated body-extreme reference;
- wick `High/Low` is not substituted for the marked body;
- no mandatory second touch, exact double/triple morphology, H&S, named pattern, eCSD/CSD, breakout or fixed candle count is required merely to establish initial formation.

Classification: **DIRECT SOURCE BODY-MARKING / RETEST CONCEPT + MINIMAL STRUCTURAL TURNING-POINT PROJECT MAPPING**.

## Decision 7 — marked body freezes immediately when formation is established
The project adopts **immediate freeze of the marked highest/lowest body reference at the same closed-candle transition that establishes formation**.

Locked semantics:
- bottom-side MHV freezes the lowest `BodyBottom` accumulated through the candle immediately before the move-away trigger;
- top-side MHV freezes the highest `BodyTop` accumulated through the candle immediately before the move-away trigger;
- later candles must not drag or recalculate the anchor;
- later price action creating another extreme must be classified by later lifecycle rules as retest, continuation, invalidation/supersession or new formation/cycle;
- no fixed-N delay, eCSD/CSD prerequisite, wick substitution or moving-neckline behavior is added.

Canonical transition:

`LOSS OF MOMENTUM -> BODY EXTREME -> FIRST CLOSED MOVE AWAY -> FORMATION ESTABLISHED + MARKED BODY FROZEN`

Classification: **DIRECT SOURCE MARKED-BODY / RETEST CONCEPT + MINIMAL FIXED-REFERENCE PROJECT MAPPING**.

## Decision 8 — range/wick interaction with frozen marked body completes retest
The project adopts **first valid price-range interaction with the frozen marked body as the minimum deterministic retest-completion rule**.

Locked semantics:
- bottom-side MHV retest: later candle `Low <= FrozenMarkedBody`;
- top-side MHV retest: later candle `High >= FrozenMarkedBody`;
- range/wick interaction is sufficient; no universal body-close-at-line rule is added;
- no extra close-away confirmation, named pattern, mandatory second/third touch, exact double/triple morphology or eCSD/CSD prerequisite is added merely to complete retest;
- formation-establishing move-away candle cannot simultaneously count as the later retest candle;
- frozen reference remains unchanged during/after retest;
- applicable invalidation has priority if the same candle/structure triggers it;
- `RETEST COMPLETE / ACTIVE MHV SETUP` remains setup/context maturity only, not standalone entry authority.

Classification: **DIRECT SOURCE MARKED-BODY / RETEST CONCEPT + MINIMAL RANGE-INTERACTION PROJECT MAPPING**.

## Decision 9 — M15 MHV/MLV inside REM requires formation-established maturity, not retest completion
Minimum M15 maturity for the MHV/MLV leg of REM is:

`MHV/MLV FORMATION ESTABLISHED + FROZEN MARKED BODY`

Locked semantics:
- exact REM signature remains `H4 Re-Entry + H1 Extreme + M15 MHV/MLV`;
- eligible parent context, pending loss-of-momentum or unfrozen provisional formation is insufficient;
- later `RETEST COMPLETE` is not mandatory merely to satisfy REM component maturity;
- no eCSD/CSD, second retest, double/triple morphology, fixed wait or broker event is added;
- a void/superseded M15 MHV/MLV cannot satisfy REM;
- H4 Re-Entry and H1 Extreme maturity remain governed by their own contracts.

Canonical component condition:

`H4 VALID RE + H1 REVERSAL-CONFIRMED EXTREME + M15 MHV/MLV FORMATION ESTABLISHED WITH FROZEN BODY -> REM COMPONENT SET COMPLETE`, subject to normal downstream validation/invalidation authority.

Classification: **DIRECT SOURCE REM SIGNATURE + SOURCE-INFERRED COMPONENT-MATURITY MAPPING**.

## Decision 10 — same-cycle eCSD/CSD advances the cycle; it does not retroactively void completed MHV/MLV
The project adopts **same-cycle direction progression without retroactive MHV/MLV invalidation**.

Locked semantics:
- source-valid same-cycle `eCSD` or `CSD` is the normal next direction stage after valid MHV/MLV;
- appearance of eCSD/CSD does not turn completed MHV/MLV into `VOID`;
- distinguish **current active stage ownership** from **completed structural provenance**: direction may become active while completed MHV/MLV remains immutable same-cycle history;
- frozen marked body stays frozen;
- no fixed candle/session/day expiry or generic "new signal erases old setup" rule is added.

Canonical progression:

`MHV/MLV FORMATION / RETEST -> SAME-CYCLE eCSD/CSD -> DIRECTION STAGE ACTIVE`, with completed MHV/MLV retained as same-cycle provenance until a separately approved structural supersession event occurs.

Classification: **DIRECT SOURCE CYCLE ORDER + SOURCE-INFERRED STATE-PROGRESSION / ACTIVE-STAGE-vs-PROVENANCE MAPPING**.

## Decision 11 — outer-BB/Momentum invalidation window closes when valid same-cycle direction stage takes ownership
The project adopts **STAGE-BOUNDED MHV/MLV INVALIDATION**.

Locked operational rule:
- source-valid outside-outer-BB close / Momentum/CSM can void the MHV/MLV while MHV is still the pending/current authoritative stage, including formation and retest/active-setup processing before valid same-cycle direction ownership has taken over;
- if a candle simultaneously satisfies an MHV promotion/retest event and the applicable source-valid Momentum/outer-BB invalidation contract, invalidation has priority;
- once a valid same-cycle `eCSD` or `CSD` has structurally taken ownership as the direction stage, the active MHV invalidation window closes;
- later same-cycle Re-Entry and CSM/Momentum are normal cycle progression and must **not retroactively convert the completed MHV/MLV provenance into `VOID`**;
- after direction-stage takeover, MHV/MLV is historical same-cycle provenance rather than the current active setup stage; its frozen marked body remains immutable historical/reference data until the separately defined cycle-supersession event terminates that provenance;
- no fixed-N expiry, session/day reset or "first later Momentum erases MHV" rule is introduced;
- this decision governs the **invalidation window only**. The exact new-cycle event that finally terminates/supersedes historical MHV provenance remains pending Review 5L.

Canonical stage boundary:

`MHV PENDING / FORMATION / ACTIVE MHV STAGE -> [OUTER-BB / SOURCE-VALID MOMENTUM] -> VOID`

but

`VALID MHV -> SAME-CYCLE eCSD/CSD TAKES DIRECTION OWNERSHIP -> MHV ACTIVE INVALIDATION WINDOW CLOSED -> RE-ENTRY / SAME-CYCLE CSM-MOMENTUM DOES NOT RETROACTIVELY VOID MHV PROVENANCE`

Classification: **DIRECT SOURCE MHV INVALIDATION + CYCLE-PROGRESSION PRINCIPLE, WITH SOURCE-INFERRED INVALIDATION-WINDOW MAPPING**.

## Source support for Decisions 1–11
- primary PDF digest page 2: cycle proceeds `Extreme -> TP -> MLV/MHV -> eCSD/CSD -> Re-Entry -> CSM/Momentum -> later opposite Extreme/cycle restart`;
- primary PDF digest pages 5–6: Extreme requires reversal behaviour and an isolated Extreme does not by itself prove a trend reversal;
- primary PDF digest pages 7–8: MLV normally forms after Extreme, uses highest/lowest body marking for possible retest, and is void when price breaks/closes outside the relevant outer BB during MLV context;
- primary PDF digest pages 12–13: exact REM signature is `H4 Re-Entry + H1 Extreme + M15 MLV/MHV`;
- Finale V05 OA-F-V05-006 to 009: MHV follows Extreme + TP Wajib, represents loss of prior momentum, must remain inside relevant outer BB, and uses marked body/retest structure;
- Finale V05 OA-F-V05-010 to 016: eCSD/CSD provide subsequent direction, followed by Re-Entry and continuation; direction is a signal rather than direct entry;
- Finale V05 OA-F-V05-017/019 corroborate the multi-timeframe family relationship while the PDF governs exact REM signatures.

The exact software states, body-edge formulas, close-to-close turning predicates, fixed-anchor rule, range-interaction retest predicate, REM component-maturity threshold, active-stage/provenance bookkeeping, and invalidation-window boundary are project-level deterministic mappings and are not claimed as verbatim Oma Ally Boolean formulas.

## Rejected alternatives
- one-candle detector as the complete MHV/MLV model;
- generic consolidation without prior Extreme provenance;
- MHV before normal TP-Wajib completion;
- RAW Extreme as sufficient MHV parent;
- requiring standalone Extreme entry-ready state merely for MHV provenance;
- first non-Momentum candle as sufficient MHV proof;
- ATR/ADX/BB_FLAT/fixed-pip/body-size/fixed-N heuristics as canonical MHV proof;
- mandatory exact double/triple/H&S morphology;
- waiting for eCSD/CSD before initial MHV formation;
- moving the marked body after formation;
- wick High/Low as replacement for source body reference;
- mandatory extra close-away/named-pattern/double-touch confirmation for retest;
- pending loss-of-momentum as sufficient M15 REM component;
- mandatory MHV retest completion merely for REM component maturity;
- same-cycle eCSD/CSD as retroactive MHV invalidation;
- allowing later same-cycle Re-Entry/CSM/Momentum to retroactively erase a completed MHV after direction-stage takeover;
- generic fixed candle/session/day expiry.

## Remaining specification before code
Decisions 1–11 are locked. One Core semantic decision remains before F1 specification closure:
- define the structural **new-cycle event that finally terminates/supersedes completed same-cycle MHV/MLV provenance** (Review 5L).

After that:
- reconcile `MASTER_QUEUE.md` and Strategy Core Source of Truth V2;
- migrate/remove legacy duplicate detector semantics;
- patch/audit M09 only after the complete canonical contract is closed.

No EA code change is authorized by these decisions alone.