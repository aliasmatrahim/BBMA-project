# Q9 Build 4.94 P10 Entry Displacement Telemetry — 2026-09-19

Issue: #101
Branch: `q9-nmje-v2-p10-entry-displacement-101`
Base: P9 audit head `b5e945b864e0e39f1f9b075afd021e533d5ed01c`
Build: `4.94` / `V494_Q9_P10_ENTRY_DISPLACEMENT_20260919`
Status: RESEARCH TELEMETRY ONLY / NO ACTIVATION

## Confirmed telemetry gap

Before P10, `decision.EntryPrice` is overwritten by `ResolveExecutionReferencePrice()` with the live broker-side ASK/BID before order submission.

After a successful fill, `TradeInfo.initial_entry_price` records `OrderOpenPrice()`.

Therefore the existing data did not preserve a separate closed-candle source reference, so outcome analysis could not separate:
- source -> preflight displacement; and
- preflight -> broker-fill displacement.

This was a telemetry gap only. It was not a Strategy-Core or execution-eligibility defect.

## Implementation

P10 adds `NMJEEntryDisplacementState` and keeps the same-runtime measurement in `TradeInfo.entry_displacement`.

Measurement is built only after a genuine broker ticket exists and `OrderOpenPrice()` is available.
The source reference is read from the already-frozen P9 semantic `SLTPSourceComponent`:
- exact source signal type;
- exact source timeframe;
- exact source candle identity;
- exact closed source candle `iClose()`.

This source close is an EA engineering telemetry reference, not a universal BBMA entry-price rule.

Recorded prices:
- `SourceReferencePrice`;
- `PreflightReferencePrice` from the existing resolved execution reference;
- `BrokerOpenPrice` from the actual order.

Signed pips are direction-normalized:
- BUY: `(to - from) / pip`;
- SELL: `(from - to) / pip`.

Positive means farther in the selected trade direction; negative means retracement. No threshold, score, grade or rejection rule is introduced.

When existing P4 ticket-bound attribution is available, P10 mirrors the runtime measurement into its additive durable record with keys:
`DP/DSG/DTF/DCT/DSP/DPP/DBP/D12/D2B/D1B`.

Pre-P10 records remain readable. Missing P10 persistence never changes recovery, lifecycle, candidate, risk or execution state.
## Telemetry rows

P10 uses dedicated rows:
- `[Q9-P10-DISP-OPEN]`;
- `[Q9-P10-DISP-OUT]`.

The separate rows avoid changing the meaning of existing P4 rows and avoid the MQL4 `Print()` parameter-count limit.

## Corrected validation defects

1. **CONFIRMED BUG — durable mirror self-assignment**
   - interrupted decoupling accidentally produced `info.entry_displacement = info.entry_displacement`;
   - fixed to `info.nmje_attribution.EntryDisplacement = info.entry_displacement`.

2. **CONFIRMED COMPILE BUG — P4 Print parameter overflow**
   - adding all P10 fields directly to the already-long P4 output caused MetaEditor error 199;
   - fixed by dedicated P10 OPEN/OUT telemetry rows.

Both defects were corrected before the final static/native/tester evidence.

## Authority firewall

P8 -> P10 exact-body equality is preserved for candidate construction, comparator, M15, M16, execution-reference resolution, M17 SL/TP resolver, risk, preflight, TradeLock and broker send.

No merge / no production activation.
