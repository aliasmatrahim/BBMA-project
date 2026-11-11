# SIG-06 MHV natural-history origin / restart milestone — 2026-11-11

Status: PARTIAL — bounded engineering restart proof passes on M1/M5/M15/H1; full historical origin/session/availability acceptance remains HOLD. Current signal remains SIG-06 MHV. No later signal or production source change.

Baseline91ab4d28f51c7bb9648f8e757ee22a9eb70592ff; branch feat/custom-mtf-v1-20261108; Draft PR303; Build6.11 rev003 source LF SHA a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb unchanged. New test/evidence files only. Dates here use the user's Malaysia date; all historical timestamps below are MT4 chart labels, not authenticated UTC.

## What changed in the evidence

Previous checkpoint had only zero-initialized controller owners and trusted structural fixtures. New diagnostics invoke actual M08/M09 engines on installed native price history, record the actual Extreme/reversal/TPW/formation lineage, and compare four different initial-state hypotheses. Hypotheses are never treated as historical facts.

The bounded inventory scans600 existing fully closed source candles per7TF,4200 total. It breaks the sequence at every non-nominal boundary rather than inventing or skipping bars.57 candidate chains were recorded;23 candidate points had complete M08/M09 state convergence across4 hypotheses.

| TF | Source bars | Candidate chains | Converged candidates | New restart proof |
|---|---:|---:|---:|---|
| M1 |600|9|6|24 source bars / full state match|
| M5 |600|4|3|24 source bars / full state match|
| M15 |600|13|9|24 source bars / full state match|
| M30 |600|9|0|Not accepted|
| H1 |600|14|5|24 source bars / full state match|
| H4 |600|8|0|Not accepted|
| D1 |600|0|0|Not accepted|

Zero candidates in these bounded D1 segments is not proof of no MHV in D1 history.

## Strong witness and retained rejection

The first converged M15 candidate (chart epoch1784895300) failed2 of6 checks: its BUY M08 raw and opposite M09 parent originated before the first Momentum reset. Four-hypothesis convergence alone was therefore insufficient for the stricter checkpoint witness. The run is retained as RED, including source/binary hashes and native log. It was not promoted.

The next M15 candidate (chart epoch1784912400) passes the unchanged witness:
- actual selected parent RAW -> reversal -> normal TPW -> formation after a source Momentum reset;
- both M08 raw origins and both M09 parent origins after the first source Momentum reset in the same nominally contiguous segment;
- full state convergence across4 hypotheses;
-24 subsequent exact existing source candles, with no boundary crossed.

M1/M5/H1 select the first point satisfying those same tests plus24 available future contiguous source bars. This is checkpoint-test selection, not a new trading condition or profit optimization.

## Physical process restart and field equality

For each of4 TFs, one isolated MT4 process writes the naturally reconstructed candidate and uninterrupted control states. After that process exits, a different MT4 process reloads the serialized snapshot and replays24 bars from the same unchanged HST inputs.

Each state contains all20 fields of each M08 side and all31 fields of each M09 side:102 fields. The test-only CSV codec round-trips numbers/enums/timestamps and encoded Reason strings; the existing equality helpers compare all102 fields. Every replayed state is equal to uninterrupted control, including lineage, frozen anchors, lifecycle status, supersession and cursor metadata.

Results: producer6/6 + consumer28/28 perTF,136 checks total;96 post-reload source-bar state comparisons;8 distinct terminal PIDs, all exit0. All3 new harnesses strict0 errors/0 warnings. Source, harness/binary, codec/equality-header,7 unchanged HST hashes, snapshot hash and2553 unique snapshot-record keys per case verified by collector4500 exit0. No broker orders or primary-terminal restart.

## Remaining observed boundaries

| TF | Example chart labels | Unobserved nominal slots | Ruling |
|---|---|---:|---|
| M30 |2026-07-14 22:30 ->23:30;23:30 ->2026-07-15 00:30|1 each|Derived fixture/source-boundary provenance not authenticated|
| H4 |2026-03-20 20:00 ->2026-03-23 00:00|12|No automatic weekend/UTC classification|
| D1 |2024-04-12 00:00 ->2024-04-15 00:00|2|No automatic historical closure classification|

These are observed timestamp gaps, not confirmed missing market data or approved session closures. M30 remains a derived engineering fixture. Native history source identity does not by itself authenticate broker historical schedules or all possible prior owner states.4 initial hypotheses do not exhaust every valid prehistory.

## Scope / exact next action

This milestone closes a bounded natural-history restart subproof; it does not globally authenticate an M08/M09 epoch, arbitrary unknown-state reconstruction, non-contiguous recovery, seven-TF market coverage or executable Custom MTF availability. Existing session/UTC/source-authority limits still control.

Next: establish authoritative same-feed closure-vs-missing classifications tied to these HST hashes, first for a selected M30/H4/D1 boundary; then reconstruct/validate the owner across that boundary and compare full continuous-vs-recovered owners. Do not use an arbitrary NONE, price-fitted UTC offset, another feed's calendar or synthetic fill to close the gate. No already verified source audits were rerun and no raw data downloaded.

Evidence: mhv611_natural_origin_restart_summary.json and mhv611_natural_origin_restart_evidence.zip; archive SHA256 6f8455ddcf13aad9c538f7b4a93d510159641488727b5e77f06ce36ca3c410ae. Inventory/source CSVs,4 full candidate/control snapshots, native manifests, failed first-case record and binding metadata are archived. Code/driver/codec are test-only.

SIG01–05 bounded acceptances unchanged. MLV/Re-Entry remain pending. All77 semantic/executable availability and custom auto-entry OFF. No merge/deployment or profitability claim.
