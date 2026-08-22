# CORE-V2-F7 — M17 SL/TP Provenance Audit

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **RE-AUDITED AGAINST FINALE V01–V07 / SOURCE-GOVERNANCE DECISION STILL REQUIRED / NO CODE BUG CLAIM**

## Scope
Determine whether the currently executable M17 SL/TP mapping can accurately be described as fully derived from the authoritative BBMA/Oma Ally Core sources, including the newer accepted Finale subtitle evidence V01–V07.

## Source-supported findings
The authoritative rule digest and Finale evidence strongly support normal **Extreme TP-Wajib** structure:
- SELL Extreme -> opposite MA5/MA10 Low area as the normal first mandatory objective;
- BUY Extreme -> opposite MA5/MA10 High area as the normal first mandatory objective;
- Mid BB is farther/max context.

The accepted Finale evidence also supports structural invalidation/exit ideas in specific contexts:
- V04: an attempted Extreme/retest that converts to accepted outside-BB Momentum is no longer a valid Extreme context and the taught Extreme position should be exited;
- V05: a Re-Entry setup may penetrate MA5, but closing through/clearing the relevant MA5/MA10 cluster invalidates the taught Re-Entry context.

These are structural context/invalidation statements. They do **not** define one universal initial broker hard-SL price formula for every executable H1 Re-Entry / REM / RRE / REE trade.

## Finale V01–V07 cross-check
### V01
- Confirms Extreme -> TP Wajib -> MHV -> direction -> Re-Entry -> Momentum cycle.
- Confirms mandatory profit-taking for normal/basic Extreme.
- Does not define a universal executable TP or hard-SL formula for Re-Entry/REM/RRE/REE.

### V02
- Flat-BB outside excursion examples repeatedly use Mid BB as a minimum/reference destination.
- Extracted rule itself warns this must not be converted into a guaranteed universal execution rule.
- No universal Re-Entry/REM/RRE/REE hard-SL rule is defined.

### V03
- Clarifies direction vs Momentum and MA5 Re-Entry zone.
- No universal executable TP/SL rule for Re-Entry/REM/RRE/REE is defined.

### V04
- Gives very strong normal Extreme TP-Wajib evidence: opposite MA5/MA10 first, Mid BB farther/max.
- Gives structural Extreme invalidation when an attempted retest becomes accepted outside-BB Momentum.
- Does not establish H1/H4/D1 outer BB as universal TP for Re-Entry/REM/RRE/REE.
- Does not establish source-Re-Entry-candle wick +/- one point as universal hard SL.

### V05
- Reconfirms normal Extreme TP-Wajib.
- Gives Re-Entry close-side invalidation: price may penetrate MA5 but should not close through/clear both relevant MA5 and MA10 against the setup.
- This is setup validity/structural invalidation evidence, not an explicit universal broker hard-SL formula.
- No accepted rule states that every Re-Entry/REM/RRE/REE must TP at the outer BB of its Re-Entry source timeframe.

### V06
- Focuses on Re-Entry confluence, MTF completion and first-candle-validation / second-candle-entry timing.
- No universal executable TP/SL formula for Re-Entry/REM/RRE/REE is defined.

### V07
- Contains a personal stop methodology using MA10 plus allowance and risk sizing.
- The Finale extraction explicitly classifies this as personal risk-management material, not universal Strategy Core.
- The conflict register keeps this as `REJECT/HOLD FROM CORE` for universal SL ownership.

## Current M17 project contract
The current M17 contract deliberately separates provenance:
- `PDF_CORE` — explicit source semantics;
- `FORUM_SUPPORTED` — community-supported BBMA destination/exit interpretation;
- `EA_SAFETY` — deterministic broker-side autonomous protection.

Current executable mapping is:
- standalone H1 Re-Entry -> H1 outer BB TP;
- REM -> H4 outer BB TP;
- RRE/REE -> D1 outer BB TP;
- hard SL -> exact mapped Re-Entry source-candle wick +/- one broker point.

The contract itself classifies the hard SL as **EA_SAFETY informed by FORUM_SUPPORTED structural practice**, not as an explicit PDF/Finale Core rule.

## Re-audit conclusion after V01–V07
The newer Finale evidence **does not invalidate F7**. It makes the provenance boundary more precise:

1. **Normal Extreme TP-Wajib is strongly Core-supported.**
2. **Structural invalidation/exit concepts are additionally supported** for Extreme and Re-Entry contexts.
3. **The current executable H1 Re-Entry / REM / RRE / REE outer-BB TP mapping is still not established as a universal explicit Oma-Ally Core rule by the accepted V01–V07 evidence.**
4. **The current source-candle wick +/- one broker point hard SL is still not established as a universal explicit Oma-Ally Core rule by V01–V07.**
5. V07's MA10+allowance stop cannot be promoted into universal Core without overriding the project's own accepted source classification.

Therefore the current M17 mapping remains internally explicit and provenance-honest, but it is **not accurate to call the complete executable SL/TP pair 100% PDF/Finale/Oma-Ally Core-derived** based on the accepted source set.

This remains a governance/classification issue rather than a proven execution-code defect.

## Decision boundary
### Option A — retain current mixed-provenance execution policy
Keep the current deterministic broker TP/SL mapping, but continue labeling it accurately as `FORUM_SUPPORTED` / `EA_SAFETY` where applicable. Do not advertise the complete executable SL/TP as explicit PDF/Finale Core.

### Option B — require fully Core-derived executable SL/TP
Do not call M17 final until stronger authoritative source evidence is found for each executable Re-Entry/REM/RRE/REE TP and hard-SL rule. If no such evidence exists, redesign/exclude unsupported broker exit mapping rather than silently inventing it.

## Recommendation after Finale V01–V07 re-audit
For engineering continuity, **Option A remains the safer implementation policy** because it preserves deterministic broker protection while keeping provenance accurate. The Finale set strengthens source-supported structural lifecycle/invalidation but does not supply the missing universal broker TP/SL formulas for the current executable Re-Entry combinations.

No EA source code was changed by this re-audit.
