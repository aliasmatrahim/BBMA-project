# CORE-V2 — D1 Canonical Contract Reconciliation Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Status: **RECONCILIATION IN PROGRESS / DOCUMENTATION-ONLY / NO EA SOURCE CHANGE**

## Purpose
Reconcile the resolved Home Course / D1 major-trend findings into one canonical project hierarchy without changing the frozen EA source.

Target hierarchy:

`D1 strategic owner -> H4 structural/setup parent -> H1/M15 execution structure`

Scope:
- canonical Strategy Core V2;
- prior F4 H1/H4 parent decision;
- M11 D1 major-trend owner contract;
- M15 final entry authority contract;
- M16 downstream validity contract;
- `CURRENT.md`;
- `MASTER_QUEUE.md`.

## Source / governance preflight
Applied mandatory order:

`PROJECT_INSTRUCTIONS -> SOURCE_INDEX -> Core V2 -> primary/secondary PDF evidence -> Finale -> retained forum evidence -> Home Course D1 reconciliation -> active contracts/code`

Relevant conclusions already resolved by `HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`:
- D1/MA50 is strategic major-trend authority;
- H4 remains immediate structural/setup parent and cannot override D1;
- D1 BUY confirmed requires closed D1 price above MA50 with MA50 rising;
- D1 SELL confirmed requires closed D1 price below MA50 with MA50 falling;
- otherwise valid but non-agreeing D1 states are `D1_TRANSITION`;
- transition/unresolved D1 blocks **new** strategy entries rather than freezing the prior owner as executable authority;
- `D1_TRANSITION` is not itself a live-position close rule;
- REM/RRE/REE signatures remain unchanged.

## Canonical ownership result
### M11
Sole producer of D1 strategic owner classification from closed D1 price + MA50 slope.

### H4 owner
Remains structural/setup parent for standalone H1 and lower-TF timing where applicable. H4 has no authority to bypass an opposite/transition/unresolved D1 strategic state.

### M15
Sole final new-entry strategic authority. It must apply D1 strategic-direction eligibility to otherwise structurally valid candidates.

### M16
Revalidates the frozen D1-owner snapshot/identity before downstream execution but does not independently compute a second D1 trend formula.

### M13/M14
Exact REM/RRE/REE component signatures remain unchanged. D1 strategic gating is not implemented by adding a fourth REM component.

### Live-position lifecycle
Unchanged by this reconciliation. D1 transition is not promoted into an ordinary broker-close trigger.

## Current implementation gaps confirmed
1. active `TimeframeData.trend` uses price-vs-EMA50 only and therefore cannot represent price-side + MA50-slope confirmation;
2. Module 11 has no dedicated D1 major-trend owner state;
3. standalone H1 Re-Entry currently requires H4 owner only and lacks the stronger D1 strategic gate;
4. REM final eligibility lacks a separate D1 strategic gate;
5. RRE/REE D1 Re-Entry components are not equivalent to the new D1 MA50 strategic-owner proof;
6. previous Mode-1 static compliance status is historical relative to the pre-Home-Course D1 interpretation and must be re-audited after implementation.

## Change-control boundary
This audit authorizes documentation/specification reconciliation only.

It does **not** authorize changing `blueprint/source/BBMA_EA.mq4` while the current P3 runtime candidate is frozen. A future source patch must use a new unique left-aligned build identifier and fresh native compile/runtime evidence.

## Completion criterion
This audit is complete only when Core V2, F4, M11/M15/M16 contracts, `CURRENT.md`, and `MASTER_QUEUE.md` all express the same hierarchy and no stale statement still grants standalone H1/REM execution authority from H4 alone against an unresolved/opposite D1 state.
