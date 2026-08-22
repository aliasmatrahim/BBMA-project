# CORE-V2-F3 — Re-Entry Type 1 Context

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED CORE PHILOSOPHY; DETERMINISTIC RANGE DEFINITION STILL PENDING**
Branch: `blueprint-dev`

## User-approved decision
Re-Entry Type 1 must **not** be defined by an arbitrary MA5/MA10 touch alone.

Required structural context:

`PRIOR RISE/FALL -> SIDEWAYS/RANGING PHASE -> RELEVANT MA5/MA10 RETEST -> VALID CLOSE-SIDE`

Direction mapping remains source-derived:
- SELL Type 1: relevant MA5/MA10 High acts as resistance; the validating candle finds the cluster and remains/closes on the permitted SELL side.
- BUY Type 1: relevant MA5/MA10 Low acts as support; the validating candle finds the cluster and remains/closes on the permitted BUY side.

## Evidence classification
The requirement for **rise/fall + sideways/ranging + MA5/MA10 support/resistance behavior** is directly source-backed by the primary PDF page-9 Type 1 description.

Finale provides supporting context rather than a dedicated numeric Type 1 formula:
- V01 places Re-Entry after directional confirmation in the normal cycle.
- V03 repeatedly frames MA5 as the Re-Entry/retest area after direction/momentum develops.
- V05 explicitly states that direction is a signal, not the entry, and that the trader waits for Re-Entry; it also reinforces the MA5/MA10 close-side boundary.
- V06 again teaches Re-Entry after direction confirmation around MA5, with MA10 confluence strengthening the setup.

Therefore the project rejects `MA touch alone = Type 1` as too broad relative to the source structure.

## Important unresolved sub-specification
The source uses natural-language `sideways/ranging` but does **not** provide a deterministic numeric algorithm such as:
- exact candle count;
- exact pip/range width;
- exact Bollinger width ratio;
- RSI/ADX threshold;
- fixed ATR threshold.

None of those may be silently invented and represented as Oma Ally rules.

A separate sub-review must define a source-faithful deterministic representation of the sideways/ranging phase before M12 Type 1 code is patched.

## Rejected alternatives
- MA5/MA10 touch + close-side only: rejected as incomplete.
- Automatically equating Type 1 sideways with `BB_FLAT`: not accepted yet; Finale gives flat-BB semantics but does not explicitly define flat BB as the universal Type 1 ranging criterion.
- Requiring CSD/CSM as a universal Type 1 precursor: not accepted; this risks collapsing Type 1 into the source-defined Type 3/Type 4 families.
- Disabling Type 1 indefinitely: not selected.

## Implementation guard
No code patch is authorized until the deterministic sideways/ranging sub-specification is resolved. The current active implementation remains subject to this known Core gap.
