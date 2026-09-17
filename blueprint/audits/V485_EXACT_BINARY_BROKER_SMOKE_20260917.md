# Build 4.85 Exact-Binary Broker Smoke — 2026-09-17

Issue: #174
Branch: ix/q5-m12n-order-174
Owner sync: d1-owner-dev@0d8c8ac71aeb9947d48f89239f46a88c31981182
Candidate source commit before evidence commit: 4b74257d65565954a4d637348fa8daa161dbd45a

## Identity
- Build: 4.85 — M12N Orchestration Order Repair.
- MQ4 SHA-256: C66B33546AC93DFA88A4B3E0AF299F8483CC9A614BFD2623657D46F1F28C8D2A.
- EX4 SHA-256 used by this exact-binary run: D2F278CA037881361D7DC3FB50AEB37DA11B353C6C2D093760B976D08CDDF309.
- Fresh native compile: 0 errors / 0 warnings, 744 ms.

## Runtime boundary
Isolated clone: D:\BBMA\MT4_Q5_174_Demo; MetaQuotes-Demo; primary MT4 untouched.
Runtime profile: EntryMode=1, up to 20 requested FX pairs, MaxTradePerPair=0, MaxTotalTrade=0, TradeLockMode=2, terminal ExpertsTrades=false, DebugLevel=4.
18 pairs resolved/loaded by the broker environment.

## Observed exact-binary result
- Connected heartbeat: Init=1 / Connected=1.
- N1-NMJE observations: 28.
- P3M1 RE_EVAL observations: 0.
- P3M1 RE_ADMIT observations: 0.
- OrderSend markers: 0.
- The live state did not contain a confirmed H1 Re-Entry that emitted RE_EVAL during this bounded run, so exact-binary N1 -> RE_EVAL ordering was not observable live.

This does not replace or weaken the deterministic historical Strategy Tester chronology package. That bounded harness changes only tester-environment symbol/timer behavior and already proves 68/68 RE_EVAL observations had a prior same-M15-time N1 observation with zero ordering violations.

## Classification
- Exact production binary broker init/N1 observation: VERIFIED.
- Exact production binary live N1 -> RE_EVAL chronology: NOT VERIFIED / NOT OBSERVABLE IN CURRENT LIVE STATE.
- Harness-assisted historical N1 -> RE_EVAL chronology: VERIFIED (68/68, zero violations).
- Broker orders: disabled; none observed.

Evidence log: lueprint/audits/V485_EXACT_BINARY_BROKER_SMOKE_20260917.log, SHA-256 $hash.
