# C10 Build 4.72–4.78 Exact Lineage Manifest

Status: **MATERIALIZED / BYTE-EXACT RECONSTRUCTION PASS / NO MERGE / NO ACTIVATION**

Issue: #124
Branch: `provenance/c10-local-473-478-recovery`
Remote document/history anchor: PR #108 head `5b73090639f1985f208f5daecae35a2008dd0688`  
Exact native source anchor: Build 4.72 SHA-256 `0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99`

## Representation

The historical Windows/native source is preserved as one deterministic gzip+base64 Build 4.72 base plus one deterministic gzip+base64 line patch per subsequent build. `reconstruct_lineage.py` reconstructs the exact original bytes and fails closed on every source SHA-256 boundary.

This representation is provenance-only. It does not replace `blueprint/source/BBMA_EA.mq4`, activate C10/NMJE authority, or change Strategy Core, risk, sizing, execution or trade lifecycle.

## Exact identities and stage boundaries

| Build | Stage | Exact source SHA-256 | Delta | Materialization commit |
|---|---|---|---|---|
| 4.72 | Offline Tester Symbol Compatibility | `0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99` | anchor | `c25d9f4436e999efc23f04d9397689f1cd5af123` |
| 4.73 | Offline Tester Timer Compatibility | `5D7D1CF9880773B067F445136CE4FC75EB37AE4A88BBA9EE7A756A29A146A2C6` | +24 / -8 | `6aad3d9b1cb42b06be9ee730e9ffe2bde58d4c00` |
| 4.74 | C10 Audit Ledger Stage A | `5FD416BE64389005C287A7904B3C094530DB6A9C6F89E2335943C4AB85E14EB6` | +410 / -4 | `0049a8635cee6f9540b4aa47a7800e10f544426a` |
| 4.75 | C10 Audit Ledger Stage B | `6607C061EF7BEAD88A640E733435D72E57D2AC47A26DEC551B81E313E47EF4CD` | +239 / -28 | `cd80eade64e38ce94a4b3577b7081c0b9868a350` |
| 4.76 | C10 Audit Ledger Stage C | `E8525A0172E568F9A12469A302D6784A1B1EE4F92B6C45B5B69D92D53AFB1F6A` | +224 / -9 | `1e4ed3a3f8ec2fc3648d91d22330226d6b572de1` |
| 4.77 | C10 Shadow Outcome Stage D-A | `D4B405ED9C30F584C1C7BDEB774A3063FF26CE6826D6867B8F699A0BF0DDFAE5` | +276 / -12 | `babe2844e2e2cc1a4a8e34308bd65a231fdd5ed3` |
| 4.78 | C10 Evidence Completion Stage D-B | `E4751E1DF464F61900CE3718702C4CBB8F1591193CA97B77F8936E983B5EC2EB` | +689 / -48 | `1c12d79e567e928e0931fa6e4951b1f964704ed6` |

Reconstruction harness filename correction: `398efd8af05e9a74e86110b942c97bdc8c9aaf77`.

## Files

- `NATIVE_BUILD472_BASE.mq4.gz.b64`
- `PATCH_72_TO_73.json.gz.b64`
- `PATCH_73_TO_74.json.gz.b64`
- `PATCH_74_TO_75.json.gz.b64`
- `PATCH_75_TO_76.json.gz.b64`
- `PATCH_76_TO_77.json.gz.b64`
- `PATCH_77_TO_78.json.gz.b64`
- `reconstruct_lineage.py`

## Verification — 2026-09-07

Fresh reconstruction from the materialized files reproduced all six target hashes exactly:

- 4.73 `5D7D1CF9880773B067F445136CE4FC75EB37AE4A88BBA9EE7A756A29A146A2C6`
- 4.74 `5FD416BE64389005C287A7904B3C094530DB6A9C6F89E2335943C4AB85E14EB6`
- 4.75 `6607C061EF7BEAD88A640E733435D72E57D2AC47A26DEC551B81E313E47EF4CD`
- 4.76 `E8525A0172E568F9A12469A302D6784A1B1EE4F92B6C45B5B69D92D53AFB1F6A`
- 4.77 `D4B405ED9C30F584C1C7BDEB774A3063FF26CE6826D6867B8F699A0BF0DDFAE5`
- 4.78 `E4751E1DF464F61900CE3718702C4CBB8F1591193CA97B77F8936E983B5EC2EB`

`git diff --no-index --numstat` also reproduced the recorded stage deltas exactly: 24/8, 410/4, 239/28, 224/9, 276/12, 689/48.

The reconstructed Build 4.78 contains embedded C10 SourceHash:
`D56D0820858ADCB847CE7A70354C7825374903890E93CB11761D6F003856F991`.

Therefore the historical local Build 4.73–4.78 lineage is now reproducible from repository materialization without modifying the active EA source.

## Next boundary

Do not merge or activate this provenance branch. The next isolated engineering step is to port the already-staged Build 4.79 / Issue #122 fix onto the verified 4.78 lineage, validate it, then stack Build 4.80 / Issue #123. Runtime acceptance remains mandatory before either repair can be promoted.

## Exact source-view commit chain — 2026-09-07

The deterministic base/patch representation is additionally materialized as one exact native MQ4 source view at:
`blueprint/provenance/c10-local-473-478/source_view/BBMA_EA.mq4`.

`source_view/.gitattributes` sets `BBMA_EA.mq4 -text` so Git stores the recovered Windows/native bytes without line-ending normalization.

| Build | Source-view commit | Git-stored byte SHA-256 |
|---|---|---|
| 4.72 | `4c13db5fa6f0b5a6973197a60a2d889bc48719d3` | `0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99` |
| 4.73 | `6e992d37b1dd018e21ad25705b4fcf690ec2b278` | `5D7D1CF9880773B067F445136CE4FC75EB37AE4A88BBA9EE7A756A29A146A2C6` |
| 4.74 | `35b89c9314540a10e79e5609486c82d7a16ca496` | `5FD416BE64389005C287A7904B3C094530DB6A9C6F89E2335943C4AB85E14EB6` |
| 4.75 | `c53a19b04bff60e6665681a5d035396c2e6965a3` | `6607C061EF7BEAD88A640E733435D72E57D2AC47A26DEC551B81E313E47EF4CD` |
| 4.76 | `da7dab9618f2c2cfbd0d50666ee8e86cd3888b51` | `E8525A0172E568F9A12469A302D6784A1B1EE4F92B6C45B5B69D92D53AFB1F6A` |
| 4.77 | `0c006d38fb14a3dc7532c803a68f3df0e112ca37` | `D4B405ED9C30F584C1C7BDEB774A3063FF26CE6826D6867B8F699A0BF0DDFAE5` |
| 4.78 | `03eafc4279915b8436d05600a48b131bba344a87` | `E4751E1DF464F61900CE3718702C4CBB8F1591193CA97B77F8936E983B5EC2EB` |

This source-view chain is provenance-only and does not replace `blueprint/source/BBMA_EA.mq4` on any canonical/owner branch. The PR #108 Git/native mismatch is recorded in `PR108_GIT_NATIVE_ANCHOR_MISMATCH_20260907.md`.