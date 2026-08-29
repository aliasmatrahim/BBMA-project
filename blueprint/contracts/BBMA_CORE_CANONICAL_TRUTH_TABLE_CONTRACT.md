# BBMA Core Canonical Truth-Table Contract

Date: 2026-08-29  
Status: **C1-A AUDIT LOCK / NO SOURCE OR STRATEGY CHANGE**

## Purpose

Lock the source-observed BBMA signal ownership, maturity, invalidation, and
composition rules before historical performance work. This contract describes
build 4.71; it does not redefine the strategy or authorize runtime activation.

## Frozen authority

- D1 is the strategic owner and H4 is the immediate directional owner.
- H1 supplies setup context.
- M15 is the sole processing and final-decision clock.
- M5 is closed-candle shadow/refinement context only.
- M22 is the sole `OrderSend` owner.
- M23/M24 own lifecycle and recovery surfaces.
- NMJE execution authority, D1TPW, and C044 remain disabled.
- W1 and M30 remain unimplemented; primary M1 remains excluded.
- No daily-loss limit or gate may be added. Same-currency exposure control and
  loss/broker-failure cooldown remain KIV with no authority.

## Single-writer map

| Family | Canonical owner | Export/consumer boundary |
|---|---|---|
| BB shape | M07 | Geometry state only |
| Extreme | M08 | RAW is not exportable; reversal-confirmed/retest states may export |
| MHV/MLV | M09 | Reads the M08 parent; never mutates the parent Extreme lifecycle |
| Momentum (CSM), CSD, eCSD | M10 | Closed source-timeframe classifications |
| Re-Entry Types 1-4 | M12 | Only confirmed, valid Re-Entry may export |
| REM/RRE/REE | M13 | Collection only; creates no final decision |
| Sequence validation | M14 | Exact signature and direction-consistency validation only |
| Candidate selection | M15 | Sole final signal authority |

## Atomic detector truth

### Extreme

- SELL RAW: MA5 High or MA10 High is above the upper Bollinger Band.
- BUY RAW: MA5 Low or MA10 Low is below the lower Bollinger Band.
- RAW alone is not a combination component.
- Reversal confirmation must occur on a subsequent closed source-timeframe
  candle and match the reversal direction.
- Relevant outer-BB continuation or accepted Momentum invalidates before any
  maturity promotion.
- Reversal-confirmed, retest-phase, and retest-ready states are mature only
  while valid.
- A newer opposite reversal-confirmed Extreme supersedes the older owner.
  Equal confirmation time remains ambiguous and fails closed downstream.

### Momentum / CSM

- BUY requires widening BB, rising MID and upper BB, and close above upper BB.
- SELL requires widening BB, falling MID and lower BB, and close below lower BB.
- An outside close without directional BB expansion is not canonical CSM.

### CSD and eCSD

- BUY eCSD body-crosses MA5 High and MA10 High upward.
- SELL eCSD body-crosses MA5 Low and MA10 Low downward.
- CSD additionally body-crosses MID BB in the same direction.
- When CSD and eCSD classify the same candle/direction, CSD owns and eCSD is
  suppressed for combination snapshots.

### MHV/MLV

- BUY MHV attaches to a mature SELL M15 Extreme; SELL MHV attaches to a mature
  BUY M15 Extreme.
- The canonical order is parent-ready, TP-Wajib complete, loss developing,
  formation established, optional retest complete, then direction taken.
- Momentum/outer-BB continuation invalidates before formation or takeover.
- eCSD/CSD takeover is valid only on a later closed candle after formation.
- After direction takeover, same-cycle continuation cannot retroactively erase
  MHV provenance; only a newer canonical parent may supersede it.

### Re-Entry

- Specific ownership precedence is Type 3 (post-CSM), Type 4 (post-CSD), Type 2
  (MA5/10 plus MID-BB collision), then generic Type 1 context.
- Type 1 requires a prior source-valid direction owner plus structural
  retrace/ranging; MA touch alone is insufficient without that owner.
- Type 1 has structural owner lifetime and no generic candle TTL.
- Types 2-4 use the existing intrinsic expiry window.
- Type 2 requires three qualifying observations and MA-cluster touch.
- Type 3 confirms on post-CSM retrace to MA5 or MA50.
- Type 4 confirms on post-CSD retrace to MA5/MA10.
- Opposite direction ownership clears Type-1 context atomically.

## Composite signatures

All three components must be present, source-valid, and direction-consistent.

| Composite | Component 1 | Component 2 | Component 3 |
|---|---|---|---|
| REM | H4 Re-Entry | H1 Extreme | M15 mature MLV |
| RRE | D1 Re-Entry | H4 Re-Entry | H1 Extreme |
| REE | D1 Re-Entry | H4 Extreme | H1 Extreme |

M13 may collect these signatures. M14 may validate them. Neither module may
select or execute a trade.

## Candidate and semantic-source boundary

- Mode 1 admits confirmed H1 Re-Entry only under the matching recovered H4
  owner.
- Mode 2 admits Re-Entry plus exact REM/RRE/REE signatures and separately
  authorized D1 opportunity candidates.
- Candidate direction must match its applicable D1 authority identity.
- D1-opportunity Re-Entry uses H1 Re-Entry as semantic source, with explicit
  M15 fallback. Legacy Re-Entry uses H1; REM uses H4 Re-Entry; RRE/REE use D1
  Re-Entry.
- NMJE/M5 metadata cannot create, reject, rank, delay, resize, or execute a
  candidate.

## Golden-fixture boundary

`blueprint/tests/fixtures/bbma_core_golden_truth_table.json` is a deterministic
state/signature fixture derived from the source rules above. It verifies state
labels, valid transitions, symmetry, exact composite topology, and fail-closed
illegal transitions. It is not market-performance evidence and cannot prove a
trading edge.

## C1-B closed-candle price equivalence

`blueprint/tests/test_bbma_core_candle_price_equivalence.py` locks numeric
BUY/SELL examples and exact boundary behavior for:

- RAW Extreme and reversal direction;
- candle-body crossing, CSM, CSD, and eCSD;
- Re-Entry MA5/MA10 cluster and MA5/MA50 interaction;
- Type-1 close-side failure and structural retrace;
- Extreme retest start/body/MA5 interaction;
- MHV TP-Wajib completion, loss phase, move-away, and marked-body retest.

The accompanying source-static guard binds those fixtures to the exact MQL4
predicate text and build-4.71 source SHA-256. Strict comparisons remain strict;
inclusive touches remain inclusive. These fixtures are deterministic offline
predicate evidence, not native MQL4 execution or market-performance evidence.

## Change boundary

Any change to a detector predicate, transition, component topology, processing
clock, candidate eligibility, semantic source, or execution authority is a
strategy semantic change. It requires a separate explicit user decision,
visible EA build/header increment, deterministic comparison, native 0E0W, and
broker/demo evidence where applicable.

