# M11 D1 Major-Trend Owner Contract

Date: 2026-08-24  
Status: **CANONICAL SPECIFICATION — IMPLEMENTED IN ACTIVE OWNER BUILD 5.15; RUNTIME NOT VERIFIED**

## Role
M11 is the sole producer of the project D1 major-trend strategic owner used for **new-entry eligibility**.

Canonical hierarchy:

`D1 strategic owner -> H4 structural/setup parent -> H1/M15 execution structure`

M11 does not detect Re-Entry, Extreme, MHV/MLV, eCSD/CSD or CSM; does not assemble REM/RRE/REE; does not choose a final trade; and does not close broker positions.

## Source basis
Accepted source interpretation:
- MA50 is the major-trend reference and must be confirmed on D1/Daily;
- price above MA50 together with an ascending MA50 establishes bullish major-trend context;
- price below MA50 together with a descending MA50 establishes bearish major-trend context;
- Home Course evidence strengthens D1 as strategic directional authority over an opposite H4 local/setup condition;
- a closed D1 candle governs the next D1 directional reading.

Decision provenance:
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`;
- `blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- `blueprint/decisions/R3_03_D1_TRANSITION_REACHABILITY_RECONCILIATION_20260923.md`.

## Closed-D1 input contract
Only fully closed D1 data may classify the owner.

Required minimum inputs:
- `Close1` = latest fully closed D1 close;
- `MA50_1` = MA50/EMA50 on that same closed D1 candle;
- `MA50_2` = MA50/EMA50 on the immediately previous fully closed D1 candle;
- exact latest closed D1 candle time.

Current/live D1 candle data must not be substituted.

## Canonical owner states
Conceptual states:
- `D1_OWNER_BUY_CONFIRMED`;
- `D1_OWNER_SELL_CONFIRMED`;
- `D1_TRANSITION`;
- `D1_OWNER_UNRESOLVED`.

### BUY confirmed
`Close1 > MA50_1` AND `MA50_1 > MA50_2`.

### SELL confirmed
`Close1 < MA50_1` AND `MA50_1 < MA50_2`.

### D1_TRANSITION
With otherwise valid closed-D1 data, any state that is neither confirmed BUY nor confirmed SELL is transition.

**Reachability clarification:** the accepted MA50 is EMA50 applied to Close, and M11 compares the latest closed EMA50 with the immediately previous closed EMA50. For this exact mapping, same-bar price side and immediate EMA slope have the same sign for every non-equality input:
- `Close1 > MA50_1` implies `MA50_1 > MA50_2`;
- `Close1 < MA50_1` implies `MA50_1 < MA50_2`.

Therefore the former examples “close above MA50 while MA50 is flat/falling”, “close below MA50 while MA50 is flat/rising”, and “first opposite-side cross while immediate slope remains previous-direction” are not reachable non-equality market states under the canonical formula. A naturally reachable valid transition is limited to equality/flat degeneracy permitted by exact input arithmetic and may not occur in finite broker history.

The transition branch is retained as a fail-closed software state. Do not widen it by changing MA type, slope lookback, tolerance, confirmation days, or fallback owner merely to obtain test coverage.

### D1_OWNER_UNRESOLVED
Use only when the required closed-D1 price/MA50 history is missing, invalid or cannot be resolved deterministically.

## Execution-authority meaning
- BUY confirmed -> only BUY-direction strategy candidates may remain eligible, subject to all other BBMA gates.
- SELL confirmed -> only SELL-direction strategy candidates may remain eligible, subject to all other BBMA gates.
- `D1_TRANSITION` -> **block all new strategy entries**.
- `D1_OWNER_UNRESOLVED` -> **block all new strategy entries**.

The previous confirmed D1 direction may be retained as historical/diagnostic provenance during transition, but it is not current entry authority.

## No invented confirmation delay
No fixed two-day/three-day confirmation, timer, percentage, pip buffer, ATR/ADX/RSI, score, session, news or volatility gate is added.

