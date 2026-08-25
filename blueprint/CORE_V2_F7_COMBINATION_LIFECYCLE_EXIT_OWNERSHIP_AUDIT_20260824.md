# CORE-V2-F7 — REM/RRE/REE Lifecycle Exit Ownership Audit

> **2026-08-25 EXECUTABLE-PRECEDENCE NOTICE**
> This document is retained as historical/provisional evidence reconstruction. Where it treats post-Re-Entry no-Momentum, re-arm, hold/no-TP, or related lifecycle-close behavior as executable/source-spec `RESOLVED`, that promotion is superseded by `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`, `docs/references/HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`, and the current authoritative Strategy Core. Those material lifecycle behaviors remain HOLD unless a later explicit strategy decision reopens them. No EA execution authority may be derived from the superseded conclusion alone.

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: combination-specific owner timeframe for the accepted post-Re-Entry Momentum / no-Momentum lifecycle exit  
Status: **AUDIT COMPLETE — OWNER TIMEFRAME RESOLVED: REM=H4, RRE=D1, REE=D1; STATIC OUTER-BB TP STILL UNRESOLVED; NO EA CODE CHANGE**

## 1. Question

For each executable BBMA combination setup — REM, RRE and REE — which Re-Entry component/timeframe is the authoritative lifecycle owner for the already accepted post-entry rule:

`VALID RE-ENTRY POSITION -> MOMENTUM PENDING -> SAME-DIRECTION CSM = CONTINUE; REVERSE CONFIRMATION BEFORE SAME-DIRECTION CSM = NO-MOMENTUM FAILURE / CLOSE; OPPOSITE CSM = STRONGER INVALIDATION / CLOSE`

The audit must resolve this independently from the current M17 static TP mapping. Existing code/contract behavior is not treated as proof of source semantics.

No EA source change is authorized by this audit while the P3 runtime candidate remains frozen.

---

## 2. Governance / evidence order

Applied mandatory project order:

`Original Evidence -> Canonical Strategy Core -> Combination Contracts -> Existing M17/M23 behavior`

Evidence groups checked:
- primary operational PDF `Oma ally BBMA - AL.pdf`;
- secondary `BBMA technique.pdf`;
- authenticated strong-provenance `BBMA Home Course Workbook`;
- Finale V05/V06 extracted/original evidence;
- retained Forex Factory extraction register;
- canonical Strategy Core V2;
- current M13, M17 and M23 contracts.

Forum evidence remains supplemental/non-authoritative. Current M17 mapping is examined only after source ownership is established.

---

## 3. Primary PDF — direct combination hierarchy

The primary PDF states that REM/RRE/REE are setups in which three setups form across three different timeframes.

### 3.1 REM

Source wording frames the setup as:

> for a **Re-Entry on H4**, there will be an Extreme on H1 and MLV on M15.

Canonical project signature:

`REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV`

The sentence is written from the perspective of the H4 Re-Entry; H1 Extreme and M15 MHV/MLV are the lower-timeframe structures that accompany/complete that H4 setup.

### 3.2 RRE

Source wording frames the setup as:

> for a **Re-Entry on D1**, there will be a Re-Entry on H4 and an Extreme on H1.

Canonical project signature:

`RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme`

This is decisive for the two-Re-Entry ambiguity: the D1 Re-Entry is the parent setup being described; H4 Re-Entry is a supporting lower-timeframe Re-Entry inside that D1 context.

### 3.3 REE

Source wording frames the setup as:

> for a **Re-Entry on D1**, there will be Extremes on H4 and H1.

Canonical project signature:

`REE = D1 Re-Entry + H4 Extreme + H1 Extreme`

Again, the D1 Re-Entry is the parent setup; H4/H1 are supporting lower-timeframe structures.

### Primary-PDF conclusion

The combination letters are not three equal lifecycle owners. The source describes one higher-timeframe Re-Entry as the setup being completed/read through lower-timeframe structures.

