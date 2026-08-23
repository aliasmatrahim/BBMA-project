# P3-FINAL-DELTA R1 — Strategy Lifetime Source Resolution

Date: 2026-08-23  
Branch: `blueprint-dev`  
Status: **SOURCE RESOLUTION COMPLETE — NO CODE PATCH IN THIS RECORD**

## Purpose
Resolve the two timer-related findings from `P3_FINAL_DELTA_P0_P3_POST_SOURCE_EXPANSION_REVALIDATION.md` before any repair is attempted:

1. Extreme component lifetime currently controlled by `MaxWaitBars_Extreme`.
2. Re-Entry Type 2/3/4 lifetime currently controlled by `MaxWaitBars_ReEntry`.

Mandatory evidence group: primary/secondary PDF digest, BBMA Finale V01–V07, relevant forum corroboration, canonical Core V2.

---

## 1. Extreme lifetime

### Source-supported lifecycle
Accepted evidence supports:

`RAW EXTREME -> REVERSAL-CONFIRMED -> optional reversal continuation -> RETEST PHASE -> RETEST/ENTRY-READY`

with structural failure/termination through:
- accepted outside-BB close / Momentum behavior -> `VOID`;
- opposite reversal-confirmed Extreme on the same source timeframe -> old-cycle `SUPERSEDED` / cycle restart.

Finale V04/V05 explicitly teaches that the retest may span multiple candles; it does not establish a universal fixed maximum number of bars. The source examples mention two/three candles descriptively, not as a hard expiry. Core F2 explicitly forbids inventing arbitrary candle-count lifecycle rules.

### R1 verdict — Extreme
**REJECT GENERIC FIXED AGE EXPIRY AS STRATEGY AUTHORITY.**

`MaxWaitBars_Extreme` has no accepted PDF/Finale/forum basis as a universal Extreme death rule and must not invalidate a still-structurally-valid Extreme component solely because age elapsed.

Approved lifetime principle for repair:
- M08/F2 structural state owns Extreme validity;
- outside-BB/Momentum invalidation owns `VOID`;
- opposite reversal-confirmed Extreme owns cycle `SUPERSEDED`;
- M16 may verify exact current owner identity, but must not add an independent age-based Strategy-Core death rule.

---

## 2. Re-Entry Type 2 lifetime

### Source-supported structure
Type 2 / Powerful Re-Entry requires:
- MA5/MA10 + Mid BB confluence/collision;
- MA50 confluence is the stronger form;
- minimum three candles on the relevant timeframe.

The source defines the minimum formation requirement but does **not** define a universal five-bar expiry.

The existing code already has a source-consistent structural candidate failure: if the required Type-2 confluence breaks before confirmation, the candidate resets.

### R1 verdict — Type 2
**REJECT GENERIC `MaxWaitBars_ReEntry` EXPIRY.**

Candidate validity should be controlled by whether the Type-2 confluence/owner structure still exists, not by an unrelated five-bar timer.

---

## 3. Re-Entry Type 3 lifetime

### Source-supported structure
Type 3 sequence:

`CSM -> later retrace/reversal to MA5 or MA50 -> Re-Entry`

Finale/PDF evidence does not specify that the retrace must occur within five bars.

General Re-Entry validity also requires that price not clear/close through the relevant MA5/MA10 structure against the intended setup direction. Opposite authoritative BBMA direction/cycle evidence can supersede the old context.

### R1 verdict — Type 3
**REJECT GENERIC `MaxWaitBars_ReEntry` EXPIRY.**

The candidate remains a structural CSM-owned setup only while that source context remains valid. Exact code transition rules must use existing BBMA owner/invalidation events, not another numerical timer.

---

## 4. Re-Entry Type 4 lifetime

### Source-supported structure
Type 4 sequence:

`CSD -> later gyration/retrace to MA5/MA10 -> Re-Entry`

No accepted source establishes a five-bar expiry.

The setup must fail/reclassify when its source direction/MA close-side structure is invalidated or an authoritative contradictory cycle takes ownership.

### R1 verdict — Type 4
**REJECT GENERIC `MaxWaitBars_ReEntry` EXPIRY.**

Use structural owner/invalidation transitions rather than elapsed-candle age.

---

## 5. Confirmed Re-Entry provenance
The source describes repeated Re-Entries during an ongoing BBMA cycle and uses higher-timeframe Re-Entry as a component of REM/RRE/REE. Therefore a confirmed Re-Entry must not disappear from combination provenance merely because an arbitrary project timer elapsed while the owning structure remains authoritative.

Repair principle:
- a newer source-valid Re-Entry on the same owner slot may replace/supersede the older exact snapshot;
- opposite authoritative cycle/owner handover may invalidate old current-cycle authority;
- explicit source-valid structural failure may reset the setup;
- age alone is not Strategy-Core invalidation.

This is a source-derived owner/provenance principle. Exact bookkeeping is project engineering and must remain fail-closed when ownership cannot be proved.

---

## 6. Forum corroboration checked
Relevant ForexFactory BBMA discussions corroborate:
- Extreme requires reversal/retest and can develop over multiple candles;
- MHV/Extreme lifecycle is structural rather than fixed-bar timed;
- Re-Entry follows direction and retracement into the MA zone;
- multi-timeframe R/E/M structures may remain relevant across different source-timeframe durations.

Forum evidence is corroborating only and does not create the no-timer rule by itself. The no-timer verdict follows primarily from the absence of a source TTL plus the explicit structural lifecycle now locked in PDF+Finale Core.

---

## 7. Repair authorization produced by R1
The following code changes are now evidence-authorized for the later consolidated repair pass:

1. remove `MaxWaitBars_Extreme` from active Strategy-Core validity decisions;
2. remove generic `MaxWaitBars_ReEntry` expiry from Type 2/3/4 candidate/confirmed validity;
3. preserve source-defined structural invalidation/reset/supersession;
4. keep any age field only for diagnostics if useful, never as entry authority;
5. update M08/M12/M16 contracts after code repair;
6. rerun Mode 1, Mode 2 and purity regression.

Do **not** replace `5` with another tuned number.

## Final R1 result
**SOURCE RESOLUTION PASS.**

The current fixed-bar Extreme and Type2/3/4 Re-Entry expiry mechanisms are not supported as BBMA Strategy-Core rules and are authorized for removal/replacement by structural ownership logic in the repair pass.
