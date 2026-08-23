# KIV — Home Course D1 Major Trend / Transition

Status: **KIV / DO NOT IMPLEMENT YET**
Date: 2026-08-24
Branch owner: `blueprint-dev`

## Reason for KIV
Parallel project work is currently running. This item is frozen to avoid concurrent edits or strategy/code drift while another chat/workstream may be operating on the same branch.

## Evidence/audit already completed
- `blueprint/audits/BBMA_HOME_COURSE_RECONCILIATION_AUDIT_20260824.md`
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`
- `blueprint/audits/D1_MAJOR_TREND_TRANSITION_AUDIT_20260824.md`

## Current reconciled finding
- D1/MA50 = major-trend authority/context.
- H4 = immediate structural/setup parent for the intraday H1 chain; these roles are not identical.
- Home Course evidence strengthens D1 authority and states that conflicting H4 direction should not automatically override D1 major trend.
- Do **not** reduce the implementation to `D1 Close > MA50 = BUY` / `D1 Close < MA50 = SELL` alone.
- Existing source also supports MA50 slope/ascending-descending context and MA50 break as reversal/continuation context.
- Use closed D1 candles for Daily context; do not use an unfinished D1 candle as final authority.

## Unresolved implementation decision
When D1 crosses/breaks MA50 but MA50 slope/structure has not yet aligned with the opposite direction, determine the deterministic `D1_TRANSITION` policy.

Candidate policy currently preferred by audit, but **NOT LOCKED / NOT IMPLEMENTED**:
- `D1_MAJOR_BUY`
- `D1_MAJOR_SELL`
- `D1_TRANSITION`
- During `D1_TRANSITION`, block new entries until major-trend authority becomes deterministic again, rather than immediately flipping owner or silently retaining an unsupported direction.

## Mandatory resume procedure
Before any code change:
1. Re-read the three records above and the latest Strategy Core Source of Truth.
2. Reconcile any commits made by parallel chats/workstreams after this KIV record.
3. Re-audit current `BBMA_EA.mq4` rather than assuming the previous snapshot is still current.
4. Resolve/lock the exact D1 transition predicate and transition entry policy from source evidence + minimal deterministic project mapping.
5. Update Source of Truth / decision records first if required.
6. Only then modify EA code and repeat static regression + native MetaEditor compile/runtime gates as applicable.

## Protection rule
Until this KIV is explicitly resumed, do not modify D1/H4/MTF strategy authority, H4 owner semantics, or D1 major-trend execution gating based solely on the Home Course findings.
