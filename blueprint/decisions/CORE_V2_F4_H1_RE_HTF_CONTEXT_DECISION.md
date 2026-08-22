# CORE-V2-F4 — Higher-Timeframe Context for Standalone H1 Re-Entry

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED H4 PARENT + AUTHORITATIVE CYCLE-STATE ALIGNMENT + INHERITED DIRECTIONAL OWNER + eCSD AUTHORITY; OPPOSITE TRANSITION/FRESHNESS DETAILS STILL PENDING**
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

## Evidence classification
The source explicitly requires multi-timeframe reading and instructs that Re-Entry direction be checked against higher timeframes. The primary PDF also gives intraday H4/H1/M15 alignment guidance.

Finale strongly corroborates parent/child timeframe ownership and inherited cycle progression:
- V05 teaches that a lower-timeframe direction signal may actually be completing a higher-timeframe Re-Entry and therefore must not be interpreted atomically;
- V05 teaches higher-TF Re-Entry with lower-TF completion across chains including H4/H1/M15;
- V05 explicitly distinguishes early direction (eCSD), stronger direction (CSD), Re-Entry setup and later Momentum/continuation;
- V06 repeats the cycle `Extreme -> MHV -> direction -> Re-Entry -> Momentum/continuation` across timeframes.

Classification: **DIRECT SOURCE PRINCIPLE + SOURCE-INFERRED / STRONG HINT FOR H4 AS THE IMMEDIATE PARENT AND FOR OWNER/STATE-BASED ALIGNMENT/INHERITANCE**.

The source does not provide a single verbatim Boolean formula or software state-machine for every standalone H1 Re-Entry. Exact supersession/freshness details remain project specification.

## Rejected alternatives
- H1-only execution with no higher-timeframe context: rejected as inconsistent with the source's MTF requirement.
- universal D1 + H4 hard alignment for every H1 Re-Entry: not selected; this is stricter than the source clearly establishes for the H4/H1/M15 intraday chain.
- `H4 OR D1` alignment as a generic fallback: rejected as an unsupported engineering compromise.
- H4 EMA50-only alignment: rejected as an insufficient substitute for BBMA higher-timeframe context.
- current-H4-candle-only directional gating: rejected as too atomic for the source's cycle/state teaching.
- raw H4 Extreme-only or raw H4 MHV/MLV-only ownership: rejected because those stages do not by themselves establish authoritative direction.
- treating every H4 eCSD/CSD/Re-Entry/CSM occurrence as an unrelated independent owner: rejected in favor of inherited same-cycle directional ownership.
- requiring CSD/Re-Entry/CSM before a valid H4 eCSD may establish directional ownership: rejected as an unsupported extra hard filter.

## Remaining sub-specification
Before code is patched, define the remaining H4 authorization/transition details.

The next review must decide:
- how opposite H4 eCSD/CSD/CSM or cycle restart terminates or supersedes the old owner;
- how a neutral/transitional H4 state with **no active authoritative owner** affects H1 eligibility;
- owner freshness/supersession so stale H4 context cannot authorize a new H1 Re-Entry;
- whether an opposite early eCSD is enough to kill the old owner immediately or should create a transitional/no-owner state until stronger opposite confirmation appears.

No M12/M15 code patch is authorized until this H4 owner-state contract is fully resolved.
