# P3-SRC — BBMA Source Uncertainty Resolution Audit

Status: **SOURCE-GOVERNANCE PASS — NO EA CODE CHANGE REQUIRED BY THIS AUDIT**
Date: 2026-08-22
Branch target: `blueprint-dev`

## Purpose
Resolve the remaining BBMA Strategy-Core uncertainty items without inventing new trading rules. This audit reconciles the primary PDF-derived Core, BBMA Finale V01–V07 extracted rules, the existing project decisions/contracts, and corroborating forum material. Forum material is supporting evidence only and cannot silently override the primary PDF/Core hierarchy.

## Source hierarchy used
1. `Oma ally BBMA - AL.pdf` / page-indexed project digest — primary operational reference.
2. `BBMA technique.pdf` — secondary/historical corroboration.
3. `BBMA Finale V01–V07` — supplemental clarification evidence.
4. Existing approved project decisions/contracts — deterministic implementation mapping of accepted Core.
5. ForexFactory/community material — corroborating evidence only; not sufficient by itself to weaken the primary Core.

## Resolution summary

### CF-02 — Extreme MA touch vs outside
**Previous:** HOLD / CONFLICT.

**Evidence:**
- Primary Core requires the relevant MA5 or MA5/MA10 to be outside the appropriate outer BB for RAW Extreme.
- Finale V04 states MA5 outside the outer BB as criterion 1 with very high confidence.
- Finale V05 says touch-only may sometimes be treated as Extreme, but explicitly presents outside as the better form.
- Corroborating forum descriptions of Oma Ally-style Extreme consistently use MA5/MA10 outside BB and reversal confirmation.

**Resolution:** **CLOSED — STRICT OUTSIDE-BB RULE REMAINS AUTHORITATIVE.**

The touch-only statement is retained as instructional/edge-case evidence but is **not promoted into universal Core**. It cannot create RAW Extreme in the executable project contract. No code relaxation is justified.

Reason: supplemental evidence is insufficient to weaken the explicit established strict condition, and the project source hierarchy already requires the stricter rule to remain when evidence conflicts.

### CF-03 — Extreme reversal candle position
**Previous:** HOLD / CONFLICT.

**Evidence:**
- Finale V04 describes reversal close inside BB as **preferable**, not an unconditional hard requirement.
- Finale V05 gives a nuanced case where a reversal candle can remain outside BB but close inside the relevant MA5; it distinguishes this from continued momentum beyond MA5.
- Primary PDF digest requires reversal-candle behaviour and separately governs Extreme invalidation; it does not provide a sufficiently precise universal Boolean `CloseInsideBB` formula.
- Existing approved F2 deterministic lifecycle intentionally does **not** impose a universal close-back-inside-BB requirement and gives source-valid outside-BB/Momentum invalidation higher priority.

**Resolution:** **CLOSED — NO UNIVERSAL `CLOSE INSIDE BB` GATE, AND NO UNIVERSAL OUTSIDE-BB EXCEPTION.**

Authoritative project interpretation:
- reversal confirmation remains a reversal-direction closed-candle event under the approved F2 lifecycle;
- `inside BB` is preferred/confirmatory teaching context, not a mandatory universal Boolean gate;
- an outside-BB candle is not automatically accepted merely because it is inside MA5;
- source-valid Momentum/CSM / accepted outside-BB invalidation still overrides and voids the Extreme lifecycle;
- no new detector exception is added from the V05 edge case alone.

This resolves the coding ambiguity by refusing both unsupported extremes: neither `must always close inside BB` nor `outside BB + inside MA5 is always valid` becomes Core.

### CF-04 — Advanced / MTF Extreme without normal TP Wajib
**Previous:** HOLD / UNDERDEFINED.

**Evidence:**
- Normal Extreme TP Wajib is strongly supported by the PDF/Core and Finale V04/V05: opposite MA5/MA10 area first, with Mid BB as farther context.
- Finale mentions advanced/MTF Extreme situations without the normal TP-Wajib behaviour but does not provide a deterministic classifier sufficient for universal coding.
- Forum material shows MTF/advanced interpretations vary and does not provide stronger source authority than the primary Core.

**Resolution:** **CLOSED FOR EXECUTABLE CORE — ADVANCED NO-TP EXCEPTION EXCLUDED UNTIL DETERMINISTIC PRIMARY-SOURCE CLASSIFICATION EXISTS.**

The project does not assert that such advanced cases never exist. It asserts that they are not source-defined precisely enough to be an executable universal exception. Therefore:
- normal Extreme retains normal TP Wajib;
- canonical MHV/MLV parent provenance continues to require normal TP-Wajib structural completion;
- no advanced/MTF no-TP bypass may be used by M08/M09/M13/M14/M15/M17 unless a future stronger source resolves the classification.

### CF-05 — Re-Entry first validation candle / second entry candle
**Previous:** CLARIFY / VERIFY SEMANTICS.

**Existing resolution confirmed:** **CLOSED AT STATIC SEMANTIC LEVEL; RUNTIME TRACE STILL REQUIRED.**

`CORE-V2-F6` already maps the closed Re-Entry candle as the validation candle and permits execution during the immediately following live source-TF candle. No extra full-candle delay is added. This matches Finale teaching and corroborating Oma Ally SSS notes. Runtime evidence remains necessary only to verify actual order timing, not to redefine the source rule.

## Items not changed
- CF-01 MHV/MLV remains a terminology alias decision.
- CF-06 is corroboration, not a conflict.
- CF-07 exact REM/RRE/REE signatures remain PDF-derived; Finale chart pointing does not override them.
- CF-08/09/10/11 remain excluded from universal Core as personal/research/qualitative material.

## Strategy/code consequence
This audit produces **no immediate `.mq4` strategy patch**.

Reason:
- CF-02 confirms the existing strict RAW Extreme boundary.
- CF-03 confirms the already-approved F2 philosophy: no universal close-inside-BB gate and no blanket V05 exception.
- CF-04 explicitly keeps the advanced no-TP case outside executable Core.
- CF-05 is already statically mapped by F6.

Any future code change must be based on a separately proven implementation mismatch against these resolved rules, not on the existence of the old conflict labels.

## Confidence after resolution
- Executable Strategy-Core source governance for CF-02/03/04: **HIGH**.
- Historical/advanced BBMA teaching completeness: **not claimed 100%**; ambiguous advanced exceptions are intentionally excluded rather than invented.

## Next action
Proceed with the remaining runtime evidence gates already recorded in `MASTER_QUEUE.md`, especially:
1. P3-M1 runtime Mode 1 trace;
2. F1/F2/F3/F4/F5/F6 focused runtime traces as applicable;
3. opposite-direction same-pair runtime verification;
4. P3 Step 5 runtime closure.

Do not reopen CF-02/03/04 unless materially stronger primary-source evidence is added to the repository.
