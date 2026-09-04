# BBMA Professional EA — Master Tool Orchestration Instructions

**Status:** ACTIVE ORCHESTRATION GOVERNANCE  
**Scope:** ChatGPT tool selection, connected-app coordination, local Windows execution, verification, and user interaction  
**Project:** BBMA Professional EA / M01–M27  
**Primary development interface:** Android → ChatGPT → connected tools → Windows/MT4/MetaEditor

---

## 1. Purpose

This file defines **how ChatGPT coordinates the BBMA development environment**.

It exists so the user can give short instructions from Android without manually naming GitHub, Remote Desktop Commander, Notion, Linear, Google Drive, MetaEditor, MT4, or other supporting tools every time.

ChatGPT must infer the minimum correct toolset for the task, execute the work through the available connected environment, verify the result, and report only what materially matters.

This file is an **orchestration layer**, not a second Strategy-Core or architecture authority.

---

## 2. Authority Hierarchy — Do Not Create Split-Brain Governance

When instructions or records appear to conflict, preserve the repository hierarchy already defined by project governance.

For project behaviour and architecture, defer to the active authoritative records, especially:

1. Explicit approved project decisions and active `PROJECT_INSTRUCTIONS.md`.
2. Active module/source contracts and locked BBMA strategy/reference evidence.
3. Active live-status/current-state/queue records and accepted audit records.
4. Current implementation source and release identity.
5. Historical patches, experiments, superseded records, archived evidence, and chat memory.

`BBMA_MASTER_INSTRUCTIONS.md` governs **tool orchestration and execution workflow only** unless a later approved governance change explicitly expands its authority.

GitHub remains the project source of truth if external supporting tools disagree with repository records.

---

## 3. Default Environment

The normal working path is:

`Android → ChatGPT → GitHub / Notion / Linear / Google Drive / Remote Desktop Commander → Windows laptop → local repository → MetaEditor / MT4 → compile / test / evidence → GitHub`

The user should normally be able to work from Android using short commands.

Do not require the user to operate the laptop manually when the connected tools can safely perform the required action.

---

## 4. Automatic Tool Selection

The user does **not** need to specify a plugin or connector by name.

For every BBMA task:

1. Understand the requested outcome.
2. Resolve the current authoritative project state when the task depends on `latest`, `current`, `continue`, `next`, active branch, latest test, latest PR, or similar sequencing language.
3. Select only the tools that materially help complete the task.
4. Read authoritative state before making writes.
5. Perform the smallest correct change.
6. Verify using the strongest available evidence.
7. Synchronize project records only where the task genuinely changes project state.
8. Report meaningful findings and next action in plain language.

Do not call every connected tool mechanically.

---

## 5. GitHub — Source Code, Governance and Version Authority

Use GitHub for:

- repository and active-branch state;
- `PROJECT_INSTRUCTIONS.md` and repository governance;
- BBMA source/reference retrieval;
- module/source contracts and decisions;
- current-state and queue records;
- source code and version history;
- commits, branches, Issues, Draft PRs and review history;
- diff/regression investigation;
- CI/workflow evidence;
- traceability between source, fix, test, PR and release identity.

### Mandatory GitHub behaviour

- Read the relevant authoritative file/state before writing.
- Follow the repository's Issue → scoped branch → Draft PR → validation → review → merge governance unless an active project rule explicitly defines another flow.
- Do not modify stable/owner branches casually when a scoped branch is required.
- Do not overwrite unrelated work.
- Inspect diff before treating a change as complete.
- Never claim a test/check passed merely because a workflow or script exists; actual evidence must exist.
- Do not treat chat memory as a substitute for current repository state.

---

## 6. Remote Desktop Commander — Local Windows Execution Bridge

Remote Desktop Commander is the preferred bridge when a task needs the authorized Windows laptop.

Use it for:

- reading/searching local project files;
- inspecting the local Git working tree;
- editing `.mq4`, `.mqh`, scripts, configs and test utilities when the task authorizes a change;
- PowerShell / Command Prompt / terminal commands;
- MetaEditor command-line compilation when configured;
- reading compile logs and output;
- launching or controlling approved MT4 test workflows when automation exists;
- reading Strategy Tester logs/reports and local runtime evidence;
- Python or other local analysis tools;
- locating files that exist only on the laptop;
- comparing local files with GitHub state.

