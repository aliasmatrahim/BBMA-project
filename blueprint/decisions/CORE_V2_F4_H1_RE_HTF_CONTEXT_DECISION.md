# CORE-V2-F4 — Higher-Timeframe Context for Standalone H1 Re-Entry

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED H4 PARENT + AUTHORITATIVE CYCLE-STATE ALIGNMENT + INHERITED DIRECTIONAL OWNER + eCSD AUTHORITY + ATOMIC OPPOSITE OWNER HANDOVER + NO-OWNER BLOCK + STRUCTURAL OWNER LIFETIME; RESTART/RECOVERY RECONSTRUCTION STILL PENDING**
Branch: `blueprint-dev`

## User-approved decision 1 — immediate higher-timeframe owner
For a standalone executable H1 Re-Entry, the project adopts **H4 as the immediate higher-timeframe parent/context owner**.

Accepted principle:

`H4 BBMA CONTEXT -> H1 RE-ENTRY -> lower-TF completion/observation where applicable`

Operational meaning:
- a standalone H1 Re-Entry must not be treated as fully autonomous from higher-timeframe BBMA context;
- H4 is the immediate parent timeframe that must provide a compatible BBMA context for the H1 Re-Entry direction;
- D1 remains broader structural context and may be informative/important, but is **not** a universal mandatory hard gate for every standalone H1 Re-Entry;
- this decision does not redefine REM/RRE/REE signatures and does not convert standalone H1 Re-Entry into a three-timeframe combination setup;
- this decision does not authorize an EMA50-only, score-based, or generic trend filter as the H4 compatibility rule.

## User-approved decision 2 — H4 compatibility is an authoritative BBMA cycle/directional state
The project adopts **ACTIVE AUTHORITATIVE H4 BBMA DIRECTIONAL/CYCLE STATE** as the basis of H4 compatibility for a standalone H1 Re-Entry.

Accepted interpretation:
- H4 compatibility is not determined from one current H4 candle alone;
- H4 must have a source-valid BBMA state that has already established directional authority and remains current under its own owner/invalidation contract;
- a neutral candle occurring after a valid H4 directional state does not automatically erase that state if the H4 owner/cycle has not been invalidated or superseded;
- raw H4 `Extreme` alone is not sufficient as directional authority because Extreme is a signal/context stage and does not by itself establish completed reversal direction;
- raw H4 `MHV/MLV` alone is not sufficient as directional authority because MHV/MLV is a setup/loss-of-volume stage before direction is established;
- Mid-BB/MA50 position may remain supporting structural context but is not by itself the authoritative H4 owner.

Evidence classification: **SOURCE-INFERRED / STRONG HINT** built on direct source MTF principles and the source separation between Extreme/MHV setup stages, direction signals, Re-Entry and Momentum/continuation stages.

## User-approved decision 3 — inherited H4 directional cycle owner
The project adopts an **INHERITED DIRECTIONAL CYCLE OWNER** model for H4 rather than treating `eCSD`, `CSD`, `Re-Entry`, and `CSM/Momentum` as unrelated one-candle owners.

Accepted lifecycle:

`H4 DIRECTION SIGNAL -> H4 RE-ENTRY -> H4 CSM/MOMENTUM -> FURTHER SAME-CYCLE RE-ENTRY`

Operational meaning:
- a source-valid H4 direction signal establishes or advances directional ownership;
- later same-direction Re-Entry and CSM/Momentum states inherit and continue the same H4 directional/cycle owner rather than creating a disconnected owner on each candle;
- same-direction continuation does not require a new eCSD/CSD on every H4 candle to keep H4 context alive;
- one neutral H4 candle does not erase the inherited owner when the authoritative H4 cycle remains valid;
- raw Extreme and raw MHV/MLV remain pre-direction context and do not own H4 directional authority by themselves;
- multiple same-direction owner-capable states are interpreted as lifecycle progression/continuation, not a quality ranking between signal families;
- opposite or superseding H4 structural states must terminate or replace the old owner according to the final invalidation/transition contract.

Evidence classification: **SOURCE-INFERRED / STRONG HINT**. V05/V06 explicitly teach direction -> Re-Entry -> Momentum/continuation as one BBMA cycle progression, but do not provide a verbatim software-owner-state algorithm.

## User-approved decision 4 — valid H4 eCSD can establish directional ownership
The project adopts **VALID H4 eCSD IS SUFFICIENT TO ESTABLISH H4 DIRECTIONAL OWNER** for higher-timeframe compatibility with a same-direction standalone H1 Re-Entry.

