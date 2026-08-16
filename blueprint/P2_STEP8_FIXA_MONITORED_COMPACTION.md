# P2 Step 8 Fix A — Monitored Trade Compaction

Status: **APPLIED — REQUIRES NATIVE METAEDITOR 0E/0W VERIFICATION**

Canonical source SHA-256 after fix:
`5dcd2f93bfe72b5dc5c210671f511d8ebcccef3d30e2a64bfb40dcdb9eee8e59`

Closed broker-confirmed monitored records are compacted before new tickets are appended. Failed OrderSelect records are preserved fail-closed. No BBMA strategy semantics changed.