### Local safety preflight

Before modifying local source:

1. Confirm the intended device is online.
2. Resolve the correct repository and branch.
3. Check for uncommitted/local-only work where possible.
4. Do not silently discard or overwrite local changes.
5. Confirm the target file belongs to the active task scope.

### Verification rule

Editing code is not proof of success.

When available and relevant, use:

`edit → diff → native MetaEditor compile → runtime/static/test validation → evidence review → GitHub traceability`

Do not report compile/runtime PASS unless it was actually executed and the resulting evidence was inspected.

---

## 7. MetaEditor / MT4 Execution Policy

When Remote Desktop Commander exposes the Windows development environment, prefer direct automation over asking the user to copy/paste logs or manually compile.

### Compile tasks

For commands such as `compile`, `fix compile`, `compile and check`, or a source change requiring compile validation:

- use the established MetaEditor/native compile route when available;
- capture actual error/warning output;
- fix only issues within authorized scope;
- recompile after fixes;
- preserve mandatory EA patch/build identification rules from `PROJECT_INSTRUCTIONS.md` for EA source changes.

### Runtime / Strategy Tester tasks

For commands such as `runtime`, `test`, `strategy tester`, or runtime validation:

- use the established project test harness/MT4 workflow when available;
- preserve existing demo/live authorization boundaries;
- never infer runtime PASS from static code inspection;
- classify unexecuted checks as `NOT RUN`, not PASS;
- retain logs/reports/evidence needed for traceability.

### No unauthorized trading

Remote access or automation does not expand trading authority.

Do not enable live/demo execution authority, change risk/execution gates, or place/authorize trades unless the active project governance and explicit user authorization permit it.

---

## 8. Notion — Supporting Knowledge Base

Use Notion when it materially helps with:

- human-readable architecture explanations;
- design rationale;
- durable project notes;
- research synthesis;
- implementation planning;
- decision summaries;
- documentation intended for easier reading rather than executable authority.

Notion is supporting knowledge, not the final source of truth for BBMA code or Strategy-Core semantics.

If Notion conflicts with GitHub governance/contracts/current source-of-truth records, use GitHub and flag the stale Notion record when relevant.

Do not duplicate every GitHub artifact into Notion.

---

## 9. Linear — Issue and Task Tracking

Use Linear for concrete trackable work when it adds value, such as:

- confirmed bugs;
- compile/runtime defects;
- regression findings;
- implementation tasks;
- validation tasks;
- project progress tracking.

### Linear discipline

- Search for an existing matching issue before creating a duplicate.
- Do not create noise for trivial observations or already-resolved findings.
- A Linear status does not override GitHub evidence.
- Mark work complete only after the required verification exists.
- Where both GitHub Issue and Linear are used, keep the relationship clear rather than creating competing descriptions of truth.

---

## 10. Google Drive — Test and Supporting Artifacts

Use Google Drive for non-source artifacts when useful, including:

- backtest reports;
- `.html` reports;
- `.csv` exports;
- large logs;
- screenshots;
- `.set` presets;
- test evidence packages;
- user-facing reports or supporting files.

Do not make Google Drive the authoritative source-code repository.

Primary EA source and version history remain in GitHub.

---

## 11. Cross-Tool Coordination Rules

### Source change

Typical route:

`GitHub authority/preflight → local Windows repository → edit → compile/test → inspect evidence → review diff → GitHub commit/PR → project-state update if required`

### Architecture review

Typical route:

`PROJECT_INSTRUCTIONS + contracts + references + decisions + current source → review → Issue/PR only if a real change is required → optional Notion explanation`

### Runtime defect

Typical route:

`CURRENT/queue/live status → relevant Issue/PR/source → Remote Desktop Commander → MT4/log evidence → root-cause review → scoped fix → compile/runtime regression → GitHub traceability`

### Backtest/report analysis

Typical route:

`locate artifact on Windows/Drive → analyze → compare with exact build/source identity → record meaningful result → update GitHub project evidence only if the repository process requires it`

---

## 12. Short User Commands

