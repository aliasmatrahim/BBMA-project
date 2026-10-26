# M15 Final Signal / Entry Authority Contract

## Status
P0 Step 6 architecture contract for Module 15, reconciled 2026-08-24 with the D1 major-trend strategic-owner decision.

The BBMA source hierarchy governs strategy semantics. `Oma ally BBMA - AL.pdf` remains the primary operational reference. The locked `ENTRY_MODE_CONTRACT.md` governs Entry Mode 1 and Entry Mode 2. D1 strategic-owner semantics are supplied by `M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`.

## Final-authority ownership
M15 is the single final **new-entry direction / entry-eligibility authority** for one pair on one closed-M15 processing cycle.

M15 does not detect Extreme, MHV/MLV, CSD/eCSD, CSM, Re-Entry or D1 major trend. It consumes only owner-produced snapshots/candidates:
- M11 D1 major-trend owner snapshot;
- M12 confirmed H1 Re-Entry snapshot;
- M14 validated REM/RRE/REE combination candidates.

Raw detector `Valid=true` is never sufficient to create an M15 execution candidate.

## D1 strategic-direction gate — canonical first eligibility layer
Before a structurally valid candidate may participate in final new-entry selection, it must pass the M11 D1 strategic-owner gate.

Accepted M11 states:
- `D1_OWNER_BUY_CONFIRMED`;
- `D1_OWNER_SELL_CONFIRMED`;
- `D1_TRANSITION`;
- `D1_OWNER_UNRESOLVED`.

Eligibility:
- confirmed BUY -> only BUY candidates survive;
- confirmed SELL -> only SELL candidates survive;
- transition -> no candidate survives for new entry;
- unresolved -> no candidate survives for new entry.

A previous/last-confirmed D1 direction retained for diagnostics during transition must not be used as current execution authority.

M15 must not derive D1 direction independently from price/MA50. It consumes the M11 result.

### Gate order
The canonical order inside M15 is:

`STRUCTURALLY VALID CANDIDATES -> D1 STRATEGIC DIRECTION FILTER -> ATOMIC SURVIVING-DIRECTION CHECK -> CANONICAL SAME-DIRECTION SELECTION`

This means the old conservative simultaneous BUY+SELL conflict rule applies **after** source-authorized D1 strategic filtering. D1 is not an invented tie-break; it is the higher-timeframe strategic authority established by the reconciled source contract.

If malformed data somehow leaves both BUY and SELL eligible after a single confirmed D1 direction has been applied, fail closed and create no trade decision.

## Entry Mode implementation
### EntryMode 1 — RE_ENTRY_ONLY
Eligible structural candidate type:
- `SIGNAL_RE_ENTRY` only.

The standalone candidate is the authoritative confirmed **H1 Re-Entry** snapshot from M12.

Final eligibility additionally requires:
1. source-valid confirmed H1 Re-Entry;
2. active compatible H4 structural/directional owner under F4;
3. confirmed same-direction D1 strategic owner under M11.

H4 alone is no longer sufficient after the Home Course/D1 reconciliation.

Candidate/unconfirmed/expired Re-Entry is not eligible.

### EntryMode 2 — ALL_VALIDATED_BBMA_ENTRIES
Structurally eligible candidate types:
- standalone H1 `SIGNAL_EXTREME` only from exact M08 `RETEST/ENTRY-READY` maturity;
- confirmed H1 `SIGNAL_RE_ENTRY`;
- validated `SIGNAL_REM`;
- validated `SIGNAL_RRE`;
- validated `SIGNAL_REE`.

All still require the same-direction confirmed D1 strategic owner before final new-entry authority. Standalone H1 Extreme also preserves the existing same-direction active H4 immediate-owner boundary.

M15 does not redetect Extreme. Its standalone Extreme candidate identity is the exact H1 M08 lifecycle: one `SIGNAL_EXTREME` component anchored to `RetestCompletionCandleTime`, with `SequenceStartTime = RawCandleTime`. RAW and reversal-only standalone Extreme remain non-executable. CSD, eCSD, CSM and MHV/MLV remain non-executable directly.

## REM / RRE / REE boundary
M15 must preserve exact source signatures produced/validated by M13/M14:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

D1 major trend is **not** inserted as a fourth REM component.

Instead, M15 applies it as a separate strategic-direction gate to the already validated candidate.

A D1 Re-Entry component inside RRE/REE is setup/component identity and does not replace M11 D1 MA50 owner confirmation.

## Atomic BUY / SELL rule
M27 must collect candidate snapshots first and M15 must make one pair-level final-authority decision per closed M15 processing cycle.

After D1 filtering:
- if no candidate survives -> no trade decision;
- if surviving candidates contain contradictory directions -> fail closed / no trade decision;
- if one direction survives -> canonicalize within that direction only.

This preserves at most one final new-entry decision path per pair per closed M15 cycle.

## No arbitrary BBMA tier ranking
M15 does not use `SignalMode`, SAFE/NORMAL/AGGRESSIVE labels or invented REM/RRE/REE superiority as strategy authority.

`SignalMode` remains compatibility/display only.

The D1 direction filter is not a quality score. It is the source-reconciled strategic-direction gate.

