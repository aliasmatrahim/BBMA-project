# NMJE D1→M15 Coverage Audit — 2026-08-26

Branch: `d1-owner-dev`

## Status
**PARTIAL COVERAGE / N1 ARCHITECTURE CORRECT / CURRENT OBSERVABILITY MAP LAGS CURRENT EA STATE COVERAGE / NO EXECUTION BUG / NO MQL4 CHANGE IN THIS AUDIT**

## Source identity audited
- EA: `Version 4.5.6 - C044 Deterministic Replay Stage`
- source blob: `f0f80decbdbda836c12b6073f5dbc6e347662b13`
- source SHA-256: `d2d94e5f7cf0f5b513fd2f8dfd877264fe33aad1425d54e056effccb33d782f4`
- `EnableC044Lifecycle=false`

## Audit question
Does current M12N/NMJE represent the full BBMA/D1O state universe that the active EA now owns across `D1 -> H4 -> H1 -> M15`, while remaining N1 observation-only?

## Canonical boundary
The N1 design itself is correct and remains authoritative:
- NMJE consumes owner-produced snapshots;
- it does not re-detect Extreme, MHV/MLV, eCSD/CSD/CSM, Re-Entry or D1 MA50 ownership;
- it does not create/reject/rank/execute trades;
- exact REM/RRE/REE signatures remain unchanged;
- nested relation remains diagnostics/shadow-research metadata only;
- `TRADE BEHAVIOUR BEFORE NMJE == TRADE BEHAVIOUR AFTER NMJE`.

The coverage issue below is therefore an observability/research-integrity issue, not a strategy-authority defect.

## Current implemented coverage matrix

### D1
Current NMJE D1 node covers:
- confirmed D1 Re-Entry;
- D1 strategic owner BUY/SELL;
- D1 transition/unresolved state.

Current active EA additionally owns or exposes:
- D1 Extreme lifecycle for BUY/SELL;
- `D1OpportunityJourney` with families `D1_OPP_EXTREME_TPW`, `D1_OPP_CSD`, `D1_OPP_RE_ENTRY`, `D1_OPP_MOMENTUM_RETRACE`;
- D1 opportunity direction, source signal, source candle, activation, tactical flag, TPW completion and CycleID;
- D1 eCSD watch event;
- D1 CSD/CSM opportunity source events.

Coverage result: **PARTIAL**.

### H4
Current NMJE H4 node covers:
- confirmed H4 Re-Entry;
- candidate H4 Re-Entry;
- active H4 directional owner;
- H4 owner source signal through `StageType`;
- active H4 Extreme lifecycle.

This is broadly aligned with the currently persistent H4 owner-state surface. No independent H4 MHV/MLV owner exists in current `PairState`; NMJE must not invent one.

Coverage result: **GOOD / no material current gap found**.

### H1
Current NMJE H1 node covers:
- confirmed H1 Re-Entry;
- candidate H1 Re-Entry;
- active H1 Extreme lifecycle.

H1 direction-stage context may exist internally inside Re-Entry Type-1 ownership/ranging provenance, but there is no separate canonical H1 direction-owner object equivalent to H4. NMJE should not invent one.

Coverage result: **GOOD FOR CURRENT PERSISTENT OWNER SURFACE / minor lifecycle-detail compression only**.

### M15
Current NMJE M15 node covers:
- canonical MHV/MLV lifecycle only.

Current active EA additionally owns or computes:
- persistent M15 Re-Entry BUY/SELL state;
- persistent M15 Extreme BUY/SELL lifecycle;
- same-cycle M15 CSD, eCSD and CSM snapshots;
- D1 Opportunity execution may use fresh confirmed M15 Re-Entry when its H4 alignment requirement is satisfied.

Coverage result: **MATERIAL PARTIAL COVERAGE**.

## Confirmed coverage gaps

### NMJE-COV-01 — D1 Opportunity overlay absent from NMJE journey state
Severity: **HIGH for observability / NONE for execution**

`D1OpportunityJourney` is now a first-class active state in the EA, but `NestedJourneyState`/D1 node does not expose its family, direction, source signal, activation, tactical flag, TPW state or CycleID.

