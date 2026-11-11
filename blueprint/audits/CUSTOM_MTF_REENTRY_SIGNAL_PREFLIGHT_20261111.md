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
