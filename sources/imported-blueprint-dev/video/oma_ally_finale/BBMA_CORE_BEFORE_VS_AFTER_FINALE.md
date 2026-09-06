# BBMA Strategy Core — Before vs After BBMA Finale

## Scope
This comparison is **BBMA Strategy Core only**. It excludes money management, portfolio protection, trade lock, scheduler, dashboard, logging, broker handling, execution plumbing and other EA-management functions.

“BEFORE” = the current project Core already derived from the supplied PDFs and locked source contracts.

“AFTER” = that same Core after adding BBMA Finale V01–V07 as supplemental instructional/clarification evidence.

Important: this table compares **Core knowledge**, not merely the current code. Active-code mismatches are separated into `BBMA_FINALE_CORE_IMPLEMENTATION_GAP_REGISTER.md`.

## Comparison

| Core component | BEFORE Finale | AFTER Finale evidence | Assessment | Final decision |
|---|---|---|---|---|
| BBMA cycle | Extreme → TP → MLV/MHV → direction → Re-Entry → CSM → further Re-Entry → opposite Extreme | Same sequence, repeatedly demonstrated | **KEEP** | No Core change |
| Momentum / BB state | Current M10 contract already requires outside-BB close + expanding/directional BB; horizontal BB is not directional momentum | Finale explicitly repeats expanding vs flat BB and says flat-BB outside close is not momentum | **KEEP / STRONG CORROBORATION** | No Core change |
| Extreme signal | Relevant MA5/10 outside outer BB; Extreme is a signal; outside close/CSM voids context | Same framework, demonstrated in more detail | **KEEP / CLARIFY** | Keep current normal rule |
| Extreme reversal/retest | Current M08 contract already records reversal confirmation and retest candle as point of entry, but standalone lifecycle is intentionally not executable because universal deterministic patterning was not locked | Finale states condition 1 alone is insufficient; reversal + retest required; retest may span multiple candles | **CLARIFY / STRENGTHEN** | Preserve standalone withholding until exceptions are resolved |
| Extreme reversal close | Existing baseline favors/uses inside-BB confirmation semantics | Finale says inside BB is preferable, but also describes a case outside BB yet inside MA5 | **CONFLICT** | HOLD |
| Extreme MA location | Current strict rule requires relevant MA outside outer BB | Finale says touch-only may sometimes qualify, while outside is better | **CONFLICT** | HOLD; keep stricter rule |
| Normal Extreme TP Wajib | Existing digest: mandatory movement toward MA5/10 or Mid BB | Finale makes opposite MA5/MA10 High/Low the explicit mandatory first area, with Mid BB farther/max context | **CLARIFY** | Adopt as normal Extreme interpretation; currently dormant because standalone Extreme is non-executable |
| Advanced Extreme without normal TP Wajib | Not deterministically defined | Mentioned in advanced/MTF contexts | **UNCERTAIN** | HOLD |
| MHV/MLV terminology | Primary summary says MLV; historical reference uses MHV | Finale repeatedly says MHV = Market Hilang Volume | **TERMINOLOGY** | Treat as aliases pending deliberate naming standardization |
| MHV/MLV validity | Existing Core already says after Extreme; outside relevant BB close voids; mark body for retest; double/triple morphology supported | Same, with richer retest and H&S-like examples | **KEEP / CLARIFY** | No fundamental Core change; active M09 needs audit |
| eCSD / early direction | Cross relevant MA5/10 pair; weaker/earlier direction signal | Finale explicitly describes early direction before Mid BB | **KEEP / CLARIFY** | No Core change |
| CSD / strong direction | Cross relevant MA5/10 + Mid BB; stronger direction intent | Finale explicitly labels this strong direction | **KEEP / CLARIFY** | No Core change |
| Direction-signal execution | Raw eCSD/CSD are non-executable; Re-Entry follows retracement | Finale explicitly says do not enter on candle direction; wait Re-Entry | **KEEP** | No Core change |
| Re-Entry role | Four source-defined types; actual entry/setup occurs around relevant MA support/resistance/retracement | Same, repeatedly demonstrated | **KEEP / CLARIFY** | No Core change |
| Re-Entry MA5/MA10 close-side validity | Current M12 confirmation already requires BUY close on/above MA5/10 Low cluster and SELL close on/below MA5/10 High cluster | Finale says candle may penetrate MA5 but should not close through/clear both MA5 and MA10 | **KEEP / CORROBORATION** | Verify all type paths, but no new blanket rule needed |
| Re-Entry first/second-candle wording | Current engine confirms only after a source candle closes and then executes from the later live market price; contract does not describe this as “first validates / second enters” | Finale repeatedly uses that phrase across TFs | **CLARIFY / VERIFY SEMANTICS** | Do not add an extra candle delay unless runtime/source mapping proves it is missing |
| Type 2 Powerful Re-Entry | MA5/10 + Mid BB confluence, strongest with MA50, minimum 3 candles | Same | **KEEP** | No Core change |
| MTF relationship | Existing PDFs/contracts already require multi-timeframe context and define REM/RRE/REE | Finale more clearly explains higher-TF Re-Entry being completed/read through lower-TF structures and warns against isolated interpretation of lower-TF opposite direction | **KEEP / CLARIFY** | Preserve exact contracts; improve explanatory spec only |
| REM exact signature | H4 RE + H1 Extreme + M15 MLV | Finale names REM but SRT chart-pointing is insufficient to redefine signature | **KEEP** | Keep PDF-derived signature |
| RRE exact signature | D1 RE + H4 RE + H1 Extreme | Same | **KEEP** | Keep PDF-derived signature |
| REE exact signature | D1 RE + H4 Extreme + H1 Extreme | Same | **KEEP** | Keep PDF-derived signature |
| Personal H4-only workflow | Not universal Core | V07 speaker personally selects H4 Re-Entry after strong H4 direction | **REJECT FROM CORE** | Research/workflow only |
| V07 early-direction win-rate statistic | Not Core | Approx. 33% result from one stated backtest sample | **REJECT FROM CORE** | Research note only |
| Personal stop/risk/lot rules | Outside Strategy Core | V07 personal MA10+allowance SL/risk sizing discussion | **REJECT FROM CORE** | Keep outside Core |

