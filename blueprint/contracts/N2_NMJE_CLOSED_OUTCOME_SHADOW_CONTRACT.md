# N2 NMJE Closed-Outcome Shadow Contract

Date: 2026-08-25
Status: DESIGN LOCK — diagnostic/research only

## Purpose
Provide a deterministic, non-trading telemetry bridge from a validated NMJE-tagged decision to its realized closed-order outcome, so N2 research can measure observed performance by nested relation without changing entry, exit, SL/TP, risk, priority or execution behavior.

## Ownership
This component is **not** a strategy module and owns no BBMA state. It may only read:
- an already-closed EA-owned MT4 order;
- the existing monitored-trade identity snapshot;
- the already-created N2 validated-decision shadow identity.

It must never call or modify:
- M08–M12 detectors/lifecycles;
- M13 combination assembly;
- M14 validation;
- M15 final selection;
- M16 invalidation;
- M17 SL/TP resolution;
- risk sizing/portfolio gates;
- `OrderSend`, `OrderClose`, `OrderModify` or any broker execution function.

## Required closed-outcome record
Canonical diagnostic marker:

```text
[N2-NMJE-OUT] PAIR=<symbol> TICKET=<ticket> DID=<decision-id-or-> DIDH=<execution-hash-or-> NET=<net-profit> CLOSE=<unix-time> REC=<recovery-state>
```

`NET` must equal realized `OrderProfit() + OrderSwap() + OrderCommission()` from the selected closed order.

## Identity rules
1. Freshly executed trade with full in-memory `decision_id`: emit both `DID` and existing persisted execution hash (`DIDH`).
2. Recovered trade where full `decision_id` is unavailable: emit `DID=-` and the exact persisted execution hash already recovered from the MT4 order comment.
3. No pair-only, timestamp-only or direction-only outcome matching is permitted.
4. Research tooling may use `DIDH` only after it proves that the hash maps to exactly one N2 validated DecisionID in the analyzed dataset. Any collision or ambiguity must fail closed and remain unattributed.
5. Missing identity is a research-data limitation, never a reason to alter or close a trade.

## Hook placement
Preferred hook is the existing monitored-trade compaction/removal path, immediately after a monitored ticket is proven closed and **before** that registry row is discarded. The telemetry call must be read-only. Existing compaction order and removal semantics must remain unchanged.

## Duplicate rule
One closed monitored registry row should emit at most one outcome record before removal. The research parser must still detect duplicate ticket/identity records and fail closed rather than double-counting.

## Recovery behavior
A restart may reduce identity from full DecisionID to the persisted execution hash. This is acceptable for telemetry if explicitly marked. The engine must never reconstruct a full DecisionID by guesswork.

## Accounting
Outcome classification is external research logic only:
- net > 0: observed win;
- net < 0: observed loss;
- net == 0: observed breakeven.

No outcome classification feeds back into NMJE state or future trade selection in N2.

## N2 scope guard
This contract authorizes telemetry and research attribution only. It does **not** authorize `NestedConfirmation`, rejection of `NESTED_CONFLICT`, preference for `NESTED_ALIGNED`, altered entry count, or any other execution gate.

## Implementation dependency
Implement only after N2-01 validated-decision shadow has materialized and passed native MT4 compile. The outcome logger must then receive its own static ownership guard and native 0E0W compile before runtime observation.
