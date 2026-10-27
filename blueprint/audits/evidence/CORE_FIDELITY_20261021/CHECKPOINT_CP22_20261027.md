# CP22 — Cross-module reference identity and mutation map

Date: 2026-10-27  
Task: Issue #292 / Draft PR #293  
Phase: **VALIDATION — STATIC AUDIT RECORDED; OWNERSHIP PARTIAL**

## Authority and artifacts
- Audit branch: `audit/core-fidelity-20261021`; branch head before this checkpoint package: `2a01b5bc44fa78cb7f86e7188322460d05c397d8`.
- Exact owner source: Build 5.15, `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, source blob `09de8b80fdaeeb2fd614de0a1826134e9a8b2411`.
- Accepted root graph stays pinned at `23def0919386263007ead1898b94637cc17f7f36`; the current-owner overlay stays separate.
- PR #296 merged at `7fb1cfdbb0fb2d7e30fe75e382e176199199416f`; deterministic-tooling passed for head `fe021e2b424b1e2866fe328be618f0de86a28e3a`.
- Machine inventory: `config/bbma_reference_identity_inventory_build515.json`, blob `a4a159631e6021598a000d454abca9b5f9979ab1`.

## Verified static result
- Parser reconfirmed 431 functions, 1,478 calls, 502 cross-module call occurrences, 96 module edges and 364 function pairs.
- 317 cross-module struct-by-reference callsites resolve to 90 global subobjects, 69 forwarded references (51 whole-param / 18 nested-member), 151 local objects and 7 local copies.
- Propagation records 344 origin associations and 0 unresolved/unbound/cyclic rows. Nineteen callsites retain multiple context-insensitive origins.
- Write tracing finds 122 parameter write paths and 195 with no detected parameter write path. All 317 target signatures are mutable; no-write detection is not a read-only guarantee.
- M27 passes canonical PairState subobjects to producer paths; M16 D1 snapshot validators use a local PairState copy; C044 replay can use local counterfactual or monitored TradeInfo state. Ownership remains PARTIAL_CONTEXT_INSENSITIVE.

## State, limits and next action
- No EA/Core source, tests, compile, Strategy Tester, broker runtime, terminal restart or trading activation changed/ran in CP22.
- G40 is online in the device registry; process/terminal and qualified history are not verified here. Strategy Tester remains NOT RUN.
- Last Q10 R5 live-state artifact is dated 2026-09-24: R5-14/R5-16 remain natural-event blockers, R6 is not promoted, and PID 2336 was running at that checkpoint; current process state is NOT VERIFIED.
- Next local task: inspect exact callee bodies behind the 195 no-detected-write parameters and prove a minimal read-only candidate set. Any `const` source change requires exact-candidate native strict compile on G40. Keep Q10 R5/R6 gates unchanged.
