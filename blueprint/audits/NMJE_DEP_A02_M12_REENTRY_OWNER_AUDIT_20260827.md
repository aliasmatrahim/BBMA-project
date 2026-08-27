# NMJE Dependency Hardening Audit — DEP-A02 M12 Re-Entry Owner/Lifecycle

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE
Runtime-candidate rule: preserve the currently running/frozen EA candidate; findings below are queued for the appropriate implementation window.

## Scope
Review M12 as an upstream canonical owner consumed by NMJE. Focus: deterministic ownership, lifecycle identity, maturity/export, invalidation/supersession, expiry semantics, and N3-readiness. This audit does not invent new BBMA entry filters.

## Baseline verdict
M12 is materially implemented as a stateful Re-Entry owner and is suitable as an NMJE upstream source, but it is not yet fully hardened for N3 enforcement.

Current strengths observed in source:
- separate ReEntryData owner state per direction/timeframe;
- closed-candle guard and same-candle double-processing guard;
- explicit NONE/CANDIDATE/CONFIRMED/EXPIRED lifecycle;
- confirmed export freezes confirmation candle/time, entry price and MA/BB snapshot fields;
- Type-1 requires prior BBMA directional-owner context before structural ranging/retrace and MA5/10 validation;
- opposite source-valid direction/momentum clears stale Type-1 directional context;
- exact Type-3/Type-4 precursors are allowed to take ownership ahead of generic Type-1;
- confirmed Type-1 remains conditional on structural owner survival;
- NMJE consumes M12 state rather than re-detecting Re-Entry.

## Findings requiring hardening before N3 enforcement

### DEP-A02-F1 — Stable canonical Re-Entry event identity is missing
ReEntryData exposes timestamps/state but no explicit immutable EventID/OwnerID. N1 can observe state using candle times, but N3 enforcement/recovery should not infer canonical identity from mutable fields alone.

Queue action:
- derive a deterministic ReEntry Owner/Event identity from source-owned facts only, e.g. pair + timeframe + direction + type + owner/start anchor;
- freeze identity when the canonical owner is installed;
- confirmation may advance maturity but must not silently create an unrelated identity;
- no scoring or strategy rule is added.

### DEP-A02-F2 — Generic expiry semantics are mixed with Type-1 structural semantics
Specific Re-Entry candidates use MaxWaitBars_ReEntry/ExpiryCandleTime. Type-1 comments explicitly state no fixed structural expiry, yet the common expiry block applies when State is CANDIDATE or CONFIRMED if IsReEntryIntrinsicExpired() evaluates true. Type-1 currently initializes ExpiryBar/ExpiryCandleTime to zero, so behaviour may be safe in practice, but the ownership contract is implicit rather than type-explicit.

Queue action:
- make expiry ownership explicit by Re-Entry type;
- Type-1 structural lifecycle must remain source-structural and must not acquire an invented fixed timeout;
- project component-freshness overlays, if retained downstream, must not erase canonical M12 provenance.

### DEP-A02-F3 — Confirmed Type-2/3/4 lifecycle invalidation/supersession needs explicit owner contract
After confirmation, the generic final branch keeps ReEntryData valid and updates LastUpdate*. Type-1 has explicit post-confirmation owner-survival logic; Type-2/3/4 do not show equivalent explicit lifecycle retirement in the reviewed section.

Queue action:
- audit source-backed invalidation/supersession for confirmed Type-2/3/4;
- where source is silent, do not invent market filters: preserve provenance and use deterministic project states such as superseded/unresolved only where necessary for software ownership;
- distinguish component freshness from canonical structural invalidation.

### DEP-A02-F4 — Ownership transfer should be monotonic and reason-coded
Current Type-1 reset/adoption behaviour is structurally sensible, but ResetReEntryState can erase the prior owner representation. N3/replay diagnostics need to know whether an owner ended by opposite direction, MA-cluster failure, expiry, or exact-family takeover.

Queue action:
- retain terminal provenance/reason for the retired owner or emit a deterministic transition record before reset;
- never allow an older retired owner to resurrect after restart/history refresh;
- keep M12 as sole writer of canonical Re-Entry state.

### DEP-A02-F5 — Restart/replay equivalence must be proven
M12 uses mutable lifecycle context including Type1ContextState, Type1PreviousClose, StartCandleTime, qualifying counts and confirmation fields. N3 cannot rely on M12 until reconstruction after MT4 restart/missed processing is deterministic or safely unresolved.

Queue action:
- add deterministic replay scenarios for Type-1 owner -> ranging -> confirmation, opposite-owner takeover, Type-2 3-candle qualification, Type-3/4 precursor -> retrace, expiry and restart at each stage;
- reconstructed state must equal uninterrupted state, otherwise NMJE marks lineage UNRESOLVED/fail-closed for new-entry use.

### DEP-A02-F6 — NMJE candidate visibility must not become execution authority
N1 currently observes both candidate and confirmed Re-Entry states. Candidate visibility is useful for BUILDING lineage but must not become a confirmed entry component at N3.

Queue action:
- preserve strict maturity distinction: CANDIDATE = observational/building context only; CONFIRMED = eligible canonical Re-Entry component subject to the normal setup contract;
- no N3 shortcut may promote candidate Re-Entry because nesting looks favourable.

## N3 readiness assessment
- Canonical detector/owner present: PASS
- Closed-candle discipline: PASS
- Confirmation/export maturity: PASS
- Stable immutable owner identity: PARTIAL / HARDEN
- Type-explicit expiry ownership: PARTIAL / HARDEN
- Post-confirmation lifecycle for all RE types: PARTIAL / AUDIT
- Restart/replay equivalence: NOT YET PROVEN
- Safe for N1/N2 observation: YES
- Safe for mandatory N3 enforcement today: NO

## Implementation timing
Do not patch the currently running runtime candidate for these findings. Execute after the frozen runtime evidence is preserved and before mandatory N3 enforcement, coordinated with the queued NMJE hardening work.

## Next dependency audit
DEP-A03: M08 Extreme owner/lifecycle — canonical event identity, maturity, opposite-Extreme supersession, terminal-state monotonicity and restart/replay suitability.
