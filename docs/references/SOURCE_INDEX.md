# BBMA Source Reference Index

## Purpose
This directory defines the source hierarchy used when auditing and repairing the BBMA Professional EA Master Blueprint.

GitHub remains the project source of truth. Source material is used to validate BBMA Core semantics; it must not be silently reinterpreted to fit existing code.

## Mandatory retrieval map
This index is the **first stop** for every BBMA Strategy-Core review. Do not infer that a source is absent merely because GitHub code search returns zero matches.

Canonical retrieval sequence:

1. `docs/references/SOURCE_INDEX.md` — this source map and precedence policy.
2. `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` — active accepted Core consolidation.
3. `docs/references/video/oma_ally_finale/BBMA_FINALE_MASTER_RULE_INDEX.md` — reconciled Finale synthesis.
4. `docs/references/video/oma_ally_finale/V01` through `V07` — episode-level `extracted_rules.md` / `summary.md` evidence when needed.
5. `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` — PDF-derived rule index.
6. Primary PDF evidence: `docs/references/original/Oma ally BBMA - AL.pdf`.
7. Secondary PDF evidence: `docs/references/original/BBMA technique.pdf`.
8. Original BBMA Finale subtitle evidence: `docs/references/original/video/oma_ally_finale/`.
9. Tier-B BBMA Home Course Workbook evidence as registered by `blueprint/CORE_V2_F7_WORKBOOK_AUTHENTICATION_AUDIT_20260824.md` and the related rule-reconciliation decisions. The reviewed binary is product-linked / strong-provenance but not Tier-A original provenance.
10. `docs/references/video/oma_ally_finale/BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md` — unresolved source conflicts/HOLD items.
11. `docs/references/video/oma_ally_finale/BBMA_FINALE_CORE_IMPLEMENTATION_GAP_REGISTER.md` — known implementation mismatches.
12. Relevant module source contracts and then the active Master Blueprint / EA implementation.

**Existence rule:** zero-result code search is not proof of absence. For an expected source, use this index and known path/directories before reporting it missing.

## Canonical derived Strategy-Core reference
### `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
- Project role: **ACTIVE / AUTHORITATIVE CONSOLIDATED BBMA STRATEGY-CORE SPECIFICATION**.
- Scope: accepted Strategy-Core rules only.
- Built from: the primary PDF, secondary/corroborating PDF, accepted BBMA Finale V01–V07 evidence, and explicitly reconciled high-value findings from the authenticated Tier-B BBMA Home Course Workbook copy.
- Excludes: `HOLD`, `UNCERTAIN`, personal workflow, money-management and EA-management material.
- Important: this is a **derived project specification**, not a replacement for the original source files and not an independent claim of publication/authorship provenance.
- Every material rule must remain traceable to its evidence layer and/or an explicit reconciliation decision.

This canonical file is the preferred **developer-facing Core rule reference**. Original PDFs, Finale transcripts, workbook provenance/audit records, rule extractions and conflict registers remain the evidence/provenance layer behind it.

## Primary operational reference
### Oma ally BBMA - AL.pdf
- Project role: **PRIMARY OPERATIONAL BBMA REFERENCE**
- Repository path: `docs/references/original/Oma ally BBMA - AL.pdf`
- Storage status: **ORIGINAL BINARY STORED IN REPOSITORY**
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
- Repository path: `docs/references/original/BBMA technique.pdf`
- Storage status: **ORIGINAL BINARY STORED IN REPOSITORY**
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
- Repository archive: `docs/references/original/video/oma_ally_finale/`.
- Storage status: **ALL 7 ORIGINAL SRT FILES ARCHIVED / HASH VERIFIED**.
- Provenance status: **USER-SUPPLIED / USER-IDENTIFIED ATTRIBUTION; NOT INDEPENDENTLY AUTHENTICATED FROM THE SRT FILES ALONE**.
- User validation status: **V01–V07 confirmed usable/OK**.
- Processing status: original SRT evidence is archived byte-for-byte; corrected, extracted-rule and summary artifacts were prepared separately; derived Markdown analysis is committed under `docs/references/video/oma_ally_finale/`.
- Original/corrected SRT hashes and synchronization status are recorded in `docs/references/video/oma_ally_finale/VIDEO_SOURCE_INDEX.md`; the immutable original archive manifest is `docs/references/original/video/oma_ally_finale/MANIFEST.md`.

### Reconciled Finale findings
After comparing Finale against the current PDF-derived Core contracts, most important Finale statements are corroboration/clarification rather than brand-new Core rules:
- expanding/directional BB is already part of current momentum/CSM semantics; Finale strongly confirms that flat-BB outside closes are not momentum;
- the existing Extreme source contract already knows reversal + retest before standalone entry; Finale adds richer timing/context but leaves several exceptions unresolved;
- normal Extreme TP Wajib is clarified more specifically toward the opposite MA5/MA10 area, with Mid BB as farther context;
- MHV/MLV retest, validity and morphology are explained more richly and expose active M09 implementation gaps;
- eCSD vs CSD and the non-executability of raw direction signals are strongly corroborated;
- first-Re-Entry-candle validation / second-candle entry is treated as a semantic/timing verification item;
- higher-timeframe Re-Entry / lower-timeframe completion context is emphasized without changing the exact PDF-derived REM/RRE/REE signatures.

