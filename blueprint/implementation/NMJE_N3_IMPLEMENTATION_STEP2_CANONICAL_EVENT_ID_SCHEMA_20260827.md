# NMJE N3 Implementation Step 2 — Canonical Event Identity Schema

Date: 2026-08-27
Branch: `nmje-n3-hardening-dev`
Status: DESIGN LOCK / SOURCE CHANGE NOT YET APPLIED

## Purpose
Define deterministic owner/event identity required by N3 without changing BBMA strategy semantics.

## Core invariant
Identity is provenance only. It must never become a quality score, entry filter, confidence value, timeframe vote or substitute for canonical M08–M12 maturity rules.

## Canonical identity fields
For canonical owner events consumed by NMJE, identity is derived only from source-owned facts:

`Pair | OwnerKind | Timeframe | Direction | StructuralAnchorTime | OwnerEpoch`

Where:
- `Pair` = resolved EA symbol identity;
- `OwnerKind` = D1 owner / H4 owner / Extreme / MHV-MLV / Re-Entry;
- `Timeframe` = canonical owner timeframe;
- `Direction` = canonical structural direction where applicable;
- `StructuralAnchorTime` = immutable source candle that installed the owner/cycle;
- `OwnerEpoch` = deterministic monotonic cycle identity, not wall-clock processing time.

## Re-Entry identity
Recommended canonical anchor:
- Type 1: `StartCandleTime` from the structurally proven ranging/retrace owner installation;
- Type 2/3/4: `StartCandleTime` when the exact candidate family is installed;
- confirmation advances maturity but does not silently replace the owner identity.

Derived token example:
`RE|<pair>|<tf>|<dir>|<type>|<StartCandleTime>`

The token may be hashed for compact storage, but the un-hashed provenance fields remain authoritative.

## Extreme identity
Recommended canonical anchor:
- `RawCandleTime` identifies the Extreme cycle;
- `ConfirmationCandleTime` is maturity metadata, not a new Extreme identity;
- a genuinely new RAW Extreme after terminal state creates a new cycle identity.

Derived token example:
`EXT|<pair>|<tf>|<dir>|<RawCandleTime>`

## MHV/MLV identity
Recommended canonical anchor:
- frozen parent Extreme identity + MHV direction;
- `ConfirmationCandleTime` identifies formation maturity within that parent cycle;
- new reversal-confirmed parent Extreme creates a new MHV/MLV epoch.

Derived token example:
`MLV|<pair>|M15|<dir>|<ParentExtremeRawTime>|<ParentExtremeConfirmTime>`

## D1 strategic owner identity
D1 owner remains an atomic closed-D1 snapshot. N3 identity should include:
`D1OWN|<pair>|<owner-direction-or-transition>|<SourceCandleTime>`

TRANSITION and UNRESOLVED are states, not executable directions.

## H4 owner identity
H4 owner already has persistent source signal and source candle provenance. N3 identity should include:
`H4OWN|<pair>|<dir>|<SourceSignal>|<SourceCandleTime>`

Neutral H4 candles must preserve the same owner identity.

## Monotonicity rules
1. Confirmation/maturity advancement within one canonical owner does not create a new owner identity.
2. VOID/SUPERSEDED/EXPIRED terminal provenance cannot resurrect under the same identity.
3. A genuinely new canonical owner must receive a distinct identity.
4. Restart/replay over identical closed-candle history must reproduce the same identity.
5. NMJE may derive JourneyID from canonical identities but may not rewrite them.

## Candidate and decision freeze
At N3 integration:
- M15 freezes the exact NMJE JourneyID + canonical owner identities used by the selected candidate;
- M16 revalidates those frozen identities against current canonical owner states;
- identity mismatch/supersession is fail-closed for the pending new-entry decision;
- this does not imply automatic close of an already-live trade.

## Implementation order
1. Complete M09 single-writer refactor and regression.
2. Add non-strategy identity fields/helpers to canonical owner structures where necessary.
3. Populate identity only at owner installation/handover points.
4. Add N1/N2 diagnostic exposure first.
5. Prove restart/replay identity equivalence.
6. Freeze identity into N3 candidate/decision payload only after shadow evidence passes.

## Explicit prohibitions
- no score/confidence field;
- no random UUID;
- no current-tick/time-based identity;
- no identity derived from mutable price/MA values;
- no N3 promotion of CANDIDATE to CONFIRMED;
- no duplicate detection formulas inside M12N;
- no universal full-chain nesting requirement.