## What actually changes after Finale?
The answer is **less than initially expected** because the current project had already source-aligned several important rules from the PDFs.

### Genuine Core clarifications worth carrying forward
- Normal Extreme retest can span multiple candles; raw MA-outside condition is definitely not entry authority.
- Normal Extreme TP Wajib is more precisely described as the opposite MA5/MA10 area before treating Mid BB as the farther possibility.
- MHV/MLV retest/morphology teaching is richer.
- Higher-TF ownership of lower-TF signals is explained more explicitly.
- “First Re-Entry candle validates, second candle enters” is useful terminology, but must be mapped to the existing closed-candle execution semantics rather than blindly adding a delay.

### Rules Finale mainly confirms rather than changes
- Expanding BB is required for momentum; flat-BB outside close is not momentum.
- eCSD vs CSD distinction.
- Raw candle direction is not entry authority.
- Type 2 minimum three-candle confluence.
- Existing BBMA cycle.
- REM/RRE/REE family structure.

## HOLD — must not enter Core yet
- MA5 touch-only Extreme as equivalent to clearly outside-BB Extreme.
- Reversal candle outside BB but inside MA5 as a universal rule.
- Advanced/MTF Extreme without normal TP Wajib without deterministic classification.
- Any new REM/RRE/REE signature inferred only from SRT chart-pointing.

## REJECT — do not merge into universal Core
- Personal H4-only trading preference.
- Sample win-rate statistics.
- Personal risk %, leverage, lot sizing and psychology rules.
- Personal stop methodology unless separately established as universal source-owned BBMA Core.
- Qualitative certainty language as literal guarantees.

## Development consequence
Do **not** rewrite the EA simply because the Finale videos were added. The source comparison shows that much of the current Core is already aligned. The next useful action is a focused audit of places where the active implementation fails to express the Core that both the PDFs and Finale now support, especially M09 MHV/MLV. Those findings are isolated in the implementation gap register.
