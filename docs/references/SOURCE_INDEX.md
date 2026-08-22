# BBMA Source Reference Index

## Purpose
This directory defines the source hierarchy used when auditing and repairing the BBMA Professional EA Master Blueprint.

GitHub remains the project source of truth. Source material is used to validate BBMA Core semantics; it must not be silently reinterpreted to fit existing code.

## Canonical derived Strategy-Core reference
### `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
- Project role: **ACTIVE / AUTHORITATIVE CONSOLIDATED BBMA STRATEGY-CORE SPECIFICATION**.
- Scope: accepted Strategy-Core rules only.
- Built from: the primary PDF, secondary/corroborating PDF, and accepted BBMA Finale V01–V07 evidence.
- Excludes: `HOLD`, `UNCERTAIN`, personal workflow, money-management and EA-management material.
- Important: this is a **derived project specification**, not a replacement for the original source files and not an independent claim of publication/authorship provenance.
- Every material rule must remain traceable to the source digest and/or timestamped Finale evidence.

This canonical file is the preferred **developer-facing Core rule reference**. Original PDFs, Finale transcripts, rule extractions and conflict registers remain the evidence/provenance layer behind it.

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

### Reconciled Finale findings
After comparing Finale against the **current** PDF-derived Core contracts, most important Finale statements are corroboration/clarification rather than brand-new Core rules:
- expanding/directional BB is already part of current momentum/CSM semantics; Finale strongly confirms that flat-BB outside closes are not momentum;
- the existing Extreme source contract already knows reversal + retest before standalone entry; Finale adds richer timing/context but leaves several exceptions unresolved;
- normal Extreme TP Wajib is clarified more specifically toward the opposite MA5/MA10 area, with Mid BB as farther context;
- MHV/MLV retest, validity and morphology are explained more richly and expose active M09 implementation gaps;
- eCSD vs CSD and the non-executability of raw direction signals are strongly corroborated;
- first-Re-Entry-candle validation / second-candle entry is treated as a **semantic/timing verification item**, because the current closed-candle architecture may already execute at the beginning of the next candle;
- higher-timeframe Re-Entry / lower-timeframe completion context is emphasized without changing the exact PDF-derived REM/RRE/REE signatures.

Unresolved items remain in `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`. Active code mismatches are separated into `BBMA_FINALE_CORE_IMPLEMENTATION_GAP_REGISTER.md`.

The Finale material does **not automatically override** the established PDF contracts. A source clarification and an implementation fix are deliberately treated as separate decisions.

## Source precedence / conflict policy
1. `PROJECT_INSTRUCTIONS.md` governs project scope and change-control rules.
2. The original user-supplied BBMA source documents remain the evidence layer governing BBMA Core semantics.
3. `Oma ally BBMA - AL.pdf` remains the primary operational reference because it contains the more explicit cycle, four Re-Entry types, MLV/CSD relationships and REM/RRE/REE contracts.
4. `BBMA technique.pdf` remains the historical/secondary corroborating reference.
5. BBMA Finale V01–V07 is a supplemental instructional/clarification source. It may strengthen, clarify or expose gaps in existing Core rules, but it must not silently overwrite an established PDF rule.
6. `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` is the canonical **derived developer-facing consolidation** of only accepted Core rules from the evidence hierarchy above.
7. If any sources conflict, **do not silently choose or merge rules**. Record the contradiction and resolve it explicitly in the blueprint audit/source-conflict register.
8. Master Blueprint code/specification must never override a clearly supported BBMA Core source rule merely because the current implementation behaves differently.
9. Project-reference status does not imply independent authentication of authorship or publication provenance.

## Current implementation relevance
The canonical V2 Core preserves the previously reconciled contracts, including:
- Type 1: MA5/10 High resistance for sell in an uptrend; MA5/10 Low support for buy in a downtrend.
- Type 2: MA5/10 and MID BB meet/collide; strongest when MA50 also meets; minimum 3 candles per timeframe.
- Type 3: CSM forms, then price reverses/retraces to MA5 or MA50 for Re-Entry setup.
- Type 4: CSD forms, then price gyrates/retraces toward MA5/10; direction follows the relevant MA5/10 High/Low context.
- REM: H4 Re-Entry + H1 Extreme + M15 MHV/MLV.
- RRE: D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE: D1 Re-Entry + H4 Extreme + H1 Extreme.

Post-Finale implementation mismatches must be handled through the separate implementation-gap register and subsequent blueprint/code audit. They must not be confused with source-of-truth changes.

## File-storage note
The GitHub connector used by ChatGPT exposes UTF-8 text writes but no mounted/local-file upload parameter. The exact raw PDF filenames/hashes remain recorded here. For the BBMA Finale series, full original/corrected SRT files are preserved in the generated source pack; GitHub synchronization state and hashes are recorded in `VIDEO_SOURCE_INDEX.md`. Derived analysis Markdown is committed directly to GitHub.
