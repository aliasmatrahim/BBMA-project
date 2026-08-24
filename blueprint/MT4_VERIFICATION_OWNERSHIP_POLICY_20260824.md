# MT4 Verification Ownership Policy

Date: 2026-08-24  
Status: **ACTIVE FOR CURRENT DEVELOPMENT TRACK**

## Purpose
Separate verification work that can be automated on GitHub from checks that require the user's real broker/VPS environment.

## GitHub / CI responsibility
GitHub-side verification should be performed whenever technically possible before asking for manual verification:

1. source/build identity verification;
2. static architecture/integrity checks;
3. native MT4 MetaEditor compile;
4. require `0 errors / 0 warnings` and EX4 production;
5. launch a real MT4 terminal on a Windows runner where practical;
6. attach/load the EA with trading disabled for runtime smoke testing;
7. collect and inspect MT4 Journal and MQL4 Experts logs;
8. fail on fatal MQL runtime signatures such as array-out-of-range, zero-divide, access violation, stack overflow, invalid pointer, unresolved import, or EA initialization failure;
9. preserve runtime evidence as CI artifacts;
10. extend to Strategy Tester automation where deterministic symbol/history data are available.

An unavailable broker feed/symbol history on a GitHub runner is an **environment limitation**, not automatically an EA defect. It must be distinguished from an actual MQL/runtime failure.

## User responsibility — real broker verification only
Manual verification is reserved for behavior that genuinely depends on the user's actual MT4 broker/VPS environment, including:

- broker symbol names/suffixes and contract specifications;
- real spread, tick value/tick size, stop level, lot-step/min/max lot;
- live/demo broker price feed and history availability;
- broker trade permissions and execution response;
- slippage/requotes/latency and server-side order rules;
- actual OrderSend/OrderModify/OrderClose behavior;
- VPS/terminal restart and real-account recovery behavior;
- forward-test confirmation under the intended broker environment.

## Rule
Do not ask the user to repeat a check that GitHub CI can perform reliably. Ask for manual evidence only when the remaining verification depends on the real broker/VPS environment or when GitHub is technically unable to reproduce the required state.

## Current D1 track
- D1-01: native MetaEditor 0E0W verified on GitHub Windows runner.
- D1-02: implemented on `d1-owner-dev`; native MetaEditor 0E0W verified.
- MT4 Journal/Experts runtime-smoke CI has been added on `d1-owner-dev` and is being exercised separately from the frozen `blueprint-dev` candidate.
