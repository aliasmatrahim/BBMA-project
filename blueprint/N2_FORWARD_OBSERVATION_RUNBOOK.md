# N2 NMJE Forward Observation Runbook

Date: 2026-08-25  
Status: ACTIVE RESEARCH RUNBOOK / NO EXECUTION GATING

## Objective
Collect real broker-connected MT4 evidence linking:

`[N1-NMJE] journey context -> [N2-NMJE-DEC] validated decision -> [N2-NMJE-OUT] realized closed outcome`

without allowing nested relation to influence trading.

## Required EA build
Use the `d1-owner-dev` build only after the N2-13 closed-outcome shadow has passed native MT4 0E0W and materialized.

## Required log coverage
A usable observation set should contain, where naturally produced:
- `[N1-NMJE]` records;
- `[N2-NMJE-DEC]` records with token-safe `DID` and `DIDH`;
- `[N2-NMJE-OUT]` records after monitored EA trades close.

Do not manufacture trades merely to populate the dataset.

## Research command
From the repository root:

```bash
python blueprint/tools/n2_nmje_auto_research_pipeline.py <mt4-log-1> [<mt4-log-2> ...] --out-dir <report-directory>
```

Generated research evidence:
- `correlation.json`
- `extraction.json`
- `reconciliation.json`
- `outcomes_reconciled.csv`
- `outcome_attribution.json`
- `evidence.json`

## Fail-closed integrity rules
Do not use a dataset for strategy conclusions when:
- duplicate DecisionID/ticket identity exists;
- a `[N2-NMJE-DEC]` DIDH disagrees with reconstructed `SHORT_HASH(DecisionID)`;
- a full `[N2-NMJE-OUT]` DIDH is missing or mismatched;
- full outcome pair does not match its validated decision;
- a recovered hash maps to more than one DecisionID;
- a recovered hash pair does not match;
- pipeline reports invalid identity.

## Interpretation
N2 statistics are descriptive research only. Compare observed closed outcomes by nested relation and signal while preserving uncertainty/coverage information. Do not infer a deterministic edge from a small sample and do not introduce arbitrary sample thresholds solely to force an execution decision.

## Strategy guard
No N2 result automatically authorizes:
- rejecting `NESTED_CONFLICT`;
- preferring `NESTED_ALIGNED`;
- increasing or decreasing entry count;
- modifying D1/M15 authority;
- modifying REM/RRE/REE;
- changing SL/TP or risk.

Any future execution use of NMJE requires a separate explicit strategy decision after observed evidence is reviewed.
