# CORE-FIDELITY-292 — CP17 Core §9 MTF Hierarchy Audit

Date: 2026-10-27. Phase: STATIC MAPPING / PARTIAL / USER POLICY GATE. Issue #292.
Branch: audit/core-fidelity-20261021; parent CP16: 0b337b837bf31f82ac5656f5c7ae81c29bee495b.
Owner: d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de, Build 5.15.
Accepted Core blob at main: 3c450d7157db6b7a6bf53549f645bb75c88371e5.
PR #293 remains open, draft, unmerged and explicitly DO NOT MERGE.

## VERIFIED — static only
- M27 closed D1/H4/H1/M15 snapshots → M11 D1 and recovered H4 owner → M06–M12 owners → M12N read-only MTF observer → M13/M14 exact signatures → M15 D1/H4 final gates → M16 frozen-identity revalidation → M17/preflight.
- M11 confirmed D1 logic uses closed Close1 and current/previous closed MA50; missing/invalid inputs become unresolved, and unconfirmed values become transition.
- Standalone H1 Re-Entry requires active same-direction H4 and confirmed same-direction D1. H4 recovery fails closed without verified checkpoint/replay provenance.
- M5 is shadow-only; no M1 execution path is approved. M12N cannot create/reject/rank or affect M15 selection.
- D1O-01 permits D1_OPP_EXTREME_TPW to oppose the strategic owner with aligned H4 and fresh H1 prerequisites, but does not explicitly settle D1_TRANSITION.

## HOLD / NOT RUN
- Build 5.15 M15 special-cases D1_OPP_EXTREME_TPW and admits valid D1_TRANSITION because it rejects only D1_OWNER_UNRESOLVED. Core §9.2 and M15 contract say transition blocks all new entries.
- EnableD1TPWLifecycle is false; M17 ResolveApprovedInitialSLTP rejects this identity before downstream risk/order execution. The mismatch is currently non-executable but remains a policy gate.
- No tests, compile, Strategy Tester, broker/runtime or order trace ran. Qualified G40 history remains NOT VERIFIED.

## Exact next action
- Ask whether D1_TRANSITION blocks D1_OPP_EXTREME_TPW or whether this family is an explicit project-only exception to Core §9.2. Keep the D1 TPW gate OFF until this decision and the separate lifecycle runtime gates are satisfied.
