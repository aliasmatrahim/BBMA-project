# M14 BBMA Combination Validation Contract

## Status
P0 Step 5 source-alignment contract for Module 14.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference.

## Source basis
Primary reference pages 12–13 define REM, RRE and REE as three-component BBMA setups across three different timeframes. For the project's fixed D1/H4/H1/M15 universe, the source-supported rows are:
- REM = H4 Re-Entry + H1 Extreme + M15 MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M13 assembles only those source-locked rows. M14 validates them; it does not detect or mutate any strategy state.

## Removed invalid legacy validators
The previous M14 validated unrelated signatures:
- `Extreme -> MLV/MHV -> CSD` as `SIGNAL_REVERSAL`;
- `CSD -> Re-Entry -> REM` as `SIGNAL_CONTINUATION`;
- `REE/RRE -> CSD -> Re-Entry` as `SIGNAL_MAJOR_REVERSAL`.

Those signatures did not validate the REM/RRE/REE sets produced by M13 and are removed from the active combination path.

## Exact signature validation
A candidate is valid only when:
- `ComponentCount == 3`;
- all three components have non-zero type, direction, timeframe and candle time;
- all three directions match;
- `CombinationType` is REM, RRE or REE;
- component types and timeframes match the exact source-locked project row for that combination.

No alternative type substitution or timeframe substitution is accepted.

## No artificial chronology
The old universal rule:
`Comp1.CandleTime < Comp2.CandleTime < Comp3.CandleTime`
is removed.

The source describes REM/RRE/REE as three setups forming across three different timeframes, including wording that they form at the same time. That does not support a universal chronological ordering between D1, H4, H1 and M15 component candle times.

M13 supplies components that coexist as valid owner snapshots during the current M15 processing cycle. M14 validates identity/signature/direction only. Freshness, owner expiry and final candidate eligibility remain downstream responsibilities.

## Candidate payload integrity
M14 now copies the validated set into:
- `candidate.Components[0] = set.Comp1`;
- `candidate.Components[1] = set.Comp2`;
- `candidate.Components[2] = set.Comp3`.

This repairs the previous architecture bug where M15 consumed `candidate.Components[]` even though M14 never populated it.

`candidate.SequenceType` is the actual BBMA combination type: `SIGNAL_REM`, `SIGNAL_RRE`, or `SIGNAL_REE`.

## Validate-only ownership guard
M14 does not assign strategy rules not present in the supplied source.

Therefore:
- `SLTPSource = SIGNAL_NONE` remains unresolved for downstream SL/TP ownership;
- `PriorityTier = TIER_NONE` remains unresolved for M15 priority policy;
- M14 does not select an entry, direction winner, SL/TP, lot, risk or execution action.

This intentionally prevents M14 from inventing a ranking such as REM > RRE > REE or any SL/TP source rule that is not stated in the PDF.

## Temporal / expiry guard
Step 5 removes the invalid strict chronology but does not certify the current M27/M15 generic expiry formula as BBMA-correct. Candidate freshness must ultimately respect the active owner-state validity of the underlying Re-Entry/MLV/Extreme components rather than deriving all expiry from `Comp1` with a generic M15 multiplier.

That remains a downstream M15/M16 integration item.

## Implementation record
Patch:
`blueprint/patches/0012-p0-step5-m14-combination-validation.patch`

Patch commit:
`0fe0713907e1ba81068911a65449a2d967d21963`

Local patch SHA-256:
`0b5addc3c6334a6ef5cccc65977ef72df26ea1d94df1f3901b48c915d7b87252`

## Verification
Focused post-Step4 verification:
- patch dry-run: clean;
- patch apply: clean;
- braces balanced: 488 / 488;
- parentheses balanced: 1457 / 1457;
- brackets balanced: 342 / 342;
- legacy strict chronology validator absent;
- legacy reversal/continuation/major-reversal validators absent from the M13 combination path;
- REM/RRE/REE exact signature checks present;
- `candidate.Components[0..2]` populated;
- M14 assigns neither priority tier nor SL/TP source.

The complete 0001-through-current patch chain has not yet been rematerialized exactly in one source file, so no new full-working-source SHA is claimed by Step 5.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
