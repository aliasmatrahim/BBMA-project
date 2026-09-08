# F7/C044 Restart Atomicity Audit — 2026-09-08

Classification: **CONFIRMED BUG / RESTART-PERSISTENCE ATOMICITY**. No Strategy-Core semantic mismatch is asserted.

## ISSUE
Canonical v4.61 `SaveC044ReplaySeed()` writes replay version marker `R|V=1` **before** rewriting the replay payload (`R0..R19`, `B0..B18`, `S0..S18`). It does not invalidate/delete the marker before the write and does not use a new generation/commit token.

`LoadC044ReplaySeed()` accepts `V==1`, then only proves that every payload key exists. On a later save, those keys normally already exist from the previous committed seed. A terminal/process interruption after only part of the new payload is written can therefore leave:
- `V==1` still valid;
- all keys still present;
- some keys from the new replay seed and some stale keys from the previous seed.

The loader can accept that mixed-generation state if the limited final direction/timeframe checks still pass.

`SaveC044Checkpoint()` has the same generation-boundary weakness for its ten lifecycle metadata keys: values are overwritten in place and key existence alone is checked. Replay-seed save is invoked before those metadata fields are written, so a crash can also leave replay and lifecycle metadata from different save generations.

## IMPACT
After physical MT4/EA interruption during a checkpoint update, F7 restart replay can consume a structurally mixed snapshot rather than fail frozen. That can change which later owner candle is interpreted as same-Re-Entry, mature opposite Extreme, hold, or exit condition. This violates the F7 requirement that replay/recovery be deterministic and fail-frozen when history/identity/state cannot be proven.

This is persistence infrastructure, not a new BBMA rule. No evidence currently proves this torn-write window occurred in the observed live session.

## FIX BOUNDARY
Do not hotfix the frozen primary runtime candidate.

Post-freeze smallest authorized design should make one checkpoint generation atomic/fail-closed, for example:
1. invalidate/delete a commit/version marker before writing a generation;
2. write replay payload + lifecycle metadata while the generation is invalid;
3. verify all required writes/identity fields;
4. publish the commit/version/generation marker **last** and flush;
5. loader accepts only one complete committed generation and rejects mixed/partial state.

A generation/checksum scheme is acceptable if it covers both replay seed and lifecycle metadata together. Do not create a second F7 lifecycle owner.

## Required validation
- deterministic torn-write tests at every payload/metadata prefix, including overwrite of an already-existing prior generation;
- repeated restart equivalence from committed generations;
- fail-frozen on missing/mixed generation;
- existing hold/re-arm/opposite-CSM/opposite-Extreme semantics unchanged;
- M20 precedence and M23 close ownership unchanged;
- native MetaEditor 0E0W;
- focused physical restart runtime after the current freeze is released.

## Current action
Record and queue only. No canonical MQ4 write or primary MT4 reload is performed by this audit.
