# CORE-V2-F7 — Static TP vs Lifecycle Exit Coexistence Audit

> **2026-08-25 EXECUTABLE-PRECEDENCE NOTICE**
> This document is retained as historical/provisional evidence reconstruction. Where it treats post-Re-Entry no-Momentum, re-arm, hold/no-TP, or related lifecycle-close behavior as executable/source-spec `RESOLVED`, that promotion is superseded by `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`, `docs/references/HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`, and the current authoritative Strategy Core. Those material lifecycle behaviors remain HOLD unless a later explicit strategy decision reopens them. No EA execution authority may be derived from the superseded conclusion alone.

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: executable H1 Re-Entry / REM / RRE / REE take-profit architecture under Path A  
Status: **AUDIT COMPLETE — LIFECYCLE EXIT IS PRIMARY STRATEGY-CORE TP MECHANISM FOR RE-ENTRY-OWNED TRADES; STATIC OUTER-BB BROKER TP IS NOT CORE-AUTHORIZED; NO EA CODE CHANGE WHILE P3 CANDIDATE IS FROZEN**

## 1. Question

For executable BBMA trades whose strategy owner is a Re-Entry (standalone H1 Re-Entry, REM, RRE, REE), should the EA:

1. place a broker-side static TP and also run the accepted post-Re-Entry Momentum/no-Momentum lifecycle exit; or
2. treat the Momentum/no-Momentum lifecycle as the primary Strategy-Core profit-taking mechanism, with no universal static Re-Entry TP unless a separately proven source rule exists?

This audit is independent of the current M17 implementation. Existing code is examined only after source semantics are established.

No EA source change is authorized by this audit while the current P3 runtime candidate remains frozen.

---

## 2. Mandatory source / GitHub preflight

Applied project order:

`Original Evidence -> Canonical Strategy Core -> Contracts / Blueprint -> Current Code -> Runtime State`

Relevant governance:
- `PROJECT_INSTRUCTIONS.md` requires BBMA-derived SL/TP/exit behavior to be source-backed and forbids inventing unresolved trading semantics;
- `SOURCE_INDEX.md` preserves PDF precedence, Finale as clarification, and explicit HOLD handling;
- Path A requires strict Core provenance for executable M17 SL/TP behavior.

