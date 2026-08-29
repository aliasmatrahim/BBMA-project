# BBMA Core Perfection Queue — 2026-08-29

Status: **PLANNING / NO STRATEGY OR EXECUTION ACTIVATION**

## User decision lock

- Do not add a daily-loss limit or daily-loss trading gate.
- Keep same-currency concurrent-exposure control as `KIV`; it has no source,
  risk, candidate, or execution authority.
- Keep cooldown after a loss sequence or broker failure as `KIV`; it has no
  timer, suppression, delay, candidate, or execution authority.
- W1 and M30 remain intentionally unimplemented. Primary M1 remains
  intentionally excluded from NMJE authority.
- Do not add generic indicators, ML, news/session filters, or an additional
  processing clock as a substitute for canonical BBMA semantics.

Any KIV item requires a new explicit strategy/risk-policy approval before
source implementation. KIV does not mean approved backlog.

## Core-perfection queue

### C1 — Canonical BBMA truth tables and golden fixtures

Status: **C1-B COMPLETE** — C1-A locked the build-4.71 ownership map,
34 deterministic lifecycle transitions, BUY/SELL symmetry, exact REM/RRE/REE
topology, semantic-source mapping, and static authority boundary. C1-B adds 59
source-bound closed-candle price cases for Extreme, CSM, CSD/eCSD, Re-Entry,
retest, and MHV predicates. No EA source or strategy behavior changed. Native
MT4 execution and historical performance evidence remain C3 work.

Formally lock the candle-by-candle meaning, maturity, invalidation,
supersession, and ownership rules for Extreme, Momentum, MHV/MLV, Re-Entry,
CSD/eCSD/CSM, REM, RRE, and REE. Build deterministic golden fixtures for both
directions and every active timeframe. This is correctness work only; it must
not change geometry or opportunity frequency.

### C2 — End-to-end journey invariant audit

Status: **C2-A COMPLETE** — the build-4.71 D1/H4/H1/M15 journey is locked
through M15/M16/M17/M21/M19/M20/M22/M23/M24 with deterministic identity,
legal-transition, single-writer, broker-action ownership, and fail-closed
recovery regressions. No EA source, strategy, risk policy, or authority changed.
Native broker/restart evidence remains C4 work.

Prove that one immutable lineage connects D1 owner epoch, H4 journey, H1 setup,
M15 decision, M16 revalidation, M17 geometry, M21 sizing, M22 execution, and
M23/M24 lifecycle/recovery. Add static single-writer checks for every protected
state and broker action.

### C3 — Historical baseline-versus-shadow evidence

Run the native MT4 Strategy Tester on the available broker history and compare
the locked four-timeframe baseline with the NMJE/M5 shadow classifications.
Preserve pair, setup family, journey phase, spread, displacement, outcome,
drawdown, frequency, coverage, and uncertainty. Shadow results must not activate
or patch the EA automatically.

### C4 — Broker execution resilience matrix

Exercise digits, tick size, stop level, freeze level, spread expansion,
requotes, slippage, trade-context contention, disconnect/restart, partial
history, and duplicate-action prevention. Fail closed where identity or broker
state cannot be proven. Do not introduce a new BBMA signal filter.

### C5 — Lifecycle activation ladder

Validate one isolated change at a time: locked baseline, NMJE shadow, D1TPW
demo verification, then any separately approved limited NMJE policy, and only
later C044. Never activate D1TPW, NMJE execution authority, and C044 together.
Every rung requires rollback identity, native 0E0W, deterministic regressions,
and broker/demo evidence.

### C6 — Build and configuration provenance

Bind each run to visible EA build/header identity, source revision, symbol
mapping, broker properties, inputs/configuration fingerprint, history window,
and test mode. Detect configuration drift before interpreting results.

### C7 — BBMA decision explainability ledger

For each accepted or rejected candidate, emit one concise deterministic reason
chain using canonical BBMA owners and state transitions. The ledger is evidence
only and must not create scores, votes, or hidden filters.

### C8 — Multi-pair performance and determinism audit

Measure M15-cycle runtime, log/storage growth, Global Variable pressure, history
availability, and replay determinism across the supported pair set. Optimize
only after equivalence tests prove unchanged BBMA decisions and identities.

### C9 — Conditional NMJE limited-policy package

Only if observed evidence supports review, prepare a dated proposal for the
smallest reversible behavior. The preferred first candidate is equal-eligibility
tie-breaking between two or more already-valid candidates. NMJE must not reject
the sole valid M15 candidate. Implementation still requires explicit approval.

## Priority order

`C1 -> C2 -> C3 -> C4 -> C6 -> C7 -> C8 -> C5 -> C9`

C5 and C9 remain manual strategy/activation boundaries. The two risk items
listed as KIV remain outside this execution order.
