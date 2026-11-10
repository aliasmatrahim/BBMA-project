# M10 BBMA Direction / Momentum Source Contract

## Active direction decision — 2026-11-10

`../decisions/M10_DIRECTION_CLOSE_ONLY_USER_DECISION_20261110.md` supersedes the historical open-to-close body-span interpretation below. Direction admission uses valid closed price beyond the relevant MA pair, MidBB or both; Open is not a criterion. Implementation is pending: Build6.06 still uses the old body predicates. This is an explicit user semantic decision, not a newly authenticated founder quote. Do not reopen the Open ambiguity or remove unrelated Extreme/MHV body-anchor calculations. MOM and raw-signal/no-direct-entry authority remain unchanged.

The sections below preserve historical Step3E provenance; their Open/body-span details are not the active target. Follow the linked decision and current task queue for pending implementation/verification.

## Historical status
P0 Step 3E source-alignment contract for Module 10.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference; `BBMA technique.pdf` is secondary corroboration.

## Source-derived signal roles
The primary reference classifies CSM, eCSD and CSD as BBMA **signals**, not standalone execution authority.

Primary reference page 8 states:
- eCSD = candlestick that crosses MA5/10;
- CSD = candlestick that crosses MA5/10 and MID BB;
- CSD shows real intent of price direction by crossing MID BB;
- retracement often follows CSD/eCSD and the later MA5/10 retracement is where Re-Entry context appears.

Therefore M10 detects signal mechanics only. It does not turn CSM/eCSD/CSD directly into trades.

## eCSD contract
Source rule:
- eCSD crosses MA5/10.

Operational directional mapping retained for deterministic implementation:
- BUY eCSD crosses the MA5 High and MA10 High pair upward.
- SELL eCSD crosses the MA5 Low and MA10 Low pair downward.

The supplied text says `MA5/10` but does not explicitly spell out which High/Low pair is used for each direction. The mapping above is therefore an implementation interpretation consistent with the directional MA arrangement already used throughout the BBMA project; it must not be quoted as verbatim PDF wording.

## CSD contract
Source rule:
- CSD crosses MA5/10 **and MID BB**;
- the MID BB cross distinguishes the stronger direction signal and shows real price intent.

Operational mapping:
- BUY CSD crosses MA5 High, MA10 High and MID BB upward.
- SELL CSD crosses MA5 Low, MA10 Low and MID BB downward.

## Deterministic meaning of `crosses`
The PDF uses the word `crosses` but does not provide a wick-vs-body coding formula.

Step 3E encodes crossing as the **closed candle body spanning the required line from open to close**:
- BUY: `open <= level && close > level`.
- SELL: `open >= level && close < level`.

Wick-only touches do not count as a cross.

This is an explicit engineering interpretation required for deterministic EA behaviour, not a claimed verbatim Oma Ally rule.

## CSM contract
Primary reference pages 2 and 5 describe CSM as momentum candle(s) created while price travels in its intended direction after a short retracement, continuing until momentum diminishes.

Secondary reference page 18 provides the missing operational momentum law:
- candlestick close outside TOP BB while BB is vertical marks upward momentum;
- candlestick close outside LOW BB while BB is declining/vertical marks downward momentum.

The same secondary reference explains that expanding BB reflects strengthening momentum, while page 19 distinguishes horizontal-BB outer closes as reversal context rather than directional momentum.

Therefore Step 3E rejects the old CSM implementation based on:
- exactly three same-colour candles; and
- each body being greater than 70% of the three-candle average body.

Those conditions are not supported by the supplied BBMA sources.

### Deterministic CSM encoding
A source-valid CSM requires:
- BUY: closed candle `close > TOP_BB`;
- SELL: closed candle `close < LOW_BB`;
- current BB width greater than previous closed-candle BB width;
- MID BB and the relevant outer BB moving in the same direction as momentum.

The width increase + directional MID/outer movement is the project's deterministic encoding of the source phrase `BB vertical / expanding`. No arbitrary percentage threshold is added.

## Downstream consequences
### M12 Re-Entry Type 3
Type 3 now receives a source-aligned CSM precursor from M10. The existing Step 3B lifecycle remains:
`CSM precursor -> candidate -> later retrace to MA5 or MA50 -> confirmed Re-Entry`.

### M12 Re-Entry Type 4
Type 4 now receives the corrected CSD crossing signal as its precursor. Its existing Step 3B lifecycle remains:
`CSD precursor -> candidate -> later retrace to MA5/10 -> confirmed Re-Entry`.

### M08 Extreme invalidation
The primary reference states that Extreme is no longer valid in the presence of CSM. Step 3E repairs the CSM producer, but M08 currently represents raw per-candle Extreme detection rather than a persistent Extreme lifecycle. Therefore historical Extreme invalidation by a later CSM still requires an explicit owner/lifecycle connection; Step 3E does not falsely claim that this temporal invalidation is already solved.

## Collector classification note
A candle that crosses MA5/10 and MID BB mechanically also satisfies the simpler MA5/10 crossing predicate. The source distinguishes CSD from eCSD by the MID BB cross. M10 defines both predicates; M13 must later decide collector-level classification precedence so the same candle is not incorrectly double-counted as two independent confirmations.

## Scope guard
Step 3E does not change:
- Re-Entry retracement confirmation rules already locked in M12;
- REM/RRE/REE combination contracts;
- M14 sequence validation;
- final M15 entry eligibility;
- SL/TP, risk or execution logic.

## Implementation record
Patch:
`blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`

Patch commit:
`d3b804da58e8cb837e66f46d65c9c56fc1e3840d`

## Verification
Focused reconstruction verification:
- patch dry-run: clean;
- patch apply: exact output match;
- braces balanced;
- parentheses balanced;
- brackets balanced;
- old three-candle / 70%-average-body CSM formula removed;
- CSD requires MA5/10 + MID BB crossing;
- eCSD requires MA5/10 crossing;
- CSM requires directional outer-BB close plus expanding/directional BB context.

Because the project previously discovered that a partial reconstruction had been mislabeled as a full-chain source, no new full-working-source SHA is claimed from this focused Step 3E verification.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.


## Sequential implementation candidate — Build6.07 / SIG-01

eCSD alone now targets the accepted MA-pair Close-only predicate and rejects shift0/negative. Its raw predicate may overlap stronger direction, as before; existing collector precedence is unchanged. CSD/CSAK retains historical body code until its own sequential task. The canonical function signature is unchanged; no new custom eCSD token or executable availability is added. Source validation remains in progress until the SIG-01 acceptance checklist closes. No other signal is being migrated in this patch.

SIG-01 update2026-11-10: eCSD canonical Close-only implementation accepted in bounded Build6.07 scope; see CUSTOM_MTF_ECSD_SIGNAL_ACCEPTANCE_20261110.md and exact native/controller/source proofs. CSD/CSAK and user MidBB CSA remain separate pending tasks; this is not complete M10/custom execution acceptance.

## SIG-02 CSA source/context — Build6.08

The user MidBB CSA uses one shared M10 closed-input/fingerprint reader and classifier: BUY Close>MidBB, SELL Close<MidBB. Open/MA/expansion are not criteria;20 valid finalized inputs suffice. Requested read-only snapshots carry symbol/TF/direction/source-candle identity and stay recoveryOnly/non-executable. eCSD is not aliased. Native154/154 and actual-controller210 views accepted in CUSTOM_MTF_CSA_SIGNAL_ACCEPTANCE_20261110.md. CSD/CSAK retains historical body predicate until SIG-03. This is not full M10 or execution acceptance.
