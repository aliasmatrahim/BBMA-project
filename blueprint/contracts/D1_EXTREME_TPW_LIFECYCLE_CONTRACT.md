# D1 Extreme TP-Wajib Lifecycle Contract

Date: 2026-08-26
Branch: `d1-owner-dev`
Status: **ACTIVE SPECIFIC CONTRACT / SUPERSEDES CONFLICTING GENERIC SLTP-LIFECYCLE WORDING FOR `D1_OPP_EXTREME_TPW` ONLY**

## 1. Scope

This contract governs only executable decisions whose frozen D1 Opportunity identity is exactly:

`D1_OPP_EXTREME_TPW`.

It does not redefine:
- normal standalone H1 Re-Entry;
- REM / RRE / REE;
- D1 CSD / D1 Re-Entry / D1 Momentum-ReTrace opportunity families;
- C044 generic post-Re-Entry lifecycle;
- M20 emergency protection.

Where an older generic M17/M22/M23/M24 statement assumes every D1 Opportunity uses the selected Re-Entry as both execution identity and TP owner, this newer specific contract controls the `EXTREME_TPW` case.

## 2. Provenance split

### Strategy semantic owner
D1 Extreme owns normal TP-Wajib semantics.

Tag: `[BBMA-ORIGINAL]` for the underlying Extreme/TP-Wajib lifecycle.

### Execution identity / hard-SL owner
Fresh confirmed LTF Re-Entry owns:
- executable sequence identity / dedup;
- selected entry structure;
- approved structural hard-SL provenance.

Tag: existing BBMA Re-Entry structure plus project execution mapping.

### D1 Opportunity wrapper
Using D1 Extreme/TPW as a D1-to-LTF opportunity family is:

`[BBMA-SOURCE-CONSISTENT][PROJECT-EXTENSION]`.

It must not be presented as a verbatim original Oma Ally family name.

## 3. Entry prerequisites remain unchanged

The current approved D1 Opportunity entry rules remain:
- Mode 2 only;
- D1 Extreme must be source-valid and at least reversal-confirmed under the existing D1 opportunity contract;
- TP-Wajib must still be structurally active at opportunity activation;
- valid/recovered aligned H4 owner is required;
- fresh confirmed H1 Re-Entry is required; M15-only is insufficient for this tactical family;
- M15 remains sole final entry authority;
- D1 CycleID/family attribution cannot manufacture a second execution identity for the same fresh LTF Re-Entry.

No entry condition is added by this lifecycle contract.

## 4. Normal D1 TP-Wajib completion

The semantic event is evaluated from fully closed D1 candles after the frozen D1 Extreme confirmation/source candle.

### D1 Extreme SELL
Normal TP-Wajib completes on the first later fully closed D1 candle whose price range reaches either:
- current same-candle D1 MA5 Low; or
- current same-candle D1 MA10 Low.

### D1 Extreme BUY
Normal TP-Wajib completes on the first later fully closed D1 candle whose price range reaches either:
- current same-candle D1 MA5 High; or
- current same-candle D1 MA10 High.

The MA objective is **dynamic structural evidence**, not a frozen entry-time numeric target.

Mid BB remains farther/maximum context. The first valid opposite MA5/MA10 completion ends the normal TP-Wajib objective; the EA must not require Mid BB afterward merely to extend reward.

## 5. Advanced repeated-Extreme exception boundary

The bounded advanced repeated-LTF/valid-HTF exception does **not** suppress this D1 TP-Wajib lifecycle.

Reason:
- the exception requires an independently valid immediate higher timeframe MHV/MLV or Re-Entry parent;
- the current approved EA hierarchy stops at D1;
- no Weekly/Monthly parent execution architecture is approved.

Therefore `D1_OPP_EXTREME_TPW` remains under normal D1 TP-Wajib semantics.

## 6. M17 initial payload

For a validated `D1_OPP_EXTREME_TPW` lifecycle trade **when the dedicated D1-TPW feature gate is enabled**:
- preserve exact selected LTF Re-Entry source component;
- resolve the approved hard structural SL from that Re-Entry lifecycle;
- set broker TP to `0` / absent;
- mark the payload `D1TPWLifecycleManaged=true`;
- do **not** mark the same trade C044-managed;
- do not resolve the generic Re-Entry outer-BB destination as a substitute TP.

