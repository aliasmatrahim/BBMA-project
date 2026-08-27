# NMJE Dependency Hardening Audit — DEP-A03 M08 Extreme Owner/Lifecycle

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE
Runtime-candidate rule: preserve the currently running/frozen EA candidate; findings below are queued for the appropriate implementation window.

## Scope
Review M08 as an upstream canonical Extreme lifecycle owner consumed by NMJE. Focus: RAW detection, maturity progression, frozen body/reference identity, invalidation, opposite-Extreme supersession, terminal-state monotonicity, and restart/replay readiness. This audit does not add strategy filters.

## Source/contract baseline
Canonical F2 lifecycle is already resolved as:
`RAW EXTREME -> REVERSAL-CONFIRMED -> RETEST PHASE -> RETEST/ENTRY-READY`, with accepted outside-BB/Momentum invalidation taking precedence. REM/REE require at least reversal-confirmed Extreme; standalone Extreme requires retest/entry-ready. No fixed candle/session expiry is allowed for canonical Extreme lifecycle.

## Baseline verdict
M08 is materially aligned with the current F2 canonical specification and is a strong upstream owner for N1/N2 observation. It is not yet fully hardened as an immutable lineage source for mandatory N3 enforcement.

### Confirmed strengths in current source
- RAW detector is isolated from maturity logic; RAW alone is not exported as an executable combo component.
- only closed valid source-TF candles advance the lifecycle;
- first later same-TF directional reversal candle promotes RAW -> REVERSAL-CONFIRMED;
- provisional reversal-body anchor can evolve only before retest begins;
- retest-start freezes the body anchor and excludes the trigger candle from anchor construction;
- first valid range interaction with frozen body anchor OR relevant MA5 completes RETEST/ENTRY-READY;
- invalidation is evaluated before maturity promotion;
- no fixed lifecycle expiry is applied; MaxWaitBars_Extreme is explicitly downstream freshness only;
- opposite reversal-confirmed Extreme can atomically supersede the older mature opposite cycle;
- equal opposite confirmation times remain ambiguous and are left fail-closed downstream;
- VOID and SUPERSEDED are terminal until a genuinely later RAW Extreme appears.

## Findings requiring hardening before N3 enforcement

### DEP-A03-F1 — Stable canonical Extreme EventID/CycleID is missing
ExtremeLifecycleData carries RawCandleTime, ConfirmationCandleTime, Direction and Timeframe but no explicit immutable owner/event identity. N1 can observe the current state, but N3 lineage should not infer identity only from whichever timestamp happens to be populated.

Queue action:
- create deterministic Extreme EventID/CycleID from source-owned facts only, e.g. pair + timeframe + direction + RawCandleTime;
- freeze it when RAW is installed;
- later confirmation/retest changes maturity, not identity;
- a genuinely newer RAW after VOID/SUPERSEDED must receive a new identity;
- no score or new trading rule.

### DEP-A03-F2 — Terminal-state provenance is overwritten when a later RAW starts
Current logic correctly allows a later RAW candle to reset a VOID/SUPERSEDED state and begin a new lifecycle. For N3/replay, however, the retired owner needs enough terminal provenance to prove that an older cycle did not resurrect.

Queue action:
- preserve or emit retired-cycle identity + terminal reason + terminal candle before reset;
- enforce monotonic identity: old EventID may never become active again after VOID/SUPERSEDED;
- new RAW must be distinguishable as a new cycle even when direction/timeframe are unchanged.

### DEP-A03-F3 — Opposite-Extreme equal-time ambiguity needs explicit lineage handling
ResolveOppositeExtremeSupersession intentionally leaves equal confirmation times ambiguous. That is safe today because downstream conflict remains fail-closed, but N3 should carry an explicit reason-coded unresolved/conflict provenance rather than merely relying on both states remaining mature.

Queue action:
- expose deterministic conflict reason such as OPPOSITE_EXTREME_EQUAL_CONFIRMATION;
- NMJE may classify lineage UNRESOLVED/CONFLICT but must not choose a winner heuristically;
- M08 remains the sole writer of Extreme lifecycle state.

### DEP-A03-F4 — Historical indicator reads used by invalidation need replay/atomicity proof
IsExtremeMomentumInvalidation recalculates the previous BB from broker history while the current band/data are supplied from the processing snapshot. This is deterministic under stable history, but restart/history refresh can theoretically produce a mixed snapshot if broker history changes between reads.

Queue action:
- include current/previous BB inputs in the same closed-candle replay test set;
- prove uninterrupted vs restart/reload results are identical;
- if required later, freeze the exact source-candle indicator identity used by M08 rather than adding any new strategy rule.

### DEP-A03-F5 — Restart/replay equivalence is not yet proven end-to-end
M08 state includes provisional/frozen anchors, PreviousClose, retest-start and terminal timestamps. N3 lineage cannot treat those as authoritative across restart until reconstruction is deterministic or safely unresolved.

Queue action:
Build deterministic replay cases for:
- RAW -> reversal confirmation;
- multiple reversal-phase candles updating provisional anchor;
- retest-start and same-candle retest completion;
- later retest completion;
- invalidation before confirmation;
- invalidation during retest phase;
- opposite mature Extreme supersession;
- equal confirmation ambiguity;
- VOID/SUPERSEDED -> genuinely newer RAW;
- restart/missed-candle at every stage.
For identical closed-candle history, M08 output and Extreme EventID must be identical before/after replay.

### DEP-A03-F6 — N3 maturity consumption must preserve existing F2 boundary
NMJE currently observes RAW as context and reversal-confirmed/retest states as stronger context. Mandatory N3 enforcement must not change the canonical maturity rule.

Queue action:
- RAW remains observational/building only;
- REM/REE Extreme component minimum remains REVERSAL-CONFIRMED;
- standalone Extreme minimum remains RETEST/ENTRY-READY;
- favourable nesting must never promote RAW or bypass retest for standalone Extreme.

## N3 readiness assessment
- RAW detector ownership: PASS
- Closed-candle discipline: PASS
- F2 maturity progression: PASS
- Frozen anchor/retest semantics: PASS
- Opposite-cycle supersession: PASS / HARDEN IDENTITY
- No fixed canonical expiry: PASS
- Stable immutable EventID/CycleID: NOT YET PRESENT
- Terminal provenance/monotonic identity: PARTIAL / HARDEN
- Restart/replay equivalence: NOT YET PROVEN
- Safe for N1/N2 observation: YES
- Safe as mandatory N3 lineage authority today: NOT YET

## Implementation timing
Do not patch the currently running runtime candidate. Execute identity/provenance/replay hardening after frozen runtime evidence is preserved and before mandatory N3 enforcement, coordinated with N3-H09/H11/H13/H16.

## Next dependency audit
DEP-A04: M09 MHV/MLV lifecycle identity — parent Extreme identity, frozen marked-body provenance, TP-Wajib completion, direction takeover, supersession, and replay suitability.
