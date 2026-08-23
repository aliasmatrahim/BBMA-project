# Reconciliation — D1 Major Trend vs H4 Immediate Parent

## Status
RESOLVED AT STRATEGY-MODEL LEVEL / IMPLEMENTATION IMPACT REQUIRES FOLLOW-UP AUDIT

## Source-derived findings
1. BBMA Home Course explicitly states that major trend is MA50, MA50 works properly from minimum D1, H4 does not carry the major trend, and if D1 says BUY while H4 says SELL, follow D1.
2. The original Oma Ally PDF likewise says to always confirm trend on MA50 on the Daily chart.
3. Home Course separately teaches that when H4 provides a setup/direction, traders move to lower timeframes to find same-direction additional entries; within an H4 candle/three-candle movement, lower-TF setups are used for additional entries.
4. Home Course also says that when D1 has a SELL setup, lower-timeframe retracements are SELL opportunities and repeatedly instructs to follow the major trend.

## Reconciliation
There is no true contradiction if the two concepts are assigned different roles:

- D1 = MAJOR-TREND / STRATEGIC DIRECTION AUTHORITY.
- H4 = IMMEDIATE SETUP / STRUCTURAL PARENT for H1/M15 timing where the H4 setup is aligned with D1.
- H1/M15 = lower-timeframe completion, timing and additional-entry layers.

Therefore H4 may be the immediate parent of a lower-TF entry, but it must not be allowed to override a valid opposite D1 major-trend state merely because H4 has its own local directional setup.

Canonical hierarchy:
D1 major trend/context -> H4 setup parent -> H1 signal/completion -> M15 fine entry/additional entry.

## Conflict rule
When D1 and H4 disagree:
- D1 has strategic directional priority under the Home Course wording.
- An H4 counter-D1 condition should be interpreted as local retracement/countertrend structure unless source-valid evidence establishes a D1 transition/reversal.
- A lower-TF entry must not inherit counter-major-trend execution authority solely from H4.

## Important distinction
This does NOT mean every executable BBMA signature must literally contain a D1 Re-Entry component.

REM remains structurally H4 Re-Entry + H1 Extreme + M15 MHV/MLV. D1 is a separate major-trend context/gate, not an added fourth component of the REM signature.

RRE/REE already contain D1 structurally, so their D1 ownership remains intrinsic to those signatures.

## Implementation consequence to audit
The existing project decision that standalone H1 Re-Entry needs an authoritative H4 owner remains useful but is incomplete after Home Course reconciliation if it permits H4 to authorize execution against a valid D1 major trend.

Required next audit:
- inspect current D1 trend/MA50 calculation and semantics;
- inspect H4-owner execution gates for standalone H1 RE and REM;
- determine whether D1 should be a hard directional gate, a setup-quality classification, or requires a deterministic transition state before counter-D1 trades can execute;
- do not modify code until the exact D1 Boolean/transition semantics are source-faithfully resolved.

## Non-rules
Do not infer from this reconciliation that:
- every H4 signal against D1 is invalid as a detector;
- D1 must be a Re-Entry for every trade;
- W1 is mandatory for every entry;
- H4 has no useful parent role;
- a raw price-vs-MA50 snapshot alone is sufficient to define every D1 reversal transition without further audit.
