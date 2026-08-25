from pathlib import Path

current = Path('blueprint/CURRENT.md')
queue = Path('blueprint/MASTER_QUEUE.md')

current_marker = '# 2026-08-26 N1-N3 Technical Completion Overlay'
queue_marker = '## 2026-08-26 — N1-N3 Completion / Runtime-First Queue Overlay'

current_overlay = r'''

# 2026-08-26 N1-N3 Technical Completion Overlay

This is the latest NMJE phase-status overlay and supersedes older wording that says N1/N2/N3 are parked or unfinished. Historical sections remain provenance only.

## N1-N3 status
- **N1/N1.1: CLOSED / PASS — observation-only.** Coverage and call-order reconciliation are recorded in `blueprint/N1_NMJE_V458_FINAL_CLOSURE_AUDIT_20260826.md`.
- **N2: CLOSED / PASS — research & telemetry complete.** Source ownership guard + synthetic identity/research suite passed run `32912134419`, job `98008262714`. Real forward outcomes remain an evidence dependency, not an N2 implementation gap.
- **N3: TECHNICALLY COMPLETE / CLOSED — execution policy NONE / inactive.** Evidence-to-policy review-readiness tooling and activation firewall passed run `32912473753`, job `98009255525`. Any future execution policy still requires real N2 forward evidence plus separate explicit strategy approval.

## Frozen EA candidate
- build: `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage`;
- `#property version "4.58"`;
- source blob: `a166ffb23aba5e6b4011a28d9de8896cd00e33a1`;
- canonical SHA-256: `ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc`;
- native MetaEditor: **0 errors / 0 warnings**;
- `EnableD1TPWLifecycle=false`;
- `EnableC044Lifecycle=false`.

N1-N3 completion changed only documentation/contracts/research tools/tests/CI. `blueprint/source/BBMA_EA.mq4` remained unchanged throughout the phase.

## Hosted smoke
v4.58 hosted MT4 probe run `32909061219`, job `97999302151` compiled 0E0W and launched MT4 build 1478 with no fatal runtime signature. Classification remained `HOSTED_ENVIRONMENT_UNCLASSIFIED_NO_FATAL_SIGNATURE`; this is smoke evidence only, not broker-runtime closure.

## Current next gate
**Broker/runtime closure against the frozen v4.58 candidate.** Do not reopen N1-N3 source work without new runtime evidence or a separately approved N3 strategy policy.

Canonical phase freeze record:
`blueprint/N1_N3_V458_PHASE_COMPLETION_RC_FREEZE_20260826.md`
'''

queue_overlay = r'''

## 2026-08-26 — N1-N3 Completion / Runtime-First Queue Overlay

> This overlay supersedes the earlier v4.58 queue sentence stating `N1/N2/N3 remain parked`. N1-N3 technical work is now complete. Historical queue entries remain provenance only.

### Closed — do not requeue without new evidence
- **N1/N1.1 NMJE observation/coverage:** CLOSED / PASS.
- **N2 NMJE research/telemetry/identity pipeline:** CLOSED / PASS.
- **N3 NMJE evidence-to-policy staging:** TECHNICALLY COMPLETE / CLOSED; `execution_policy=NONE`, activation inactive.
- N1-N3 protected-surface comparison confirms no EA source change; v4.58 source remains blob `a166ffb23aba5e6b4011a28d9de8896cd00e33a1`.

### Active execution order — broker/runtime closure
1. **D1 TP-Wajib lifecycle runtime gate** — restart/checkpoint, closed-D1 TPW completion, close idempotency, no duplicate close/new entry.
2. **C044 runtime gate** — checkpoint/replay, failed-Momentum close, Momentum -> next Re-Entry re-arm, opposite mature Extreme supersession, M20 precedence.
3. **D1 owner / D1O runtime matrix** — BUY/SELL/TRANSITION/UNRESOLVED, stable execution hash, invariant direction, D1O dedup identity.
4. **Validation -> order timing** — prove closed validation candle can execute only in the intended following live candle; capture actual `OrderOpenTime()`.
5. **M17 structural SL runtime** — BUY/SELL and JPY/non-JPY geometry with live broker specifications.
6. **Remaining P3/Core runtime traces** — F1-F6, TradeLock, cumulative prospective risk and remaining live Tests B/C/D.
7. **N2 real forward outcome collection** — collect broker-connected `[N1-NMJE] -> [N2-NMJE-DEC] -> [N2-NMJE-OUT]` evidence for any future N3 policy review.

### N3 activation boundary
`REVIEW_READY` is only evidence-review readiness. It is never automatic trading authority. Any future relation-based execution policy requires a new dated strategy decision, explicit approval, default-OFF implementation, protected-surface regression, native 0E0W and broker/demo validation.

### Freeze rule
Do not modify v4.58 strategy source opportunistically while these runtime gates are being attributed. A source patch requires either a concrete runtime defect or a separately approved strategy change.

Phase freeze record:
`blueprint/N1_N3_V458_PHASE_COMPLETION_RC_FREEZE_20260826.md`
'''

ct = current.read_text(encoding='utf-8')
qt = queue.read_text(encoding='utf-8')
changed = []
if current_marker not in ct:
    current.write_text(ct.rstrip() + current_overlay + '\n', encoding='utf-8')
    changed.append(str(current))
if queue_marker not in qt:
    queue.write_text(qt.rstrip() + queue_overlay + '\n', encoding='utf-8')
    changed.append(str(queue))
print('TRACKING_CHANGED=' + ','.join(changed) if changed else 'TRACKING_ALREADY_SYNCED')
