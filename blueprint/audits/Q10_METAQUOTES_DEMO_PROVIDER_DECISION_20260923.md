# Q10 MetaQuotes-Demo Provider Decision — 2026-09-23

Issue: #109
Baseline: `d1-owner-dev@cd3a9853ad4ed687a9648a70623cf5922674208a`
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Decision

The user explicitly selected **MetaQuotes-Demo** as the demo provider for final Q10 runtime acceptance.

The original Issue #109 requires attributable demo-account evidence and does not require HFM specifically. Later HFM-only wording in Q10 tooling was an implementation restriction, not a Strategy-Core requirement.

## Scope

- Q10 AUTH accepts only a connected account positively identified by MT4 as demo.
- Current allowed provider identity is MetaQuotes / MetaQuotes-Demo.
- Live accounts remain prohibited.
- Dedicated-terminal separation, exact candidate/source/EX4/settings binding, evidence SHA binding, resumable state, clean restart, and R3 -> R4 -> R5 -> R6 ordering remain unchanged.
- No Strategy Core, risk/MM, execution, lifecycle, recovery, dashboard or EA source semantics change.
## Evidence boundary

MetaQuotes-Demo can close the generic final **demo-runtime acceptance** gate in Issue #109.

It does **not** prove HFM-specific spread, stop-level, server, execution-latency or broker-policy behavior. Those broker-specific claims must not be made from MetaQuotes-Demo evidence.

Historical HFM audit/evidence files are preserved unchanged as provenance.

## Validation

- Q10 targeted pytest: 13/13 PASS.
- Full repository pytest: 35/35 PASS.
- Frozen Build 5.11 candidate verification: PASS.
- EA source diff against owner baseline: zero.
- Probe MQ4 source identity is line-ending normalized; probe EX4 hash remains raw-byte strict.
