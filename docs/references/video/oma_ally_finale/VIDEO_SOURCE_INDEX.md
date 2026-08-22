# BBMA Finale Video Source Index

## Status
**COMPLETE: V01–V07 received and user-confirmed OK.**

## Purpose
This source set preserves the BBMA Finale class subtitles and the derived BBMA Strategy Core analysis with full part-by-part provenance. Original subtitles are immutable. Corrected subtitles are conservative AI text normalization only; extracted rules and summaries are separate derived artifacts.

## Processing policy
1. Never overwrite `Vxx_original.srt`.
2. Keep each video separate; do not merge SRT files.
3. `Vxx_corrected.srt` preserves timestamps and corrects obvious ASR/BBMA terminology where context is sufficiently clear.
4. Ambiguous speech is not silently invented or resolved. A corrected SRT is **not audio-certified** because the processing basis is the subtitle text, not a fresh listen to the original audio.
5. `Vxx_extracted_rules.md` is the traceable Strategy Core extraction with timestamps and assessment.
6. `Vxx_summary.md` is the human-readable per-video conclusion.
7. Final Core decisions are made only in the master comparison/conflict files; a video statement does not automatically override the existing PDF references.

## Source files

| Part | Original filename | Entries | Approx end | SHA-256 original | SHA-256 corrected | Status |
|---|---|---:|---|---|---|---|
| V01 | `(srt-original-subtitles-multilingual)_bbma-finale-video-1-hd.srt` | 2336 | 01:08:30,000 | `993cad7bd58e54118f566a5ae7e73ee6dc608e798c671d5fff7d092e98452a4e` | `9aa290d71b4ce7c4706dbc04b57901508a07560452212883019a7812cc2901a3` | CONFIRMED OK |
| V02 | `(srt-original-subtitles-multilingual)_bbma-finale-video-2-hd.srt` | 1214 | 00:56:20,920 | `02d165b788867179f5a5f2f4bea787b56059dd72d8b84b3fd1ac1e9adcd0e0a2` | `d2f52dedba936d383103b6b4b3a0c10e65f282cd5d4a57f64d9f7d84634fbf6a` | CONFIRMED OK |
| V03 | `(srt-original-subtitles-multilingual)_bbma-finale-video-3-hd.srt` | 1383 | 00:55:45,000 | `142400c282db2dfda9bb41fba4022146c2e436f2c1a96bbf10a65a1b04a08228` | `0830ec5c71996db8935a8e7e458c2bac7d8648daf932b8b3c1d253f5e2c67684` | CONFIRMED OK |
| V04 | `(srt-original-subtitles-multilingual)_bbma-finale-video-4-hd.srt` | 1017 | 00:43:48,000 | `6b0c2ece21702e8f4c8494c54251ddd18d5db6a893fa197dc22a88dfcf9d4e9d` | `56e1be1ae4d19787ba2331635f8fe09f1e85f2c02a12fcef5783ff6c321345ac` | CONFIRMED OK |
| V05 | `(srt-original-subtitles-multilingual)_bbma-finale-video-5-hd.srt` | 1233 | 00:55:41,000 | `2abdc1d217932b0998483dbfb440a813207d3a51351b9cb7a0d461d834eecfbc` | `63a62df65bbb7cd9b5bade947c2b45e19a8d4c9a7186f2abd87f431713b76ee9` | CONFIRMED OK |
| V06 | `(srt-original-subtitles-multilingual)_bbma-finale-video-6-hd.srt` | 1334 | 01:01:35,640 | `7550eb8f05db83746cb60ee63836593acfb3da2c1d4a8334efb9b316a7615e62` | `f066dc164a3b3f3e1aae4f39de053f922be82243f22daf278621cf273dc7c537` | CONFIRMED OK |
| V07 | `(srt-original-subtitles-multilingual)_bbma-finale-video-7-hd.srt` | 1280 | 00:57:42,400 | `d16dca4690576afc7c9dce5f5f1975ff862c5b8fa513cec927b1a39938a5502f` | `f956ed910e0ae1032c33a8effdc5801f245ba420cbbd626cf4d5798f424ccb0b` | CONFIRMED OK |

## Artifact set per part
Prepared source pack for every `Vxx/` contains:
- `Vxx_original.srt` — immutable original.
- `Vxx_corrected.srt` — conservatively corrected subtitle.
- `Vxx_extracted_rules.md` — BBMA Strategy Core rules with timestamps.
- `Vxx_summary.md` — per-video summary/conclusion.

### GitHub synchronization status
The derived Markdown files (`extracted_rules` and `summary`) are committed in the corresponding `V01`–`V07` directories on `blueprint-dev`, together with the master analysis files below.

The GitHub connector available in this session accepts UTF-8 **text content** but does not expose a mounted/local-file upload parameter. Therefore the 14 full SRT files (7 original + 7 corrected) are preserved in the generated source pack with the hashes above and are **pending direct/manual GitHub file upload**. They must not be represented as already committed until that upload is completed.

## Master artifacts committed to GitHub
- `BBMA_FINALE_MASTER_RULE_INDEX.md`
- `BBMA_CORE_BEFORE_VS_AFTER_FINALE.md`
- `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`
- `PROCESSING_NOTES.md`
- `VIDEO_SOURCE_INDEX.md`
