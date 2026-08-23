# P3-M2-07 — Opposite Extreme Deep Research

Date: 2026-08-23
Branch: `blueprint-dev`
Status: **EVIDENCE RESOLUTION COMPLETE — SIGNAL/CYCLE/PENDING AUTHORITY RESOLVED; LIVE-TRADE FORCED CLOSE NOT AUTHORISED**

## Research question
When `Extreme A` exists and a valid `opposite Extreme B` later forms, what exactly becomes invalid or ends?

Scopes tested:
1. prior Extreme signal/lifecycle;
2. prior directional cycle ownership;
3. pending setups/candidates derived from the prior cycle;
4. already-open live trade.

## Evidence hierarchy
Primary project sources:
- `Oma ally BBMA - AL.pdf`
- `BBMA technique.pdf`
- project Finale-derived reconciled architecture and source contracts

External corroboration:
- ForexFactory BBMA Trading discussion
- mirrors/notes reproducing BBMA basic material

Project pseudocode is treated only as historical supporting implementation evidence, not as independent Oma Ally authority.

## Finding A — Prior Extreme signal loses directional authority: HIGH CONFIDENCE
The Oma Ally summary states that an opposite Extreme is created when trend/momentum ends and this is where the BBMA cycle restarts or reverses. ForexFactory BBMA discussion states explicitly that an Extreme Sell becomes invalid if an opposite Extreme Buy forms (and vice versa by symmetry).

Therefore, once opposite Extreme B is **valid/mature enough to count as the new Extreme**, Extreme A must no longer remain the active directional Extreme owner for new decisions.

Important distinction: a raw MA excursion or unconfirmed potential Extreme is not enough. Existing BBMA rules still require the source-defined validity/maturity conditions; CSM/momentum can invalidate an apparent Extreme before it becomes authoritative.

## Finding B — Prior directional cycle ends/restarts/reverses: HIGH CONFIDENCE
The primary Oma Ally cycle description explicitly places an opposite Extreme at the end of the previous trend/momentum and says the cycle/process then restarts or reverses.

Canonical consequence:
- opposite **valid/mature Extreme** is a cycle-boundary event;
- the previous directional cycle must stop producing fresh authority;
- the new opposite cycle becomes the active cycle context subject to its own confirmation/lifecycle rules.

## Finding C — Pending setups/candidates dependent on old cycle must be invalidated or revalidated: HIGH CONFIDENCE AS ARCHITECTURAL CONSEQUENCE
The sources do not use EA-state terminology such as `pending candidate`, but a setup whose validity depends on Extreme A / old-cycle ownership cannot remain automatically executable after that owner is superseded by opposite Extreme B.

Therefore:
- pending standalone/combined candidates that contain a component owned by the superseded cycle must fail exact-owner revalidation;
- old-cycle Re-Entry/add-on authority must not survive merely because its historical candle still exists;
- REM/RRE/REE or other pending sequences must be rebuilt/revalidated against current authoritative owners rather than carrying stale direction forward.

This is an implementation consequence of the source-defined cycle restart, not a new scoring/filter rule.

## Finding D — Opposite Extreme does NOT by itself authorise immediate forced-close of an already-open live trade: MEDIUM-HIGH CONFIDENCE
No primary source located in this research pass states a universal rule equivalent to:
`opposite Extreme appears -> immediately market-close every existing opposite position`.

Instead, BBMA material provides setup-specific management/exit concepts such as:
- Extreme-entry `TP Wajib` at the opposite MA5/MA10 / up to MID BB;
- structural invalidation/cancellation conditions;
- Re-Entry/CSM/CSA progression and exit guidance.

Secondary notes sometimes describe closing orders when momentum ends / an opposite Extreme appears, but this is not sufficiently authoritative or universal to encode as a mandatory forced-close engine rule for every BBMA entry family.

Therefore canonical EA policy must be:
- opposite Extreme changes **signal/cycle authority**;
- it may invalidate fresh/pending old-cycle entries;
- an already-open trade remains managed by its approved SL/TP and any separately source-proven trade-management exit rule;
- do NOT invent `CloseTradeOnOppositeExtreme()` without stronger source evidence.

## Critical consequence for PR #35
The current draft P3-M2-07 guard — `if any opposite EA-owned live position exists, block the new opposite-direction decision until that old position closes` — is **too coarse**.

Why:
1. The BBMA source says a valid opposite Extreme can legitimately restart/reverse cycle authority.
2. Existing live-position direction is therefore not the same thing as current BBMA cycle direction.
3. A stale old-cycle trade could remain open due to its own SL/TP while the market has already produced a valid new opposite cycle.
4. Blocking every fresh opposite decision solely because the old trade remains live can suppress a source-valid new-cycle setup.

PR #35 should therefore **not be merged in its present form**.

## Recommended architecture
Use **cycle-owner invalidation**, not a permanent position-direction lock:

1. Valid/mature Extreme B opposite to Extreme A appears.
2. Mark/supersede Extreme A and old directional cycle owner.
3. Invalidate/revalidate pending old-cycle candidates through M16 exact-owner checks.
4. Allow new-cycle candidates only after their own source-defined confirmation/MTF authority is complete.
5. Existing old-cycle live trade remains under its existing source-approved SL/TP/trade-management contract.
6. Do not open an opposite trade merely from the raw Extreme signal; the new entry still needs normal BBMA execution authority.
7. Do not forced-close the old trade solely on opposite Extreme unless future source evidence explicitly proves that exit rule for its entry family.

## Confidence table
| Scope | Result | Confidence |
|---|---|---|
| Extreme A signal authority | Superseded/invalidated by valid opposite Extreme B | High |
| Old directional cycle | Ends/restarts/reverses | High |
| Pending old-cycle setup/candidate | Must be invalidated or exact-owner revalidated | High (architectural consequence) |
| Existing live trade | Not automatically force-closed by opposite Extreme alone | Medium-High |
| Fresh new-cycle entry | May become eligible after its own confirmation/authority | High |
| Permanent `no opposite order while old trade alive` rule | Not source-supported; too restrictive | High |

## Next development action
1. Keep PR #35 unmerged.
2. Audit current M08/M16 lifecycle to verify that valid opposite Extreme actually supersedes the prior Extreme/cycle owner atomically.
3. If missing, implement a source-derived **Opposite Extreme Cycle Supersession** patch with a new About/header build identifier.
4. Do not add forced-close logic.
5. Re-run M2-07/M2-08 downstream static regression and compile 0E0W if source changes are made.
