# D1O Step 9 — Canonical Dedup Analyzer Self-Test

Date: 2026-08-25
Branch: `d1-owner-dev`

Status: **PASS**

The D1O-09 runtime-log analyzer is aligned with D1O-07 execution identity semantics:
- reuse of one canonical execution hash across D1 CycleID/family attribution changes is diagnostic/expected when the LTF identity is unchanged;
- the same execution hash changing direction is an integrity failure;
- D1 opportunity decisions missing OSH are an integrity failure;
- family/cycle attribution consistency remains independently checked.

Synthetic self-test includes both an expected cross-attribution reuse case and a forbidden same-hash/opposite-direction case.
