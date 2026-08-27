# NMJE N3 Pre-Enforcement Contract Draft — 2026-08-27

Status: DRAFT / DOCUMENTATION ONLY / NO EA SOURCE CHANGE
Purpose: define the minimum architecture that must be satisfied before NMJE may become an execution-aware gate.

## 1. Role
NMJE is BBMA multi-timeframe journey/lineage context infrastructure. It is not a new strategy, signal detector, score, optimizer or order executor.

## 2. Authority boundaries
- M08 owns Extreme lifecycle.
- M09 owns MHV/MLV lifecycle.
- M10 owns canonical direction/Momentum/eCSD/CSD/CSM event predicates used by owner modules.
- M11 owns D1 strategic owner.
- M12 owns Re-Entry lifecycle.
- M13/M14 own exact REM/RRE/REE combination/signature validation.
- M12N/NMJE derives lineage/context only.
- M15 remains sole final new-entry selector.
- M16 remains final pending-decision revalidator/invalidation authority.
- M22 remains dumb broker execution.
- M23/M24/lifecycle/emergency contracts own live-position exits/recovery.

## 3. Canonical input rule
NMJE consumes owner outputs only. It may not independently redetect Extreme, Re-Entry or MHV/MLV and may not add a third Momentum definition.

## 4. Event identity schema
Every canonical owner event used by NMJE must have deterministic immutable identity sufficient to distinguish separate journeys. Minimum conceptual fields:
- pair;
- canonical owner module/type;
- timeframe;
- direction;
- source/anchor candle time;
- owner cycle/epoch identity where applicable;
- maturity/state;
- valid/terminal status.

Identity must be derived from canonical source-owned facts only. No score/confidence field.

## 5. Journey identity
A JourneyID is a deterministic derived identity built from the exact canonical parent/child EventIDs and setup scope. It must change when canonical ownership/cycle changes and must not change merely because diagnostic labels change.

## 6. Verdict semantics
Minimum semantic outcomes:
- BUILDING / WAIT: source-valid journey incomplete; not automatically reject unless the executable setup requires completion now;
- SUPPORTING: useful context only, not standalone entry authority;
- ALIGNED / VALID: required relationship proven for the setup scope;
- CONFLICT / BLOCK: approved relationship is contradicted;
- UNRESOLVED: required identity/history cannot be proven; fail closed for affected new-entry scope;
- SUPERSEDED: frozen/previous journey owner has been replaced by a newer canonical cycle.

Reason codes are diagnostics, never weights.

## 7. Scope-aware gating
NMJE may enforce only the relationship required by the executable setup contract. It must not require universal perfect D1->H4->H1->M15 nesting.

Exact REM/RRE/REE signatures remain unchanged. NMJE is not a fourth component.

## 8. Maturity preservation
NMJE cannot promote:
- RAW Extreme into executable REM/REE maturity;
- candidate Re-Entry into confirmed Re-Entry;
- pre-formation MHV/MLV into a mature MHV component.

Canonical owner maturity remains authoritative.

## 9. Processing synchronization
Per pair/processing cycle:
1. freeze closed-TF market snapshot/processing epoch;
2. update required canonical owner modules;
3. prove owner-update barrier complete;
4. evaluate NMJE exactly once for that epoch;
5. assemble/validate combinations;
6. M15 selects/freeze candidate + NMJE payload;
7. M16 revalidates frozen owner/journey identity;
8. only validated decision proceeds to risk/SLTP/execution.

Different TF candle times are valid; the epoch proves they belong to one processing pass, not one wall-clock candle.

## 10. M15 frozen NMJE payload
When N3 is enabled, an admitted M15 decision should freeze at least:
- JourneyID;
- verdict;
- reason code;
- relevant parent/child EventIDs;
- processing epoch;
- setup scope/relationship type;
- whether NMJE was required for this candidate.

## 11. M16 revalidation
M16 may verify the frozen NMJE identity against current M12N/canonical owner state but may not recreate owner formulas. Superseded/unresolved/mismatched frozen context invalidates the pending decision according to contract.

## 12. New-entry versus live-position separation
NMJE N3 governs new-entry eligibility/pending decisions only unless a separate source-backed live-position lifecycle rule explicitly says otherwise. Opposite/new cycle must not implicitly close an already-live order.

## 13. Single-writer rule
Only canonical owner modules mutate their underlying strategy state. NMJE, M15 and M16 must not rewrite M08–M12 owner state.

Known pre-N3 issue to resolve: M09 supersession helper currently can install an Extreme parent and must be reconciled with M08 single-writer ownership.

## 14. Recovery/replay
Canonical owner recovery occurs before NMJE journey recovery. For identical closed-candle history, uninterrupted and replayed execution must produce identical:
- owner identities/states;
- JourneyID;
- verdict;
- reason code.

If proof fails, affected journey = UNRESOLVED for new-entry use.

## 15. N2 promotion evidence
Before enabling N3 enforcement, N2 must provide sufficient shadow evidence for:
- BUILDING->ALIGNED;
- CONFLICT;
- UNRESOLVED;
- supersession;
- restart/replay;
- standalone H1 RE;
- REM/RRE/REE;
- D1 opportunities;
- local H4 opposition under D1;
- no-decision/rejected counterfactuals.

No win-rate threshold is a strategy rule. Outcome data is diagnostic only and may be used to detect implementation regressions, not to invent filters.

## 16. Explicit prohibitions
No confidence score, majority voting, weighted TF score, AI/ML ranking, hidden quality filter, session/news/correlation/volatility filters, heuristic TTL, or universal perfect nesting.

## 17. Production gate
N3 cannot be production-locked until:
- dependency hardening findings are resolved;
- N1/N1.1 observer correctness remains PASS;
- N2 evidence gate is satisfied;
- contract is reconciled with Core/source;
- code implements frozen identities/verdicts without authority leakage;
- M12N limiter raised to EXPERT-RESTRICTED;
- native MetaEditor 0E0W;
- static cross-module/Core purity regression PASS;
- deterministic replay/recovery PASS;
- runtime scenarios PASS;
- no implicit live-position close rule is introduced.

## Current boundary
This draft authorizes no EA source modification while the current runtime candidate remains under evidence collection. Source implementation requires the runtime freeze/evidence boundary to be explicitly released or superseded by project decision.
