# M15 Final Signal / Entry Authority Contract

## Status
P0 Step 6 architecture contract for Module 15, with M27 atomic routing support.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference. The locked project `ENTRY_MODE_CONTRACT.md` governs the meaning of Entry Mode 1 and Entry Mode 2.

## Final-authority ownership
M15 is the single final BBMA direction/entry-eligibility authority for one pair on one closed-M15 processing cycle.

M15 does not detect Extreme, MLV, CSD/eCSD, CSM or Re-Entry. It consumes only candidates that have already been made valid by their owning modules:
- M12 confirmed H1 Re-Entry snapshot;
- M14 validated REM/RRE/REE combination candidates.

Raw detector `Valid=true` is never sufficient to create an M15 execution candidate.

## Entry Mode implementation
### EntryMode 1 — RE_ENTRY_ONLY
Eligible candidate type:
- `SIGNAL_RE_ENTRY` only.

The standalone project candidate is the authoritative **confirmed H1 Re-Entry** snapshot from M12. H4 and D1 Re-Entry remain higher-timeframe context/components for REM/RRE/REE in the current D1/H4/H1/M15 architecture.

Candidate/unconfirmed/expired Re-Entry is not eligible.

### EntryMode 2 — ALL_VALIDATED_BBMA_ENTRIES
Currently implemented eligible candidate types:
- confirmed H1 `SIGNAL_RE_ENTRY`;
- validated `SIGNAL_REM`;
- validated `SIGNAL_RRE`;
- validated `SIGNAL_REE`.

This does not make raw Extreme, CSD, eCSD, CSM or MLV directly executable.

Standalone Extreme is intentionally still withheld because the supplied source requires reversal-candle confirmation/retest and the project has not yet locked a deterministic standalone Extreme entry lifecycle. Mode 2 can only expand when another source-valid entry contract is explicitly completed.

## Atomic BUY / SELL rule
M27 must collect both BUY and SELL candidates first, then call M15 **once** for the pair.

The old architecture called final authority separately inside the BUY loop and SELL loop, which could create two independent decisions from the same closed M15 processing cycle.

Step 6 removes that path.

### Opposite validated candidates
If at least one eligible BUY candidate and at least one eligible SELL candidate coexist in the same atomic pool:
- M15 creates **no trade decision**;
- an opposite-direction conflict package is recorded;
- M15 does not invent a winner.

This is a conservative project safety policy, not a claimed BBMA source rule. The supplied references do not define a universal deterministic tie-break between simultaneous opposite validated setups.

## No arbitrary BBMA tier ranking
Step 5 deliberately left M14 candidates at `TIER_NONE` because the supplied REM/RRE/REE source does not define a quality ranking such as REM > RRE > REE.

Therefore Step 6 removes `SignalMode` / SAFE / NORMAL / AGGRESSIVE priority-tier gating from M15 final entry authority.

`SignalMode` is retained as a compatibility/display input only; it no longer decides whether a validated BBMA candidate may trade.

M15 assigns no invented BBMA quality tier to the selected decision.

## Multiple candidates in the same direction
If several eligible candidates exist but all point in the same direction, they do not conflict.

M15 selects one **canonical candidate** only so the decision has one stable identity/hash. This canonicalization is engineering bookkeeping, not strategy ranking:
1. candidate with the latest component candle anchor;
2. then latest `SequenceStartTime`;
3. then deterministic `SequenceHash` tie-break.

The rule must never be described as REM/RRE/REE quality superiority.

## Candidate freshness / expiry ownership
The old downstream formula derived every combination expiry from `Comp1.CandleTime` using a generic `* 900` M15 multiplier. That formula is removed from M27 candidate construction.

New ownership rule:
- candidates are rebuilt from current owner-valid snapshots every closed M15 cycle;
- persistent owner state decides whether the underlying setup still exists;
- confirmed standalone Re-Entry carries the explicit M12 `ExpiryCandleTime` into M15;
- REM/RRE/REE candidates are current-cycle assemblies of owner-valid components and do not receive an invented generic Comp1/M15 expiry.

M16 still contains legacy generic decision-expiry logic and is the next repair target. Step 6 does not falsely certify M16 freshness semantics.

## Decision payload
When exactly one direction survives:
- `Direction` = surviving direction;
- `SignalType` = canonical validated candidate type;
- `SequenceHash` = canonical candidate hash;
- `CandleTime` = latest component candle anchor;
- `CycleStartTime` = candidate metadata start time;
- `PriorityTier = TIER_NONE`;
- `SLTPSource = SIGNAL_NONE`.

M15 does not invent SL/TP source. M17+ must resolve entry/SL/TP under the later source-governed contract.

## M27 orchestration consequence
M27 now:
1. builds frozen D1/H4/H1/M15 data;
2. runs signal/state owners for BUY and SELL;
3. builds confirmed H1 Re-Entry and validated REM/RRE/REE candidates for both directions;
4. appends them into one pair-level candidate pool;
5. calls M15 once;
6. only after final atomic direction authority passes does the decision proceed to M16/M17/risk/execution.

This guarantees at most one final decision path per pair per closed M15 processing cycle before downstream validation.

## Input validation
`EntryMode` is valid only when:
- `1 = RE_ENTRY_ONLY`; or
- `2 = ALL_VALIDATED_BBMA_ENTRIES`.

The old comment `2=AllSignals` is removed.

## Scope guard / next blockers
Step 6 does not certify or repair:
- M16 legacy generic decision expiry;
- temporal CSM invalidation of an existing Extreme;
- standalone Extreme reversal/retest lifecycle;
- M17 entry/SL/TP resolver and direction-aware validation;
- risk / portfolio / execution logic.

## Implementation record
Patch:
`blueprint/patches/0013-p0-step6-m15-final-authority-atomic-entry-mode.patch`

Patch commit:
`0a5c721337ecdedca606e15978a2f043e08717c4`

Focused patch SHA-256:
`9933e041a1999b865c18f340454536ae5371a777d2a6af5d28f2e0d561258b0e`

## Verification
Focused post-Step5 verification:
- patch dry-run: clean;
- patch apply: clean;
- applied output exact-match to generated Step 6 target;
- braces balanced: 484 / 484;
- parentheses balanced: 1467 / 1467;
- brackets balanced: 334 / 334;
- `IsTierAllowed()` removed from M15 authority path;
- legacy `CompareCandidates()` quality-tier comparison removed;
- generic `Comp1.CandleTime + ... * 900` combination expiry assignment removed from M27 candidate construction;
- `PriorityEngine_Atomic(allCandidates, ...)` is called once at pair level;
- old per-direction final-authority call absent;
- Entry Mode candidate guard present;
- standalone confirmed Re-Entry candidate builder present.

This verification is focused on the current Step 5/Step 6 affected regions. It does not reinstate a full-chain working-source SHA claim until the entire ordered patch chain is exactly materialized.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
