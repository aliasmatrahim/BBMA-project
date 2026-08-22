# P3 Cleanup Pass 2 Plan

Status: IN PROGRESS

Purpose: remove only proven dead residual symbols after Cleanup Pass 1 compiled 0E0W.

Rules:
- No BBMA strategy condition changes.
- No risk/execution/recovery behavior changes.
- Remove only symbols that have no active reference.
- Preserve MQL4 event callbacks and active compatibility surfaces.
- Native MetaEditor must remain 0E0W after merge.

Initial proven candidates:
- `GetEffectiveExpiry()` residual helper: no caller.
- `ENUM_SIGNAL_MODE`: definition-only.
- `SignalMemory` instance fields `buy_signal_memory` / `sell_signal_memory`: declaration-only; struct may be removable if no other use survives.
- Other enum constants/fields may be removed only if fixed-point reference scan proves definition-only.
