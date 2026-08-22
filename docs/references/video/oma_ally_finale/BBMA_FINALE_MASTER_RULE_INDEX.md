# BBMA Finale — Master Strategy Core Rule Index

## Status
Evidence synthesis from BBMA Finale V01–V07. This file is **not yet a code change** and does not silently rewrite the locked EA/blueprint contracts. It is the source-analysis layer used to decide what the next BBMA Core specification should contain.

## Source basis
- Current operational baseline: `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` and existing source/entry contracts.
- Existing primary PDF: `Oma ally BBMA - AL.pdf`.
- Existing corroborating historical PDF: `BBMA technique.pdf`.
- New evidence: BBMA Finale class V01–V07 user-confirmed subtitles, corrected and extracted part-by-part in this directory.

## 1. Core cycle — KEEP
**Finale synthesis:** Extreme → TP Wajib → MHV/MLV → candle direction → Re-Entry → momentum/CSM → further Re-Entry → opposite Extreme / cycle restart.

**Evidence:** V01 00:57:06–00:59:17; V05 00:42:04–00:43:04; V06 00:06:09–00:08:49.

**Decision:** KEEP. Finale strongly corroborates the existing lifecycle. Signals and setups remain distinct.

## 2. Bollinger Band state and Momentum — CLARIFY / CORRECT
### Rule
- BB has at least two operational states in this teaching: expanding and flat/horizontal.
- An outside-BB close is momentum **when read in an expanding BB context**.
- An outside-BB close while BB is flat/horizontal is explicitly taught as **not momentum** and tends to revert in the illustrated cases.

**Evidence:** V02 00:13:51–00:18:07; 00:24:44–00:26:18.

**Decision:** ACCEPT as a high-priority Core clarification. Any implementation that equates `close outside BB` with momentum without BB-state context is too broad.

## 3. Extreme — CLARIFY / ADD with unresolved exceptions
### Normal/basic Extreme entry lifecycle
1. Relevant MA5 extends outside the appropriate outer BB.
2. Reversal candle appears.
3. Retest occurs; standalone Extreme entry is taken at/after the retest, not from condition 1 alone.
4. Retest may span multiple candles in the teaching examples.
5. If price closes outside the BB and becomes momentum during the attempted Extreme structure, the Extreme context is invalidated.

**Evidence:** V04 00:27:23–00:31:55; 00:37:27–00:40:53; V05 00:07:05–00:08:22.

### Normal Extreme TP Wajib
- Extreme sell: mandatory target is the opposite MA5/MA10 Low area.
- Extreme buy: mandatory target is the opposite MA5/MA10 High area.
- Mid BB is taught as a farther/maximum possibility, not the sole mandatory first target.

**Evidence:** V04 00:41:02–00:42:42; V05 00:16:41–00:18:02.

### Unresolved Extreme exceptions
- V05 says MA5 merely touching the outer BB may sometimes qualify, while “outside” is preferred.
- V05 says a reverse candle may sometimes be acceptable outside BB if it has returned inside MA5.
- V04/V05 mention advanced or higher-TF-context Extremes without the normal TP Wajib.

**Decision:** ACCEPT the three-step normal Extreme lifecycle and TP clarification. HOLD the exceptions. Do not relax the current outside-BB / normal TP rules until the conflicts are deterministically resolved.

## 4. MHV / MLV — KEEP / CLARIFY / ADD
### Terminology
The Finale repeatedly uses **MHV = Market Hilang Volume**. The primary summary PDF uses `MLV`; the historical technique PDF uses `MHV`. Treat them as source aliases until project terminology is deliberately standardized.

### Structural rule
- Forms after Extreme / TP phase in the taught cycle.
- Represents loss of prior momentum/volume.
- Must fail to close outside the relevant outer BB; outside close voids the setup and signals momentum.
- Uses a marked body/level and retest behavior.
- Can resemble double/triple top/bottom; Finale also mentions head-and-shoulders-like morphology.
- It is a setup/context stage, not a raw direction candle.

**Evidence:** V05 00:18:07–00:28:12; V01 00:59:18–01:00:05.

**Decision:** KEEP the existing validity/void rule; ADD/CLARIFY retest and broader morphology. Do not make H&S a mandatory condition.

