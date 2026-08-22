# CORE-V2-F3 — Re-Entry Type 1 Context

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED CORE PHILOSOPHY + STRUCTURAL RANGING; MINIMUM-CANDLE SUB-SPEC STILL PENDING**
Branch: `blueprint-dev`

## User-approved decision 1 — Type 1 context
Re-Entry Type 1 must **not** be defined by an arbitrary MA5/MA10 touch alone.

Required structural context:

`PRIOR RISE/FALL -> SIDEWAYS/RANGING PHASE -> RELEVANT MA5/MA10 RETEST -> VALID CLOSE-SIDE`

Direction mapping remains source-derived:
- SELL Type 1: relevant MA5/MA10 High acts as resistance; the validating candle finds the cluster and remains/closes on the permitted SELL side.
- BUY Type 1: relevant MA5/MA10 Low acts as support; the validating candle finds the cluster and remains/closes on the permitted BUY side.

## User-approved decision 2 — structural meaning of sideways/ranging
The project adopts **BBMA structural ranging** rather than equating Type 1 ranging to one fixed numeric threshold or to `BB_FLAT` alone.

Accepted interpretation:
- a prior directional rise/fall has already occurred;
- active directional momentum has paused/ended rather than continuing as a valid CSM/momentum state;
- price consolidates/retraces rather than continuing impulsively;
- the relevant MA5/MA10 cluster begins acting as support/resistance for the intended Re-Entry direction;
- the final Re-Entry candle must still satisfy the accepted MA5/MA10 close-side rule.

`BB_FLAT` / horizontal BB may be **supporting evidence** for the ranging phase, but it is not by itself a universal or mandatory definition of Type 1 sideways.

## Evidence classification
The requirement for **rise/fall + sideways/ranging + MA5/MA10 support/resistance behavior** is directly source-backed by the primary PDF page-9 Type 1 description.

Finale provides supporting context rather than a dedicated numeric Type 1 formula:
- V02 distinguishes expanding BB from flat/horizontal BB and states that flat BB has no directional momentum.
- V01 places Re-Entry after directional confirmation in the normal cycle.
- V03 repeatedly frames MA5 as the Re-Entry/retest area after direction/momentum develops.
- V05 explicitly states that direction is a signal, not the entry, and that the trader waits for Re-Entry; it also reinforces the MA5/MA10 close-side boundary.
- V06 again teaches Re-Entry after direction confirmation around MA5, with MA10 confluence strengthening the setup.

Therefore:
- `MA touch alone = Type 1` is rejected as too broad;
- `BB_FLAT alone = Type 1 sideways` is also rejected as too narrow/unsupported.

The structural-ranging interpretation is classified as **SOURCE-INFERRED / STRONG HINT** built on an explicit PDF requirement for sideways/ranging.

## Important unresolved sub-specification
The source uses natural-language `sideways/ranging` but does **not** provide a universal numeric minimum-candle algorithm.

It does not explicitly state:
- exact candle count for Type 1 ranging;
- exact pip/range width;
- exact Bollinger width ratio;
- RSI/ADX threshold;
- fixed ATR threshold.

None of those may be silently invented and represented as Oma Ally rules.

A separate sub-review must decide whether the executable specification should use no fixed candle count or an explicitly-labelled project/engineering minimum before M12 Type 1 code is patched.

## Rejected alternatives
- MA5/MA10 touch + close-side only: rejected as incomplete.
- `BB_FLAT` alone as the ranging definition: rejected.
- fixed ATR/pip/range threshold as a Core rule: rejected as unsupported.
- requiring CSD/CSM as a universal Type 1 precursor: not accepted; this risks collapsing Type 1 into the source-defined Type 3/Type 4 families.
- disabling Type 1 indefinitely: not selected.

## Implementation guard
No code patch is authorized until the remaining deterministic Type 1 sub-specification is resolved. The current active implementation remains subject to this known Core gap.