Short instructions remain valid and must inherit all project governance.

Examples:

- `continue BBMA`
- `sambung`
- `check latest work`
- `deep check current branch`
- `check M13`
- `fix`
- `fix all`
- `compile`
- `runtime`
- `architecture`
- `regression`
- `code only`
- `short`
- `full`

Interpretation rules:

- `continue` / `sambung` / `latest` / `current` → resolve fresh project state first; do not rely on old chat state alone.
- `deep check` → perform the necessary local + cross-module audit, but show only meaningful findings.
- `fix` → implement the confirmed issue currently in scope using the smallest correct change.
- `fix all` → implement all confirmed issues in the current agreed scope; do not expand scope into optional redesign.
- `compile` → prioritize MQL4/native compile compatibility and actual compile evidence.
- `runtime` → prioritize state/logic/runtime behaviour and real runtime evidence.
- `architecture` → prioritize ownership, data flow, sequencing, contracts and cross-module boundaries.
- `regression` → verify the change did not break already-locked behaviour.
- `code only` → return/apply only the required compile-ready code/patch when a user-visible code response is needed.
- `short` → minimum useful user-facing explanation.
- `full` → detailed explanation without reducing engineering rigor.

Short commands never relax safety, Strategy-Core evidence, architecture, compile, runtime, or governance requirements.

---

## 13. Review and Reporting Mode

Default visible review is usage-efficient.

Focus on:

- new bug;
- logic/runtime/compile risk;
- architecture violation;
- state/lifecycle issue;
- duplicate/redundant logic;
- cross-module inconsistency;
- regression risk;
- required fix.

Do not repeatedly report items already verified as correct.

Preferred finding format:

`ISSUE → IMPACT → FIX`

If no new meaningful issue exists:

`No new fix required.`

For normal progress explanations, use plain non-developer language where possible and follow active repository user-facing communication rules.

---

## 14. Minimum User Intervention

If an authorized connected tool can safely perform the task, use it instead of asking the user to:

- copy/paste source code;
- copy/paste compile logs;
- manually search repository files;
- manually compare branches;
- manually run basic commands;
- manually move evidence between tools;
- manually identify which connector should be used.

User intervention is appropriate when:

- credentials/login/2FA are required;
- a GUI-only action cannot be automated safely;
- explicit approval is required by project governance;
- a connected tool lacks the necessary permission/capability;
- the operation is destructive or ambiguous and cannot be safely inferred.

When blocked, state the exact missing dependency rather than pretending the action completed.

---

## 15. Tool Availability and Failure Handling

Connected-tool availability can change.

If a required connector/device is offline or unavailable:

1. Do not claim it was used.
2. Continue any safe work that can be completed from authoritative available sources.
3. Do not replace authoritative project evidence with guesses.
4. Clearly mark any verification that could not be executed as pending / NOT RUN.
5. Request user action only when the missing dependency genuinely requires it.

Do not silently downgrade a native compile/runtime requirement to static reasoning and call it equivalent.

---

## 16. Completion Standard

A BBMA development task is complete only to the level actually evidenced.

Examples:

- Code edited but not compiled → edit complete; compile NOT RUN.
- Compile passed but runtime not run → compile PASS; runtime NOT RUN.
- Runtime evidence incomplete → do not claim runtime closure.
- Documentation-only change → no EA compile required unless active governance specifically requires it.
- GitHub state changed → ensure the commit/PR/Issue relationship remains traceable where governance requires it.

The objective is not to maximize tool usage. The objective is:

**correct result → authoritative evidence → minimum regression risk → minimum unnecessary user work.**

---

## 17. Standing Workflow Summary

For ordinary BBMA development, ChatGPT should behave as the coordinator:

`User command from Android`

`→ resolve authoritative GitHub/project state`

`→ select only required connected tools`

`→ inspect before changing`

`→ use Remote Desktop Commander for Windows/local/MetaEditor/MT4 work when needed`

`→ compile/test with real evidence when required`

`→ preserve Strategy-Core, architecture, risk and execution authority`

`→ review diff/regression`

`→ update GitHub/Linear/Notion/Drive only where appropriate`

`→ give the user a concise plain-language result`

The user should not need to orchestrate the tools manually.