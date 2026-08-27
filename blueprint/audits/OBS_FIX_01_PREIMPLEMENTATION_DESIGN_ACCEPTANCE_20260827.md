# OBS-FIX-01 — Preimplementation Design & Acceptance Matrix

Date: 2026-08-27
Status: PREPARATION ONLY / OBSERVER SOURCE UNTOUCHED
Scope: observability only

## 1. Timing and safety boundary

This record prepares the next observer build but does **not** modify `blueprint/runtime/V459_Runtime_Observer.mq4`.

The active R1 evidence candidate must not be changed mid-run. Implementation is locked until the current attributable runtime evidence is preserved, per `blueprint/queue/OBS_FIX_01_EVENT_DRIVEN_OBSERVER_20260827.md`.

No BBMA detection, M08-M16 authority, risk, SL/TP, lot sizing, execution, recovery decision or canonical EA source change is authorized by this preparation.

## 2. Current root cause

Current observer v1.00 is timer-driven:
- `OnInit()` sets `EventSetTimer(SnapshotSeconds)` and immediately calls `EmitSnapshot()`.
- every `OnTimer()` calls `EmitSnapshot()` again.
- every snapshot prints environment state, every relevant terminal GlobalVariable, every exact magic-range open BUY/SELL order, every matching historical order inside `HistoryLookbackHours`, and a snapshot-end marker.

Therefore an unchanged terminal produces repeated equivalent output indefinitely. Reducing `SnapshotSeconds` frequency or history lookback reduces volume but does not fix the underlying duplicate-log behaviour.

## 3. Locked future behaviour

Default observer mode must be **silent unless materially changed**.

The observer should keep local read-only fingerprints and emit records only when the observed state transitions.

### 3.1 Environment transitions
Track at least:
- terminal connected/disconnected;
- trade allowed/not allowed.

Emit only on initial state and subsequent transition.

### 3.2 GlobalVariable transitions
For relevant D1TPW/C044/EXEC_ID persistence namespaces:
- build a deterministic name-sorted snapshot;
- emit NEW when a relevant variable first appears;
- emit CHANGED when its value changes materially;
- emit REMOVED when a previously observed variable disappears;
- do not reprint unchanged variables.

The observer must never create, set or delete terminal GlobalVariables.

### 3.3 Live-order transitions
Track exact owned live BUY/SELL orders by ticket.

Always emit:
- OPEN_NEW when a new owned ticket appears;
- OPEN_CHANGED if execution-critical observable geometry changes, including SL, TP, lot, comment or other recorded identity fields;
- OPEN_REMOVED when a previously live ticket leaves the open pool.

Order enumeration order must not itself count as a state change. Ticket ordering/fingerprinting must be deterministic.

### 3.4 Closed-history transitions
Historical scanning may remain periodic, but output must be event-driven:
- emit HIST_NEW once when a newly closed owned ticket becomes visible;
- do not repeatedly print the same historical ticket on subsequent scans;
- if the terminal later exposes a materially different final record for the same ticket, emit HIST_CHANGED explicitly rather than silently replacing evidence.

`HistoryLookbackHours` may limit discovery scope but must not cause already-observed state to be spammed again.

### 3.5 Observer verbosity
Prepare an explicit observer verbosity input with a small, clear surface:
- `OBS_CHANGES_ONLY` — default; state transitions only;
- `OBS_DIAGNOSTIC` — transitions plus bounded diagnostic/heartbeat information;
- `OBS_VERBOSE` — deliberate full snapshot mode for short troubleshooting sessions.

Verbose mode must be opt-in. The default must never revert to periodic full-snapshot spam.

## 4. Execution-critical visibility boundary

The observer is a separate read-only Expert Advisor. It does not control or suppress `Print()` output emitted by the trading EA.

Therefore main-EA execution-critical records such as decision-final, execution attempt/result and broker rejection remain governed by the trading EA and must remain untouched by OBS-FIX-01.

