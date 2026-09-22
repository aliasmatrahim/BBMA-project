# N1 P1 Build 5.08 Architecture / Regression Review

Issue #231. Source-bearing commit: `3d6b0b6ac7b247f240dec259c3b17af33a4968c1`.

## ISSUE -> IMPACT -> FIX
**CONFIRMED PROVENANCE BUG** — D1-owner NMJE identity used latest `SourceCandleTime`, so an ordinary same-owner D1 refresh could rotate JourneyID.

Impact: child lineage could appear to migrate to a new journey without a material owner transition, weakening deterministic restart/research attribution.

Fix: provenance-only contiguous D1 owner epoch + canonical EventID/ParentEventID, with JourneyID anchored to exact parent identity. Historical reconstruction calls the same canonical M11 classifier as live owner evaluation.

## Ownership review
- M11 remains sole D1 strategic formula owner.
- M12N remains observation/read-only.
- M15 remains sole final entry authority; M16 remains revalidation authority.
- M19/M20/M21 and TradeLock are unchanged.
- M22 OrderSend ownership unchanged; F07/N2 Build 5.07 repair unchanged.
- M23/M24 lifecycle/recovery unchanged.
- N3 execution policy remains NONE / inactive.

## Regression review
25 protected Build 5.07 function bodies are exact-equal.
Normal EveryTick trading traces are exact-equal to Build 5.07.
Only intended NMJE lineage metadata changes; N2 decision payload is otherwise exact after normalizing `J=`.
No additional source fix identified within #231 scope.

## Result
Build 5.08 is **SCOPED OFFLINE VERIFIED / NOT MERGED / NOT PRODUCTION ACTIVATED / NOT LIVE BROKER VERIFIED**.
