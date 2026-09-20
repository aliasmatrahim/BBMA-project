# D1O Build 4.98 EXTREME_TPW Same-Identity Enrichment Validation

Date: 2026-09-20
Issue: #214
Branch: `fix/d1o-extreme-tpw-same-identity-precedence-214`
Base: `d1-owner-dev@8da9dae0801f414f8d4c659a226ff58451cca7e6`
Status: **VERIFIED IN SCOPED DRAFT BRANCH / NOT MERGED / NOT ACTIVATED**

## Decision authority

User selected Option A on 2026-09-20.

Exact same canonical H1 Re-Entry identity shared by:
- otherwise-valid standalone H1 Re-Entry; and
- otherwise-valid `D1_OPP_EXTREME_TPW`

is one executable identity with EXTREME_TPW attribution/lifecycle enrichment.

H1 remains entry/dedup/hard-SL owner. D1 Extreme owns TP semantics and D1 TP-Wajib owns normal lifecycle exit semantics for that exact overlap.

This is not generic D1 Opportunity precedence.

Decision record:
`blueprint/decisions/D1O_EXTREME_TPW_SAME_IDENTITY_PRECEDENCE_DECISION_20260920.md`

## Implementation

Build:
- `4.98`
- `V498_D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_20260920`
- `D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_214_20260920`

The only executable semantic delta is in M15 canonical candidate ordering:
- exact Re-Entry signal type;
- same valid BUY/SELL direction;
- same non-empty SequenceHash;
- same canonical anchor;
- same SequenceStartTime;
- both candidates contain the same H1 Re-Entry identity at that anchor;
- one candidate is standalone;
- the other is specifically `D1_OPP_EXTREME_TPW`.

Only then does EXTREME_TPW attribution win the tie.

Different identities retain existing recency/hash ordering. Other D1 Opportunity families receive no new priority.

No second SequenceHash or DecisionID is created.

## TDD / static validation

Pre-change static test against Build 4.86 failed at the expected missing Build 4.98 / precedence implementation marker.

Post-change:
- same-identity precedence model: **PASS**;
- scoped source/static guard: **PASS**;
- existing D1O execution identity contract guard: **PASS**;
- existing D1O canonical dedup analyzer self-test: **PASS**;
- existing F7 source guards: **PASS**;
- `git diff --check`: **PASS**.

Build 4.86 -> 4.98 protected bodies are byte-exact for:
- `GenerateDecisionID()`;
- executed-decision lookup;
- standalone Re-Entry candidate construction;
- D1 Opportunity candidate construction;
- candidate anchor;
- SL/TP source component resolution;
- D1 Opportunity authority readiness/freeze;
- `PriorityEngine_Atomic()`;
- M16 D1 Opportunity revalidation;
- D1TPW and F7 lifecycle identity;
- M17 SL/TP resolution;
- risk preflight;
- M22 existing-ticket lookup and send/retry;
- M24 recovery.

Only the canonical comparator plus the new exact-overlap helper changed.

Q9 P11 compatibility check: pre-patch `CompareCanonicalCandidates()` is byte-identical between owner Build 4.86 and scoped Q9 P11 Build 4.96, so this fix has no pre-existing comparator semantic conflict with Q9.

## Native compile

Canonical:
- MetaEditor: **0 errors / 0 warnings**
- MQ4 SHA-256: `67B1D8861E013C7DFDD2579C3CFD5AD1431439027B6DCC8CC3A49651FD883ADF`
- EX4 SHA-256: `5F157D9BE81430238818BAAF13C978EF6F80D17B8BFC88A39F1C790879862413`

Tester adapter:
- exact three environment-only transform: **PASS**
- MetaEditor: **0 errors / 0 warnings**
- MQ4 SHA-256: `CDA6E020637BE49B14CD3A8C50493C4A64593BC2F498624FE627E047DF2D454A`
- EX4 SHA-256: `2896F482F3D6443E6CE4999E8213F3AE7B27C8F61F3AEDB778E433DE08E5CCCE`

## Targeted offline runtime regression

Profile: verified GBPUSD engineering profile, M15, 2026-08-01 through 2026-09-01, Every Tick.

Build 4.98 vs verified Build 4.86 baseline:
- total trades: 14 / 14;
- M15_COUNTS: 523 / 523 exact;
- M15_SELECT: 523 / 523 exact;
- M16_PASS: 523 / 523 exact;
- DECISION_FINAL: 523 / 523 exact;
- EXEC: 14 / 14 exact;
- C044 MOMENTUM_HOLD: 3 / 3 exact;
- C044 EXIT_LATCHED: 10 / 10 exact;
- C044 CLOSE_SUCCESS: 10 / 10 exact;
- targeted fatal runtime faults: 0.

Natural EXTREME_TPW strategy occurrence in this smoke remains 0, so this runtime evidence proves no regression outside the new exact overlap; it does not claim live/natural overlap execution proof.

OfflineDiag GlobalVariables were restored exactly after the smoke:
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.

Q3 isolated C10 terminal PID 13064 was not restarted or modified.

## Runtime / activation boundary

The exact same-identity EXTREME_TPW overlap is deterministic-model + source-guard verified. The retained GBPUSD historical smoke does not naturally produce that overlap.

The D1TPW feature gate remains unchanged. While OFF, a selected enriched EXTREME_TPW decision must continue to fail closed through existing M17/D1TPW gating. No static outer-BB/C044 fallback is authorized.

No production activation is authorized by this scoped validation.

## Exit result

**Issue #214 scoped implementation exit criteria: VERIFIED.**

Draft PR only. No merge or production activation.
