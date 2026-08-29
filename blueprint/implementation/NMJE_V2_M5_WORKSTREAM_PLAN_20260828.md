# NMJE v2 / M5 Isolated Workstream Plan — 2026-08-28

## Branch and dependency

- Branch: `nmje-v2-m5-dev`
- Starts from verified N3 4-TF baseline lock `3dd5245e5779b8e0b912010a3120370e609a4222`.
- Must remain isolated from PR #97 source work.
- Issue #101 is the authoritative accuracy queue.
- No source edit occurs in this preparation commit.

## Stage A — contract and regression harness

Status: COMPLETE (local deterministic/static evidence PASS; GitHub runner
availability remains separately unclassified).

1. Freeze the 4-TF baseline identity fixtures.
2. Define M5 node/event schema without wiring it into the processing loop.
3. Define immutable parent chain fixtures through the D1 epoch.
4. Add fail-closed tests for stale-child migration, restart/recovery, and ordinary refresh stability.
5. Add static authority tests prohibiting M5 execution, rejection, ranking, and clock ownership.

Exit gate: deterministic fixtures and static firewall PASS; no EA source modification.

## Stage B — P1 lineage schema

Status: COMPLETE — schema-only source materialization; no processing wiring.

1. Add provenance-only M5 identity and ParentEventID/JourneyID rules.
2. Model parent transition and continuation/re-arm semantics.
3. Verify the same closed-candle inputs produce the same identity after restart.
4. Verify stale children cannot attach to a new parent epoch.

Exit gate: P1 tests PASS and explicit review of the schema boundary.

## Stage C — P2/P3 shadow context

Status: C2 COMPLETE — canonical M5 Re-Entry/Extreme context is classified and
bound to immutable parent/journey identity on the existing M15 clock. The
result is shadow-only and has no candidate or decision-path influence.

1. Materialize M5 closed-candle observation only. COMPLETE.
2. Derive canonical relation + reason without a second clock. COMPLETE.
3. Add journey-coherence metadata for equal-eligibility arbitration only.
4. Prove a temporary M5 conflict cannot reject the sole valid M15 candidate.
5. Keep all results diagnostic/shadow-only.

Exit gate: authority matrix, replay/recovery, frequency-preservation, and native 0E0W evidence PASS.

## Stage D — P4 attribution

Status: D1 COMPLETE — base journey and M5 shadow metadata are frozen after M15
selection, persisted by stable execution identity, recovered independently, and
joined to exact closed-order outcome telemetry. Attribution remains non-authoritative.

1. Persist base-path and M5 shadow metadata using exact decision/execution identity. COMPLETE.
2. Join attributes to exact closed-trade outcomes. COMPLETE.
3. Track coherence, M5 state, maturity, density, conflict subtype, and entry displacement.
4. Make no live decision change.

Exit gate: deterministic attribution and replay completeness PASS.

## Stage E — P5-P11 accuracy research

Status: E1 / P5 COMPLETE — deterministic conflict-family telemetry is attached
to base and M5 shadow relations, persisted with P4 attribution, and emitted with
closed outcomes. Canonical relations and live decisions remain unchanged.

Status: E2 / P6 COMPLETE — categorical BBMA journey maturity is captured for
base and M5 contexts, persisted with attribution, and emitted with outcomes.
No generic score or minimum-maturity gate is introduced.

Status: E3 / P7 COMPLETE — a five-bit D1/H4/H1/M15/M5 support-presence mask,
its bit count, and the already-selected candidate's existing requirement and
sequence completeness are persisted for outcomes. They do not affect selection.

Status: E4 / P8 COMPLETE — the prior canonical observation parent is retained
only while its exact EventID and D1 epoch remain current. Parent changes are
attributable transitions; no time-based decision delay or trade suppression exists.

Status: E5 / P9 COMPLETE — the user-verified SL/TP semantic-source mapping is
retained unchanged and protected by an audit-only static regression. Source
selection is explicit by candidate family/timeframe and cannot fall back to
component processing order. EA source, build, geometry, and authority are unchanged.

Status: E6 / P10 COMPLETE — exact source-confirmation, validation-entry,
broker-fill, and structural-anchor prices are joined under durable execution
identity with directional pip deltas and descriptive classification. P10 runs
after broker ticket selection and cannot filter, delay, reject, rank, or resize.

Status: E7 / P11 COMPLETE — forward closed-M15 transitions and exact
Journey/Parent/D1 identity distinguish first, continuation/re-arm, new journey,
and unresolved provenance. A durable pair checkpoint makes same-candle replay
and restart classification fail closed instead of assuming newest/earliest.

P5-P11 are implemented as correctness, provenance, or shadow telemetry. No
activation, strategy-policy change, hard gate, or eligible-trade reduction is
authorized.

## Mandatory evidence per source-bearing stage

- visible EA build/header increment;
- prepared unit/selftests;
- N3/NMJE static authority and identity guards;
- replay and recovery fail-closed regression;
- deterministic baseline comparison;
- native MT4 MetaEditor 0E0W;
- no activation marker;
- draft PR and explicit evidence summary.

## Stop boundaries

Stop before:

- any M5 processing-clock or trade authority;
- any rule that rejects the sole valid candidate;
- any change to D1TPW or C044;
- any W1, M30, or primary M1 addition; these are intentional exclusions, not
  backlog, and require new explicit user strategy-scope approval;
- any activation or merge decision;
- any strategy-policy change lacking explicit approval and attributable evidence.

