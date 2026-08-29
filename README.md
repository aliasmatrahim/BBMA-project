# BBMA Professional EA

Production-oriented MetaTrader 4 / MQL4 project using the established M01-M27 BBMA architecture, with M12N as the approved logical overlay between M12 and M13.

## GitHub is the source of truth

This repository stores the implementation, architecture contracts, decisions, runtime evidence, validation tooling, and release history used to develop and audit the EA.

### Current branch map

| Branch | Current role |
| --- | --- |
| `main` | Default branch for repository governance, dispatcher/tooling and GitHub Actions integration. |
| `d1-owner-dev` | Active implementation/source branch containing the EA source, detailed contracts, decisions, runtime evidence and project instructions. |

Current EA source:

`d1-owner-dev:blueprint/source/BBMA_EA.mq4`

The current dispatcher/native-compile workflows on `main` intentionally check out and validate source from `d1-owner-dev`. Do not assume that absence of `.mq4` on `main` means the EA source is missing.

## Canonical project records

On the active implementation branch, start with:

- `PROJECT_INSTRUCTIONS.md` - project governance and non-negotiable architecture rules.
- `blueprint/CURRENT.md` - current project state.
- `blueprint/MASTER_QUEUE.md` - active development queue.
- `blueprint/contracts/` - module/source contracts and ownership boundaries.
- `blueprint/decisions/` - explicit architecture/strategy decisions.
- `blueprint/source/BBMA_EA.mq4` - current EA implementation source.
- `blueprint/source/EA_RELEASE_IDENTITY.json` - release identity.
- `docs/DEVELOPMENT_VERIFICATION_RELEASE_HISTORY.md` - development verification/release history.

Historical patches, experiments and archived evidence are not automatically authoritative over active contracts/decisions.

## Development workflow

1. Create a structured GitHub Issue for the defect or intentional architecture change.
2. Create a scoped branch from the branch that owns the target.
3. Make the smallest correct change and preserve unaffected architecture.
4. Open a Draft PR using the repository PR template.
5. Run the existing specialized compile/static/runtime checks applicable to the change.
6. Review architecture and regression impact.
7. Merge only when required evidence is green and material review findings are resolved.
8. Keep the Issue, PR, decisions/contracts and release evidence linked so every change remains traceable.

See `docs/REPOSITORY_GOVERNANCE.md` for the full policy.

## BBMA architecture guardrails

Normal fixes must preserve the active contracts, including where applicable:

- closed-candle processing;
- M15 as the sole processing clock;
- deterministic signal lifecycle and duplicate suppression;
- strict module ownership boundaries;
- risk modules as risk/filter owners rather than signal generators;
- execution modules as executors of already-approved decisions;
- multi-pair state isolation and symbol-specific runtime data;
- MQL4 compatibility.

Strategy/ownership changes require an explicit architecture decision and contract update rather than a silent code change.

## Validation

The repository already contains specialized GitHub Actions for native MetaEditor compilation, static/runtime checks and architecture invariants. Prefer extending the canonical check that owns an invariant instead of adding redundant generic CI.

Never report a check as PASS unless evidence was actually produced.

## Repository protection status

`main` is currently not branch-protected. The intended final policy is PR-only integration with appropriate required checks. Branch protection must be enabled in GitHub repository settings/rulesets before it can be treated as enforced.
