# Q9 P2/P3 Retrospective Source Reconciliation — 2026-09-19

Issue: #101  
Base: Q9 P4 verified head `ae9e861d542b10d905306aa696393e7b236f03d7`  
Scope: read-only Strategy-Core/source reconciliation before P5  
Status: COMPLETE / NO EA CHANGE / P5 INPUT IDENTIFIED

## Authority and evidence
Preflight followed `SOURCE_INDEX.md` -> accepted Core -> M12N/N1 contract/decision -> Group-3 + PRIMARY15 FINAL_CORRECTED/A3/A4 evidence -> Build 4.88/4.89 code and validation.

Corpus inspected explicitly:
- `BBMATV Group-3`: `FINAL_CORRECTED_20260911/GROUP3` + `A3_VIDEO_EVIDENCE.jsonl` + A4/A5 disposition.
- `PRIMARY15`: `FINAL_CORRECTED_20260911/PRIMARY15` + `A3_VIDEO_EVIDENCE.jsonl`.
- A4/A5 semantic closure remains authoritative for its nine retained rows: 6 `CORROBORATION_ONLY`, 3 `REJECTED`, 0 `ACCEPTED_CORE`.

No subtitle-only statement is promoted above accepted Core. Residual uncertain wording remains excluded.

## Reconciliation matrix

| Q9 item | Source result | Classification | Executable effect |
|---|---|---|---|
| P2 recursive journey/coherence metadata | Both corpora corroborate HTF/LTF journey reading; accepted N1 decision already classifies recursive MTF as strongly corroborated | CORROBORATED | None |
| P2 deterministic ordering among ALIGNED/SUPPORTING/BUILDING/CONFLICT | No source/contract ordering found | HOLD / UNRESOLVED | Forbidden; current comparator remains unchanged |
| P3 M5 as lower-TF context | Group-3 contains explicit 5-minute nested-context teaching; PRIMARY15 also contains five-minute/lower-TF setup references | CORROBORATED CONTEXT | Shadow/diagnostic only |
| P3 M5 detector/lifecycle reuse | Applying existing Re-Entry/Extreme helpers to closed M5 data is software mapping, not a new source rule | ENGINEERING MAPPING | Allowed only while authority remains zero |
| P3 temporary opposite child activity | Accepted N1 principle says opposite-looking LTF activity does not automatically prove independent reversal | CORROBORATED PRINCIPLE | Must not become automatic reject/rank/execute authority |
| P3 exact conflict subtype semantics | Corpus does not lock a deterministic universal subtype/ordering formula | HOLD / UNRESOLVED | Diagnostic-only pending P5 bounded mapping |

## Material evidence
PRIMARY15 examples include lower-timeframe setup/confirmation teaching and an explicit five-minute setup reference in `video_15_day3_v04` around 233-249s. These remain corroboration, not standalone Core authority.

Group-3 provides stronger explicit nested examples:
- `0XoRUraiyLk` links H4 Re-Entry to H1 and M15 completion structures;
- `7SkZ8XRUz5U` links H4 Re-Entry with H1 Extreme/full setup;
- `VMDF27J0MxU` explicitly describes H4 -> H1 -> M15 -> M5 structure and lower-timeframe setup under larger-timeframe context.

For `VMDF27J0MxU`, A4/A5 controls still apply: disputed 57-74s and 108-115s wording is retained only as `CORROBORATION_ONLY`; disputed terms are excluded.

## Code/contract reconciliation finding

**CONFIRMED BUG — diagnostic relation overclassification**

Build 4.88, inherited by verified Build 4.89, maps an opposite active M5 Extreme to:
`NESTED_CONFLICT / M5_TEMPORARY_EXTREME_OPPOSES_PARENT`.

The active M12N contract states that `NESTED_CONFLICT` is for resolved authoritative states that cannot coexist under accepted parent/child interpretation and explicitly says not to classify raw/pre-direction Extreme or MHV as conflict merely because nominal direction differs.

Impact:
- no current trade-behaviour change because M5 remains shadow-only and P2 ordering is HOLD;
- telemetry semantics are nevertheless stronger than the active contract and would be unsafe input for later P5/P6 research or any future activation.

Required smallest correction:
- P5 must remove automatic top-level `NESTED_CONFLICT` classification for opposite M5 Extreme based only on nominal direction;
- use a conservative non-conflict developmental state unless stronger owner provenance proves structural conflict;
- do not alter candidate eligibility, comparator, M15/M16, risk, lifecycle or execution.

## Additional HOLD

`opposite confirmed M5 Re-Entry -> NESTED_CONFLICT / temporary-conflict reason` is not promoted to an executable fact by this reconciliation. The sources support nested child structure and caution against treating opposite-looking LTF activity as automatic reversal, but do not provide a universal Boolean conflict formula. P5 must keep this diagnostic/non-executable unless a bounded contract mapping can be proven without inventing Strategy Core.

## Decision

P2/P3 source reconciliation is complete.

- Existing P2 metadata-only behaviour: KEEP.
- P2 active tie-break ordering: HOLD / UNRESOLVED.
- M5 shadow observation: KEEP as context/engineering mapping.
- No EA change is authorized by video corroboration itself.
- One diagnostic contract mismatch is confirmed and becomes the smallest eligible P5 corrective task.
- Any ambiguous/conflicting subtype remains HOLD and non-executable.