While the dedicated D1-TPW feature gate is OFF:
- a candidate with valid `D1_OPP_EXTREME_TPW` identity must **fail closed** before execution;
- it must never silently fall back to the legacy selected-Re-Entry outer-BB broker TP.

## 7. MinRR / MaxSL / money management

Targetless lifecycle rule:
- `MinRRRatio == 0` -> may continue through normal gates;
- `MinRRRatio > 0` -> fail closed because no deterministic fixed reward coordinate exists at entry.

Do not retain or invent a fake TP just to calculate RR.

Hard-SL ownership remains unchanged:
- MaxSL may reject, never clip/manufacture;
- M21 AutoLot sizes from final actual SL distance;
- M21 remains sole lot-sizing owner.

## 8. M22 execution

M22 remains dumb/idempotent.

For a validated lifecycle payload it may send:
- market entry;
- hard SL > 0;
- TP = 0.

M22 must not:
- calculate D1 MA5/MA10 TP-Wajib;
- decide lifecycle completion;
- change D1 opportunity identity;
- create duplicate entry from D1 family/cycle changes.

## 9. M23 lifecycle close

M23 owns normal broker full-close after receiving/deriving the canonical closed-D1 TP-Wajib completion event under this contract.

Required:
- process D1 lifecycle evidence only on the existing M15 processing clock;
- evaluate/replay fully closed D1 candles oldest -> newest after the persisted cursor;
- latch at most one close event for the first canonical D1 MA5/MA10 completion;
- execute full position close only;
- no partial close, TP2/TP3, trailing or breakeven migration;
- no opposite automatic entry after TPW close.

M20 emergency liquidation has higher precedence than this normal lifecycle close.

## 10. M24 persistence / recovery

M24 must persist/reconstruct enough immutable identity to prove:
- trade ticket / magic / open time;
- trade direction;
- D1 TPW lifecycle-managed flag;
- frozen D1 Extreme source/confirmation candle;
- last processed fully closed D1 candle;
- exit-latched state + latched D1 candle;
- frozen/fail-safe state.

Recovery rules:
- exact closed D1 source/cursor identity must resolve in history;
- missing/corrupt/ambiguous lifecycle identity -> fail frozen;
- a targetless order with both C044 and D1TPW checkpoint families is ambiguous -> fail frozen;
- a targetless order with neither valid lifecycle checkpoint family -> fail frozen;
- restart replay may reconstruct missed D1 candles but must not duplicate a latched/executed close.

## 11. Mutual exclusion with C044

A position has one normal strategy lifecycle exit owner at a time.

For `D1_OPP_EXTREME_TPW`:
- D1 TP-Wajib lifecycle = owner;
- C044 = not owner.

For other approved C044-managed Re-Entry-owned trades:
- C044 may be owner when its own feature gate is later enabled;
- D1 TPW lifecycle = not owner.

Both targetless lifecycle identities on one position are invalid/ambiguous and must fail frozen.

## 12. Runtime activation gate

The dedicated D1 TP-Wajib lifecycle gate must remain OFF until authenticated MT4 broker/demo evidence proves at minimum:
- BUY TPW completion close;
- SELL TPW completion close;
- MA5 and MA10 alternative completion paths;
- restart persistence;
- missed-D1-candle replay;
- duplicate-close prevention;
- M20 emergency precedence;
- no C044/D1TPW lifecycle ambiguity;
- no legacy LTF outer-BB TP fallback.

Native compile/static gates alone do not authorize live activation.

## 13. Ownership invariant

`D1 EXTREME = TP SEMANTIC OWNER`

`FRESH LTF RE-ENTRY = ENTRY / DEDUP / HARD-SL STRUCTURAL OWNER`

`M15 = FINAL NEW-ENTRY AUTHORITY`

`M23 = NORMAL LIFECYCLE BROKER CLOSE OWNER`

`M24 = PERSISTENCE / RECOVERY OWNER`

`M20 = EMERGENCY PRECEDENCE`

No module may collapse those identities merely for implementation convenience.