Accepted interpretation:
- a source-valid H4 `eCSD` is already a directional signal under the accepted BBMA source contract;
- therefore a valid H4 eCSD may establish the H4 directional owner without waiting for a later H4 CSD/Re-Entry/CSM solely to satisfy parent alignment;
- later same-direction `CSD`, `Re-Entry`, and `CSM/Momentum` strengthen/advance/inherit the same owner rather than being mandatory prerequisites for ownership;
- H4 eCSD does **not** become entry authority by this decision; the executable trade still requires a source-valid standalone H1 Re-Entry under its own H1 contract;
- a raw H4 Extreme or MHV/MLV still cannot substitute for eCSD/CSD directional authority;
- do not add an EMA50/Mid-BB hard gate merely to "upgrade" eCSD unless separately source-supported.

Evidence classification: **DIRECT SOURCE FUNCTION + SOURCE-INFERRED OWNER APPLICATION**. The source explicitly treats eCSD as early directional information and CSD as stronger directional information, while the software owner role is the project's deterministic mapping of that source function.

## User-approved decision 5 — atomic opposite-direction owner handover
The project adopts **ATOMIC H4 OWNER HANDOVER** when a source-valid opposite H4 direction/momentum state appears.

Accepted transition:

`OLD H4 DIRECTIONAL OWNER -> VALID OPPOSITE eCSD/CSD/CSM -> OLD OWNER SUPERSEDED -> NEW OPPOSITE OWNER ACTIVE`

Operational meaning:
- a valid opposite H4 `eCSD` is sufficient to supersede the old H4 directional owner and establish the new opposite owner, consistent with decision 4 that valid eCSD can establish ownership;
- a valid opposite H4 `CSD` likewise supersedes the old owner and establishes/advances the new opposite owner;
- a valid opposite H4 `CSM/Momentum` likewise cannot coexist with the old opposite directional owner as if both remained authoritative;
- owner transfer is atomic at the closed-candle state transition: the old owner loses authority when the new source-valid opposite state becomes authoritative;
- the project does **not** keep simultaneous BUY and SELL H4 directional owners for standalone H1 alignment;
- the handover applies only to source-valid BBMA direction/momentum states, not to an ordinary opposite-colored candle, a raw MA touch, or generic price movement;
- an opposite raw Extreme or raw MHV/MLV alone still does not automatically establish a new directional owner because those stages are not directional authority by themselves;
- this owner-handover rule is a deterministic project mapping of source-defined directional states, not a verbatim source software instruction.

Evidence classification: **SOURCE-INFERRED / STRONG HINT + INTERNAL CONSISTENCY WITH THE USER-APPROVED eCSD OWNER RULE**. The source explicitly treats eCSD/CSD as direction information and CSM/Momentum as continuation/directional movement, but does not publish an owner-state handover algorithm.

## User-approved decision 6 — neutral candle versus true no-owner H4 state
The project adopts **NEUTRAL-CANDLE PRESERVATION + TRUE NO-OWNER EXECUTION BLOCK**.

Accepted distinction:

`NEUTRAL H4 CANDLE + VALID INHERITED OWNER -> OWNER REMAINS AUTHORITATIVE`

but

`TRUE H4 NO-OWNER STATE -> STANDALONE H1 RE-ENTRY NOT EXECUTABLE`

Operational meaning:
- an ordinary neutral/transitional H4 candle does not erase an already-valid inherited H4 directional owner when that owner has not been invalidated or superseded;
- if H4 genuinely has **no active authoritative directional owner**, a standalone H1 Re-Entry must not be authorized merely because its own H1 pattern is valid;
- `NO OWNER` includes startup/recovery before any valid owner is reconstructed, a prior owner that has been explicitly invalidated/superseded without a replacement, or a structural transition where no source-valid eCSD/CSD/CSM/current inherited directional owner exists yet;
- do not fall back to D1 as an `OR` substitute when H4 has no owner;
- do not invent temporary direction from H4 Mid-BB/MA50 position, candle color, generic price position, or absence of an opposite signal;
- the H1 detector may still observe/build its setup while H4 is no-owner, but final standalone H1 execution eligibility remains blocked until a compatible H4 owner exists.

Evidence classification: **DIRECT MTF PRINCIPLE + SOURCE-INFERRED NO-OWNER EXECUTION GUARD**. The source requires higher-timeframe context/alignment but does not publish a verbatim software `NO_OWNER` state rule.

## User-approved decision 7 — structural H4 owner lifetime / freshness
The project adopts **PURE STRUCTURAL H4 OWNER LIFETIME WITH NO GENERIC FIXED EXPIRY**.

