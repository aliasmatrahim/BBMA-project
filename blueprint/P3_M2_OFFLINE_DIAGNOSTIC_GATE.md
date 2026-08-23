# P3-M2 Offline Diagnostic / Static Gate

Date: 2026-08-23
Branch: `blueprint-dev`
Status: **M2-01..M2-06 STATIC PASS; M2-07 FINDING REQUIRES DESIGN/SOURCE RESOLUTION; DOWNSTREAM FIX PAUSED**

## Scope completed without live market

### M2-01 Entry-universe audit — PASS
`EntryMode == 2` admits only four execution candidate families in M15:
- `SIGNAL_RE_ENTRY`
- `SIGNAL_REM`
- `SIGNAL_RRE`
- `SIGNAL_REE`

Raw/context families such as Extreme, MHV/MLV, CSD/eCSD/CSM do not independently receive Mode-2 execution authority from `IsEntryModeCandidateAllowed()`.

### M2-02 Source/authority boundary — PASS for implementation boundary
M13 collects components only; M14 validates exact combination signatures and direction consistency; M15 is final signal authority. No score or manual tier is used to grant execution authority.

### M2-03 MTF/cycle boundary — PASS for implemented signatures
Canonical signatures are explicit:
- standalone RE = H1 RE under immediate valid/recovered H4 directional owner;
- REM = H4 RE + H1 Extreme + M15 MLV;
- RRE = D1 RE + H4 RE + H1 Extreme;
- REE = D1 RE + H4 Extreme + H1 Extreme.

### M2-04 REM/RRE/REE sequence/signature — PASS
M14 requires three valid components and same-direction consistency before a combination becomes a validated candidate.

### M2-05 Candidate-to-execution separation — PASS
Flow remains M13 collect -> M14 validate -> M15 select -> M16 exact-owner revalidate -> M17 source-owned SL/TP -> M19/M20 risk/portfolio -> M22 dumb execution. Detector/context components cannot jump directly to OrderSend.

### M2-06 Priority/opposite conflict — PASS with deterministic same-direction selection
If eligible BUY and SELL candidates coexist in the same M15 decision pool, M15 fails closed with `CONFLICT_DIRECTION_VIOLATION` and selects no winner. If candidates are same direction, canonical selection is deterministic by latest component anchor, then sequence start, then sequence hash; scoring/manual tiers do not decide the winner.

## M2-07 Multi-trade / existing-position finding — STOP POINT
A material policy question remains and must not be guessed:

- `MaxTradePerPair = 2` permits a second live position on the same pair when portfolio limits allow it.
- `TradeLockMode = LOCK_OFF` (default) does not compare a new valid decision against an already-open trade's BBMA owner/authority/risk quality.
- `LOCK_SAME_DIRECTION` blocks only an opposite-direction add; it permits additional same-direction positions.
- `LOCK_ONE_POSITION` blocks every second position on the pair.
- Duplicate protection prevents re-executing the same `DecisionID`, but a distinct later BBMA decision can still open another trade.

Therefore the current code has **no source-derived rule that says a second distinct trade must be rejected because its authority/quality is weaker or its incremental risk is worse than the first trade**. Adding such a comparison now would invent strategy/policy unless it is reconstructed from the approved BBMA sources/project governance.

This is directly relevant to the previously observed two-trade same-pair behaviour. The static code is internally consistent with the configured portfolio/TradeLock policy, but the desired BBMA-purity policy for competing *existing position vs new decision* is not yet formally resolved.

## Required resolution before M2-07 fix
Perform an evidence/design resolution specifically for:
1. whether BBMA source permits multiple distinct entries in one directional cycle;
2. whether an existing position owns/locks the pair/cycle;
3. whether a later same-direction RE/REM/RRE/REE may add exposure;
4. whether a later opposite-direction authoritative cycle invalidates, blocks, or coexists with the existing trade;
5. whether incremental account risk alone is an EA safety rejection or whether relative setup quality may ever reject the later setup.

Do **not** implement a score/quality comparison without source authority.

## Downstream status
M2-08 SL/TP mapping, M2-09 risk-overlay separation, M2-10 purity regression and M2-11 diagnostic readiness remain queued. They can continue after M2-07 policy is resolved, or may be audited independently if no code change is made.

Live/runtime evidence remains KIV until market/data execution is available.
