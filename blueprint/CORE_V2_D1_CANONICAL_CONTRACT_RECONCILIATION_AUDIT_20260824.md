# CORE-V2 — D1 Canonical Contract Reconciliation Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Status: **RECONCILIATION COMPLETE / DOCUMENTATION-ONLY / NO EA SOURCE CHANGE**

## Purpose
Reconcile the resolved Home Course / D1 major-trend findings into one canonical project hierarchy without changing the frozen EA source.

Canonical hierarchy:

`D1 strategic owner -> H4 structural/setup parent -> H1/M15 execution structure`

Scope completed:
- `docs/references/SOURCE_INDEX.md`;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- prior F4 H1/H4 parent decision;
- new M11 D1 major-trend owner contract;
- M15 final entry authority contract;
- M16 downstream validity contract;
- `CURRENT.md`;
- `MASTER_QUEUE.md`.

## Source / governance preflight
Applied mandatory order:

`PROJECT_INSTRUCTIONS -> SOURCE_INDEX -> Core V2 -> primary/secondary PDF evidence -> Finale -> retained forum evidence -> Home Course D1 reconciliation -> active contracts/code`

Relevant conclusions resolved by `HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md` and now propagated canonically:
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

Canonical contract:
`blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`.

### H4 owner
Remains structural/setup parent for standalone H1 and lower-TF timing where applicable. H4 has no authority to bypass an opposite/transition/unresolved D1 strategic state.

The older F4 wording that D1 was only broader context and not a mandatory strategic gate is superseded by the reconciled F4 record.

### M15
Remains sole final new-entry strategic authority.

Canonical order:

`structurally valid candidates -> D1 strategic filter -> surviving-direction check -> canonical same-direction selection`

M15 does not compute MA50 itself and does not add D1 as a fourth REM component.

### M16
Revalidates the frozen D1-owner snapshot/identity before downstream execution but does not independently compute a second D1 trend formula.

A transition/unresolved/opposite/mismatched D1 state invalidates the pending **new-entry decision** fail-closed; it is not a live-position close instruction.

### M13/M14
Exact REM/RRE/REE component signatures remain unchanged:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

D1 strategic gating remains separate from component identity.

### Live-position lifecycle
Unchanged by this reconciliation. D1 transition is not promoted into an ordinary broker-close trigger.

## Reconciled files
1. `docs/references/SOURCE_INDEX.md`
   - registered the Tier-B Home Course Workbook evidence/reconciliation chain;
   - added the D1 strategic-owner relevance to the source map.
2. `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
   - added D1 major-trend strategic authority;
   - added `D1_TRANSITION` / unresolved semantics;
   - reconciled H4 as subordinate structural parent;
   - kept REM/RRE/REE signatures unchanged.
3. `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`
   - reopened/reconciled the previous H4-only execution interpretation;
   - now requires same-direction D1 strategic owner + H4 structural owner for standalone H1 higher-timeframe alignment.
4. `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`
   - new canonical producer contract.
5. `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`
   - added D1 strategic-direction eligibility before final selection;
   - preserved exact entry-mode structural candidate types and exact REM/RRE/REE signatures.
6. `blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md`
   - added frozen M11 owner-state revalidation;
   - explicitly forbids duplicate D1 formula ownership.
7. `blueprint/CURRENT.md`
   - records documentation/specification ahead of frozen code;
   - reopens old F4/P3-M1 compliance status relative to stronger D1 evidence.
8. `blueprint/MASTER_QUEUE.md`
   - adds the post-freeze D1 implementation gate;
   - marks the older H4-only F4 and Mode-1 passes as historical/partial relative to the new Core.

## Current implementation gaps confirmed
1. active `TimeframeData.trend` uses price-vs-EMA50 only and therefore cannot represent price-side + MA50-slope confirmation;
2. Module 11 has no dedicated D1 major-trend owner state;
3. standalone H1 Re-Entry currently requires H4 owner only and lacks the stronger D1 strategic gate;
4. REM final eligibility lacks a separate D1 strategic gate;
5. RRE/REE D1 Re-Entry components are not equivalent to the new D1 MA50 strategic-owner proof;
6. M15 decision payload does not yet carry the canonical M11 owner identity for M16 verification;
7. previous Mode-1 static compliance status is historical relative to the pre-Home-Course D1 interpretation and must be re-audited after implementation.

## Change-control boundary
This reconciliation is **documentation/specification only**.

It does **not** change `blueprint/source/BBMA_EA.mq4`, the About/header build identifier, broker behavior, risk sizing, order execution, or the current P3 runtime candidate.

A future source patch must:
- wait until the current runtime freeze is deliberately released/replaced;
- use a new unique left-aligned build identifier;
- implement M11 -> M15 -> M16 in dependency-safe order;
- receive native MetaEditor 0E0W;
- pass static cross-module/Core purity regression;
- receive focused runtime evidence including D1 BUY/SELL/TRANSITION/UNRESOLVED and D1/H4 disagreement cases;
- rerun P3-M1 compliance under the new canonical Core.

## Final verdict
**D1 canonical contract reconciliation is complete.**

The project now has one consistent specification:

`CONFIRMED D1 STRATEGIC DIRECTION`
`-> COMPATIBLE H4 STRUCTURAL PARENT WHERE REQUIRED`
`-> H1/M15 BBMA EXECUTION STRUCTURE`

and:

`D1_TRANSITION / D1_OWNER_UNRESOLVED -> BLOCK NEW ENTRY`

without altering exact REM/RRE/REE signatures and without turning D1 transition into an unsupported live-position exit rule.

**Implementation remains intentionally pending.**