Unresolved items remain in `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`. Active code mismatches are separated into `BBMA_FINALE_CORE_IMPLEMENTATION_GAP_REGISTER.md`.

The Finale material does **not automatically override** the established PDF contracts. A source clarification and an implementation fix are deliberately treated as separate decisions.

## Product-linked supplemental source
### BBMA Home Course Workbook — Tier B / strong-provenance copy
- Artifact reviewed: 19-page `BBMA Home Course Workbook` PDF supplied by the user.
- Authentication record: `blueprint/CORE_V2_F7_WORKBOOK_AUTHENTICATION_AUDIT_20260824.md`.
- Classification: **TIER B / STRONG-PROVENANCE COPY — NOT TIER A AUTHENTICATED ORIGINAL**.
- Important provenance limit: the reviewed binary came through a third-party distribution path and has not been hash-matched to a purchaser-preserved or official-distribution original.
- Use rule: workbook material may strengthen or clarify Strategy Core only after explicit cross-source reconciliation; workbook-only statements do not silently override the primary PDF.

High-value reconciled findings include:
- strong corroboration of the recurring `Re-Entry -> Momentum -> Re-Entry` lifecycle;
- strong product-linked evidence for `Re-Entry -> no Momentum -> TP/close` as a lifecycle principle after explicit F7 reconciliation;
- D1/MA50 major-trend hierarchy evidence that, when reconciled with the primary PDF's price-side + MA50-slope rule, establishes D1 as strategic direction authority over a conflicting H4 local/setup condition.

D1 reconciliation records:
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`;
- `blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- `blueprint/CORE_V2_D1_CANONICAL_CONTRACT_RECONCILIATION_AUDIT_20260824.md`.

## Source precedence / conflict policy
1. `PROJECT_INSTRUCTIONS.md` governs project scope and change-control rules.
2. The original user-supplied BBMA source documents remain the evidence layer governing BBMA Core semantics.
3. `Oma ally BBMA - AL.pdf` remains the primary operational reference because it contains the more explicit cycle, four Re-Entry types, MLV/CSD relationships and REM/RRE/REE contracts.
4. `BBMA technique.pdf` remains the historical/secondary corroborating reference.
5. BBMA Finale V01–V07 is supplemental instructional/clarification evidence. It may strengthen, clarify or expose gaps but must not silently overwrite an established PDF rule.
6. The Tier-B Home Course Workbook is product-linked supplemental evidence. It may enter accepted Core only through an explicit reconciliation that remains compatible with higher-precedence evidence.
7. `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` is the canonical **derived developer-facing consolidation** of accepted reconciled rules.
8. If sources conflict, **do not silently choose or merge rules**. Record the contradiction and resolve it explicitly in a decision/audit/source-conflict record.
9. Master Blueprint code/specification must never override a clearly supported BBMA Core source rule merely because the current implementation behaves differently.
10. Project-reference status does not imply independent authentication of authorship or publication provenance.

## Current implementation relevance
The canonical V2 Core preserves the previously reconciled contracts, including:
- Type 1: MA5/10 High resistance for sell in an uptrend; MA5/10 Low support for buy in a downtrend.
- Type 2: MA5/10 and MID BB meet/collide; strongest when MA50 also meets; minimum 3 candles per timeframe.
- Type 3: CSM forms, then price reverses/retraces to MA5 or MA50 for Re-Entry setup.
- Type 4: CSD forms, then price gyrates/retraces toward MA5/10.
- REM: H4 Re-Entry + H1 Extreme + M15 MHV/MLV structure.
- RRE: D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE: D1 Re-Entry + H4 Extreme + H1 Extreme.
- D1 major-trend strategic owner: confirmed only when closed D1 price side and MA50 slope agree; transition/unresolved blocks new entries.
- H4 remains immediate structural/setup parent for standalone H1 but cannot override D1 strategic direction.
- D1 strategic gating is separate from REM/RRE/REE component signatures.

Post-source implementation mismatches must be handled through the implementation-gap / decision / queue process and subsequent blueprint/code audit. They must not be confused with source-of-truth changes.

## Source-integrity controls
For every material Strategy-Core change or compliance audit:

- begin from this index rather than ad-hoc search;
- retrieve the canonical V2 Core and relevant original/Finale/workbook evidence;
- check conflict/HOLD status before encoding logic;
- distinguish source clarification from implementation correction;
- trace the accepted rule to its owning module and code behaviour;
- do not ask the user to repeatedly re-establish that BBMA/Oma Ally fidelity is required — it is permanent project governance under `PROJECT_INSTRUCTIONS.md`.

## File-storage note
The two original user-supplied PDF binaries are preserved in GitHub under `docs/references/original/` with their original filenames. Their SHA-256 hashes above remain the integrity reference and must continue to match the archived binaries.

All seven original BBMA Finale SRT files are preserved in GitHub under `docs/references/original/video/oma_ally_finale/` with their original supplied filenames and verified hashes.

The reviewed Tier-B Home Course Workbook is currently represented in GitHub by its authentication/reconciliation records; do not relabel it as an original Tier-A archived source unless a purchaser-preserved/official binary provenance chain is later established and recorded.

The GitHub connector used by ChatGPT exposes UTF-8 text writes but no mounted/local-file upload parameter, so future binary/local-file source additions may require manual upload to the repository. Derived analysis Markdown can be committed directly to GitHub.
