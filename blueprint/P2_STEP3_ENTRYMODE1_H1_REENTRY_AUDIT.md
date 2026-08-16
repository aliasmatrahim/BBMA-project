# P2 Step 3 — Entry Mode 1 / H1 Re-Entry End-to-End Static Audit

Status: **PASS (STATIC FUNCTIONAL AUDIT)**

Canonical source audited:
`blueprint/source/BBMA_PROFESSIONAL_EA.mq4`

Canonical SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

## Scope
Audit EntryMode=1 from H1 Re-Entry ownership through final decision, invalidation, SL/TP resolution, sizing/risk gates and execution handoff. Runtime Strategy Tester confirmation remains deferred because P2 Step 1 is KIV due to MT4 historical-data integrity problems.

## Findings

### M12 — H1 Re-Entry lifecycle
- Re-Entry detector/state owner remains M12.
- Only valid closed timeframe data advances lifecycle.
- Type 1 confirms directly on source-valid MA5/10 cluster touch.
- Type 2 requires three distinct consecutive closed candles retaining MA5/10 + MID BB confluence, followed by the required MA-cluster touch.
- Type 3 begins on CSM and confirms only on later MA5/MA50 retrace.
- Type 4 begins on CSD and confirms only on later MA5/10 retrace.
- Candidate/confirmed states use intrinsic expiry via `MaxWaitBars_ReEntry` on the owner timeframe.
- Confirmed H1 Re-Entry preserves direction, confirmation candle, owner timeframe, entry snapshot and expiry metadata.

### M15 — Entry Mode 1 authority
`IsEntryModeCandidateAllowed()` explicitly permits only `SIGNAL_RE_ENTRY` when `EntryMode == 1`.

REM/RRE/REE cannot pass Entry Mode 1 eligibility. No signal-score or PriorityTier ranking can override this gate.

`BuildConfirmedReEntryCandidate()` further requires:
- owner state = `RE_STATE_CONFIRMED`;
- `IsValid == true`;
- BUY/SELL direction only;
- timeframe exactly `PERIOD_H1`;
- valid confirmation candle;
- owner expiry not already passed.

Therefore Entry Mode 1 is statically constrained to confirmed **H1 Re-Entry only**.

### M15 direction conflict behavior
BUY and SELL candidates are collected before the single atomic M15 decision pass. If valid opposite-direction entries coexist, M15 refuses to invent a preference and emits conflict/no canonical trade.

### M16 — owner-aware revalidation
A standalone H1 Re-Entry decision is revalidated against the persistent M12 owner state before execution. Direction, timeframe and confirmation candle must still match the owner snapshot. Owner expiry produces `DEC_EXPIRED`; owner-state mismatch produces invalidation.

### M17 — Entry Mode 1 SL/TP provenance
For `SIGNAL_RE_ENTRY`, the approved SL/TP source component must be a H1 Re-Entry component.

The executable geometry is source-owned:
- structural SL = one broker point beyond the source closed H1 candle wick (EA safety buffer explicitly separated from BBMA source semantics);
- TP = approved Bollinger destination from that same source timeframe;
- stale/crossed destinations fail closed;
- MaxSL and MinRR remain rejection filters only and do not manufacture SL/TP.

### M21/M19/M20/M22 downstream preservation
After M17 resolves valid geometry:
- M21 sizes only from frozen Entry/SL/account snapshot;
- M19 filters risk only;
- M20 applies prospective portfolio/protection gate only;
- M22 executes the immutable approved decision and applies duplicate/idempotency protection.

No downstream module is permitted to convert a REM/RRE/REE candidate into an Entry Mode 1 trade or alter H1 Re-Entry strategy identity.

## Non-blocking observation
`BuildReEntrySignal()` still exists as a legacy helper using MaxSL/MinRR-derived geometry. It is **not accepted as M17 source resolution** in the audited executable path. It should remain non-authoritative; future cleanup may remove it only if call-site analysis proves it is dead code. This is not a P2 Step 3 blocker.

## Result
**P2 Step 3 static audit PASS.**

No new Entry Mode 1 / H1 Re-Entry architectural or functional defect was found requiring a source repair.

Runtime confirmation remains pending until P2 Step 1 Strategy Tester data quality is available.

Next recommended gate: **P2 Step 4 — Entry Mode 2 REM/RRE/REE end-to-end static audit.**
