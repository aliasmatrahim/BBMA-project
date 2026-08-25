# Project Directive — Park N1–N3 / Gap Closure First

Date: 2026-08-26
Branch: `d1-owner-dev`
Authority: explicit project-owner direction

## Decision

Effective immediately, **N1, N2 and N3 are PARKED**.

This includes N1.1 coverage-only extension work. Existing N1/N2/N3 decisions, patchers, workflows and audit evidence may remain in the repository for provenance, but they are not the active execution priority and must not be used to materialize new EA behaviour while this directive is active.

## Active project priority

**Close existing implementation / source / contract / runtime gaps before resuming N1–N3.**

This dated directive supersedes older `CURRENT.md` / `MASTER_QUEUE.md` active-next wording wherever those records point to N1, N2 or N3 expansion as the immediate next task.

## Source freeze at directive entry

At directive entry the active EA source remains:

- build header: `Version 4.5.6 - C044 Deterministic Replay Stage`;
- `#property version "4.56"`;
- Git blob: `f0f80decbdbda836c12b6073f5dbc6e347662b13`;
- C044 feature gate: OFF.

N1.1 had passed source-bound static patch/protected-surface checks in validation runners, but **was not materialized into the active EA source**. Therefore v4.56 remains the source baseline for gap closure.

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
