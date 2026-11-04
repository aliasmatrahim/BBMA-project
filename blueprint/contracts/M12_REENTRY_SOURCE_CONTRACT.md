# M12 Re-Entry Source Contract

## Status
P0 Step 3B source-alignment contract for Module 12.

The user-supplied `Oma ally BBMA - AL.pdf` is the primary operational BBMA reference. `BBMA technique.pdf` is a secondary corroborating reference. GitHub remains the project source of truth for the active blueprint.

## Source-derived rules

### General Re-Entry
Primary reference page 9 states that Re-Entry forms after a rise/fall as price forms sideways/ranging behaviour.

Secondary reference page 19 states the general BBMA entry-side law:
- BUY only on MA5/10 Low.
- SELL only on MA5/10 High.

M12 therefore maps the relevant MA cluster as:
- BUY -> MA5 Low + MA10 Low.
- SELL -> MA5 High + MA10 High.

### Type 1
Primary reference page 9:
- SELL context: price finds MA5/10 High and candlesticks are below MA5/10 High.
- BUY context: price finds MA5/10 Low and candlesticks are above MA5/10 Low.

Blueprint consequence:
- The old EMA50-near / EMA50-cross Type 1 detector is rejected as non-source-aligned.
- A CLOSED candle touching the relevant MA5/10 cluster and closing on the stated support/resistance side is the confirmed Type 1 setup.
- M12 does not invent a second EMA50 confirmation candle.

Trend wording is intentionally not hard-gated inside M12 because the primary reference also contains higher-timeframe trend-alignment guidance elsewhere. M12 owns setup detection; final trade-eligibility trend alignment belongs downstream and must be reconciled separately rather than silently resolving source wording inside the detector.

### Type 2 — Powerful Re-Entry
Primary reference page 10:
- Powerful Re-Entry: MA5/10 and MID BB meet/collide.
- Most Powerful Re-Entry: MA5/10 + MID BB + MA50 meet/collide.
- Minimum duration stated: 3 candles per timeframe.

Blueprint consequence:
- Old BB-width / close-outside-BB detector is rejected.
- Candidate begins when the relevant MA5/10 cluster collides with MID BB.
- MA50 confluence is retained as stronger Type 2 metadata, not a separate strategy type.
- Confirmation requires the minimum-candle contract plus the general Re-Entry MA5/10 entry-cluster touch.

### Type 3 — CSM Re-Entry
Primary reference page 10:
- CSM forms first.
- Price then reverses/retraces to MA5 or MA50, indicating Re-Entry.

Blueprint consequence:
- CSM alone is only a candidate precursor, never an immediately valid Re-Entry.
- Confirmation occurs on a later closed candle that retraces to the relevant MA5 or MA50 support/resistance level.

### Type 4 — CSD Re-Entry
Primary reference page 10:
- CSD forms first.
- Price then gyrates/retraces toward MA5/10.
- BUY uses the MA5/10 Low context; SELL uses the MA5/10 High context.

Blueprint consequence:
- CSD alone is only a candidate precursor, never an immediately valid Re-Entry.
- Confirmation occurs on a later closed candle that reaches the relevant MA5/10 entry cluster.

## Lifecycle contract

Only confirmed Re-Entry state may be exported downstream as `SIGNAL_RE_ENTRY`.

Type-specific lifecycle:
- Type 1: source-valid direction owner -> structural ranging/retrace -> `CANDIDATE` -> `CONFIRMED`; validity ends only through source-owned structural invalidation/ownership transfer.
- Type 2: `NONE -> CANDIDATE -> CONFIRMED`; confluence break, MA5/MA10 close-side failure or opposite source-valid direction/momentum resets the current owner.
- Type 3: `NONE -> CANDIDATE(CSM) -> CONFIRMED(retrace MA5/MA50)`; MA5/MA10 close-side failure or opposite source-valid direction/momentum resets the current owner.
- Type 4: `NONE -> CANDIDATE(CSD) -> CONFIRMED(retrace MA5/10)`; MA5/MA10 close-side failure or opposite source-valid direction/momentum resets the current owner.

`MaxWaitBars_ReEntry` is not Strategy-Core lifetime authority for Type 1/2/3/4. Age/expiry fields may remain for compatibility or diagnostics only and must not invalidate an otherwise source-valid owner.

M15 remains the sole orchestration clock, but H1/H4/D1 lifecycle state advances only when a new closed candle of that state slot's own timeframe is observed.

