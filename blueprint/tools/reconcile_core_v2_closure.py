from pathlib import Path

p = Path('docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md')
s = p.read_text(encoding='utf-8')


def one(old: str, new: str, label: str):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1, found {n}')
    s = s.replace(old, new, 1)

old_53 = '''### 5.3 Extreme rules that remain HOLD
The following are **not authoritative Core rules yet**:
- MA5 merely touching the outer BB as equivalent to the established outside-BB Extreme condition.
- A reversal candle remaining outside BB but inside MA5 as a universal acceptance rule.
- Advanced / higher-timeframe Extreme exceptions without the normal TP-Wajib behaviour.

These remain governed by `BBMA_FINALE_SOURCE_CONFLICT_REGISTER.md`.
'''
new_53 = '''### 5.3 Extreme edge-case closure
The former broad HOLD is closed by the 2026-08-26 source/forum/web reconciliation:
- **MA5 merely touching the outer BB is not equivalent to canonical Extreme.** The established Extreme condition requires the relevant MA extension outside the band. Touch/equality may be context only and cannot create Extreme/TP-Wajib/execution authority.
- **A reversal-direction candle that remains closed outside the relevant outer BB is not a universal valid-Extreme shortcut merely because it is inside MA5.** Accepted outside-close/Momentum invalidation retains precedence over maturity promotion.
- **Advanced repeated-Extreme behavior is a bounded MTF exception, not a blanket no-TP rule.** Later same-direction LTF Extremes may omit a fresh local TPW/local MHV cycle only when no opposite LTF Extreme intervenes and the immediate HTF independently owns a valid mature MHV/MLV or Re-Entry compatible with the sequence. The HTF state must be proven by its own owner; RAW LTF Extreme maturity cannot be bypassed.
- The bounded repeated-LTF exception does **not** apply to the current D1 `EXTREME_TPW` path because D1 is the top approved owner in the EA hierarchy and has no independently validated larger parent.

Authority:
- `blueprint/decisions/CORE_V2_RESIDUAL_HOLD_CLOSURE_DECISION_20260826.md`;
- `blueprint/decisions/ADVANCED_REPEATED_EXTREME_TPW_EXCEPTION_DECISION_20260826.md`.
'''
one(old_53, new_53, 'section 5.3')

one('- advanced Extreme without normal TP Wajib remains `HOLD / UNCERTAIN` and cannot bypass this canonical rule;\n',
    '- the bounded repeated-LTF/valid-HTF exception does not manufacture a fresh same-timeframe MHV parent and does not weaken this canonical same-TF MHV provenance rule;\n',
    'section 6.2 advanced bullet')

start = s.index('### 8.6 First-candle validation / second-candle entry wording')
end = s.index('\n---\n\n## 9. Multi-timeframe relationship', start)
new_86 = '''### 8.6 Validation-candle / immediately-following live-candle timing
The teaching phrase “first Re-Entry candle validates; second candle is entry” is now **closed at semantic/project-mapping level**.

Canonical mapping:
- the source-timeframe Re-Entry validation candle must be fully closed;
- after that closed candle confirms the Re-Entry, execution may become eligible during the **immediately following live source-timeframe candle**, subject to the normal M15/final-authority and downstream validation gates;
- no extra full source-timeframe candle must close merely to reinterpret the teaching phrase;
- `EntryCandle` observability metadata refers to the immediately following source-TF candle and must not duplicate `ConfirmationCandle`.

This is consistent with `CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md`. Remaining broker `OrderOpenTime()` traces are runtime evidence, not a Strategy-Core semantic HOLD.

Evidence classification:
- first-validating / next-entry-candle teaching = **SOURCE-SUPPORTED**;
- exact closed-candle autonomous-EA timing = **PROJECT DETERMINISTIC MAPPING / ENGINEERING**.
'''
s = s[:start] + new_86 + s[end:]

