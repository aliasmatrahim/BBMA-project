# SIG-01 eCSD acceptance — 2026-11-10

Status: VERIFIED for canonical eCSD detector, existing consumers and bounded native/controller evidence below. This is not T04-D completion, full Custom MTF execution acceptance or release readiness.

Branch feat/custom-mtf-v1-20261108; tested code checkpoint3c14938b8e2c2ab79d47101e61a8d90362a94091 (local e7b8704eed755458d12befcd4186861ec8ae6931). Build6.07 / V607_ECSD_CLOSE_ONLY_20261110 / ECSD_CLOSE_ONLY_001_20261110. Source LF SHA2563c2745e4fd9d0d84c66c6e5442388f0d8de05ccb211fff81bd4ed38a2e310b44. Final evidence commit recorded in Draft PR303.

## Change and scope

User decision M10_DIRECTION_CLOSE_ONLY_USER_DECISION_20261110.md is binding: valid completed-candle Close above both MA5High/MA10High for BUY, below both MA5Low/MA10Low for SELL. Open is not accessed by DetectECSD. A shared Close-pair helper owns that comparison; nonpositive required Close/MA, invalid direction, shift0/negative and equality fail closed. Caller signatures remain unchanged.

Only eCSD is migrated. Nine protected CSD/MOM/owner/consumer bodies match the frozen6.06 baseline. Other signal state machines, ordering, M15 processing clock, risk/execution and custom admission remain untouched. The legacy CSD body-pair helper is still used by CSD; it is not dead code or a second eCSD detector. CSD will migrate only in its own signal task. Raw eCSD may overlap a stronger same-bar predicate; existing Momentum > CSD > eCSD collector precedence is retained, not replaced by a new Mid exclusion/colour/TTL rule.

## Exit evidence

| Exit | Observed evidence | Ruling |
|---|---|---|
| Approved spec and baseline defect | Actual extracted6.06 detector rejected Close102 above MA101/101.5 because Open105; test RED before production patch | PASS |
| Cloud regression | Final repository-root pytest76/76 in1.35s; runner/test py_compile and diff check PASS | PASS; not native syntax proof |
| Native full compile | EA and final eCSD harness0 errors/0 warnings; source/include/harness/final binary bindings | PASS |
| Native eCSD cases |190/190: seven-TF BUY/SELL/Open-independent/no-Open-read/equality/closed-shift/invalid-input cases plus D1/M11/M12 fixture delegation and same-candle H4 identity | PASS |
| Source-data comparisons |140 actual closed-history comparisons (20 per TF) against finalized native iMA/iClose; all seven TF ready, positive observations on each | PASS; M30 remains derived OHLC fixture |
| Affected regression | MOM55, MHV-TF238, M09producer52, M09replay57, canonical47, observer4, producer22, recovery27, higher23, flow12, prefreeze61 | PASS in existing separate scopes |
| Actual controller | GBPUSD Aug4 2026 02:00-06:00 chart time, actual OnTick/OnTimer -> M27 -> ProcessPair, M1 tester delivery/model2, canonical M15 clock |16 cycles per profile |
| Monitor independence | Candidate OFF/ON12,224-row full scalar traces identical, all fields retained | PASS in this window |
| Prior-source comparison | Frozen6.06, same initial checkpoint fixture:136 rows differ in H4 owner and H4 SELL M12 Type1 precursor fields; no final Decision fields differ in this sample | Expected wider direction qualification; not unchanged legacy-history proof |
| Orders | Candidate OFF/ON and baseline606 each valid decisions0, captured attempts0, no orders | No positive selected-entry/broker execution/P&L claim |
| Publication | Code checkpoint/Draft PR saved; full native bundle, baseline proof, final three gzip traces, queue/checklist linked | Final SHA recorded in Draft PR |

M1/M5/M15/M30/H1/H4/D1 source checks each compared10 closed bars in both directions. Positive matches per TF were5/5/4/3/8/3/8. These are source-read checks, not authenticated market coverage or signal frequency measurements.

## Initial controller failure and root cause

Initial OFF/ON full-trace comparison failed in eight H4Owner.RecoveredFromCheckpoint values. The first case's canonical EA persisted its H4 checkpoint; the following case inherited it. No decision/value field was dropped to hide the difference.

The test harness now explicitly clears only its F4H4|StrategyID|Instance82|GBPUSD| D/S/T fixture keys before canonical OnInit, guarded by IsTesting, exact GBPUSD and Instance82. The production H4 recovery implementation is unchanged. The final manifests record checkpointBefore=true and checkpointAfter=false for all three cases. With equal initial fixture state, full trace parity passes. This is a test-isolation correction, not permission to clear deployment owners on restart. It does not test arbitrary restart/session reconstruction.

RED traces/manifests are retained on G40 at evidence/controller607_checkpoint_red; initial manifest and eight differences are also embedded in ecsd607_native_evidence.json. A resume-wrapper count assertion initially expected16 rather than the observed8; a PowerShell file-write failure left that wrapper unchanged. Both failed before any additional native case was started. Exact-file replacement corrected the wrapper; verified eCSD/regression runs were reused. Final controller/collector process6836 exited0, ECSD607_FINAL_NATIVE_BINDINGS_PASS.

## Old/new state effect

The136 old/new rows comprise updated H4 source/advance time and reason, H4 SELL Type1 context state/owner signal/candle/previous-close/reason, and eight recovered-origin flag values. Candidate source observations qualify later H4 eCSD bars that the old Open requirement excluded; M11 and M12 then consume the accepted signal through unchanged functions. Those lineage/origin values can legitimately differ from frozen6.06 even with equal initial checkpoints. Do not conflate this intended baseline comparison with the initial same-candidate test-isolation failure.

No final Decision.Valid became true in the sampled controller window. That does not prove downstream behavior will never change on other data. The broader change in qualifying eCSD bars is intentional under the user decision and requires retained downstream acceptance gates before activation.

## Integrity and limitations

Full manifests, source/include/test helper hashes and native rows: blueprint/runtime/custom_mtf/ecsd607_native_evidence.json. Final EA and each unique harness binary were rebound; older repeated EA compilation identities remain recorded in their own manifests, not falsely matched to the last overwritten binary. Native source SHA and cloud source SHA match. Protected function proof: ecsd607_baseline.json. Three complete final scalar traces are archived under controller607; candidate OFF/ON raw SHA bf2ca903df2fb1cf2b6271f294806a78d0cb317cd32362bc82a4e04cd68313e7.

Timer callbacks are manually delivered by the harness; wall-clock timer/live reattachment is not proved. M30 is the previously declared complete-bucket OHLC fixture. No authenticated historical session/UTC/structural epoch, multi-symbol broker execution, custom admission, standalone raw-direction entry or profitability is claimed. The eCSD name is not added to the approved11-token custom grammar; user MidBB CSA is not aliased to eCSD.

## Sequence

SIG-01 canonical eCSD is complete in this scoped acceptance. Next eligible signal is SIG-02 CSA (user MidBB direction), only after this checkpoint publication is verified. No other signal was developed while SIG-01 remained unfinished. CSD/CSAK Close-only migration and later signal/TF/custom-trigger/recovery gates remain separate. Auto-entry/all77 semantic availability OFF; no merge/deployment/primary-terminal restart.
