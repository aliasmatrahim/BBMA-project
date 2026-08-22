# BBMA Finale Video Source Index

## Status
**COMPLETE: V01–V07 received and user-confirmed OK.**

## Purpose
This directory preserves the BBMA Finale class subtitles and the derived BBMA Strategy Core analysis with full part-by-part provenance. Original subtitles are immutable. Corrected subtitles are conservative AI text normalization only; extracted rules and summaries are separate derived artifacts.

## Processing policy
1. Never overwrite `Vxx_original.srt`.
2. Keep each video separate; do not merge SRT files.
3. `Vxx_corrected.srt` preserves timestamps and corrects obvious ASR/BBMA terminology where context is sufficiently clear.
4. Ambiguous speech is not silently invented or resolved. A corrected SRT is **not audio-certified** because the processing basis is the subtitle text, not a fresh listen to the original audio.
5. `Vxx_extracted_rules.md` is the traceable Strategy Core extraction with timestamps and assessment.
6. `Vxx_summary.md` is the human-readable per-video conclusion.
7. Final Core decisions are made only in the master comparison/conflict files; a video statement does not automatically override the existing PDF references.

## Source files

| Part | Original filename | Subtitle entries | Approx end time | Corrected text lines | SHA-256 original | Status |
|---|---|---:|---|---:|---|---|
| V01 | `(srt-original-subtitles-multilingual)_bbma-finale-video-1-hd.srt` | 2336 | 01:08:30,000 | 51 | `993cad7bd58e54118f566a5ae7e73ee6dc608e798c671d5fff7d092e98452a4e` | CONFIRMED OK |
| V02 | `(srt-original-subtitles-multilingual)_bbma-finale-video-2-hd.srt` | 1214 | 00:56:20,920 | 89 | `02d165b788867179f5a5f2f4bea787b56059dd72d8b84b3fd1ac1e9adcd0e0a2` | CONFIRMED OK |
| V03 | `(srt-original-subtitles-multilingual)_bbma-finale-video-3-hd.srt` | 1383 | 00:55:45,000 | 120 | `142400c282db2dfda9bb41fba4022146c2e436f2c1a96bbf10a65a1b04a08228` | CONFIRMED OK |
| V04 | `(srt-original-subtitles-multilingual)_bbma-finale-video-4-hd.srt` | 1017 | 00:43:48,000 | 60 | `6b0c2ece21702e8f4c8494c54251ddd18d5db6a893fa197dc22a88dfcf9d4e9d` | CONFIRMED OK |
| V05 | `(srt-original-subtitles-multilingual)_bbma-finale-video-5-hd.srt` | 1233 | 00:55:41,000 | 149 | `2abdc1d217932b0998483dbfb440a813207d3a51351b9cb7a0d461d834eecfbc` | CONFIRMED OK |
| V06 | `(srt-original-subtitles-multilingual)_bbma-finale-video-6-hd.srt` | 1334 | 01:01:35,640 | 49 | `7550eb8f05db83746cb60ee63836593acfb3da2c1d4a8334efb9b316a7615e62` | CONFIRMED OK |
| V07 | `(srt-original-subtitles-multilingual)_bbma-finale-video-7-hd.srt` | 1280 | 00:57:42,400 | 29 | `d16dca4690576afc7c9dce5f5f1975ff862c5b8fa513cec927b1a39938a5502f` | CONFIRMED OK |

## Artifact set per part
Each `Vxx/` directory contains:
- `Vxx_original.srt` — immutable original.
- `Vxx_corrected.srt` — conservatively corrected subtitle.
- `Vxx_extracted_rules.md` — BBMA Strategy Core rules with timestamps.
- `Vxx_summary.md` — per-video summary/conclusion.

## Master artifacts
- `BBMA_FINALE_MASTER_RULE_INDEX.md`
- `BBMA_CORE_BEFORE_VS_AFTER_FINALE.md`
- `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`
- `PROCESSING_NOTES.md`
