# Q5 / Issue #175 Runtime Verification — 2026-09-17

## Scope
Verify the approved standalone H1 Extreme Mode-2 implementation through natural historical evidence and broker-connected demo smoke without changing BBMA Strategy-Core semantics.

Approved execution policy:
- lifecycle window: `RAW Extreme candle -> RETEST completion candle`, inclusive;
- structural buffer: `3.0 pip` outside the lifecycle wick extreme;
- this numeric SL mapping is `PROJECT_EXECUTION_POLICY`, not universal BBMA Core;
- standalone execution maturity remains exact M08 `RETEST/ENTRY-READY`;
- raw/reversal-only Extreme remains non-executable.

## Canonical candidate identity
- Build: `4.84 - Q5 Standalone Extreme Execution`
- MQ4 SHA-256: `CAF8FB9156FA72D2377460FE77FA746EF0366CEA0BF6E821253F22ECA0436053`
- EX4 SHA-256: `118FBACBAAD991E42C5833B56211D6B68C4FF6A43E59C9407E115F94F6337EA2`
- Native MetaEditor compile: `0 errors, 0 warnings`.
- Fresh verification compile on 2026-09-17 again produced `0 errors, 0 warnings` from the same MQ4 SHA, but MetaEditor emitted a byte-different EX4 (`F1E17B09...`) on recompilation. The committed EX4 is intentionally restored to `118FBACB...`, the exact binary deployed in the isolated broker-connected demo; the fresh compile log is retained separately as source-compile evidence.

## Offline T2 harness boundary
Exact 4.84 cannot execute its full strategy path in disconnected MT4 because the default offline environment has no broker symbol catalogue, `IsConnected()==false`, and Strategy Tester rejects `EventSetTimer()`.

T2 is therefore a tester-only environment adapter. It changes only `IsTesting()` infrastructure behavior:
- current tester symbol may satisfy symbol resolution;
- tester may pass terminal-connected guard;
- timer registration is skipped in tester because closed-M15 processing remains driven by `OnTickMain()`.

No M08-M17 detector, maturity, selection, validation, SL/TP, risk, dedup or execution strategy logic is changed by T2.

## Natural historical event — PASS
First natural standalone Extreme selection was found in the June 2025 EURUSD scan.

Event identity:
- processing time: `2025-06-09 16:00`;
- H1 source/retest-completion candle: `2025-06-09 00:00`;
- direction: `BUY`;
- D1 owner: `D1_OWNER_BUY_CONFIRMED`;
- H1 owner state: `EXT_MAT_RETEST_READY`;
- M15 pool: BUY=1, SELL=0;
- DecisionID: `EURUSD|2025.06.09 00:00|1|1|F951645181243D68`;
- M16: exact identity `PASS`;
- M17: `Extreme=Y`;
- simulated execution: ticket 5, one execution only.

M17 runtime payload:
- `Start=2025.06.06 18:00`;
- `Confirm=2025.06.09 00:00`;
- `StructuralAnchor=1.13810`;
- `ConfirmationWick=1.13903`;
- `StructuralSL=1.13780`;
- `FinalBrokerSL=1.13780`;
- `TP=1.13979`;
- entry at execution: `1.13971`.

Independent HST check found 7 actual H1 bars in the inclusive lifecycle window (weekend gap preserved). Lowest Low was exactly `1.13810`, on the RAW/start candle. EURUSD pip size is `0.00010`; therefore `1.13810 - 3 * 0.00010 = 1.13780`, matching M17 exactly.

TP-Wajib independent HST check at the exact H1 source candle:
- MA5 High LWMA = `1.139794`;
- MA10 High LWMA = `1.140052545...`;
- BUY first edge = `min(MA5 High, MA10 High) = 1.139794`;
- outward/tick normalization produced `1.13979`, matching M17.

## Dedup / lifecycle result — PASS for order uniqueness
June 2025 natural scan:
- standalone Extreme M15 selections: 168;
- unique Extreme DecisionIDs: 4;
- maximum selections in one closed-M15 processing cycle: 1;
- Extreme executions: 4;
- unique executed DecisionIDs: 4;
- maximum executions per DecisionID: 1.

The same current owner-valid candidate may be rebuilt on later closed-M15 cycles by contract. After ticket 5 executed, the next same-DecisionID attempt was rejected `REJ_DUPLICATE`; no second order was created. Later fail-closed `REJ_SLTP_UNRESOLVED` rows occur when the fixed TP-Wajib edge is no longer beyond the then-current entry price and do not create an order.

Event excerpt: `blueprint/runtime/q5_175_offline_harness/q5_175_natural_extreme_event_excerpt_20250609.log`, SHA-256 `555EDD00BD7CB750EFCE9BF9285E779B6487652153DC7158F88B595EC83E5334`.

## Broker-connected exact 4.84 smoke — PASS / execution event pending
An isolated clone of the installed MT4 build 1479 was created; primary MT4 was not restarted or modified. The clone uses the saved `MetaQuotes-Demo` environment.

Exact canonical 4.84 was deployed with the hashes above. Read-only smoke proved symbol resolution, broker specification, EA initialization and `[F7-TELEM] Init=1 Connected=1`. After first launch populated H1/H4/D1 history, a second smoke proved current D1 owner resolution from broker history (`D1_OWNER_SELL_CONFIRMED`) and `Connected=1`.

The isolated demo clone is now execution-enabled for EURUSD only, fixed `0.01` lot, Mode 2, and retains exact canonical 4.84. No current standalone H1 Extreme was present at the verified restart, so broker-side standalone Extreme OrderSend/SL/TP evidence remains pending a genuine future event.

## Classification
- Offline natural BUY mechanism: **VERIFIED**.
- M08 RETEST_READY -> M15 -> M16 -> M17 identity flow: **VERIFIED**.
- RAW->RETEST inclusive wick reconstruction + 3.0 pip BUY SL: **VERIFIED**.
- BUY TP-Wajib first-edge mapping: **VERIFIED**.
- Per-cycle decision atomicity and per-DecisionID order dedup: **VERIFIED**.
- Exact 4.84 broker connection / symbol spec / history owner smoke: **VERIFIED**.
- Standalone Extreme SELL natural runtime: **VERIFICATION REQUIRED**.
- Exact 4.84 broker-side standalone Extreme OrderSend event: **VERIFICATION REQUIRED** until a genuine demo event occurs.
- Release status: **NOT RELEASE READY**; no merge authorization is implied.
