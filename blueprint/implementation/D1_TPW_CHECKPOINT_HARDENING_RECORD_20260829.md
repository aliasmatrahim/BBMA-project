# D1TPW Checkpoint Hardening Record — 2026-08-29

## Scope

This isolated downstream workstream hardens restart persistence while both
D1TPW and C044 remain disabled. It does not activate lifecycle execution or
change BBMA strategy semantics.

## Audit findings addressed

The prior checkpoint used eight independently written Global Variables and
treated key presence as completion. It had no version-last commit marker and
did not bind the checkpoint to pair, D1 opportunity cycle, or durable execution
identity. A torn or stale write therefore lacked a sufficiently strong
recovery proof.

Checkpoint v2 now:

- deletes the version marker before payload writes;
- checks every payload write;
- stores pair, D1 opportunity cycle, and execution hashes losslessly as 16-hex
  chunks;
- writes version `2` last as the commit marker;
- rejects pair/execution mismatch, missing cycle identity, invalid candle
  history, cursor reversal, and frozen-plus-latched impossible state;
- retains the existing M15 processing clock, D1 TP semantic owner, M23 close
  owner, M22 execution owner, hard SL, and fail-closed recovery behavior.

## Build identity

- Header: `Version 4.7.1 - D1TPW Restart-Safe Checkpoint Hardening`
- Property: `4.71`

## Verification evidence

- D1TPW static authority/checkpoint firewall: PASS
- deterministic restart/torn-write/identity-mismatch model: PASS
- N3 D1 epoch selftest: PASS
- N3 policy readiness, authority, identity, recovery, and replay: PASS
- NMJE v2 M5 lineage plus Stage A/B/C1/C2/D1/E1-E7: PASS
- Python test-harness compilation: PASS
- N3 static authority guard: PASS
- native MT4 MetaEditor: `0 errors, 0 warnings`, 379 ms
- compiled EX4: 598,284 bytes

## Non-authorization

`EnableD1TPWLifecycle=false` and `EnableC044Lifecycle=false` remain mandatory.
This record does not authorize merge, release, demo/live activation, C044,
or any trade-geometry/policy change.

