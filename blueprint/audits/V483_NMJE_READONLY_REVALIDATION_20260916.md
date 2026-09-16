# Build 4.83 NMJE Read-Only Revalidation â€” 2026-09-16

Issue: #141  
PR: #142  
Branch: `fix/nmje-readonly-authority-141`  
Current owner base synced: `e2c1a35743e6251f8ee499870aad248e43adb06b`

## Root cause
Canonical owner v4.61 still routes `NESTED_CONFLICT` / `NESTED_BUILDING` through `NMJE_PassExecutionGate()` inside entry preflight, allowing M12N observation state to reject an M15/M16-valid decision. This conflicts with the active read-only M12N/N3 boundary.

## TDD evidence
The existing focused test was run against the exact owner source before restoring the fix:
- RED: 3 failures / 1 pass; failures prove the owner still contains the NMJE gate and v4.61 identity.
- GREEN on Build 4.83: 4 passed.
- N3 activation-firewall self-test: PASS.

No replacement NMJE trading rule, score or filter is introduced.
## Native compile revalidation
MetaEditor: `C:\Program Files (x86)\MetaTrader 4\metaeditor.exe`

Exact synced source compile result:
- 0 errors;
- 0 warnings;
- 744 msec elapsed;
- MQ4 SHA-256 `FC6DEF0B225F473DDF81E5A3B027546256C8D76D462D1F6AC9230586A556D087`;
- EX4 SHA-256 `D91235BDBD9BB8966AB36E39ABC497256C4BEAE8CA5C29B6A248F931C7CD2845`.

The fresh compiler log is `blueprint/audits/V483_METAEDITOR_COMPILE_20260916_REVALIDATION.log`.

## Scope/result
Static authority fix remains limited to removing the NMJE execution rejection path while preserving N1/N2 observation telemetry. D1/M15/M16/M17/risk/execution semantics are otherwise unchanged by this repair.

Runtime status: **NOT RUNTIME VERIFIED on the 2026-09-16 synced candidate**. No primary MT4 restart or trading activation was performed.

