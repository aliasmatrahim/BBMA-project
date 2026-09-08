# Primary-15 Engine Consistency Audit — 2026-09-08

Status: **SOURCE EXTRACTION / ASR-DRAFT ONLY**. No Strategy-Core promotion and no EA source change.

## Source-policy boundary
`docs/references/SOURCE_INDEX.md` remains authoritative for source precedence. Primary-15 YouTube/ASR material is supplementary evidence under review; it cannot silently override the primary PDF, accepted Finale evidence, reconciled Tier-B workbook findings, conflict/HOLD registers or accepted Core V2.

## Production re-transcription profile
Current consistency target:
- engine: `faster-whisper`;
- model: `standard-large-v3-turbo-ct2`;
- compute: CPU `int8`, 2 threads;
- beam size: 5;
- language: Malay (`ms`);
- VAD: false;
- chunk size: 600 seconds;
- BBMA terminology prompt retained.

## Current coverage
- Videos 12–15 / Day-3 selective set: **COMPLETE** with the production profile. Example video 12 manifest records 8 chunks / 4405.134 sec, completed 2026-09-08 05:18:51 +08:00.
- Videos 05–11: **IN PROGRESS** under `remaining_primary_faster_transcribe.py`; video 05 was at 2/12 chunks in the latest sampled log.
- Videos 01–04: older `ASR-DRAFT` material exists from `ggml-large-v3-turbo-q5_0.bin`, but that is not the same production-engine lineage.

## Consistency correction prepared
A separate `primary15_reprocess_01_04_faster.py` has been prepared to re-transcribe videos 01–04 with the same faster-whisper production profile while preserving the prior transcripts.

A lightweight waiter `wait_then_reprocess_01_04.ps1` is running. It starts videos 01–04 only after the videos 05–11 log emits `PRIMARY15_REMAINING_COMPLETE`, preventing two CPU-heavy transcription pipelines from running concurrently.

## Claim boundary
Until all 15 videos have same-engine manifests and the resulting drafts receive semantic/visual review:
- do **not** claim Primary-15 transcription is uniformly complete;
- do **not** treat ASR output as verbatim source where wording is uncertain;
- do **not** promote a new BBMA rule from noisy/ambiguous ASR;
- use `MATCH / PARTIAL / MISSING / CONFLICT` during reconciliation and retain ambiguity as pending evidence.

## Next evidence sequence
1. finish videos 05–11;
2. automatically reprocess videos 01–04 with the same engine;
3. verify manifests/chunk completeness for videos 01–15;
4. perform targeted semantic review starting with Day-3 Extreme/MHV/Re-Entry/CSA-CSAK/Momentum/F7-relevant passages;
5. cross-check each material statement through current `SOURCE_INDEX.md` before any accepted-Core decision.
