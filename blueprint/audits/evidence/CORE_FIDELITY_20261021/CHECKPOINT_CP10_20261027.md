# CORE-FIDELITY-292 — CP10 Core §4 BB-state / Momentum trace
Date: 2026-10-27. Phase: AUDIT / PARTIAL. Issue #292.
Branch: `audit/core-fidelity-20261021`; parent: `1215e9622cd2768f41bc538b9578470e5a71ee5f`.
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15. Candidate: Build 5.22 / PR #293.

## VERIFIED
- Routed Core §4 through SOURCE_INDEX, accepted Core, source rule index, primary/secondary page map and Finale V02 timestamped rules; no source rule or strategy code changed.
- Added M07 ownership/shape contract. M07 output is auxiliary and currently has no downstream reader; M10 CSM does not consume BB-state enums.
- M10 `DetectCSM` → M12 Type-3/direction-owner path is present. M08 Extreme lifecycle checks a local CSM-equivalent predicate before maturity promotion; it does not directly call M10.
- Updated the incremental matrix, cross-module ledger and stale M08/M10 contract text to preserve direct-call vs equivalent-formula distinction.

## PARTIAL / NOT VERIFIED
- Focused M07 or M08/M10 parity tests and attributable runtime remain NOT VERIFIED; none were run in CP10.
- M07's legacy 0.9/1.1 labels can classify modest widening as CONTRACTING, but they are currently write-only and not an entry gate.
- Full accepted-Core denominator, nested-field ownership and runtime matrix remain PARTIAL. Qualified G40 history remains NOT VERIFIED; Strategy Tester remains NOT RUN.
- Owner/production branch unchanged; PR #293 remains draft/unmerged.

## Modified files
M07 contract; M08/M10 contracts; source-fidelity matrix; Build 5.15 cross-module ledger; CURRENT; MASTER_QUEUE; this checkpoint.

## Exact next action
Continue accepted Core §5 Extreme lifecycle mapping across M06/M08/M09/M11J/M13/M15/M16; preserve source HOLD boundaries and keep tester gated on qualified-history evidence.
