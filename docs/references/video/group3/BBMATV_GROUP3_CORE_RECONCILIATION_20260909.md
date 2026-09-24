# BBMATV Group-3 → Strategy Core Reconciliation

**Record date:** 2026-09-09  
**Scope:** video-evidence reconciliation only.  
**Authority:** `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` remains the accepted Core. Group-3 videos corroborate, clarify, or expose an unresolved point; they do not amend the Core or EA.

## Method and guardrails

- Evidence uses the archived `FINAL_CORRECTED.srt`; original `ASR_DRAFT.srt` remains preserved.
- Only an intelligible, timestamped statement is used. Garbled or competing audio remains `UNCLEAR`.
- `MATCH` means the stated proposition agrees with an existing Core proposition.
- `PARTIAL` means it supports part of the Core but omits a required guard or is too broad to become an operational rule.
- `UNCLEAR` means the audio is unreliable or the statement conflicts with the current accepted Core; it has no rule authority.
- No strategy rule, source-precedence rule, implementation, test, or runtime setting changes are made by this record.

## Reconciliation

| ID | Group-3 evidence | Core comparison | Status | Result |
|---|---|---|---|---|
| G3-EXT-001 | **Extreme** — [yEQNXorLJiU](https://www.youtube.com/watch?v=yEQNXorLJiU), 00:00:49–00:02:26. “MA keluar daripada BB … extreme”; then reverse candle, body marking and retest. | Core §5.1 and §5.4 require the MA-outside condition, reversal confirmation, frozen body/MA5 reference and later retest for standalone Extreme maturity. | **MATCH** | Corroborates the accepted Extreme lifecycle. It does not replace the Core's precise closed-candle and invalidation guards. |
| G3-MHV-001 | **MHV** — [cYjUO0rxuZ0](https://www.youtube.com/watch?v=cYjUO0rxuZ0), 00:00:25–00:01:40. “Setelah Extreme TP wajib … MHV”; candles inside BB, reverse candle and retest at reverse candle or MA5/MA10. | Core §6.2–§6.5 defines the prior Extreme → TP-Wajib → MHV/MLV parent chain, inside-BB loss-of-momentum context and frozen marked-body/MA retest concept. | **MATCH** | Corroborates MHV as a setup/context stage, not standalone execution authority. |
| G3-MTF-001 | **Structure & Re-entry** — [VMDF27J0MxU](https://www.youtube.com/watch?v=VMDF27J0MxU), 00:02:07–00:04:59. “extreme, TT wajib, MHV, CSAK, … re-entry, … momentum”; H4 Re-entry is illustrated with lower-TF structure. | Core §3 establishes the same ordered cycle. Core §6.5 and Source Index define the accepted REM signature: H4 Re-Entry + H1 Extreme + M15 MHV/MLV. | **MATCH** | Supports multi-timeframe structural completion. It does not create new combinations or execution authority. |
| G3-BB-001 | **Bollinger Band** — [v42DSUA0GEY](https://www.youtube.com/watch?v=v42DSUA0GEY), 00:02:19–00:04:04. Outside-BB close is described as market strength; close through Mid BB as direction change. | Core §4 accepts outside close only with expanding/directional BB for Momentum/CSM; it explicitly rejects a lone outside close with flat BB. Direction detection is not direct execution authority. | **PARTIAL** | The clip supports BB context and Mid-BB direction framing, but omits the BB-expansion guard and execution boundary. |
| G3-MA50-001 | **MA50** — [azwd9X-blVg](https://www.youtube.com/watch?v=azwd9X-blVg), 00:00:32–00:05:54. MA50 is used to view trend; H4-to-M1 is called current trend and D1/W1/MN major trend. | Core §2 accepts MA50 as structural/trend reference. The project’s operational owner hierarchy is D1 → H4 → H1 → M15; it does not promote W1/MN from this clip. | **PARTIAL** | Supports MA50 trend framing only. It cannot change the accepted timeframe-owner hierarchy. |
| G3-CSAK-001 | **CSAK / CSM / Re-entry** — [sZ_ib-DyOqQ](https://www.youtube.com/watch?v=sZ_ib-DyOqQ), 00:00:30–00:02:02. The intelligible portion describes a direction-change signal crossing MA5, MA10 and Mid BB. | Core §7 distinguishes eCSD/CSD direction stages and §3 says raw direction is not direct execution authority. | **PARTIAL** | Corroborates direction-stage language only; no direct-entry interpretation is accepted. |
| G3-MA5-001 | **MA5 High & Low** — [NaoTb0HG7lE](https://www.youtube.com/watch?v=NaoTb0HG7lE), 00:00:40–00:04:02. MA5 High sell is said to work in downtrend; MA5 Low buy in uptrend. | Source Index “Current implementation relevance” records Type 1 differently: MA5/10 High sell resistance in an uptrend; MA5/10 Low buy support in a downtrend. | **UNCLEAR** | Direct conflict with accepted Core wording. No reconciliation, rule change, or implementation change is made here; source-conflict review would require separate authoritative evidence. |
| G3-AUDIO-001 | **CSAK / CSM / Re-entry** — [sZ_ib-DyOqQ](https://www.youtube.com/watch?v=sZ_ib-DyOqQ), 00:02:02–00:03:20. Several phrases remain corrupted after alternate audio recheck, including the claimed entry sequencing. | No reliable proposition is available for comparison. | **UNCLEAR** | Excluded from rule evidence. Preserve the transcript and recheck queue; do not infer an entry rule. |
| G3-AUDIO-002 | **Structure & Re-entry** — [VMDF27J0MxU](https://www.youtube.com/watch?v=VMDF27J0MxU), 00:00:57–00:02:07. The term transcribed as “DB Mendata” is unresolved. | No accepted Core term can be mapped safely. | **UNCLEAR** | Excluded from rule evidence. No terminology substitution is permitted. |

## Outcome

- **MATCH:** 3
- **PARTIAL:** 3
- **UNCLEAR:** 3
- **New Core rules:** 0
- **EA/source/runtime changes:** 0

## Evidence locations

Each cited video retains its local immutable original ASR draft and its derived corrected transcript under:

`D:\BBMA_SOURCE_AUDIT_VIDEOS\group3_bbmatv_48\<YouTube-ID>\transcript\`

This record is the GitHub reconciliation index; transcript material remains evidence, not a replacement for the primary PDF or accepted Core.