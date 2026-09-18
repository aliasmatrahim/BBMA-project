# Q9 Build 4.89 P4 D1 Validation Closure — 2026-09-19

Issue: #101
Stack base: verified Q9 Stage-C head `24b83ba0a201665a9fe050ffdd2fb938ea143228`
Source-bearing P4 commit: `dab9c9e04b9898105131b2327dd8d7ee9eeafc92`

## Result

**Q9 P4 D1 VERIFIED — DURABLE RESEARCH ATTRIBUTION / OBSERVER-ONLY / NO ACTIVATION.**

Build identity:
- Version `4.89`;
- BuildTag `V489_Q9_P4_SHADOW_ATTR_20260919`;
- SourceRev `Q9_P4_D1_ATTRIBUTION_101_20260919`;
- MQ4 SHA-256 `d274de09860ca137d90a7113494998fb7637a2e997fbff3cfe7eef6f32f757c6`;
- EX4 SHA-256 `bd1a091c05e1cf42598a848eca63ecea47677b0633827d2cd1f18aeb90ccae82`.

## P4 D1 observer flow

The implementation freezes NMJE/Journey/M5 metadata only after the canonical decision is already `DEC_VALIDATED`.

If a broker ticket is subsequently created by the unchanged execution path:
1. existing execution identity is persisted;
2. existing D1TPW/C044 lifecycle initialization/checkpoint work runs;
3. P4 attribution is independently persisted in the ticket-scoped `BBXA1` domain;
4. P4 persistence failure logs only and cannot change `DecisionState`, `RejectionReason`, `recovery_state`, C044/D1TPW state, risk, lot or broker action.

Recovery determines canonical trade `recovery_state` first, then attempts P4 metadata load. The P4 result is diagnostic only.

Closed outcome attribution uses the existing exact selected closed order and its ticket/pair/magic checks before emitting realized net P/L plus P4 hashes.

## Static / regression

PASS:
- Q9 P4 attribution authority guard;
- Q9 P4 deterministic fail-closed persistence model;
- Stage-C/P2-P3 authority guard;
- deterministic P1 epoch model;
- NMJE read-only authority: 6/6;
- D1O execution identity guard;
- M12N orchestration-order guard;
- N3 activation firewall;
- `git diff --check`.

Cross-module comparison to verified Build 4.88:
- `CompareCanonicalCandidates`: byte-identical;
- `PriorityEngine_Atomic`: byte-identical;
- `InvalidationEngine_Atomic`: byte-identical;
- `RunEntryPreflightAndExecute`: byte-identical;
- `CheckRiskBeforeTrade`: byte-identical;
- `SendOrderWithRetry`: byte-identical;
- broker primitive counts unchanged: OrderSend=1, OrderClose=3, OrderModify=0, OrderDelete=0;
- C044 init/save/load call counts unchanged.

## Native compile

Portable MT4 MetaEditor: **0 errors / 0 warnings**, 1138 ms.

Evidence: `blueprint/audits/Q9_BUILD489_METAEDITOR_COMPILE_20260919.log`.

## Runtime

Isolated EURUSD M15 environment only:
- `ExpertsTrades=false`;
- `MaxTradePerPair=0`;
- `MaxTotalTrade=0`;
- InstanceID 89.

The first attempt encountered MT4 error 4024 while registering the unchanged EA timer. OnInit/OnTimer/OnDeinit were confirmed byte-identical to verified Build 4.88. MT4 then autosaved the profile without the failed expert; this explained why the first retry opened without EA attachment.

After restoring the profile from the verified Build 4.88 read-only template, the final clean retry proved:
- exact Build 4.89 identity;
- successful broker/pair/magic initialization;
- successful EA initialization;
- normal D1/NMJE/M5 observer state;
- connected heartbeat with zero monitored/F7-managed trades;
- graceful deinitialization.

Evidence: `blueprint/audits/Q9_BUILD489_RUNTIME_20260919.log`.

## Runtime limitation

Because the isolated acceptance intentionally disables trading and sets zero trade caps, no live `[NMJE-P4-OPEN]`, `[NMJE-P4-RECOVER]` or `[NMJE-P4-OUT]` event was generated. No synthetic trade was created.

Therefore this closure verifies P4 D1 architecture, fail-closed persistence model, native compilation and zero-authority runtime startup safety. It does **not** claim live-broker trade-attribution proof or production activation.

## Boundary

NMJE remains observation-only. M15 remains sole processing/final-decision clock. P4 cannot create/reject/rank/delay/risk-approve/execute/close a trade, cannot change C044/D1TPW lifecycle authority, and cannot change canonical recovery state.

Next Issue #101 work must remain separately scoped. P5 conflict subtype research may be re-audited next; no old source-bearing commit may be blindly cherry-picked.
