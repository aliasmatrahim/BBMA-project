# D1-06 — MinRR Default-Off Decision

Date: 2026-08-24  
Branch: `d1-owner-dev`  
Decision: **KEEP `MinRRRatio` AVAILABLE, DEFAULT DISABLED (`0.0`)**

## User decision
`MinRRRatio` is retained as an optional project-level rejection filter, but it must not be enabled by default.

## Runtime meaning
- `MinRRRatio = 0.0` => filter disabled.
- `MinRRRatio > 0.0` => existing RR rejection check remains available where the current payload has a valid static TP distance.
- This optional numeric filter is **not represented as a universal BBMA/Oma Ally Core rule**.
- Future F7 targetless/lifecycle-managed Re-Entry payloads remain governed by the F7 resolution: they must structurally bypass numeric RR when no source-valid static reward distance exists, regardless of this input.

## Scope
This decision changes only the default input state and build identity. It does not alter BBMA detectors, D1/H4/H1/M15 hierarchy, SL/TP construction, lot sizing, execution order, or lifecycle rules.
