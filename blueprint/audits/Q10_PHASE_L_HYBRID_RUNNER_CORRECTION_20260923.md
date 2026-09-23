# Q10 Phase-L Hybrid Runner Correction — Build 5.11 — 2026-09-23

Issue: #109  
Owner baseline: `d1-owner-dev@5be9ad6e18d49ea465cfe31957f3874a62e6ceeb`  
Scoped branch: `fix/q10-phase-l-hybrid-live-109`  
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Classification

**CONFIRMED BUG / ACCEPTANCE TOOLING**

No EA source or Strategy-Core behavior change.

## Issue

After PR #255 integrated the reconciled hybrid Phase-H state, the policy correctly allowed Phase L with:
- 56 PASS;
- 1 conditional INCOMPLETE (R5-19);
- 0 FAIL;
- no HOLD.

However, `q10_demo_acceptance.py` still analyzed live stages against the full stage matrix. That old behavior required historical-only cases to PASS again on MetaQuotes-Demo, contradicting `FINAL_BUILD511_HYBRID_EVIDENCE_POLICY.json`, whose final live phase requires:
- mandatory `live_only_cases`;
- mandatory `live_reconfirm_cases`;
- no repeated requirement for historical-only cases.

This would have incorrectly kept R3 blocked by rare historical cases already satisfied by Phase H.

## Fix

The Q10 runner now:
1. validates the hybrid policy against the stage matrix;
2. initializes a fresh `BBMA_Q10_STATE_V2` for `LIVE_RECONFIRM` only after Phase-H eligibility is proven;
3. re-verifies exact candidate source/build, native EX4, settings, dedicated terminal and authenticated MetaQuotes-Demo evidence;
4. analyzes Phase-L assertions using only mandatory `live_only + live_reconfirm` cases;
5. preserves conditional matrix cases as optional;
6. treats any observed FAIL, including an optional case, as stage FAIL;
7. rejects recording a non-`LIVE_RECONFIRM` analysis into a Phase-L state;
8. preserves formal `R3 -> R4 -> R5 -> R6` ordering.

## Conditional-case correction

`R6-09` is live-only but conditional / `required=false`. The corrected runner does not promote it into a mandatory Phase-L blocker.

## Validation

Exact scoped branch:
- Q10 targeted pytest: **19 passed**;
- full repository pytest: **63 passed**;
- `git diff --check`: PASS;
- EA source diff from owner baseline: **0**.

Actual G40 Phase-L dry-run:
- prior MetaQuotes-Demo AUTH state: PASS;
- Phase-H V4: 56 PASS / 1 conditional INCOMPLETE / 0 FAIL;
- exact Build 5.11 candidate: PASS;
- exact native EX4/settings binding: PASS;
- generated state schema: `BBMA_Q10_STATE_V2`;
- phase: `LIVE_RECONFIRM`;
- next formal stage: `R3`.

Existing authenticated R3 bundle re-analysis under corrected semantics:
- mandatory live R3 set: `R3-00, R3-02, R3-04, R3-05, R3-12, R3-15`;
- PASS from existing attributable evidence: R3-00, R3-02, R3-04, R3-05, R3-15;
- remaining live blocker: **R3-12** restart continuity;
- historical-only R3 cases are correctly non-mandatory in Phase L.

## Runtime boundary

This correction does not itself claim R3 PASS. A fresh attributable MetaQuotes-Demo R3 run/restart sequence is still required to close R3-12.

Primary/Q3 MT4 remains separate and must not be touched.

## Final result

**TOOLING FIX VERIFIED.**

Phase L can proceed against the accepted hybrid evidence contract without recreating historical-only scenarios live.

## Same-day run-boundary hardening

A fresh Phase-L launch exposed a second acceptance-tooling provenance gap: the legacy collector could read an entire daily MQL4 log. On a day containing an earlier R3 run, this could mix old and fresh stage markers or leave bundle hashes dependent on a live file that continued to grow.

The collector is now run-bounded when `--start-marker` is supplied:
- the last matching launch marker is authoritative for the new run boundary;
- lines before that marker are excluded;
- the selected run is copied to an immutable `<stage>_runtime.log` snapshot under the evidence bundle;
- bundle SHA validation uses that snapshot, not the still-growing terminal daily log;
- source daily-log path/hash-at-collection and start-line provenance are retained;
- a missing requested marker fails closed.

Targeted regression after this hardening: **21 passed** before final full-suite validation.

This remains Q10 acceptance-tooling only. EA source/runtime semantics are unchanged.