Impact:
- N1 journey diagnostics can describe D1 owner/Re-Entry context while omitting the active D1 Opportunity family that actually contextualized a Mode-2 LTF decision;
- N2 decision shadow separately logs `AUTH`, `OFAM`, `OC` and `LTF`, so execution identity is not lost, but the N1 relation snapshot itself is less complete than the current EA state universe.

Safe future direction:
- add D1 Opportunity as read-only overlay metadata;
- do **not** make it a new `NESTED_PARENT_*` execution/priority authority.

Classification: `[PROJECT-EXTENSION][ENGINEERING-ONLY OBSERVABILITY]`.

### NMJE-COV-02 — D1 Extreme/TPW lifecycle absent from D1 node
Severity: **MEDIUM-HIGH for journey completeness / NONE for execution**

The EA maintains D1 Extreme lifecycle and uses mature D1 Extreme + active TP-Wajib for `D1_OPP_EXTREME_TPW`, but the NMJE D1 node currently prefers only confirmed D1 Re-Entry or D1 strategic owner/transition.

Impact:
- a tactical D1 Extreme/TPW journey can exist without being visible as such in the D1 node;
- this is especially relevant for counter-MA50 tactical D1O research.

Safe future direction:
- expose mature D1 Extreme/TPW as secondary read-only D1 metadata;
- do not replace D1 strategic owner or D1 Re-Entry parent rules.

Classification: TPW/Extreme lifecycle `[BBMA-ORIGINAL]`; using it as D1O family `[BBMA-SOURCE-CONSISTENT][PROJECT-EXTENSION]`; NMJE representation `[ENGINEERING-ONLY]`.

### NMJE-COV-03 — M15 Re-Entry absent from M15 node
Severity: **HIGH for N1/N2 coverage / NONE for execution**

The EA has persistent `re_m15_buy_state` / `re_m15_sell_state`, and D1 Opportunity execution explicitly evaluates fresh confirmed M15 Re-Entry. Current `NMJE_BuildM15Node()` only reads MHV/MLV.

Impact:
- the exact LTF structure that may authorize a D1O entry can be invisible in the M15 node;
- simultaneous H1/M15 D1O cluster research can therefore have an incomplete nested-state picture even though D1O decision metadata itself remains correct.

Safe future direction:
- include confirmed/candidate M15 Re-Entry in M15 observation;
- preserve read-only semantics and existing execution identity.

Classification: Re-Entry `[BBMA-ORIGINAL]`; node coverage `[ENGINEERING-ONLY]`.

### NMJE-COV-04 — M15 Extreme lifecycle absent from M15 node
Severity: **MEDIUM for journey completeness / NONE for execution**

The EA maintains M15 Extreme lifecycle because canonical MHV/MLV provenance depends on a same-TF mature Extreme. NMJE M15 currently shows MHV/MLV only.

Impact:
- the pre-MHV portion of the M15 BBMA lifecycle can be invisible;
- `Extreme -> TP Wajib -> MHV/MLV` is therefore not fully observable on M15 through one NMJE node.

Safe future direction:
- expose M15 Extreme as secondary/pre-MHV observation metadata;
- do not change MHV lifecycle ownership.

Classification: `[BBMA-ORIGINAL]` lifecycle, `[ENGINEERING-ONLY]` representation.

### NMJE-COV-05 — Child-activity / relation classifier ignores M15 Re-Entry and M15 Extreme
Severity: **HIGH for research bucket integrity / NONE for execution**

`NMJE_HasChildActivity()` currently considers:
- H1 candidate/confirmed Re-Entry;
- H1 Extreme;
- M15 MHV/MLV.

It does not consider persistent M15 Re-Entry or M15 Extreme.

The main relation classifier similarly gives authoritative directional comparison to confirmed H1 Re-Entry and supporting/building treatment to H1 Extreme/M15 MHV, but no equivalent visibility for M15 Re-Entry.

