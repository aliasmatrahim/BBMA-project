# P2 Step 5 — SL/TP Provenance, Direction, MaxSL/MinRR, Broker StopLevel Audit

## Scope
Static audit of canonical P1 release-candidate source:
`blueprint/source/BBMA_PROFESSIONAL_EA.mq4`

Canonical SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

This step verifies only the authoritative execution path. Legacy/non-authoritative helper builders are not treated as active SL/TP ownership.

## Findings

### 1. Source owner mapping — PASS
M15 resolves the SL/TP source component only from a Re-Entry component with the expected owner timeframe:
- standalone H1 Re-Entry -> H1 Re-Entry source
- REM -> H4 Re-Entry source
- RRE -> D1 Re-Entry source
- REE -> D1 Re-Entry source

No raw Extreme, MLV, CSD, eCSD, CSM, dashboard or scoring module can become the SL/TP owner.

### 2. Closed-candle provenance — PASS
M17 resolves the exact source candle by `iBarShift(..., true)` and rejects any source resolving to shift < 1. The resolved time must exactly equal the stored component candle time. Therefore current/forming candle data cannot silently replace the locked source candle.

### 3. Structural SL — PASS
The protective SL is derived from the source-owned closed candle wick:
- BUY: source candle low minus one broker point
- SELL: source candle high plus one broker point

The one-point extension is explicitly engineering safety (`EA_SAFETY`), not represented as a PDF Oma Ally rule.

### 4. BB destination TP — PASS
The target is resolved from the source-owned timeframe and exact closed source candle:
- BUY -> upper Bollinger Band
- SELL -> lower Bollinger Band

If that historical destination is already crossed/stale relative to the live execution reference, M17 fails closed. It does not substitute a fixed-pip, RR-derived, TP2/TP3 or other invented target.

### 5. Direction geometry — PASS
M17 requires:
- BUY: SL < Entry < TP
- SELL: TP < Entry < SL

Market execution reference is ASK for BUY and BID for SELL. Broker close/trigger-side validation uses BID for BUY and ASK for SELL.

### 6. MaxSLPips — PASS as risk cap only
`MaxSLPips` does not manufacture or move the structural SL. After source resolution, M17 rejects the setup when the actual structural SL distance exceeds the configured maximum.

### 7. MinRRRatio — PASS as rejection filter only
`MinRRRatio` does not create TP. The already source-resolved TP/SL pair is measured and rejected when its RR is below the configured threshold.

### 8. Broker StopLevel — PASS
The compile-repair-completed `RiskValidationSnapshot.StopLevel` is used in M17. Minimum broker distance is calculated as `StopLevel * Point` and both SL and TP are rejected if too close to the correct close/trigger-side market price.

### 9. Fail-closed behavior — PASS
M17 rejects unresolved source ownership, invalid historical source shift, invalid market price, bad directional geometry, excessive SL, insufficient RR, and broker StopLevel violations. It does not repair these by inventing another SL/TP.

## Non-blocking observation
A legacy helper `BuildReEntrySignal()` still contains MaxSL/MinRR-derived construction logic, but it is not the authoritative M17 execution path audited here. It should remain classified as dead/legacy code unless later runtime evidence proves it is reachable. Do not re-enable it as SL/TP authority.

## Result
**P2 STEP 5 = PASS (STATIC FUNCTIONAL AUDIT)**

No new fix is required from this step.

Runtime Strategy Tester verification remains deferred together with P2 Step 1 until MT4 historical-data integrity is available.
