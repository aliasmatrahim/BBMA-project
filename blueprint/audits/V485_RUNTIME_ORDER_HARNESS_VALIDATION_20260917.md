# Build 4.85 M12N Runtime Order Validation — 2026-09-17

Issue: #174
Branch: `fix/q5-m12n-order-174`
Production candidate: `2ef8976183985187218c0ec8833fa8f80b3e43b4`
Status: **HARNESS-ASSISTED RUNTIME CHRONOLOGY PASS**

## Purpose
Validate that runtime `N1-NMJE` observation occurs before standalone Re-Entry candidate evaluation after the Build 4.85 M12N orchestration repair.

## Why a tester harness was required
The exact Build 4.85 binary cannot initialize unchanged in MT4 Strategy Tester because two tester-only API constraints occur before strategy processing:
1. `GBPUSD` is present and already selected, but `SymbolSelect(Symbol(), true)` returns false, causing `FindActualSymbol()` to reject the current tester symbol.
2. `EventSetTimer(1)` fails in Strategy Tester with error 4059.

A tester-only harness was generated from the exact Build 4.85 source. Its only differences are:
- under `IsTesting()`, return `Symbol()` when the requested pair equals the current tester symbol;
- under `IsTesting()`, skip timer registration; `OnTick()` continues to drive `OnTickMain()`.

No `ProcessPair()`, M06-M16, detector, candidate, selection, risk or execution logic was changed.
Harness delta: `V485_RUNTIME_ORDER_HARNESS_DELTA_20260917.patch`.
## Exact identities
- Production MQ4 SHA-256: `C66B33546AC93DFA88A4B3E0AF299F8483CC9A614BFD2623657D46F1F28C8D2A`.
- Production EX4 SHA-256: `0F1E8CC7C0A81A53C2B8DB0A21290CBE028AC508256B071E3FB6C045AC3B1D8C`.
- Harness MQ4 SHA-256: `EFB877AF916555D841CE549B748F3DBC18192410E595AAF6F88A403B1EB7B40B`.
- Harness EX4 SHA-256: `070EE0BBE06A5CE7CB18D8B8D3BAA76E75248BC3D47BB890CEF5C318D9D06385`.
- Harness native compile: **0 errors / 0 warnings**.

## Strategy Tester run
- Isolated runner: `D:\BBMA\MT4_TesterRunner_Diag`.
- Symbol / timeframe: GBPUSD / M15.
- Model: 1.
- Window: 2026-08-10 through 2026-08-12.
- `EntryMode=1`, `MaxTradePerPair=0`, `MaxTotalTrade=0`, `TradeLockMode=2`, `DebugLevel=4`, `InstanceID=85`.
- 6,738 tick events, 192 M15 bars, 7,769 bar states.
- Broker-order markers: 0.

Deterministic full-run analyzer result:
- `N1-NMJE`: 192 across 192 unique M15 timestamps.
- `P3M1/RE_EVAL`: 68.
- `P3M1/RE_ADMIT`: 19.
- RE_EVAL ordering violations: **0 / 68**.
- Initialization failures in accepted run: 0.

Representative same-cycle evidence at 2026-08-10 14:00:00: raw run lines 469-471 are `N1-NMJE -> RE_EVAL -> RE_ADMIT` in that order.
## Evidence package
- Raw accepted run SHA-256: `B3BF0F2948FB6069249763FDEA819BF7BFC5630B78907F6CA188127A79DE9801`.
- Analyzer summary SHA-256: `412C38F45DF1AB1697AF11914C686C68A7C3B90897860F83450CDC58E71023EE`.
- Harness delta SHA-256: `66964E90D00F82DFA92D529C146468E181EF4212D4CA34027C34B8D911BEDD59`.
- Harness compile log SHA-256: `11378B5ABAC52813A32B2C5B906347C77F2D22D5D8E38AF795C1D08792D5006D`.

## Result
**PASS for #174 runtime chronology under the bounded Strategy Tester harness.** Every observed Re-Entry evaluation occurred after `N1-NMJE` for the same M15 processing timestamp.

This is not claimed as exact-production-binary runtime verification because the unchanged production binary is blocked by MT4 Strategy Tester API behavior before strategy processing. No primary MT4 restart, live broker action, production activation, or #175 Mode-2 scope change occurred.