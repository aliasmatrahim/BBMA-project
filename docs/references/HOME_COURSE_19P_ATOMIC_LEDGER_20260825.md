# BBMA Home Course Workbook — 19-Page Atomic Rule Ledger

Status: ATOMIC EXTRACTION COMPLETE / CORE-V2 ROW MAPPING NEXT
Date: 2026-08-25
Source: `docs/references/original/333531988-BBMA-Home-Course.pdf`
Target: `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
Parent audit: `docs/references/HOME_COURSE_19P_FORENSIC_AUDIT_20260825.md`

## Contract

One row = one materially testable or semantically independent source claim. UI/cosmetic/account/news-only material is retained for provenance but tagged NON_CORE. Summary repetitions are retained and tagged DUP candidates rather than silently deleted. This ledger does NOT yet publish coverage; exact Core-V2 row mapping and dedup must complete first.

Legend: `A` applicable Strategy-Core candidate; `N` NON_CORE; `D` duplicate/corroboration candidate; `H` hold/needs reconciliation.

## Page 1 — Lesson 1 BB

HC-P01-001 [N] Example chart instrument is EUR/USD.
HC-P01-002 [N] First indicator is Bollinger Bands.
HC-P01-003 [N] MT4 menu path for Bollinger Bands.
HC-P01-004 [N] Workbook uses default BB setting/cosmetics Royal Blue, thickness 2.
HC-P01-005 [A] BB has Top, Low and Mid lines.
HC-P01-006 [A] BB state/shape conveys information when expanding, contracting or horizontal/sideways.
HC-P01-007 [A] Expansion beginning from horizontal indicates strong Momentum is occurring.
HC-P01-008 [A] BB acts as a price boundary/container.
HC-P01-009 [A] Normal price/candles generally operate inside BB.
HC-P01-010 [A] Candle outside BB is an abnormal/significant condition.
HC-P01-011 [A] Horizontal BB indicates no Momentum/strength and price ranges between Top and Low BB.
HC-P01-012 [A] Greater BB expansion corresponds to stronger price movement.
HC-P01-013 [A] Workbook distinguishes directional/vertical BB from horizontal BB.

## Page 2 — Horizontal vs directional BB

HC-P02-001 [A] Horizontal-BB and directional-BB boundary interactions have different meanings.
HC-P02-002 [A/H] Horizontal BB: wick pierces Top BB but close remains inside -> downside expectation at least to Mid BB.
HC-P02-003 [A/H] Horizontal BB: wick pierces Low BB but close remains inside -> upside expectation at least to Mid BB.
HC-P02-004 [A/H] Horizontal BB: body+wick outside and close outside -> source expects movement/reversion at least toward Mid BB; directional wording is ambiguous in text.
HC-P02-005 [A/H] Horizontal BB: wick approaches/pierces without exceeding boundary -> source expects movement toward Mid BB; exact direction requires chart context.
HC-P02-006 [A] Directional BB: wick pierces Top/Bottom and closes inside -> price continuation in prevailing direction.
HC-P02-007 [A] Directional BB: body+wick close outside BB -> price continuation in prevailing direction.
HC-P02-008 [A] Candle close outside BB is a Momentum candle.
HC-P02-009 [H] Horizontal BB width around 10–20 pips is stated to precede a large breakout; absolute wording requires reconciliation.
HC-P02-010 [A] BB interpretation should reference multiple timeframes.
HC-P02-011 [A] When a candle closes outside directional BB, do not trade against it; follow price direction.
HC-P02-012 [A] Every directional-BB outside close has a Re-Entry on a lower timeframe.

## Page 3 — Mid BB

HC-P03-001 [A] Mid BB is SMA20.
HC-P03-002 [A] Mid BB to Top BB is named Buying Zone.
HC-P03-003 [A/H] In Buying Zone, source instructs looking for Buy opportunity.
HC-P03-004 [A] Crossing Mid BB from Buying Zone enters Selling Zone.
HC-P03-005 [A] Mid BB to Lower BB is named Selling Zone.
HC-P03-006 [A/H] In Selling Zone, source instructs looking for Sell opportunity.
HC-P03-007 [A] Mid-BB slope (up/down/horizontal) is a same-timeframe trend guide.

## Page 4 — MA5

HC-P04-001 [N] MA5 is the next indicator introduced.
HC-P04-002 [N] MT4 menu path for Moving Average.
HC-P04-003 [A] MA5 High = period 5, Linear Weighted, applied High.
HC-P04-004 [N] MA5 High cosmetic color red/thickness 2.
HC-P04-005 [A] MA5 Low = period 5, Linear Weighted, applied Low.
HC-P04-006 [N] MA5 Low cosmetic color magenta/thickness 2.
HC-P04-007 [A] During falling price, candles are below sloping MA5 High.
HC-P04-008 [A] During falling price, MA5 Low lies above candle body.
HC-P04-009 [D] Outside-BB close is Momentum.
HC-P04-010 [A/H] During falling price, close outside MA5 Low is also described as Momentum.
HC-P04-011 [A/H] Close outside BB and MA5 Low while MA5 Low hugs Lower BB is described as very strong Momentum.

## Page 5 — MA10 High / direction candle

HC-P05-001 [A] MA10 High = period 10, Linear Weighted, applied High.
HC-P05-002 [N] MA10 High cosmetic color yellow/thickness 2.
HC-P05-003 [A] During falling price, MA10 High is relatively far from candles.
HC-P05-004 [A/H] Price is not considered to have risen/reversed upward until a candle closes above MA10 High.
HC-P05-005 [A] First candle closing above MA10 is named Candle Arah (direction candle).
HC-P05-006 [A] Close beyond MA10 but not Mid BB = weak/not-strong direction; market change not confirmed.
HC-P05-007 [A] Close beyond MA10 and Mid BB = strong direction.

## Page 6 — MA10 Low / MA ordering

HC-P06-001 [A] MA10 Low = period 10, Linear Weighted, applied Low.
HC-P06-002 [N] MA10 Low cosmetic color white/thickness 2.
HC-P06-003 [A] MA5/MA10 High/Low relationships differ between rising and falling markets.
HC-P06-004 [A] During down move, candles are below MA5 High and MA10 High.
HC-P06-005 [A] During down move, MA10 High is above MA5 High.
HC-P06-006 [A] During down move, MA10 Low is above MA5 Low.

## Page 7 — MA50

HC-P07-001 [A] MA50 = period 50, Exponential, applied Close.
HC-P07-002 [N] MA50 cosmetic color aqua/thickness 2.
HC-P07-003 [A] MA50 indicates trend.
HC-P07-004 [A] In downtrend, candle is below MA50 and Mid BB.
HC-P07-005 [A] In downtrend, MA5/MA10 High/Low are below MA50.
HC-P07-006 [A] MA5/MA10 cross Mid BB before crossing MA50 during structural transition.

## Page 8 — Basic laws / Mid-BB confirmation

HC-P08-001 [A] Basic law: MA should not be outside BB.
HC-P08-002 [A] MA outside BB is Extreme.
HC-P08-003 [A] Extreme is a signal, not a setup.
HC-P08-004 [A] Extreme is an early signal that a move is beginning to end.
HC-P08-005 [A] Basic law: candle should not close outside BB.
HC-P08-006 [A] Candle close outside BB is Momentum.
HC-P08-007 [A] Momentum means market strength is beginning/active.
HC-P08-008 [A] BB controls/frames market movement.
HC-P08-009 [A] Top BB governs whether upside continuation persists or is stopped.
HC-P08-010 [A] Low BB governs whether downside continuation persists or is stopped.
HC-P08-011 [A] Outside-BB close means Momentum continues.
HC-P08-012 [A] No outside Top/Low close means no Momentum.
HC-P08-013 [H] Source says no Momentum means market will change direction; deterministic wording requires lifecycle context.
HC-P08-014 [A] Mid BB separates rising and falling zones.
HC-P08-015 [A] Rise/fall direction is confirmed at Mid BB.
HC-P08-016 [A/H] Break Mid BB -> retest -> failure to recross Mid BB confirms direction change (example rise to fall).

## Page 9 — Extreme lifecycle

HC-P09-001 [A] Extreme occurs when a setup/condition violates basic BBMA law.
HC-P09-002 [A] MA5 outside BB defines Extreme in Workbook summary.
HC-P09-003 [A] Extreme lifecycle requires MA5 outside BB, reverse candle, then retest candle.
HC-P09-004 [A] Reverse candle marks the current highest-volume/reference area and signals the prior rise/fall may be ending.
HC-P09-005 [A] Mark reverse-candle reference and wait for retest.
HC-P09-006 [A] Retest candle is the Extreme entry event.
HC-P09-007 [A] Extreme entry has mandatory TP at MA5/MA10, with Mid BB as furthest target; no compromise.

## Page 10 — MHV

HC-P10-001 [A] MHV means Market Hilang Volume.
HC-P10-002 [A] MHV: candle fails to close beyond Top BB for sell-side exhaustion example.
HC-P10-003 [A] MHV requires reverse candle; it terminates/invalidates prior rise continuation.
HC-P10-004 [A] MHV entry is a later retest of the marked highest-volume/reverse-candle area.
HC-P10-005 [A] Retest tests whether the marked volume can be exceeded or movement ends there.
HC-P10-006 [A] MHV occurs after Extreme.
HC-P10-007 [A] MHV TP is not obligatorily MA5/10 or Low BB; management depends on next candle behavior.
HC-P10-008 [A] After MHV, if next candle closes outside BB, source says hold because Momentum exists.
HC-P10-009 [A/H] After MHV, if next candle closes inside BB, source says close position because market will reverse toward Top BB; directional example requires symmetric mapping.
HC-P10-010 [A] MHV -> direction candle -> Re-Entry -> no Momentum => mandatory TP.

## Page 11 — Candle Arah

HC-P11-001 [A] Close beyond MA5/MA10 but not Mid BB = early/weak direction, not confirmed.
HC-P11-002 [A] Close beyond MA5/MA10 and Mid BB = strong direction.
HC-P11-003 [A] Retest intersection of marked volume and MA5 High is a strong entry location (sell-side example).
HC-P11-004 [A] Close below MA5/MA10 and Mid BB ends prior rise and confirms fall (sell-side example).
HC-P11-005 [H] Strong direction reaching Low BB without Momentum is stated not to require TP when Re-Entry has not yet occurred; hold lifecycle requires reconciliation.
HC-P11-006 [A] Strong direction must be followed by Re-Entry; if absent, source expects one to form.

## Page 12 — Re-Entry core

HC-P12-001 [A] Re-Entry is second/add-on entry level after MHV retest entry.
HC-P12-002 [A] Re-Entry candle close does not exceed MA5 and MA10.
HC-P12-003 [A] Re-Entry failing to exceed MA5, MA10 and Mid BB is a strong entry location.
HC-P12-004 [A] MA5+MA10+Mid-BB confluence Re-Entry is associated with minimum 3-candle movement on that timeframe.
HC-P12-005 [A] Direction/Momentum is followed by Re-Entry.
HC-P12-006 [N/H] Workbook labels MA5/MA10/Mid-BB Re-Entry as large-lot location; position sizing language is NON_CORE.
HC-P12-007 [A] Falling movement eventually forms sideways; sideways forms Re-Entry.
HC-P12-008 [N] Trader should distinguish small-lot and large-lot entry locations.
HC-P12-009 [A] When an opposite/new Extreme appears, TP.
HC-P12-010 [D] Re-Entry candle close does not exceed MA5/MA10.
HC-P12-011 [N] Wait for specified entry location.
HC-P12-012 [A] Do not enter directly at Candle Arah.
HC-P12-013 [A] Candle Arah is a market-change signal.
HC-P12-014 [A] Entry authority belongs to Re-Entry setup.
HC-P12-015 [D] MA5+MA10+Mid-BB Re-Entry implies minimum 3 candles of movement.
HC-P12-016 [N/H] Large-lot wording at powerful Re-Entry is money-management material; 3-candle structural claim remains applicable via HC-P12-004.

## Page 13 — Re-Entry MTF

HC-P13-001 [A] 3 candles means 3h on H1 and 12h on H4.
HC-P13-002 [A/H] During H4 three-candle Re-Entry window, source expects additional lower-TF entries.
HC-P13-003 [A] Lower-TF setups should be sought in higher-TF direction.
HC-P13-004 [A/H] Within one H4 candle, lower-TF entry opportunities may be used as additional entries.
HC-P13-005 [D/H] During 12h/3 H4 candles, source expects lower-TF setup(s).
HC-P13-006 [A] H4 sell Momentum -> move to lower TF and seek sell entry.
HC-P13-007 [A] If higher TF is sell, lower-TF rises/retracements are sell opportunities; do not oppose trend.
HC-P13-008 [A] If D1 setup is sell, lower-TF retracements are sell opportunities.
HC-P13-009 [A] Re-Entry is described as the best entry because direction has been strongly confirmed.
HC-P13-010 [A] Follow major trend.
HC-P13-011 [A] Candle Arah destination is an outer BB (Top or Low according to direction).
HC-P13-012 [A/H] Candle Arah formed in retracement has outer-BB destination (Top BB in given example).
HC-P13-013 [H] Strong direction -> Re-Entry -> outer BB without Momentum -> wait for reverse confirmation then retest entry; lifecycle needs deterministic reconciliation.
HC-P13-014 [A] Retracement/rise ends when direction signal appears aligned with major trend.
HC-P13-015 [A] Re-Entry must not close beyond MA5, MA10 and Mid BB.
HC-P13-016 [H] In downtrend, strong bullish D1 direction candle is stated to target Top BB; countertrend destination claim requires scope clarification.
HC-P13-017 [A] At D1 Top BB destination, inspect lower TF for continuation-aligned or reversal setup.
HC-P13-018 [A] Close failing MA5/MA10 at Mid-BB confluence is high-quality entry.

## Page 14 — Major trend / cross-TF structure

HC-P14-001 [H] Strong direction reaching Low BB without prior Re-Entry and without Momentum -> hold because Re-Entry is still expected.
HC-P14-002 [A] Extreme against major trend is weak/not strong.
HC-P14-003 [A] Major trend is determined by MA50.
HC-P14-004 [A] Price/candles above MA50 = major trend Buy.
HC-P14-005 [A/H] In major Buy trend, MA5/MA10 Low contacts are Re-Entry Buy locations.
HC-P14-006 [A] Repeated same-side Extremes without opposite Extreme between them indicate higher-timeframe structure may be forming.
HC-P14-007 [H] Double Extreme on H1 is stated to correspond to MHV on H4.
HC-P14-008 [H] If higher-TF MHV is complete/valid, lower-TF Extreme may be entered without waiting for another lower-TF MHV.
HC-P14-009 [D/H] Two H1 Extreme Sell without Extreme Buy between are stated to mean H4 MHV is forming.
HC-P14-010 [H] If H4 MHV is valid, source states there will be no further H1 MHV; absolute wording requires verification.
HC-P14-011 [A] MA50 major-trend function is said to work properly from minimum D1.
HC-P14-012 [A/H] H4 does not own major trend in Workbook; daily movement is owned by D1.
HC-P14-013 [A] Daily movement must be determined from D1 candle.
HC-P14-014 [H] If D1 says Buy while H4 says Sell, follow D1; execution precedence must be reconciled with current owner contract.
HC-P14-015 [A] D1 sell Momentum means that day's market strength is sell/down.
HC-P14-016 [H] Today's D1 close is stated to determine tomorrow's movement; predictive wording requires constrained interpretation.

## Page 15 — Re-Entry notes

HC-P15-001 [D] Direction must be followed by Re-Entry.
HC-P15-002 [D] Falling movement eventually enters sideways; at sideways wait for Mid-BB confluence.
HC-P15-003 [D] Sideways forms Re-Entry.
HC-P15-004 [A/H] During Re-Entry formation there must also be direction context.

## Page 16 — Momentum lifecycle

HC-P16-001 [A] Canonical local sequence: Direction -> Re-Entry -> Momentum.
HC-P16-002 [A] Momentum is followed by Re-Entry.
HC-P16-003 [H] Direction -> Re-Entry -> no Momentum => close position; market expected to reverse.
HC-P16-004 [H] Direction -> no Re-Entry => position may be held while waiting for Re-Entry.
HC-P16-005 [D] Momentum candle closes beyond Top/Low BB.
HC-P16-006 [N] Large-news event is said to create Momentum.
HC-P16-007 [N/H] News-specific instruction: after Momentum candle closes, enter next candle if lower TF aligns.
HC-P16-008 [N] News-specific permission to enter each candle.
HC-P16-009 [N] News move should align with major trend.
HC-P16-010 [N] If D1/Weekly major trend is down and news pushes up, do not follow news move.
HC-P16-011 [N] If news aligns with major trend, enter second candle after Momentum.
HC-P16-012 [A/H] Strong H1 Re-Entry with MA5/MA10/Mid BB and 3-candle expectation can use M5 during candles 2/3 for aligned lower-TF entry; execution signature expansion requires approval.
HC-P16-013 [A/H] Extreme Magic = MA5 and MA10 both outside BB; rare and associated with prolonged sideways.
HC-P16-014 [A] Re-Entry normally does not enter on first candle: first candle validates by closing on required side of MA5/MA10; second candle is entry.
HC-P16-015 [A] Candle crossing Mid BB + MA5 + MA10 + MA50 is described as very strong direction.

## Page 17 — Summary

HC-P17-001 [D] Extreme = MA5 outside BB.
HC-P17-002 [D] Extreme requires reverse candle.
HC-P17-003 [D] Extreme retest candle is entry.
HC-P17-004 [D] Extreme is early signal move is ending.
HC-P17-005 [D] Extreme mandatory TP at MA5/MA10 or Mid BB.
HC-P17-006 [D] MHV candle fails outer Top BB close in example.
HC-P17-007 [D] MHV requires reverse candle.
HC-P17-008 [D] Mark highest-volume body and wait for retest.
HC-P17-009 [D] MHV retest at marked volume + MA5 High.
HC-P17-010 [D] Early Candle Arah closes beyond MA5/MA10.
HC-P17-011 [A/H] Early Candle Arah may rotate/retest Top BB or earlier highest-volume area.
HC-P17-012 [D] Strong Candle Arah closes beyond MA5/MA10 + Mid BB.
HC-P17-013 [D] Direction is followed by Re-Entry.
HC-P17-014 [A/H] Re-Entry at Mid BB is stated 'no compromise'.
HC-P17-015 [A] Re-Entry with MA5+MA10+Mid BB+MA50 is stronger than ordinary Re-Entry.
HC-P17-016 [H] At trend-change direction, Re-Entry at MA5+MA10+Mid BB+MA50 is stated mandatory/no compromise.
HC-P17-017 [D] Momentum = outside-BB close.
HC-P17-018 [D] Momentum is followed by Re-Entry.
HC-P17-019 [D] Re-Entry occurs again after Momentum.
HC-P17-020 [A] Lower timeframe forms a replay/repetition of the BBMA sequence.
HC-P17-021 [A] Canonical cycle: Extreme -> MHV -> Candle Arah -> Re-Entry -> Momentum -> Re-Entry.

## Page 18 — Cycle management

HC-P18-001 [D] Cycle includes Extreme -> mandatory TP -> MHV -> Candle Arah -> Re-Entry -> Momentum -> Re-Entry.
HC-P18-002 [H] Re-Entry without subsequent Momentum causes market to make a reversal/rotation.
HC-P18-003 [A] Momentum implies another Re-Entry continuation opportunity.
HC-P18-004 [H] If no Re-Entry after Candle Arah, source permits hold until Re-Entry occurs.
HC-P18-005 [D/H] MHV -> strong direction -> Low BB without Re-Entry => no TP; wait for Re-Entry.
HC-P18-006 [D/H] Same rationale: direction requires later Re-Entry, so reaching Low BB before Re-Entry is not exit authority.
HC-P18-007 [A/H] At outer BB after strong direction, two branches: Momentum -> wait for Re-Entry; no Momentum -> source expects reversal.
HC-P18-008 [D/H] MHV -> Candle Arah -> Low BB without Re-Entry -> wait rather than TP.
HC-P18-009 [A] After Re-Entry, expected next phase is Momentum.
HC-P18-010 [D] After Momentum, wait for next Re-Entry.
HC-P18-011 [D/H] MHV -> Candle Arah -> Re-Entry -> no Momentum => TP because source expects reversal.
HC-P18-012 [A] Same MHV setup can branch into different lifecycle outcomes depending on Momentum/Re-Entry sequence.
HC-P18-013 [D] Full cycle starts Extreme -> mandatory TP -> MHV -> Candle Arah -> Re-Entry -> Momentum -> Re-Entry.
HC-P18-014 [D] Sideways forms Re-Entry.
HC-P18-015 [A] Sideways on a larger TF produces/newly exposes setups on smaller TFs.

## Page 19 — Account workflow

HC-P19-001 [N] Example starts with account balance 500.
HC-P19-002 [N] Grow example account from 500 to 1000.
HC-P19-003 [N] Split grown account back into two 500 accounts.
HC-P19-004 [N] Early-stage workflow emphasizes making money and splitting accounts.
HC-P19-005 [N] Source suggests postponing withdrawals for several months.
HC-P19-006 [N] Grow trading accounts.
HC-P19-007 [N] Transfer profits from growth accounts to main account.
HC-P19-008 [N] Transfer profit from any profitable account to main account.
HC-P19-009 [N] Withdraw only from main account.
HC-P19-010 [N] Scalping account should be used only for scalping.
HC-P19-011 [N] Swing account should be used only for swing trading.

## Extraction totals (pre-dedup / pre-Core mapping)

- Total atomic provenance rows: **189**.
- Rows intentionally retain summary repetitions and source-level absolutes.
- `N` rows are excluded from Strategy-Core coverage denominator.
- `D` rows will be deduplicated to canonical atomic rules while preserving provenance aliases.
- `H` rows remain applicable candidates but cannot be silently promoted until reconciled against higher-priority evidence and existing project contracts.

## Next gate

1. Convert this provenance ledger into canonical deduplicated atomic-rule IDs.
2. Map each canonical applicable rule to exact Core V2 section(s).
3. Assign `COVERED`, `PARTIAL`, `MISSING`, or `CONFLICT/HOLD`.
4. Reconcile all `H` rows against Oma Ally primary PDF, BBMA Technique, Finale V01–V07, and conflict register.
5. Only then compute exact `covered / applicable = coverage%` and decide whether Core V2 needs V2.x/V3 promotion.
