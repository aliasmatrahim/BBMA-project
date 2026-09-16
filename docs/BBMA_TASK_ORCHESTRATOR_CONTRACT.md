# BBMA Task Orchestrator Contract

Status: **PROPOSED GOVERNANCE CONTRACT**  
Scope: task selection, execution continuity, checkpointing, model routing and closure.  
Issue: #148  
This contract does not change BBMA Strategy Core, M01-M27/M12N ownership, EA source, release state or trading behaviour.

## 1. Purpose

Make BBMA development quota-resilient and state-driven rather than chat-driven.

The orchestrator must always optimize for:

**correctness -> evidence -> architecture integrity -> minimum regression -> traceability -> progress**.

Chat text and memory are navigation aids only. Live repository/system artifacts remain authoritative.

## 2. Authority and preflight

Before selecting or resuming any material task, resolve the live state in this order:

1. GitHub governance and current branch ownership.
2. `README.md`, active `CURRENT.md` and `MASTER_QUEUE.md`.
3. Task-specific issue/PR/report/checkpoint and live Git/worktree state.
4. For Strategy-Core work: `SOURCE_INDEX.md` -> routed evidence -> accepted Core -> contracts/decisions.
5. Current canonical source and relevant compile/runtime/test evidence.
6. Chat memory only after the above, and never as authority.

If live artifacts disagree with an older report/chat claim, the live artifacts win and the discrepancy must be recorded.

## 3. Task selection gate

Select only work that is currently eligible.

A task is eligible only when:

- its owner branch/layer is known;
- required predecessors satisfy their exit criteria;
- no higher-authority HOLD/UNRESOLVED/SOURCE CONFLICT blocks it;
- the task does not silently widen Strategy Core or architecture;
- required environment/tooling is available, or the task can progress safely without it.

If the user explicitly requests a task that is not yet eligible, do not silently skip prerequisites. Execute the smallest prerequisite/remediation/verification task first and preserve the requested target as pending.

Priority is taken from the live queue after eligibility is established. Priority never overrides a failed dependency gate.

## 4. Atomic task sizing

Default unit of work: **maximum medium-sized atomic task**.

An atomic task must:

- have one technical purpose;
- have explicit scope and exclusions;
- end at an independently verifiable evidence boundary;
- have clear exit criteria;
- avoid unrelated refactors or cleanup;
- be resumable without reconstructing project history.

Split a task when source adjudication, implementation, compile, runtime or unrelated modules can be verified independently. Do not split merely for ceremony when separation adds no validation value.

## 5. Task state model

Execution phase:

`PENDING -> PREFLIGHT -> IN_PROGRESS -> VALIDATION -> CLOSED`

Closure/result classifications:

- **PASS** — all mandatory exit criteria have evidence.
- **FAIL** — required validation ran and failed.
- **BLOCKED** — a real dependency/environment/permission/physical action prevents progress.
- **NOT VERIFIED** — a claim exists but evidence is insufficient.
- **HOLD / UNRESOLVED / SOURCE CONFLICT** — semantics or authority cannot be made deterministic safely.
- **NOT RUN** — a specific required validation has not been executed; this is never PASS.

Partial execution is not completion.

## 6. Aggressive checkpoint policy

Create or refresh a compact checkpoint after every expensive or high-risk boundary, including where applicable:

- accepted source/Core adjudication;
- material code patch completion;
- native MetaEditor compile;
- targeted regression/test batch;
- Strategy Tester or runtime evidence capture;
- long transcription/download/data batch milestone;
- remote process launch whose result may outlive the chat session;
- pre-commit/savepoint boundary;
- before stopping because of quota/session/tool instability.

Checkpoint target: **<= 40 lines**.

It must record at minimum:

- task/roadmap ID and phase;
- branch/commit/worktree or artifact identity;
- latest verified completed step;
- current partial output/process state;
- validation status;
- unresolved blocker/HOLD items;
- exact next safe action.

Do not overwrite historical checkpoints when a new continuation checkpoint is required.

## 7. Interruption and resume

After quota exhaustion, disconnect, hang, crash or unexpected stop:

1. Re-read the latest task prompt/report/checkpoint.
2. Verify live files, Git state, processes, logs and partial outputs.
3. Determine the latest VERIFIED boundary.
4. Classify remaining work as COMPLETED / IN PROGRESS / PENDING / BLOCKED / NOT STARTED / NOT VERIFIED.
5. Reuse valid partial outputs.
6. Verify a process is not still running/progressing before starting a duplicate.
7. Continue only the unfinished portion of the same task.
8. Re-enter roadmap selection only after the interrupted task satisfies its original closure gate.

Never redo expensive completed work solely because the chat session changed.

## 8. Model routing

Use the lowest reasoning level that can safely satisfy the task; escalate when ambiguity or impact increases.

| Work type | Default routing |
| --- | --- |
| Mechanical extraction, formatting, manifest/report normalization | routine/light model |
| Repo inspection, straightforward documentation, deterministic comparisons | standard/medium reasoning |
| MQL4 implementation, cross-module debugging, regression reasoning | high reasoning |
| Strategy-Core adjudication, source contradiction, architecture ownership conflict, difficult causal/runtime analysis | high/xhigh adjudication model |

Current product labels may change; choose the closest available equivalent. Explicit roadmap/user model routing overrides the default unless it is technically incapable of the required task.

Do not spend XHigh-class reasoning on mechanical work that has deterministic tooling.

## 9. Execution and validation discipline

Execution must use the smallest authorized change and preserve unrelated work.

For EA source changes, the normal evidence chain remains:

`static/cross-module -> native compile -> targeted regression -> runtime/test evidence as required`.

For Strategy-Core changes/reviews, the normal authority chain remains:

`SOURCE_INDEX -> routed evidence -> accepted Core -> contract/Blueprint -> code -> validation`.

Long-running computation should run on G40/local tooling when appropriate; ChatGPT orchestrates, inspects and validates the resulting artifacts rather than requiring one chat session to remain alive.

## 10. Git/savepoint rule

Use Issue -> scoped branch -> smallest change -> Draft PR when repository workflow requires isolation.

Before staging/committing locally, verify the current branch and working tree. Preserve unrelated/uncommitted work. Stage only exact task-owned files and inspect the staged diff before commit.

Never automatically force-push, merge, delete branches, destructively reset, deploy, enable production trading, or rewrite project history.

A documentation-only orchestrator change does not require an EA build/version increment.

## 11. Closure gate

A task may close only when:

- required outputs exist and are attributable;
- all mandatory exit criteria are evaluated;
- validation statuses are recorded truthfully;
- unresolved limitations are carried forward;
- report/checkpoint identifies the final branch/commit/artifacts;
- the next safe step is derived from the actual result.

Next-step rule:

- PASS -> next eligible roadmap task.
- FAIL -> smallest corrective task.
- BLOCKED -> smallest unblock task.
- NOT VERIFIED -> evidence-verification task.
- NOT RUN -> required validation task.
- HOLD/UNRESOLVED/SOURCE CONFLICT -> evidence/adjudication task; no executable rule invention.

## 12. User interaction boundary

Proceed continuously through safe, authorized work. User intervention is required only for genuine gates such as explicit strategic approval, credentials, physical action, destructive approval, unavailable dependency, or unresolved BBMA semantic conflict.

The orchestrator must not stop merely to restate a plan when the next safe action is already determined.
