# CORE-FIDELITY-292 — CP14 Core §8 Re-Entry

Date: 2026-10-26. Phase: AUDIT / PARTIAL. Issue #292.
Branch: `audit/core-fidelity-20261021`; parent: `b6eb96d2f58cee094c1905f2092e2b96657b1ec2` (CP13).
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.
PR #293 remains open, draft and unmerged, with explicit DO NOT MERGE; Issue #292 remains open.

## VERIFIED
- Recovered branch roles from main governance/README, live queue/current state, Issue/PR and CP13. Active Task Orchestrator Contract: main@`00324e5c85f9b75894b21aabbdd313a9224e2ada`.
- Source chain reviewed: SOURCE_INDEX; accepted Core §8.1–8.6; PDF-derived index pp.9–10 and secondary pp.35–36; Finale V05/V06; forum provenance/digests; F3/F6; D1O-01; M12/M10/M11J/M13/M14/M15/M16/M27 contracts and exact Build 5.15 source. Raw PDF binaries were not reopened.
- M12 maps Type1 structural retrace/range; Type2 MA5/10+Mid-BB confluence for at least three candles; Type3 CSM then later MA5/MA50 retrace; Type4 CSD then later MA5/MA10 retrace. Shared close-side validation applies; no generic Type1–4 expiry. Type1 geometry and `IsNear < 2 points` remain engineering mappings.
- M27 updates closed D1/H4/H1/M15 owners. M13/M14 collect/validate exact REM/RRE/REE; M15 is final selection; M16 revalidates owner identity; M17/risk/M22 execute downstream.
- D1O-01 consumes D1 `EntryCandle` as `ActivationTime` and requires fresh LTF RE readiness strictly after activation. F6 unused-by-eligibility statement was overbroad; this is not a general order timer or extra ordinary-entry wait.
- Empty M12 owner starts Type3→Type4→Type2 before Type1. Reviewed sources do not specify overlap precedence; code does not prove mutual exclusion. Marked UNRESOLVED; no trading rule or EA code changed.

## PARTIAL / NOT VERIFIED
- Build 5.15 stale-source admission remains; Build 5.22 all-component freshness candidate is still unmerged.
- G40 is online; no active RDC/MetaTrader/MetaEditor/Tester process in latest snapshot. Qualified history remains NOT VERIFIED; Strategy Tester NOT RUN.
- No CP14 test, native compile, Tester, broker runtime or order trace ran. Full rule-to-runtime denominator remains PARTIAL.

## Changed
- Corrected F6 timing audit and Finale index; documented M12 overlap hold; updated fidelity matrix, cross-module ledger, gap register, CURRENT and MASTER_QUEUE; added this checkpoint. No EA source changed.

## Exact next action
- Resolve Type2/3/4 overlap policy with authoritative evidence or explicit project decision before M12 arbitration changes. Keep Core §9 queued; do not merge PR #293 or start Tester without qualified G40 history.
