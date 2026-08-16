# P2 Step 2 — Static Functional Path Audit

Status: **PASS (STATIC PATH AUDIT)**

Canonical source audited:
`blueprint/source/BBMA_PROFESSIONAL_EA.mq4`

Canonical SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

## Scope
This step audits code-path ownership and functional routing without requiring MT4 historical-data quality. It does not replace Strategy Tester runtime evidence.

## Verified paths

### 1. M13 collector path
- M13 only copies owner snapshots.
- Same-candle CSD/eCSD duplicate classification is suppressed.
- REM/RRE/REE candidates use exact source-defined component/TF signatures.
- M13 does not assign SL/TP authority.

### 2. M14 validation path
- M14 validates exact REM/RRE/REE component signatures.
- Direction consistency is required.
- No invented priority ranking is introduced.
- Valid candidates remain SL/TP-source neutral for downstream resolution.

### 3. M15 final-entry authority
- Entry Mode 1 admits only `SIGNAL_RE_ENTRY`.
- Entry Mode 2 admits `SIGNAL_RE_ENTRY`, `SIGNAL_REM`, `SIGNAL_RRE`, `SIGNAL_REE` only.
- Standalone Re-Entry normalization accepts confirmed H1 Re-Entry only.
- Opposite BUY/SELL validated opportunities fail closed instead of inventing a tie-break.
- Same-direction canonical selection is deterministic bookkeeping based on freshness/identity, not a BBMA quality ranking.

### 4. M16 owner-aware invalidation
- Decision components are revalidated against persistent owner state.
- Re-Entry/MLV/Extreme expiry is owner-specific.
- Invalid owner state and expiry are distinguished.
- Explicit candidate expiry is used only when supplied by an owner.

### 5. M17 -> M21 -> M19 -> M20 -> M22 preflight
- M17 resolves and validates source-owned SL/TP first.
- M21 sizes from the frozen M17 payload/snapshot and cannot repair Entry/SL/TP.
- M19 validates prospective risk after lot sizing.
- M20 blocks during emergency latch and performs prospective portfolio limits.
- M22 receives immutable approved payload and is execution-only.

### 6. M22 idempotent execution
- Stable execution identity is checked before each send attempt.
- Ambiguous broker outcomes are reconciled and are not automatically resent.
- Execution deviation is checked against the frozen decision entry reference.
- Trade-lock checks are limited to exact EA-owned live trades.

### 7. M23 lifecycle
- Broker-side M17 SL/TP is preserved for normal exits.
- No trailing stop, breakeven, TP2/TP3, synthetic TP or partial-close policy is active.
- Emergency basket-loss closure is the only active M23 broker-side close policy.
- EA ownership/magic is revalidated before lifecycle action.

### 8. M24 recovery
- Recovery operates only after exact EA ownership validation.
- Stable execution hash is required.
- Truncated comment metadata is not used to fabricate full strategy identity.
- Broker-side Entry/SL/TP/lot are preserved.
- Recovery states fail closed when geometry/lot ownership is invalid.

### 9. M27 orchestration
- Both BUY and SELL owner snapshots are collected before the single M15 final-authority pass.
- Entry routing is `M13 -> M14 -> M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22`.
- Tick lifecycle remains `M20 ManagePortfolio -> M23 ManagePositions -> emergency gate -> strategy scan`.
- Processing is driven by a new closed M15 candle per pair.

## Findings requiring repair
**None found in this static path audit.**

No BBMA semantic change is required by P2 Step 2.

## Limitation
P2 Step 1 remains KIV because local MT4 Strategy Tester historical data produced `TestGenerator: unmatched data error`. Runtime assertions such as actual signal occurrence, broker error handling, and order behavior still require clean tester/live-demo data.

## Result
**P2 STEP 2 = PASS — no new static functional-path defect found.**

Next recommended gate: P2 Step 3 — focused static/deterministic audit of Entry Mode 1 eligibility and H1 Re-Entry lifecycle end-to-end, while P2 Step 1 remains KIV.
