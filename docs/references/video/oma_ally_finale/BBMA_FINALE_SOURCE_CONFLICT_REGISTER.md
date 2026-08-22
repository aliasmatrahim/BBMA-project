# BBMA Finale — Source Conflict / Hold Register

## Purpose
Record Finale statements that must **not** be silently merged into BBMA Strategy Core. `HOLD` means no detector/entry rule change until the source conflict or semantic ambiguity is explicitly resolved.

| ID | Topic | Existing baseline | Finale evidence | Status | Required handling |
|---|---|---|---|---|---|
| CF-01 | MHV vs MLV name | `Oma ally BBMA - AL.pdf` uses MLV; historical `BBMA technique.pdf` uses MHV | Finale repeatedly says MHV = Market Hilang Volume | **TERMINOLOGY** | Treat as semantic aliases; do not create two independent setup types from naming alone |
| CF-02 | Extreme MA touch vs outside | Current primary contract requires relevant MA5/10 outside outer BB | V05 00:11:37–00:12:14 says MA5 touching can sometimes count, while outside is better | **HOLD / CONFLICT** | Keep stricter outside-BB rule until visual/PDF/audio resolution |
| CF-03 | Extreme reversal candle position | Existing contract/source treatment favors an inside-BB reversal confirmation | V04 says inside BB is preferable; V05 describes a nuanced case outside BB but inside MA5 | **HOLD / CONFLICT** | Do not relax the current stricter rule until the exact acceptance boundary is resolved |
| CF-04 | Advanced Extreme without TP Wajib | Normal Core has mandatory profit-taking after Extreme | V04/V05 mention some advanced/MTF Extremes without the normal TP Wajib | **HOLD / UNDERDEFINED** | Keep normal TP Wajib; require deterministic advanced classification before any exception |
| CF-05 | Re-Entry first-candle validation / second-candle entry | Current M12 confirms from a fully closed source candle; execution occurs later from live broker price, but contract terminology does not call this “second candle entry” | V06 repeats first validates / second enters across multiple TFs | **CLARIFY / VERIFY SEMANTICS** | Do not add an extra candle delay automatically; compare source candle timestamps with actual execution timing first |
| CF-06 | Re-Entry MA5/MA10 close-side condition | Current M12 confirmation already requires BUY close on/above MA5/10 Low cluster and SELL close on/below MA5/10 High cluster | V05 says candle may penetrate MA5 but should not close through both MA5 and MA10 | **CORROBORATION, NOT CONFLICT** | Verify all Re-Entry type paths use the same valid close-side logic; do not invent a new duplicate filter |
| CF-07 | REM/RRE/REE visual mapping | Exact PDF signatures are already explicit | Finale names REM/RRE/REE but chart pointing is not reliably recoverable from SRT alone | **NO OVERRIDE** | Keep existing PDF signatures |
| CF-08 | V07 personal H4 workflow | Not a universal Core rule | Speaker personally selects H4 Re-Entry after strong H4 direction | **REJECT FROM CORE** | Keep only as personal workflow/research evidence |
| CF-09 | V07 ~33% early-direction result | No universal win-rate number belongs to Core | One stated backtest sample | **REJECT FROM CORE** | Research note only; do not create a strategy threshold from it |
| CF-10 | V07 MA10+allowance stop | Universal source-owned SL is not established by this personal statement | Speaker says “Saya menggunakan MA10...” plus allowance | **REJECT/HOLD FROM CORE** | Do not redefine the BBMA Core SL/TP contract from a personal risk-plan section |
| CF-11 | Qualitative certainty | No source-valid setup can be encoded as guaranteed | Phrases such as “entry yang pasti”, “100%”, “paling selamat” occur pedagogically | **REJECT AS LITERAL RULE** | Preserve as teaching emphasis only; never encode a guarantee |

## Resolution rule
A conflict is resolved only when the project explicitly decides it using the strongest available source context. Until then:
- an established Core rule remains in force;
- no subtitle-only exception silently weakens a stricter PDF-derived rule;
- no additional candle delay or setup condition is added merely because the natural-language teaching can be read that way;
- implementation gaps are tracked separately from source conflicts.
