# C044 Step 4 — Deterministic Restart / Replay Implementation Audit — 2026-08-26

Branch: `d1-owner-dev`

## Status
**IMPLEMENTED / STATIC INTEGRITY PASS / DETERMINISTIC MULTI-CANDLE REPLAY / FEATURE GATE OFF / NATIVE METAEDITOR COMPILE PENDING**

## Source identity
- Build: `Version 4.5.6 - C044 Deterministic Replay Stage`
- Source Git blob after patch: `f0f80decbdbda836c12b6073f5dbc6e347662b13`
- `EnableC044Lifecycle=false` remains locked OFF.

## Closed gap
Step 3 froze any gap larger than one owner-TF candle because current M08/M12 owner state could not prove intermediate events. Step 4 removes that limitation without inferring strategy events.

Each C044-managed trade now persists a replay seed containing the same-direction canonical Re-Entry owner state, both BUY/SELL Extreme lifecycle states, and the exact processed owner-TF cursor.

On restart or any multi-candle gap, every missed fully closed owner-TF candle is replayed oldest-to-newest through existing canonical functions: `UpdateReEntryState()`, `DetectExtreme()` + `UpdateExtremeLifecycle()`, `ResolveOppositeExtremeSupersession()`, and `DetectCSM()` for the approved C044 failed-Momentum test. No Re-Entry, Extreme or Momentum formula is duplicated inside C044.

## Runtime cursor correction
The Re-Entry confirmation candle remains immutable lifecycle provenance / epoch. The processed runtime cursor now initializes to the latest fully closed owner-TF candle when the broker position actually exists, preventing pre-position candles from being treated as missed lifecycle events.

## Fail-closed boundary
Missing/corrupt replay seed, missing exact historical candle, invalid cursor ordering, or unavailable owner data freezes the lifecycle rather than guessing an event.

## Execution authority
No new `OrderClose()` authority was added. M23 remains the only C044 close executor, M20 emergency close retains precedence, and the feature gate remains OFF. Static outer-BB TP therefore remains current live behavior in this staged build.

## Next gate
Native MT4 MetaEditor compile is required for the exact v4.56 source, target **0 errors / 0 warnings**. Then run deterministic replay self-tests before any activation decision.
