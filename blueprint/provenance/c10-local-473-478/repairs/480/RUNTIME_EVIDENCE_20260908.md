# Build 4.80 C10 runtime evidence — 2026-09-08

Status: PARTIAL RUNTIME PASS / PHYSICAL LIVE RESTART STILL PENDING.

## Identity
- Build: `4.80 - C10 Ledger Writer Namespace Fix`.
- Source SHA-256: `E9C8CFBE574786BE22003D76F015E5438E9D2EEFD8BF11E377DD93FE61BAE0E1`.
- C10 SourceHash: `5C672778E35AA2602702824778F8F7F6EE4BCDCDFB99B7E32679A17CC0DA2DC6`.
- Exact EX4 SHA-256: `98A6A7C58E33190152E4309A12C6C3FEFC5DFEAC7BF6921208692E9E05A9B40F`.
- C10 remains `Authority=NONE`.

## Authentic ACTIVE checkpoint capture
An isolated MT4 Strategy Tester run on exact Build 4.80 / InstanceID 80 produced an EA-written ACTIVE checkpoint before outcome resolution:
- DecisionID: `GBPUSD|2026.08.10 13:00|1|7|6365325817470039`;
- ConfigFingerprint: `68A827F0705F7E35`;
- Entry=`1.35027`, SL=`1.34923`, TP=`1.35031`;
- RecordType=`ACTIVE`;
- checksum=`1BED180881D74A98`.
The process was suspended at detection and the exact checkpoint was preserved before termination.

## Deterministic checkpoint recovery replay
The authentic ACTIVE checkpoint was restored into the isolated tester state and the same Build 4.80 / InstanceID 80 was started again.
Observed marker:
`[C10][SHADOW_RECOVERY] Active=1 Seen=1 Authority=NONE`
The recovered DecisionID emitted exactly one conservative outcome and did not disable the ledger.

Recovered outcome:
- OutcomeEventID=`1BEECA4E6D1A4BAD`;
- ExitReason=`UNKNOWN`;
- EvidenceResolution=`SHADOW_TIME_PROVENANCE_UNPROVABLE`;
- this is fail-closed because Strategy Tester restart begins at the day's 00:00 clock rather than resuming the original intraday clock.
This replay therefore proves checkpoint identity/load/recovery and conservative provenance failure, but is not substituted for the remaining physical live-clock restart gate.

Tester evidence after recovery:
- signal rows=14 / unique EventID=14 / duplicate EventID=0;
- outcome rows=2 / unique OutcomeEventID=2 / duplicate OutcomeEventID=0;
- `[C10][LEDGER_DISABLED]` count=0;
- Strategy Tester `Total trades = 0`.

## Concurrent live writer isolation
On the broker-connected main MT4, Build 4.74 and Build 4.80 were observed concurrently with Build 4.80 configured `MaxTradePerPair=0`, `MaxTotalTrade=0`.
Build 4.74 signal ledger: 48 rows, 27/27 columns on every row, 0 malformed, 0 duplicate EventID, BuildID only `4.74`.
Build 4.80 namespaced signal ledger: 46 rows, 27/27 columns on every row, 0 malformed, 0 duplicate EventID, BuildID only `4.80`.
Build 4.80 namespaced outcome ledger: 11 rows, 35/35 columns on every row, 0 malformed, 0 duplicate OutcomeEventID, BuildID only `4.80`.
Build 4.80 live owner token: `OC0A403111A4E`.
Across 9,143 Build-4.80 log lines reviewed: 0 C10 ledger/file/checkpoint failure markers and 0 `OrderSend`, `OrderClose`, `OrderModify`, `OrderDelete`, or `DEC_EXECUTED` markers.

## Remaining acceptance gate
A separate isolated live Build 4.80 terminal is now attached with `ExpertsTrades=false`, `MaxTradePerPair=0`, `MaxTotalTrade=0`, InstanceID=80. It is waiting for a fresh live `ACTIVE` shadow so the same terminal can be physically stopped and restarted at the live clock. Issue #122/#123 remain open until that final restart evidence is captured and checked.

## 2026-09-08 pre-closure hardening update
The final live physical-restart gate is now guarded by `verify_runtime_closure.py`.
The verifier cross-checks exact ACTIVE identity across restart, M5 enrollment chronology, safe launch parameters, CSV schema width, cross-file same-provenance duplicate IDs, target-outcome chronology, post-restart recovery/Authority=NONE markers, ledger-disable absence and zero broker-action markers.

Verifier controls were exercised separately from runtime evidence:
- clean synthetic fixture built from authentic Build 4.80 checkpoint/ledger data -> PASS;
- injected duplicate EventID -> FAIL as expected;
- injected `OrderSend` -> FAIL as expected.

This tooling validation does not satisfy the remaining live acceptance gate by itself. The isolated broker-connected InstanceID 80 watcher remains responsible for capturing a fresh live ACTIVE state and performing the same-terminal physical restart before the verifier can issue a runtime PASS.
