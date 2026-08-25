# NMJE Coding Limiter Stage Policy

**Status:** LOCKED GOVERNANCE DECISION  
**Scope:** M12N / Nested Multi-Timeframe Journey Engine (NMJE)  
**Applies to:** N1, N2 and N3 implementation stages

## Locked policy

The NMJE coding-complexity limiter follows the highest authority/complexity reached by the active implementation stage:

| Stage | NMJE role | Direct influence on trade eligibility/execution | Required limiter |
|---|---|---|---|
| N1 | Nested MTF mapping / lineage / JourneyID / relation classification | No | `INTERMEDIATE` |
| N2 | Shadow validation, telemetry, attribution and outcome analysis | No direct execution authority | `INTERMEDIATE` |
| N3 | Execution-aware NMJE; NMJE output may be consumed by M15/M16 as an approved validation/revalidation gate | Yes, safety-critical | `EXPERT-RESTRICTED` |

## Final-source rule

The active M12N source carries one limiter representing the highest complexity/authority of the production implementation. Therefore, once N3 becomes active production behaviour, M12N MUST be promoted from `INTERMEDIATE` to `EXPERT-RESTRICTED`.

Promotion to `EXPERT-RESTRICTED` does not authorize unnecessary complexity. The implementation must remain the simplest correct design that satisfies the approved state/lifecycle/orchestration contract.

`EXPERT` is not required unless a future explicitly approved architecture materially expands M12N beyond its context/gating responsibility into substantially more complex execution/recovery infrastructure.

## Boundary

Even at N3, NMJE does not become an independent signal detector or direct order executor. Strategy detection remains with its owning BBMA modules. Final entry authority and fail-closed/revalidation responsibilities remain with the approved downstream architecture, including M15/M16 as defined by the applicable N3 contract.