---

## 4. Home Course Workbook — higher-timeframe ownership corroboration

The workbook materially corroborates the parent/child hierarchy:

- when Re-Entry occurs on H4, the trader is told to use the lower timeframes during that H4 Re-Entry window to find additional/confirming entries;
- when D1 has the setup/direction, lower-timeframe retracements are read in the direction of the D1 structure;
- the workbook explicitly says that if D1 and H4 disagree on the broader daily direction, D1 governs the major trend context;
- the post-Re-Entry lifecycle rule is stated as `Arah -> Re-Entry -> Momentum` and `Arah -> Re-Entry -> Tiada Momentum -> Close`.

This supports evaluating the post-Re-Entry continuation/failure lifecycle on the timeframe of the **parent Re-Entry being completed**, rather than allowing a lower-timeframe component to become an independent broker-close authority.

The workbook does not provide a separate rule saying that every lower-timeframe component in REM/RRE/REE has equal authority to close a higher-timeframe Re-Entry position.

---

## 5. Finale V05/V06 reconciliation

Finale V05/V06 strongly corroborate the hierarchy:

- higher-timeframe Re-Entry is read/completed through lower-timeframe Extreme/MHV/Re-Entry structures;
- examples begin from the higher-timeframe Re-Entry and then inspect one or more lower timeframes for supporting structure;
- Re-Entry is the actual setup/entry stage; direction/Extreme/MHV on other timeframes are context/components;
- Momentum follows Re-Entry in the cycle and may generate further Re-Entries.

Important consequence:

A lower-timeframe opposing-looking structure cannot automatically be promoted into a broker-close command against the higher-timeframe parent. Finale explicitly warns that lower-timeframe direction can be part of completion of a higher-timeframe Re-Entry and must be interpreted in the larger-timeframe context.

No Finale evidence was found that gives H1/M15 equal lifecycle-close ownership over an H4 REM, or H4/H1 equal lifecycle-close ownership over a D1 RRE/REE.

---

## 6. Secondary PDF / forum evidence

### Secondary PDF

`BBMA technique.pdf` corroborates general Re-Entry, momentum, BB expansion and multi-timeframe BBMA structure, but does not define a different REM/RRE/REE exit owner hierarchy.

### Forex Factory register

Retained community evidence corroborates multi-timeframe coding and examples, but does not supply a higher-precedence, deterministic post-entry lifecycle-owner rule.

It therefore neither changes nor contradicts the primary/workbook/Finale hierarchy.

---

## 7. Canonical Core / contract reconciliation

### Strategy Core V2

The accepted Core already carries the exact combination identities:

- REM: H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE: D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE: D1 Re-Entry + H4 Extreme + H1 Extreme.

The Core did not previously define post-entry combination lifecycle-exit ownership.

### M13

M13 is collector-only and explicitly does not own SL/TP selection or lifecycle close semantics. It must not choose an exit owner merely from component order.

### M23

M23 is the broker-side lifecycle owner for already-open positions, but its current contract correctly blocks dynamic BBMA closes until a source-owned closed-candle mapping is approved.

The preceding F7 Deterministic No-Momentum Exit audit supplied the event class. This audit supplies the combination-specific source timeframe owner.

---

## 8. Ownership decisions

### CLEO-01 — REM owner

**RESOLVED: H4 RE-ENTRY IS THE LIFECYCLE OWNER.**

Identity:

`REM = H4 Re-Entry [OWNER] + H1 Extreme [SUPPORTING COMPONENT] + M15 MHV/MLV [SUPPORTING COMPONENT]`

Future no-Momentum lifecycle evaluation:
- observation candles: **closed H4 candles** after the REM position is open;
- same-direction H4 source-valid CSM -> continuation confirmed;
- first later H4 reverse-direction confirmation before same-direction H4 CSM -> no-Momentum failure / close;
- source-valid opposite H4 CSM -> stronger invalidation / close.

