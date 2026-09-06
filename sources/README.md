# BBMA Source Evidence Library

This directory is the canonical GitHub index for BBMA/Oma Ally source evidence used by the project.

## Priority hierarchy

- `tier-a-primary/` — direct Oma Ally / official BBMAOA / original class material. Highest authority.
- `tier-b-strong-supporting/` — strong supporting manuals, slides, PDFs, or recognized BBMA teaching material consistent with Tier A.
- `tier-c-secondary/` — community tutorials, explanations, and secondary educational material.
- `tier-d-cross-reference-only/` — adaptations, indicators, EA implementations, blogs, TradingView/community interpretations. Never sufficient alone to change BBMA Core.

## Per-source package

Every source should contain or link to:

1. `metadata.md` — title, author/channel, URL, date, runtime/pages, source type, authority tier, local archive reference.
2. `transcript/` — ASR draft and reviewed transcript where applicable.
3. `visual-notes.md` — slides/charts/onscreen information not recoverable from audio alone.
4. `rule-extraction.md` — BBMA rules, lifecycle conditions, examples, exceptions, and contradictions extracted from that source.
5. `evidence-map.md` — mapping from claims/rules to timestamps/pages and EA modules where relevant.

## Evidence policy

Tier A overrides lower tiers when a genuine contradiction is established. Lower-tier material may clarify or cross-reference but must not silently alter BBMA Core. Unreliable ASR must remain marked draft/unverified and must not be promoted to authoritative evidence.

## Binary media policy

Large raw videos/audio remain in the local evidence archive on the connected laptop because normal GitHub file storage is unsuitable for very large media files. GitHub must still contain the source URL, metadata, transcript, visual audit, hashes/identifiers where available, and extracted evidence so every project decision remains traceable.
