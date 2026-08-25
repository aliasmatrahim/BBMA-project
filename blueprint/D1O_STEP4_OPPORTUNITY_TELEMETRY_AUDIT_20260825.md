# D1O-04 — Opportunity Telemetry Research Self-Test Audit

Date: 2026-08-25  
Status: **PASS**

GitHub Actions run: `32793706566`  
Workflow: `N2 NMJE Research Tooling PR Self-Test`

The full N2/D1O synthetic research suite passed after adding optional validated-decision telemetry fields:

- `AUTH` — strategic vs D1 Opportunity authority;
- `OFAM` — D1 Opportunity family;
- `OC` — D1 Opportunity CycleID.

Outcome attribution can now report separately by D1 authority and opportunity family while retaining exact DecisionID joins and existing fail-closed identity reconciliation. This tooling does not alter EA trading behavior.