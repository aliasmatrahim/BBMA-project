# CORE-FIDELITY-292 — CP12 Core §6 MHV/MLV lifecycle
Date: 2026-10-26. Phase: AUDIT / PARTIAL. Issue #292.
Branch: `audit/core-fidelity-20261021`; parent: `3438397b7f62fb51a9752ad52f83556164bb6568` (CP11).
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.

## VERIFIED
- Recovered the live owner and audit refs, latest commit histories, PR #293, Issue #292, current queue/current records, `PROJECT_INSTRUCTIONS.md` §§17–20, SOURCE_INDEX, accepted Core §6/F1 decision, Finale records, implementation-gap register and the exact Build 5.15 owner source. PR #293 remains open/draft/unmerged and explicitly says DO NOT MERGE; PR/issue comment checks returned zero comments. Owner SHA remains unchanged.
- Source chain used: accepted Core V2 §§6.1–6.8; primary PDF-derived rule index pp.2, 7–8; secondary technique reference pp.31–34; Finale V05 00:18:07–00:28:12 and V01 00:59:18–01:00:05; F1 lifecycle decision; C039/C040; exact owner code. Raw PDF binaries were not reopened in this connector pass.
- M09 is a canonical **M15-only** lifecycle. `PairState` has only BUY/SELL MLV states and initializes each to PERIOD_M15. `IsMHVParentExtremeMature` requires a valid, confirmed M15 Extreme parent; `AttachCanonicalMHVParent` records parent raw/confirmation identity.
- M09 owner stages map to F1/Core §6: reversal-confirmed parent → later normal TP-Wajib MA5/MA10 area interaction → inside-BB loss-of-prior-momentum phase without prior-direction CSM → min BodyBottom/max BodyTop accumulation → first later close-away establishes formation and freezes the pre-trigger body → later frozen-body range/wick retest or same-cycle eCSD/CSD direction takeover.
- Outer-BB/prior-direction Momentum invalidation is checked before same-cycle direction takeover. Opposite RAW Extreme is only a candidate; the later reversal-confirmation installs the opposite-cycle parent and atomically supersedes old provenance. The canonical path has no generic candle/session/day expiry.
- M27 updates both M08 M15 Extreme owners before calling M09 for both MHV directions. M15 SELL Extreme parents BUY MHV; M15 BUY Extreme parents SELL MHV. The same M15 closed eCSD/CSD snapshots are passed as direction-takeover context.
- M13 exports the M15 MHV signal and passes the persistent MLV state to combination building. REM remains H4 RE + H1 Extreme + M15 MHV/MLV. The accepted mature state includes FORMATION_ESTABLISHED with frozen body, so retest completion is not required for the REM leg. M14 validates the exact component/timeframe signature. M16 checks the persistent M15 direction, mature state, frozen body and exact formation candle identity; the owner has no generic expiry.
- M12N is read-only. It captures and displays the M15 MLV overlay; the H4/H1 node builders do not capture an MHV state. Build 5.15 has no H4/H1 MHV owner or `H4_MHV_WATCH` implementation.
- Current C039/C040 decisions document bounded HTF observer/context semantics but explicitly do not authorize MQL4 source changes by themselves. The source feature is absent and needs its own scoped contract/task; this is separate from canonical M09/Core §6 compliance.
- Historical IG-01–IG-03 and the old P1 M09 repair claim are stale against this owner and are not patch instructions. The CP07 Build 5.22 portable probe covers stale MLV component admission only; it does not verify M09 lifecycle parity.
- Updated the incremental source matrix, cross-module connection ledger, implementation-gap register, Finale master index, CURRENT and MASTER_QUEUE. No EA source or owner artifact changed.

## PARTIAL / NOT VERIFIED
- CP12 is a static owner/source reconciliation. No M09-focused test, native compile, Strategy Tester or attributable broker/runtime run was performed. M09/F1 TP-Wajib and lifecycle parity remains NOT VERIFIED.
- Qualified G40 history remains NOT VERIFIED; Strategy Tester remains NOT RUN. No terminal restart, merge or trading action occurred.
- A standalone M09 contract is still absent. The C039/C040 HTF MHV observer/context extension is unimplemented and requires a separate scoped task/contract before source changes.
- Full Core/module/runtime denominator remains PARTIAL; no conclusion here certifies runtime parity or trading readiness.

## Exact next action
Audit accepted Core §7 CSD/eCSD against the M10 source contract and owner, then trace M10 → M12 → M13/M27 handoffs. Keep source behavior unchanged unless the evidence establishes an authorized mismatch. Strategy Tester remains gated on qualified G40 history.
