# CORE-V2-F7 — MinRR + Protective Payload Resolution Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: `MinRRRatio`, M17 validation payload, M21/M19 compatibility, M22 `OrderSend()`, and restart implications after the Path-A decision that Re-Entry-owned trades have no source-proven universal static TP  
Status: **AUDIT COMPLETE — TARGETLESS PROTECTIVE PAYLOAD RESOLVED FOR RE-ENTRY-OWNED TRADES; MINRR DISABLED FOR THOSE TRADES; M22 TP=0 PATH AUTHORIZED; NO EA CODE CHANGE WHILE P3 CANDIDATE IS FROZEN**

## 1. Question

After the preceding F7 audits established that:

- standalone H1 Re-Entry / REM / RRE / REE are Re-Entry-owned executable trades;
- their primary Strategy-Core profit-taking mechanism is the post-Re-Entry Momentum/no-Momentum lifecycle;
- the current H1/H4/D1 outer-BB static TP mapping is not proven as universal BBMA Core;

what should happen to:

1. `MinRRRatio`;
2. M17 validation when `TakeProfit == 0` by design;
3. M21 lot sizing and M19 prospective risk checks;
4. M22 `OrderSend()` payload and pre-send guards;
5. M24 restart geometry, which currently assumes a positive TP?

This audit resolves architecture/specification only. The current compiled P3 runtime candidate remains unchanged.

---

## 2. Mandatory source + GitHub preflight

Applied project order:

`Original evidence -> canonical Strategy Core -> F7 decisions -> contracts -> active source -> runtime state`

Live governance checked:
- `PROJECT_INSTRUCTIONS.md`;
- `docs/references/SOURCE_INDEX.md`;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- current `CURRENT.md` / `MASTER_QUEUE.md` state;
- M17, M19, M21, M22, M23 and M24 contracts;
- active `blueprint/source/BBMA_EA.mq4`.

Relevant source evidence checked:
- primary `Oma ally BBMA - AL.pdf`;
- authenticated strong-provenance `BBMA Home Course Workbook`;
- secondary BBMA reference;
- Finale V05/V06 / Master Rule Index;
- prior F7 workbook reconciliation, deterministic no-Momentum exit, combination owner, and static-TP coexistence audits.

No current-code behavior is used as proof of BBMA semantics.

---

## 3. Source finding on Risk:Reward

### 3.1 The source recognizes Risk:Reward qualitatively

The primary PDF says there is no reason to enter at an MLV-associated Extreme when the Risk:Reward is low and instead points to the later retest / Re-Entry locations as better entries.

This establishes only a **qualitative trade-location principle**: some entry locations are poor because reward relative to risk is poor.

It does **not** establish:
- a universal numeric minimum RR such as 1.0, 1.5 or 2.0;
- a formula requiring a static TP to compute reward for every Re-Entry;
- a rule that a valid Re-Entry/REM/RRE/REE must be rejected because a projected outer-BB target gives RR below a configured threshold.

### 3.2 Re-Entry exit evidence is lifecycle based

The workbook repeatedly teaches:

`Arah -> Re-Entry -> Momentum`

and:

`Arah -> Re-Entry -> Tiada Momentum -> Close / TP`

The primary PDF and Finale corroborate:

`Re-Entry -> Momentum/CSM -> further Re-Entry -> eventual cycle transition`.

Therefore there is no source-proven deterministic reward distance at entry for the currently executable Re-Entry-owned trades once the unsupported universal outer-BB TP is removed.

### 3.3 MinRR conclusion

A numeric `MinRRRatio` applied to a fabricated or non-Core target would itself become a hidden strategy gate derived from an unproven TP.

Under strict Path A this is not allowed.

---

## 4. Current implementation mismatch

The active source still implements the old complete SL+TP assumption.

### M17
Current behavior:
- resolves outer-BB `destination`;
- requires both `StopLoss > 0` and `TakeProfit > 0`;
- requires BUY `SL < Entry < TP` / SELL `TP < Entry < SL`;
- computes `tpDistance`;
- rejects when `tpDistance / slDistance < MinRRRatio`;
- applies broker stop-distance validation to both SL and TP.

### M22
Current behavior:
- `SendOrderWithRetry()` rejects `takeProfit <= 0`;
- `ProcessEntry()` rejects `decision.TakeProfit <= 0`;
- `OrderSend()` receives the positive TP;
- `TradeInfo.initial_take_profit/current_tp` are populated from the broker order.

### M24
Current recovery behavior requires:
- `initial_take_profit > 0`;
- BUY `SL < Entry < TP`;
- SELL `TP < Entry < SL`.

A future targetless Re-Entry order would therefore be incorrectly marked `REC_RECOVERY_INVALID` after restart unless M24 is changed in the same future implementation series.

Classification:

**BLUEPRINT / IMPLEMENTATION GAP RELATIVE TO RESOLVED F7 PATH-A SEMANTICS.**

This is not a reason to modify the frozen P3 candidate now.

---

## 5. Resolution — protective payload model