Impact:
- current D1O M15-Re-Entry activity can be omitted from `BUILDING/ALIGNED/CONFLICT` reasoning;
- N2 outcome research may therefore bucket some trades under a relation that is descriptively incomplete.

This does **not** change trading because N1/N2 relation is not an execution gate.

Safe future direction:
- extend child-activity observation to M15 RE/Extreme only after their immutable same-cycle snapshots are available;
- define relation semantics conservatively and separately from M15 final authority.

Classification: `[ENGINEERING-ONLY OBSERVABILITY/RESEARCH INTEGRITY]`.

### NMJE-COV-06 — Single-primary-stage node compresses simultaneous valid states
Severity: **MEDIUM architecture limitation**

`NestedTFNode` has one `StageType`, one direction and one state code. Current EA can legitimately have more than one relevant state on the same timeframe, for example:
- M15 MHV/MLV plus fresh M15 Re-Entry;
- a D1 strategic owner plus an active D1 Opportunity family;
- owner context plus an Extreme lifecycle state.

A single primary stage is sufficient for the original minimal N1 observer, but it is no longer sufficient for complete current-state coverage without losing secondary context.

Safe future direction:
- preserve the existing primary node for compatibility;
- add compact secondary read-only flags/metadata rather than inventing a ranking or replacing owner state.

Classification: `[ENGINEERING-ONLY]`.

## Intentionally excluded / not a gap

### D1 MHV/MLV
The contract allows D1 MHV/MLV as watch/context only, but current source has no persistent D1 MHV/MLV owner equivalent to the M15 canonical lifecycle. NMJE must not infer or re-detect it merely to fill a dashboard field.

Status: **NOT A CURRENT NMJE BUG / producer coverage absent by design**.

### D1 eCSD
Current D1O path logs eCSD as WATCH ONLY. Its absence from the primary D1 node is a low-priority observability omission, not a strategy gap.

### Parent kinds
Current parent preference `H4 RE -> H4 owner -> D1 RE -> D1 strategic owner` remains valid for N1. D1 Opportunity should not silently become a new parent kind merely because it is exposed as metadata.

## D1→M15 coverage scorecard
- D1 strategic owner: **COVERED**
- D1 confirmed Re-Entry: **COVERED**
- D1 Extreme/TPW: **PARTIAL / not in node**
- D1 Opportunity family/source: **MISSING FROM NMJE overlay**
- H4 Re-Entry: **COVERED**
- H4 directional owner/source signal: **COVERED**
- H4 Extreme: **COVERED**
- H1 Re-Entry: **COVERED**
- H1 Extreme: **COVERED**
- M15 MHV/MLV: **COVERED**
- M15 Re-Entry: **MISSING FROM M15 node**
- M15 Extreme: **MISSING FROM M15 node**
- M15 CSD/eCSD/CSM transient snapshots: **NOT REPRESENTED / requires safe same-cycle snapshot interface if ever added**

## Overall conclusion
The current NMJE is **architecturally correct for N1** and remains safely read-only, but it is **not yet a complete D1→M15 state map of the current v4.56 EA**.

The most important gaps are:
1. M15 Re-Entry coverage;
2. D1 Opportunity overlay coverage;
3. child-activity/relation awareness of M15 Re-Entry/Extreme;
4. D1 Extreme/TPW observation;
5. M15 Extreme observation;
6. single-primary-stage compression.

These gaps can reduce diagnostic and N2 research fidelity but do not currently alter or corrupt trade execution.

## Recommended next step
Before any N3/execution use of nested relation, create an **N1.1 coverage-only extension** that:
1. adds read-only D1 Opportunity metadata;
2. adds M15 RE + M15 Extreme observation;
3. extends child-activity coverage without changing candidate counts or M15 authority;
4. preserves current parent kinds;
5. never calls strategy detectors from NMJE;
6. consumes only already-owned immutable snapshots;
7. keeps `TRADE BEHAVIOUR BEFORE NMJE == TRADE BEHAVIOUR AFTER NMJE`;
8. receives static regression + native MetaEditor 0E0W + N2 telemetry compatibility checks.

No source implementation is authorized by this audit alone.
