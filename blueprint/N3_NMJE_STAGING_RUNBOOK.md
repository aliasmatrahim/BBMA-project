# N3 NMJE Staging Runbook

Date: 2026-08-26
Status: **ACTIVE STAGING RUNBOOK / EXECUTION INACTIVE**

## Objective
Convert an N2 evidence bundle into a policy-review readiness report without allowing research output to change EA trading behavior.

## Inputs
Primary input:
- N2 `evidence.json` produced by `blueprint/tools/n2_nmje_auto_research_pipeline.py` or the equivalent N2 research pipeline.

The N2 bundle must remain traceable to its MT4 log/outcome dataset. Synthetic fixtures may be used for tooling self-tests only.

## Command
From repository root:

```bash
python blueprint/tools/n3_nmje_policy_readiness.py <n2-evidence.json> --json <n3-readiness.json>
```

## Readiness results
### `IDENTITY_BLOCKED`
The evidence cannot be used for strategy review because attribution identity is not trustworthy.

### `EVIDENCE_COLLECTION`
Identity may be valid, but closed-outcome evidence is incomplete, empty, or missing the N2 descriptive-only boundary.

### `REVIEW_READY`
The observed N2 sample is complete for the analyzed dataset and identity is valid. This means the bundle is ready to be reviewed for a possible strategy proposal.

`REVIEW_READY` does **not** mean a nested policy is approved or should be coded.

## Mandatory N3 output firewall
Before any separately approved strategy decision, every N3 output must contain:

```text
execution_policy = NONE
automatic_policy_authorized = false
source_modification_authorized = false
activation_authorized = false
```

If any research result or tool output violates this firewall, N3 fails closed.

## What to review when real evidence becomes available
Review at minimum:
- identity integrity;
- outcome coverage;
- counts by nested relation;
- counts by signal;
- relation × signal behavior;
- win/loss/breakeven counts;
- net/average realized outcome;
- Wilson 95% intervals;
- relation buckets with no decisive outcomes;
- wide uncertainty;
- pair/signal/time-period diversity available in the source dataset.

Do not convert point-estimate differences into a trading rule automatically.

## Future policy decision workflow
Only after real forward evidence is `REVIEW_READY`:
1. prepare a dated strategy proposal from the evidence;
2. state the exact behavior being proposed, e.g. whether a particular relation would gate a specific existing candidate family;
3. explicitly identify what remains unchanged;
4. obtain explicit strategy approval;
5. implement with a default-OFF gate;
6. run protected-surface regression + native MetaEditor 0E0W;
7. run broker/demo forward validation;
8. activate only after the activation review.

## Prohibited shortcuts
Do not:
- automatically block `CONFLICT`;
- automatically prefer `ALIGNED`;
- manufacture a score/threshold from relation labels;
- use synthetic test results as trading evidence;
- patch `BBMA_EA.mq4` from this runbook/tool;
- activate N3 because the research tooling itself passed tests.

## Completion definition
N3 staging is technically complete when:
- contract exists;
- readiness tool exists;
- activation-firewall tests pass;
- source remains unchanged;
- execution policy remains `NONE`;
- future activation dependency is explicitly recorded as real N2 forward evidence + separate approval.