### MP-01 — Re-Entry-owned executable payload

**RESOLVED.**

For current executable Strategy-Core decisions:
- standalone H1 `RE_ENTRY`;
- `REM`;
- `RRE`;
- `REE`;

the future strict-Path-A broker payload is:

`EntryPrice = live execution reference`

`StopLoss = approved protective hard stop (EA_SAFETY; exact universal Core provenance still not claimed)`

`TakeProfit = 0.0`

`Exit authority = M23 lifecycle using the resolved owner-timeframe Momentum/no-Momentum state`

This audit does not reopen or upgrade the hard-SL source classification. The current hard stop remains an explicit safety mechanism, not a universal Oma Ally Core rule.

### MP-02 — Explicit TP-absence semantics

**RESOLVED.**

`TakeProfit == 0.0` must mean **INTENTIONALLY NO STATIC TP**, not `UNRESOLVED TP`.

The future decision payload should make this explicit rather than relying only on a magic numeric zero.

Minimum metadata concept:
- `HasStaticTakeProfit = false` for Re-Entry-owned lifecycle trades; or
- equivalent explicit exit-policy state.

Exact field name is an implementation detail.

M22 must consume that state; it must not infer strategy policy on its own.

### MP-03 — M17 validation boundary

**RESOLVED.**

For lifecycle-managed Re-Entry-owned decisions, M17 must validate the **protective payload**, not a mandatory SL+TP pair.

Required checks:
- valid direction;
- valid live `EntryPrice`;
- source/owner component identity required for the protective stop remains resolvable;
- `StopLoss > 0`;
- BUY: `StopLoss < EntryPrice`;
- SELL: `StopLoss > EntryPrice`;
- positive SL distance;
- `MaxSLPips` cap remains applicable as project safety policy;
- broker StopLevel/price-normalization checks apply to the SL;
- `TakeProfit == 0` is valid when the payload explicitly declares lifecycle-managed/no-static-TP;
- no TP geometry, TP StopLevel, static reward-distance, or target-staleness test is run in that mode.

M17 must not manufacture a placeholder TP merely to satisfy legacy validators.

### MP-04 — `MinRRRatio`

**RESOLVED: DO NOT APPLY TO LIFECYCLE-MANAGED RE-ENTRY TRADES.**

Reason:
- reward distance is not source-deterministic at entry;
- the old ratio depended on the now-unproven outer-BB static TP;
- inventing an estimated lifecycle reward would violate Path A;
- setting the user's input to zero manually is not an acceptable architecture control.

Future behavior:
- `MinRRRatio` must be bypassed structurally for standalone H1 Re-Entry / REM / RRE / REE;
- these decisions must never emit `REJ_INVALID_RR` merely because they have no static TP;
- no synthetic reward amount is created.

Because all currently executable decision types are Re-Entry-owned, `MinRRRatio` becomes **dormant for the current executable strategy set** under Path A.

Input/UI follow-up:
- preferably remove it from the active visible trading inputs or clearly mark it compatibility-only/inactive;
- do not require users to remember to set `MinRRRatio=0`.

If a future source-proven static-target executable setup is introduced, MinRR may be reconsidered as an explicitly labelled project rejection policy for that target-bearing setup, not automatically as BBMA Core.

---

## 6. M21 and M19 compatibility

### MP-05 — M21 lot sizing

**NO STRATEGY LOGIC CHANGE REQUIRED.**

Current AutoLot sizing uses:

`risk_per_lot = abs(EntryPrice - StopLoss) * TickValue / TickSize`

It does not need TP to size risk.

Required future contract clarification only:
- M21 consumes an M17-approved **Entry + protective SL** payload;
- it must not require or synthesize TP;
- lot sizing remains based on downside risk only.

### MP-06 — M19 prospective risk

**NO CORE CALCULATION CHANGE REQUIRED.**

M19 total-risk accounting uses each trade's Entry/SL distance and the proposed trade's Entry/SL/lot.

It does not require positive TP for risk exposure calculation.

Important ownership clarification:
- the active numeric `MinRRRatio` check currently lives in **M17 validation**, not M19;
- M19 should remain risk/exposure-only and must not inherit a new reward estimator.

---

## 7. M22 OrderSend resolution

### MP-07 — `OrderSend()` with TP=0

**TECHNICALLY AUTHORIZED / REQUIRES RUNTIME VERIFICATION ON THE PROJECT BROKER.**

MetaQuotes' MQL4 reference includes an official market-order example calling:

`OrderSend(..., stoploss=0, takeprofit=0, ...)`

This demonstrates that the MQL4 API accepts zero stop parameters as an order payload shape. The project design will be stricter: non-zero protective SL + zero TP.

Official reference:
`https://docs.mql4.com/runtime/resources`

Therefore the future M22 path may pass:

`OrderSend(pair, direction, lot, executionPrice, Slippage, stopLoss, 0.0, ...)`

for an explicitly authorized lifecycle-managed decision.

Broker/runtime acceptance still requires direct MT4 validation in the eventual new build.

