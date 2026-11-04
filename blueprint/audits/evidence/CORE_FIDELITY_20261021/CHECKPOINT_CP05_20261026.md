# CORE-FIDELITY-292 — CP05 static module/data connection inventory
Date: 2026-10-26. Phase: AUDIT / PARTIAL. Issue #292.
Branch: audit/core-fidelity-20261021; parent checkpoint: d82a5abd7a9d4c5e98613407c6362309c8287c48.
Owner source: d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de, Build 5.15.
Checkpoint SHA: commit adding this file; exact SHA is recorded in Draft PR #293.

## VERIFIED static boundary
- Scanned the pinned source: 29 module headers including the previously omitted M11J; 431 function definitions detected.
- Recorded 96 cross-module direct-call edges / 364 caller-callee pairs, 23 M01 input fields, 68 M01/M02 type declarations and 37 M03 global identifiers in the machine-readable graph.
- Added M11J to module and regression maps; mapped it to the approved D1O-01 project execution decision, and added the D1O-01 route to SOURCE_INDEX.
- BlockNMJEConflict and BlockNMJEBuilding have no code readers; M01 explicitly marks both inactive legacy compatibility inputs because NMJE is observation-only.
- Added M11 and M11J D1 owner-field handoffs to the connection ledger. No BBMA rule or EA code changed.

## PARTIAL / NOT TESTED
- Static identifier references do not classify every nested-field read/write owner or variable alias; consumer-edge coverage remains PARTIAL.
- M11J has no module-specific regression assignment in the current map; D1O runtime is NOT VERIFIED.
- M12 stale-owner admission remains VERIFICATION REQUIRED. The next action is an end-to-end unreadable H1/H4 refresh reproduction.
- Full accepted-Core denominator, source provenance, combined regression, qualified G40 data and runtime coverage remain PARTIAL / NOT VERIFIED.
- No tests, compile, Strategy Tester, orders, exits or restart run were performed for CP05. Active owner still contains confirmed M06 defect; candidate repair remains only in Draft PR #293.

## Related draft
Machine-readable static-map reconciliation: Draft PR #294, separately based on main.

## Exact next action
Reproduce unreadable H1/H4 refresh through candidate construction -> M15 admission -> M16 revalidation -> M17/risk/portfolio preflight. Classify before any M12 change; preserve structural owner lifetime and current fail-closed contracts.