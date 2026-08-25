# GAP-A2 — Static TP vs C044 Lifecycle Reclassification

Date: 2026-08-26
Branch: `d1-owner-dev`
Baseline: `Version 4.5.7 - N1.1 NMJE Coverage Overlay`
Status: **REPO SOURCE/CONTRACT GAP CLOSED / RUNTIME-ACTIVATION GAP REMAINS**

## Finding being reconciled

`SLTP-02` observed that a universal static Re-Entry-owned outer-BB broker TP cannot represent the complete approved post-Re-Entry continuation/failure lifecycle.

## Architecture is already resolved

The later approved C044 TP Architecture Reconciliation explicitly resolves the conflict:

- a C044-managed Re-Entry-owned position does not keep the universal static outer-BB broker TP;
- M17 resolves the hard structural SL and marks the payload lifecycle-managed;
- M22 sends `TP=0` for that managed payload;
- the owner-timeframe outer BB becomes an event boundary, not a resting mandatory broker TP;
- M23 owns the normal full-position lifecycle close after a latched C044 exit;
- M24 owns persistence/recovery/fail-frozen reconstruction;
- M20 emergency protection retains precedence;
- `MinRRRatio > 0` fails closed for targetless C044 unless a future deterministic reward reference is approved.

The active source already contains these gated paths. In v4.57:
- `decision.TakeProfit = EnableC044Lifecycle ? 0.0 : normalizedTP`;
- `decision.C044LifecycleManaged = EnableC044Lifecycle`;
- M17/M22 accept SL-only C044 payload geometry;
- M23/M24 C044 lifecycle/recovery machinery is present;
- `EnableC044Lifecycle = false` remains locked OFF.

## Why the gate remains OFF

Static/native validation is not the remaining blocker. The hosted MT4 attach/runtime step could not establish a broker session.

Still required on a broker/demo environment:
- targetless checkpoint persistence across terminal restart;
- chronological replay of missed owner-timeframe closed candles;
- failed-Momentum close timing after an outer-BB test;
- valid Momentum -> wait-next-ReEntry -> re-arm;
- opposite mature Extreme cycle supersession;
- M20 emergency precedence;
- no duplicate lifecycle close or new-entry authority.

## Reclassification

`GAP-A2` is therefore **not an open repo-closable source/contract gap anymore**.

It is moved to the broker/runtime class:

`C044 architecture/source implemented and gated OFF -> broker/demo runtime evidence -> explicit activation review`.

The current gate-OFF static outer-BB behaviour remains evidence-continuity behaviour; it must not be described as the final C044 exit architecture.

## Non-change guarantees

- C044 remains OFF;
- no N1/N2/N3 work resumes;
- no new lifecycle rule is invented;
- no TP2/TP3, trailing, partial-close or automatic opposite entry;
- no change to REM/RRE/REE or owner-timeframe identity.

## Verdict

**GAP-A2 repo source/contract closure: PASS. Remaining work is Class-B broker/demo validation plus a later explicit C044 activation review.**
