# BBMA Finale — Master Strategy Core Rule Index

## Status
Final evidence synthesis from BBMA Finale V01–V07, reconciled against the **current** PDF-derived BBMA Core contracts and the active `blueprint/source/BBMA_EA.mq4` on the status-owner branch identified by `blueprint/CURRENT.md`.

This is a source-analysis layer only. It does **not** authorize an EA code change by itself.

## Source basis and precedence
- Existing operational baseline: `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` and locked Core contracts.
- Existing primary PDF: `Oma ally BBMA - AL.pdf`.
- Existing corroborating historical PDF: `BBMA technique.pdf`.
- Supplemental instructional evidence: BBMA Finale V01–V07 user-confirmed subtitles.

Where Finale merely confirms a rule already present in the current Core, it is classified **KEEP**, not falsely described as a new rule. Where subtitle/chart context is insufficient or conflicts with the established PDF rule, the item is **HOLD**.

## 1. Core cycle — KEEP
**Rule:** Extreme → TP Wajib → MHV/MLV → candle direction → Re-Entry → momentum/CSM → further Re-Entry → opposite Extreme / cycle restart.

**Finale evidence:** V01 00:57:06–00:59:17; V05 00:42:04–00:43:04; V06 00:06:09–00:08:49.

**Current-Core comparison:** Already present in the PDF-derived rule digest.

**Decision:** **KEEP.** Finale strongly corroborates the existing lifecycle and the distinction between signal and setup.

## 2. Bollinger Band state and Momentum — KEEP / STRONG CORROBORATION
**Rule:**
- Expanding/directional BB + close outside the relevant outer BB = momentum/CSM context.
- A close outside the BB while the BB is flat/horizontal is explicitly **not** treated as momentum in the Finale teaching.

**Finale evidence:** V02 00:13:51–00:18:07; 00:24:44–00:26:18.

**Current-Core comparison:** The existing M10 source contract already requires an outside-BB close together with expanding/directional BB movement and explicitly rejects the old simplistic momentum logic. Therefore Finale does **not** introduce a new momentum gate; it validates the current contract.

**Decision:** **KEEP.** No Strategy-Core change required here. Flat/expanding BB remains an important semantic distinction.

## 3. Extreme — KEEP / CLARIFY; accepted F2 lifecycle

### Normal/basic Extreme lifecycle
1. The relevant MA5 or MA5/MA10 extends outside the appropriate outer BB under the strict Core detector.
2. A reversal candle confirms the Extreme context.
3. A later retest is the standalone Extreme entry stage; the retest may span multiple candles.
4. A later accepted outside-BB/Momentum invalidation voids the lifecycle before maturity promotion.

**Finale evidence:** V04 00:27:23–00:31:55; 00:37:27–00:40:53; V05 00:07:05–00:08:22.

**Current-Core / owner-code comparison (CP11, 2026-10-26):** Core V2 §5.4 and the user-approved F2 decision now provide a deterministic project mapping. Build 5.15 contains the M08 RAW → REVERSAL_CONFIRMED → RETEST_READY lifecycle. Reversal-confirmed H1/H4 snapshots feed M13's unchanged REM/RRE/REE signatures. Standalone H1 Extreme is eligible only in Mode 2 from exact RETEST_READY state, with M15's same-direction active H4 and M11 D1 gates, M16 exact-identity revalidation, and M17's approved SL/TP mapping. RAW and reversal-only standalone signals remain non-executable.

This is a static owner mapping, not a claim of focused lifecycle tests, broker/runtime verification or production readiness. The exact close-progression/body-edge/first-touch formulas are the minimal project mapping in Core V2 §5.4, not verbatim Oma Ally formulas.

### Normal Extreme TP Wajib
- Extreme SELL: the opposite MA5/MA10 Low area is the normal first TP-Wajib area.
- Extreme BUY: the opposite MA5/MA10 High area is the normal first TP-Wajib area.
- Mid BB is farther/maximum context, not a required extension after first valid opposite-MA completion.
- M17's exact H1 zone-edge coordinate on the RETEST completion candle is the separate, approved Q5 project execution mapping. It does not alter the source-owned TP-Wajib area.
- M11J's D1 `D1_OPP_EXTREME_TPW` route is a distinct project extension; it is not the standalone H1 path. Its dedicated lifecycle feature gate is currently OFF and M17 fails closed rather than substituting a legacy TP.

