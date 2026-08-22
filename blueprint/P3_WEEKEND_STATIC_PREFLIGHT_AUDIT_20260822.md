# P3 Weekend Static Preflight Audit

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **STATIC PREFLIGHT PASS / RUNTIME EVIDENCE STILL REQUIRED**

## Purpose
Use the market-closed window to inspect the exact current 0E0W runtime candidate without changing EA source semantics or invalidating the already-captured runtime evidence.

## Test B — frozen-state log suppression
Static source inspection shows `RecoverExistingOrders()` is invoked from initialization after `RebuildExecutionHistory()` and before `g_is_initialized=true`. The `[P3S5][RECOVERY]` diagnostic is printed inside `RecoverExistingOrders()` while reconstructing exact-owned live orders. No tick/timer call-site to `RecoverExistingOrders()` was found in the current source path inspected for this audit.

Static verdict: **SUPPORTS EXPECTED PASS BEHAVIOR** — the recovery burst is designed as initialization/reconstruction output rather than a per-cycle diagnostic.

Runtime closure remains required by the Step 5 checklist because the project explicitly requires direct evidence that the diagnostic does not spam after initialization.

## Test C — fresh M22 execution identity persistence
Static source inspection confirms the post-OrderSend path:
- derives `expectedExecutionHash = SHORT_HASH(decision.DecisionID)`;
- re-selects/reads the broker-returned `OrderComment()`;
- extracts the persisted hash from that broker-returned comment;
- sets `Persist=PASS` only when the returned hash exists and equals the expected hash;
- sets `TradeInfo.execution_hash` only when the broker-returned hash matches;
- prints `[P3S5][EXEC_ID]` with `Persist`, `HashFound`, `HashMatch`, expected/persisted hashes and raw comment.

Static verdict: **SOURCE CONTRACT PRESENT / RUNTIME BROKER PERSISTENCE STILL UNPROVEN**.

## Test D — restart after fresh hashed trade
Static recovery inspection confirms:
- `RecoverExistingOrders()` reads `OrderComment()` from each exact-owned open order;
- `ExtractExecutionHash()` is evaluated before recovery classification;
- a found hash avoids `REC_IDENTITY_MISSING_FROZEN` solely for missing identity;
- matching full metadata can recover as `REC_NORMAL`; hash-only identity can recover as `REC_IDENTITY_HASH_ONLY`;
- execution-hash tombstone handling is driven by the observed broker-returned hash rather than fabricated identity.

Static verdict: **SOURCE RECOVERY PATH PRESENT / RESTART RUNTIME EVIDENCE STILL REQUIRED**.

## Change-control conclusion
No EA source change was made in this audit. This intentionally preserves the exact current native-compile/runtime candidate that already has:
- native MetaEditor **0 errors / 0 warnings**;
- initialization PASS;
- P3 Step 5 Test A PASS.

Tests B–D remain live-runtime gates when the FX market reopens.