H1/M15 component events may remain diagnostics/context and may affect future signal/setup validity, but they do not independently direct-close the already-open H4-owned REM position under this lifecycle rule.

Evidence classification: **DIRECT PRIMARY-PDF PARENT FRAMING + STRONG WORKBOOK/FINALE MTF CORROBORATION; deterministic lifecycle routing is a minimal project mapping.**

### CLEO-02 — RRE owner

**RESOLVED: D1 RE-ENTRY IS THE PRIMARY LIFECYCLE OWNER.**

Identity:

`RRE = D1 Re-Entry [OWNER] + H4 Re-Entry [SUPPORTING CHILD RE-ENTRY] + H1 Extreme [SUPPORTING COMPONENT]`

The presence of two `R` components does not create dual broker-close ownership.

Reason:
- the primary PDF explicitly frames RRE as a **D1 Re-Entry** for which an H4 Re-Entry and H1 Extreme appear;
- workbook/Finale teach the smaller timeframe as completion/entry-detail within the larger Re-Entry context;
- treating H4 as an equal post-entry exit owner could terminate a valid D1 Re-Entry merely because a normal lower-timeframe rotation occurs.

Future no-Momentum lifecycle evaluation:
- observation candles: **closed D1 candles** after the RRE position is open;
- same-direction D1 source-valid CSM -> continuation confirmed;
- first later D1 reverse-direction confirmation before same-direction D1 CSM -> no-Momentum failure / close;
- source-valid opposite D1 CSM -> stronger invalidation / close.

H4 Re-Entry remains important provenance/confirmation and may have its own lower-timeframe signal lifecycle, but it is not an independent broker-close owner of the D1-owned RRE trade under this rule.

Evidence classification: **DIRECT PRIMARY-PDF PARENT FRAMING + STRONG MTF CORROBORATION; single-owner routing is a source-derived deterministic architecture mapping.**

### CLEO-03 — REE owner

**RESOLVED: D1 RE-ENTRY IS THE LIFECYCLE OWNER.**

Identity:

`REE = D1 Re-Entry [OWNER] + H4 Extreme [SUPPORTING COMPONENT] + H1 Extreme [SUPPORTING COMPONENT]`

Future no-Momentum lifecycle evaluation:
- observation candles: **closed D1 candles** after the REE position is open;
- same-direction D1 source-valid CSM -> continuation confirmed;
- first later D1 reverse-direction confirmation before same-direction D1 CSM -> no-Momentum failure / close;
- source-valid opposite D1 CSM -> stronger invalidation / close.

H4/H1 Extremes are not Re-Entry owners and do not independently trigger the no-Momentum lifecycle close.

Evidence classification: **DIRECT PRIMARY-PDF PARENT FRAMING + STRONG MTF CORROBORATION; deterministic routing is a minimal project mapping.**

---

## 9. Cross-timeframe close guard

The following guard is required to preserve source hierarchy:

> A lower-timeframe supporting component must not directly close a higher-timeframe parent Re-Entry position merely because its own candle is neutral, reverse-coloured, Extreme, MHV, or opposite-looking.

Reason:
- lower-timeframe structures can be part of the higher-timeframe Re-Entry itself;
- price structure differs by timeframe;
- the source repeatedly tells the trader to read smaller timeframes inside the larger setup rather than treating each timeframe as an autonomous trade thesis.

This guard does **not** make lower-timeframe state irrelevant. Lower components remain valid for:
- pre-entry combination construction/validation;
- provenance/diagnostics;
- future add-on Re-Entries where separately authorized;
- detecting structural developments that may later be reflected in the owner timeframe.

But the accepted F7 no-Momentum broker-close event is evaluated only on the resolved owner timeframe.

---

## 10. Relationship to current M17 mapping

Current M17 happens to use the same Re-Entry timeframe as its static destination source:

