# BBMA User-Facing Communication Rules

**Status:** MANDATORY PROJECT COMMUNICATION GOVERNANCE

This document controls only how BBMA project progress is explained to the user. It does **not** change EA strategy logic, BBMA Core rules, architecture, module ownership, testing standards, safety controls, or engineering rigor.

## 1. Plain-language default

All normal project updates to the user must be written in simple language suitable for a non-developer.

- Avoid developer jargon, acronyms, and implementation terminology when they are not necessary.
- Do not assume the user understands GitHub, CI/CD, runtime, state machine, regression, telemetry, lifecycle, or similar technical terms.
- When a technical term is necessary, immediately explain what it means in ordinary language.
- Do not reduce the technical depth of the actual work. Simplify only the explanation presented to the user.

## 2. Default progress format

For meaningful BBMA progress updates, use this user-facing structure whenever practical:

1. **Apa saya buat** — explain what was done in simple terms.
2. **Kenapa saya buat** — explain why it matters to the EA/user.
3. **Keputusan** — state whether it passed, failed, remains uncertain, or needs more work.
4. **Apa seterusnya** — explain the next meaningful step.

Keep the visible explanation concise unless the user asks for full technical detail.

## 3. Technical accuracy must be preserved

Plain-language reporting must never hide or soften an important problem.

- A failure must still be called a failure.
- An incomplete test must not be described as complete.
- A compile pass must not be described as proof that the strategy is profitable.
- A simulated/offline result must not be presented as live-market proof.
- Uncertainty, unresolved evidence, or blocked work must be stated clearly.

## 4. Technical detail remains available

The underlying project work must continue to use the full technical standards required by `PROJECT_INSTRUCTIONS.md`, contracts, audits, tests, and source evidence.

If the user asks for technical detail, provide it. Otherwise, translate the result into plain language rather than exposing raw developer terminology unnecessarily.

## 5. No side effect on EA behaviour

This communication rule is presentation-only. It must not be used as justification to:

- simplify or weaken code reviews;
- skip tests;
- omit technical evidence from repository records;
- change BBMA Core behaviour;
- change architecture or module responsibilities;
- reduce compile/runtime/regression checks;
- alter risk, entry, exit, execution, or lifecycle logic.

**Required principle:**

> Full technical work in the background; clear non-developer explanation to the user.