The first later fully closed D1 candle that satisfies BUY or SELL confirmed conditions restores strategic entry authority. If its direction differs from the previous confirmed owner, that closed-D1 state is the atomic major-trend owner handover.

## Relationship to H4
H4 remains the immediate structural/setup parent for H1/M15 timing where applicable, but H4 cannot override:
- a confirmed opposite D1 owner;
- `D1_TRANSITION`;
- `D1_OWNER_UNRESOLVED`.

This is not an `H4 OR D1` model. Both strategic D1 authority and the setup-specific H4 requirements must be satisfied where the entry contract requires H4.

## Relationship to REM/RRE/REE
Exact source signatures are unchanged:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M11 D1 owner is a **separate strategic execution gate**, not an added REM component.

A D1 Re-Entry component in RRE/REE is setup/component identity and does not replace MA50 major-trend authority.

## Snapshot interface to M15/M16
For deterministic downstream use, the M11 result should expose/freeze at least:
- owner state;
- owner direction (`DIR_BUY`, `DIR_SELL`, or none);
- latest closed D1 candle time;
- `Close1`;
- `MA50_1`;
- `MA50_2`;
- validity flag/reason.

M15 consumes this result for new-entry strategic gating. M16 may verify the frozen M11 identity/state but must not create a second MA50 formula.

## Existing live positions
A change to `D1_TRANSITION` is **not** by itself a broker-close rule.

M11 has no position-lifecycle authority. Existing live trades remain governed by the approved lifecycle/SL/emergency-protection contracts.

## Restart/recovery
No persisted D1 owner checkpoint is required merely to make the strategic gate deterministic.

On restart, rebuild the current state from the latest two fully closed D1 MA50 observations and latest closed D1 close. If those inputs cannot be proven, return `D1_OWNER_UNRESOLVED` and block new entries.

No H4/current-candle/last-known-direction fallback is allowed.

## Evidence classification
- D1/MA50 major-trend authority: **DIRECT SOURCE / STRONGLY CORROBORATED**.
- price-side + MA50-slope agreement: **DIRECT PRIMARY-PDF RULE**.
- explicit transition/unresolved software states and fail-closed blocking: **MINIMAL DETERMINISTIC PROJECT MAPPING**.

## Current owner implementation status — reconciled 2026-10-26
The previous implementation-gap statement was written against an older source snapshot and is superseded for static implementation status by owner Build 5.15 at `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`.

- M11 owns `UpdateD1MajorTrendOwner` and the atomic D1 snapshot.
- M27 calls the M11 producer during the closed-M15 processing cycle.
- M15 consumes and freezes the M11 owner; M16 revalidates that frozen identity.
- No second D1 trend formula is added by this reconciliation.

Classification: **STATIC IMPLEMENTATION PRESENT / NATIVE RUNTIME NOT VERIFIED**. This status does not claim broker-connected or Strategy Tester acceptance.

## D1-03 implementation record — atomic M11 snapshot
Build `Version 4.5.1 - D1-03 M11 Snapshot Atomicity` on isolated `d1-owner-dev` closes the M11 snapshot-interface ownership gap without changing the accepted D1 formula.

- M11 now owns `Close1`, `MA50_1`, and `MA50_2` inside `D1MajorTrendOwner` together with state/direction/candle/validity/reason.
- M11 re-evaluates the latest fully closed D1 snapshot on every M15 processing cycle; it does not freeze a same-candle classification across a refreshed broker-history snapshot.
- `current_daily_ema50` / `prev_daily_ema50` remain compatibility mirrors only and are not downstream D1 identity authority.
- M15 freezes only the M11-owned atomic snapshot; M16 verifies only against the current M11-owned atomic snapshot.
- BUY/SELL/TRANSITION/UNRESOLVED semantics and exact REM/RRE/REE signatures are unchanged.
- `blueprint-dev` remains unchanged as a separate historical branch. The active owner source contains the D1 implementation; production/runtime acceptance remains separately gated.
