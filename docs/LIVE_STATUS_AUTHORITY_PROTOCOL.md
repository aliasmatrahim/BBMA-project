# BBMA Live Status Authority Protocol

Status: **MANDATORY GOVERNANCE FOR STATUS/SEQUENCING QUERIES**

Issue: #113

## Purpose

Prevent stale-but-authoritative-looking records from being reported as the current project/test/runtime state.

This protocol applies whenever a user asks for the `latest`, `current`, `next`, `active`, `status`, `what test`, `what step`, runtime state, release state, branch ownership, or what should be continued next.

Chat memory and prior assistant answers are navigation aids only. They are never status authority.

## Hard rule

Do **not** answer a live-status question after reading only one authoritative-looking artifact.

A status answer may be called `latest/current/next` only after the mandatory reconciliation below is complete.

If reconciliation cannot be completed deterministically, return:

`STATUS CONFLICT / VERIFICATION REQUIRED`

Never guess.

## Mandatory live-status preflight

### Gate 1 — Repository governance / branch ownership

1. Read the repository `README.md` on `main`.
2. Resolve the branch that currently owns governance, implementation/source, and the relevant workstream.
3. Do not assume `main`, `d1-owner-dev`, or any remembered branch is the current work owner.

### Gate 2 — Canonical current-state records

Read the current owner branch copies of:

- `blueprint/CURRENT.md`;
- `blueprint/MASTER_QUEUE.md`;
- relevant contracts/decisions when status depends on them.

Record their apparent active step and any reconciliation date/timestamp they expose.

These files are necessary but **not sufficient** for a `latest` answer because active stacked branches/PRs or later owner decisions may be newer.

### Gate 3 — Repository delta / freshness sweep

Before answering, inspect at minimum:

1. open PRs relevant to the project/workstream, ordered by most recently updated;
2. recent repository commits, especially on active/scoped branches;
3. relevant open and recently closed issues;
4. issue/PR comments newer than the canonical current-state record or older candidate status;
5. head SHA/build identity for the newest relevant active candidate.

A newer stacked Draft PR is not automatically canonical production source, but it can be the authoritative **current work/test candidate**. Distinguish those concepts explicitly.

### Gate 4 — Supersession scan

Search the newer evidence for explicit sequencing/status language such as:

- `supersedes`;
- `stopped` / `STOPPED`;
- `replaced`;
- `deferred`;
- `blocked` / `unblocked`;
- `inactive`;
- `closed`;
- `not authorized`;
- `next safe action`;
- `active queue`;
- `current workstream`;
- `implementation-first`;
- `ready for collection`;
- `no merge` / `no activation`.

A later explicit owner sequencing decision overrides older scheduling text for **what is active next**. It does not retroactively rewrite the historical PASS/FAIL result of an older test.

### Gate 5 — Separate the four clocks

Never collapse these into one statement:

1. **Latest project/test-plan update** — newest governance/plan/commit defining what should be tested.
2. **Latest actual test attempt** — newest runtime/tester/demo execution attempt with attributable evidence.
3. **Latest valid PASS evidence** — newest completed test that actually produced sufficient PASS evidence.
4. **Next required test** — the next action after applying dependency, authorization, and supersession rules.

If the user asks `latest test`, determine which of these is intended from context; when ambiguity matters, state all four briefly instead of silently choosing one.

## Timestamp and identity requirements

Before using `latest/current/next`, capture enough identity to make the claim auditable:

- branch;
- PR/issue when relevant;
- head commit SHA;
- visible EA build/property when source-bearing;
- timestamp of the decisive commit/comment/run;
- test/run ID when applicable;
- result class: `PASS`, `FAIL`, `INCOMPLETE`, `BLOCKED`, `NOT_RUN`, `WAITING_FOR_SETUP`, or `WAITING_FOR_ORGANIC_SIGNAL` as defined by the owning record.

When reporting time to the user, preserve the source timestamp and convert to Malaysia time (`Asia/Kuala_Lumpur`, UTC+8) when useful. Do not confuse a document date with an actual runtime timestamp.

## Evidence precedence for live status

For scheduling/status only, use this reconciliation order:

1. explicit newer owner sequencing/authorization decision;
2. current active/scoped PR head and its linked issue/records;
3. current owner-branch `CURRENT.md` / `MASTER_QUEUE.md`;
4. older issue/PR/audit history;
5. chat memory.

This ordering is **not** Strategy-Core source precedence. Strategy semantics remain governed by `docs/references/SOURCE_INDEX.md` and the accepted Core/contracts.

## Fail-closed conditions

Return `STATUS CONFLICT / VERIFICATION REQUIRED` instead of a definitive latest/current/next claim if any of these remain unresolved:

- CURRENT/MASTER_QUEUE says one active step while a newer owner decision explicitly stops or replaces it;
- a newer PR exists but its relationship to the canonical branch/workstream cannot be established;
- build/source identity of the running or tested EA is unknown;
- a plan/checklist exists but no actual tester/runtime evidence exists;
- a workflow is marked failed but created zero executable steps or otherwise produced no attributable test evidence;
- timestamps identify only documentation/commit activity, not an actual test attempt;
- historical evidence is being mistaken for current workstream authority.

## Minimum response contract

For a simple status question, answer compactly but internally verify the full protocol.

When the user asks to confirm/double-check, include:

- `Current work/test candidate:` branch/PR/build;
- `Decisive timestamp:` exact date/time;
- `Latest actual test evidence:` timestamp + result;
- `Next required step:` one action;
- `Superseded:` only when an older step is materially likely to cause confusion.

## Regression example — R1 vs C3

An old R1 record can remain detailed and historically correct while a newer owner decision stops R1 as the current workstream and later stacked implementation/test PRs move the project to C3/build 4.72.

Under this protocol, reading the R1 issue alone can never justify the statement `R1 is the latest/current test`. The delta/freshness and supersession gates must be completed first.

## Scope boundary

This protocol changes governance/status resolution only. It does not change BBMA Strategy Core, candidate/decision logic, risk, lot sizing, execution, lifecycle, D1TPW, C044, NMJE authority, or release authorization.