start = s.index('### 11.1 Home Course 19-page completeness boundary')
end = s.index('\n\n---\n\n## 12. Change-control rule', start)
new_111 = '''### 11.1 Home Course / 49-family completeness boundary — fully classified

The historical 2026-08-25 revalidation recorded `28 COVERED + 10 PARTIAL/mixed + 11 MISSING/HOLD`. Subsequent dated source decisions supersede that count as the current gap status.

Current authority:
- `docs/references/BBMA_CORE_49_FAMILY_CLOSURE_REBASELINE_20260826.md`;
- `blueprint/decisions/CORE_REMAINING_GAPS_CLOSURE_DECISION_20260826.md`;
- `blueprint/decisions/CORE_V2_RESIDUAL_HOLD_CLOSURE_DECISION_20260826.md`;
- `blueprint/decisions/ADVANCED_REPEATED_EXTREME_TPW_EXCEPTION_DECISION_20260826.md`.

Current result: **49/49 Home Course families explicitly classified and 0 unresolved Core semantic HOLDs.**

“Closed” does not mean “directly executable.” Each former non-full family now terminates in one explicit category:
- accepted Core;
- accepted bounded/source-consistent context only;
- bounded advanced MTF interpretation;
- deterministic project/engineering mapping with provenance label;
- or rejected from current universal Core.

Important bounded outcomes:
- horizontal-BB rejection/compression, zones, Mid-BB slope and MA5-strength wording remain context/annotation unless an existing canonical setup owns execution;
- C018 Mid-BB break/retest/failure-to-recross is direction-confirmation context, not a standalone CSD detector;
- C024 MHV Momentum/no-Momentum behavior is a lifecycle principle, without inventing a new MHV direct-entry path;
- C034 Candle Arah Top/Low-BB destination is structural context, not a guaranteed universal resting broker TP;
- C035 pre-Re-Entry outer-BB hold is bounded to the pre-ReEntry stage;
- C038 D1 precedence is scoped strategic ownership, not an unconditional raw D1-vs-H4 shortcut;
- C039/C040/C041 repeated-Extreme/HTF-MHV relationships are bounded nested context and never manufacture HTF confirmation or suppress genuine LTF detectors;
- C042 prior-day D1 is strategic prior/context, not deterministic next-day prediction;
- C044 post-Re-Entry failed-Momentum is accepted as lifecycle source principle, while its exact automated outer-test/latch/recovery machinery is labelled project mapping and remains feature-gated pending broker validation;
- C048 Extreme Magic is a strength subtype, not independent execution authority;
- repeated same-direction LTF Extreme may omit a fresh local TPW/local MHV cycle only under the separately accepted bounded valid-HTF MHV/RE condition; D1 is excluded in the current hierarchy.

No historical HOLD/rejected wording may silently re-enter execution after this closure rebaseline.
'''
s = s[:start] + new_111 + s[end:]

old_tail = '''- H4 restart uses verified checkpoint + deterministic replay as engineering policy; D1 current strategic state is rebuilt from closed-D1 price/MA50 history.

The unresolved Extreme exceptions, personal/workflow material, and any still-unresolved SL/TP provenance issues remain outside authoritative Core until their own explicit reconciliation is complete.'''
new_tail = '''- H4 restart uses verified checkpoint + deterministic replay as engineering policy; D1 current strategic state is rebuilt from closed-D1 price/MA50 history;
- the 49-family Home Course completeness set is fully classified with no unresolved Core semantic HOLD;
- residual Extreme touch/outside-reversal ambiguities are closed by rejection of unsupported universal shortcuts;
- the repeated-LTF Extreme / valid-HTF MHV-or-ReEntry exception is accepted only in bounded MTF scope and does not apply to D1 in the current hierarchy;
- Re-Entry validation-candle / immediately-following live-candle timing is closed at semantic/project-mapping level;
- SL/TP items without universal BBMA broker formulas are explicitly classified as Core, lifecycle principle, context, or project/EA-safety mapping rather than left as undefined Core obligations.

**Current unresolved BBMA Core semantic HOLD count: 0.**'''
one(old_tail, new_tail, 'section 13 tail')

p.write_text(s, encoding='utf-8', newline='\n')
print('Core V2 closure reconciliation applied')
