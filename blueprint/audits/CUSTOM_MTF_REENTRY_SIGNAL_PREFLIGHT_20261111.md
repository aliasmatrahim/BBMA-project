# Serial Re-Entry audit — preflight on Build 6.13

Status: IN PROGRESS. MHV and MLV bounded signal acceptances are published. This preflight concerns the Re-Entry family only.

## Source and owner

Use SOURCE_INDEX → Core V2 §8 → primary PDF pages 9–10 and Finale timing/context → F6 timing audit → M12 owner and its downstream candidate callers. The baseline EA in Draft PR #303 is Build 6.13 at `53fe1d112f5b03f1f7df86da936e4e2756ce8d2b`, LF SHA `43470ff9795b18e44844bb815deceee778072a004b8815666e18e8ffa584d15c`.

| Type | Current source path reviewed |
| --- | --- |
| 1 | Prior BBMA direction owner, structural retrace/ranging and valid MA5/10 touch. No fixed candle count or generic TTL. |
| 2 | MA5/10 and Mid BB confluence, three qualifying candles and a valid MA-cluster touch. The optional MA50 confluence is classified as most powerful. |
| 3 | Source-valid CSM first, then a later retrace to MA5 or MA50. |
| 4 | Source-valid CSD first, then a later retrace to MA5/10. |
| All | Shared M12 lifecycle and confirmed export. Custom RE/RE1–RE4 are read-only views. Re-Entry entry-window diagnostic uses actual current source candle plus the recorded EntryCandle. |

This maps the code paths to the accepted family. Runtime lifecycle coverage on this exact build is still to be adjudicated.

## Confirmed standalone H1 timing gap

An H1 Re-Entry owner can remain structurally valid beyond its entry window. Build 6.13's `BuildConfirmedReEntryCandidate` checks confirmation and matching active H4 authority but does not check current H1 candle against `EntryCandle`. If H4 aligns later, the old event can still enter the candidate pool. This is a candidate admission defect, independent of M12 structural validity and custom read-only projection.

Exact source comparison: the complete standalone builder body is identical to owner Build 5.15. Build 6.13 has one production caller. Draft PR #301 at `afb206aac93e82322b3a33318e06fb0b0e6912c9` already implements the source-current gate on Build 5.16 while keeping `candidate.Expiry=0`. Its GBPUSD August 2026 isolated Strategy Tester report records seven timely trades retained and one late entry excluded. This evidence is for that candidate build. Draft #293's remaining order-open trace and draft #301's eligibility evidence are distinct checkpoints.

Next: reuse #301's positive-window and late-H4 controls on the exact Custom MTF lineage in an isolated candidate, verify Types 1–4 and entry-window behavior, and keep cross-session source admission under the existing T04-B/E recovery requirements. Canonical deployment still requires the owner-branch integration decision. No EA code change, new runtime pass, merge or order activation in this checkpoint.

## Native isolated EntryCandle validation

Reused the exact standalone builder change and single caller adaptation from Draft #301 in isolated Build 6.14. G40 driver PID 12104 exited 0. Full EA and harness strict compile were 0 errors/0 warnings on both builds. Each build ran 58 checks in the same GBPUSD M15 tester fixture using MT4's actual current H1 candle, with seeded owner states.

- Build 6.13 reproduced 24 failures (34 passes). Each of Types 1–4 and BUY/SELL incorrectly admitted the too-early, late H4 alignment and missing EntryCandle cases.
- Isolated Build 6.14 passed 58/58. Timely entries remained eligible, opposite H4 and invalid owners stayed ineligible, and stale entry eligibility did not erase structural M12 validity. Both runs placed zero orders.
- Candidate source LF SHA `ad76809f3c63134d9b170c5b0078b34b36720d489819e5ed0ecb85256fb913e2`. Native row names, summaries, manifest hashes and executable bindings are in `reentry614_entrycandle_probe.json`. The candidate also corrects the F7 build label, which prints 6.10 in baseline 6.13 despite the actual 6.13 build tag and source hash.

The 6.14 source is an isolated validation candidate, with no EA source applied to Draft #303 or the active owner branch. The confirmed-owner probe does not establish market-driven formation of all types, exact-build controller/OrderOpenTime behavior, or session-boundary admission. Re-Entry remains IN PROGRESS. Reuse the already approved overlap order (Type 3 → Type 4 → Type 2 → Type 1, empty-owner only) from Draft #293's M12 decision when validating the lifecycle. It is a project policy. The next runtime action is exact-build market-driven M12/EntryCandle replay at the M15 controller, carrying forward the older #301 positive-window and late-H4 witness cases where the input history and test profile match.

## Market-driven controller replay

The paired tester replay reused Draft #301's GBPUSD M15 August 2026 profile (EntryMode 1, fixed spread 20, tester model 0). Both exact-build lineages used the same tester-only connectivity adapter and fail-on-live initialization guard. The adapter source hashes, EX4 hashes, tester log hashes, six unchanged HST hashes and preset hash are in `reentry614_market_replay.json`. Both EA adapters compiled strict 0 errors/0 warnings, both terminals and the driver exited 0. Strategy tester produced a report for both runs.

Actual isolated GBPUSD August 2026 M15 controller replay completed: Build 6.13 emits 16 late candidate admission rows for one Type 3 confirmation; isolated 6.14 emits zero. The 1,296 RE_EVAL rows are identical. Both runs have zero orders; no timely H4-aligned window and no market Type 2 confirmation were observed. Re-Entry remains IN PROGRESS. The source confirms the H1 candle after 28 August 17:00 actually existed at 18:00. The 16 admissions occurred 31 August 00:00–03:45 and were all tied to the 28 August confirmation. Both runs showed the same 7 Type 1, 4 Type 3 and 22 Type 4 market confirmation events. Of 132 timely M15 evaluations, 124 had unresolved H4 recovery and 8 had active H4 in the opposite direction. This proves late-candidate suppression through the actual controller and preserves observed M12 state. Positive market execution timing remains unverified on this lineage.

Next eligible work is Re-Entry only: use a verified history/profile that can provide an active same-direction H4 owner during the H1 entry candle and capture the M15/M16/OrderOpenTime trace, plus a Type 2 market witness. Preserve H4 fail-closed behavior and existing session-boundary conditions.
