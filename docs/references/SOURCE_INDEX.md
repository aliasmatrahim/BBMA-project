# BBMA Source Reference Index

## Purpose
This directory defines the source hierarchy used when auditing and repairing the BBMA Professional EA Master Blueprint.

GitHub remains the project source of truth. Source material is used to validate BBMA Core semantics; it must not be silently reinterpreted to fit existing code.

## Primary operational reference
### Oma ally BBMA - AL.pdf
- Project role: **PRIMARY OPERATIONAL BBMA REFERENCE**
- Document title: `BBMA Basics – Oma Ally`
- Attribution stated by document: `summarized by – Leeeta FX`
- Pages: 14
- Original filename supplied by user: `Oma ally BBMA - AL.pdf`
- SHA-256: `3e6065dd97c20951bd8af96bc81b81ca138800184be6fc4740a32aa4ab0a9c9c`
- Provenance status: **USER-SUPPLIED / NOT INDEPENDENTLY AUTHENTICATED AS AN OFFICIAL ORIGINAL OMA ALLY PUBLICATION**

### High-value sections
- Page 1: MA/BB settings and MA50 trend framing.
- Page 2: BBMA cycle: Extreme → MLV → CSD → Re-Entry → CSM.
- Pages 5–6: Signal/setup distinction and Extreme definition/validity.
- Pages 7–8: MLV formation, validity/void rules, CSD/eCSD relationship.
- Page 9: Re-Entry Type 1.
- Page 10: Re-Entry Type 2, Type 3 and Type 4, minimum-candle and multi-timeframe notes.
- Pages 12–13: REM/RRE/REE multi-timeframe combinations and trend-alignment notes.

## Secondary corroborating reference
### BBMA technique.pdf
- Project role: **SECONDARY / CORROBORATING BBMA REFERENCE**
- Pages: 44
- Original filename supplied by user: `BBMA technique.pdf`
- SHA-256: `b3457fb600f8a1ef7586e463938816de3da2e1801b53234d89511de38c946de1`
- PDF metadata title: `Microsoft Word - BBMA technique`
- Provenance status: **USER-SUPPLIED / HISTORICAL REFERENCE; NOT INDEPENDENTLY AUTHENTICATED AS AN OFFICIAL ORIGINAL OMA ALLY PUBLICATION**

### High-value sections
- Pages 18–19: basic BBMA laws, momentum/horizontal BB and buy/sell MA5/10 placement.
- Pages 27–30: Extreme definitions/examples.
- Pages 31–34: MHV definition, valid/void behaviour and examples.
- Pages 35–36: general Re-Entry definition/examples.

## Supplemental instructional / clarification source
### BBMA Finale V01–V07 subtitles
- Project role: **SUPPLEMENTAL INSTRUCTIONAL / CLARIFICATION EVIDENCE**.
- Source form: seven user-supplied SRT transcripts from a video class series identified by the user as `BBMA Finale` / Oma Ally class.
- Provenance status: **USER-SUPPLIED / USER-IDENTIFIED ATTRIBUTION; NOT INDEPENDENTLY AUTHENTICATED FROM THE SRT FILES ALONE**.
- User validation status: **V01–V07 confirmed usable/OK**.
- Processing status: part-by-part original, corrected, extracted-rule and summary artifacts prepared; derived Markdown analysis committed under `docs/references/video/oma_ally_finale/`.
- Raw/corrected SRT hashes and synchronization status are recorded in `docs/references/video/oma_ally_finale/VIDEO_SOURCE_INDEX.md`.

### High-value Finale findings pending formal Core reconciliation
- BB state qualifies momentum: an outside-BB close under flat/horizontal BB is explicitly distinguished from true expanding-BB momentum.
- Normal standalone Extreme is taught as a three-stage lifecycle: MA extension → reversal candle → retest before entry.
- Normal Extreme TP Wajib is clarified toward the opposite MA5/MA10 area, with Mid BB as farther context.
- MHV/MLV retest and inside-BB validity are explained more explicitly.
- Early candle direction vs strong candle direction is clarified; raw direction remains signal-only, not entry.
- Re-Entry receives a possible new deterministic timing rule: first Re-Entry candle validates, second Re-Entry candle is the entry candle.
- Higher-timeframe Re-Entry / lower-timeframe completion context is emphasized.
- Several statements remain intentionally unresolved and are tracked in `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md` rather than being silently merged.

The Finale material does **not automatically override** the established PDF contracts. Any ADD/CORRECT candidate must go through explicit Core/Blueprint reconciliation before implementation.

## Source precedence / conflict policy
1. `PROJECT_INSTRUCTIONS.md` governs project scope and change-control rules.
2. User-supplied BBMA source documents govern BBMA Core semantics.
3. `Oma ally BBMA - AL.pdf` remains the primary operational reference because it contains the more explicit cycle, four Re-Entry types, MLV/CSD relationships and REM/RRE/REE contracts.
4. `BBMA technique.pdf` remains the historical/secondary corroborating reference.
5. BBMA Finale V01–V07 is a supplemental instructional/clarification source. It may strengthen, clarify or expose gaps in existing Core rules, but it must not silently overwrite an established PDF rule.
6. If any sources conflict, **do not silently choose or merge rules**. Record the contradiction and resolve it explicitly in the blueprint audit/source-conflict register.
7. Master Blueprint code/specification must never override a clearly supported BBMA Core source rule merely because the current implementation behaves differently.
8. Project-reference status does not imply independent authentication of authorship or publication provenance.

## Current P0 relevance
The primary reference directly supports the prior P0 Step 3B reconciliation:
- Type 1: MA5/10 High resistance for sell in an uptrend; MA5/10 Low support for buy in a downtrend.
- Type 2: MA5/10 and MID BB meet/collide; strongest when MA50 also meets; minimum 3 candles per timeframe.
- Type 3: CSM forms, then price reverses/retraces to MA5 or MA50 for Re-Entry setup.
- Type 4: CSD forms, then price gyrates/retraces toward MA5/10; direction follows the relevant MA5/10 High/Low context.

## File-storage note
The GitHub connector used by ChatGPT exposes UTF-8 text writes but no mounted/local-file upload parameter. The exact raw PDF filenames/hashes remain recorded here. For the BBMA Finale series, full original/corrected SRT files are preserved in the generated source pack; GitHub synchronization state and hashes are recorded in `VIDEO_SOURCE_INDEX.md`. Derived analysis Markdown is committed directly to GitHub.
