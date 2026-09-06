# Oma Ally BBMA YouTube — video-by-video source audit

Date started: 2026-09-06
Source: https://www.youtube.com/@bolingerband5025
Status: ACTIVE SOURCE AUDIT

## Evidence policy

No automatic transcript is accepted as strategy authority by itself.

Status ladder:
1. `PENDING` — source not yet processed.
2. `SOURCE-DOWNLOADED` — original audio captured from YouTube.
3. `ASR-DRAFT` — machine transcript generated; not authoritative.
4. `AUDIO-CHECKED` — uncertain/critical segments checked against original audio.
5. `VERIFIED` — transcript context, timestamps, BBMA terminology, rule/exception/example mapping, and contradictions have been reviewed sufficiently to use as source evidence.

Only `VERIFIED` material may be promoted into blueprint/EA strategy authority.

## Accuracy method

- Primary ASR: `whisper.cpp` with `ggml-large-v3-turbo-q5_0` (not tiny/base).
- Spoken language is transcribed, not translated, to preserve BBMA terminology.
- Maintain timestamps.
- Flag low-confidence or semantically suspicious segments.
- Re-listen to every segment that contains a strategy rule, exception, timeframe dependency, lifecycle transition, invalidation, SL/TP rule, or unclear BBMA term.
- Cross-check repeated claims against later videos before declaring them universal rules.
- Keep examples separate from universal requirements.
- Record contradictions instead of silently choosing one interpretation.

## YouTube inventory and audit order

| Audit # | YouTube ID | Title | Duration | YouTube auto-caption | Status |
|---|---|---|---:|---|---|
| 01 | `pU9E_ckLtkI` | 1. Oma Ally BBMA Intensive Day 1 Video 1 | 1:54:45 | No | SOURCE-DOWNLOADED / transcription setup |
| 02 | `hq44GaNaW4c` | 2. Oma Ally BBMA Intensive Day 1 Video 2 | 1:57:26 | No | PENDING |
| 03 | `dm04snPxet8` | 3. Oma Ally BBMA Intensive Day 1 Video 3 | 47:26 | No | PENDING |
| 04 | `_kCE3vd9bPk` | Oma Ally BBMA Intensif DVD 2 Day 1 Video 03 | 44:10 | Yes | PENDING |
| 05 | `8dCN4zoVrtA` | Oma Ally BBMA Intensif DVD 2 Day 1 Video 04 | 1:57:37 | No | PENDING |
| 06 | `lN_yPAKHiL4` | 5. Oma Ally BBMA Intensive Day 2 Video 1 | 1:26:25 | No | PENDING |
| 07 | `7-rc0D_Fqe0` | 6. Oma Ally BBMA Intensive Day 2 Video 2 | 1:26:49 | No | PENDING |
| 08 | `zywjq6rBr0M` | Oma Ally BBMA Intensif DVD 2 Day 2 Video 02 | 1:27:31 | No | PENDING |
| 09 | `jdghjcQwa_4` | Oma Ally BBMA Intensif DVD 3 Day 2 Video 03 | 1:24:40 | No | PENDING |
| 10 | `4IEAEkTZ2lU` | Oma Ally BBMA Intensif DVD 3 Day 2 Video 04 | 1:37:49 | No | PENDING |
| 11 | `RU_Zz7mIDDU` | Oma Ally BBMA Intensif DVD 3 Day 2 Video 05 | 1:45:27 | No | PENDING |
| 12 | `W1RCxzpznBA` | Oma Ally BBMA Intensif Day 3 VIDEO 01 | 1:13:26 | No | PENDING |
| 13 | `6kdBxqFDZEI` | Oma Ally BBMA Intensif Day 3 VIDEO 02 | 24:27 | Yes | PENDING |
| 14 | `XkcNUPb-8Aw` | Oma Ally BBMA Intensif Day 3 VIDEO 03 | 47:51 | Yes | PENDING |
| 15 | `M-G4bItJ4cA` | Oma Ally BBMA Intensif Day 3 VIDEO 04 | 31:07 | Yes | PENDING |

## Current local evidence

- Channel inventory refreshed directly from YouTube with yt-dlp 2026.08.19.
- Subtitle inventory checked for all 15 videos.
- Exactly four videos expose YouTube automatic captions: `_kCE3vd9bPk`, `6kdBxqFDZEI`, `XkcNUPb-8Aw`, `M-G4bItJ4cA`.
- The other eleven have no YouTube subtitle or automatic-caption track.
- Video 01 original 127 kbps m4a audio has been downloaded locally and converted to 16 kHz mono WAV for transcription.

## Promotion rule

Do not modify EA strategy logic merely because an ASR draft appears to say something. A source statement must survive audio checking and context review first. When a video becomes `VERIFIED`, record its timestamped rule map in a dedicated audit file before reconciling it against the current blueprint/source.
