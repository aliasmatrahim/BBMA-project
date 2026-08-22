# CORE-V2-F4 — H4 Parent/Directional Owner Implementation Audit

Date: 2026-08-22
Status: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**
Branch: `blueprint-dev`

## Scope
Implements the resolved `CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md` contract without changing REM/RRE/REE signatures or weakening F1/F2/F3 semantics.

## Implemented owner contract
- Standalone H1 Re-Entry now requires an active, recovered, same-direction H4 authoritative owner.
- H4 eCSD, CSD and CSM/Momentum can establish/advance directional ownership; classification precedence is CSM > CSD > eCSD for one closed H4 candle.
- A valid opposite authoritative event performs atomic handover. BUY and SELL owners are never simultaneously authoritative.
- A neutral H4 candle preserves the inherited owner; owner age alone does not expire it.
- Raw H4 Extreme/MHV do not establish the directional owner.
- D1, EMA50/Mid-BB, candle colour and absence-of-opposite are not fallback owners.
- Same-direction H4 Re-Entry is recorded as inherited lifecycle progress but does not manufacture direction from NO_OWNER.

## Standalone H1 execution gate
`BuildConfirmedReEntryCandidate()` receives the pair's H4 owner and rejects standalone H1 Re-Entry candidate construction unless recovery is complete, state is `H4_OWNER_ACTIVE`, owner is valid, and directions match. Combination signatures are untouched.

## Recovery
- Terminal Global Variables persist the latest independently verifiable H4 owner-producing event: direction, source family and closed-H4 candle time.
- Checkpoints are verified by exact closed-H4 timestamp plus re-running the same eCSD/CSD/CSM classifier at the provenance candle.
- Invalid/missing checkpoints are not trusted.
- Recovery replays closed H4 history chronologically, applying the same owner/handover rules used at runtime.
- If history cannot prove an owner, the pair resolves to `H4_OWNER_NONE`; standalone H1 execution remains blocked.
- Ambiguous simultaneous BUY/SELL authoritative classification is fail-closed to `NO_OWNER`.

## Static invariants
- explicit H4 owner/recovery/no-owner states exist;
- one per-pair owner exists, not separate simultaneous BUY/SELL owners;
- checkpoint verification and closed-H4 replay are wired before strategy execution;
- runtime update uses closed H4 data and preserves neutral-candle inheritance;
- standalone H1 Re-Entry checks H4 direction compatibility;
- no generic H4 owner TTL or D1/EMA fallback is introduced;
- same-direction H4 Re-Entry can inherit but cannot establish a no-owner direction;
- source lexical brace/parenthesis/bracket sanity passes.

## Remaining verification
1. Native MetaEditor compile must report **0 errors / 0 warnings** for the F1-F4 integrated source.
2. Runtime traces: fresh start with no provable history -> NO_OWNER block; eCSD establishes owner; neutral H4 preserves owner; same-direction H1 Re-Entry admitted; opposite H1 blocked; opposite H4 eCSD/CSD/CSM atomic handover; same-direction H4 Re-Entry inheritance; restart with valid checkpoint + replay; corrupt checkpoint fallback replay; insufficient history -> NO_OWNER.
3. Re-run Strategy Core V2 audit after F5/F6 closure.

Decision provenance: `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`.
