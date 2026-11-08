# M10 direction terminology and shared computation — 2026-11-08

Scope: user-authorized evidence review, CSA/CSAK mapping and shared M10 calculation; Issue #302 / Draft PR #303. No trading activation or merge.

## Retrieval and findings
SOURCE_INDEX routes accepted Core, Finale synthesis/extractions, original subtitles, PDF evidence and contracts. The expected episode file names are V05/V05_extracted_rules.md and V06/V06_extracted_rules.md; the earlier generic extracted_rules.md path is not the routed file name.

Original Finale V05 00:29:58–00:30:06 and 00:31:19–00:31:32 describes early direction as passing MA5/MA10 without Mid BB. V05 00:30:35–00:31:18 explains Mid BB as direction separator. V06 00:17:07–00:17:45 connects the Mid BB break with direction and MA5/MA10 with strengthening confirmation. V06 00:20:07–00:20:18 describes a close beyond MA5, MA10 and Mid BB as strong direction. These are user-supplied subtitle evidence, not independently authenticated publication/audio verification.

Derived corroboration: OA-F-V05-010/011/012 in the episode extraction; accepted Core section 7; M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md. Secondary BBMA technique PDF text does not by itself establish the exact CSA acronym mapping; zero acronym matches are not absence proof. Original subtitle ambiguity is not silently normalized into a new detector.

## Mapping and authority
| Product term | Mapping | Status |
|---|---|---|
| Early direction | Existing eCSD concept: MA5/MA10 crossing; source describes not yet passing Mid BB | Accepted concept. Legacy detector may overlap CSD, with downstream collector precedence; no new exclusion introduced here. |
| CSA | User's Mid-BB direction term | Must not alias to legacy eCSD. Mid-BB direction role corroborated; exact independent executable classifier/maturity still requires resolved mapping and tests. |
| CSAK | Strong direction: relevant MA5/MA10 plus Mid BB | Semantic correspondence to existing CSD corroborated. Body-cross versus close-side remains engineering mapping, not verbatim founder formula. |
| MOM | Existing M10 CSM | Separate expanding/directional BB rule; unchanged. |

This corrects the earlier blanket SOURCE CONFLICT diagnosis: terminology differences do not alone establish source contradiction. The retained boundary is ALIAS/IMPLEMENTATION VERIFICATION REQUIRED, not permission to rewrite canonical detectors. No raw CSA/CSAK/CSD/eCSD gets standalone order authority.

## Consumers audited
- M11 H4 owner: Classify/ownership handover uses DetectCSD/DetectECSD at H4; body-cross outcomes preserved.
- M12 precursor resolution and Type4: direction/Momentum dependencies and CSD precursor preserved.
- D1 opportunity journey: DetectD1OpportunityCSD and DetectD1OpportunityECSDWatch retain existing wrappers and identity rules.
- M27 M15 collection: DetectCSD/DetectECSD outputs, collector precedence and snapshots unchanged.
- M13/M14/M15/M16: no component signature, selected direction, gate, maturity or authority change.

## Implementation
Build 5.90 / V590_M10_SHARED_PAIR_20261108 / M10_SHARED_PAIR_001_20261108 adds one shared M10_CandleBodyCrossesMAPair helper. Both detectors use it for the relevant High/Low pair; CSD additionally uses the existing Mid-BB body-cross helper. Existing price/MA positivity guards and direction checks remain. Inputs and detector signatures unchanged. This shares calculation logic, not a new per-cycle snapshot cache; once-per-event materialization remains T04 work.

No new CSA predicate, signal enum, lifecycle or executable alias is added. CandleBodyCrossesLevel remains the existing engineering open-to-close spanning interpretation; source close-beyond wording is not silently converted into a changed predicate.

## Verification
- Test first: shared-helper assertion failed before helper existed.
- Test shape corrected: each detector has BUY and SELL branches, therefore two static helper call sites but one executed per invocation.
- Extracted actual numeric predicates compiled as C++: 19,683 value/direction combinations equivalent to the original conjunction. This is numeric equivalence evidence, not MQL4 runtime.
- Full candidate native MQL4 strict compile: MetaEditor 5.0.0.2425, 0 errors / 0 warnings, 999 ms; isolated m10-stage directory under MT4_CustomMTF_302_Unit. No primary terminal restart.
- Full EA Strategy Tester/runtime NOT RUN. Full pytest suite remains unavailable in cloud Python; no full regression PASS or Core-compliance claim.

Next: validate shared detector outputs in native targeted runtime, resolve CSA alias entry eligibility separately, and continue unaffected custom input integration. Existing parser and slot proofs are unchanged but not rerun in this patch.
