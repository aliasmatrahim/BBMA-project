# P2 Step 7 Fix A — Execution Tombstone UPSERT

Status: **APPLIED — AWAITING NATIVE METAEDITOR RECOMPILE**

Fixes:
- `MarkDecisionExecuted()` now UPSERTs an executed tombstone even when no prior DecisionID history row exists.
- Same-session duplicate prevention therefore survives position closure.
- `CleanupGlobalSignalHistory()` no longer removes executed ticket-backed tombstones through generic size cleanup.
- Non-executed rows remain eligible for size cleanup.

Post-fix source SHA-256:
`dda18da4ef08c61efe2e465133165f89ec2de8a980df849726639ca481b0ae63`

Strategy semantics: unchanged. This is execution/idempotency infrastructure only.

Gate: native MetaEditor compile must return 0 errors / 0 warnings before Step 7 can be re-audited and passed.
