# CORE-FIDELITY-292 — CP15 Primary PDF Re-Entry Arbitration Check

Date: 2026-10-27. Phase: SOURCE VERIFICATION / PARTIAL. Issue #292.
Branch: `audit/core-fidelity-20261021`; parent: `186ba6fecbebad571d062bb4929966056a652283` (CP14).
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.
PR #293 remains open, draft, unmerged, and explicitly DO NOT MERGE; Issue #292 remains open.

## VERIFIED
- Inspected supplied primary PDF pages 9–10 as extracted text and rendered images. SHA-256 `3e6065dd97c20951bd8af96bc81b81ca138800184be6fc4740a32aa4ab0a9c9c` matches the primary artifact hash in SOURCE_INDEX.
- Page 10 lists Type2 (MA5/10 + Mid-BB; minimum three candles), Type3 (CSM then MA5/MA50 retrace), and Type4 (CSD then MA5/10 retrace) individually. It states no overlap precedence, tie-break or mutual exclusivity. Page 9 defines Type1 rise/fall and ranging; it does not arbitrate Types 2–4.
- Existing Build 5.15 M12 empty-owner order remains Type3→Type4→Type2→Type1. This is implementation behavior, not a PDF rule. No source evidence resolves the project policy.
- M12 contract, source fidelity matrix, cross-module ledger, gap register, CURRENT, MASTER_QUEUE and Finale index updated to record direct-source result. No EA code changed.

## PARTIAL / NOT VERIFIED
- M12 overlap policy requires an explicit project decision: keep current order, fail closed, or retain separate owners for M15 evaluation.
- Qualified G40 history remains NOT VERIFIED; Strategy Tester NOT RUN. No test, compile, runtime or order trace ran in CP15.

## Exact next action
- Await policy decision before changing M12 arbitration; keep Core §9 queued and PR #293 draft/unmerged.
