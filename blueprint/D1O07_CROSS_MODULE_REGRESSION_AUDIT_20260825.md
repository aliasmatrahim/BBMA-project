# D1O-07 Cross-Module Regression Audit

Date: 2026-08-25
Branch: `d1-owner-dev`
Build: `Version 4.5.1 - D1O-07 Canonical LTF Dedup`
EA SHA-256: `c911790b45fb7a75270fdee1204a7c97313605dca194f57380441b92a66896c2`
Status: **PASS / NO CODE FIX REQUIRED**

## Scope

Focused current-baseline regression across the execution chain requested by `MASTER_QUEUE.md`:

`M15 selection -> M16 authority/component revalidation -> M17 source SL/TP -> risk/MM/portfolio preflight -> M22 idempotent execution -> M24 recovery identity`

This audit also verifies that D1O-07 canonical LTF dedup does not drift execution identity when D1 attribution metadata changes.

## Automated evidence

GitHub Actions workflow: `D1O-07 Mode1 cross-module regression`
Run: `32817790689`
Job: `97709483350`
Conclusion: **success**

Machine outputs:
- `D1O07_MODE1_STATIC_COMPLIANCE=PASS`
- `D1O07_CROSS_MODULE_REGRESSION=PASS`
- `EA_SHA256=c911790b45fb7a75270fdee1204a7c97313605dca194f57380441b92a66896c2`
- `git diff --check` PASS.

## Findings

### M15 — PASS

M15 remains sole final candidate-selection authority.

Normal candidates must pass D1 strategic-owner compatibility. D1 Opportunity candidates use their separately frozen opportunity authority only in Mode 2.

The selected decision freezes:
- direction;
- signal type;
- canonical components;
- canonical sequence hash;
- SL/TP source component;
- candidate expiry;
- D1 authority snapshot;
- final `DecisionID`.

### D1O-07 canonical identity — PASS

For D1 Opportunity execution, fresh LTF Re-Entry owns execution identity:

`RE_ENTRY | direction | identity timeframe | ConfirmationCandle`

H1+M15 same cluster uses H1 as structural identity owner. M15-only uses M15 identity.

`D1OpportunityCycleID`, family and source attribution remain metadata and are not part of the canonical LTF sequence hash.

### M16 — PASS

Before validation M16 requires:
1. no blocking opposite conflict;
2. current D1 authority to match the frozen snapshot;
3. exact component owner identity/freshness to remain valid;
4. candidate expiry not exceeded.

A stale or changed D1/component owner cannot silently continue to execution.

### M17 — PASS

SL/TP source resolution remains source-owned:
- normal standalone Re-Entry -> H1 Re-Entry;
- D1 Opportunity Re-Entry -> H1 preferred, M15 fallback only when H1 is absent;
- REM -> H4 Re-Entry;
- RRE/REE -> D1 Re-Entry.

No D1 attribution metadata changes this source-component rule.

### Preflight/risk chain — PASS

`RunEntryPreflightAndExecute()` requires `DEC_VALIDATED` and preserves:

`ResolveExecutionReferencePrice -> ResolveApprovedInitialSLTP -> ValidateSLTP -> CalculateLotSize -> CheckRiskBeforeTrade -> FinalPortfolioGuard -> ProcessEntry`

No strategy family is manufactured downstream.

### M22 execution identity / idempotence — PASS

Execution duplicate identity is anchored by `SHORT_HASH(DecisionID)` in the broker comment prefix:

`BBMA|H:<execution-hash>`

The comment also persists the short sequence hash under `Q:`.

`FindExistingExecutionTicket()` and executed-history checks prevent the same DecisionID from being sent twice, including ambiguous/retry paths.

### M24 recovery — PASS

Recovery:
- extracts the execution hash from the broker comment;
- parses full metadata when available;
- rejects full-metadata identity mismatch;
- restores persisted execution/sequence hashes;
- rebuilds tombstones for live owned orders.

Therefore restart recovery preserves execution identity instead of generating a new D1-owned identity from attribution metadata.

## Residual runtime evidence

Static cross-module integrity is closed. Broker/demo evidence remains useful for:
- same fresh H1 LTF identity retaining the same execution hash while D1 CycleID/family attribution changes;
- M15-only D1 Opportunity identity;
- one execution hash never changing direction;
- restart recovery retaining the same persisted execution hash;
- validation-candle-to-order-open timing.

## Verdict

**D1O-07 focused M15 -> M16 -> M17 -> M22 -> M24 regression: PASS.**

No source-code correction is required from this gate.
