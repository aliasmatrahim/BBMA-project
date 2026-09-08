# P3 Step 5 Runtime Evidence Rescan — 2026-09-09

Status: **EVIDENCE HARVEST ONLY / NO CLOSURE PROMOTION**.

## Governance boundary
- Active implementation owner remains `d1-owner-dev@c3318c20970b9c4413b75b46e01976a6e511bf92`.
- Canonical source remains `blueprint/source/BBMA_EA.mq4` / v4.61 F7.
- Runtime/source attribution remains qualified by Issue #133 because the v4.61 label was reused across distinct source variants.
- No primary MT4 restart/reload and no EA source change were performed for this rescan.

## Test C — fresh M22 execution identity persistence
Local MT4 Experts logs contain **21** `[P3S5][EXEC_ID]` runtime records across 2026-09-04, 2026-09-05 and 2026-09-07.

All 21 observed records report:
- `Persist=PASS`;
- `Local=Y`;
- `BrokerHashFound=Y`;
- `BrokerHashMatch=Y`;
- compact broker comment `BBMA|H:<16hex>`.

Twelve of those records carry the runtime label `BBMA_EA_v461_F7`.

Classification: **SUPPORTING RUNTIME EVIDENCE / NOT FORMAL TEST-C PASS** because Issue #133 prevents exact source/binary attribution from the reused v4.61 label alone.

## Test D — restart after fresh hashed trade
Ticket `1622779145` was opened with:
`[P3S5][EXEC_ID] ... Persist=PASS ... BrokerHashMatch=Y ...`

A later initialization recovered that ticket as:
`[P3S5][RECOVERY] Ticket=1622779145 Pair=GBPJPY State=REC_IDENTITY_HASH_ONLY Cause=EXECUTION_HASH_ONLY HashFound=Y FullMeta=N`.

However the execution record is labelled `BBMA_EA_V459_NMJE_FORWARD` while the recovery record is labelled `BBMA_EA_v461_F7`.

Classification: **PARTIAL / CROSS-BUILD RECOVERY EVIDENCE ONLY**. It proves the broker hash survived across a later restart/re-attachment path, but it does not satisfy exact same-candidate Test D.

## Frozen-state / missing-hash evidence
The currently retained local `MQL4/Logs` set contains no `REC_IDENTITY_MISSING_FROZEN` line. The checklist's historical Test-A PASS remains sourced from its previously recorded evidence; this rescan does not replace or weaken that record.

## Closure status
P3 Step 5 remains **IN PROGRESS**. Do not mark Tests C or D PASS from this rescan. Exact build/source/runtime identity plus a same-candidate restart remains required.