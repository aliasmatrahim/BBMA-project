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

## Source precedence / conflict policy
1. `PROJECT_INSTRUCTIONS.md` governs project scope and change-control rules.
2. User-supplied BBMA source documents govern BBMA Core semantics.
3. `Oma ally BBMA - AL.pdf` is the primary operational reference because it contains the more explicit cycle, four Re-Entry types, MLV/CSD relationships and REM/RRE/REE contracts.
4. `BBMA technique.pdf` is used to corroborate or challenge interpretations.
5. If the two source documents conflict, **do not silently choose or merge rules**. Record the contradiction and resolve it explicitly in the blueprint audit.
6. Master Blueprint code/specification must never override a clearly supported BBMA Core source rule merely because the current implementation behaves differently.
7. Project-reference status does not imply independent authentication of authorship or publication provenance.

## Current P0 relevance
The primary reference directly supports the pending P0 Step 3B reconciliation:
- Type 1: MA5/10 High resistance for sell in an uptrend; MA5/10 Low support for buy in a downtrend.
- Type 2: MA5/10 and MID BB meet/collide; strongest when MA50 also meets; minimum 3 candles per timeframe.
- Type 3: CSM forms, then price reverses/retraces to MA5 or MA50 for Re-Entry setup.
- Type 4: CSD forms, then price gyrates/retraces toward MA5/10; direction follows the relevant MA5/10 High/Low context.

## Binary-file storage note
The GitHub connector used by ChatGPT currently exposes UTF-8 text writes but no direct binary-file upload parameter. Therefore this index records the exact original filenames and SHA-256 hashes. The raw PDF files should be placed under `docs/references/` unchanged when binary upload is available or via the GitHub UI. Until then, the exact user-supplied PDFs remain the source files used during the active audit.
