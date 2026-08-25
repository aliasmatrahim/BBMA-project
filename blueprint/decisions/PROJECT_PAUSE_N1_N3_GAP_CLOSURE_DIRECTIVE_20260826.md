# Project Directive — Park N1–N3 / Gap Closure First

Date: 2026-08-26
Branch: `d1-owner-dev`
Authority: explicit project-owner direction

## Decision

Effective immediately, **N1, N2 and N3 are PARKED**.

This includes any further N1.1 coverage extension work. Existing N1/N2/N3 decisions, patchers, workflows and audit evidence may remain in the repository for provenance, but they are not the active execution priority and must not be used to materialize further EA behaviour while this directive is active.

## Active project priority

**Close existing implementation / source / contract / runtime gaps before resuming N1–N3.**

This dated directive supersedes older `CURRENT.md` / `MASTER_QUEUE.md` active-next wording wherever those records point to N1, N2 or N3 expansion as the immediate next task.

## Corrected source freeze at directive entry

Post-directive provenance review established that the N1.1 verification runner had already completed and committed before this directive was written. Therefore the correct active baseline entering gap closure is:

- build header: `Version 4.5.7 - N1.1 NMJE Coverage Overlay`;
- `#property version "4.57"`;
- Git blob: `2285b90b82c4512b50279bb3546f9801dbc652a3`;
- N1.1 source SHA-256: `82264cf82707a3831262a7e14539432a4dab173fe04d277972f81980f88bf40f`;
- N1.1 verification: protected-function source guard PASS, M12N ownership scan PASS, official MT4 MetaEditor 0 errors / 0 warnings;
- C044 feature gate: OFF.

N1.1 is **read-only observability already materialized before the park directive**. It does not change primary node/parent kinds, REM/RRE/REE, D1O candidate construction, M15/M16 authority, SL/TP, risk, MM, execution, lifecycle or recovery. It is therefore retained as the verified baseline rather than reverted. **No further N1/N2/N3 work is authorized while this directive is active.**

Implementation evidence: `blueprint/N1_1_NMJE_COVERAGE_IMPLEMENTATION_AUDIT_20260826.md`.

## Gap-closure governance

1. Do not add new execution paths, new filters, optimization logic or N1/N2/N3 expansion while material gaps remain open.
2. Close source/contract mismatches before patching trading behaviour.
3. Preserve accepted BBMA semantics and existing module ownership boundaries.
4. Technical integrity fixes that do not alter strategy semantics may proceed with source-bound regression + native 0E0W gates.
5. Broker/demo-only evidence gaps are classified separately and must not block safe static/source reconciliation work.
6. Any HOLD family remains non-executable until its source evidence is explicitly reconciled and accepted.
7. `REJ_INVALID_LOT` diagnostics and dashboard trade count remain CLOSED/PASS and must not be reopened without new evidence.

## Immediate gap priority

The newest targeted SL/TP audit is the primary active gap source. Its verdict is `REPAIR / SOURCE-RESOLUTION REQUIRED` and it identifies:

- `SLTP-01` HIGH — D1 Opportunity `EXTREME_TPW` is not TP-Wajib-owned in M17;
- `SLTP-02` HIGH — generic static outer-BB TP does not represent the complete lifecycle exit evidence;
- `SLTP-03` MEDIUM/HIGH — generic Re-Entry structural-range SL provenance remains unresolved;
- `SLTP-04/05` are safety/infrastructure separations to preserve, not gaps to rewrite.

Primary audit: `blueprint/audits/TARGETED_SLTP_IMPLEMENTATION_AUDIT_20260826.md`.

## Resume condition for N1–N3

N1–N3 may resume only after the active gap register has no unresolved **repo-closable HIGH/CRITICAL** item, or after an explicit project-owner decision changes this directive.
