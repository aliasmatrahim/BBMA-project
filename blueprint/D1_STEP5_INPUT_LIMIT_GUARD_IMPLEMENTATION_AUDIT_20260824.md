# D1 Step 5 — Input Limit Guard Implementation Audit

Date: 2026-08-24  
Branch: `d1-owner-dev`  
Build: `Version 4.5.1 - D1-05 Input Limit Guard`  
Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS**

## User-visible defect
Changing `MaxActivePair` above the internal `MAX_PAIRS` capacity caused `ValidateInputParameters()` to return false. `OnInit()` then returned `INIT_PARAMETERS_INCORRECT`, so MT4 detached the EA from the chart even though the condition was recoverable.

## Fix
- Internal pair-state capacity raised from 20 to 40.
- `MaxActivePair` is normalized to an effective runtime range of 1..40 before fatal validation.
- Values outside that range generate an unconditional Experts/Journal warning and the EA remains attached.
- Oversized `PairList` no longer causes fatal parameter rejection; the existing bounded loader ignores entries beyond 40 and emits a warning.
- M20 current and prospective active-pair checks consume the sanitized effective limit.
- Other genuinely invalid/fatal initialization conditions remain fail-closed.

## Safety / architecture regression
- `MAX_PAIRS`-sized pair-state and portfolio-count arrays scale together to 40.
- `MAX_MONITORED` and `MaxTotalTrade` protections are unchanged.
- PairID range remains 1..99 and is sufficient for 40 configured pairs.
- No BBMA Strategy-Core detector, combination, D1/H4/H1/M15 hierarchy, SL/TP, money-management formula, execution, or lifecycle semantics were modified.
- `blueprint-dev` remains untouched.

## Verification
Focused static integrity: **PASS**.  
Native MT4 MetaEditor: **0 errors / 0 warnings; EX4 produced**.  
Real broker check: set `MaxActivePair` above 40 and confirm warning + EA remains attached; final broker-side confirmation remains user-owned.
