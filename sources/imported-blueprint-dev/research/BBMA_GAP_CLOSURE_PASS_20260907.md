# BBMA Gap Closure Pass — 2026-09-07

Status: RESEARCH / EVIDENCE ONLY. No EA, blueprint execution rule, or accepted Strategy-Core modification.

## Purpose
Continue research only on gaps that remain unresolved after prior extra-deep and forum passes. Classify each gap as CLOSED-FOR-RESEARCH, PARTIAL, or NEED-PRIMARY-VIDEO.

## Source precedence
Primary project PDFs > Finale V01-V07 > Tier-B Home Course > Intensive video transcripts > community/forum/web material. Community/dashboard material never overrides higher-precedence evidence.

## Gap 1 — RRM
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE, NOT CORE.
Repeated BBMA teaching material defines RRM as Re-Entry -> Re-Entry -> MHV. Signal Identification BBMA Oma Ally also places it in the same MTF taxonomy as REE/RRE/REM. No accepted project primary source currently contains RRM, so it remains a candidate taxonomy only.
Evidence: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY

## Gap 2 — RME
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE, NOT CORE.
Multiple community/teaching sources now agree on RME = Re-Entry -> MHV -> Extreme across three successive MTF layers. ForexFactory gives a concrete example: M15 Re-Entry, M5 MHV, M1 Extreme. A separate BBMA 101 note gives Weekly Re-Entry, Daily MHV, H4 Extreme and describes confirmation chronology. Therefore the semantic signature is research-closed, but provenance is still below accepted primary project evidence.
Evidence: https://www.forexfactory.com/thread/post/14090568 ; https://www.studocu.com/row/document/university-of-the-punjab/business-finance/bbma-notes-bbma-101-forex-trading-strategies-by-ashi-q/160767949

## Gap 3 — ZZL / Zone Zero Loss
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE DEFINITION, NOT CORE.
Across community notes, indicators, later analyzer implementations, and a detailed BBMA teaching copy, the stable semantic core is: Re-Entry-only context after strong direction, with Mid BB, MA5/MA10, candle/price and EMA50 ordered consistently on the trend side. The same teaching copy states TP/exit when a strong opposite direction candle appears. Exact automation Boolean remains non-canonical.
Evidence: https://www.mql5.com/en/code/55233 ; https://www.scribd.com/document/980644232/BBMA-OA-3-3 ; https://www.scribd.com/document/670542296/BBMA-OA-MyEnglishVersion1-1

## Gap 4 — RZZL / Re-Entry in ZZL
Status: CLOSED-FOR-RESEARCH AS TOOLING/ADVANCED TAXONOMY; NOT CORE.
SharpShooter documentation explicitly defines RZZL as Re-Entry in ZZL condition: a Re-Entry exists while the current timeframe is in Zone Zero Loss condition. Later scanner versions reuse Re-Entry-in-ZZL as the major-TF component of Diamond. This closes the semantic meaning, but does not establish RZZL as original Oma Ally taxonomy.
Evidence: https://pt.scribd.com/document/715250853/BBMA-OMA-ALLY-ANALYZER-DASHBOARD-EA-V3-60-Bahasa-Indonesia ; https://www.mql5.com/en/market/product/102503/updates

## Gap 5 — Rejected EMA50
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE STRUCTURE, NOT CORE.
Repeated teaching material gives a consistent directional form: in a higher-TF Re-Entry context, EMA50 sits on the structurally correct side of Mid BB and a candle rejects EMA50. Additional advanced notes indicate a candle closing beyond EMA50 can invalidate certain EMA50-rejection/advanced setups, but this is not stable enough to encode universally. Exact wick/body/close Boolean remains implementation-unsafe without primary video confirmation.
Evidence: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY ; https://www.scribd.com/document/866338054/bbma-somesetup

## Gap 6 — Gap BB to EMA50
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE STRUCTURE, NOT CORE.
Repeated teaching material defines the structural case as EMA50 outside the relevant outer BB while higher timeframe is in Re-Entry context, with a rejection from the relevant outer BB. Exact gap distance, rejection candle Boolean, and invalidation are not source-closed.
Evidence: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY

## Gap 7 — Diamond Setup
Status: CLOSED-FOR-RESEARCH AS LATER ADVANCED/TOOLING FAMILY; DO NOT PROMOTE TO CORE.
Diamond definitions change materially across analyzer versions: older versions use ZZL -> Rejected EMA50 -> MHV; later versions use ZZL -> Rejected EMA50 -> Re-Entry; latest scanner permits TF3 Extreme/MHV/Re-Entry. This evolution strongly indicates a later advanced/tooling taxonomy rather than a stable original Core contract.
Evidence: https://www.scribd.com/document/815678196/BBMA-OMA-ALLY-ANALYZER-DASHBOARD-EA-V3-50-English ; https://www.scribd.com/document/1071140576/Bbma-Oma-Ally-Analyzer-Dashboard-Ea-v3-60-english ; https://www.mql5.com/en/market/product/102503/updates