### MP-08 — M22 pre-send guards

**RESOLVED.**

M22 remains dumb executor.

It should validate only payload consistency, for example conceptually:
- `stopLoss > 0` always;
- lifecycle/no-static-TP payload -> `takeProfit == 0` allowed/expected;
- static-target payload, if any future approved type exists -> positive TP required;
- negative TP is invalid;
- M22 must never invent a TP.

The current unconditional checks:
- `takeProfit <= 0 -> reject`;
- `decision.TakeProfit <= 0 -> reject`;

must therefore be removed/replaced in the future implementation.

M22's execution identity, retry, trade-lock, deviation and idempotency behavior do not depend on TP and remain unchanged.

---

## 8. M24 recovery consequence

### MP-09 — targetless geometry

**REQUIRED FOLLOW-UP BEFORE IMPLEMENTATION CAN BE CALLED RESTART-SAFE.**

M24 currently treats `TP <= 0` as invalid geometry.

Future recovery must distinguish the execution payload mode.

For an authorized lifecycle-managed position:
- BUY valid protective geometry: `SL < Entry`, `TP == 0`;
- SELL valid protective geometry: `SL > Entry`, `TP == 0`.

If a static-target mode is ever authorized separately, its old three-point geometry may remain applicable to that mode.

M24 must not infer that TP was accidentally lost merely because `OrderTakeProfit()` returns 0 for a lifecycle-managed trade.

### MP-10 — identity dependency

Targetless lifecycle management increases the importance of durable strategy identity.

Recovery must be able to prove, without fabrication:
- this trade is lifecycle-managed;
- lifecycle owner timeframe/component;
- lifecycle state / last processed owner candle once M23/M24 lifecycle is implemented.

If those cannot be recovered safely, freeze ordinary lifecycle actions rather than fabricate a static TP or close rule.

---

## 9. Failure-mode / safety consequences

The future design removes broker-side automatic profit-taking for these Re-Entry-owned trades. Therefore normal profit exit depends on EA lifecycle processing.

Required engineering protections:
- broker-side hard SL remains present;
- M20 emergency liquidation keeps precedence;
- M22 execution identity remains restart-stable;
- M24 lifecycle recovery must be deterministic;
- duplicate close attempts must be idempotent;
- market/broker failure while attempting M23 lifecycle close must be retried safely according to a future lifecycle execution contract.

These are EA reliability controls, not new BBMA strategy rules.

---

## 10. What is NOT changed by this audit

- no EA source file is changed;
- no current broker TP is removed from the frozen P3 candidate;
- no new build identifier is created;
- no current runtime evidence is invalidated;
- no hard-SL formula is promoted to Strategy Core;
- no trailing stop, breakeven, TP2 or TP3 is introduced;
- normal Extreme TP-Wajib remains a separate accepted Core rule.

---

## 11. Future implementation dependency chain

After the current P3 runtime candidate is closed, the F7 implementation sequence should be:

1. update canonical Core/spec for accepted Re-Entry lifecycle exit semantics;
2. redesign M17 contract from mandatory `SL+TP` to explicit protective-payload / exit-policy validation;
3. structurally disable `MinRRRatio` for lifecycle-managed current executable decisions;
4. update M22 contract and code to allow authorized `TP=0` without inventing a target;
5. update M23 contract/code for owner-timeframe lifecycle close;
6. update M24 recovery geometry + lifecycle identity/state recovery;
7. recheck M21/M19 invariants (Entry/SL risk remains unchanged);
8. assign a new unique left-aligned build/header identifier;
9. native MetaEditor compile at 0 errors / 0 warnings;
10. static Strategy-Core / cross-module regression;
11. fresh runtime validation including TP=0 OrderSend, restart recovery, same-direction CSM continuation, no-Momentum reverse close, opposite CSM close, and emergency-close precedence.

---

## 12. Final verdict

For current executable Re-Entry-owned trades under strict Path A:

**Reward model at entry:**
`NO SOURCE-PROVEN STATIC REWARD DISTANCE`

**MinRRRatio:**
`BYPASS / INACTIVE FOR CURRENT EXECUTABLE RE-ENTRY-OWNED TRADES`

**M17 payload:**
`ENTRY + PROTECTIVE SL + EXPLICIT NO-STATIC-TP MODE`

**Broker TP:**
`0.0`

**M21 sizing:**
`UNCHANGED — ENTRY/SL BASED`

**M19 total risk:**
`UNCHANGED — ENTRY/SL/LOT BASED`

**M22:**
`ALLOW EXPLICITLY AUTHORIZED TP=0; NEVER MANUFACTURE TP`

**M24:**
`MUST LATER ACCEPT TARGETLESS PROTECTIVE GEOMETRY AND RECOVER LIFECYCLE IDENTITY`

**Current code status:**
`KNOWN GAP / DEFERRED UNTIL P3 RUNTIME FREEZE CLOSES`

This resolves the MinRR and broker protective-payload question without inventing a reward target simply to preserve a legacy RR filter.