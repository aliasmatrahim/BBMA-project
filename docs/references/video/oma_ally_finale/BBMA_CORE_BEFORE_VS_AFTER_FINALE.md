# BBMA Strategy Core — Before vs After BBMA Finale

## Scope
This comparison is **Strategy Core only**. It intentionally excludes money management, portfolio protection, trade lock, scheduler, dashboard, logging, broker handling, execution plumbing and other EA-management features.

“Before” means the current project BBMA Core as documented by the existing PDF-derived rule index and locked entry-mode semantics. “After” means the **proposed source model after adding BBMA Finale V01–V07 evidence**, with unresolved conflicts still held rather than forced into Core.

## Comparison

| Core component | BEFORE Finale | AFTER adding Finale evidence | Assessment | Decision |
|---|---|---|---|---|
| BB state | Expand vs flat/ranging known, but not fully tied to every momentum decision | Outside-BB close counts as momentum only in expanding-BB context; flat-BB outside close is explicitly not momentum | **CLARIFY / CORRECT** | ACCEPT |
| BBMA cycle | Extreme → TP → MLV/MHV → direction → Re-Entry → CSM → Re-Entry → opposite Extreme | Same sequence, strongly repeated across multiple videos | **KEEP** | ACCEPT |
| Extreme raw signal | MA5/10 outside outer BB + reversal behavior; outside close invalidates | Same normal framework, but entry requires the full 3-stage chain: outer-BB MA condition → reversal → retest | **ADD / CORRECT** | ACCEPT normal lifecycle |
| Extreme entry timing | Standalone lifecycle not deterministically locked; therefore standalone Extreme not execution-eligible in current Mode 2 contract | Entry is at/after retest; retest can take multiple candles; first outer-BB condition alone is explicitly insufficient | **ADD** | ACCEPT for next Core spec; do not enable until reconciled |
| Extreme reversal close | Current implementation/reference favors reversal candle inside BB | Finale says inside BB is preferable, but V05 gives an exception where outside-BB reversal may still qualify if inside MA5 | **CONFLICT** | HOLD |
| Extreme MA location | Current rule requires relevant MA outside outer BB | V05 says touch-only can sometimes qualify, while outside is better | **CONFLICT** | HOLD; keep stricter current rule |
| Extreme TP Wajib | Current source says MA5/10 or Mid BB; implementations have sometimes simplified to Mid BB | Normal Extreme explicitly targets opposite MA5/MA10 High/Low as TP Wajib; Mid BB is farther/max context | **CLARIFY / CORRECT** | ACCEPT normal rule |
| Advanced Extreme TP exception | Not deterministically defined | Some advanced/MTF-context Extreme said to have no normal TP Wajib | **UNCERTAIN** | HOLD / do not generalize |
| MHV/MLV terminology | Primary summary uses MLV; other project material also uses MHV | Finale repeatedly uses MHV = Market Hilang Volume | **TERMINOLOGY** | Treat as alias pending deliberate standardization |
| MHV/MLV validity | After Extreme; valid if price fails to close outside outer BB; double/triple morphology | Same, plus explicit retest/marked-level behavior and broader visual examples including H&S-like structure | **KEEP / ADD** | ACCEPT retest clarification; morphology non-mandatory |
| eCSD / early direction | Crosses relevant MA5/10; direction signal | Explicitly “arah awal”: crosses MA5/10 but not Mid BB | **KEEP / CLARIFY** | ACCEPT |
| CSD / strong direction | Crosses MA5/10 + Mid BB; stronger direction intent | Explicitly “arah kukuh”: crosses MA5/10 + Mid BB | **KEEP / CLARIFY** | ACCEPT |
| Direction-signal execution | Raw eCSD/CSD non-executable in current entry contract | Finale explicitly says do not enter on candle direction; wait Re-Entry | **KEEP** | ACCEPT |
| Re-Entry role | Source-defined setup, four types; MA5/10/MidBB confluence rules | Reaffirmed as actual setup/entry zone after direction/momentum | **KEEP / CLARIFY** | ACCEPT |
| Re-Entry invalidation | Type contracts exist, but subtitle-derived “through both MA5+MA10” boundary not explicit in current master digest | Re-Entry may penetrate MA5 but should not close through/clear both MA5 and MA10 in the taught structure | **ADD / CORRECT** | ACCEPT candidate; reconcile per type/direction |
| Re-Entry candle timing | Current confirmed lifecycle does not encode a universal first-candle-validate / second-candle-entry rule | V06 repeatedly states first Re-Entry candle validates; second candle is point of entry, across TFs | **MAJOR ADD / CORRECT** | ACCEPT candidate for next Core specification |
| Type 2 Re-Entry | MA5/10 + Mid BB confluence; minimum 3 candles; strongest with MA50 | Same, directly corroborated | **KEEP** | ACCEPT |
| MTF context | D1/H4/H1/M15 roles and exact REM/RRE/REE contracts | Adds clear rule that higher-TF Re-Entry is completed/read via lower-TF structures; opposite lower-TF signals must be checked in higher-TF context | **CLARIFY / ADD** | ACCEPT |
| REM/RRE/REE exact signatures | REM H4 RE + H1 E + M15 MLV; RRE D1 RE + H4 RE + H1 E; REE D1 RE + H4 E + H1 E | Finale names the same families and general MTF logic, but subtitle-only evidence is insufficient to redefine exact signatures | **KEEP** | Keep current PDF-derived signatures |
| Personal H4-only workflow | Not a universal Core rule | V07 speaker personally selects H4 Re-Entry after strong H4 direction | **REJECT FROM CORE** | Research/workflow only |
| Win-rate/backtest numbers | Not Core | V07 33% early-direction result from one stated sample | **REJECT FROM CORE** | Research note only |
| Personal stop/risk/lot rules | Outside Strategy Core | V07 describes MA10+allowance stop and risk-based sizing personally | **REJECT FROM CORE** | Keep outside Core |

## Net Core change
The proposed post-Finale Core is **not a different strategy**. It is a more deterministic version of the same BBMA cycle. The biggest changes are precision at transition points:

1. **Momentum:** BB expansion state becomes part of the classification.
2. **Extreme:** standalone entry cannot occur until reversal + retest completes.
3. **Extreme TP:** normal TP Wajib is anchored first to opposite MA5/MA10, with Mid BB as farther context.
4. **MHV:** retest and inside-BB lifecycle become explicit.
5. **Direction:** early vs strong mapping is clearer and remains non-executable alone.
6. **Re-Entry:** explicit MA5/MA10 validity boundary and first-candle validation → second-candle entry timing.
7. **MTF:** higher-timeframe ownership/context is more explicit.

## What must NOT be changed yet
The following are held and must not be inserted into Core until resolved:
- MA5 touch-only Extreme as equivalent to outside-BB Extreme.
- Reverse candle outside BB but inside MA5 as a universal Extreme confirmation rule.
- Advanced Extreme “no TP Wajib” exception without deterministic classification.
- Any reinterpretation of REM/RRE/REE exact signatures based solely on ambiguous subtitle/chart-pointing.

## Development consequence
This document is a **source-analysis proposal**, not an instruction to edit the EA immediately. The next deliberate Core reconciliation should update the specification first, then audit affected detector/lifecycle modules, and only afterward change code. Runtime/debug work should remain separate.
