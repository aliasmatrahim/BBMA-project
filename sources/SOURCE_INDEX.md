# BBMA Canonical Source Index

Canonical source root: `sources/` on `main`.

## Search rule
Always search this `sources/` tree on `main` first before concluding that a BBMA source is missing. Development branches are not canonical source registries.

## Registered collections

### Existing authority-tier registry
- `tier-a-primary/` — primary/direct source material.
- `tier-b-strong-supporting/` — strong supporting material.
- `tier-c-secondary/` — secondary/community explanation.
- `tier-d-cross-reference-only/` — cross-reference only.

### Consolidated blueprint-dev reference library
- `imported-blueprint-dev/` — complete preserved `docs/references/` source library imported from `blueprint-dev`.
- Includes original PDFs, ForexFactory evidence, BBMA Finale original subtitles 1–7, Finale per-video summaries/rule extraction, source indexes, conflict registers, and source-of-truth/reference documents.

## BBMA Finale quick path
- Original subtitles: `sources/imported-blueprint-dev/original/video/oma_ally_finale/`
- Finale analysis/rules: `sources/imported-blueprint-dev/video/oma_ally_finale/`

## Canonical policy
1. All BBMA source material must live under or be registered from `sources/` on `main`.
2. `sources/SOURCE_INDEX.md` is the first lookup point.
3. Do not conclude a source is absent after searching only another branch.
4. Raw large video binaries remain in the D: source backup; GitHub stores source records, subtitles/evidence, summaries, rule extraction, identifiers, and legally appropriate artifacts.
5. `docs/references/` on development branches is legacy/non-canonical after this consolidation.

Consolidated from `blueprint-dev` reference tree on 2026-09-06 without deleting the legacy branch copy.