Relevant evidence:
- primary operational PDF `Oma ally BBMA - AL.pdf`;
- secondary `BBMA technique.pdf`;
- Tier-B strong-provenance `BBMA Home Course Workbook`;
- Finale V05/V06 / Master Rule Index;
- canonical `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- prior F7 workbook reconciliation, deterministic no-Momentum exit, and combination lifecycle-owner audits.

Relevant live architecture:
- M17 currently requires a non-zero mapped static TP;
- M23 currently preserves broker SL/TP and does not perform normal dynamic BBMA closes;
- M24 recovery preserves broker Entry/SL/TP but does not yet reconstruct the new lifecycle exit state.

---

## 3. Critical source distinction: Extreme TP versus Re-Entry TP

### 3.1 Extreme has an explicit TP-Wajib destination

The source set is strong and consistent for **normal Extreme**:
- Extreme has a TP-Wajib phase;
- normal first TP-Wajib area is the opposite MA5/MA10 area;
- Mid BB is a farther / maximum context.

This is already accepted in Strategy Core V2.

Therefore this audit does **not** remove or reinterpret the normal Extreme TP-Wajib rule.

### 3.2 Re-Entry does not inherit the Extreme TP formula

The same source set does not state that every Re-Entry must use a universal static broker TP.

Primary PDF cycle:

`... CSD/direction -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`

The Re-Entry stage is followed by a continuation test through Momentum/CSM, not by an explicitly stated universal fixed target.

Finale likewise attaches `TP Wajib` explicitly to the Extreme stage and teaches Re-Entry as the setup/entry stage followed by Momentum.

Conclusion:

> Extreme TP-Wajib provenance cannot be silently generalized into a universal Re-Entry static TP rule.

---

## 4. Home Course Workbook — strongest direct exit evidence

### 4.1 Post-Re-Entry lifecycle is conditional on Momentum

The workbook repeatedly gives the sequence:

`Arah -> Re-Entry -> Momentum`

and:

`Arah -> Re-Entry -> Tiada Momentum -> Close position / TP`

The summary repeats:
- Re-Entry + Momentum -> continuation and another Re-Entry;
- Re-Entry + no Momentum -> market rotates / take profit.

This is a **state-dependent exit model**.

### 4.2 Pre-Re-Entry hold rule disproves a universal outer-BB TP assumption

The workbook explicitly distinguishes:

`Arah -> no Re-Entry yet -> HOLD / wait for Re-Entry`

It also gives examples where strong direction reaches the outer BB before the expected Re-Entry and says not to take profit merely because that destination was reached; the Re-Entry is still expected.

This is important because it shows that an outer-BB destination is not automatically equivalent to `broker TP must execute here`.

### 4.3 Direction destination is not the same as Re-Entry broker TP

The workbook says candle direction can have a Top-BB / Low-BB destination. However, in the same Re-Entry lesson it governs whether the position is held or closed by the later Re-Entry/Momentum sequence.

Therefore the phrase `destination = Top/Low BB` is useful market-structure context but is insufficient to prove:

- every Re-Entry must have a resting broker TP at that outer BB;
- the destination must close the trade before the Momentum/no-Momentum lifecycle can resolve;
- the exact H1/H4/D1 outer-BB mapping currently used by M17.

### 4.4 MHV example also uses lifecycle management

The workbook describes MHV profit-taking as negotiable depending on whether the following candle becomes Momentum or closes back inside the BB.

This further shows that BBMA exit teaching can be **state/lifecycle based**, not universally a static price target.

---

## 5. Primary PDF reconciliation

The primary PDF establishes:
- Re-Entry after direction / retracement;
- price then travels in the intended direction and creates Momentum/CSM;
- Momentum may continue and create later Re-Entries;
- opposite Extreme appears once trend/momentum ends.

It does **not** establish:
- H1 Re-Entry -> mandatory H1 outer-BB broker TP;
- REM -> mandatory H4 outer-BB broker TP;
- RRE/REE -> mandatory D1 outer-BB broker TP;
- a rule that a static TP must coexist with the post-Re-Entry Momentum/no-Momentum lifecycle.

Assessment:

**Strong structural support for lifecycle continuation/failure; insufficient support for universal static Re-Entry TP.**

---

## 6. Finale reconciliation

Finale V05/V06 and the Master Rule Index establish:
- normal Extreme -> TP Wajib;
- direction signal -> Re-Entry;
- Re-Entry -> Momentum/continuation;
- Momentum can create further Re-Entry opportunities;
- higher-timeframe Re-Entry is read through lower-timeframe structures.

Finale does not provide a universal static Re-Entry TP formula equivalent to the current M17 H1/H4/D1 outer-BB mapping.

A particularly important source-governance distinction is that `TP Wajib` is taught as an Extreme-stage obligation rather than as a universal label for every Re-Entry.

Assessment:

**Supports lifecycle as the strategy-owned post-Re-Entry mechanism; does not authorize static outer-BB TP coexistence as Core.**

---

## 7. Secondary PDF / forum reconciliation

### Secondary PDF

The secondary PDF corroborates:
- Momentum through directional/expanding BB behavior;
- MHV as loss of momentum;
- Re-Entry structure;
- outer BB / MA support-resistance context.

It does not close the universal static Re-Entry TP question.

### Forum evidence

The retained Forex Factory evidence remains supplemental and does not provide sufficiently strong, traceable authority for the exact current M17 static mapping.

Under Path A, forum/community convention cannot rescue an otherwise unresolved static TP rule.

---

## 8. Coexistence decision

### STLE-01 — Primary Re-Entry profit-taking mechanism

**RESOLVED: LIFECYCLE EXIT IS THE PRIMARY STRATEGY-CORE MECHANISM.**

For an executable Re-Entry-owned position:

`POSITION OPEN -> MOMENTUM_PENDING`

Then on the resolved lifecycle-owner timeframe:

- same-direction source-valid CSM -> continuation confirmed / keep position under the initial no-Momentum rule;
- first later reverse-confirmation candle before same-direction CSM -> no-Momentum failure / close;
- source-valid opposite CSM -> stronger invalidation / close.

Owner timeframes already resolved by the preceding audit:
- standalone H1 Re-Entry -> H1;
- REM -> H4;
- RRE -> D1;
- REE -> D1.

This mechanism is source-owned because the workbook directly teaches the post-Re-Entry Momentum/no-Momentum branch and the other canonical sources strongly corroborate the cycle.

### STLE-02 — Universal static outer-BB TP

**NOT CORE-AUTHORIZED.**

The following cannot be retained as `BBMA Strategy Core` solely from current evidence:
- H1 Re-Entry -> H1 Top/Low BB broker TP;
- REM -> H4 Top/Low BB broker TP;
- RRE/REE -> D1 Top/Low BB broker TP.

The resolved lifecycle-owner timeframe matching the old M17 TP-source timeframe does **not** prove the owner's outer BB is a mandatory static TP.

### STLE-03 — Static TP + lifecycle close coexistence

**NOT AUTHORIZED AS CORE UNDER PATH A.**

Source evidence does not establish that every Re-Entry trade should have both:
1. a resting static outer-BB TP; and
2. the post-Re-Entry Momentum/no-Momentum lifecycle close.

Keeping both would create a race between two exit authorities:
- broker may close at the static TP before lifecycle continuation is allowed to develop; or
- lifecycle may close earlier while the static TP remains merely an unused cap.

Because the source does not define this coexistence or precedence, Path A forbids silently inventing it.

Therefore the future strict-Core design should **not require a universal broker-side TP for Re-Entry-owned trades** unless stronger source evidence later establishes a specific static target.

### STLE-04 — Optional project-policy TP

A static TP could theoretically exist as an explicitly labelled non-Core project risk/profit policy, but that would be **Path B-style project execution policy**, not the currently selected strict Path A Core-only resolution.

Therefore it is outside the accepted Path A Strategy-Core design unless governance is explicitly changed later.

---

## 9. Broker order implication

For future strict-Core Re-Entry execution, the source-faithful architecture is conceptually:

- broker-side protective hard SL remains present as `EA_SAFETY` until/unless stronger source SL provenance is established;
- broker TP for Re-Entry-owned trades is **not mandatory** and may be `0` / absent;
- profit-taking occurs through the approved lifecycle close event in M23;
- normal Extreme TP-Wajib remains a separate source-owned rule if standalone Extreme execution is ever enabled.

This conclusion is about strategy provenance, not a statement that MT4 technically requires or forbids TP=0.

---

## 10. Downstream architecture mismatch exposed

The current source/contract still assumes a non-zero static TP before execution:

- M17 `ResolveApprovedInitialSLTP()` resolves an outer-BB destination into `decision.TakeProfit`;
- `HasSourceResolvedSLTP()` requires both SL and TP > 0;
- `ValidateSLTP()` rejects `TakeProfit <= 0`;
- `MinRRRatio` is calculated from static TP distance;
- M22 sends the broker order with that TP;
- M23 preserves the resting TP and currently has no normal dynamic BBMA lifecycle close.

This is now classified as:

**BLUEPRINT / IMPLEMENTATION GAP RELATIVE TO THE NEWLY RESOLVED STRICT-PATH-A EXIT SEMANTICS**, not proof that the old code was irrational under its previous contract.

The gap must remain deferred while the P3 runtime candidate is frozen.

---

## 11. MinRR consequence

A lifecycle-managed Re-Entry trade has no source-proven deterministic reward distance at entry under the current evidence set.

Therefore the existing `MinRRRatio` filter cannot continue to claim a Strategy-Core reward calculation by using the unproven static outer-BB TP.

Future resolution must choose one of the following without invention:
- disable / bypass `MinRRRatio` for lifecycle-managed Re-Entry trades; or
- only use it when a separately source-proven static target exists.

Do **not** manufacture an estimated lifecycle reward distance merely to preserve the filter.

This is an architecture follow-up item, not implemented by this audit.

---

## 12. M23 / M24 implication

If implemented after the runtime freeze:

### M23
Must become the normal broker-side close executor for the approved lifecycle event while preserving:
- no partial close;
- no breakeven migration;
- no trailing stop;
- no TP2/TP3.

M23 must consume owner-timeframe lifecycle evidence rather than recreate M10/M12 detection semantics independently.

### M24
Must persist/recover enough immutable strategy identity to reconstruct:
- lifecycle owner timeframe;
- lifecycle owner Re-Entry identity;
- `MOMENTUM_PENDING` versus `MOMENTUM_CONFIRMED` state;
- last processed owner-timeframe closed candle / idempotency boundary.

If identity cannot be safely recovered, existing fail-frozen behavior remains preferable to fabricating lifecycle authority.

---

## 13. Runtime / failure-mode consequence

Removing a broker-side TP increases dependence on the EA being alive for normal profit-taking.

Therefore the future implementation must preserve:
- hard protective SL at the broker;
- restart-idempotent recovery;
- lifecycle state reconstruction;
- duplicate-close protection;
- M20 emergency-close precedence.

This is an engineering reliability requirement, not a new BBMA trading rule.

---

## 14. Current P3 freeze

**NO EA CODE CHANGE NOW.**

The current compiled P3 candidate must remain unchanged until its pending runtime evidence is closed, so the evidence remains attributable to one source/build.

This audit is documentation/source-governance only.

After P3 runtime closure, implementing the resolved F7 semantics requires a new build and at minimum:

1. canonical Core/spec update;
2. M17 contract redesign to permit protective-SL-only Re-Entry payloads;
3. M23 lifecycle-close contract update;
4. M24 lifecycle recovery/persistence update;
5. M19/MinRR compatibility decision;
6. M22 TP=0 execution-path validation;
7. new unique left-aligned build/header identifier;
8. static cross-module / Strategy-Core purity audit;
9. native MetaEditor 0 errors / 0 warnings;
10. fresh runtime tests for continuation, no-Momentum reversal close, opposite CSM close, restart recovery, and emergency-close precedence.

---

## 15. Final verdict

For **Re-Entry-owned executable trades**:

**Primary Strategy-Core TP mechanism:**

`Re-Entry -> Momentum/no-Momentum lifecycle`

**Universal static outer-BB broker TP:**

`NOT PROVEN / NOT CORE-AUTHORIZED`

**Static outer-BB TP + lifecycle close coexistence:**

`NOT AUTHORIZED AS CORE UNDER PATH A`

**Future strict-Core broker payload:**

`protective hard SL (EA_SAFETY) + no mandatory static TP`, with M23 executing the source-approved lifecycle close.

**Normal Extreme remains separate:**

`Extreme -> TP Wajib at the source-supported MA5/MA10 area (Mid BB farther context)` remains accepted Core and is not removed by this audit.

This resolves the coexistence question without converting an unproven static target into BBMA Core.