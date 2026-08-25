# M17 SELL Spread-Buffer Execution Normalization Decision — 2026-08-25

Status: **LOCKED / APPROVED / DEFERRED FOR NEXT SOURCE UPDATE / NO CURRENT MQL4 CHANGE**

## Purpose
Preserve the user-approved broker-execution normalization for SELL protective stops without redefining BBMA Strategy Core structural SL semantics.

## Provenance / classification
- BBMA source continues to define the structural Re-Entry wick/structure.
- This decision is **EA_SAFETY / broker execution normalization**, not a new BBMA Core trading rule.
- The current M17 source-candle structural anchor remains authoritative.

## Locked behavior
### BUY
- Keep the current BUY structural hard SL behavior unchanged.
- No spread buffer is added to BUY SL.
- Existing BUY AutoLot/risk sizing flow remains unchanged.

### SELL
1. Resolve the approved BBMA structural SELL SL exactly as currently specified from the source-owned Re-Entry wick plus the existing one-point engineering buffer.
2. Read the **current frozen spread snapshot** from the same preflight `RiskValidationSnapshot` used for execution/risk validation.
3. Convert current spread to project pips using the canonical pip-price helper.
4. Compute the SELL spread buffer by **rounding upward to the next whole pip**, with a **minimum buffer of 2.0 pips**:

   `SpreadBufferPips = max(2.0, ceil(CurrentSpreadPips))`

   Examples:
   - 0.6 pip -> 2 pip
   - 1.0 pip -> 2 pip
   - 1.1 pip -> 2 pip
   - 1.8 pip -> 2 pip
   - 2.0 pip -> 2 pip
   - 2.1 pip -> 3 pip
   - 2.9 pip -> 3 pip
   - 3.0 pip -> 3 pip
5. Convert the rounded buffer back to price units and place the SELL broker hard stop farther above the structural SL:

   `SELL BrokerSL = StructuralSL + SpreadBufferPrice`

6. The spread value is frozen from the entry/preflight snapshot. Do not chase/rewrite the broker SL later merely because live spread changes after entry.
7. `MaxSpreadPips` remains an **entry rejection filter only** and must not be used as the SL buffer.

## Money-management consequence
- In `MM_AUTO_LOT`, the adjusted SELL broker SL must be finalized **before M21 lot sizing** so M21 naturally recalculates a smaller lot from the larger actual entry-to-SL distance.
- The intended account-risk percentage therefore remains unchanged, subject to normal broker lot-step/min/max constraints.
- In `MM_FIXED_LOT`, lot size does not auto-reduce; the wider SELL stop therefore increases monetary risk distance. Existing risk/portfolio gates remain authoritative.
- No manual multiplier or second independent lot-reduction rule is added.

## RR consequence
- RR must be recalculated from the final broker-side SELL SL distance after spread normalization.
- Do not preserve an older nominal RR by manufacturing a new TP.

## Explicit non-scope
This decision does **not** yet change:
- BUY SL;
- BBMA structural wick definition;
- TP mapping;
- SELL TP Bid/Ask normalization;
- signal detection;
- D1/NMJE authority;
- entry timing;
- risk percentage inputs;
- `MaxSpreadPips` semantics;
- live-position trailing/dynamic SL behavior.

Any SELL TP Bid/Ask normalization remains a separate audit/decision and cannot be bundled into this implementation without explicit approval.

## Implementation placement
Target the next approved M17/M21 source update after the current runtime/evidence attribution checkpoint is preserved.

Implementation order:
1. preserve current structural SL as a separate intermediate value;
2. compute frozen current spread in pips from the preflight snapshot;
3. apply `max(2, ceil(spreadPips))` to SELL only;
4. normalize final SELL broker SL to broker tick size/digits in the safe outward direction;
5. run existing directional geometry / StopLevel / MaxSL / RR validation on the final broker SL;
6. let M21 size AutoLot from the final broker SL distance;
7. add diagnostics showing structural SL, raw spread, rounded spread buffer, final broker SL and resulting lot;
8. native MetaEditor 0 errors / 0 warnings;
9. focused static regression proving BUY path unchanged and SELL-only normalization;
10. broker/demo runtime evidence on at least one JPY cross and one non-JPY FX pair.

## Governance
- This decision is locked by explicit user approval on 2026-08-25.
- Do not silently weaken, broaden or remove the SELL-only scope.
- Do not promote the buffer rule into `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` as source-authored BBMA semantics.
