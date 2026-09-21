# D1O Build 5.03 EXTREME_TPW Same-Identity Enrichment Recovery Validation

Date: 2026-09-21
Issue: #214
Recovered from stale Draft PR: #215 at `7e8f819566f972a99a207cdd9849fbe770d26a3e`
Branch: `fix/d1o-extreme-tpw-current-owner-214`
Only base: `d1-owner-dev@e6ff0beff00af239964494d65ae19c831376d9a7` (after PR #221)
Status: **VERIFIED FOR OWNER INTEGRATION / NOT ACTIVATED**

## Recovery and decision authority

The verified scoped implementation and decision record from stale PR #215 were reused.
No fresh implementation was invented and stale compile/runtime outputs were not treated as current evidence.

User-approved Option A remains exact:

- a valid standalone H1 Re-Entry and `D1_OPP_EXTREME_TPW` overlap sharing the same canonical H1 identity remain one executable identity;
- H1 owns entry, deduplication, and hard-SL;
- EXTREME_TPW owns TP and D1 TP-Wajib lifecycle attribution;
- there is no generic D1 Opportunity precedence;
- there is no second DecisionID, SequenceHash, ticket, or order;
- M15 remains final new-entry authority;
- the D1TPW gate remains unchanged and fail-closed.

Decision record:
`blueprint/decisions/D1O_EXTREME_TPW_SAME_IDENTITY_PRECEDENCE_DECISION_20260920.md`

## Current-owner integration

Build identity:

- `5.03`
- `V503_D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_20260921`
- `D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_214_20260921`

The executable semantic delta is limited to the canonical comparator and its exact-overlap predicate.
The tie-break applies only when both candidates have the same Re-Entry type, valid direction,
non-empty SequenceHash, canonical anchor, SequenceStartTime, and embedded H1 Re-Entry identity,
with one standalone and the other specifically `D1_OPP_EXTREME_TPW`.

Different identities retain existing recency/hash ordering. Other D1 Opportunity families receive no priority.

Current-owner protected-body comparison is byte-exact for the M15/M16 ownership path, M19 risk aggregation,
D1TPW checkpoint/generation handling, C044 checkpoint restore, M17 SL/TP selection, M22 send/dedup,
and M24 recovery. This preserves M19, D1TPW, and C044.

Two stale test-only global build pins were removed from C044/Q5 guards.
Their substantive feature-body assertions remain; this restores compatibility with post-4.86/post-5.02 builds.

## Deterministic and static verification

- D1O same-identity precedence model: **PASS**
- D1O scoped source/static guard: **PASS**
- D1O execution identity contract: **PASS**
- D1O canonical dedup analyzer: **PASS**
- M19 model/static guards: **PASS**

- D1TPW generation/checkpoint guards: **PASS**
- C044 generation/recovery/static guards: **PASS**
- F7 source guard: **PASS**
- current-owner protected-body comparison: **PASS**
- `git diff --check`: **PASS**
- full pytest suite: **22 passed**

## Native compile

Canonical source:

- source equals compile input: **byte-exact**
- MetaEditor: **0 errors / 0 warnings**
- MQ4 SHA-256: `FABBB87A8D1AC0F8A3E924A15D98E078D8BDED12C55809AE9F1A062EC70A33F5`
- EX4 SHA-256: `2FB71DD42CDC6023AC6C828B91962D66FCBBE7B93E668F14F23BD70CC36EF1A4`

Tester adapter:

- exact three environment-only transforms: **PASS**
- MetaEditor: **0 errors / 0 warnings**
- MQ4 SHA-256: `A0737B3DE56A88FCC581FBED3D7EAA4DE44163BA2A9ECC10845739EBE7A7B504`
- EX4 SHA-256: `A679029434EBCB0734A6C313550D1BA724A79B81355A6590B68DD64A82F2E002`

## Isolated offline MT4 regression

Profile: GBPUSD engineering profile, M15, 2026-08-01 through 2026-09-01, Every Tick.
Baseline: exact current-owner Build 5.02 C044 smoke evidence from 2026-09-21.

Build 5.03 versus current-owner Build 5.02:

- total trades: 14 / 14
- M15_COUNTS: 523 / 523 exact
- M15_SELECT: 523 / 523 exact
- M16_PASS: 523 / 523 exact
- DECISION_FINAL: 523 / 523 exact
- EXEC: 14 / 14 exact
- C044 MOMENTUM_HOLD: 3 / 3 exact
- C044 EXIT_LATCHED: 10 / 10 exact
- C044 CLOSE_SUCCESS: 10 / 10 exact
- targeted fatal runtime faults: 0

Natural EXTREME_TPW occurrence remained 0. This proves no regression outside the exact overlap;
the overlap itself is proven by the deterministic model and static source guard, not by a claimed natural runtime occurrence.

OfflineDiag Global Variables changed during smoke and were restored byte-for-byte:

- pre/final SHA-256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`
- post-smoke-before-restore SHA-256: `02188D2932F58AE24F81BDE6AFEDBE423BF3DE83A88778BBC3866E10C0578E2B`
- exact restore: **PASS**
- isolated terminal left running: **NO**

Existing MT4 PID 13064 on the separate C10 path was not restarted, stopped, or modified.

## Runtime and activation boundary

No broker live/demo runtime was run. No primary MT4 restart and no production trading activation occurred.
Those activities remain in the final Q queue.

## Exit result

**Issue #214 current-owner recovery exit criteria: VERIFIED.**
