# SIG-04 Momentum readiness repair implementation plan

> For agentic workers: execute this scoped repair inline, task by task, under the existing continuous-execution authorization.

Goal: prevent incomplete/changing Momentum inputs from producing a signal, a false no-Momentum decision, weaker owner fallback or a consumed owner candle.
Architecture: retain the one M10 classifier and snapshot; propagate its ready/unavailable result before mutations. M15 remains the only processing clock. Existing owner and C044 freeze/recovery policies remain authoritative.
Tech stack: strict MQL4, existing isolated G40 native tester and source-extracted host checks.
Spec: M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT; accepted Core sections4/7/8; CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION; existing C044 closed-data-unavailable freeze behavior.
Base:87d185fae1426e8d8321fb1f6e6f684bc526e319, Build6.09 source d74f41d0c85e8ec5e4afdd58728c4cfcaae5765adc128f4aefa849edbfb04c25.

## Constraints
- No rule/threshold/TTL, signal grammar, strategy, risk, execution or activation change.
- Preserve proven owners and cursors on unavailable data; never turn unavailable into proven neutral/no Momentum.
- Reuse current native72/iBands1400/controller630 valid-data proof and retained17-group regression as baseline, not as proof of this repair.
- Unique Build6.10/source revision; all77 availability and custom auto-entry OFF; no merge/deployment.
- Finish SIG-04 before Extreme or later signals.

## Review focus
1. A missing interior Close cannot be skipped into partial BB arithmetic.
2. Fewer than21 closed inputs cannot establish or disprove Momentum.
3. Unordered timestamps cannot advance an owner.
4. A revision during read cannot leave buy/sell true or cache a result.
5. Unknown Momentum cannot downgrade a direction owner, enter MHV loss phase, consume replay/cycle cursors or close a C044 trade.

## Task A: native failing evidence and scope
- [x] Native actual detector fixture: missing Close9, positive current/prior partial bands -> ready=false/raw=true.0E0W.
- [x] Review direct and negative consumers: M09, M11 live/replay/checkpoint, M12, C044 and M27/custom source scheduling.
- [ ] Add native state/cursor-preservation fixtures before production patch, retaining RED evidence.

## Task B: minimum availability propagation
Modify only blueprint/source/BBMA_EA.mq4 and relevant custom_mtf tests.
- [ ] M10 snapshot exits before classification on unready inputs; clears direction flags when final fence fails; DetectCSM honors return.
- [ ] Add one source-data identity/readiness adapter over the existing snapshot.
- [ ] Gate M09/M12 owner entry points and M11 classification/live/replay before mutation or fallback.
- [ ] Preserve unverified H4 checkpoint data; distinguish unavailable from invalid; warm-up replay starts only where a full21-input window exists.
- [ ] C044 uses one ready snapshot for both directions before private replay/cursor changes; unavailable uses existing freeze policy.
- [ ] M27 pair cycle and existing custom source/replay wrappers defer/abort without consuming unavailable source candles.
- [ ] Keep valid complete-data classification exactly unchanged.

## Task C: verification and publication
- [ ] Static/cross-module, strict full EA and harness compile0E0W.
- [ ] Native missing/short/unordered/revision fixtures reject/no-mutate/no-exit; valid-data oracle and controller parity.
- [ ] Affected specialized regression only; review source/binary/trace bindings and any intended state differences.
- [ ] Independent review, durable checkpoint/acceptance and PR update. No SIG-04 VERIFIED claim until all scoped exits pass.


Completion2026-11-10: all planned bounded exits PASS on Build6.10 rev003. Native72/167,18 groups,20 bindings, controller630 views/12224 rows exact parity with OFF and6.09; collector9520 exit0. Full acceptance and retained REDs: blueprint/audits/CUSTOM_MTF_MOM_SIGNAL_ACCEPTANCE_20261110.md. No execution/epoch/release promotion. Next signal only after publication verification.
