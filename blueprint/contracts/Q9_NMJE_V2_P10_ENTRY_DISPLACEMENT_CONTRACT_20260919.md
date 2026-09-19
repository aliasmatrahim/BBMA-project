# Q9 NMJE v2 P10 Entry Displacement Telemetry Contract — 2026-09-19

Issue: #101
Base: P9 audit commit `b5e945b864e0e39f1f9b075afd021e533d5ed01c`
Target: Build 4.94 / `V494_Q9_P10_ENTRY_DISPLACEMENT_20260919`
Status: RESEARCH TELEMETRY ONLY / NO FILTER / NO ACTIVATION

## Purpose

Measure execution displacement without changing whether, when or how a BBMA trade is authorized.

P10 records the distance between:
1. the exact closed-candle price reference belonging to the already-frozen semantic SL/TP source component;
2. the live broker-side preflight reference already used by execution;
3. the actual broker `OrderOpenPrice()`.

The result is outcome-attribution data only.

## Source and semantic boundary

Accepted Core remains unchanged:
- Re-Entry confirmation is based on a fully closed source-timeframe validation candle;
- execution may become eligible during the immediately following live source-timeframe candle, subject to M15/final-authority and downstream gates;
- actual broker `OrderOpenTime()` / fill price is runtime evidence, not a new Strategy-Core rule.

P9 already verified the frozen structural source:
- standalone Re-Entry -> H1 Re-Entry;
- standalone Extreme -> H1 Extreme;
- REM -> H4 Re-Entry;
- RRE / REE -> D1 Re-Entry;
- D1 opportunity H1+M15 cluster -> H1 Re-Entry;
- D1 opportunity M15-only -> M15 Re-Entry.

P10 MUST use that frozen `SLTPSourceComponent`. It may not choose another component or create a new structural owner.

## Engineering measurement

`SourceReferencePrice` is a research reference:
- exact `iClose()` of the frozen `SLTPSourceComponent.CandleTime`;
- exact source timeframe;
- valid closed candle resolved through existing source-shift validation.

For Re-Entry this corresponds to the frozen source confirmation candle close.
For standalone Extreme it corresponds to the frozen retest-completion candle close.

This is an **EA ENGINEERING TELEMETRY MAPPING**, not a universal BBMA entry-price formula.

`PreflightReferencePrice` is the existing live broker-side price frozen by `ResolveExecutionReferencePrice()`:
- BUY -> ASK;
- SELL -> BID.

`BrokerOpenPrice` is the actual selected order `OrderOpenPrice()`.

## Direction-normalized displacement

P10 records pips with this sign convention:
- BUY: `(to - from) / pip`;
- SELL: `(from - to) / pip`.

Therefore:
- positive = price moved farther in the intended trade direction / more extended;
- negative = price retraced relative to the earlier reference;
- zero = unchanged at measurement precision.

Recorded measurements:
- source -> preflight pips;
- preflight -> broker-open pips;
- source -> broker-open pips.

No numeric threshold, grade, score, minimum/maximum displacement or hard entry-distance rule is authorized.

## Attribution lifecycle

P10 attaches telemetry only after a broker ticket exists and `OrderOpenPrice()` is available.

The P10 runtime measurement belongs to `TradeInfo.entry_displacement` and is built after a genuine broker ticket/open price exists, independently of NMJE availability.

When an existing P4 ticket-bound attribution record is available, P10 mirrors the same payload into that record for durable restart/outcome attribution. P10 does not create a second persistence owner.

The durable mirror may persist:
- source signal type;
- source timeframe;
- source candle time;
- source reference price;
- preflight reference price;
- broker open price;
- three signed displacement-pip values.

Persistence remains:
- ticket scoped;
- magic/open-time/execution-hash cross-validated by existing P4 ownership;
- additive/backward-readable for pre-P10 records;
- diagnostic only on failure.

If P4 attribution is unavailable, P10 may still emit same-runtime open/outcome measurement from `TradeInfo`; restart durability is then unavailable rather than synthesized.

On recovery, a valid P4 displacement mirror is copied back into `TradeInfo.entry_displacement`.

A P10 persistence failure MUST NOT alter recovery state, trade lifecycle, candidate state, risk or execution.

## Outcome telemetry

Open and closed-outcome research rows may include:
- `DISP=Y/N`;
- source type / timeframe / candle;
- source price;
- preflight price;
- broker-open price;
- source-to-preflight pips;
- preflight-to-open pips;
- source-to-open pips.

No outcome field may be consumed by an executable path.

## Authority invariants

P10 MUST NOT:
- create/reject/rank/delay candidates;
- change M13/M14;
- change `CompareCanonicalCandidates`;
- change `PriorityEngine_Atomic`;
- change M16;
- change M17 SL/TP geometry or source ownership;
- change risk/MM/lot sizing;
- change allowed execution deviation or broker retry rules;
- change `OrderSend` parameters;
- add a new execution-distance rejection;
- change trade count;
- activate P2;
- make M5 executable authority.

M15 remains sole processing/final-decision clock.

## Validation exit gate

Require:
- focused P10 static/model/persistence tests PASS;
- inherited P8/P7/P6/P5/P4/P2-P3/P1/read-only/M12N/D1O/N3 regressions PASS;
- protected M13/M14/comparator/M15/M16/M17/risk/preflight/order-send authority bodies unchanged except the explicitly additive post-fill telemetry hook where required;
- broker primitive counts unchanged;
- native MetaEditor 0 errors / 0 warnings;
- deterministic Strategy Tester P10 A/B on the verified GBPUSD M15 August window;
- exact P8/P10 M15/M16/decision authority-trace equality;
- exact broker-action count equality;
- P10 displacement telemetry naturally exercised if a successful fill exists in the test window; otherwise classify runtime branch bounded-unexercised rather than synthesizing a fill;
- no merge / no production activation.
