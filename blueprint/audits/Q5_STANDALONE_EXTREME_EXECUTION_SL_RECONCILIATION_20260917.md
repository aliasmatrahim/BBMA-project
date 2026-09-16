# Q5 — Standalone Extreme Execution Scope + SL Authority Reconciliation

Date: 2026-09-17
Issue: #175
Owner baseline: `d1-owner-dev@e2c1a35743e6251f8ee499870aad248e43adb06b`
Scope: source/contract reconciliation only; no EA/Core/runtime-authority change in this audit.

## Executive result

Standalone Extreme entry semantics are source-resolved at `RETEST/ENTRY-READY` maturity, and normal Extreme TP-Wajib semantics are source-resolved.

The remaining blocker for autonomous standalone Extreme execution is the protective hard-SL mapping. The primary PDF provides a real Extreme-context wick/shadow stop concept, but not enough deterministic detail for a complete two-sided MQL4 broker formula without an explicit project execution mapping.

Classification:
- entry maturity: **SOURCE-SUPPORTED / RESOLVED**;
- TP semantics: **SOURCE-SUPPORTED / RESOLVED**;
- structural wick/shadow SL concept: **PARTIAL SOURCE-SUPPORTED**;
- exact autonomous hard-SL formula: **PROJECT DECISION REQUIRED / NOT SOURCE-LOCKED**;
- code authorization from this audit: **NONE**.

## Mandatory evidence route used

`SOURCE_INDEX -> Core V2 -> Finale/rule index -> primary PDF -> secondary PDF -> Tier-B Home Course -> conflict/HOLD register -> existing SLTP audits/contracts -> current EA`.

No zero-result search was treated as proof of absence.
## Entry authority reconciliation

Accepted Core already distinguishes:

`RAW EXTREME -> REVERSAL-CONFIRMED -> RETEST/ENTRY-READY`.

Only `RETEST/ENTRY-READY` is sufficient for standalone Extreme entry. RAW Extreme remains non-executable, and reversal-confirmed Extreme remains sufficient only where an approved combination contract uses it as a component.

The primary PDF and Home Course both support the sequence `Extreme -> reverse candle -> retest candle (entry)`. Current Core V2/F2 supplies the approved deterministic reversal/retest mapping.

**Finding E1 — KEEP.** No new detector, reversal rule or retest rule is required for Issue #175.

## TP authority reconciliation

Normal standalone Extreme TP-Wajib is already accepted:
- SELL Extreme -> opposite MA5/MA10 Low area first;
- BUY Extreme -> opposite MA5/MA10 High area first;
- Mid BB is farther/maximum context, not a reason to ignore the first opposite MA5/MA10 objective.

The primary PDF describes mandatory profit taking after an Extreme, and the Home Course states that Extreme entry must TP at MA5/MA10, with Mid BB as the farthest context.

**Finding E2 — KEEP / SOURCE-SUPPORTED.** Issue #175 does not need a fabricated fixed-RR or outer-BB TP.

A broker implementation still requires an explicit static-vs-lifecycle execution mapping, but that mapping must preserve the source-owned TP-Wajib event rather than manufacture reward from RR.
## Protective SL reconciliation

The primary operational PDF contains the strongest relevant stop evidence: in the Extreme section it says an SL can be placed a few pips beyond the highest shadow/wick.

This is genuine Extreme-context source support, but it does not deterministically establish all of the following for autonomous execution:
- an explicit BUY mirror below the lowest wick;
- the exact Extreme lifecycle candle window that owns the highest/lowest wick;
- the numeric value of “a few pips”;
- spread, tick-size, StopLevel or FreezeLevel normalization.

The secondary PDF does not close those details. The Tier-B Home Course strongly reinforces Extreme entry/TP-Wajib but does not provide a deterministic hard-SL formula in the reconciled relevant material.

Finale V07 MA10 + allowance stop material remains personal risk-management evidence and is explicitly REJECT/HOLD from universal Core. It cannot be substituted for the missing deterministic Extreme formula.

Registered forum evidence retained by the project provides no stronger traceable Extreme hard-SL formula. Existing F7/SLTP audits reached the same provenance boundary.

**Finding E3 — PROJECT DECISION REQUIRED.** The source supports a structural wick/shadow protection concept, but exact two-sided broker-SL execution still needs an explicitly labelled project/EA-safety mapping.

No fixed-pip, RR-derived, MA10+allowance, arbitrary lookback, ATR, swing-scan or Re-Entry SL formula may be silently reused to close this gap.
## Minimal Option-A execution scope

For Issue #175, the smallest architecture-preserving executable scope is **standalone H1 Extreme at `RETEST/ENTRY-READY` maturity only**, still passing the existing M11 D1 strategic-owner gate and M15 atomic final-authority flow.

Reason:
- H1 is the current main signal/standalone-entry layer;
- D1 already has a separate `D1_OPP_EXTREME_TPW` project-extension contract with LTF Re-Entry execution identity;
- H4 is the immediate structural/setup parent;
- M15 is the sole processing clock / lower-TF orchestration layer.

This H1-only boundary is a **PROJECT EXECUTION SCOPE**, not a verbatim source statement. It avoids silently creating four independent standalone-Extreme execution families.

The current `D1_OPP_EXTREME_TPW` hard-SL design must not be copied into standalone Extreme. Its hard-SL owner is a fresh LTF Re-Entry by explicit contract, which is a different execution identity.

## Required decision before code

To continue Option A safely, choose between:

1. **Strict source-only:** keep standalone Extreme non-executable until stronger evidence resolves the exact BUY/SELL hard-SL formula; or
2. **Explicit project execution mapping:** approve a deterministic Extreme-specific structural hard-SL mapping while preserving its provenance as `PROJECT_EXECUTION_POLICY / EA_SAFETY`, not universal Oma Ally Core.

If option 2 is selected, the project must separately lock:
- wick-window ownership;
- BUY/SELL symmetric mapping;
- numeric buffer policy for “a few pips”;
- broker normalization;
- MaxSL as rejection-only and MinRR as rejection-only.
## Evidence pointers

- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` sections 5.1–5.4 and 11–13
- `docs/references/original/Oma ally BBMA - AL.pdf` pages 2, 5–6
- `docs/references/original/333531988-BBMA-Home-Course.pdf` Lesson 7 / summary
- `docs/references/video/oma_ally_finale/BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md` CF-10
- `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`
- `blueprint/CORE_V2_F7_M17_SLTP_PROVENANCE_AUDIT.md`
- `blueprint/decisions/CORE_V2_F7_PATH_A_STRICT_CORE_PROVENANCE_DECISION.md`
- `blueprint/audits/SLTP_RECONCILIATION_MATRIX_20260826.md`
- `blueprint/contracts/D1_EXTREME_TPW_LIFECYCLE_CONTRACT.md`
- `blueprint/contracts/M17_ENTRY_SLTP_CONTRACT.md`
- `blueprint/source/BBMA_EA.mq4`

## Final classification

ISSUE: Mode 2 cannot safely admit standalone Extreme yet because the exact protective SL mapping is not deterministic under strict source-only authority.

IMPACT: adding `SIGNAL_EXTREME` directly to M15 would create an entry family that M17 cannot resolve with provenance-correct SL ownership without either failing closed or inventing policy.

FIX: keep #175 at a bounded decision gate. Entry maturity and TP semantics are resolved; obtain explicit approval for an Extreme-specific project execution/EA-safety SL mapping before any M15/M16/M17 code patch.

No EA source, Strategy Core rule, behavior-bearing contract, runtime artifact or release authority is changed by this audit.