Within the observer's own authority, new/changed open orders, ticket identity, history-close events, persistence-state changes, connection changes and recovery-relevant persistence transitions must remain visible even in changes-only mode.

## 5. Duplicate suppression design

Duplicate suppression must be semantic, not merely time-based.

Required properties:
- identical consecutive state does not print again;
- a state that changes away and later returns is a new transition and is printed;
- order-pool enumeration order cannot create false changes;
- GlobalVariable enumeration order cannot create false changes;
- one category changing must not force unrelated unchanged categories to be reprinted;
- observer restart may emit one attributable initial baseline, then returns to change-only behaviour.

## 6. Static safety guard for future implementation

Any OBS-FIX-01 implementation must fail if the observer source contains broker-write or strategy-authority calls.

At minimum forbid:
- `OrderSend(`
- `OrderClose(`
- `OrderModify(`
- `OrderDelete(`
- `GlobalVariableSet(`
- `GlobalVariableDel(`
- any inclusion/copy of BBMA signal-selection, validation, risk or execution authority.

Allowed operations are terminal reads, local in-memory comparison, deterministic formatting and `Print()` telemetry only.

## 7. Acceptance matrix

| ID | Case | Expected result | Evidence |
|---|---|---|---|
| OBS-00 | observer attach, normal state | one attributable initial baseline/start; no repeating unchanged flood | runtime |
| OBS-01 | no state changes for several timer periods | no repeated ENV/GV/OPEN/HIST records | runtime |
| OBS-02 | connection Y→N→Y | one record for each actual transition | runtime |
| OBS-03 | relevant GV created | one NEW record | runtime |
| OBS-04 | relevant GV value changes | one CHANGED record with old/new attributable values | runtime |
| OBS-05 | relevant GV unchanged | no duplicate record | runtime |
| OBS-06 | relevant GV removed | one REMOVED record | runtime |
| OBS-07 | new owned trade opens | one OPEN_NEW with ticket/pair/type/magic/open/SL/TP/lots/comment | runtime |
| OBS-08 | same open ticket remains unchanged | no duplicate OPEN record | runtime |
| OBS-09 | SL/TP or other tracked geometry changes | one OPEN_CHANGED | runtime |
| OBS-10 | live ticket disappears | one OPEN_REMOVED; later history discovery attributable to same ticket | runtime |
| OBS-11 | newly closed order appears in history | one HIST_NEW only | runtime |
| OBS-12 | same history ticket remains in lookback window | no repeated HIST record | runtime |
| OBS-13 | order-pool enumeration order changes only | no observer event | runtime |
| OBS-14 | GV enumeration order changes only | no observer event | runtime |
| OBS-15 | changes-only mode | default silent-unless-changed behaviour | native/runtime |
| OBS-16 | diagnostic mode | bounded diagnostics without periodic full history flood | runtime |
| OBS-17 | verbose mode | explicit full snapshots allowed only while selected | runtime |
| OBS-18 | observer restart | one fresh initial baseline then duplicate suppression resumes | runtime |
| OBS-19 | trading EA execution-critical event | trading EA logs remain untouched; observer does not suppress them | runtime |
| OBS-20 | static authority scan | no broker writes, no GV writes/deletes, no strategy/risk authority | static |
| OBS-21 | native compile | 0 errors / 0 warnings | MetaEditor |

## 8. Promotion gate

OBS-FIX-01 may not replace the current observer until:
1. current R1 evidence using the existing observer/runtime candidate is preserved;
2. implementation occurs on a separate build/branch;
3. duplicate-suppression selftests pass;
4. static no-write/no-authority guard passes;
5. native MetaEditor compile is 0 errors / 0 warnings;
6. OBS-00..OBS-21 are completed or explicitly BLOCKED without false PASS;
7. new observer EX4 identity is recorded separately from the currently running evidence binary;
8. no current R1 evidence is retroactively attributed to the new observer binary.
