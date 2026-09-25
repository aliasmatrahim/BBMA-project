# NMJE V2 P2 Multi-Pair / Multi-Period Evidence Expansion — 2026-09-25

Status: VALIDATED / EVIDENCE EXPANSION COMPLETE / P2 ORDERING HOLD / NO EA FIX

Issue: #101
Owner base: d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de
EA: Build 5.15 / V515_NMJE_P2_TARGETLESS_REPLAY_20260925 / rev NMJE_P2_TARGETLESS_REPLAY_001_20260925
MQ4 SHA-256: B9F3876F61645B2F98009A4251A4142EDC7644ED728E41EDECA245FF1E243C45
Harness EX4 SHA-256: 56610EA60909A4E7893548D6E606448C1BC4FBCA3D66205686DD0580BAC0F6D5
Strategy-Core delta: NONE
Execution/risk authority delta: NONE

## 1. Objective

Expand the validated P2 counterfactual / targetless replay evidence beyond one GBPUSD August window without changing candidate ordering, risk/MM, execution, lifecycle ownership, M5 authority or Strategy Core.

Matrix:
- EURUSD, GBPUSD, USDJPY;
- January 2026 and August 2026;
- M15 Strategy Tester;
- exact Build 5.15 tester-only harness;
- one isolated pair per run with unique valid StrategyID/InstanceID.

No Q3/Q10 terminal was restarted or reused.

## 2. History provenance

For all three symbols, installed MetaQuotes-Demo HST coverage includes M1/M5/M15/H1/H4/D1 from 2006 through 2026-09-01, with H4/D1 through the last fully available 2026-08-31 bars.

Evidence: history_provenance.json.

An initial matrix attempt used StrategyID/InstanceID values above the EA contract maximum of 99. ValidateInputParameters() rejected those runs before strategy runtime. They were INVALID TOOLING RUNS, discarded, and not used as evidence. Runner-only IDs were corrected to valid unique values; EA source was not changed.

## 3. Valid 3x2 matrix result

Across six valid runs:

| Pair | Period | CF sets | Alternatives | Executions |
| --- | --- | ---: | ---: | ---: |
| EURUSD | 2026-01 | 9 | 16 | 34 |
| GBPUSD | 2026-01 | 4 | 5 | 34 |
| USDJPY | 2026-01 | 7 | 8 | 42 |
| EURUSD | 2026-08 | 1 | 1 | 26 |
| GBPUSD | 2026-08 | 3 | 6 | 14 |
| USDJPY | 2026-08 | 0 | 0 | 16 |

Aggregate:
- raw equal-eligibility cycles: 1,291;
- executed counterfactual sets: 24;
- OPEN rows: 60;
- OUT rows: 60;
- selected rows: 24;
- alternative rows: 36;
- alternative targetless rows: 28;
- canonical tester executions across all runs: 166.

Runtime integrity:
- clean deinit: 6/6;
- OPEN to OUT / CID pairing: 60/60;
- duplicate execution-equivalent sets: 0;
- selected-count defects: 0;
- capacity skips: 0;
- M5 semantic inference rows: 0;
- selected static-geometry mismatch: 0;
- targeted fatal runtime faults: 0.

Classification: RUNTIME MECHANICS PASS.

## 4. Selected targetless parity and weekend boundary

Selected targetless rows: 8.
- comparable selected targetless rows: 6;
- exact canonical C044 reason + owner-event-time parity: 6/6 PASS;
- strict uncomparable selected rows: 2, both UNCOMPARABLE_C044_M1_HISTORY.

The two uncomparable rows are EURUSD ticket 14 and GBPUSD ticket 10. Direct HST inspection proves the same normal weekend boundary for both:
- last Friday M1 bar: 2026-01-16 23:59;
- first Monday M1 bar: 2026-01-19 00:00.

The Build 5.15 shadow hard-SL scanner intentionally uses exact M1 boundary lookup and therefore fails closed when the requested boundary minute is inside a market-closed gap. This is not archive loss and not a canonical C044 reason/time mismatch.

Disposition: retain fail-closed behavior / NO EA FIX.
Evidence: weekend_m1_boundary_evidence.json.

Across the 28 targetless alternatives, bounded outcomes were:
- C044_HOLD_AT_BASELINE_CLOSE: 15;
- C044_FAILED_MOMENTUM: 6;
- C044_CYCLE_SUPERSEDED: 2;
- UNCOMPARABLE_C044_M1_HISTORY: 2;
- UNCOMPARABLE_C044_REPLAY_FROZEN: 2;
- SL_FIRST_TARGETLESS: 1.

## 5. Candidate-discrimination finding

Observed across all 24 executed sets:
- REL diverse within set: 0/24;
- SREL diverse within set: 0/24;
- MAT diverse within set: 0/24;
- ParentMatch diverse within set: 0/24;
- StructureMask (SD) diverse within set: 0/24;
- SignalType diverse within set: 16/24.

Static code explains the result:
- pending.Relation, pending.StableRelation and pending.Maturity are copied once from g_nested_journeys[pairIndex] before candidates are stored;
- OPEN telemetry prints those set-level fields for every candidate;
- ParentMatch is candidate-expressed but equal-direction candidate sets compare the same direction to the same parent direction;
- StructureMask is candidate-computed, but no within-set difference occurred in the expanded evidence.

Therefore relation distributions across different sets cannot decide which candidate inside one equal-eligible set should win. More pair/month repetition with the same metadata design cannot resolve that structural limitation.

## 6. Interpretation

The expanded counterfactual infrastructure is mechanically sound and supplies substantially more attributable alternative-candidate outcomes than the original single-window sample.

However current P2 coherence/context telemetry is not a candidate-level discriminator inside observed equal-direction competition sets. Accepted BBMA sources still do not define REM/RRE/REE or signal-family superiority. Outcome categories from candidates with different lifecycle semantics are research observations, not an authorized ranking rule. P5 M5 semantic ownership remains unresolved/shadow-only.

Accordingly, the expanded evidence does not justify an active comparator.

## 7. Final disposition

- multi-pair / multi-period P2 evidence expansion: COMPLETE / VALIDATED;
- Build 5.15 research overlay: UNCHANGED;
- canonical C044 lifecycle: UNCHANGED;
- M15 selection authority: UNCHANGED;
- risk/MM/execution authority: UNCHANGED;
- P2 ordering: HOLD / NON-EXECUTABLE;
- M5 execution authority: NONE;
- Strategy-Core delta: NONE;
- EA code fix: NO FIX;
- native compile rerun: NOT REQUIRED — MQ4 BYTES UNCHANGED.

A future P2 activation attempt would first need an explicitly authorized deterministic comparator and genuinely candidate-specific authoritative semantic inputs. Additional repetition of the current set-level coherence fields is not an evidence gap that runtime volume alone can solve.
