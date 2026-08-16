# P2 Step 8 Fix B — Pre-Send Monitored Registry Capacity Gate

Status: **APPLIED — REQUIRES NATIVE METAEDITOR 0E/0W VERIFICATION**

Canonical source SHA-256 after fix:
`8fa2050c34db671635c1934ca37e9a8804ee65f3285fccf212e842dd5e8afa9b`

## Fix
- Added `EnsureMonitoredRegistryCapacity()` using the existing fail-closed compaction path.
- `ProcessEntry()` now checks monitored-registry capacity before `OrderSend`.
- If no safe slot exists, the decision is rejected before any broker order can be created.
- Existing duplicate/idempotency checks remain before the capacity gate.

## Strategy semantics
No BBMA signal, EntryMode, SL/TP, money-management, risk or portfolio strategy semantics changed. This is lifecycle ownership integrity only.
