# BBMA Gap-Closure Evidence Register — 2026-09-06

Status: RESEARCH / EVIDENCE REGISTER ONLY. No EA, executable Blueprint rule, or accepted Strategy-Core rule is modified by this file.

## Governance
Source precedence remains: primary project PDF -> secondary project PDF -> Finale V01-V07 -> authenticated Tier-B Home Course -> accepted derived Core. Forum, mirrored notes, dashboards, scanners and third-party documents are discovery/corroboration only unless explicitly reconciled against stronger project evidence.

## Gap 1 — RRM
Status: PARTIAL / STRONG TIER-C CORROBORATION; NOT YET CORE.
Evidence:
- Signal Identification BBMA Oma Ally: RRM = Reentry -> Reentry -> MHV; also lists REM/RRE/REE and multi-timeframe stacks W1-D1-H4, D1-H4-H1, H4-H1-M15, H1-M15-M5.
  Source: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY
- MQL5 BBMA Oma Ally Signals Scanner product page/update history also exposes RRM in its structure taxonomy.
  Source: https://www.mql5.com/en/market/product/102503
Assessment: repeated taxonomy, but no higher-precedence project-source definition. Keep as NEW-CANDIDATE until video/PDF corroboration.

## Gap 2 — RME
Status: PARTIAL / COMMUNITY CORROBORATION ONLY.
Evidence:
- ForexFactory forum pass recorded RME = Reentry -> MHV -> Extreme as recurring community shorthand.
  Project forum register: sources/imported-blueprint-dev/research/BBMA_FORUM_DEEP_RESEARCH_20260906.md
Assessment: exact canonical timeframe signature and official Oma Ally naming still unresolved. Do not encode.

## Gap 3 — ZZL / Zone Zero Loss
Status: PARTIAL / DEFINITION STRONGLY CONVERGING; NOT YET CORE.
Evidence:
- SOP Trading BBMA: ZZL BUY = MA5/10 High & Low above Mid BB, Mid BB above EMA50, price above EMA50; ZZL SELL = inverse structure.
  Source: https://www.scribd.com/document/636284986/SOP-Trading-BBMA-converted-1
- Basic BBMA and ZZL Setup mirrors the same directional MA/MidBB/EMA50 ordering and ties ZZL to Reentry-only context.
  Source: https://fliphtml5.com/xoxfq/sslv/Basic_BBMA_and_ZZL_Setup/
- BBMA FINAL 2nd Edition mirror repeats ZZL as a Reentry-only condition with MA5/10, Mid BB and EMA50 directional ordering.
  Source: https://www.scribd.com/document/616985765/BBMA-FINAL-2nd-Edition-ms-en-2
- BBMA OA Indicator v3.3 code uses deterministic ZZL logic consistent with EMA50 < MidBB < MA10/MA5 Low for BUY and inverse for SELL.
  Source: https://www.scribd.com/document/980644232/BBMA-OA-3-3
Assessment: conceptual definition is now strongly corroborated across independent Tier-C sources. Still missing authoritative lifecycle start/end, invalidation and whether all MA5/10 High+Low relationships are universally required. Wait for project video evidence before Core promotion.

## Gap 4 — Rejected EMA50
Status: PARTIAL / STRONG TIER-C CORROBORATION.
Evidence:
- Signal Identification BBMA Oma Ally: in higher-timeframe Reentry context, BUY-side rejected EMA50 has EMA50 below Mid BB plus candle reject EMA50; SELL-side is inverse.
  Source: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY
- SharpShooter Analyzer V3.5/V3.6 repeatedly uses Rejected EMA50 as the secondary-TF component of Conservative and Diamond setups.
  Sources: https://www.scribd.com/document/1071140576/Bbma-Oma-Ally-Analyzer-Dashboard-Ea-v3-60-english ; https://www.scribd.com/document/815678196/BBMA-OMA-ALLY-ANALYZER-DASHBOARD-EA-V3-50-English
Assessment: setup family is credible, but exact candle rejection Boolean (touch/wick/close/body/sequence) remains unresolved. Do not encode until direct project evidence.

## Gap 5 — Gap BB to EMA50
Status: PARTIAL / STRONG TIER-C CORROBORATION.
Evidence:
- Signal Identification BBMA Oma Ally defines Gap BB to EMA50 under higher-TF Reentry: BUY-side EMA50 below Lower BB with candle rejection of Lower BB; SELL-side inverse at Upper BB.
  Source: https://www.scribd.com/document/769713635/SIGNAL-IDENTIFICATION-BBMA-OMA-ALLY
- MQL5 Scanner refers to Rejected EMA50/GAP as a component in advanced scanning and Diamond logic.
  Source: https://www.mql5.com/en/market/product/102503
Assessment: named concept likely genuine within advanced BBMA ecosystem, but source authority and exact invalidation remain insufficient.

## Gap 6 — Diamond Setup
Status: PARTIAL / LIKELY LATER ADVANCED EXTENSION; NOT CORE.
Evidence:
- SharpShooter V3.5: Diamond = ZZL -> Rejection EMA50 -> MHV.
  Source: https://www.scribd.com/document/590733895/BBMA-OMA-ALLY-ANALYZER-DASHBOARD-EA-V3-50-Bahasa-Indonesia
- SharpShooter V3.6: Diamond = ZZL -> Rejected EMA50 -> Reentry.
  Source: https://www.scribd.com/document/1071140576/Bbma-Oma-Ally-Analyzer-Dashboard-Ea-v3-60-english