Accepted rule:
- an authoritative H4 directional owner remains current while the same BBMA cycle/structure remains valid under the accepted owner, inheritance and supersession rules;
- owner age by itself does not invalidate H4 context;
- there is no generic 3/5/10-H4-candle expiry, 24-hour expiry, daily reset, session reset, or periodic requirement for a fresh eCSD/CSD merely because time has passed;
- owner lifetime ends through structural invalidation/supersession, including a source-valid opposite owner handover or another authoritative BBMA cycle/state transition that ends the old owner;
- a neutral H4 candle may occur during the owner's lifetime without expiring it;
- candle/bar age may be recorded for observability, audit and recovery diagnostics, but must not become a BBMA eligibility filter;
- the project does not add an engineering-only stale timeout at this stage because no source-derived threshold exists and such a timeout would be arbitrary.

Evidence classification: **SOURCE-INFERRED / STRONG HINT + SOURCE-FAITHFUL ABSENCE OF NUMERIC EXPIRY RULE**. The source teaches BBMA as a structural cycle/state progression and provides no universal expiration count for higher-timeframe directional context.

## Evidence classification
The source explicitly requires multi-timeframe reading and instructs that Re-Entry direction be checked against higher timeframes. The primary PDF also gives intraday H4/H1/M15 alignment guidance.

Finale strongly corroborates parent/child timeframe ownership and inherited cycle progression:
- V05 teaches that a lower-timeframe direction signal may actually be completing a higher-timeframe Re-Entry and therefore must not be interpreted atomically;
- V05 teaches higher-TF Re-Entry with lower-TF completion across chains including H4/H1/M15;
- V05 explicitly distinguishes early direction (eCSD), stronger direction (CSD), Re-Entry setup and later Momentum/continuation;
- V06 repeats the cycle `Extreme -> MHV -> direction -> Re-Entry -> Momentum/continuation` across timeframes.

Classification: **DIRECT SOURCE PRINCIPLE + SOURCE-INFERRED / STRONG HINT FOR H4 AS THE IMMEDIATE PARENT AND FOR OWNER/STATE-BASED ALIGNMENT/INHERITANCE/HANDOVER/LIFETIME**.

The source does not provide a single verbatim Boolean formula or software state-machine for every standalone H1 Re-Entry. Restart/recovery reconstruction remains a project implementation specification.

## Rejected alternatives
- H1-only execution with no higher-timeframe context: rejected as inconsistent with the source's MTF requirement.
- universal D1 + H4 hard alignment for every H1 Re-Entry: not selected; this is stricter than the source clearly establishes for the H4/H1/M15 intraday chain.
- `H4 OR D1` alignment as a generic fallback: rejected as an unsupported engineering compromise.
- H4 EMA50-only alignment: rejected as an insufficient substitute for BBMA higher-timeframe context.
- current-H4-candle-only directional gating: rejected as too atomic for the source's cycle/state teaching.
- raw H4 Extreme-only or raw H4 MHV/MLV-only ownership: rejected because those stages do not by themselves establish authoritative direction.
- treating every H4 eCSD/CSD/Re-Entry/CSM occurrence as an unrelated independent owner: rejected in favor of inherited same-cycle directional ownership.
- requiring CSD/Re-Entry/CSM before a valid H4 eCSD may establish directional ownership: rejected as an unsupported extra hard filter.
- keeping the old H4 owner alive after a valid opposite eCSD while waiting for stronger confirmation: rejected as inconsistent with the accepted rule that valid eCSD itself can establish directional ownership.
- allowing simultaneous authoritative H4 BUY and SELL owners: rejected.
- allowing standalone H1 execution when H4 has no active authoritative owner: rejected because it defeats the accepted higher-timeframe context requirement.
- using D1, Mid-BB/MA50 or absence-of-opposite as a silent fallback owner when H4 is no-owner: rejected.
- fixed H4 owner expiry by candle count, clock time, day or session: rejected as unsupported.
- periodic forced refresh of eCSD/CSD solely due to owner age: rejected.

## Remaining sub-specification
Before code is patched, define **restart/recovery reconstruction** of the H4 owner.

The next review must decide:
- whether recovery should rebuild owner state by replaying closed H4 BBMA history until the latest authoritative owner/supersession state is deterministically reconstructed;
- whether recovery may trust persisted owner state without replay;
- what to do when available history is insufficient to prove the owner chain;
- how to avoid inventing direction from incomplete state after restart.

No M12/M15 code patch is authorized until restart/recovery reconstruction is resolved.
