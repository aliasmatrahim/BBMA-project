# P3 — Native MetaEditor Compile Repair

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **SCREENSHOT-DERIVED SYNTAX DEFECT CONFIRMED / FIX IMPLEMENTED / RECOMPILE REQUIRED**

## Evidence
Native MetaEditor screenshot showed a cascade beginning around the F4 H4-owner block, including `semicolon expected`, identifiers reported as already used, global-scope expression errors, and undefined-function fallout.

## Root cause
The earlier F4 MQL4 reference-repair helper used `replace_between()` that retained the end marker while also embedding the same end marker inside the replacement text. That duplicated five function signatures and broke parser synchronization.

Confirmed corrupted signatures repaired:
1. `ClassifyH4AuthoritativeSignal`
2. `VerifyH4OwnerCheckpoint`
3. `RecoverH4DirectionalOwners`
4. `NoteH4ReEntryInheritance`
5. `RecoverExistingOrders`

## Preventive fix
`.github/scripts/fix_core_v2_f4_mql4_refs.py` now consumes the original end marker with `b + len(end)` instead of appending from `b`, preventing the same duplication if the helper is ever re-run.

## Strategy boundary
No BBMA strategy rule, signal condition, owner semantics, entry signature, SL/TP, risk logic, or TradeLock policy was changed. This patch is syntax/parser repair only.

## Required verification
Compile the updated `blueprint/source/BBMA_EA.mq4` in native MT4 MetaEditor. Target remains **0 errors / 0 warnings**. Any remaining compiler diagnostics must be treated as the next compile-fix loop.