## Gap 8 — Advanced / multiple / triple Extreme
Status: PARTIAL / STRONG ADVANCED TEACHING, NEED-PRIMARY-VIDEO FOR EXECUTION.
Multiple independent BBMA notes describe continuous two/three Extreme structures without an opposite Extreme. They state that repeated small-TF Extremes can be the manifestation of a larger-TF MHV/Re-Entry owner, and that later Extremes may not require the normal TP-Wajib/MHV sequence. This is repeatedly documented but conflicts with the conservative executable Core rule; deterministic owner-transfer conditions still require primary video evidence.
Evidence: https://id.scribd.com/document/352183859/Bbma-Oma-Ally ; https://id.scribd.com/document/734529476/BBMA-Basic-OA ; https://www.slideshare.net/slideshow/bbma-new-ver-ms-enjvhjsdbvhjsdbvhjsdbvjhsdbvhjsdb-pdf/272193415

## Gap 9 — Re-Entry maturity / first-validating then following candle
Status: SOURCE-SEMANTICS CLOSED; RUNTIME TRACE STILL REQUIRED.
ForexFactory BBMA notes, TradingView open-source documentation, and independent teaching copies repeatedly state that the first candle validates Re-Entry and the next/second candle is used for entry. This matches the project resolution: validation from a fully closed source-TF candle, then execution may occur during the immediately following live candle. No additional full-candle delay is justified.
Evidence: https://www.forexfactory.com/thread/1123713-bbma-trading?page=38 ; https://my.tradingview.com/script/azoFriT7-Bollinger-Bands-Moving-Average-BBMA-Oma-Ally/ ; https://www.scribd.com/document/670542296/BBMA-OA-MyEnglishVersion1-1

## Gap 10 — Re-Entry minimum-candle rule
Status: CLOSED-FOR-RESEARCH AS TEACHING RULE; CORE SCOPE STILL LIMITED.
Independent teaching copies and ForexFactory repeatedly agree: when MA5/MA10 and Mid BB meet in a strong Re-Entry, small TFs H4/H1/M15 commonly use minimum 3 candles; D1/W1/MN commonly use minimum 2 candles. This closes the research taxonomy. Project Core should still keep its current narrower Type-2 application until higher-precedence reconciliation explicitly broadens it.
Evidence: https://www.forexfactory.com/thread/post/14075760 ; https://www.scribd.com/document/670542296/BBMA-OA-MyEnglishVersion1-1

## Gap 11 — SL / cut-loss lifecycle
Status: PARTIAL / NEED-PRIMARY-VIDEO FOR UNIVERSAL CONTRACT.
No single stable fixed-price Oma Ally SL formula emerges. However, research now converges on a lifecycle principle: exit/cut when the setup is structurally invalidated by a strong opposite direction/momentum signal or a close through the defining invalidation structure. Examples include opposite CSAK/momentum, a marked lower-TF line being closed through, and certain EMA50-rejection setups being invalidated by a close beyond EMA50. Fixed-pip, ADR, swing, MA10+allowance and dashboard SL rules remain implementation/personal variants. This supports lifecycle-based invalidation research, but is not enough for one universal deterministic Core SL formula.
Evidence: https://www.youtube.com/watch?v=6iPBeLEQQns ; https://soehoe.id/threads/belajar-bareng-bbma-oma-ally.7063/page-3 ; https://www.scribd.com/document/866338054/bbma-somesetup ; https://id.scribd.com/document/492149103/bbma-oa

## Intensive Video 02 preliminary evidence
Uncorrected ASR chunks now exist for Video 02. Keyword sweep already finds repeated higher-timeframe Re-Entry ownership language, lower-TF recurrence, explicit cut-loss discussion, and several ASR hits for 'gap'. Because this transcript is still uncorrected and incomplete as an assembled artifact, these hits are discovery leads only, not accepted evidence.

## What is now research-closed
- RRM = Re-Entry -> Re-Entry -> MHV (candidate taxonomy).
- RME = Re-Entry -> MHV -> Extreme (candidate taxonomy across successive TFs).
- ZZL structural meaning.
- RZZL semantic meaning as Re-Entry in ZZL.
- Rejected EMA50 structural meaning.
- Gap BB-to-EMA50 structural meaning.
- Diamond classified as evolving advanced/tooling family rather than stable Core.
- Re-Entry first-validating/following-candle semantics.
- 3-candle small-TF / 2-candle major-TF teaching taxonomy for strong confluence Re-Entry.

## What remains genuinely open
1. Deterministic advanced/multiple-Extreme owner transfer and no-TPW exceptions.
2. Exact universal candle Boolean/invalidation for Rejected EMA50 and Gap.
3. Universal source-owned SL/cut-loss contract, if one exists beyond lifecycle invalidation.
4. Whether any of RRM/RME/RZZL should ever be promoted from advanced/community taxonomy into accepted project Core.

## Next closure source
The remaining gaps should now be closed primarily from corrected Intensive Video transcripts, not additional broad web research. Search terms: RME, RRM, ZZL/zero loss, RZZL, EMA50, reject, gap, diamond, extreme kedua/ketiga, triple extreme, tiada TP wajib, tiada MHV, candle kedua, stop loss, cut loss, invalid/batal, timeframe besar, overshoot.
