# N2 NMJE Research Tooling Observable Self-Test Audit

Date: 2026-08-25  
GitHub Actions run: `32782047965`  
Temporary PR: `#68` (closed, not merged)

## Result
**PASS — all staged N2 synthetic research-tooling tests and research-only guardrails completed successfully on GitHub Actions.**

Verified in the successful job:
- N2-02 decision/journey correlator;
- N2-03 realized-outcome attributor;
- N2-04 evidence sufficiency / Wilson uncertainty reporter;
- N2-05 end-to-end research pipeline;
- N2-07 closed-outcome MT4 log extractor;
- N2-09 fail-closed short-hash identity reconciler;
- N2-10 automatic research pipeline with token-safe DecisionID + hash recovery;
- research-only guardrail scan.

## Corrections discovered by the observable test loop
1. Python 3.12 dynamic-import tests for dataclass modules required explicit `sys.modules` registration. Test harness corrected; production research logic was unchanged.
2. A more important telemetry issue was exposed: BBMA `DecisionID` contains a human-readable `TimeToString()` component with whitespace. Raw `DID=<DecisionID>` is therefore not safe as a single whitespace-delimited log field. N2-01A now requires token-safe DecisionID logging plus `DIDH=SHORT_HASH(DecisionID)`, and the correlator restores the original DecisionID before attribution.

## Scope
Synthetic PASS validates research mechanics and identity handling only. It does **not** prove a nested trading edge and does not authorize any execution filter/generator.
