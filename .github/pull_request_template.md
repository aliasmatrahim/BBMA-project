# BBMA EA Pull Request

Closes #

## Scope
- Affected module(s):
- Change type: bug fix / runtime fix / architecture / documentation / CI-tooling / release
- Source or governance branch affected:

## Problem
Describe only the concrete problem this PR solves.

## Solution
Describe the smallest change made and why it is sufficient.

## Architecture impact
- [ ] No module ownership changes.
- [ ] Closed-candle / timing rules remain intact.
- [ ] M15 remains the sole processing clock where required.
- [ ] Candidate/confirmed/selected/executed lifecycle boundaries remain deterministic.
- [ ] Risk modules do not create trading signals.
- [ ] Execution modules do not recreate upstream strategy logic.
- [ ] Multi-pair state and symbol-specific data remain isolated.
- [ ] No new RSI/MACD/Stochastic/ADX/news/session/correlation trading logic was introduced.
- [ ] Any intentional strategy or ownership change has an explicit decision/contract update in this PR.

## Validation evidence
Record only evidence actually produced.

- Native MetaEditor compile: PASS / FAIL / NOT RUN
- Compile errors: 
- Compile warnings: 
- Static/invariant checks: PASS / FAIL / NOT RUN
- Runtime/smoke evidence: PASS / FAIL / NOT RUN
- Relevant workflow/run or audit record:

## Regression check
- [ ] Existing callers/consumers reviewed.
- [ ] Duplicate-entry / duplicate-signal risk reviewed where relevant.
- [ ] Pool/index/state lifecycle reviewed where relevant.
- [ ] Restart/recovery behavior reviewed where relevant.
- [ ] No unrelated files or behavior changed.

## Source-of-truth sync
Check every item that applies.

- [ ] `PROJECT_INSTRUCTIONS.md` remains consistent.
- [ ] `blueprint/contracts/` remains consistent.
- [ ] `blueprint/decisions/` updated if an approved decision changed.
- [ ] `blueprint/CURRENT.md` / `blueprint/MASTER_QUEUE.md` updated if project status changed.
- [ ] If project/test/runtime sequencing changed, `docs/LIVE_STATUS_AUTHORITY_PROTOCOL.md` reconciliation was performed and superseded steps were identified.
- [ ] `blueprint/source/EA_RELEASE_IDENTITY.json` / release history updated if release identity changed.

## Reviewer decision
Expected outcome: MERGE / HOLD / DO NOT MERGE

> Do not mark checks as PASS without evidence. A small correct PR is preferred over a broad rewrite.