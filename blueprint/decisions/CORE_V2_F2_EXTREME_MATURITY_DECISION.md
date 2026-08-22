# CORE-V2-F2 — Extreme Maturity inside REM / REE

Date: 2026-08-22
Status: **RESOLVED — USER-APPROVED PROJECT CORE DECISION**
Branch: `blueprint-dev`

## Decision
For an Extreme to be eligible as a component of an executable REM or REE combination, it must be at least **reversal-confirmed**.

A standalone Extreme entry remains a different maturity level and requires the later **retest** entry stage.

Operational maturity distinction:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> RETEST/ENTRY-READY EXTREME`

- RAW EXTREME: MA5/MA10 outside the relevant outer BB under the strict accepted detector rule. Not sufficient for executable REM/REE.
- REVERSAL-CONFIRMED EXTREME: raw Extreme plus source-valid reversal confirmation. Eligible as an Extreme component of REM/REE.
- RETEST/ENTRY-READY EXTREME: reversal-confirmed Extreme plus the later retest. Required for standalone Extreme entry eligibility.

## Evidence classification
This decision is **SOURCE-INFERRED / STRONG HINT**, not an explicit verbatim Oma Ally rule for REM/REE component maturity.

Evidence:
- Finale V04 00:27:23–00:31:55 distinguishes raw Extreme condition, reversal confirmation and retest, and states that the retest is the point of standalone Extreme entry.
- Finale V05 00:46:16–00:53:55 teaches higher-timeframe Re-Entry being completed/read through lower-timeframe Extreme/MHV/direction structures, supporting a distinction between supporting Extreme context and standalone Extreme entry.
- Finale V05 00:54:12–00:54:40 mentions some Extreme occurrences embedded in higher-timeframe Re-Entry context behaving differently from normal standalone Extreme TP-Wajib treatment; this remains HOLD for TP semantics but reinforces that MTF component use is not identical to standalone Extreme entry.

## Rejected alternatives
- Raw Extreme alone as executable REM/REE component: rejected as too immature relative to the accepted Extreme lifecycle.
- Reversal + retest required for every REM/REE Extreme component: rejected because the source ties retest specifically to standalone Extreme entry and does not clearly require it for supporting MTF components.
- Disable REM/REE indefinitely: rejected as a safety-only engineering choice, not the selected Core interpretation.

## Implementation guard
This decision does **not** authorize inventing a reversal-candle algorithm. The project must separately define a deterministic source-faithful reversal-confirmation contract before code is patched.

Until that contract exists, active Mode 2 REM/REE cannot be declared fully Core-V2-compliant merely because raw M08 Extreme is present.
