# P3 Step 5 — S5C Deployment Manifest

## Canonical runtime build
- Branch: `blueprint-dev`
- Canonical S5C source commit: `0b57f042c4c90a5a00531c152252c1e53332eb3f`
- Source file: `blueprint/source/BBMA_PROFESSIONAL_EA.mq4`
- Change purpose: verify broker-persisted `BBMA|H:` execution identity after a fresh M22 execution and populate `TradeInfo.execution_hash` only from a matching broker-returned hash.

## Native MT4 compile proof
- Workflow: `P3 S5C Execution Identity Persistence`
- Run: `32026948381`
- Compile job: `95378287873`
- Native MetaEditor result: `0 errors, 0 warnings, 88 msec elapsed`
- Marker: `P3_S5C_NATIVE_MT4_COMPILE=PASS`
- EX4 artifact ID: `9287742252`
- EX4 SHA-256: `380c485852993e35f919810a94dc224e36462409df958dcfe7252c0e2996b3b1`

## Deployment target
Deploy `BBMA_PROFESSIONAL_EA.ex4` from the S5C compile artifact to the MT4 terminal used for P3 runtime validation. Re-attach/restart the EA using the same configured StrategyID/InstanceID/PairList so exact-owned existing orders are reconstructed against the intended magic mapping.

## Required runtime evidence after deployment
1. Existing valid exact-owned orders without observable `BBMA|H:` must recover as `REC_IDENTITY_MISSING_FROZEN` with `Cause=MISSING_EXECUTION_HASH`.
2. The recovery diagnostic must be emitted once during reconstruction, without repeated frozen-state spam on subsequent cycles.
3. One genuine fresh post-S5C M22 execution must emit `[P3S5][EXEC_ID] ... Persist=PASS HashFound=Y HashMatch=Y ... RawComment=<BBMA|H:...>`.
4. Restart/re-attach while that fresh order remains open and verify the hash is recovered and no duplicate execution is created.

## Safety notes
- Do not create a manual surrogate order for Test C.
- Do not deliberately corrupt a live order to manufacture a hard-invalid case.
- Do not deliberately force a live-account loss to test emergency-close precedence; use safe/demo/naturally occurring evidence.

## Status
`DEPLOYMENT BUILD READY — FINAL MT4 RUNTIME EVIDENCE REQUIRED`
