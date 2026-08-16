# P2 Step 8 Fix C — Emergency Liquidation Precedence

Status: **APPLIED — REQUIRES NATIVE METAEDITOR 0E/0W VERIFICATION**

Canonical source SHA-256 after fix:
`36a29a5646fa19aec4f0a9f90805c870a29f4b3cd1fd36233a0ba256826f6264`

## Fix
- Exact ownership/magic revalidation remains before any lifecycle action.
- M20 emergency full-close now executes before recovery-state freezing.
- `REC_CORRUPTED` and `REC_RECOVERY_INVALID` positions remain frozen for normal lifecycle behavior, but cannot block emergency liquidation.
- No BBMA entry, SL/TP, trailing, breakeven, partial close, TP2 or TP3 semantics were added.
