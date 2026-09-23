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

## Multi-run stage aggregation hardening

Phase-L R3 demonstrates that one formal stage may require several independently attributable runs: ordinary authenticated runtime for R3-00/R3-02/R3-05/R3-15, a controlled missing-D1-history run for R3-04, and a future natural D1O restart run for R3-12. The prior analyzer accepted only one stage bundle, so a correct final PASS could not combine those independent evidence sources without an unsafe manual log merge.

The runner now supports `BBMA_Q10_STAGE_BUNDLE_SET_V1` and `combine-bundles`:
- each component bundle must independently pass integrity validation;
- component bundle JSON is SHA-bound in the set;
- stage, candidate source/build and demo-auth identity must match across every component;
- case evidence may reference only raw/excerpt files registered by one of the validated component bundles;
- component tampering, identity mismatch or conflicting evidence hashes fail closed.

Validation on scoped branch:
- Q10 targeted pytest: **24 passed**;
- full repository pytest: **68 passed** before final documentation-only commit;
- EA source diff: zero.

Actual Phase-L R3 bundle set combines three bounded runs:
1. fresh ordinary R3 run;
2. second ordinary run spanning M15 18:15 for R3-15;
3. controlled missing-D1-history run for R3-04.

Combined LIVE_RECONFIRM result:
- PASS: R3-00, R3-02, R3-04, R3-05, R3-15;
- INCOMPLETE: **R3-12 only** among mandatory live cases;
- no FAIL observed.

R3-04 controlled environment evidence:
- dedicated `GBPUSD1440.hst` was backed up before removal;
- missing D1 history produced `D1_OWNER_UNRESOLVED / DIR_NONE` with no execution decision;
- regenerated broker history was preserved separately;
- original D1 HST was restored byte-identically to SHA-256 `1FD3090A87940252B2B2175136FDB85FA6769B9F9CBA5F1F7BCC6CBE04284C6F`;
- primary Q3 terminal remained untouched.

R3-12 remains a genuine live gate: it requires restart while an actual D1O-origin trade/identity remains relevant. No D1O trade/identity has occurred in current Phase-L runs, so it must not be fabricated or promoted from tester/static evidence.
