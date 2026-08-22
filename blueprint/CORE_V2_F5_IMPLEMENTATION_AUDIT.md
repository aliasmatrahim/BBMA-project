# CORE-V2-F5 — M07 Flat/Horizontal Bollinger-Band State Repair

Date: 2026-08-22
Status: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**
Branch: `blueprint-dev`

## Scope
Repairs CV2-02 only: `BB_FLAT` was unreachable because every valid positive width ratio was already consumed by squeeze/expanding/contracting branches.

## Source rule preserved
The accepted Strategy Core says an outside-BB close under a flat/horizontal BB is not directional Momentum/CSM. The source does not provide a numeric flatness formula. F5 therefore implements only a minimal geometric state mapping and does **not** add a new trading filter.

## Deterministic mapping
- `BB_FLAT` is now a real geometric state: Top BB, Mid BB and Low BB must each remain horizontal versus the immediately previous closed source-TF candle within **one broker point**.
- One broker point is used only as numerical equality tolerance; it is not a pip/ATR/volatility threshold and does not become an entry rule.
- The existing project shape thresholds are otherwise preserved: width ratio `< 0.9` -> `BB_SQUEEZE`; `> 1.1` -> `BB_EXPANDING`; remaining non-flat valid states -> `BB_CONTRACTING`.
- Invalid/zero point or invalid BB geometry fails to `BB_NONE`.

## Important boundary
M10 `DetectCSM()` is intentionally unchanged. It already independently requires outside close + width expansion + directional BB movement. F5 repairs M07 state semantics so later modules can safely consume `BB_FLAT`; it does not claim that M07 is the current CSM authority.

## Static regression
- the old all-covering `0.9..1.1 -> BB_CONTRACTING` branch is removed;
- `BB_FLAT` is reachable before width-ratio classification;
- Top/Mid/Low horizontal checks are all required;
- M10 contains no newly introduced `BB_FLAT` gate;
- F1/F2/F3/F4 structural markers remain present;
- source lexical brace/parenthesis/bracket sanity passes.

## Evidence classification
- flat/horizontal BB distinction and its Momentum meaning: **DIRECT / STRONGLY CORROBORATED SOURCE PRINCIPLE**;
- exact one-broker-point three-line horizontal predicate: **MINIMAL PROJECT NUMERICAL MAPPING**, not a verbatim Oma Ally formula.

## Remaining verification
1. Native MetaEditor compile must report **0 errors / 0 warnings** for integrated F1-F5 source.
2. Runtime trace should show at least one `BB_FLAT` classification on genuinely horizontal closed BB geometry and confirm non-flat near-equal-width sloping BB is not mislabeled flat.
3. Proceed to CORE-V2-F6 timing verification before re-running the full Strategy Core audit.