## 5. Candle direction / eCSD / CSD — KEEP / CLARIFY
### Early direction
A candle closes past the relevant MA5/MA10 pair but does not yet cross Mid BB.

### Strong direction
A candle closes past the relevant MA5/MA10 pair and Mid BB.

### Entry status
Candle direction is a **signal**, not the entry setup. The class explicitly says to wait for Re-Entry.

**Evidence:** V05 00:28:41–00:36:51; V06 00:17:07–00:20:18; supported by V03.

**Decision:** KEEP the existing eCSD/CSD semantics and reinforce non-executability of raw direction signals.

## 6. Re-Entry — major ADD / CORRECT candidate
### Entry zone and invalidation
- Re-Entry follows direction/momentum and is the actual setup/entry zone.
- MA5 is the primary retest/entry area; MA10 confluence strengthens context.
- In the taught validation, the Re-Entry candle may penetrate MA5 but should not close through/clear both MA5 and MA10; doing so invalidates the shown Re-Entry structure.

**Evidence:** V05 00:37:25–00:41:16.

### Deterministic candle timing
- **First Re-Entry candle validates the setup.**
- **Second Re-Entry candle is the entry candle.**
- The rule is repeated across H4, H1, D1 and Weekly examples.

**Evidence:** V06 00:30:46–00:31:06; 00:52:48–00:56:27.

**Decision:** Strong candidate for Core adoption. This timing is one of the most material additions from Finale and should be reconciled with the current Re-Entry lifecycle before any code change.

## 7. Powerful Re-Entry / Type 2 — KEEP
- MA5 + MA10 + Mid BB meeting/confluence is a strong Re-Entry form.
- Minimum duration: three candles on the relevant timeframe.
- Existing PDF also states MA50 confluence can strengthen it further.

**Evidence:** V06 00:20:20–00:22:13; 00:32:41–00:33:31.

**Decision:** KEEP; Finale corroborates current Type 2 semantics.

## 8. Multi-timeframe relationship — KEEP / CLARIFY
- Higher-TF Re-Entry is read/completed through lower-TF signal/setup structures.
- Lower-TF opposite-looking direction can be part of a higher-TF Re-Entry and should not be treated as an independent reversal without higher-TF context.
- Timeframe chains can scale (D1/H4/H1, H4/H1/M15, H1/M15/M5, M15/M5/M1) while preserving the same structural idea.

**Evidence:** V05 00:34:48–00:36:37; 00:46:16–00:53:55; V06 00:26:57–00:29:02.

**Decision:** ACCEPT as clarification. Exact REM/RRE/REE signatures remain governed by the established PDF contracts because subtitle-only video evidence cannot reliably reconstruct the chart-pointing for every letter in every example.

## 9. REM / RRE / REE — KEEP current exact signatures
Current project signatures remain:
- REM = H4 Re-Entry + H1 Extreme + M15 MLV/MHV structure.
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

Finale explicitly names REM/RRE/REE and teaches the higher-to-lower timeframe relationship, but does not provide sufficiently unambiguous subtitle-only evidence to replace these exact PDF-derived mappings.

**Decision:** KEEP.

## 10. Items rejected from universal BBMA Strategy Core
- V07 personal preference to trade only H4 Re-Entry after strong H4 direction.
- V07 reported 33% early-direction backtest result; keep as sample-specific research only.
- Personal risk %, lot sizing, leverage, psychology, portfolio/account-management rules.
- Personal MA10 + allowance stop-loss method unless separately corroborated as a universal BBMA Core rule.
- Qualitative claims such as “pasti”, “100%”, “paling selamat” as deterministic guarantees.

## Overall result
Finale does **not replace the BBMA system**. It mostly refines the current Core and adds operational detail. The highest-value changes are:
1. BB state must qualify momentum.
2. Standalone Extreme needs a reversal + retest lifecycle before entry.
3. Normal Extreme TP Wajib is the opposite MA5/MA10 zone before treating Mid BB as the farther target.
4. MHV retest/inside-BB structure is more explicit.
5. Early vs strong candle direction is clearly separated and remains signal-only.
6. Re-Entry gains a concrete invalidation boundary and, most importantly, first-candle validation / second-candle entry timing.
7. MTF signals must be interpreted in higher-timeframe context.

Unresolved exceptions remain in the conflict register and must not be coded silently.
