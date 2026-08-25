# N3 NMJE Execution Intelligence Staging Contract

Date: 2026-08-26
Status: **STAGING CONTRACT — TECHNICAL POLICY-READINESS ONLY / EXECUTION INACTIVE**

## Purpose
N3 is the boundary between N2 descriptive research and any future optional use of NMJE in trade selection. Its technical responsibility is to decide whether an N2 evidence bundle is sufficiently intact to be presented for a separate strategy-policy review.

N3 does **not** decide that `ALIGNED` is better, that `CONFLICT` must be rejected, or that any nested relation has a trading edge.

## Hard activation firewall
N3 execution activation requires all of the following, in order:
1. real broker-connected forward evidence from N2, not synthetic fixtures alone;
2. valid DecisionID / execution-hash / pair identity reconciliation;
3. observed outcome coverage and uncertainty visible in the evidence bundle;
4. relation/signal evidence reviewed without hiding small or uncertain buckets;
5. a separate explicit strategy decision naming the exact proposed execution behavior;
6. a protected-surface implementation review and native MT4 0-error/0-warning gate after that decision.

Until those conditions are met, execution status is always:

`INACTIVE — NO NMJE EXECUTION POLICY`

## What N3 may do now
N3 may:
- read N2 `evidence.json`;
- read N2 identity/reconciliation summaries;
- expose evidence completeness and integrity;
- surface Wilson-interval uncertainty already computed by N2;
- identify missing relation buckets or missing decisive outcomes;
- report `EVIDENCE_COLLECTION`, `IDENTITY_BLOCKED`, or `REVIEW_READY`;
- produce a machine-readable review packet.

`REVIEW_READY` means only that the evidence is fit for human/strategy review. It never means a policy is approved.

## What N3 may never do without a later approved strategy decision
N3 may not:
- reject `NESTED_CONFLICT`;
- prefer or boost `NESTED_ALIGNED`;
- require `NESTED_SUPPORTING`;
- suppress `NESTED_BUILDING`;
- convert `NESTED_UNRESOLVED` into a trade permission;
- add a numeric nested score, confidence %, voting system or timeframe weights;
- change EntryMode;
- change D1 strategic owner or D1 Opportunity authority;
- change REM/RRE/REE composition or priority;
- change M15 candidate construction/selection;
- change M16 revalidation;
- change M17 SL/TP, M19/M20 protection, M21 sizing, M22 execution or M23/M24 lifecycle/recovery;
- create additional entries from nested sub-cycles;
- automatically write or patch EA source from research output.

## Evidence-readiness semantics
N3 must not invent a minimum sample size as a BBMA rule.

### `IDENTITY_BLOCKED`
Use when the N2 evidence says identity integrity is invalid or attribution cannot be trusted.

### `EVIDENCE_COLLECTION`
Use when identity is valid but the observed sample is incomplete, has no attributed closed outcomes, or otherwise still represents collection rather than a complete observed bundle.

### `REVIEW_READY`
May be used only when:
- N2 data status is `COMPLETE_OBSERVED_SAMPLE`;
- identity is valid for attribution;
- at least one correlated decision and one attributed closed outcome exist;
- evidence remains explicitly marked descriptive-only;
- uncertainty/bucket counts remain visible.

This is a data-readiness state, not a trade signal and not proof of an edge.

## Policy field
Every N3 staging report produced before a separate approved strategy decision must contain:
- `execution_policy = NONE`;
- `automatic_policy_authorized = false`;
- `source_modification_authorized = false`;
- `activation_authorized = false`.

No statistical pattern may flip those fields automatically.

## Synthetic evidence boundary
Synthetic/self-test fixtures may prove:
- parser correctness;
- state classification;
- fail-closed behavior;
- output stability.

Synthetic evidence can never make N3 `activation_authorized=true` and can never establish a trading edge.

## Future activation package
If real N2 evidence later supports a policy proposal, create a new dated decision containing at minimum:
- evidence dataset identity/time window;
- relation/signal buckets considered;
- coverage and uncertainty;
- exact proposed behavior;
- affected EntryMode(s)/signal families, if any;
- fail-closed behavior;
- rollback plan;
- native compile/static regression plan;
- broker forward validation plan.

That future decision is a strategy semantic change and requires explicit user approval before implementation or activation.

## Final N3 invariant
`N3 MAY DECLARE DATA READY FOR REVIEW; N3 MAY NOT DECLARE A TRADING POLICY ACTIVE.`