**Finale evidence:** V04 00:41:02–00:42:42; V05 00:16:41–00:18:02. Core basis: §5.2 and residual HOLD closure decision.

### Exception disposition
- **CF-02:** touch-only MA5 does not create a canonical Extreme; strict outside-BB remains.
- **CF-03:** no universal close-inside-BB rule and no blanket outside-BB reversal exception; accepted invalidation keeps precedence.
- **CF-04:** advanced repeated-LTF Extreme without a fresh local TPW/MHV is bounded by its independently valid immediate HTF parent; it does not apply to D1.

**Decision:** Keep the accepted normal lifecycle and bounded §5.3 exceptions. Do not reinstate the old claim that standalone Mode 2 Extreme is wholly non-executable; do not expand beyond the approved mappings.

## 4. MHV / MLV — KEEP / CLARIFY at Core level; implementation audit required
### Terminology
Finale repeatedly uses **MHV = Market Hilang Volume**. The primary summary PDF uses `MLV`; the historical technique PDF uses `MHV`.

**Decision:** Treat `MHV` and `MLV` as source terminology aliases for the same loss-of-volume setup family unless a future source explicitly distinguishes them. Do not create two independent setup types merely from the spelling difference.

### Core structural rule
- Forms after Extreme / TP phase in the taught cycle.
- Represents loss of prior momentum/volume.
- Must fail to close outside the relevant outer BB; an outside close voids the setup and indicates momentum.
- Highest/lowest body or equivalent marked reference is used for retest context.
- Double/triple top/bottom morphology is supported; Finale also shows H&S-like morphology as an example, not a compulsory condition.
- It is a setup/context stage, not a raw direction candle.

**Finale evidence:** V05 00:18:07–00:28:12; V01 00:59:18–01:00:05.

**Current-Core comparison:** The PDF-derived Core already contains the outer-BB void rule, body marking/retest, and double/triple morphology. Finale mostly corroborates and expands the visual explanation. However, the active M09 implementation does not fully represent that Core contract; this is tracked separately in `BBMA_FINALE_CORE_IMPLEMENTATION_GAP_REGISTER.md`.

**Decision:** **KEEP/CLARIFY** at Strategy-Core level. H&S-like appearance remains non-mandatory.

## 5. Candle direction / eCSD / CSD — KEEP / STRONG CORROBORATION
### Early direction / eCSD
Relevant MA5/MA10 pair is crossed without the stronger Mid BB cross.

### Strong direction / CSD
Relevant MA5/MA10 pair and Mid BB are crossed.

### Entry status
Candle direction is a **signal**, not the entry setup. Wait for Re-Entry.

**Finale evidence:** V05 00:28:41–00:36:51; V06 00:17:07–00:20:18; supported by V03.

**Current-Core comparison:** These semantics already exist in the M10 contract and current Mode 1/Mode 2 eligibility design.

**Decision:** **KEEP.** No raw eCSD/CSD execution.

## 6. Re-Entry — KEEP / CLARIFY, with one timing semantic to verify
### Entry zone and MA5/MA10 validity
- Re-Entry follows direction/momentum and is the actual setup/entry zone.
- MA5 is the main retest area and MA10 confluence strengthens context.
- Finale says the Re-Entry candle may penetrate MA5 but should not close through/clear both MA5 and MA10 in the taught structure.

**Finale evidence:** V05 00:37:25–00:41:16.

**Current-Core comparison:** Current M12 confirmation already requires BUY closes on/above the relevant MA5/MA10 Low cluster and SELL closes on/below the relevant MA5/MA10 High cluster. Therefore this is primarily **corroboration**, not a newly discovered invalidation rule.

### First-candle validation / second-candle entry
- Finale repeatedly states: **first Re-Entry candle validates; second Re-Entry candle is the entry candle**.
- Repeated across H4, H1, D1 and Weekly examples.

