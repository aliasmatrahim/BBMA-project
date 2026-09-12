# BBMA Model Routing Policy

**Status:** ACTIVE ROADMAP GOVERNANCE  
**Scope:** model selection and escalation for BBMA Professional EA roadmap work  
**Authority boundary:** this file governs work allocation only. It does not override `PROJECT_INSTRUCTIONS.md`, `docs/references/SOURCE_INDEX.md`, accepted Strategy Core, active contracts/decisions, current EA source, runtime evidence, or release gates.

## 1. Purpose

Model choice must not depend on chat memory or task size alone. Every substantive roadmap task must pass a **Model Routing Gate** before final analysis or mutation, and the gate must be re-evaluated whenever new evidence materially increases semantic, architectural, or regression risk.

Routing is based on **decision risk**, not workload size. A large mechanical task may remain on a lower tier; a small task that decides executable BBMA semantics may require Astra.

## 2. Routing outcomes

### `SOL HIGH DEFAULT`
Use Sol High for substantive BBMA work when the governing evidence/contracts are already deterministic and the task does not require unresolved semantic adjudication.

Typical examples:
- repository preflight and state reconciliation;
- accepted-Core-to-code compliance audit;
- cross-module review where ownership is already defined;
- diagnosis of a confirmed implementation defect;
- smallest authorized fix under an accepted contract;
- static/regression review;
- Strategy Tester/runtime evidence analysis where no new BBMA rule is being inferred;
- documentation and queue reconciliation requiring engineering reasoning.

### `ASTRA RECOMMENDED`
Astra is useful but not mandatory when complexity is unusually high, context is very long, or multiple evidence chains must be compared, while the final decision remains reversible and does not require unresolved BBMA semantic adjudication.

Sol High may continue and conclude the task if the result remains deterministic and all active contracts/evidence agree.

### `⚠️ ASTRA REQUIRED — JANGAN STEP DOWN`
Astra is mandatory for the **final adjudication/decision** when one or more hard triggers in Section 4 are present.

When this state is reached:
- the user-facing update must display the exact marker `⚠️ ASTRA REQUIRED — JANGAN STEP DOWN` prominently;
- state the precise trigger and affected roadmap item;
- lower-tier models may continue evidence collection, indexing, diffing, or mechanical validation;
- lower-tier models must not finalize the disputed semantic/architecture decision;
- no executable Strategy-Core rule or architecture authority change may be implemented from the unresolved lower-tier conclusion.

## 3. Mandatory Model Routing Gate

Before substantive work on a roadmap item, evaluate:

1. **Scope** — mechanical, evidence, strategy, architecture, code, runtime, release, or deployment.
2. **Authority clarity** — whether current source/Core/contracts already determine the answer.
3. **Evidence ambiguity** — whether material sources conflict or support more than one plausible reading.
4. **Semantic risk** — whether the decision can change BBMA entry, exit, validity, lifecycle, timing, MTF authority, or executable behaviour.
5. **Architecture breadth** — whether ownership/lifecycle contradictions span multiple modules or layers.
6. **Reversibility/regression risk** — whether a wrong decision could create broad or hidden behavioural regression.
7. **Determinism** — whether Sol High can reach one evidence-backed conclusion after mandatory retrieval/preflight.

The gate result must be one of:

- `MODEL GATE: SOL HIGH DEFAULT — PROCEED`
- `MODEL GATE: ASTRA RECOMMENDED — OPTIONAL ESCALATION`
- `MODEL GATE: ⚠️ ASTRA REQUIRED — JANGAN STEP DOWN`

## 4. Hard Astra triggers

Final adjudication is **Astra required** when any of the following is true:

1. **Unresolved source conflict affects executable semantics.** Two materially relevant BBMA evidence sources conflict and choosing either outcome would change executable Strategy Core.
2. **Multiple plausible Core interpretations remain.** Mandatory retrieval is complete but two or more reasonable semantic readings remain and a decision is required.
3. **Cross-module authority/lifecycle contradiction.** Resolving the issue may move, duplicate, remove, or redefine authority/ownership across multiple modules or signal-lifecycle stages.
4. **Core-versus-contract-versus-code adjudication is non-deterministic.** The mismatch classification itself changes what is considered canonical behaviour.
5. **A HOLD/UNCERTAIN/UNRESOLVED item would need promotion.** Any proposal to turn unresolved evidence into executable logic requires Astra-level adjudication plus the normal project approval path; Astra alone does not authorize the rule.
6. **High-regression architecture decision.** The proposed resolution can alter processing clock, closed-candle semantics, MTF authority, signal lifecycle, risk/execution boundary, restart ownership, or cross-pair state isolation and no single accepted contract already dictates the fix.
7. **Sol High cannot reach a unique evidence-backed conclusion.** After the mandatory preflight/retrieval sequence, the result remains materially non-deterministic.
8. **Release gating contains an unresolved semantic/architecture dispute.** A release decision must not bury an unresolved Core/ownership conflict under passing compile/runtime evidence.

## 5. Cases that do not require Astra by themselves

The following are not automatic Astra triggers when the governing rule is already accepted and deterministic:

- task is long or has many files;
- native MQL4 compile;
- static checks;
- running existing regression tests;
- collecting runtime logs;
- reproducing a confirmed bug;
- implementing a smallest fix already dictated by an accepted contract;
- build/version identity updates;
- telemetry-only work that does not change authority;
- queue/status/documentation updates;
- mechanical transcript cleanup or evidence indexing.

## 6. Mid-task escalation rule

The Model Routing Gate is continuous, not one-time.

A task that starts as Sol High must be reclassified immediately if new evidence activates a hard trigger. Do not finish the disputed decision first and escalate afterward.

Required transition format:

`MODEL GATE CHANGED: SOL HIGH → ⚠️ ASTRA REQUIRED — JANGAN STEP DOWN`

Then record:
- triggering evidence/finding;
- affected roadmap item;
- what Sol High may safely continue;
- what final decision is blocked pending Astra.

## 7. Roadmap integration

`docs/governance/EA_COMPLETION_ROADMAP.md` must carry a `MODEL GATE` for every roadmap work item. Phase-level model labels are advisory only; the per-item gate and this policy control escalation.

Before beginning or resuming a roadmap item:

`live repository/governance → roadmap item → MODEL_ROUTING_POLICY.md → SOURCE_INDEX when strategy-relevant → relevant evidence/Core/contracts → current code/runtime evidence → Model Routing Gate → work`

If the task is resumed in a new chat, the gate must be re-read/re-evaluated from repository state rather than assumed from prior conversation memory.

## 8. User-facing escalation requirement

When Astra is mandatory, do not bury the recommendation in a normal status paragraph. Use this exact visible heading:

**⚠️ ASTRA REQUIRED — JANGAN STEP DOWN**

Immediately state:
- `TASK:` roadmap ID/title;
- `WHY:` hard trigger(s);
- `SOL CAN CONTINUE:` safe evidence/mechanical work, if any;
- `BLOCKED UNTIL ASTRA:` the exact final adjudication or mutation that must not proceed on the lower tier.

`ASTRA RECOMMENDED` must remain clearly distinct from `ASTRA REQUIRED`; recommended escalation is not a blocking gate.

## 9. Safety boundary

Model routing never overrides project authority. Astra may provide more reasoning headroom, but it cannot:
- invent a BBMA rule;
- promote HOLD/UNCERTAIN evidence by itself;
- bypass source precedence;
- override accepted contracts without the required decision/change-control process;
- replace compile/runtime evidence;
- authorize merge, deployment, or trading without the normal project gates.
