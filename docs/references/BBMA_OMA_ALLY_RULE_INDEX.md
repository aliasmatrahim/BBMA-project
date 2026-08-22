# BBMA Oma Ally - Page-Indexed Rule Digest

## Status
Supporting digest derived from the user-supplied `Oma ally BBMA - AL.pdf`, now cross-referenced with the accepted BBMA Finale V01–V07 clarification layer.

This file is **not a replacement for the PDF**. It exists to make blueprint audits traceable by page. If this digest and the PDF ever disagree, the PDF takes precedence and the digest must be corrected.

The consolidated authoritative project Strategy-Core specification is:

`docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`

Finale statements classified `HOLD`, `UNCERTAIN` or `REJECT FROM CORE` are not promoted into the authoritative Core.

## Page 1 - Indicator contract
- BBMA uses Moving Averages and Bollinger Bands.
- MA set: MA5 High, MA10 High, MA5 Low, MA10 Low, EMA50.
- Bollinger Band: period 20, deviation 2, shift 0, applied to Close.
- MA50 is used as an important trend/support-resistance reference.

## Page 2 - BBMA cycle
Operational sequence described by the reference:
1. Extreme forms.
2. Price moves toward MA5/MA10 or Mid BB for mandatory profit taking after an Extreme entry.
3. MLV structure forms and highest/lowest body is marked for possible retest.
4. Price indicates direction through eCSD/CSD behaviour, with CSD crossing MA5/10 and Mid BB.
5. Price retraces toward MA5 and a Re-Entry may be taken.
6. Price continues with CSM/momentum candles; additional Re-Entry opportunities may occur on retracement.
7. An opposite Extreme can mark cycle restart/reversal.

## Pages 5-6 - Extreme
- Extreme is a signal; MLV is a setup.
- An isolated Extreme does not by itself establish a trend reversal.
- Extreme is associated with MA5 or MA5/10 outside the relevant BB and reversal-candle behaviour.
- Extreme becomes void if candlesticks close outside the relevant Top/Low BB.
- Presence of CSM invalidates the Extreme context described by the reference.
- The reference describes four Extreme categories.

## Pages 7-8 - MLV and direction confirmation
- MLV normally forms after an Extreme.
- MLV is invalid/void when price breaks and closes outside the relevant Top/Low BB.
- Highest/lowest body marking is used because price may retrace for a retest.
- MLV may resemble double/triple-top or double/triple-bottom structures.
- eCSD crosses MA5/10; CSD crosses MA5/10 and Mid BB.
- CSD provides stronger directional intent and retracement toward MA5/10 is associated with Re-Entry opportunity.

## Page 9 - Re-Entry Type 1
- Re-Entry forms after a rise/fall and sideways/ranging behaviour.
- Uptrend context: MA5/10 High acts as resistance; sell Re-Entry is considered when price finds MA5/10 High and candlesticks remain below it.
- Downtrend context: MA5/10 Low acts as support; buy Re-Entry is considered when price finds MA5/10 Low and candlesticks remain above it.

## Page 10 - Re-Entry Types 2-4
### Type 2 - Powerful Re-Entry
- MA5/10 and Mid BB meet/collide.
- Strongest form includes MA50 in the confluence/collision.
- Minimum duration stated: 3 candles per timeframe (for example H1 = 3 hours, H4 = 12 hours, D1 = 3 days).

### Type 3 - CSM Re-Entry
- CSM forms first.
- Price then reverses/retraces toward MA5 or MA50, indicating a Re-Entry setup.

### Type 4 - CSD Re-Entry
- CSD forms first.
- Price then gyrates/retraces toward MA5/10.
- Downtrend example: CSD finds MA5/10 Low for buy Re-Entry context.
- Uptrend example: CSD finds MA5/10 High for sell Re-Entry context.

### Multi-timeframe note
- The reference explicitly instructs checking multiple timeframes.
- MA50 on the Daily chart is highlighted for trend confirmation/continuation-vs-reversal context.

## Pages 12-13 - REM / RRE / REE
- REM, RRE and REE are multi-timeframe setups formed from three components on three timeframes.
- REM example: Re-Entry on H4 + Extreme on H1 + M15 MLV.
- REE example: Re-Entry on D1 + Extreme on H4 + Extreme on H1.
- RRE example: Re-Entry on D1 + Re-Entry on H4 + Extreme on H1.
- Re-Entry trend direction should be checked against higher timeframes.
- Intraday guidance uses H4, H1 and M15 alignment.

---

# Accepted BBMA Finale clarification supplement

This section does not rewrite the page-indexed PDF digest. It records only accepted post-Finale clarifications/corroborations that are carried into `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`.

