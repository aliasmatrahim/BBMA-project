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
Status: PARTIAL / NEED-PRIMARY-VIDEO.
Forum/community evidence uses RME as Re-Entry -> MHV -> Extreme, but no primary project PDF/Finale contract has been found. Do not treat as canonical until direct Oma Ally evidence appears in the Intensive set or another stronger source.

## Gap 3 — ZZL / Zone Zero Loss
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE DEFINITION, NOT CORE.
Across community notes, indicators, and later analyzer implementations, the consistent semantic core is: an established trend/Re-Entry context in which MA5/10, Mid BB, and EMA50 are ordered in the trend direction and price remains on the valid trend side. Modern scanner logic expresses the same directional ordering. Exact entry/exit/invalidation details vary by implementation, so only the structural definition is considered research-closed.
Evidence: https://www.mql5.com/en/code/55233 ; https://www.scribd.com/document/980644232/BBMA-OA-3-3 ; https://www.scribd.com/document/1003442568/Rule-BBMA-Oma-Ally-Original

## Gap 4 — RZZL / Re-Entry in ZZL
Status: PARTIAL / TOOLING TAXONOMY.
Modern SharpShooter scanner versions explicitly scan Reentry in ZZL as a higher-timeframe component of Diamond, but the term RZZL is not proven as original Oma Ally taxonomy. Keep as tooling/community shorthand until stronger provenance is found.
Evidence: https://www.mql5.com/en/market/product/102503/updates

## Gap 5 — Rejected EMA50
Status: CLOSED-FOR-RESEARCH / STRONG-CANDIDATE STRUCTURE, NOT CORE.
Repeated teaching material gives a consistent directional form: in a higher-TF Re-Entry context, EMA50 sits on the structurally correct side of Mid BB and a candle rejects EMA50. This is sufficiently stable as a candidate definition. Exact wick/body/close Boolean remains implementation-unsafe without primary video confirmation.
Evidence: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY

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
Multiple independent BBMA notes describe continuous two/three Extreme structures without an opposite Extreme. They also state that second/third Extreme may not follow normal TP-Wajib/MHV when a larger timeframe MHV or Re-Entry owns the move. This is plausible and repeatedly documented, but conflicts with the conservative executable Core rule; therefore it remains excluded until primary video evidence yields deterministic ownership conditions.
Evidence: https://id.scribd.com/document/352183859/Bbma-Oma-Ally ; https://id.scribd.com/document/734529476/BBMA-Basic-OA

## Gap 9 — Re-Entry maturity / first-validating then following candle
Status: SOURCE-SEMANTICS CLOSED; RUNTIME TRACE STILL REQUIRED.
ForexFactory BBMA notes, TradingView open-source documentation, and independent teaching copies repeatedly state that the first candle validates Re-Entry and the next/second candle is used for entry. This matches the project resolution: validation from a fully closed source-TF candle, then execution may occur during the immediately following live candle. No additional full-candle delay is justified.
Evidence: https://www.forexfactory.com/thread/1123713-bbma-trading?page=38 ; https://my.tradingview.com/script/azoFriT7-Bollinger-Bands-Moving-Average-BBMA-Oma-Ally/ ; https://www.scribd.com/document/670542296/BBMA-OA-MyEnglishVersion1-1

## Gap 10 — Re-Entry minimum-candle rule
Status: PARTIAL.
Community/teaching material repeatedly gives minimum 3 candles for H4/H1/M15 and usually 2 for D1/W1/MN when MA5/10 and Mid BB meet. Project Core currently accepts the three-candle requirement for Powerful Re-Entry/Type 2 only. The broader TF-dependent generalization must not be promoted without higher-precedence evidence.
Evidence: https://www.forexfactory.com/thread/1123713-bbma-trading?page=38 ; https://www.scribd.com/document/670542296/BBMA-OA-MyEnglishVersion1-1

## Gap 11 — SL / cut-loss lifecycle
Status: NEED-PRIMARY-VIDEO; UNIVERSAL FORMULA NOT CLOSED.
No single stable Oma Ally universal SL formula emerges. Community evidence conflicts among opposite momentum, opposite CSAK, MA10/allowance, swing high/low, BB boundary, and fixed/ADR/product rules. The only robust semantic candidate is state invalidation: exit/cut when the setup is structurally invalidated by a strong opposite signal or invalidating close. This is not yet sufficient to replace project SL with one universal source-owned formula.
Evidence examples: https://www.youtube.com/watch?v=6iPBeLEQQns ; https://soehoe.id/threads/belajar-bareng-bbma-oma-ally.7063/page-3 ; https://id.scribd.com/document/492149103/bbma-oa

## Intensive Video 02 preliminary evidence
Uncorrected ASR chunks now exist for Video 02. Keyword sweep already finds: repeated higher-timeframe Re-Entry ownership language, lower-TF recurrence, explicit cut-loss discussion, and several ASR hits for 'gap'. Because this transcript is still uncorrected and incomplete as an assembled artifact, these hits are discovery leads only, not accepted evidence.

## What is now research-closed
- RRM semantic expansion: Re-Entry -> Re-Entry -> MHV (candidate only).
- ZZL structural meaning (candidate only).
- Rejected EMA50 structural meaning (candidate only).
- Gap BB-to-EMA50 structural meaning (candidate only).
- Diamond classified as evolving advanced/tooling family rather than stable Core.
- Re-Entry first-validating/following-candle semantics.

## What remains genuinely open
1. RME provenance and exact timeframe signature.
2. RZZL provenance as original vs tooling shorthand.
3. Deterministic advanced/multiple-Extreme owner transfer and no-TPW exceptions.
4. Exact candle Boolean/invalidation for Rejected EMA50 and Gap.
5. Universal source-owned SL/cut-loss lifecycle, if one exists.
6. Whether the 2-vs-3 candle rule is universal or only a subset/Powerful Re-Entry teaching.

## Next closure source
The remaining gaps should now be closed primarily from corrected Intensive Video transcripts, not additional broad web research. Search terms: RME, RRM, ZZL/zero loss, RZZL, EMA50, reject, gap, diamond, extreme kedua/ketiga, triple extreme, tiada TP wajib, tiada MHV, candle kedua, stop loss, cut loss, invalid/batal, timeframe besar, overshoot.