- REM -> H4 Re-Entry;
- RRE -> D1 Re-Entry;
- REE -> D1 Re-Entry.

This audit does **not** validate M17 by circular reasoning. The owner mapping above was derived independently from original/workbook/Finale source hierarchy.

Therefore two separate conclusions now coexist:

1. **Lifecycle owner timeframe**  
   REM=H4, RRE=D1, REE=D1 -> **RESOLVED**.

2. **Static outer-BB TP destination**  
   H4/D1 Top/Low BB as universal TP -> **STILL UNRESOLVED CORE PROVENANCE under Path A**.

A source-valid lifecycle owner does not prove that the owner's outer BB is the mandatory static target.

---

## 11. Architecture routing implication

If/when the accepted F7 lifecycle is implemented in a future build:

- M10 remains sole canonical CSM/Momentum producer;
- M12 remains Re-Entry owner/producer;
- M13 remains combination assembler only;
- M14/M15 preserve the exact combination and parent-owner component identity into the executable decision;
- M23 owns the broker `OrderClose()` action for the lifecycle event;
- M24 must recover the exact combination identity, lifecycle owner timeframe, and `MOMENTUM_PENDING` / `MOMENTUM_CONFIRMED` state across restart;
- M15 orchestration may notice a new owner-timeframe closed candle through the existing processing architecture, but no alternative processing clock is introduced;
- M17 initial SL/TP behavior remains untouched by this audit.

Required owner metadata for a future implementation should be explicit and immutable after execution, e.g. conceptually:

- `LifecycleOwnerType = SIGNAL_RE_ENTRY`;
- `LifecycleOwnerTimeframe = H4` for REM;
- `LifecycleOwnerTimeframe = D1` for RRE/REE;
- owner Re-Entry candle identity/provenance;
- current lifecycle state.

Exact field names/storage are an implementation-contract decision, not a Strategy-Core rule.

---

## 12. Remaining F7 gaps

Resolved by this audit:
- REM lifecycle owner = H4 Re-Entry;
- RRE lifecycle owner = D1 Re-Entry;
- REE lifecycle owner = D1 Re-Entry;
- lower-timeframe components are supporting, not equal broker-close owners;
- no-Momentum event must be evaluated on the owner timeframe.

Still unresolved under strict Path A:
- whether a static non-Extreme TP should coexist with the dynamic lifecycle exit;
- exact universal Re-Entry hard-SL provenance beyond current `EA_SAFETY`;
- how to prioritize a future lifecycle close versus an already-resting unproven static TP while Path A remains unresolved;
- final M23/M24 persistence/recovery schema and routing implementation.

---

## 13. Runtime freeze

**NO EA CODE CHANGE NOW.**

The current P3 runtime candidate remains frozen so pending P3 runtime evidence remains attributable to the same build.

This audit is documentation/source-governance only.

A future implementation requires a new build and the mandatory sequence:

`Core/spec update -> M23/M24 contract update -> build identifier -> code patch -> static purity/cross-module audit -> native MetaEditor 0E0W -> fresh runtime validation`.

---

## 14. Final verdict

**REM**  
`H4 Re-Entry` = **LIFECYCLE OWNER**  
`H1 Extreme + M15 MHV/MLV` = supporting components.

**RRE**  
`D1 Re-Entry` = **LIFECYCLE OWNER**  
`H4 Re-Entry + H1 Extreme` = supporting components.

**REE**  
`D1 Re-Entry` = **LIFECYCLE OWNER**  
`H4 Extreme + H1 Extreme` = supporting components.

The accepted post-Re-Entry Momentum/no-Momentum exit event is evaluated on **closed candles of that owner timeframe only**.

This independently reaches the same H4/D1/D1 timeframe hierarchy that the old M17 resolver happened to use, but it **does not validate the old static outer-BB TP formula**.

**Combination-specific lifecycle ownership is now resolved. Static TP provenance and universal hard-SL provenance remain open under Path A.**