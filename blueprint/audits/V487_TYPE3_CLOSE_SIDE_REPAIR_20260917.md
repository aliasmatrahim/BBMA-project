# Build 4.87 Type-3 Re-Entry Close-Side Repair Ã¢â‚¬â€ 2026-09-17

Issue: #180
Branch: `fix/q5-type3-close-side-180`
Base: `d1-owner-dev@0d8c8ac71aeb9947d48f89239f46a88c31981182`

## Classification
**CONFIRMED IMPLEMENTATION GAP / STRATEGY-PURITY DEFECT.**

Core V2 Ã‚Â§8.1 requires a Re-Entry validation close to remain on the permitted side of the full relevant MA5/MA10 cluster. Type 3 remains `CSM -> later MA5 or MA50 retrace`; MA50 is a retrace reference, not an exemption from that general close-side rule.

## Minimum repair
- Generalize the existing Type-1 close-side helper name to `IsReEntryMAClusterCloseSideFailure()` without changing its formula.
- Preserve `DetectReEntry_Type3()` as CSM precursor authority.
- Preserve `HasReEntryMA5OrMA50Touch()` as Type-3 retrace authority.
- Before Type-3 confirmation, keep the candidate unconfirmed when the validation close clears the full MA5/MA10 cluster.
- Type 1/2/4 detector and confirmation semantics remain unchanged apart from Type-1 using the renamed shared helper.
- No new indicator, timer, pip threshold, risk rule or execution rule is added.

## TDD / static verification
Final focused suite: **6/6 PASS**.
Exact owner RED with the final test set: **4 failed / 2 passed**, failing on the missing general helper, missing Type-3 guard, missing unique Build 4.87 identity, and the Type-1 shared-helper regression expectation.
Cross-module direct guards: **13/13 PASS**.
`git diff --check`: PASS before evidence packaging.
## Native compile / identity
Build: **4.87 Ã¢â‚¬â€ Type3 Re-Entry Close-Side Repair**.
MetaEditor: **0 errors / 0 warnings**, 758 ms.
MQ4 SHA-256: `E9FD8406CF5E0E65AE2272FE23AE43286EC177B8BFB30BC2EEF64A6CA2628325`.
EX4 SHA-256: `FBCD274BD2D359C1AF43D83C6BEEFBB1916064C59974655D813C264257E15BEE`.

## Historical Strategy Tester evidence
Bounded period: GBPUSD M15, 2026-08-01 through 2026-09-01, model 1, spread 20, trade caps zero, `TradeLockMode=2`.
Harness changes are tester-only symbol/connection/timer compatibility plus read-only Type-3 close-side diagnostics.

Owner Mode 1:
- 56 natural Type-3 MA5/MA50 retraces;
- 56 confirmations;
- 0 `FullClusterFailure=Y` observations.

Build 4.87 Mode 1:
- same 56 retraces / 56 confirmations;
- 126 M15 selections / 126 M16 passes;
- zero order markers.

Build 4.87 Mode 2:
- 56 retraces / 56 confirmations;
- 159 M15 selections / 159 M16 passes;
- 10 REM selections;
- zero order markers.
### Negative-case boundary
No natural Type-3 retrace with `FullClusterFailure=Y` occurred in the bounded GBPUSD month. Therefore the negative runtime case is **NOT OBSERVED** and is not claimed as runtime-proven. A bounded EURUSD follow-up was excluded because Strategy Tester returned `no ticks generated`.

Prevention of the invalid confirmation is verified by the focused owner RED / Build 4.87 GREEN guard and direct code ordering: `MA5/MA50 touch -> full MA5/MA10 close-side guard -> confirmation`.

## Exact Build 4.87 broker smoke
Isolated `MetaQuotes-Demo` clone used exact canonical MQ4/EX4 hashes with `ExpertsTrades=false`, zero trade caps and `TradeLockMode=2`.

Observed after log flush:
- broker login and symbol/broker-spec PASS;
- EA initialization PASS;
- D1/NMJE processing active;
- `[F7-TELEM] Init=1 Connected=1`;
- graceful deinitialization;
- zero order markers.

Committed broker evidence redacts demo account/IP identifiers because they are unnecessary for technical attribution.

## Claim boundary
Build 4.87 is compile-verified, focused/regression-verified, valid-path historical-runtime verified, and exact-binary broker-attributed. The rare negative natural runtime scenario was not observed and is explicitly not claimed.

No merge, primary-MT4 modification or production activation is included.
