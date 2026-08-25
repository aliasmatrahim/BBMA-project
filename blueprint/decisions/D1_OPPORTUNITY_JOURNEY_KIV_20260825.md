# D1 BBMA Opportunity Journey — Historical KIV Design

Date: 2026-08-25  
Status: **SUPERSEDED — EXECUTION APPROVED BY USER ON 2026-08-25**

This file preserves the earlier KIV design record. The user subsequently explicitly authorized activation of this strategy and continuous implementation. The active execution decision is recorded in `D1_OPPORTUNITY_JOURNEY_EXECUTION_DECISION_20260825.md`.

## Preserved design

Two D1 authorities remain separate:

1. **D1 Strategic Owner** — existing MA50-based major-trend authority.
2. **D1 BBMA Opportunity Journey** — current BBMA cycle stage/context used to search H4/H1/M15 for a fresh valid setup.

An opportunity context is never itself a direct `OrderSend` instruction.

### Approved opportunity families

- **Extreme -> TP Wajib Journey** — reversal-confirmed D1 Extreme plus the still-active normal TP-Wajib path is one tactical journey; RAW Extreme is insufficient.
- **CSD Confirmed Journey** — D1 eCSD remains WATCH ONLY; confirmed CSD can activate directional opportunity context.
- **Re-Entry Journey** — confirmed D1 Re-Entry is the primary/strongest opportunity family; further Re-Entry remains the same family.
- **Momentum/CSM -> Retracement -> Re-Entry Journey** — Momentum/CSM is continuation context and cannot be chased; a fresh LTF retracement/Re-Entry is required.

### Watch-only precursors

- D1 MHV/MLV: WATCH ONLY; no independent directional execution authority.
- D1 eCSD: WATCH ONLY; no ordinary LTF execution authority by itself.

### Multi-LTF deduplication

Different timeframe does not automatically mean different trade; **different validated structural sequence does**.

- Same D1 CycleID + same structural chain + H1/M15 completing together -> one opportunity cluster / one trade.
- A later genuinely fresh LTF setup with a distinct source anchor/sequence identity may be considered a new trade.
- Duplicate LTF sequence identity must never execute twice merely because it appears on multiple timeframes.
- Existing portfolio/risk caps remain final constraints.

Identity basis:

`D1 CycleID + OpportunityFamily + LTF structural sequence identity`

Exact REM/RRE/REE signatures remain unchanged unless separately approved.