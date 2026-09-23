# Q10 R3 MetaQuotes-Demo Runtime Checkpoint — 2026-09-23

Issue: #109
Owner baseline: `d1-owner-dev@52c01ec7f39a1c1a9473c3f6040f7b6e21a8ea53`
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Result

**AUTH PASS / R3 INCOMPLETE / NO EA FIX**

The dedicated MetaQuotes-Demo terminal successfully authenticated and ran the exact frozen Build 5.11 candidate. R3 produced valid authenticated evidence but did not naturally cover every mandatory R3 scenario.

No Strategy Core, EA source, risk/MM, execution, lifecycle, recovery, dashboard or telemetry change is justified by this run.

## Identity

- canonical source SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`;
- native Build 5.11 EX4 SHA-256: `CFF8DA584C91AE177CA26E1C47518AA585A67F0E16C99295F932670E8CDEC6E1`;
- settings SHA-256: `37BC585EB3AB5A73914FEC3C532023636D4FACCD7D3AAAF20B774269CF92DA70`;
- Q10 read-only probe R2 EX4 SHA-256: `AD47BA707F35862239C4A29ACFC257220DC6CE9252C2F70C67AAC8B04FC888D8`;
- terminal build: 1479;
- provider: MetaQuotes-Demo;
- account class: DEMO;
- connected: YES.

No account number or credential is retained in the committed evidence package.

## AUTH

Read-only probe evidence:

- initial marker: disconnected;
- delayed-connection marker: `Demo=Y / Connected=Y / Server=MetaQuotes-Demo / Company=MetaQuotes Software Corp.`;
- `TradeAllowed=N` during the probe;
- probe contains no OrderSend/OrderClose/OrderModify/OrderDelete authority.

Formal AUTH result: **PASS**.

## R3 runtime

Dedicated runtime:
- pair/timeframe: GBPUSD M15;
- Build 5.11 loaded successfully;
- broker spec and PairID/Magic validation PASS;
- EA initialization PASS;
- MetaQuotes-Demo session connected;
- heartbeats continued throughout the run;
- processing remained on the M15 clock;
- no broker execution occurred;
- terminal closed gracefully after evidence capture.

The raw R3 log is an exact byte slice beginning at the recorded pre-run log offset, so earlier probe/Q9 runtime lines are excluded.

Raw R3 SHA-256:
`7811065AAB2A5C63F0CE764670E568C4D45C9D05D0F26AE676DDCED65237A835`.

Matched R3 SHA-256:
`24292F37A8BEC3D1ABF6B740685AB624143B6E063C5C06E2951E76BB72A48BBE`.

## Case result

PASS:
- R3-00 — exact authenticated Build 5.11 baseline;
- R3-02 — D1 SELL confirmed on fully closed 2026-09-22 D1 candle;
- R3-04 — initial unresolved D1 history fails closed with DIR_NONE and no execution;
- R3-05 — compatible D1 SELL / H4 SELL owner relationship positively observed;
- R3-15 — repeated 07:30 / 07:45 / 08:00 processing retained 2026-09-22 as the D1 owner candle while 2026-09-23 D1 was still forming.

INCOMPLETE:
- R3-01 — D1 BUY not observed;
- R3-03 — D1 TRANSITION not observed;
- R3-06 — opposite H4/D1 scenario not observed;
- R3-07 — required H4-no-owner scenario not observed;
- R3-08..R3-12 — no valid D1O executable DecisionID/ticket occurred, so attribution/hash/dedup/restart continuity cannot be positively proven;
- R3-13 — tactical `D1_OPP_EXTREME_TPW` not observed;
- R3-14 — no live exact-owned trade existed during an owner update.

Formal analyzer result: **INCOMPLETE**.

The state machine records R3 as INCOMPLETE and therefore does not permit formal R4 promotion.

## Runtime-state note

Pre-run GlobalVariables:
`F093DBF358DA27CEDDC611BBAAA5E36D265E467BEE27ABB4D2F51E993F3E4E43`.

Post-run GlobalVariables:
`D1355D6161E9860114F61022C65CD4BC918B196D1EC07B52FBE383AA55E45388`.

The change occurred during valid Build 5.11 initialization/runtime and is preserved for provenance/restart continuity. It was not silently rolled back.

Primary MT4 PID 13064 remained untouched. The dedicated Q10 terminal was gracefully closed.

## Interruption/recovery correction

During recovery the R3 process initially appeared stalled because both MT4 log files had not flushed beyond the early startup lines while the terminal was still open.

After a graceful `CloseMainWindow()`, the buffered log was flushed and showed:
- complete Build 5.11 initialization;
- authenticated MetaQuotes-Demo connection;
- regular heartbeat;
- valid 07:30 / 07:45 / 08:00 owner cycles;
- clean EA deinitialization.

Therefore the earlier apparent stall is reclassified as **log-buffering observation, not an EA/runtime stall**.

## Evidence

Small credential-free evidence is stored at:

`blueprint/audits/evidence/Q10_R3_METAQUOTES_20260923/`

Local full terminal provenance remains on G40. Terminal logs containing the demo account number are intentionally not committed.

Manifest SHA-256:
`76DB92E009354D843023A7915DFECFACFEE76F2D600D433E073F0BDD61F43AB2`.

## Exit / next gate

R3 cannot be promoted to PASS under the locked acceptance matrix until the missing mandatory runtime scenarios are positively observed, especially:
- D1 BUY;
- D1 TRANSITION;
- required opposite/no-owner H4 cases;
- D1O executable identity/dedup/restart evidence;
- EXT_TPW;
- live-trade owner-update side-effect case.

Tester/static evidence must not be substituted for these broker/demo cases.

Proceeding immediately would require changing the locked acceptance semantics or manufacturing market states. Neither is authorized by this checkpoint.