## Multiple candidates in the same direction
If several surviving candidates point in the same direction, M15 selects one canonical candidate for stable identity/hash using engineering bookkeeping only:
1. latest component candle anchor;
2. then latest `SequenceStartTime`;
3. then deterministic `SequenceHash` tie-break.

This must not be described as REM/RRE/REE quality superiority.

## Candidate freshness / expiry ownership
Candidates are rebuilt from current owner-valid snapshots every closed M15 cycle.

Freshness ownership remains:
- confirmed standalone Re-Entry carries explicit M12 owner validity/expiry;
- REM/RRE/REE are assemblies of owner-valid current components;
- no generic Comp1/M15 expiry is invented.

D1 strategic validity is a separate M11 snapshot and must be current for the same processing decision.

## D1 snapshot in decision payload
When M15 creates a decision, it must preserve enough frozen M11 identity for downstream M16 verification.

Required conceptual fields:
- D1 owner state;
- D1 owner direction;
- latest closed D1 candle time;
- D1 `Close1`;
- `MA50_1`;
- `MA50_2`;
- D1 owner validity/reason where represented.

Exact struct field names are implementation detail, but M16 must be able to verify that the decision passed the same M11 state rather than recomputing an independent formula.

## Decision payload
When one direction survives:
- `Direction` = surviving D1-compatible direction;
- `SignalType` = canonical validated candidate type;
- `SequenceHash` = canonical candidate hash;
- `CandleTime` = latest component candle anchor;
- `CycleStartTime` = candidate metadata start time;
- `PriorityTier = TIER_NONE`;
- D1 strategic-owner snapshot/identity = frozen into the decision for M16 verification.

M15 does not invent SL/TP, lot, risk or broker execution parameters.

## M27 orchestration consequence
Conceptual order becomes:
1. build frozen D1/H4/H1/M15 market data;
2. M11 classify D1 strategic owner from closed D1 + MA50 slope;
3. run signal/state owners for BUY/SELL;
4. build confirmed H1 Re-Entry and validated REM/RRE/REE candidates;
5. collect one pair-level candidate pool;
6. M15 apply D1 strategic gate + final atomic authority once;
7. M16 revalidate exact component/D1-owner identity;
8. only then proceed to M17/risk/execution.

M11 produces D1 strategy context; M15 remains final new-entry authority.

## D1 transition semantics
`D1_TRANSITION` and `D1_OWNER_UNRESOLVED` block **new entries only** at this contract boundary.

M15 must not reinterpret them as broker-close instructions for existing trades.

## Input validation
`EntryMode` is valid only when:
- `1 = RE_ENTRY_ONLY`; or
- `2 = ALL_VALIDATED_BBMA_ENTRIES`.

## Scope guard
M15 does not own:
- D1 MA50 calculation or owner-state production;
- H4 owner detection/recovery;
- Re-Entry/Extreme/MHV/CSM detection;
- REM/RRE/REE signature construction;
- SL/TP;
- lot/risk;
- position lifecycle / broker close.

## Current owner implementation status — reconciled 2026-10-26
The previous implementation-gap statement is superseded for static status by owner Build 5.15 at `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`.

- M15 consumes M11 D1 owner state and applies the D1 eligibility gate before final candidate selection.
- M15 remains the sole final new-entry authority; M27 calls its priority engine only after candidate assembly.
- M15 freezes the selected D1 owner identity for M16 revalidation.
- Exact REM/RRE/REE signatures remain unchanged.

Classification: **STATIC IMPLEMENTATION PRESENT / COMBINED REGRESSION PARTIAL / RUNTIME NOT VERIFIED**. No runtime compliance claim is made by this reconciliation.

## Implementation record — historical Step 6 baseline
Patch:
`blueprint/patches/0013-p0-step6-m15-final-authority-atomic-entry-mode.patch`

Patch commit:
`0a5c721337ecdedca606e15978a2f043e08717c4`

Focused patch SHA-256:
`9933e041a1999b865c18f340454536ae5371a777d2a6af5d28f2e0d561258b0e`

Do not merge to `main` until the current source/spec/runtime gates are reconciled and explicitly approved.

## D1-02 implementation record — `d1-owner-dev`
The 2026-08-24 D1 strategic gate is implemented on isolated `d1-owner-dev` as build `Version 4.5.1 - D1-02 M15-M16 Strategic Gate`.

- M15 consumes M11 owner state; it does not recalculate D1/MA50.
- Transition/unresolved/stale D1 blocks new-entry authority.
- Opposite-D1 candidates are filtered before the atomic surviving-direction check.
- Exact REM/RRE/REE signatures remain unchanged.
- Selected decisions freeze D1 owner state/direction/candle plus D1 close and MA50 identity for M16.
- Native MT4 MetaEditor: **0 errors / 0 warnings**.
- `blueprint-dev` remains unchanged pending explicit integration approval.

## D1-03 atomic snapshot ownership overlay
M15 continues the D1-02 gate order, but its frozen D1 identity now comes exclusively from the M11-owned `D1MajorTrendOwner` atomic snapshot (`state`, `direction`, closed-D1 candle, `Close1`, `MA50_1`, `MA50_2`). M15 no longer mixes raw `d1_data` fields with separate PairState MA mirrors when freezing a decision. Strategy semantics and candidate signatures are unchanged.
