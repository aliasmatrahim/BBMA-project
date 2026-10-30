# CP23 — Read-only M08 reference candidate review

Date: 2026-10-27  
Task: Issue #292 / Draft PR #293  
Phase: **STATIC REVIEW PASS FOR TWO CANDIDATES; SOURCE PATCH / NATIVE COMPILE PENDING**

## Exact candidate and evidence
- Candidate: Build 5.23 / `V523_D1_TPW_TRANSITION_FAIL_CLOSED_20261027`, branch `audit/core-fidelity-20261021`.
- Exact candidate source blob: `be13aac3a2a0f2e2e9eeb2f5d4006eeedf7cd562`; SHA-256: `682A0F072C2A69ADF1A59FFED464E66911C62CDFB6C98C7D8E486C53DF774F5A`.
- Existing Build 5.23 compile PASS and regression PASS apply only to that unmodified blob; they do not validate any later qualifier change.
- `GetExtremeRelevantMA5(TimeframeData &data,...)` at line 2680 reads `data.ma[0]` / `data.ma[2]` and returns a scalar. It has 8 direct callsites in the exact candidate.
- `GetExtremeReversalBodyEdge(TimeframeData &data,...)` at line 2687 reads `data.open` / `data.close` and returns a scalar. It has 2 direct callsites in the exact candidate.
- Both bodies contain no writes to `data` and make no calls, so their input reference is locally proven read-only. Other no-detected-write parameters remain unproven pending review.
- Official MQL4 reference documents compound structure inputs as by-reference and `const` as the guard against modifying them: [Passing Parameters](https://docs.mql4.com/basis/function/parameterpass) and [Formal Parameters](https://docs.mql4.com/basis/variables/formal).

## Status and exact next action
- No source code changed in CP23; no tests, compile, Strategy Tester, broker runtime or trading activation ran.
- The suggested signature is `const TimeframeData &data` for these two helpers only. It is type-safety hardening and does not authorize any BBMA rule/behavior change.
- Any source patch must use a new unique, left-aligned build identifier (Build 5.24 candidate) and compile the exact resulting source in strict mode on G40. Current terminal/process state is not verified; G40 device registry online does not establish compiler or history readiness.
- Q10 Phase L R5 remains the highest-priority final-acceptance task; R5-14/R5-16 require natural broker events, and R6 stays unpromoted until R5 PASS.
