# C040 HTF-MHV / LTF-Extreme Context Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / HTF MHV REMOVES REDUNDANT LTF-MHV WAIT / DOES NOT BYPASS EXTREME MATURITY / NO NEW EXECUTION SHORTCUT**

## Decision
The previous broad C040 HOLD is narrowed.

Accepted bounded interpretation:
- when the higher-timeframe MHV/MLV is already source-valid and mature, a lower-timeframe Extreme that forms in a structurally compatible direction may be used as lower-timeframe completion/context without waiting for an additional lower-timeframe MHV/MLV merely to restate the same nested relationship;
- the higher-timeframe MHV does **not** automatically mature the lower-timeframe Extreme;
- a lower-timeframe Extreme must still satisfy the accepted Extreme lifecycle before it can become entry-ready under any standalone Extreme authority;
- raw Extreme detection alone remains non-executable.

Canonical bounded sequence:

`HTF MHV VALID/MATURE -> descend to LTF -> source-valid LTF Extreme appears -> no redundant LTF MHV wait is required for the nested structural read -> LTF Extreme must still satisfy its own reversal confirmation/retest maturity before any entry-ready interpretation`

## Explicit guards
This decision must not be interpreted as:
- `HTF MHV + raw LTF Extreme = immediate BUY/SELL`;
- HTF MHV remotely maturing or confirming the LTF Extreme;
- bypassing Extreme reversal confirmation or retest requirements;
- bypassing Momentum invalidation;
- removing any component from the exact approved REM/RRE/REE signatures;
- converting a watch/context relationship into independent execution authority;
- authorizing advanced/no-TP Extreme exceptions that remain unresolved elsewhere.

## Exact combination preservation
The approved combination signatures remain unchanged:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

C040 cannot be used to delete or substitute any required component in those signatures.

## Source basis
- Home Course HC-P14-008 states that when the higher-timeframe MHV is complete/valid, the lower-timeframe Extreme may be used without waiting for another lower-timeframe MHV.
- Accepted Core V2 keeps normal Extreme maturity intact: raw MA/BB condition is not standalone entry authority; reversal confirmation and later retest remain part of the normal lifecycle.
- Finale contains advanced/MTF Extreme contexts, but the exact deterministic classification and TP exceptions remain unresolved and therefore do not justify a broader shortcut.
- External/community BBMA material is corroboration only and does not outrank project source governance.

## Classification
- no redundant lower-TF MHV wait after valid higher-TF MHV for structural completion/context: **SOURCE-SUPPORTED / ACCEPTED WITH BOUNDED SCOPE**;
- lower-TF Extreme maturity remains independent: **CORE / UNCHANGED**;
- immediate execution from raw lower-TF Extreme: **REJECTED / NOT AUTHORIZED**;
- advanced/no-TP Extreme exception: **SEPARATE HOLD / NOT RESOLVED HERE**.

## Current EA impact
This decision is best represented in NMJE/M12N as read-only cross-timeframe structural context. It does not authorize a new MQL4 execution path, does not alter REM/RRE/REE, and does not alter SL/TP, MM, ownership, ranking or broker execution.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this record alone.
