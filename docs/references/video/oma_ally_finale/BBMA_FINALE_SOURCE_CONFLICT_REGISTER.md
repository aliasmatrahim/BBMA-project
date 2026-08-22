# BBMA Finale — Source Conflict / Hold Register

## Purpose
Record statements that must **not** be silently merged into BBMA Strategy Core. `HOLD` means no detector/entry rule change until the source conflict is resolved explicitly.

| ID | Topic | Existing baseline | Finale evidence | Status | Required handling |
|---|---|---|---|---|---|
| CF-01 | MHV vs MLV name | `Oma ally BBMA - AL.pdf` uses MLV; historical `BBMA technique.pdf` uses MHV | Finale repeatedly says MHV = Market Hilang Volume | TERMINOLOGY | Treat as semantic alias; do not create two separate setups |
| CF-02 | Extreme MA touch vs outside | Current primary contract requires relevant MA5/10 outside outer BB | V05 00:11:37–00:12:14 says MA5 touching can sometimes count, while outside is best | **HOLD / CONFLICT** | Keep stricter outside-BB rule until visual/PDF/audio resolution |
| CF-03 | Extreme reverse candle position | Current project implementation/reference favors reversal close inside BB | V04 says inside BB “preferably”; V05 allows a nuanced case outside BB but inside MA5 | **HOLD / CONFLICT** | Do not relax hard rule yet; resolve exact acceptance boundary |
| CF-04 | Advanced Extreme without TP Wajib | Normal Core has mandatory profit-taking after Extreme | V04/V05 mention some advanced/MTF Extremes without normal TP Wajib | **HOLD / UNDERDEFINED** | Keep normal TP Wajib; require deterministic advanced classification before exception |
| CF-05 | Re-Entry second-candle timing | Current primary PDF digest does not state a universal 1st-validates/2nd-enters rule | V06 repeats this rule several times across multiple TFs | **VIDEO-ONLY ADDITION / HIGH CONFIDENCE** | Candidate for adoption after blueprint reconciliation; not a conflict, but a major new contract |
| CF-06 | Re-Entry MA5/MA10 invalidation | Current four-type contracts do not state the subtitle-derived boundary in this exact form | V05 says Re-Entry may pass MA5 but should not close through both MA5 and MA10 | **VIDEO-ONLY ADDITION** | Reconcile direction/type semantics before hard coding |
| CF-07 | REM/RRE/REE visual mapping | Exact PDF signatures are already explicit | Finale names REM/RRE/REE but chart pointing is not recoverable reliably from SRT alone | **NO OVERRIDE** | Keep existing PDF signatures |
| CF-08 | V07 personal H4 workflow / 33% statistic | Not universal Core | Personal selection and sample backtest | **REJECT FROM CORE** | Keep only as research/personal workflow evidence |
| CF-09 | V07 MA10+allowance stop | Strategy Core SL source not established by this personal statement alone | Speaker says “Saya menggunakan MA10...” plus allowance | **REJECT/HOLD FROM CORE** | Do not redefine source-owned SL from personal risk-plan section |
| CF-10 | Qualitative certainty | No setup is guaranteed | Phrases such as “entry yang pasti” appear pedagogically | **REJECT AS LITERAL RULE** | Preserve as teaching emphasis only, never encode a guarantee |

## Resolution rule
A conflict is resolved only when the project explicitly decides it using the strongest available source context. Until then, the current stable Core rule remains in force where one exists, and no hidden merge is allowed.
