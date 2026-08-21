# P3 PairID Registry Hotfix

Status: **APPLIED**

## Problem
`MAX_PAIRS` allowed 20 loaded pairs, but `GeneratePairID()` hashed every
symbol into the same 1..20 namespace. Valid 20-pair portfolios could
therefore collide and make initialization fail closed.

## Fix
- retain `MAX_PAIRS = 20` as the loaded-pair capacity;
- widen PairID namespace to the magic layout's intended two-digit range `1..99`;
- introduce a fixed one-to-one registry for 28 common FX pairs;
- preserve existing non-colliding/default PairIDs and their magic identity;
- assign unique IDs to the previously colliding requested pairs;
- reserve `29..99` as deterministic extension IDs for non-standard symbols;
- keep `ValidatePairIDCollision()` and `ValidateMagicCollision()` fail-closed.

## Requested 20-pair validation
`EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURJPY, GBPJPY, AUDJPY, CADJPY, CHFJPY, NZDJPY, EURGBP, EURAUD, EURCAD, EURCHF, GBPAUD, GBPCAD, AUDCAD`

Result: **20/20 unique PairIDs**.

## Strategy semantics
No BBMA detector, entry, SL/TP, risk, lifecycle, or execution policy was changed.
This is identity/initialization infrastructure only.
