# Q10 Hybrid Phase H — Build 5.11 Reused Historical Coverage

Date: 2026-09-23
Issue: #109
Baseline owner: `d1-owner-dev@5aebad7c744d32c9e5de5c5b7b3d484b40e43846`
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Result

**PHASE H REUSE: INCOMPLETE / 32 PASS / 27 INCOMPLETE / 0 FAIL / NO EA FIX**

This checkpoint applies the approved hybrid sequence: exact-candidate historical coverage first, final MetaQuotes-Demo reconfirmation last. It reuses the already-VERIFIED four-period Build 5.11 historical matrix; no matrix period was rerun.

Evidence classification remains:

`ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE`.

## Identity

- canonical MQ4 SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`;
- tester adapter MQ4 SHA-256: `D3ADEAA06888B1CEC03A10852EEF8491743336A95084D84DD2EFE8B703046832`;
- tester adapter EX4 SHA-256: `8F6B1D8F6665E6DC72CF5A463A99D1A67F0CBB5E8CA73C4E133A4CFFF4FE387F`;
- settings SHA-256: `37BC585EB3AB5A73914FEC3C532023636D4FACCD7D3AAAF20B774269CF92DA70`;
- source invariants: 68/68 PASS.

All four reused tester-log SHA-256 identities and all GBPUSD M15/H1/H4/D1 HST identities are recorded in the evidence manifest.

## Validated analyzer behavior

The Phase H analyzer is fail-closed and hash-bound. It:
- requires the exact Build 5.11 marker once in every reused period;
- rejects historical-log or HST hash drift;
- scopes ticket/DecisionID identity by tester run so ticket-number reuse between periods is not misclassified as duplication;
- reconstructs M17 structural windows from the exact source timeframe HST;
- distinguishes ordinary one-Point Re-Entry structural safety from the approved standalone Extreme 3-pip wick buffer;
- applies SELL frozen-spread buffer `max(2 pips, ceil(raw spread pips))`;
- evaluates targetless TP=0 only for C044/D1TPW lifecycle-managed decisions;
- correlates D1 Opportunity attribution and canonical LTF execution identity;
- treats approved tactical `D1_OPP_EXTREME_TPW` strategic-owner opposition separately from ordinary strategic/opportunity alignment;
- correlates N1/N2 runtime evidence with exact-source 68/68 authority invariants.

Validation:
- hybrid analyzer/current-source tests: 10/10 PASS;
- full `blueprint/tests`: 46/46 PASS;
- EA source diff: zero.

## Reused evidence facts

- 1,044 executions;
- 578 BUY / 466 SELL;
- duplicate execution DecisionIDs: 0;
- duplicate run-scoped tester tickets: 0;
- N2 end-to-end ticket/hash chains: 1,044;
- D1O executions: 584;
- D1 closed-owner samples: 66,408; closed-only invariant PASS;
- M17 BUY records: 10,874;
- M17 SELL records: 7,943;
- structural windows reconstructed: 1,221 unique windows;
- missing structural windows: 0;
- structural anchor mismatches: 0;
- targetless lifecycle records: 15,868, all evaluated under lifecycle-specific TP rules;
- ordinary D1 selection violations: 0;
- strategic-owner-opposite selections: 180, all correlated to approved `AUTH=OPP / OFAM=EXT_TPW` tactical exception.

## Phase H PASS cases

R3:
`R3-01, R3-02, R3-05, R3-06, R3-08, R3-09, R3-10, R3-11, R3-13, R3-15`.

R4:
`R4-00, R4-02, R4-03, R4-04, R4-05, R4-06, R4-07, R4-10, R4-12, R4-14`.

R5:
`R5-00, R5-01, R5-09`.

R6:
`R6-00, R6-01, R6-04, R6-05, R6-10, R6-11, R6-12, R6-13, R6-14`.

## Remaining Phase H gaps

R3:
`R3-03, R3-04, R3-07, R3-14`.

R4:
`R4-08, R4-09, R4-11, R4-15, R4-16`.

R5:
`R5-02, R5-03, R5-04, R5-05, R5-06, R5-07, R5-08, R5-10, R5-14, R5-15, R5-16, R5-17, R5-18, R5-19, R5-20`.

R6:
`R6-08, R6-15, R6-16`.

No FAIL is present. Missing scenarios remain INCOMPLETE; they are not inferred from absence.

## Evidence

Repository-safe evidence:
- `blueprint/audits/evidence/Q10_HYBRID_PHASE_H_REUSE_20260923/Q10_HYBRID_HISTORICAL_ANALYSIS_V3.json`;
- `blueprint/audits/evidence/Q10_HYBRID_PHASE_H_REUSE_20260923/MANIFEST.json`.

Analysis SHA-256:
`61BD9488FA4884728C574FEE61256315532A6CFAF2AE22BCC72C995D3C3E8AEC`.

Manifest SHA-256:
`272425CC09B0F57A83CB87BD7C2A72748784DF62CB256353E80F055E6DEF9C16`.

Raw large tester logs/HST remain on G40 and are hash-addressed.

## Next

Continue Phase H only for the 27 genuine gaps. Prefer deterministic exact-source fixtures for fail-closed/error/observer-tooling cases, and use targeted Strategy Tester variants only where market/runtime state is material. Do not rerun the completed four-period matrix. MetaQuotes-Demo Phase L remains last.