- MQL5 V4.80 changes Diamond to TF1 Reentry-in-ZZL, TF2 EMA50 + outer-BB rejection, TF3 Extreme/MHV/Reentry in same direction.
  Source: https://www.mql5.com/en/market/product/102503/updates
Assessment: the label is real and recurring, but its formal composition changes across versions. That instability is evidence it is implementation/tooling taxonomy rather than a stable accepted Oma Ally Core contract. KEEP OUT OF CORE unless direct higher-tier source says otherwise.

## Gap 7 — RZZL
Status: PARTIAL / TOOLING TAXONOMY.
Evidence:
- SharpShooter V3.6 defines RZZL as Reentry in ZZL condition on current TF.
  Source: https://pt.scribd.com/document/715250853/BBMA-OMA-ALLY-ANALYZER-DASHBOARD-EA-V3-60-Bahasa-Indonesia
Assessment: useful shorthand, but currently appears dashboard-derived. Do not treat as original Core family.

## Gap 8 — Multiple / continuous / triple Extreme ownership
Status: PARTIAL / HIGH-VALUE ADVANCED CANDIDATE.
Evidence:
- BBMA Basic OA mirror explicitly lists four Extreme forms and continuous/triple Extreme. It states second/third Extreme may lack normal TP Wajib/MHV when a larger timeframe is in MHV or Reentry; example: repeated H1 Extremes forming H4 MHV/Reentry.
  Source: https://id.scribd.com/document/734529476/BBMA-Basic-OA
- SOP Trading BBMA gives example of D1 Reentry with H4 rejection and H1/M15 lower-TF Extreme/TPW/MHV chains occurring during the D1 Reentry retest.
  Source: https://www.scribd.com/document/636284986/SOP-Trading-BBMA-converted-1
Assessment: repeated evidence supports parent-TF ownership as the explanation for apparent lower-TF TPW/MHV exceptions. However project conflict register intentionally excludes advanced no-TPW Extreme from executable Core until deterministic primary/video evidence exists. Do not change that decision yet.

## Gap 9 — Reentry validation / maturity chronology
Status: STATIC SEMANTICS ALREADY RESOLVED; RUNTIME VERIFICATION STILL OPEN.
Evidence:
- Project Finale V06: first Reentry candle validates, following/second candle is entry wording.
- Project conflict register CF-05 resolves this as closed source-TF validation with possible execution during immediately following live source-TF candle; no extra full-candle delay.
- External/forum material repeatedly corroborates the same teaching wording.
Assessment: no further source reinterpretation required. Remaining gap is runtime trace/F7-NMJE timing evidence, not research.

## Gap 10 — SL / exit lifecycle
Status: STILL OPEN / NO UNIVERSAL SOURCE-OWNED SL RULE.
Evidence:
- Project Finale V07 MA10 + allowance is explicitly classified personal risk-management and rejected/held from universal Core.
- Community sources conflict: swing high/low, candle boundary, opposite BB, fixed pip, fixed RR, reverse-signal close, money/percentage close and trailing methods all appear.
- Rule BBMA Oma Ally Original mirror recommends swing high/low but provenance is insufficient and conflicts with other community methods.
  Source: https://id.scribd.com/document/1003442568/Rule-BBMA-Oma-Ally-Original
Assessment: DO NOT promote any universal SL formula. TP Wajib is much better sourced than SL. Need direct 15-video evidence or stronger original material.

## Gap 11 — Universal advanced-family taxonomy
Status: OPEN.
Question: are RRM/RME/RZZL/Diamond/Conservative official Oma Ally taxonomy or later community/dashboard shorthand?
Evidence pattern:
- REM/RRE/REE are project-primary-PDF supported.
- RRM appears repeatedly in Tier-C notes/scanners.
- RME appears in forum/community evidence.
- RZZL and Diamond strongly correlate with SharpShooter dashboard versions.
Assessment: keep three buckets: SOURCE-CANONICAL (REM/RRE/REE), STRONG-CANDIDATE (RRM), COMMUNITY/TOOLING (RME/RZZL/Diamond unless higher-tier evidence appears).

## What can be improved now without waiting for transcripts
1. Documentation only: maintain this evidence register and terminology crosswalk.
2. Research queue: downgrade broad web search and focus transcript keyword extraction on unresolved advanced terms.
3. Runtime research: continue F7/NMJE Reentry maturity trace because source semantics are already sufficiently resolved.
4. No Strategy-Core/EA promotion for ZZL, Rejected EMA50, Gap, RRM, RME, Diamond, RZZL, advanced no-TPW Extreme or universal SL yet.

## What must wait for the 15-video transcripts
Highest priority keyword/evidence sweep:
- ZZL / zero loss / zone zero
- EMA50 / MA50 / reject / rejection
- gap / jarak BB / BB ke EMA50
- RRM / RME / RZZL / diamond
- double extreme / triple extreme / extreme kedua / extreme ketiga / berterusan
- TP wajib terbatal / tiada TP wajib / tiada MHV
- stop loss / cut loss / invalid / batal / exit
- overshoot / timeframe besar / reentry timeframe besar

## Current conclusion
Broad research is effectively exhausted for meaningful semantic gains. Remaining source gaps should now be closed primarily from the 15-video Intensive corpus plus targeted direct-source searches triggered by terms found there. No EA modification authorized.