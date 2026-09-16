# Q5 — A4/A5 Semantic Resolution

Date: 2026-09-16
Issue: #169
Branch: `audit/q5-semantic-resolution-169`
Base: `d1-owner-dev@ea4c48262c4bb058e375fb9a1b564fa132ba578b`
Status: RESOLUTION COMPLETE / VALIDATED / CANONICAL MERGE PENDING

## Scope and authority

This report resolves the retained A4/A5 `6 UNCLEAR + 3 PARTIAL` items at the Strategy-Core semantic layer only.
It does not rewrite uncertain transcripts, promote any item to `ACCEPTED_CORE`, modify Core/EA/contracts, or create a new BBMA rule.

Preflight followed live `SOURCE_INDEX.md`: accepted Core -> Finale evidence -> primary/secondary PDFs -> conflict/HOLD register -> A4/A5 evidence.
The active conflict policy requires unresolved or conflicting evidence to remain non-executable and forbids silent rule synthesis.

Source Autonomy explicitly separates processing/transcription quality from semantic disposition and supports `CORROBORATION_ONLY`, `REJECTED`, `PARTIAL`, `UNCLEAR`, `SOURCE_CONFLICT` and `ACCEPTED_CORE` as distinct states.

## New bounded evidence

Fresh YouTube automatic captions were downloaded to an isolated G40 folder without touching original media/subtitles.
Exact-window caption extraction summary SHA-256: `AA7407EC65D219CB37281139DB678B8CBB5DC49BFDDCF9B4B332256FCEDC9AF0`.
Visual spot frames were also extracted read-only for sZ, VMDF and W004; those frames are context only, not speech certification.
## Resolution table

| Item | Prior | Safe resolved proposition | Disposition | Core effect |
|---|---|---|---|---|
| d00Pm6BRL_8 W017 672.01–676.03 | UNCLEAR | Fresh `ms-orig` caption independently confirms the TP-Wajib / MHV sequence fragment already present in local ASR. | `CORROBORATION_ONLY` | None; existing cycle only |
| dZ6tmEwlrfA W038 1162.47–1166.21 | UNCLEAR | Fresh `ms-orig` caption confirms “subscribe/like/tekan loceng” call-to-action. | `REJECTED` | Non-Core commentary |
| qSoxRNSVwe4 W003 336.52–341.42 | UNCLEAR | Fresh `ms-orig` caption confirms introductory “kefahaman / heavy topic” metacommentary. | `REJECTED` | Non-Core commentary |
| QzGMRtkHwUw W026 899.38–903.08 | UNCLEAR | Fresh `ms-orig` caption confirms only a transition: “lepas tu kita pergi kepada Mid BB.” | `REJECTED` | Topic transition; no rule |
| sZ_ib-DyOqQ 122–126 | UNCLEAR | Surrounding stable cues state a direction change is only a direction change and does not yet establish movement strength; exact garbled noun remains excluded. | `CORROBORATION_ONLY` | Supports separation of direction signal from strength/momentum; no Boolean added |
| sZ_ib-DyOqQ 161–170 | PARTIAL | Stable phrase “Entrynya tetap pada candle 2” corroborates already-accepted first-validation / immediately-following-live-candle semantics; disputed first-candle wording remains excluded. | `CORROBORATION_ONLY` | No extra waiting candle or new timing rule |
| VMDF27J0MxU 57–74 | PARTIAL | Stable common denominator is a Re-Entry journey on a larger timeframe; disputed DB/BPM/TV term is excluded. | `CORROBORATION_ONLY` | Existing MTF Re-Entry context only |
| VMDF27J0MxU 108–115 | PARTIAL | Stable common denominator is lower-timeframe setups under a larger-timeframe context; disputed condition term is excluded. | `CORROBORATION_ONLY` | Existing HTF/LTF context only |
| 0XoRUraiyLk W004 107.82–125.06 | UNCLEAR | Duplicate attempts and source subtitle share H4 movement toward Top BB plus direction-change/signal context; conflicting opening/condition wording is excluded. | `CORROBORATION_ONLY` | Context only; no detector/filter authority |
## Why these can close semantically

The accepted Core already states that current unresolved BBMA Core semantic HOLD count is `0`.
It also states:
- eCSD/CSD expresses direction/intent and raw direction detection is not direct entry authority;
- first Re-Entry validation / immediately-following live-candle timing is closed at semantic/project-mapping level;
- higher-timeframe Re-Entry may be completed/read through lower-timeframe signal/setup structures.

Therefore these nine A4/A5 rows are evidence-quality/reconciliation artifacts, not authority to reopen an already-closed Core rule.
Where wording is incomplete, only the stable common denominator is retained as corroboration and every disputed condition is excluded.

## Residual transcript-QA notes

The following exact wording remains uncertain and must not be normalized into source text without better audio/caption evidence:
- sZ 122–126 garbled noun/strength phrase;
- sZ 161–170 first-candle wording beyond the stable second-candle statement;
- VMDF 57–74 DB/BPM/TV/BB term;
- VMDF 108–115 DB/Bibi term;
- W004 conflicting duplicate opening/condition wording.

These are transcript-QA residuals only. They do not carry executable authority and do not keep Strategy-Core semantic reconciliation open.
## Final semantic disposition totals

Prior retained state: `6 UNCLEAR + 3 PARTIAL`.
Resolved semantic state:
- `CORROBORATION_ONLY`: 6
- `REJECTED`: 3
- `UNCLEAR`: 0 at Strategy-Core semantic layer
- `PARTIAL`: 0 at Strategy-Core semantic layer
- `SOURCE_CONFLICT`: 0
- `ACCEPTED_CORE`: 0
- new rule / detector / filter / timing authority: 0

## Evidence integrity

Fresh caption hashes retained locally in the isolated resolution workspace include:
- d00 `ms-orig`: `0033EA58BB53EF8F987DF0E7EFA90DAF500972003908043D53023F91EFEE15AF`
- dZ `ms-orig`: `E53C86107CEBCAFF7256DA3D41EF178D13871D7A9BAF02DE35FCCCAFE05EABA9`
- qS `ms-orig`: `CCCFD2A2144794D749C6C86E688ACDBC8A14145211AA60969D86EF7FA8A3BD9E`
- Qz `ms-orig`: `370610CCBFB020551B03F685285C4B001192BD16DFE100630376F24948A32BDF`
- VMDF `id-orig`: `F187322C0251C72DDEE10F342B2483078D945AC4D338ECD591BAAF00F6753BB3`

YouTube caption download for sZ Malay was rate-limited (HTTP 429), and W004 exposes no automatic captions in its stored metadata. Neither failure was treated as evidence of absence or used to invent wording.

## Validation

- Resolution table contains exactly 9 retained A4/A5 rows.
- Final dispositions are exactly 6 `CORROBORATION_ONLY` + 3 `REJECTED`.
- `blueprint/source/BBMA_EA.mq4` blob is unchanged from the owner base (`6e629128f37c3fd482dd49e275360503f73fee68`).
- No Core rule, contract, EA source or runtime artifact is modified by this closure.
- Active-status reconciliation is limited to `CURRENT.md`, `MASTER_QUEUE.md`, `SOURCE_INDEX.md` and two stale branch-wording corrections in Finale governance documents.

## Decision

A4/A5 semantic reconciliation can close without Core or EA changes. Transcript-QA uncertainty remains preserved separately and may be revisited only if materially better source audio/caption evidence appears.
