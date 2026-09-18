# Q9 NMJE v2 P4 D1 Shadow Attribution Contract — 2026-09-19

Issue: #101
Stack base: verified Q9 Stage-C Build 4.88
Target build: 4.89 / V489_Q9_P4_SHADOW_ATTR_20260919
Status: ISOLATED / RESEARCH-ONLY / NO ACTIVATION

## Scope

Freeze the already-observed NMJE journey and M5 shadow metadata only after the canonical base decision reaches DEC_VALIDATED. If that decision later executes, bind the research payload to the existing execution hash, ticket, magic and broker open time, persist it independently, recover it after restart, and emit it with the exact selected closed order outcome.

## Authority boundary

P4 does not create or alter candidate eligibility, canonical comparison, M15 selection, M16 invalidation, risk, lot sizing, OrderSend parameters, C044/D1TPW lifecycle state, trade recovery state, close logic or dashboard authority.

Current-owner C044 remains active and authoritative for its approved lifecycle. P4 persistence runs only after canonical execution identity and lifecycle checkpoint work. P4 persistence failure is diagnostic only.

## Persistence

The BBXA1 terminal-GlobalVariable domain is ticket-scoped and additionally verifies:
- StrategyID / InstanceID namespace;
- magic number;
- broker open time;
- existing 16-character execution hash.

The commit marker V is written last. Missing/partial/mismatched records fail closed as attribution unavailable without changing trade state.

## Outcome attribution

The existing closed-order observer already verifies ticket, pair and magic before reporting realized net P/L. P4 adds JourneyHash, ParentEventHash and optional M5 shadow hashes/relations to that exact closed-order row.

No research field is consumed by an executable decision path.

## Exit gate

Require focused P4 static + persistence-model PASS, Stage-C/read-only regressions PASS, broker primitive counts unchanged, native MetaEditor 0E0W, isolated zero-trade runtime startup/recovery safety, and no activation/merge.
