# OBS-FIX-01 — Observer Anti-Spam / State-Change Logging

Date: 2026-08-27
Priority: NEXT BUILD — DO FIRST
Scope: Observability only. No trading-logic authority change.

## Problem
Current runtime observer is too chatty and can flood the MT4 Experts tab. Continuous/cycle-driven prints make historical execution evidence effectively impossible to inspect because new lines keep forcing the log view to move.

## Required behaviour
Convert observer logging from cycle-driven to event-driven.

Default behaviour must be `silent unless changed`.

Print only when one of these events occurs:
- canonical state changes;
- setup becomes complete;
- final decision is created/validated/rejected/invalidated;
- order execution succeeds or fails;
- lifecycle becomes invalid or resets;
- canonical owner/cycle is superseded;
- recovery state materially changes;
- other execution-critical events that must remain visible.

Do NOT print repeated unchanged state on every scan/candle/process cycle.

## Requirements
1. State-change logging only by default.
2. Duplicate log suppression for identical consecutive observer records.
3. Optional observer debug level so verbose diagnostics can be enabled deliberately when needed.
4. Execution-critical logs must always remain visible regardless of observer verbosity:
   - decision final;
   - execution attempt/result;
   - ticket/order-open details;
   - rejection/failure reason;
   - lifecycle invalid/reset where relevant to execution.
5. No change to BBMA detection, M08-M16 authority, risk, SL/TP, lot sizing, order execution, or recovery decisions.
6. Existing runtime candidate currently collecting evidence must NOT be modified mid-run.

## Timing lock
Implement this first in the next build after the current live runtime evidence is preserved. Treat it as higher immediate usability priority than cosmetic dashboard changes because observer spam currently prevents practical collection of execution evidence.

## Acceptance criteria
- Experts tab remains readable during normal runtime.
- Unchanged observer states do not repeat continuously.
- A newly opened order can be found reliably in Experts after the event.
- State transitions remain traceable.
- Verbose observer mode can be enabled explicitly for deep diagnostics.
- Native MetaEditor compile: 0 errors, 0 warnings.
- Static regression confirms no execution/strategy semantic change.
