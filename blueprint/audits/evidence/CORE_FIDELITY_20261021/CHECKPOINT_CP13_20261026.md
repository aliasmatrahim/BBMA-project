# CORE-FIDELITY-292 — CP13 Core §7 eCSD/CSD direction handoff
Date: 2026-10-26. Phase: AUDIT / PARTIAL. Issue #292.
Branch: `audit/core-fidelity-20261021`; parent: `1ba5b4d0d349e0f98a3dde2d7819cc9fb91e837c` (CP12).
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.

## VERIFIED
- Recovered live branch heads and queue/checkpoint: audit was CP12, owner remains Build 5.15 at `459c0588...`; PR #293 is open/draft/unmerged. CP12 was the latest verified checkpoint and the queue's next action was Core §7.
- Source chain: current SOURCE_INDEX, accepted Core V2 §7.1–7.3, primary PDF-derived rule index p.8 (source evidence pages 7–8), Finale V05 OA-F-V05-010–013 (00:28:41–00:36:51), V06 OA-F-V06-002/004 (00:12:55–00:20:18), V03 OA-F-V03-001/002/004, secondary PDF CSM law as recorded in M10 contract, source conflict register, M10/M12/M13/M14/M11/M12N contracts, approved D1O-01 decision, and exact Build 5.15 owner code. No relevant unresolved §7 source conflict was found; forum evidence was not needed to resolve this deterministic mapping. Raw PDF binaries were not reopened in this connector pass.
- Core mapping: eCSD is the early MA5/MA10 pair cross; CSD adds the Mid-BB cross and stronger direction intent; CSM remains the separate Momentum predicate. All are signal/context, not standalone entry. Raw `DetectECSD` can overlap a same-direction CSD; M12/M27 classify CSD first and M13 suppresses the duplicate. The exact body-span cross and directional High/Low MA mapping remain engineering interpretations.
- M10 owner functions implement the accepted signal roles statically. M12 `DetectReEntryDirectionOwnerSignal` orders CSM > CSD > eCSD; Type 3 starts from CSM and Type 4 from CSD as candidates, with their later MA retrace required for confirmation. eCSD provides direction ownership/context, not Re-Entry confirmation.
- M13 suppresses a same-direction same-candle eCSD when CSD is valid. M27's H4 direction-owner classifier uses CSM > CSD > eCSD and its M15 snapshots carry closed-candle identities. M09 consumes same-direction M15 CSD/eCSD for its MHV direction-takeover stage. REM/RRE/REE component signatures are unchanged.
- M11J's approved D1O-01 path treats a confirmed D1 CSD as opportunity context aligned with the D1 strategic owner; fresh confirmed LTF Re-Entry after activation is required. D1 eCSD is watch-only. BuildD1OpportunityCandidate materializes `SIGNAL_RE_ENTRY` from fresh LTF owners; M15 remains final authority and M16 fails closed. No direct raw CSD/eCSD entry path was found.
- M08 uses `IsExtremeLifecycleInvalidation` and its local CSM-equivalent helper, not a direct M10 `DetectCSM` call. This static helper mapping was already recorded in CP10; focused helper parity/runtime remains NOT VERIFIED.
- Updated the M10 contract to retire its stale instruction that M13 must later decide CSD/eCSD precedence. Updated the source matrix, cross-module ledger, gap register, Finale index, CURRENT and MASTER_QUEUE. No EA source or owner artifact changed.

## PARTIAL / NOT VERIFIED
- Owner Build 5.15 still carries the separately confirmed M06 incomplete-history validity defect; the repair is candidate-scoped in PR #293/Build 5.20. CP13 does not verify CSD/eCSD signals on incomplete history.
- Live G40 read-only snapshot during CP13: device was online, there were no active Desktop Commander sessions, and the current process list contained no MetaTrader, MetaEditor or Strategy Tester process. The authoritative project record still says Strategy Tester NOT RUN and qualified history NOT VERIFIED; the process scan is point-in-time presence evidence, not historical test evidence.
- CP13 is static only. No focused CSD/eCSD precedence, Re-Entry parity, native compile, Strategy Tester, or broker/runtime was run. M10 body-cross mapping and M08/M10 helper parity remain engineering mapping / NOT VERIFIED.
- Qualified G40 history remains NOT VERIFIED; Strategy Tester remains NOT RUN. No merge, terminal restart or trading action occurred.
- Overall Core/module/runtime denominator remains PARTIAL.

## Exact next action
Audit accepted Core §8 Re-Entry across M12 owner state, M10/M11 direction sources, M13/M14 collection/validation and M15/M16 eligibility. Preserve the source-defined Type 1–4 boundaries and do not add waiting/expiry rules from natural-language ambiguity. Strategy Tester remains gated on qualified G40 history.
