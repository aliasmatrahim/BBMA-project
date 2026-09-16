# Build 4.87 Type-3 Re-Entry Close-Side Repair - 2026-09-17

Issue: #180
Branch: `fix/q5-type3-close-side-180`
Base: `d1-owner-dev@0d8c8ac71aeb9947d48f89239f46a88c31981182`

## Classification
**CONFIRMED IMPLEMENTATION GAP / STRATEGY-PURITY DEFECT.**

Core V2 section 8.1 requires a Re-Entry validation close to remain on the permitted side of the full relevant MA5/MA10 cluster. Type 3 remains `CSM -> later MA5 or MA50 retrace`; MA50 is a retrace reference, not an exemption from that general close-side rule.

## Minimum repair
- Generalize the existing Type-1 close-side helper name to `IsReEntryMAClusterCloseSideFailure()` without changing its formula.
- Preserve `DetectReEntry_Type3()` as CSM precursor authority.
- Preserve `HasReEntryMA5OrMA50Touch()` as Type-3 retrace authority.
- Before Type-3 confirmation, keep the candidate unconfirmed when the validation close clears the full MA5/MA10 cluster.
- Type 1/2/4 detector and confirmation semantics remain unchanged apart from Type-1 using the renamed shared helper.
- No new indicator, timer, pip threshold, risk rule or execution rule is added.

## TDD / static verification
- Final focused suite: **6/6 PASS**.
- Exact owner RED with the final test set: **4 failed / 2 passed** on missing shared helper, missing Type-3 guard, missing Build 4.87 identity, and Type-1 shared-helper regression expectation.
- Cross-module direct guards: **13/13 PASS**.
- `git diff --check`: PASS.

## Native compile / identity
- Build: **4.87 - Type3 Re-Entry Close-Side Repair**.
- MetaEditor: **0 errors / 0 warnings**, 758 ms.
- MQ4 SHA-256: `E9FD8406CF5E0E65AE2272FE23AE43286EC177B8BFB30BC2EEF64A6CA2628325`.
- EX4 SHA-256: `FBCD274BD2D359C1AF43D83C6BEEFBB1916064C59974655D813C264257E15BEE`.

## Historical natural negative-case A/B
Bounded defect-reproduction period: GBPUSD M15, 2026-07-01 through 2026-08-01, model 1, spread 20, zero trade caps, `TradeLockMode=2`.
Harness changes are tester-only symbol/connection/timer compatibility plus read-only Type-3 close-side diagnostics. Detector/state semantics remain those of each compared source.

Natural invalid validation candle:
- direction: BUY;
- candle: `2026.07.13 12:15`;
- close: `1.33898`;
- MA5 Low: `1.33909`;
- MA10 Low: `1.33904`;
- therefore close is below the full relevant MA5/MA10 Low cluster.

Owner baseline:
- 59 Type-3 MA5/MA50 retraces;
- 1 `FullClusterFailure=Y` retrace;
- **1 invalid Type-3 confirmation** in Mode 1;
- **1 invalid Type-3 confirmation** in Mode 2.

Build 4.87:
- same 59 Type-3 retraces;
- same invalid retrace remains observable diagnostically;
- **0 invalid confirmations** in Mode 1;
- **0 invalid confirmations** in Mode 2;
- 58 valid Type-3 confirmations remain in each mode.

Mode-1 regression identity:
- Type 1: owner/fixed `264 RE_EVAL / 144 RE_ADMIT`;
- Type 3: owner/fixed `116 / 34`;
- Type 4: owner/fixed `140 / 24`;
- M15/M16: owner/fixed `147 / 147`;
- Type 2 did not naturally occur in this July window and remains covered by focused static/TDD regression only.

Mode-2 regression identity:
- owner and fixed both: `233 M15_SELECT / 233 M16_PASS`;
- zero order markers in both.

## Positive-path August regression
GBPUSD M15, 2026-08-01 through 2026-09-01 produced 56 natural Type-3 retraces and no full-cluster failures. Owner and Build 4.87 Mode 1 both retained 56 confirmations and `126 M15_SELECT / 126 M16_PASS`. Build 4.87 Mode 2 retained 56 confirmations, `159 M15_SELECT / 159 M16_PASS`, and 10 REM selections. Zero order markers were observed.

## Exact Build 4.87 broker smoke
An isolated `MetaQuotes-Demo` clone used the exact canonical MQ4/EX4 hashes with `ExpertsTrades=false`, zero trade caps and `TradeLockMode=2`.

Observed after log flush:
- broker login and symbol/broker-spec PASS;
- EA initialization PASS;
- D1/NMJE processing active;
- `[F7-TELEM] Init=1 Connected=1`;
- graceful deinitialization;
- zero order markers.

Committed broker evidence must redact demo account/IP identifiers because they are unnecessary for technical attribution.

## Claim boundary
Build 4.87 is TDD/static verified, native-compile verified, natural negative-case runtime verified in both Mode 1 and Mode 2, positive-path regression verified, and exact-binary broker-attributed.

No merge, primary-MT4 modification or production activation is included.