## F-01 - Momentum / Bollinger Band state — KEEP / STRONG CORROBORATION
- Outside-BB close alone is not sufficient for directional Momentum/CSM.
- Expanding/directional BB state is required under the accepted Core interpretation.
- Flat/horizontal BB + outside close is not directional momentum.
- Evidence: V02 00:13:51–00:18:07; 00:24:44–00:26:18.

## F-02 - Normal Extreme retest lifecycle — CLARIFY
- Raw MA-outside condition alone is not standalone Extreme entry authority.
- Reversal confirmation and later retest remain part of the normal lifecycle.
- Finale clarifies that the retest can span multiple candles.
- Evidence: V04 00:27:23–00:31:55; 00:37:27–00:40:53; V05 00:07:05–00:08:22.

## F-03 - Normal Extreme TP Wajib — CLARIFY
- SELL Extreme: opposite MA5/MA10 Low area is the normal first TP-Wajib area.
- BUY Extreme: opposite MA5/MA10 High area is the normal first TP-Wajib area.
- Mid BB is farther/max context rather than replacing the opposite MA5/MA10 area as the normal first mandatory objective.
- Evidence: V04 00:41:02–00:42:42; V05 00:16:41–00:18:02.

## F-04 - MHV / MLV terminology and structure — KEEP / CLARIFY
- Finale repeatedly uses `MHV = Market Hilang Volume`; primary summary PDF uses `MLV`; historical PDF uses `MHV`.
- Project interpretation: treat MHV/MLV as terminology aliases for the same loss-of-volume setup family unless future evidence explicitly distinguishes them.
- Retest/body-marking and double/triple morphology are reinforced.
- H&S-like morphology is an example, not a compulsory Core condition.
- Evidence: V05 00:18:07–00:28:12; V01 00:59:18–01:00:05.

## F-05 - eCSD / CSD execution meaning — KEEP / STRONG CORROBORATION
- eCSD is the earlier/weaker direction signal associated with the relevant MA5/10 cross.
- CSD is stronger direction intent with relevant MA5/10 plus Mid-BB cross.
- Raw direction candle is not direct entry authority; wait for the applicable Re-Entry structure.
- Evidence: V05 00:28:41–00:36:51; V06 00:17:07–00:20:18.

## F-06 - Re-Entry close-side validity — KEEP / CORROBORATION
- MA5 is the principal retest area and MA10 confluence strengthens context.
- Finale says the Re-Entry candle may penetrate MA5 but should not close through/clear the relevant MA5/MA10 cluster against the setup.
- Existing project close-side validity remains authoritative; do not add a duplicate filter merely from this wording.
- Evidence: V05 00:37:25–00:41:16.

## F-07 - First validation candle / second entry candle — CLARIFY / VERIFY
- Finale repeatedly teaches that the first Re-Entry candle validates and the second candle is the entry candle.
- This is **not yet a new Core delay rule** because the closed-candle architecture may already validate after candle close and execute during the following candle.
- Runtime/source timing must be mapped before any implementation change.
- Evidence: V06 00:30:46–00:31:06; 00:52:48–00:56:27.

## F-08 - Higher-TF ownership/context — KEEP / CLARIFY
- Higher-timeframe Re-Entry may be completed/read through lower-timeframe signal/setup structures.
- An opposite-looking lower-TF direction signal must not automatically be treated as an independent reversal when it structurally belongs to the higher-TF Re-Entry context.
- Exact executable project signatures remain the approved D1/H4/H1/M15 contracts.
- Evidence: V05 00:34:48–00:36:37; 00:46:16–00:53:55; V06 00:26:57–00:29:02.

## F-09 - REM / RRE / REE — KEEP exact PDF signatures
- REM = H4 Re-Entry + H1 Extreme + M15 MLV/MHV.
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.
- Finale is corroborating context only; SRT chart-pointing is not sufficient to redefine the signatures.

---

# Excluded / unresolved Finale material

The following are **not** accepted into authoritative Strategy Core:
- MA5 touch-only Extreme equivalence — HOLD.
- Universal outside-BB-but-inside-MA5 reversal-candle acceptance — HOLD.
- Advanced/MTF Extreme without normal TP Wajib — HOLD.
- Additional full-candle delay inferred from “first validates / second enters” — VERIFY, not accepted as a new rule.
- Personal H4-only workflow — REJECT FROM CORE.
- Sample win-rate statistics — REJECT FROM CORE.
- Personal risk/leverage/lot-sizing/portfolio rules — REJECT FROM CORE.
- Personal MA10+allowance stop method as universal BBMA SL — REJECT/HOLD FROM CORE.
- Literal guarantees from pedagogical words such as “pasti” or “100%” — REJECT AS LITERAL RULE.

Authoritative conflict tracking:
`docs/references/video/oma_ally_finale/BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`

## Development rule
Type 2–4 and every executable Core path must remain reconciled against the source contracts above. No substitute confirmation rule, generic signal count or unsupported filter may be invented merely to fit the current code.
