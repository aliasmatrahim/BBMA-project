# N1 P1 Build 5.08 Lineage Provenance Validation

Date: 2026-09-22
Issue: #231 / downstream #101 N1/N2/N3 provenance-firewall
Base: `d1-owner-dev@17e940a42d5495075e1f17f8b741816ff662ee59` / Build 5.07
Source-bearing commit: `3d6b0b6ac7b247f240dec259c3b17af33a4968c1`
Candidate: Build 5.08 / `V508_N1_P1_LINEAGE_PROVENANCE_20260922`

## Classification
**CONFIRMED PROVENANCE BUG -> SCOPED FIX VERIFIED OFFLINE.**

Build 5.07 rebuilt D1-owner JourneyID from the latest D1 SourceCandleTime. Ordinary same-owner D1 refresh therefore rotated identity even though the strategic owner had not materially changed.

## Smallest repair
- add provenance-only D1 `EpochStartCandleTime`;
- centralize the existing M11 price-side + MA50-slope rule under one canonical classifier;
- replay closed D1 history only to recover the contiguous owner epoch, failing closed if its boundary cannot be proven;
- add canonical EventID metadata to existing observed events and exact selected ParentEventID;
- derive JourneyID from pair + parent kind + ParentEventID;
- preserve M12N/NMJE observation-only status and N3 execution policy NONE.
## Static / regression
- pre-fix current-owner P1 static test: RED;
- P1 epoch model: PASS;
- P1 current-owner static guard: PASS;
- Build 5.07 protected bodies: 25/25 exact PASS;
- full pytest: 22 passed; one non-functional pytest cache permission warning;
- N2/F07 bridge and F07 model/static: PASS;
- NMJE read-only authority and M12N ordering guards: PASS;
- `git diff --check`: PASS;
- `OrderSend()` count remains one.

## Compile identity
- source/native MQ4 SHA-256: `222E877FC5E7BA718E90D3FAACBAE9426FA4D77D2AAF68643814C194FBDE6AE2`;
- native EX4 SHA-256: `2F92ABB440F946CF9656E7A2C1DCDA7D4D64368469A5BE91B190256D67F11346`;
- native MetaEditor: **0 errors / 0 warnings**;
- exact three-transform tester adapter invariant: PASS;
- tester adapter MetaEditor: **0 errors / 0 warnings**.

## Normal-path EveryTick regression
GBPUSD M15, 2026-08-01 through 2026-09-01, isolated tester.
Nine protected trading trace families are byte-exact to merged Build 5.07:
523 M15 counts/selects/M16/final decisions, 325 preflight passes, 14 executions, and exact F7 momentum/exit/close traces.
N2 decision count remains 523 and is exact after normalizing only the intended `J=` lineage field.
N2 closed outcomes remain 14/14 byte-exact.
## P1 runtime provenance
Natural August run:
- 2,016 D1 owner observations;
- 20 observed ordinary same-owner D1 refresh transitions retained the same epoch;
- all 2,016 N1 journey lines contained `J2` plus `ParentEventID`.

Targeted 2026-07-20 through 2026-08-10 run:
- 1,440 D1 owner observations;
- 12 same-owner refresh transitions retained the same epoch;
- 2 actual owner state/direction transitions changed epoch;
- observed SELL epoch start 2026-07-21 and subsequent BUY epoch start 2026-07-30;
- all 1,440 N1 journey lines contained `J2` plus `ParentEventID`;
- fatal runtime markers = 0.

## Runtime isolation
Both runs restored `gvariables.dat` exactly to 240 bytes, SHA-256
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.
Primary MT4 PID 13064 remained the sole terminal after both runs.

## Boundary
No M5 wiring, candidate create/reject/rank/delay behavior, M13/M14/M15/M16 semantics, risk/MM, M17, M22/M23/M24 behavior or N3 activation was added.
No live/demo broker activation is claimed.
