# BBMA C10 Local Lineage Provenance — 2026-09-04

Status: **PROVENANCE RECONSTRUCTION IN PROGRESS / NO MERGE / NO ACTIVATION**

Issue: #124

## Purpose

Recover the exact source ancestry used by the connected C10 runtime session before proposing runtime fixes #122 and #123.

This record is evidence/governance only. It does not activate strategy, risk, sizing, execution, D1TPW, C044 or NMJE authority.

## Verified remote anchor

Draft PR #108 / `c3-offline-tester-compat-dev` head:

`5b73090639f1985f208f5daecae35a2008dd0688`

PR #108 records Build 4.72 exact Windows/native source SHA-256:

`0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99`

The recovered local Build 4.72 source has the same exact file SHA-256 and header/property:

- `Version 4.7.2 - Offline Tester Symbol Compatibility`
- `#property version "4.72"`

Therefore PR #108 is the verified remote ancestry anchor for the local continuation.

## Sequential local source lineage

| Build | Stage | Exact source-file SHA-256 | Delta from previous build |
|---|---|---|---|
| 4.72 | Offline Tester Symbol Compatibility | `0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99` | remote anchor |
| 4.73 | Offline Tester Timer Compatibility | `5D7D1CF9880773B067F445136CE4FC75EB37AE4A88BBA9EE7A756A29A146A2C6` | +24 / -8 |
| 4.74 | C10 Audit Ledger Stage A | `5FD416BE64389005C287A7904B3C094530DB6A9C6F89E2335943C4AB85E14EB6` | +410 / -4 |
| 4.75 | C10 Audit Ledger Stage B | `6607C061EF7BEAD88A640E733435D72E57D2AC47A26DEC551B81E313E47EF4CD` | +239 / -28 |
| 4.76 | C10 Audit Ledger Stage C | `E8525A0172E568F9A12469A302D6784A1B1EE4F92B6C45B5B69D92D53AFB1F6A` | +224 / -9 |
| 4.77 | C10 Shadow Outcome Stage D-A | `D4B405ED9C30F584C1C7BDEB774A3063FF26CE6826D6867B8F699A0BF0DDFAE5` | +276 / -12 |
| 4.78 | C10 Evidence Completion Stage D-B | `E4751E1DF464F61900CE3718702C4CBB8F1591193CA97B77F8936E983B5EC2EB` | +689 / -48 |

The delta counts were produced by local `git diff --no-index --shortstat` against each consecutive source pair.

## C10 embedded source identities

C10 source identity begins in Stage A and advances at each source change:

- Build 4.74: `F44B7B7165EFED0D6C5FC7C690618AF962163C10D313ABD6C16293BB0D6FE4DE`
- Build 4.75: `C502B6892383D612D194A26F3A3C7A92684E6A53E683603A2A58DC13CEC5CA64`
- Build 4.76: `44A291090906BB5AE3C6DC8976F00D1834C47FB6AA8EA7EF3887D700359A150D`
- Build 4.77: `626E388F64182BB51F87E7AF8D8A2F87E171234764E05E6240D188B432D4C341`
- Build 4.78: `D56D0820858ADCB847CE7A70354C7825374903890E93CB11761D6F003856F991`

The Build 4.78 C10 SourceHash is the identity emitted by the connected runtime that reproduced Issues #122 and #123.

## Runtime-fix staging after the recovered lineage

### Issue #122 — Build 4.79

Local isolated repair only:

- title: `C10 Shadow Timeline Provenance Fix`
- C10 SourceHash: `5DC9CCF005C1237BAB8D23FB669D853ADB52FB0C292F270E96C9E2D35226CAB1`
- source-file SHA-256: `E44BAF278170530FF823BEE10437D95DF9236E9FA8C295FCCF432DF7809D856E`
- targeted static/model checks: PASS
- native MetaEditor: 0 errors / 0 warnings
- runtime: NOT VERIFIED

### Issue #123 — Build 4.80

Stacked locally on Build 4.79:

- title: `C10 Ledger Writer Namespace Fix`
- C10 SourceHash: `5C672778E35AA2602702824778F8F7F6EE4BCDCDFB99B7E32679A17CC0DA2DC6`
- source-file SHA-256: `E9C8CFBE574786BE22003D76F015E5438E9D2EEFD8BF11E377DD93FE61BAE0E1`
- Issue #122 regression checks: PASS
- Issue #123 writer-namespace checks: PASS
- embedded source-hash recomputation: MATCH
- native MetaEditor: 0 errors / 0 warnings
- runtime: NOT VERIFIED

## Current materialization boundary

This branch currently records the provenance proof only. The Build 4.73–4.78 source sequence has not yet been materialized into Git commits on this branch.

Do not treat this branch as equivalent to live Build 4.78 until the exact local lineage has been materialized and its final source identity is rechecked against the hashes above.

## Local Git access boundary

The laptop's repository remote is HTTPS and GitHub Desktop's credential manager is configured, but non-interactive Git cannot obtain a credential. Credential extraction/bypass is not authorized or required. Authorized GitHub connector writes may be used for repository records while laptop files remain the runtime evidence source.

## Next safe action

Materialize the missing local 4.73→4.78 source lineage on this isolated branch, preserving stage boundaries or equivalent reproducible provenance. Verify exact Build 4.78 identity before stacking the 4.79 and 4.80 fixes.

No merge, release, canonical owner-branch overwrite, or runtime deployment is authorized by this record.