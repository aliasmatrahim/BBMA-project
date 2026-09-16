# Build 4.84 Structural Lifetime Authority Repair — 2026-09-16

Issue: #173
Branch: `fix/q5-lifetime-173`
Base: `d1-owner-dev@e2c1a35743e6251f8ee499870aad248e43adb06b`
Status: **STATIC / NATIVE COMPILE VERIFIED; RUNTIME NOT VERIFIED**

## Root cause
Accepted lifetime resolution rejects generic fixed-age Strategy-Core death rules for Extreme and Re-Entry Type 2/3/4. The owner source still allowed `MaxWaitBars_Extreme` and `MaxWaitBars_ReEntry` to invalidate otherwise structurally valid owners through M12/M15/M16.

The repair keeps structural ownership authoritative:
- Extreme validity remains owned by M08 VOID/supersession lifecycle;
- Re-Entry candidate/confirmed validity uses MA5/MA10 close-side structural failure and opposite source-valid direction/momentum ownership transfer;
- Type 2 retains confluence-break reset;
- Type 3/4 retain their source precursor/retrace requirements;
- legacy age fields remain compatibility/diagnostic metadata only.

No replacement timer or optimized candle count is introduced. #175 Mode-2 standalone Extreme scope remains untouched/HOLD.

## TDD evidence
Focused guard: `blueprint/tests/test_q5_structural_lifetime_authority.py`.
- RED against exact owner before repair: **4 failed / 0 passed**, each on the intended active timer/structural-authority defect.
- GREEN after repair: **4 passed**.
## Regression evidence
All 13 valid owner-baseline direct self-test scripts passed after the repair. The historical `test_v459_runtime_variant_builder.py` remains excluded from this regression because it already failed on the untouched owner baseline by requiring the obsolete v4.59 canonical identity; this repair does not modify that tool.

`git diff --check`: PASS.

## Native MetaEditor compile
Exact Build 4.84 source:
- Result: **0 errors / 0 warnings**;
- elapsed: **1547 msec**;
- MQ4 SHA-256: `3246E4444423E15AB2575C812E929DF4CE1C39D8E787903BA56FF60B3AEEA5BB`;
- EX4 SHA-256: `A3279613ABE7A06393AB9C36D9130C6ED1C45ACC6660BA05523DC4E7652FC4FB`.

Compile log: `blueprint/audits/V484_METAEDITOR_COMPILE_20260916.log`.

## Contract synchronization
`M12_REENTRY_SOURCE_CONTRACT.md` and `M16_CONFLICT_INVALIDATION_CONTRACT.md` are synchronized only for lifetime/owner-validity wording. No unrelated D1 historical text or Mode-2 entry-universe policy is changed.

## Runtime boundary
**NOT RUNTIME VERIFIED.** No primary MT4 restart, trading enablement or production activation was performed. Merge remains a separate user gate because this repair changes EA Strategy-Core validity behavior.
