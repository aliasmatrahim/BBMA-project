# D1 BBMA Opportunity Journey — KIV Strategy Design

Date: 2026-08-25  
Status: **KIV / DESIGN HOLD / NOT EXECUTION-AUTHORIZED**

## Purpose
Preserve the user-approved design direction for a future expansion where D1 is treated as a full BBMA journey parent and valid lower-timeframe structures may create additional entries. This document does **not** authorize any current EA execution change.

## Core distinction
Two D1 authorities must remain separate:

1. **D1 Strategic Owner** — existing MA50-based major-trend authority.
2. **D1 BBMA Opportunity Journey** — current BBMA cycle stage/context used to decide whether H4/H1/M15 should be searched for a fresh valid setup.

An opportunity context is never a direct `OrderSend` instruction.

## Refined opportunity families

### 1. Extreme -> TP Wajib Journey
- Treat reversal-confirmed D1 Extreme and its active normal TP-Wajib path as **one tactical journey**, not two separate opportunities.
- Raw Extreme is not sufficient.
- Normal TP-Wajib remains the opposite MA5/MA10 area under the accepted Core rule.
- LTF must still produce a source-valid setup before any future entry could be considered.

### 2. CSD Confirmed Journey
- D1 eCSD alone is **WATCH ONLY** and is not strong enough to activate a normal LTF execution opportunity.
- A mature/confirmed D1 CSD may become a directional opportunity context.
- LTF still owns actual setup/timing.

### 3. Re-Entry Journey
- Confirmed D1 Re-Entry is the **primary / strongest opportunity family**.
- Further Re-Entry after Momentum belongs to the same Re-Entry family, not a separate signal family.
- Exact REM/RRE/REE signatures remain unchanged unless separately approved.

### 4. Momentum/CSM -> Retracement -> Re-Entry Journey
- D1 Momentum/CSM is strong continuation context but must not be chased as an immediate entry.
- Future opportunity maturity requires a fresh lower-timeframe retracement/Re-Entry structure.

## Watch-only precursors

### D1 MHV/MLV
- **WATCH ONLY**.
- MHV/MLV is setup/context and does not provide enough independent directional authority for an LTF opportunity by itself.
- It may be observed as a precursor to later directional maturity.

### D1 eCSD
- **WATCH ONLY**.
- It is early directional information but is not sufficient by itself to activate ordinary LTF execution search.

## Multi-LTF entry deduplication principle
Different timeframe does not automatically mean different trade; **different validated structural sequence does**.

Future execution design must preserve:
- same D1 CycleID + same structural chain + M15 merely completing/timing H1 -> **one trade**;
- H1 and M15 setup completing on the same processing cycle and belonging to the same chain -> canonicalize to **one opportunity cluster**;
- a later genuinely fresh LTF setup with a distinct source anchor / sequence identity may be considered a new trade opportunity;
- duplicate LTF sequence identity must never be executed twice merely because it appears on multiple timeframes;
- existing portfolio/risk caps remain final constraints.

Suggested future identity basis:

`D1 CycleID + OpportunityFamily + LTF SequenceHash/Anchor`

## Execution-change guard
This design is intentionally KIV. Current N1/N2 NMJE remains observation/research only. No change is authorized here to:
- M15 final entry authority;
- D1 strategic gate;
- entry count;
- exact REM/RRE/REE signatures;
- SL/TP;
- risk sizing or portfolio limits;
- broker execution.

Before activation, implement shadow measurement first and compare additional candidate/outcome data by opportunity family and structural sequence.
