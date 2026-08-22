# BBMA Finale Processing Notes

## Objective
Convert the seven user-confirmed BBMA Finale subtitle files into a traceable Strategy Core evidence set without destroying the original transcripts or silently changing BBMA rules.

## Transcript correction method
The corrected SRTs are text-based corrections, not a new audio transcription. Timestamps and subtitle block structure are preserved. Corrections are intentionally conservative and focus on recurrent ASR errors where BBMA context is strong, including examples such as Bollinger Band/BB, Mid BB, MA5/MA10, H4/H1, Re-Entry, MHV, TP Wajib, candle arah and stop loss.

Ambiguous phrases are deliberately left imperfect rather than guessed. Therefore:
- `original.srt` = evidence of the supplied transcription;
- `corrected.srt` = easier-to-read technical normalization;
- `extracted_rules.md` = curated meaning-level extraction;
- neither subtitle file is a substitute for re-listening to audio when a rule is disputed.

## Classification vocabulary
- **ADD** — deterministic/core detail not currently explicit enough in the Core baseline.
- **CORRECT** — current interpretation/implementation is too broad, too narrow or otherwise inconsistent with stronger source evidence.
- **CLARIFY** — existing Core is broadly right; Finale adds precision/context.
- **KEEP** — current rule is corroborated with no material change.
- **REJECT** — statement should not enter universal Strategy Core, usually because it is personal workflow, risk management, statistics, qualitative emphasis or outside Core.
- **UNCERTAIN / HOLD** — source conflict, transcript ambiguity or insufficient deterministic criteria; no Core change until resolved.

## Source hierarchy used for this ingestion
Existing project governance remains intact. The current user-supplied PDFs remain the established operational references. The Finale class is added as a high-value instructional/clarifying source. Where Finale and an existing reference appear to conflict, the conflict is recorded rather than silently resolved.

## Core-only boundary
The final before-vs-after comparison intentionally excludes EA management and non-Core mechanics such as money management, lot sizing, portfolio controls, scheduler, trade lock, spread handling, broker logic, dashboard, logging and execution plumbing. Personal risk-management commentary in V07 is also excluded from Strategy Core unless independently corroborated as a BBMA Core law.
