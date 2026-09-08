# Build 4.81 C10 Runtime Closure Package Template

Status: **PREPARED / NOT YET SATISFIED**. Do not use this file as PASS evidence until the automation writes a genuine runtime bundle and verifier PASS.

## Frozen expected identity
- BuildID: `4.81`
- source SHA-256: `5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57`
- C10 SourceHash: `D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D`
- deployment EX4 SHA-256: `05733566540A2E5F0BA109BADA7EB17920DF5853201DAA5D9E8023E65C1912C0`
- InstanceID=81; Authority=NONE; `ExpertsTrades=false`; zero trade caps.

## Required physical-restart evidence
1. fresh exact-identity checkpoint contains `RecordType=ACTIVE`;
2. capture exact DecisionID + frozen checkpoint fields before stop;
3. stop the isolated MT4 process, not the primary MT4;
4. restart the same isolated terminal/config;
5. checkpoint recovers the same DecisionID as ACTIVE with frozen fields unchanged;
6. post-restart log contains `[C10][SHADOW_RECOVERY] Active=1` and exact-config `[C10][READY] ... Authority=NONE`;
7. post-enrollment chronology is valid; no pre-enrollment outcome;
8. no `LEDGER_DISABLED`, malformed/interleaved rows or same-domain duplicate IDs;
9. no `OrderSend`, `OrderClose`, `OrderModify`, `OrderDelete` or `DEC_EXECUTED`;
10. hardened verifier returns PASS.
## Closure decision rule
- Issue #122 may be closed only after every #122 acceptance row in `ACCEPTANCE_MATRIX_122_123_20260908.md` is PASS using exact Build 4.81 evidence.
- Issue #123 may be closed only after the inherited writer-namespace fix is shown to remain intact through the same successor restart and the original #123 criteria remain satisfied.
- If the verifier fails, keep both issues open and classify the exact failure before any new source change.
- A new source change requires a new unique build identity; never patch Build 4.81 in place.

## Explicit exclusions
- no merge of PR #129/#130/#131;
- no write to `d1-owner-dev` canonical source;
- no trading enablement;
- no Strategy Core modification;
- no D1/F7/NMJE authority change;
- no release-ready claim from this template alone.