# BBMA Strategy Core V2.x — Workbook Safe Clarifications

Status: ACTIVE CLARIFICATION LAYER — NON-EXECUTION-CHANGING
Date: 2026-08-25
Parent authority: `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
Evidence gate: `HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`

## Scope guard

This clarification layer records only Home Course Workbook findings that were cross-source reconciled as compatible with the authoritative Core V2. It does **not** create a new detector, entry path, exit rule, TP exception, timeframe-owner override, REM/RRE/REE signature, or lower-timeframe execution shortcut.

If wording here can be read more broadly than Core V2, Core V2 and its explicit execution/owner contracts win.

## V2.x-C1 — Mid-BB named zones

Descriptive vocabulary accepted from the Workbook:
- area from Mid BB toward Top BB = `Buying Zone`;
- area from Mid BB toward Low BB = `Selling Zone`.

Guard:
- zone membership is structural/context vocabulary only;
- being inside a named zone is **not** standalone entry authority;
- no existing Re-Entry, Extreme, MHV/MLV, Momentum or combination eligibility condition is weakened by this terminology.

## V2.x-C2 — Direction-strength hierarchy

The Workbook's weak-to-strong direction wording is reconciled with the existing Core hierarchy:
- `eCSD` = earlier/weaker direction indication associated with the relevant MA5/MA10 cross;
- `CSD` = stronger direction intent associated with relevant MA5/MA10 plus Mid-BB cross;
- MA50 may strengthen higher structural/trend context where source-valid.

Guard:
- raw eCSD/CSD remains context/direction evidence, not direct execution authority;
- this clarification does not create an additional strength score or threshold.

## V2.x-C3 — MA50 / D1 structural context

MA50 remains an important trend/support-resistance reference. Daily MA50 may be used as higher-timeframe context for continuation-versus-reversal interpretation, consistent with the primary PDF MTF note.

Guard:
- this does **not** mean universal `D1 overrides H4` execution precedence;
- existing project timeframe-owner contracts and exact approved signatures remain authoritative;
- no trade is accepted/rejected solely because a broad D1 directional statement disagrees with a lower owner timeframe unless the existing approved contract already requires that relationship.

## V2.x-C4 — Bounded nested-MTF interpretation

A higher-timeframe Re-Entry may be structurally completed/read through valid lower-timeframe BBMA signal/setup development. An apparently opposite lower-timeframe direction event may belong to the higher-timeframe Re-Entry context rather than automatically representing an independent trend reversal.

This is the accepted bounded meaning of `nested MTF` for Core V2.x.

Executable boundary remains unchanged:
- REM = `H4 Re-Entry + H1 Extreme + M15 MHV/MLV`;
- RRE = `D1 Re-Entry + H4 Re-Entry + H1 Extreme`;
- REE = `D1 Re-Entry + H4 Extreme + H1 Extreme`;
- approved D1/H4/H1/M15 owner and maturity contracts remain unchanged;
- lower-TF replay does not authorize unlimited recursive entries, arbitrary timeframe substitution or additional add-on trades.

## V2.x-C5 — Re-Entry duration corroboration

For the source-described Powerful Re-Entry, the minimum duration wording of three candles per source timeframe is corroborated by both Workbook and primary PDF digest (for example H1 = 3 hours, H4 = 12 hours, D1 = 3 days).

Guard:
- this clarification does not create an extra delay beyond the existing accepted Re-Entry lifecycle;
- first-validation/following-live-candle execution semantics remain governed by the existing Core/CF-05 resolution.

## Explicitly NOT promoted

The following Workbook findings remain outside authoritative executable Core pending strategy decision or stronger reconciliation:
- universal D1-over-H4 precedence;
- Double H1 Extreme -> H4 MHV deterministic inference;
- H4 MHV -> direct H1 Extreme execution shortcut;
- claim that valid H4 MHV prevents any further H1 MHV;
- universal hold/no-TP rule when direction reaches outer BB before Re-Entry;
- universal mandatory exit/reversal rule when Re-Entry is not followed by Momentum;
- detailed horizontal-BB wick/body reversion table as deterministic execution law;
- absolute 10–20 pip horizontal-BB breakout threshold;
- MA5 relationship as an independent Momentum validity tier;
- `Extrem Magic` as independent executable detector/authority;
- deterministic next-day prediction from today's D1 close.

## Implementation impact

`NONE` by design.

This file is documentation clarification only. No MQL4 implementation change is authorized by this patch. Any future code diff claiming this document as authority must demonstrate that it only improves interpretation/diagnostics or must pass an explicit strategy-decision gate before changing trading behavior.

## Provenance

Primary reconciliation sources:
- `BBMA_OMA_ALLY_RULE_INDEX.md` — primary PDF page digest + accepted Finale supplement;
- `video/oma_ally_finale/BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`;
- `HOME_COURSE_19P_ATOMIC_LEDGER_20260825.md`;
- `HOME_COURSE_19P_CANONICAL_ROW_MAP_20260825.md`;
- `HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`.
