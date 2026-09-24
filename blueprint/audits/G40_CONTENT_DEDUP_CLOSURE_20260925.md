# G40 Content Dedup Closure — 2026-09-25

Status: **PASS / NO STRONG CONTENT DUPLICATE DETECTED**
Scope: local `youtube_priority/P0` intake versus the reconciled Group-3 + PRIMARY15 FINAL_CORRECTED corpus and archived Finale V01-V07 text evidence.

## Method
- 13 locally readable intake text artifacts were normalized from VTT or combined ASR transcript.
- Canonical comparison set: 66 text units (63 FINAL_CORRECTED video units + archived Finale text units discovered by the mechanical scanner).
- Exact VideoID dedup remains governed by `G40_STRICT_SOURCE_DEDUP_GATE_20260924.md`; this pass tests content similarity rather than ID equality.
- Rolling 5-word n-gram coverage was measured on candidate segments to detect mirrored/re-uploaded content despite different file names.
- The two media-only blockers were additionally checked with rolling 3-word n-gram coverage to reduce false uniqueness caused by different ASR engines.

## Result
No candidate produced content coverage consistent with a mirror/re-upload of a reconciled canonical source.

Media-only blockers:
- Momentum `-nMZUF1Bx0k`: max rolling 5-gram coverage ~0.26%; loose 3-gram max ~6.81%.
- Personal Meeting Room `hqzptZ9uRmg`: max rolling 5-gram coverage ~1.01%; loose 3-gram max ~7.89%.

The loose matches are consistent with shared BBMA terminology and teaching phrases, not duplicated source text.

## Evidence
- `blueprint/audits/evidence/G40_CONTENT_DEDUP_20260925/content_dedup.json`
- `blueprint/audits/evidence/G40_CONTENT_DEDUP_20260925/content_dedup.tsv`
- mechanical scripts remain outside Core authority and do not define semantic equivalence.

## Authority / safety
- NEW CONTENT != NEW RULE.
- This gate only closes the mirror/re-upload screening question.
- Semantic authority still follows SOURCE_INDEX precedence and explicit reconciliation.
- ASR ambiguity, personal workflow, unsupported exceptions and source conflicts remain HOLD/non-executable.
- Core delta: **NONE**.
- EA/runtime delta: **NONE**.
