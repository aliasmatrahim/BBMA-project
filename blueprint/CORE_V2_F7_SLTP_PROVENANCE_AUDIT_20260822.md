# CORE-V2-F7 — M17 SL/TP Provenance Audit

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **SOURCE-GOVERNANCE DECISION REQUIRED / NO CODE BUG CLAIM**

## Scope
Determine whether the currently executable M17 SL/TP mapping can accurately be described as fully derived from the authoritative BBMA/Oma Ally Core sources.

## Source-supported findings
The authoritative rule digest explicitly supports normal **Extreme TP-Wajib** structure:
- SELL Extreme -> opposite MA5/MA10 Low area as the normal first mandatory objective;
- BUY Extreme -> opposite MA5/MA10 High area as the normal first mandatory objective;
- Mid BB is farther/max context.

The authoritative Core digest does **not** state a universal executable rule that every confirmed H1 Re-Entry, REM, RRE or REE must use the outer Bollinger Band of its Re-Entry source timeframe as broker TP.

The authoritative Core digest also does **not** state a universal broker hard-SL formula of exact Re-Entry source-candle wick plus one broker point.

Finale conflict tracking explicitly excludes/rejects a personal MA10+allowance stop method as a universal Core SL and does not promote a universal hard-SL formula into Core.

## Current M17 project contract
The current M17 contract deliberately separates provenance:
- `PDF_CORE` — explicit source semantics;
- `FORUM_SUPPORTED` — community-supported BBMA destination/exit interpretation;
- `EA_SAFETY` — deterministic broker-side autonomous protection.

Current executable mapping is:
- standalone H1 Re-Entry -> H1 outer BB TP;
- REM -> H4 outer BB TP;
- RRE/REE -> D1 outer BB TP;
- hard SL -> exact mapped Re-Entry source-candle wick +/- one broker point.

The contract itself classifies the hard SL as **EA_SAFETY informed by FORUM_SUPPORTED structural practice**, not as an explicit PDF rule.

## Audit conclusion
The current M17 mapping is internally explicit and provenance-honest, but it is **not accurate to call the complete executable SL/TP pair 100% PDF/Oma-Ally Core-derived** based on the currently accepted source set.

This is a governance/classification issue rather than a proven execution-code defect.

## Decision boundary
A project-level decision is required before F7 can close:

### Option A — retain current mixed-provenance execution policy
Keep the current deterministic broker TP/SL mapping, but continue labeling it accurately as `FORUM_SUPPORTED` / `EA_SAFETY` where applicable. Do not advertise the complete executable SL/TP as explicit PDF Core.

### Option B — require fully Core-derived executable SL/TP
Do not call M17 final until stronger authoritative source evidence is found for each executable Re-Entry/REM/RRE/REE TP and hard-SL rule. If no such evidence exists, redesign/exclude unsupported broker exit mapping rather than silently inventing it.

## Recommendation
For engineering continuity, **Option A** is the safer implementation policy because it preserves a deterministic protective broker SL/TP while keeping provenance honest. However, this choice affects the project's claim of “100% BBMA Core” and therefore requires explicit user approval.

No EA source code was changed by this audit.
