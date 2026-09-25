# NMJE V2 P2 Targetless Counterfactual Lifecycle Replay — 2026-09-25

Status: **VALIDATED / TESTER-ONLY C044 SHADOW REPLAY / P2 ORDERING HOLD REMAINS**

Issue: #101
Owner base: `d1-owner-dev@ce73919556ec458efd5b1d962b9d7e5cdb348e4a`

## 1. Objective

Extend Build 5.14 equal-candidate attribution so targetless C044-managed alternatives can be classified without:
- creating a virtual broker order;
- changing M15 selection;
- calling risk/MM for an alternative;
- inventing a TP;
- duplicating M08/M10/M12 detection;
- changing M23 live lifecycle authority.

D1 Extreme TP-Wajib replay is excluded because its dedicated activation gate remains OFF.

## 2. Source and ownership boundary

The approved C044 decisions define a targetless Re-Entry lifecycle:
`Re-Entry owner -> no universal static broker TP -> owner-TF closed-candle lifecycle -> failed Momentum / cycle supersession / opposite CSM exit`.

The lifecycle owner is the exact frozen Re-Entry source timeframe:
- standalone Re-Entry -> H1;
- REM -> H4 Re-Entry;
- RRE/REE -> D1 Re-Entry.

M15 remains sole new-entry authority. M23 remains live-position lifecycle owner.
The canonical comparator remains untouched.

## 3. Build identity

- Build: `5.15`
- Build tag: `V515_NMJE_P2_TARGETLESS_REPLAY_20260925`
- Source rev: `NMJE_P2_TARGETLESS_REPLAY_001_20260925`
- MQ4 SHA-256: `B9F3876F61645B2F98009A4251A4142EDC7644ED728E41EDECA245FF1E243C45`
- Production EX4 SHA-256: `AB315243E453725816C92DF376451DEB296F233DC984DA7FC3EED5976DC5BE5A`
- Harness EX4 SHA-256: `56610EA60909A4E7893548D6E606448C1BC4FBCA3D66205686DD0580BAC0F6D5`
- Strategy-Core delta: **NONE**

## 4. Replay design

Build 5.15 does not implement another C044 state machine.

At baseline fill, a targetless C044 alternative is initialized through the existing `InitializeC044TradeStateFromDecision` path and its canonical replay seed is frozen into the counterfactual record.

At baseline close, the research overlay restores that private state and calls the unchanged canonical `ProcessC044OwnerClosedCandle` for each eligible fully closed owner-TF candle.

Only two canonical side effects are suppressed for shadow replay:
- `SaveC044Checkpoint` becomes an in-memory success/no-op when `c044_shadow_replay=true`;
- `F7Telemetry` emits nothing for that shadow state.

Live monitored trades always reset `c044_shadow_replay=false`.

### Hard-SL ordering

Between owner events, complete closed M1 bars are used only to determine whether the candidate-specific hard SL would have triggered first.
SELL uses the already-frozen spread as the explicit Ask-side engineering proxy.

The baseline broker close time is only the paired observation horizon.
It is **not** treated as a counterfactual exit rule or target.

### Fail-closed states

Missing owner history, M1 history, replay seed or invalid canonical state remains explicitly `UNCOMPARABLE_C044_*`.
No replacement exit or target is manufactured.

## 5. Static / compile validation

- Native MetaEditor: **0 errors / 0 warnings**.
- Tester harness MetaEditor: **0 errors / 0 warnings**.
- Full repository Python suite: **72/72 PASS**.
- Targeted authority regression: **PASS**.
- Protected comparator/M16/risk/preflight/execution functions are normalized-exact to Build 5.14.
- Canonical `ProcessC044OwnerClosedCandle`, `InitializeC044TradeStateFromDecision` and `AdvanceC044OwnerEventOneCandle` are normalized-exact to Build 5.14.
- Broker primitives remain `OrderSend=1 / OrderClose=3`.
- Targetless replay contains no `OrderSend`, `OrderClose`, risk approval, lot sizing or `ProcessEntry`.
- Targetless replay calls canonical C044 processing and does not call `DetectCSM`, `DetectExtreme`, `UpdateExtremeLifecycle` or `UpdateReEntryState` itself.

## 6. Final Strategy Tester evidence

Environment:
- GBPUSD / M15;
- 2026-08-01 through 2026-09-01;
- isolated StrategyID 91 / InstanceID 92;
- Build 5.15 rev001 harness.

Results:
- counterfactual sets: **3**;
- OPEN rows: **9**;
- OUT rows: **9**;
- selected rows: **3**;
- alternative rows: **6**;
- execution-equivalent duplicate sets: **0**;
- OPEN/OUT candidate-ID pairing errors: **0**;
- capacity skips: **0**;
- M5 semantic inference rows: **0**;
- fatal runtime errors: **0**.

Targetless coverage:
- selected targetless rows: **2/2 canonical-seed match**;
- alternative targetless rows: **4/4 C044 replay present**;
- legacy `UNCOMPARABLE_TARGETLESS`: **0**;
- alternative outcomes: **3 C044_HOLD_AT_BASELINE_CLOSE + 1 SL_FIRST_TARGETLESS**.

Selected-shadow parity:
- ticket 4: canonical `C044_EXIT_CYCLE_SUPERSEDED` == shadow `C044_CYCLE_SUPERSEDED`, exact owner-event close time;
- ticket 12: canonical `C044_EXIT_FAILED_MOMENTUM` == shadow `C044_FAILED_MOMENTUM`, exact owner-event close time.

Authority regression:
- canonical executions Build 5.15: **14**;
- Build 5.14 baseline executions: **14**;
- exact execution trace equality: **PASS**;
- tester report trade/profit/drawdown fields equal Build 5.14: **PASS**.

## 7. Research interpretation

Build 5.15 closes the methodology gap that made four Build 5.14 alternatives `UNCOMPARABLE_TARGETLESS`.
They are now attributable inside the paired baseline horizon without a duplicate trade or invented TP.

This still does **not** authorize P2 ordering.
The sample remains small and the replay is an engineering research comparison, not proof that one candidate family or coherence state is superior.

P2 active tie-break therefore remains **HOLD / NON-EXECUTABLE**.

## 8. Evidence

- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/evidence_manifest_rev001.json`
- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/targeted_regression_result.json`
- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/final_runtime_analysis_rev001.json`
- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/runtime_rev001_key_rows.log`
- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/execution_trace_515_rev001.txt`
- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/native_compile_rev001.log`
- `blueprint/audits/evidence/NMJE_V2_P2_TARGETLESS_REPLAY_20260925/harness_compile_rev001.log`

## 9. Exit decision

Targetless C044 counterfactual lifecycle replay is complete for the current research-safe scope.

Classification:
- implementation: **VALIDATED TESTER-ONLY RESEARCH OVERLAY**;
- live C044 lifecycle authority: **UNCHANGED**;
- M15 selection authority: **UNCHANGED**;
- P2 ordering: **HOLD**;
- D1 TPW replay/activation: **NOT INCLUDED**;
- Strategy-Core delta: **NONE**.