**Finale evidence:** V06 00:30:46–00:31:06; 00:52:48–00:56:27.

**Current-Core comparison:** M12 confirms only from a fully closed source candle. The EA then makes the decision/execution after that candle has closed, which operationally can place execution at the beginning/current price of the next candle. Therefore the Finale wording may already match the runtime architecture rather than require an additional one-full-candle delay. The current data field names (`ConfirmationCandle`, `EntryCandle`, `EntryPrice`) blur this distinction because confirmation metadata is stored from the closed validation candle while broker execution uses the later live market price.

**Decision:** **CLARIFY / VERIFY SEMANTICS**, not an automatic code correction. Do **not** add another candle delay until the exact intended mapping is proven against chart/audio examples and runtime timestamps.

## 7. Powerful Re-Entry / Type 2 — KEEP
- MA5 + MA10 + Mid BB confluence is Powerful Re-Entry.
- MA50 confluence strengthens it further.
- Minimum duration is three candles on the relevant timeframe.

**Finale evidence:** V06 00:20:20–00:22:13; 00:32:41–00:33:31.

**Current-Core comparison:** Already encoded in the current M12 source contract.

**Decision:** **KEEP.**

## 8. Multi-timeframe relationship — KEEP / CLARIFY
- Higher-TF Re-Entry is read/completed through lower-TF signal/setup structures.
- A lower-TF opposite-looking direction can belong to a higher-TF Re-Entry and must not automatically be interpreted as an independent reversal.
- The structural idea scales across chains such as D1/H4/H1, H4/H1/M15, H1/M15/M5 and M15/M5/M1.

**Finale evidence:** V05 00:34:48–00:36:37; 00:46:16–00:53:55; V06 00:26:57–00:29:02.

**Current-Core comparison:** Multi-timeframe confirmation already exists in the PDF baseline and exact REM/RRE/REE contracts. Finale adds useful teaching context but does not replace the locked mappings.

**Decision:** **KEEP / CLARIFY.**

## 9. REM / RRE / REE — KEEP exact PDF-derived signatures
Current signatures remain:
- REM = H4 Re-Entry + H1 Extreme + M15 MLV/MHV structure.
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

Finale names REM/RRE/REE and demonstrates the higher-to-lower-timeframe principle, but subtitle-only evidence cannot reliably reconstruct every chart-pointing detail.

**Decision:** **KEEP.** Do not reinterpret the exact signatures from SRT alone.

## 10. REJECT from universal BBMA Strategy Core
The following Finale material must not be promoted into universal Core without stronger independent Core evidence:
- V07 personal preference to trade only H4 Re-Entry after strong H4 direction.
- V07 reported ~33% early-direction backtest result from the speaker's stated sample.
- Personal risk %, leverage, lot sizing, psychology and portfolio/account-management rules.
- Personal MA10 + allowance stop-loss method as a universal source-owned BBMA SL rule.
- Literal encoding of qualitative phrases such as “pasti”, “100%” or “paling selamat”.

## Overall conclusion
BBMA Finale does **not create a new BBMA strategy**. Relative to the current project Core, most of its important teaching is **corroboration and clarification**, not wholesale replacement.

The strongest post-Finale gains are:
1. stronger source confidence in the current expanding-BB momentum rule;
2. clearer standalone Extreme reversal/retest lifecycle and TP Wajib interpretation; Core §5.3 resolves the touch-only and reversal-position conflicts and bounds the repeated-LTF exception;
3. richer MHV/MLV retest/morphology explanation;
4. stronger confirmation that eCSD/CSD are direction signals and Re-Entry is the entry setup;
5. a useful first-candle-validation / second-candle-entry teaching phrase that must be mapped carefully to the existing closed-candle execution architecture;
6. stronger higher-TF ownership/context for lower-TF signals.

The current Build 5.15 owner has a canonical M09 MHV/MLV lifecycle; its full Core §6 owner, consumer and runtime reconciliation remains the next audit task. Historical IG-01–IG-03 are marked stale against this owner in the live implementation gap register and must not be treated as patch instructions. Runtime verification remains separate.
