# Custom MTF — source discriminator and recovery-epoch retrieval, 2026-11-10

Task: pending C / T04-D mapping and T04-B/E owner-epoch evidence. Branch feat/custom-mtf-v1-20261108. Base f71b574ece3f07f6134ae0951351b178e969ffd7, Build6.06 source SHA0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e. Publication SHA in Draft PR303.

## Result

Retrieval progressed; neither semantic exit criterion passes. Both remain HOLD/VERIFICATION REQUIRED. No production/test code, detector, alias, recovery rule or availability changed. Auto-entry/all77 cells OFF. No merge/deployment/trading.

| Requested proof | Newly retrieved evidence | Limit / ruling |
|---|---|---|
| Labelled candle separating body-cross from close-side | Eight original V05 frames decoded at1885,1892,1900,1925,1935,1950,1960,1966 seconds; five visually reviewed at1892/1935/1950/1960/1966. One archived1966 frame, full hashes/inventory retained | No numeric discriminator accepted. Screens show M15 to H1 context changes, not an unambiguous labelled candle with all required indicator/open/close identities. |
| Actual owner-epoch history | Read-only bounded discovery across four listed roots:3904 file names scanned,210 candidate records hashed/marked; selected current manifests and two historical records reviewed | Candidate indexing is not full semantic review of all210 files, and not a G40-wide absence proof. No accepted historical M08/M09 epoch checkpoint recovered from reviewed records. |
| Historical epoch record | N1_P1_BUILD508 EPOCH_R1_ANALYSIS.json records real D1 directional-owner observations/epochs | This is M11 strategic ownership. It cannot initialize M08/M09 structural lifecycle, parent anchors or replay cursor. |
| File named snapshot | Q10_R3_METAQUOTES_20260923/state_snapshot.json | Build5.11 validation-stage/deployment identity record, not a serialized6.06 M08/M09 source owner. Filename does not establish authority. |
| Contemporary actual-controller state | First unseeded6.06 controller cycle has all16 M08 raw/M09 parent anchor fields zero across D1/H4/H1/M15, both directions | An initialized zero is not authenticated historical NONE. Nonzero M12 update times cannot establish the missing M08/M09 epoch. Seeded3/3 handovers remain fixture mechanics only. |

## Source example: why the new frame does not decide A/B

Original V05 subtitles at32:36-32:50 discuss sell/early direction and close beyond MA5/MA10. In the32:40 and32:46 frames, the cursor/tooltip concerns2016.01.07 10:00 on the H1 chart. The bottom OHLC display reads approximately O1.07831/C1.08125, a BUY body, while the spoken discussion concerns SELL. These pixels are observations, not a machine-verified numeric price series. The speaker may be referring to a neighbouring candle; hover position alone does not establish the labelled signal candle. Thus do not apply the spoken sell label to that hovered BUY candle, infer a counterexample, or silently select close-side semantics. The BB tooltip also does not establish every MA level for the intended candle.

The already accepted distinction between source wording and project engineering body-span mapping remains. The user's MidBB CSA definition must not be silently aliased to MA-only eCSD. Founder/classification example and exact event maturity remain unresolved.

## Epoch evidence boundary

A qualifying record must identify the same actual symbol/feed/history revision, source TF, source candle/replay cursor, full existing M08 and both M09 owners (and M12 where required), the parent-cycle origin and how that origin was established. It must precede the target recovery range and preserve every intervening accepted source event. This is an engineering evidence checklist, not a new BBMA rule.

Native replay code requires exact existing source anchors and nominal contiguous bars. The historical July31-August3 session classification is still not authenticated. Neither M11 OwnerEpochStart nor trade-specific C044 EpochAnchorCandle is a substitute for the M08/M09 epoch. Do not initialize NONE from an arbitrary first loaded bar or promote a fixture seed to a genuine checkpoint.

## Verification and provenance

source_epoch_followup606_inventory.json contains bounds,210 candidate-file hashes/markers and eight frame hashes. source_epoch_followup606_evidence.json binds16 zero-anchor trace rows and the two historical records. Remote and local historical JSON contents compare equal; raw byte hashes differ and are deliberately recorded separately, not falsely labelled byte-identical. Initial exact-byte assertion failed; JSON-content comparison established the permitted semantic equality without overwriting either artifact.

Archived frame SHA is checked against the G40 extractor inventory; original videos are unchanged. Decode used installed ffmpeg with -ss SECOND -frames:v1 -q:v2, original V05 input, no video editing. Source-video attribution/provenance limits from the previous source registry still apply.

No EA or test changes: strict native compile/regressions and final cloud75/75 remain exact-source historical evidence; they were not rerun merely for these evidence/doc additions. Fresh validation checks frame SHA, JSON schemas/content, source SHA,16 trace rows and diff integrity. No new native/runtime/recovery PASS is claimed.

## Exact next action

C: inspect a discriminating source window with the explicitly identified signal candle and all MA/Mid levels, rather than equating hover position with the spoken label. The32:36-32:50 example is excluded as a numerical discriminator until candle attribution is resolved; no repeated extraction of these same frames is needed.

B/E: acquire or construct a source-proven cycle-origin checkpoint using the existing canonical engines on authenticated same-feed history, then bind the full owner snapshot before a controlled restart and compare continuous-vs-recovered owners. The origin must first be justified by source-valid lifecycle/reset evidence; arbitrary NONE startup is not adequate. Authenticating historical session/UTC boundaries remains a separate prerequisite for crossing the weekend. A new trusted snapshot cannot be supplied by renaming the M11/C044 records found here.

Do not advance T04-F or T05 until those exits pass. The retrieval substep is recorded; the requested semantic/epoch gates remain unresolved.
