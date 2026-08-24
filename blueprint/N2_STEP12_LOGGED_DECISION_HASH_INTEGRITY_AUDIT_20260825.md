# N2-12 — Logged Decision Hash Integrity Audit

Date: 2026-08-25  
Status: **PASS — observable synthetic research tooling gate**

GitHub Actions run: `32789964067`  
Workflow: `N2 NMJE Research Tooling PR Self-Test`  
Conclusion: **success**

N2-12 verifies that token-safe `[N2-NMJE-DEC]` DecisionID telemetry may carry `DIDH`, that the decoded DecisionID is hashed locally using the EA-compatible `SHORT_HASH` mirror, and that a logged hash mismatch is excluded from identity recovery and makes the reconciliation integrity state fail closed.

Scope: research/diagnostic only. This audit does not authorize nested execution gating or alter BBMA entry, SL/TP, risk or execution behavior.
