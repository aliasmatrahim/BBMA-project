# PR #108 Git / Native Build 4.72 Anchor Mismatch — 2026-09-07

Status: **CONFIRMED PROVENANCE DEFECT / NO STRATEGY CHANGE / NO ACTIVATION**

Issue: #124  
Draft PR: #125  
Remote document anchor: PR #108 head `5b73090639f1985f208f5daecae35a2008dd0688`

## Finding

The Build 4.72 source committed at PR #108 is not byte-equivalent or normalized-text-equivalent to the native source that PR #108 records as the compile input.

PR #108 records:
- native Windows source SHA-256: `0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99`;
- normalized source SHA-256: `1C40C6D692A66652F5CDFF25D7F81A6CA7FED2D340F8BEEE24EA797D30FD4E49`;
- native MetaEditor: 0 errors / 0 warnings.

The actual PR #108 Git blob for `blueprint/source/BBMA_EA.mq4` is:
- Git blob SHA-1: `0a66cdb4960ff349ed27cf3b5402defcfb9d48a0`;
- file SHA-256: `AB1F80807E5EB10DC8555463BAA525BF0E537F3A6281A0114708A7C756345B53`;
- size: 436,481 bytes.

The recovered native Build 4.72 source is 480,286 bytes and normalizes to 469,841 bytes. The Git blob is therefore not the recorded compile source.## Structural comparison

After normalizing the recovered native source to LF, the comparison against the PR #108 Git blob shows approximately:
- 963 added source lines;
- 3 deleted source lines;
- 3 diff hunks.

The largest hunk replaces the malformed Git fragment `ift + i);` with approximately 960 lines of valid source, including broker-spec validation, processing-time helpers, utility functions and PairID/Magic helpers.

This is not a CRLF/LF-only difference.

## Provenance interpretation

PR #108 remains the remote **document/history anchor** because it records the exact native Build 4.72 identity and native compile evidence, but its committed MQ4 blob is not the native compile artifact.

For source ancestry, the recovered native Build 4.72 with SHA-256 `0F461312...1E99` is the exact source anchor. The existing 4.73–4.78 deterministic patch stack is based on that exact native anchor and reconstructs every later recorded source identity.

Do not use PR #108's committed MQ4 blob as the input for the 4.73–4.78 reconstruction or for Issue #122/#123 repair stacking.

## Safety boundary

This finding is provenance/source-history only. It does not alter BBMA Strategy Core, M15 authority, risk, sizing, execution, D1TPW, C044 or NMJE execution authority.