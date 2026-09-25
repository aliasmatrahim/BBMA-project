# NMJE V2 Build 5.17 — P2/P5 Closure + N3 Active Selection Implementation — 2026-09-26

Status: **IMPLEMENTED / DEFAULT OFF / STATIC+NATIVE+TARGETED PASS / FULL RUNTIME VALIDATION PENDING**

Issue: #101
Owner base: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`
Implementation lineage: Build 5.16 preparation -> Build 5.17 active-policy implementation.

## Build identity
- Build: `5.17`
- Build tag: `V517_NMJE_ACTIVE_SELECTION_POLICY_20260926`
- Source rev: `NMJE_ACTIVE_SELECTION_POLICY_001_20260926`
- MQ4 SHA-256: `B28E8C7F493D96899A681397FECE14876EFAAF7F73435274E5A3EA6E33394F9F`
- Native EX4 SHA-256: `21B93E75B7465C41737CB5CAF64912DC9510BC599FA27564748DCE54E0C9E4A5`

## P2 closure
User authorization on 2026-09-26 creates the explicit project policy required by the earlier HOLD record.

Active N3 selection can run only when:
- at least two candidates are already eligible;
- all candidates compete in one same-direction M15 decision;
- existing D1 authority already permits them;
- V1 journey is valid/resolved and `ALIGNED` or `SUPPORTING`;
- canonical M5 semantic context is resolved and `ALIGNED` or `SUPPORTING`.

Comparator is bounded and lexicographic:
1. canonical structural prefix length;
2. canonical distinct stage count;
3. existing M15 comparator fallback.

No weighted score, probability, timeframe vote or new detector formula is introduced. Sole-candidate eligibility/timing is unchanged.

## P5 closure
M5 has **no executable hard-conflict authority**.
- opposite confirmed M5 Re-Entry remains `UNRESOLVED`;
- opposite candidate Re-Entry / active Extreme remain `BUILDING`;
- multiple mapped M5 states remain `UNRESOLVED`;
- M5 never independently rejects a trade.

Existing V1 owner-level conflict classification remains unchanged.

## N3 implementation
New input:
`EnableNMJESelectionPolicy=false`

The implementation hook is inside M15 `PriorityEngine_Atomic`.
M15 remains final decision owner. NMJE does not call risk, sizing, OrderSend, OrderClose or lifecycle authority.

Protected downstream functions remain exact to Build 5.16:
- `InvalidationEngine_Atomic`
- `CheckRiskBeforeTrade`
- `IsSignalAllowed`
- `ResolveExecutionReferencePrice`
- `ResolveSelectedSLTPSourceComponent`
- `IsApprovedSLTPSourceComponent`
- `SendOrderWithRetry`
- `RunEntryPreflightAndExecute`

## Validation completed
- Build 5.17-only `git diff --check`: PASS.
- Native MetaEditor compile: **0 errors / 0 warnings**.
- Targeted active-policy regression: **PASS**.
- Full repository Python suite using project Python 3.12 runtime: **72/72 PASS**.
- Specialized GitHub NMJE authority invariant check: implementation-head run #19 core verification step PASS; final evidence-head check to be re-run automatically after this checkpoint commit.
- Broker primitive ownership: one `OrderSend` call remains.
- Protected downstream hashes: exact to Build 5.16.

Targeted policy model proves:
- policy disabled -> legacy winner;
- one candidate -> unchanged;
- non-positive/unresolved context -> legacy winner;
- positive coherent context -> richer bounded structural candidate may win;
- equal structural completeness -> legacy comparator wins.

## Not yet claimed
- no Strategy Tester A/B run with `EnableNMJESelectionPolicy=true` has been accepted yet;
- no multi-pair active-policy regression accepted yet;
- no demo-forward active-policy execution/outcome accepted yet;
- no restart/provenance/order-log active-policy validation accepted yet;
- no production/release readiness claim.

## Classification
P2 active selection policy: **CLOSED / IMPLEMENTED / DEFAULT OFF**.
P5 M5 true-conflict policy: **CLOSED — NO M5 HARD CONFLICT AUTHORITY**.
N3 active selection implementation: **IMPLEMENTED / DEFAULT OFF**.
Remaining work: **TESTING / VALIDATION ONLY before activation acceptance**.
