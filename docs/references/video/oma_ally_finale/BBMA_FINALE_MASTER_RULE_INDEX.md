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

## 3. Extreme — KEEP / CLARIFY, with unresolved exceptions
### Normal/basic Extreme lifecycle
1. Relevant MA5 or MA5/MA10 extends outside the appropriate outer BB.
2. Reversal candle confirms the Extreme context.
3. Retest is the point of standalone Extreme entry.
4. Finale clarifies that the retest may take more than one candle and that condition 1 alone is not an entry.
5. A later outside-BB close / momentum condition voids the Extreme context.

**Finale evidence:** V04 00:27:23–00:31:55; 00:37:27–00:40:53; V05 00:07:05–00:08:22.

**Current-Core comparison:** The existing M08 contract already records Extreme as a signal, reversal confirmation, and the retest candle as entry. The current EA intentionally keeps standalone Extreme non-executable because the earlier sources did not provide a sufficiently deterministic universal reversal/retest algorithm. Finale strengthens and clarifies this lifecycle but still introduces unresolved exceptions, so it does not yet justify enabling standalone Extreme in Mode 2.

### Normal Extreme TP Wajib
- Extreme SELL: opposite MA5/MA10 Low area is taught as TP Wajib.
- Extreme BUY: opposite MA5/MA10 High area is taught as TP Wajib.
- Mid BB is presented as a farther/maximum possibility rather than the sole first mandatory target.

**Finale evidence:** V04 00:41:02–00:42:42; V05 00:16:41–00:18:02.

**Current-Core comparison:** The existing digest already says mandatory profit-taking after Extreme is toward MA5/MA10 or Mid BB. Finale makes the normal first target more explicit. This currently affects only the dormant/non-executable standalone Extreme contract; executable Mode 1/Mode 2 trades obtain TP from their validated Re-Entry source component.

### Unresolved Extreme exceptions
- V05 says MA5 merely touching the outer BB may sometimes qualify, although outside is preferred.
- V05 says a reversal candle may sometimes remain outside BB if it has returned inside MA5.
- V04/V05 mention advanced/higher-TF-context Extremes without the normal TP Wajib.

**Decision:** **KEEP/CLARIFY** the normal Extreme lifecycle and TP interpretation. **HOLD** all three exceptions. Do not relax the current stricter detector or enable standalone Extreme until these exceptions have deterministic source resolution.

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
2. clearer standalone Extreme reversal/retest lifecycle and TP Wajib interpretation, while still withholding ambiguous exceptions;
3. richer MHV/MLV retest/morphology explanation;
4. stronger confirmation that eCSD/CSD are direction signals and Re-Entry is the entry setup;
5. a useful first-candle-validation / second-candle-entry teaching phrase that must be mapped carefully to the existing closed-candle execution architecture;
6. stronger higher-TF ownership/context for lower-TF signals.

The most important practical finding is not that the current Core specification is broadly wrong, but that **some active implementation details—especially M09 MHV/MLV—do not fully express the already-supported source semantics**. Those are separated into the implementation gap register so source changes are not confused with coding fixes.
