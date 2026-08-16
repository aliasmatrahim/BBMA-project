# P2 Step 9 — Restart / Recovery Re-Audit

## Result
PASS — static re-audit after Fix A. Native MetaEditor compile already confirmed by user at 0 errors / 0 warnings.

## Scope
M24 restart/recovery path on canonical `blueprint-dev` source after P2 Step 9 Fix A.

## Re-Audit Findings

1. Exact EA ownership remains authoritative. Recovery first requires the live order to pass exact pair/symbol/magic ownership checks.
2. Missing or truncated execution hash no longer causes the live EA-owned order to disappear from lifecycle ownership.
3. When `H:` identity is missing, the order is still rebuilt into `g_monitored_trades` using broker truth for ticket, symbol, direction, entry, SL, TP, lot and open time.
4. No full `DecisionID` or execution hash is fabricated.
5. Missing execution identity maps to `REC_RECOVERY_INVALID`, freezing normal lifecycle actions while preserving risk accounting, portfolio counting and emergency liquidation ownership.
6. A tombstone is only upserted when a valid execution hash actually exists.
7. Hash-only recovery remains supported as `REC_IDENTITY_HASH_ONLY` when stable `H:` exists but full metadata is unavailable.
8. Full metadata is accepted only when parsed identity/pair/direction agrees with live broker state; otherwise it is downgraded safely.
9. Broker-side Entry/SL/TP/lot are preserved; recovery does not recreate strategy SL/TP or re-arm deprecated partial/breakeven behavior.
10. Initialization order remains fail-closed: pairs/magics are validated, local registries are reset, execution history and live monitored positions are rebuilt, then `g_is_initialized` becomes true.

## Residual Risk Review
No new static defect found in the audited restart/recovery path after Fix A.

Runtime restart behavior still requires controlled demo/Strategy Tester verification when MT4 data/runtime testing is available, especially broker comment truncation variants and terminal restart with live positions.

## Status
P2 Step 9: PASS (STATIC + COMPILE 0E/0W)
