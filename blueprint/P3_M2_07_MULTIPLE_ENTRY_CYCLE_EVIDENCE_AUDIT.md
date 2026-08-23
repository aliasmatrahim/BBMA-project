# P3-M2-07 — Multiple Entry / Cycle Ownership Evidence Audit

Date: 2026-08-23
Branch: `blueprint-dev`
Status: **EVIDENCE RESOLUTION COMPLETE / CODE POLICY PATCH REQUIRED**

## Audit question
Cross-check the approved BBMA source set for:
1. multiple entry opportunities inside one directional cycle;
2. add-on/re-entry while an earlier same-direction trade exists;
3. cycle ownership and when direction changes;
4. opposite-direction entry while an older trade remains open;
5. whether a later setup should be rejected merely because it is "weaker" or has worse relative quality than an earlier setup.

## Evidence synthesis

### 1. Multiple Re-Entry opportunities inside one BBMA cycle — RESOLVED: YES
Primary PDF evidence states that after CSD, price may retrace to MA5 for Re-Entry and that **for every CSD a Re-Entry can be made at MA5/10/Mid-BB confluence**. The same reference diagram/text shows repeated CSM -> consolidation -> Re-Entry structures before the final opposite Extreme.

This means one directional BBMA cycle is not limited to a single Re-Entry opportunity.

### 2. Same-direction add-on / layered entry — RESOLVED: SOURCE-COMPATIBLE
The PDF explicitly describes repeated Re-Entry opportunities in one ongoing directional path. It does not impose a one-position-per-cycle rule.

Forum corroboration is more explicit operationally: BBMA practitioners describe adding another entry/layer when price reaches the Re-Entry MA5/10 zone, including keeping the same SL on both positions. This forum evidence is supporting/corroborative, not elevated to explicit Oma Ally PDF wording.

Project consequence: a second **distinct, source-valid, same-direction** RE/REM/RRE/REE decision may be allowed, subject to account risk, portfolio cap, duplicate protection and broker safety. It must not be created merely because MaxTradePerPair > 1; it still needs an independent valid DecisionID/setup.

### 3. Directional cycle ownership / cycle end — RESOLVED
Primary PDF evidence states that an **opposite Extreme is created when trend/momentum ends and this is when the cycle restarts or reverses**. It also instructs traders to establish direction first and then seek Re-Entry, and to trade strong Re-Entries with aligned trend/MTF context.

Therefore the active BBMA cycle has directional ownership; an opposite-cycle event is a regime/cycle transition, not a normal invitation to carry two contradictory cycle directions simultaneously as independent fresh entries.

### 4. Simultaneous opposite-direction EA positions on one pair — RESOLVED: SHOULD NOT BE NORMAL ENTRY POLICY
The approved source set does not support opening a fresh opposite-direction position while treating the previous opposite cycle as concurrently authoritative. Primary evidence says the cycle restarts/reverses at the opposite Extreme. Forum corroboration describes opposite CSM as a cut-loss/invalidation cue for the earlier entry rather than a reason to hedge the same pair with a fresh opposite trade while the old thesis remains active.

Project consequence: **new opposite-direction entry should be blocked while an EA-owned opposite position remains live on the same pair.** Existing trade exit/SL/TP/lifecycle remains the trade-management responsibility; this audit does not invent a forced-close rule.

This is best classified as `SOURCE-DERIVED CYCLE DIRECTION GUARD + EA SAFETY`, not a new indicator/filter.

### 5. "Second setup weaker than first" comparison — RESOLVED: DO NOT INVENT
No approved source establishes a numeric or ordinal comparison between an already-open trade and a later valid RE/REM/RRE/REE decision such as "reject trade #2 because it is weaker" or "compare RR/score and keep only the stronger setup."

Therefore:
- do not introduce signal scoring or relative-quality ranking against an existing position;
- same-direction later setup is independently valid or invalid under BBMA source rules;
- incremental account risk may reject it through M19/M20 safety overlays;
- source-derived validity and account safety remain separate.

## Final policy resolution

1. **Multiple same-direction entries:** ALLOWED only for distinct independently validated BBMA decisions, capped by portfolio/risk settings.
2. **Duplicate same decision:** BLOCKED.
3. **Opposite BUY/SELL live coexistence created by new EA entries:** BLOCKED at pair-direction execution admission.
4. **Existing trade automatically closed on opposite signal:** NOT authorised by this audit; current SL/TP/trade lifecycle remains unchanged unless separately source-resolved.
5. **Relative setup-quality comparison:** NOT authorised; do not add scoring/ranking.
6. `MaxTradePerPair=2` remains valid as a portfolio cap for same-direction distinct setups.

## Current-code delta
Current `TradeLockMode=LOCK_OFF` allows a later opposite distinct decision to pass when portfolio/risk rules allow it. That is inconsistent with the resolved cycle-direction policy above.

A code patch is required to make opposite-direction pair coexistence impossible regardless of optional TradeLock mode, while preserving same-direction add-ons under `LOCK_OFF` / `LOCK_SAME_DIRECTION` and preserving `LOCK_ONE_POSITION` as the strict one-position option.

## Patch constraints
The patch must:
- add a hard pair-direction guard before OrderSend;
- inspect only live EA-owned positions for that exact pair/magic ownership;
- reject a new decision if any live EA-owned position on the pair has the opposite direction;
- preserve same-direction add-ons subject to MaxTradePerPair and risk/portfolio limits;
- preserve duplicate DecisionID protection;
- not force-close existing positions;
- not add score/quality comparison;
- update the mandatory EA About/header patch/build identifier in the same source change;
- compile MetaEditor 0E0W before merge.

## Evidence confidence
- Multiple Re-Entry opportunities in one cycle: **HIGH** (direct PDF).
- Same-direction add-on compatibility: **HIGH for setup opportunities; MEDIUM-HIGH for simultaneous layering** (direct repeated-Re-Entry concept + explicit forum corroboration).
- Opposite cycle restarts/reverses prior cycle: **HIGH** (direct PDF).
- Block new opposite-direction coexistence: **HIGH as source-derived project policy / safety mapping**, while forced-close semantics remain unresolved and are intentionally not added.