### Unreadable current source refresh — execution-safety boundary

An invalid, unclosed or mismatched H1/H4 refresh preserves the last M12/H4 structural owner; persistence is not evidence that the latest required source snapshot was readable. M15 must not admit a new entry that depends on that snapshot until the exact latest closed source candle is valid. M16 repeats the check before validation. When readable data returns, the still-valid structural owner may be reconsidered. This is a data-integrity execution safeguard, not an age-based Strategy-Core expiry or a new BBMA signal rule.

## Explicit implementation interpretations
These are engineering encodings needed to turn source language into deterministic code. They are NOT claimed as verbatim source rules.

1. **Type 2 minimum 3 candles**
   - Encoded as three distinct consecutive closed candles maintaining MA5/10 + MID BB confluence.
   - If confluence breaks before the minimum is reached, the Type 2 candidate is reset.

2. **Meet/collide numerical tolerance**
   - Uses the project's existing `IsNear()` helper only as a numerical representation of line collision.
   - The PDF gives no numeric collision tolerance. This tolerance must not be presented as an Oma Ally rule and may require later validation/backtesting.

3. **MA touch representation**
   - Uses candle high/low reaching the relevant MA support/resistance cluster together with close remaining on the source-stated side.
   - This avoids inventing a new pip-distance trading threshold.

### Overlapping Type 2/3/4 precursor predicates — project policy selected

The primary PDF (p.10), accepted Core V2 §§8.3–8.5, Finale evidence and this contract define the individual Type 2, 3 and 4 structures but do not set a priority when more than one precursor predicate qualifies on the same source-timeframe candle. CP15 directly inspected primary PDF p.10 (SHA-256 matches SOURCE_INDEX: 3e6065dd97c20951bd8af96bc81b81ca138800184be6fc4740a32aa4ab0a9c9c) and confirmed there is no overlap priority, tie-break or mutual-exclusion instruction. Static review does not establish that such overlap occurred in market data.

**Project policy approved 2026-10-27:** when the direction/timeframe M12 owner is empty, preserve the existing Build 5.15 short-circuit sequence: Type 3 → Type 4 → Type 2 → Type 1. The first matching Type 3, Type 4 or Type 2 precursor starts the owner; Type 1 remains the fallback when no specific precursor starts. This makes the existing deterministic implementation order an explicit project policy. It is not an Oma Ally, Core V2 or Finale source rule.

The policy does not assert that the predicates overlap or are mutually exclusive. It does not change type detectors, confirmed-owner persistence/lifecycle, close-side validation, higher-timeframe eligibility, M15/M16 authority, risk or execution. No owner source change is needed for this decision because Build 5.15 already follows the selected order.

Status: **PROJECT POLICY SELECTED — source precedence remains unspecified; market overlap not verified**. Decision record: blueprint/decisions/M12_REENTRY_OVERLAP_PRIORITY_POLICY_DECISION_20261027.md.
## Removed non-source logic
Step 3B removes/rejects these active M12 behaviours:
- Type 1 EMA50-near candidate + later EMA50-cross confirmation.
- Type 2 BB-width contraction + close beyond outer BB.
- Type 3 `CSM == immediately valid Re-Entry` shortcut.
- Type 4 generic MA5/MA10 interval test using High MAs for both directions.
- Wrong ReEntry snapshot mapping where BUY stored High MAs and SELL stored Low MAs.

## Upstream dependencies still blocking full production trust
Step 3B aligns the M12 contract, but it does not certify upstream producers:

1. **M06 MA producer**
   - The current blueprint's MA5/10 High/Low producer still requires a separate source-correctness repair before M12 numeric output can be trusted in production.

2. **M10 CSM/CSD producer**
   - Type 3 depends on M10 CSM detection; Type 4 depends on M10 CSD detection.
   - M12 does not redefine those signals. Their exact source alignment must be audited in their owning module.

3. **Higher-timeframe trend alignment**
   - Primary reference pages 10 and 13 instruct multi-timeframe / higher-timeframe trend confirmation.
   - This is not silently hard-coded into M12 setup detection. It must be enforced in the later final entry-eligibility/priority contract.

## Implementation record
Patch:
`blueprint/patches/0006-p0-step3b-reentry-source-alignment.patch`

Do not merge to `main` until upstream producer dependencies and downstream entry eligibility are also source-aligned and the full blueprint is explicitly approved as MASTER BLUEPRINT LOCKED.
