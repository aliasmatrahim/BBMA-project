# M17 Entry / SL / TP Resolution & Validation Contract

## Status
P0 Step 8 engineering repair is complete and P0 Step 8B is now **APPROVED AT ARCHITECTURE CONTRACT LEVEL**.

The previous source gap is no longer treated as a single undifferentiated problem. The project now explicitly separates:
- `PDF_CORE` rules;
- `FORUM_SUPPORTED` BBMA destination / invalidation practices;
- `EA_SAFETY` deterministic protective-stop engineering.

The detailed authority for the Step 8B decision is:
`blueprint/contracts/M17_SLTP_EXIT_RESOLUTION_CONTRACT.md`

Implementation is still fail-closed until Step 8C patches the active blueprint so every executable decision carries the required source payload.

## Source governance
The user-supplied BBMA PDFs remain the primary authority for BBMA strategy semantics.

ForexFactory BBMA Strategy by Oma Ally material may support destination and invalidation rules but is not promoted to PDF-core authority.

Engineering rules required for autonomous order safety must be labelled `EA_SAFETY` and must not be described as explicit Oma Ally PDF rules.

## Approved TP destination mapping
For current M15 executable decisions:

| Decision | Destination source | BUY TP | SELL TP |
|---|---|---|---|
| H1 RE_ENTRY | H1 Re-Entry | H1 TOP BB | H1 LOW BB |
| REM | H4 Re-Entry | H4 TOP BB | H4 LOW BB |
| RRE | D1 Re-Entry | D1 TOP BB | D1 LOW BB |
| REE | D1 Re-Entry | D1 TOP BB | D1 LOW BB |

The destination must come from the closed-candle snapshot belonging to the validated source component. M17 may not silently substitute a different timeframe or manufacture a fixed-pip TP.

If the destination is already crossed, stale, on the wrong side of entry, or otherwise invalid, the decision fails closed.

## Approved protective hard SL
The universal deterministic hard-SL formula remains an engineering safety concern rather than a PDF-core rule.

Approved architecture principle:
- BUY hard SL is below the most recent structurally relevant confirmed swing-low / lowest wick belonging to the executable decision's source setup;
- SELL hard SL is above the corresponding structurally relevant confirmed swing-high / highest wick;
- anchor data must come from closed candles and from an explicit upstream source payload;
- a small broker-normalized safety buffer may be added and must be labelled `EA_SAFETY`;
- if no unambiguous source-owned anchor is available, resolution fails closed with `REJ_SLTP_UNRESOLVED`.

M17 validates/normalizes this anchor; it must not invent an unrelated lookback swing.

## Dynamic BBMA invalidation
An opposite confirmed CSM/momentum state with BB expansion may invalidate a live BBMA thesis before the protective hard SL.

This is a **post-execution lifecycle exit**, not an initial SL-price builder.

M17 does not own that close action. M23/M24 lifecycle ownership must be audited before dynamic invalidation-close logic is enabled.

M16 may invalidate signal state but must not directly become a broker-position closer unless the blueprint explicitly routes that state to the lifecycle owner.

## No fixed-pip manufacture
The old blueprint helper behavior that manufactured SL/TP from `MaxSLPips` and `MinRRRatio` remains rejected as BBMA source logic.

`MaxSLPips` and `MinRRRatio` remain project rejection filters only:
- `MaxSLPips` may reject an excessively distant source-resolved structural SL;
- `MinRRRatio` may reject a valid resolved pair whose reward-to-risk is too low;
- neither parameter may create the SL or TP.

## Execution reference price
M17 distinguishes broker execution geometry from BBMA strategy semantics:
- BUY market execution reference = ASK;
- SELL market execution reference = BID.

This does not redefine the BBMA setup location.

## Direction-aware geometry
A resolved pair is structurally valid only when:
- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`.

Inverted or unresolved geometry is rejected.

## StopLevel / FreezeLevel side awareness
Direction-aware broker geometry remains mandatory:
- BUY position stop/freeze checks use BID as the close/trigger side;
- SELL position stop/freeze checks use ASK.

## StopLossPoints semantics
After successful source resolution:
`decision.StopLossPoints = abs(EntryPrice - StopLoss) / Point`.

## Ownership guard
M17 owns:
- execution-reference price normalization;
- selection of the approved destination mapping for an already-selected decision;
- TP-level resolution from the validated source snapshot;
- consumption/validation of a source-owned structural SL anchor;
- BUY/SELL SL/TP geometry validation;
- broker StopLevel/FreezeLevel geometry helpers;
- MaxSL and MinRR rejection filters;
- fail-closed source-resolution behavior.

M17 does **not** own:
- BBMA detection;
- final direction selection;
- combination invention;
- arbitrary swing detection unrelated to the selected source payload;
- lot sizing;
- portfolio risk;
- order execution;
- post-entry dynamic invalidation close;
- trailing stop;
- TP2/TP3.

## Current implementation gap — Step 8C
Architecture is now resolved, but the active blueprint implementation still needs a patch so that:
1. each executable decision carries its destination-producing source component/timeframe;
2. each executable decision carries an unambiguous source-owned structural SL anchor;
3. M17 resolves TP from the Step 8B table;
4. M17 validates the protective hard SL without inventing a strategy signal;
5. stale/missing/invalid payload remains fail-closed;
6. lifecycle invalidation is not enabled until M23/M24 ownership is audited.

Until Step 8C is complete, `REJ_SLTP_UNRESOLVED` remains the correct safety behavior for decisions lacking a complete approved payload.

## Existing Step 8 engineering record
Patch:
`blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

Patch commit:
`fe06331500acf5cbce11ce2e411134e9b9b333d2`

Focused patch SHA-256:
`8aeeb013aaa76182f222b31eb0b0dfeb67a2765090cc8dad7dc9a488188e0b8c`

## Step 8B architecture record
Contract:
`blueprint/contracts/M17_SLTP_EXIT_RESOLUTION_CONTRACT.md`

Step 8B contract commit:
`451f98c251f7fb92c23ea45cd122d76561b41c13`

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
