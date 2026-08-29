# MT4 VPS Runtime Testing Architecture — KIV

Status: **LOCKED DIRECTION / FUTURE RUNTIME SETUP / DO NOT IMPLEMENT YET**

## Recommended responsibility split

- **GitHub** = source of truth, version control, audit trail, static/regression checks, CI automation.
- **Native MT4 / MetaEditor** = authoritative compile and runtime environment.
- **VPS-hosted MT4** = preferred live/runtime validation environment because it can remain online 24/7 in a stable environment.
- **Laptop** = access/control/inspection terminal for the VPS, not the authoritative runtime host when VPS is available.

## Preferred future flow

`ChatGPT/code audit -> GitHub -> deploy/sync candidate -> native MT4 on VPS -> compile/runtime/live evidence -> audit results back into GitHub`

## Why VPS MT4 is preferred over laptop MT4 for live validation

VPS provides a more consistent runtime environment and is less affected by:
- laptop sleep/shutdown/restart;
- local internet interruptions;
- accidental closure of MT4;
- inconsistent local workstation use.

## GitHub boundary

GitHub must not be treated as a replacement for native MT4 runtime testing. GitHub workflows can perform source management, automation, repair scripts and static checks, but broker-dependent behaviour must be validated in native MT4.

Broker/runtime-only evidence includes, among others:
- genuine ticks;
- spread;
- broker symbol/digit/spec behaviour;
- OrderSend/execution results;
- slippage/requotes;
- SL/TP placement behaviour;
- restart/recovery and persisted execution identity;
- genuine BBMA signal-to-order lifecycle;
- long-running 24/5 state behaviour.

## Current constraint

Do not change the current runtime candidate solely to implement this infrastructure while an active runtime-validation cycle is still being attributed to that candidate build.

Future optional upgrade after runtime closure: structured telemetry/log bridge from VPS MT4 back to a reviewable storage/endpoint so runtime evidence can be audited with less manual screenshot collection.
