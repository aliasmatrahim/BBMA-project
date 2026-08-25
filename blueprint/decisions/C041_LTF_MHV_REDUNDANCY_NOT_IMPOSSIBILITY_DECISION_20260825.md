# C041 LTF-MHV Redundancy / Not-Impossibility Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / CORRECT / REJECT ABSOLUTE CLAIM / REDUNDANT-MHV REQUIREMENT ONLY / NO DETECTOR SUPPRESSION**

## Decision
The previous broad C041 HOLD is resolved as a source-interpretation correction.

Accepted bounded interpretation:
- when a higher-timeframe MHV/MLV or Re-Entry is already source-valid and mature, an additional lower-timeframe MHV/MLV may be unnecessary for a specific nested lower-timeframe Extreme sequence;
- `not required` must not be interpreted as `cannot occur`;
- a genuine lower-timeframe MHV/MLV may still form naturally and must remain detectable and retain its own source-valid lifecycle;
- higher-timeframe completion does not suppress, invalidate or disable lower-timeframe structure detection.

Canonical interpretation:

`HTF MHV/RE-ENTRY VALID -> nested LTF repeated-Extreme structure -> additional LTF MHV may be REDUNDANT for that specific structural completion`

but:

`LTF MHV may still form -> if source-valid, preserve it as genuine structure`

## Explicitly rejected
The following absolute interpretations are rejected:
- `HTF MHV valid => LTF MHV is impossible`;
- disabling/suppressing H1 or other LTF MHV detectors after HTF MHV;
- invalidating a source-valid LTF MHV merely because the parent HTF already has MHV/Re-Entry;
- using this rule to create or accelerate an execution path;
- deleting any component from exact REM/RRE/REE signatures.

## Relationship to C040
C041 clarifies the semantics behind C040:
- C040: valid HTF MHV can remove a redundant requirement to wait for another LTF MHV in a bounded nested relationship;
- C041: this redundancy does not mean the LTF MHV is forbidden or impossible.

## Exact combination preservation
The approved combination signatures remain unchanged:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

A contract-required MHV/MLV component remains required even if another nested reading would otherwise regard an additional MHV as redundant.

## Source basis
- Home Course material uses wording equivalent to `tidak perlu ada MHV` in the nested/repeated-Extreme context after a valid higher-timeframe MHV/Re-Entry.
- The prior ledger wording was more absolute and therefore required correction.
- Finale supports recursive/cross-timeframe BBMA structure but does not establish a universal law that HTF MHV makes later LTF MHV impossible.
- External/community BBMA material is corroboration only and does not outrank project source governance.

## Classification
- extra LTF MHV not required in bounded nested context: **SOURCE-SUPPORTED / ACCEPTED**;
- LTF MHV impossible after HTF MHV: **REJECTED**;
- source-valid LTF MHV detection/lifecycle: **PRESERVED**;
- new execution authority: **NOT AUTHORIZED**.

## Current EA impact
No detector should be disabled or suppressed because of this decision. The current owner/detector architecture remains intact. This decision does not alter entry eligibility, combination signatures, SL/TP, MM, ownership, ranking or broker execution.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this record alone.
