# Post-P0 Protected-Surface Regression Matrix — PREP ONLY

Date: 2026-08-26  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / DOCUMENTATION-ONLY / EXECUTION BLOCKED UNTIL P0 #94 BROKER-RUNTIME PASS**

## 1. Purpose

Define the exact regression gate that must be run after P0 EXEC_ID runtime acceptance and before the v4.59 execution-identity fix is canonicalized onto `d1-owner-dev`.

This record does not modify `blueprint/source/BBMA_EA.mq4`, does not merge branches, does not enable D1TPW or C044, and does not change BBMA strategy, SL/TP, MM/risk, lifecycle, portfolio, or execution authority.

Its purpose is to make one thing explicit: after P0 passes runtime, the integration is accepted only if the execution/recovery fix is present and every unrelated protected surface remains semantically unchanged.

## 2. Current source-lineage snapshot

At preparation time:

- canonical development branch: `d1-owner-dev`;
- canonical head: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`;
- canonical head is documentation-only relative to the shared EA-source merge base;
- P0 branch head before this record: `90f9b3191c5e190da541905f6dcd7a1b07389660`;
- P0 production implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- P0 source build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`;
- `#property version "4.59"`;
- P0 source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`;
- `EnableD1TPWLifecycle=false`;
- `EnableC044Lifecycle=false`.

The final integrated source identity must be captured again after a fresh integration branch is created from the then-current `d1-owner-dev`. The identities above are preparation references, not permission to skip fresh identity capture.

## 3. Integration rule before regression

After P0 Issue #94 broker/demo runtime PASS:

1. create a fresh integration branch from the then-current `d1-owner-dev`;
2. preserve all current canonical documentation/audit history;
3. apply only the reviewed P0 production EA-source execution/recovery delta;
4. do not merge the hotfix branch wholesale;
5. exclude one-shot trigger/workflow plumbing unless separately approved as permanent infrastructure;
6. run this protected-surface regression before updating `d1-owner-dev`.

A regression result on the isolated P0 branch is not a substitute for regression on the exact integrated candidate.

## 4. Allowed semantic delta

The integrated EA source is allowed to differ from the canonical pre-P0 source only in the following functional areas:

### A. M22 execution identity / ambiguous result handling

Allowed:

- compact broker comment `BBMA|H:<16hex>`;
- terminal-side durable execution identity persistence;
- local identity first for duplicate lookup and post-send verification;
- broker `OrderComment()` as secondary/fallback evidence only;
- no `REC_NORMAL` path when durable local identity persistence failed;
- MT4 error 128 classified as ambiguous/fail-closed rather than blindly retryable;
- reconciliation logic needed to prove or safely reject an ambiguous send result.

Not allowed under P0:

- changing entry eligibility;
- changing approved signal direction;
- changing lot sizing;
- changing SL/TP coordinates;
- changing risk percentages or portfolio limits;
- changing normal lifecycle exit semantics.

### B. M24 persistence/recovery identity integration

Allowed:

- durable execution-hash/ticket persistence using terminal GlobalVariables;
- ticket/magic/open-time/direction cross-validation;
- local-first recovery/history reconstruction;
- compact broker-hash fallback/migration support;
- safe recovery classification when only compact identity is available;
- fail-closed handling when durable identity is absent/corrupt/ambiguous.

Not allowed under P0:

- inventing strategy owner state;
- changing D1/C044 lifecycle state-machine semantics;
- reconstructing unsupported signal events;
- changing M20 emergency precedence;
- allowing identity ambiguity to create a new trade.

### C. Build/user-facing identity

Allowed:

- source header/build marker update to v4.59;
- `#property version "4.59"`;
- dashboard/init build identity synchronization.

No other display/input behavior change is authorized by P0.

## 5. Protected-surface regression matrix

| ID | Protected surface | Required invariant | Allowed P0 delta | PASS evidence | FAIL condition |
|---|---|---|---|---|---|
| PS-01 | M06–M12 detectors | Extreme, BB, MHV/MLV, CSD/eCSD/CSM, Re-Entry detection semantics remain unchanged | none | source diff/static checks show no detector-formula or state-transition semantic change | any detector threshold/formula/state ownership change |
| PS-02 | M12N NMJE | observation/research-only boundary remains unchanged; no execution authority introduced | none | no new entry/close/risk authority from M12N | NMJE influences trading authority or N3 activation |
| PS-03 | M13 collector | remains collector of already-owned signals/components only | none | no new interpretation/confirmation inside M13 | M13 creates or upgrades strategy authority |
| PS-04 | M14 validator | combination/sequence validation semantics unchanged | none | same validation rules and ownership boundaries | new filtering, direction rewrite, score authority or lifecycle logic |
| PS-05 | M15 final authority | remains sole final new-entry authority on closed M15 processing clock | none | no bypass path to M22; same closed-candle gating | direct detector/M23/M24 execution path bypasses M15 |
| PS-06 | M16 invalidation | existing expiry/invalidation/compaction semantics unchanged | none | no altered invalidation precedence or owner reconstruction | candidate lifetime or direction invalidation changes |
| PS-07 | D1 strategic owner | BUY/SELL/TRANSITION/UNRESOLVED semantics unchanged | none | D1 owner producer/consumer logic unchanged | P0 changes D1 owner formula, direction, transition or fail-closed rules |
| PS-08 | D1 Opportunity | family identity, tactical exception scope and dedup semantics unchanged except execution persistence below | durable execution hash storage only | same DecisionID/family/direction generation; only persistence path differs | family materialization/direction/eligibility changes |
| PS-09 | RE/REM/RRE/REE | canonical family definitions, selected component ownership and direction remain unchanged | none | no strategy-family diff outside identity transport | any changed composition, priority, source timeframe or direction rule |
| PS-10 | M17 SL/TP | structural SL provenance and current TP/lifecycle classification remain unchanged | none | same inputs/outputs for identical decision + market snapshot | SL anchor, spread buffer, TP mapping, MinRR semantics or targetless classification changes |
| PS-11 | M21 money management | frozen lot sizing uses unchanged final SL/risk model | none | same lot result for same validated inputs | lot formula, caps, normalization or MM-mode semantics change |
| PS-12 | M19 risk | trade-level risk admission semantics unchanged | none | same accept/reject result from same risk snapshot | risk threshold/formula/order changes |
| PS-13 | M20 portfolio/emergency | portfolio limits and emergency-close precedence unchanged | none | emergency authority still precedes normal lifecycle close | M22/M23/M24 identity logic bypasses or delays M20 authority |
| PS-14 | M22 normal send payload | pair, direction, lot, entry, SL, TP and magic stay from approved decision | identity/comment + ambiguous reconciliation only | order payload geometry unchanged except compact comment | M22 recalculates strategy, lot, SL or TP |
| PS-15 | M22 retry policy | only confirmed retryable errors may retry; ambiguous error 128 does not blindly resend | P0 change required | 128 routes to reconciliation/fail-closed; no duplicate send loop | 128 or other ambiguous result triggers blind retry |
| PS-16 | M22 duplicate protection | same execution identity cannot create another ticket | P0 change required | local-first lookup + runtime evidence | duplicate ticket for one execution hash/DecisionID |
| PS-17 | M23 lifecycle semantics | C044/D1TPW/normal lifecycle close state machines unchanged and dormant gates stay OFF | none | no strategy-exit semantic diff | P0 edits event criteria, close reason, lifecycle owner, or gate default |
| PS-18 | M24 recovery ownership | recovery persists exact-owned trades without fabricating strategy authority | identity persistence/recovery only | local durable hash used first; fallback is secondary | recovery invents owner/cursor/signal data or silently drops exact-owned trade |
| PS-19 | C044 gate | `EnableC044Lifecycle=false` in canonical integrated baseline | none | exact declaration remains OFF | default ON or implicit activation path |
| PS-20 | D1TPW gate | `EnableD1TPWLifecycle=false` in canonical integrated baseline | none | exact declaration remains OFF | default ON or implicit activation path |
| PS-21 | N3 firewall | `execution_policy=NONE`; no relation-based trading activation | none | no active N3 execution marker/path | N3 gains order/close authority |
| PS-22 | Inputs/defaults | user inputs unrelated to P0 remain unchanged | none | normalized input declaration comparison | changed default risk, trade limits, pair list, MM, MinRR, spread, lock mode, etc. |
| PS-23 | Magic identity | existing StrategyID/InstanceID/pair magic-generation semantics unchanged | none | same magic for same configuration | magic range/formula changes |
| PS-24 | Closed-candle timing | processing-clock and source-candle timing semantics unchanged | none | no current/forming-candle shortcut introduced | tick/current-bar entry authority introduced |
| PS-25 | Trade registry | successful order remains added/owned according to existing architecture | identity-state update only | monitored ownership and risk visibility preserved | identity failure hides live trade from portfolio/risk ownership |
| PS-26 | Broker comment authority | broker comment is no longer sole authority | P0 change required | blank/replaced comment does not erase valid local identity | recovery still depends exclusively on `OrderComment()` |
| PS-27 | Legacy compatibility | legacy full comment parser may remain fallback only | compatibility allowed | old metadata parser does not override validated local identity | legacy comment can contradict and replace stronger local identity silently |
| PS-28 | Build identity | header/property/dashboard/init all identify same v4.59 integrated candidate | P0 change required | exact consistent strings/version | mixed v4.58/v4.59 user-facing identity |
| PS-29 | Compile cleanliness | exact integrated MQ4 compiles in official MT4 MetaEditor | none | 0 errors / 0 warnings | any compile error or warning |
| PS-30 | Runtime attribution | compiled EX4/logs correspond to exact integrated source blob/SHA | none | commit/blob/SHA/EX4 hash all recorded | evidence cannot be tied to exact candidate |

## 6. Focused cross-module execution-path regression

The minimum execution-path review must follow this order:

`M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22 -> M24`

with lifecycle sanity through M23.

For one representative validated BUY and one representative validated SELL decision, verify the following invariant chain conceptually/staticly:

1. M15 produces the same approved decision identity/direction as before P0;
2. M16 does not change validity for P0 reasons;
3. M17 resolves the same hard SL/TP classification;
4. M21 resolves the same lot from the same inputs;
5. M19 accepts/rejects on the same trade-risk rule;
6. M20 accepts/rejects on the same portfolio/emergency rule;
7. M22 sends the same trade payload except for compact broker comment and new identity persistence/reconciliation behavior;
8. M24 stores/reconstructs execution identity without changing strategy ownership;
9. M23 receives no new strategy authority from P0.

Any discrepancy before M22 identity handling is presumed outside approved P0 scope and blocks canonicalization until explained or corrected.

## 7. Diff classification rule

Every integrated-source diff hunk must be classified as one of:

- `P0_REQUIRED` — directly necessary for compact identity, durable local identity, local-first lookup/recovery, ambiguous-send reconciliation, or build identity sync;
- `P0_SUPPORTING` — non-semantic support required to compile/integrate the P0 fix safely;
- `UNRELATED_EXPECTED` — only if the latest `d1-owner-dev` itself gained an independently approved source change after this preparation record; must be traced to its own commit/decision;
- `UNAUTHORIZED` — any unexplained strategy/MM/risk/lifecycle/input semantic change.

`UNAUTHORIZED` is an automatic regression FAIL.

Do not hide an unrelated source change inside a P0 integration commit merely because the final compile passes.

## 8. Specific forbidden-drift checklist

The integrated candidate must fail review if any of these appear without a separately approved source decision:

- RSI, MACD, Stochastic, ADX, news/session/volatility/correlation entry filters;
- new score-based trading authority;
- current/forming-candle execution shortcut;
- changed D1 strategic-owner formula;
- changed Re-Entry/REM/RRE/REE composition;
- new SL formula, lookback, ATR/fractal/swing substitution;
- TP stretching to manufacture RR;
- changed AutoLot/risk percentage math;
- changed `MaxTotalRiskPercent`, drawdown/basket semantics or portfolio-limit logic;
- trailing stop, breakeven, partial close, TP2 or TP3;
- D1TPW/C044 default activation;
- N3 execution-policy activation;
- any duplicate-send workaround that retries an ambiguous broker result without identity reconciliation.

## 9. Identity-specific regression checks

Because P0 exists specifically to repair durable execution identity, the following are mandatory positive checks on the integrated candidate:

### PR-ID-01 — Compact comment

`CreateOrderComment()` must produce only compact hash-oriented broker metadata suitable for the observed broker limit.

### PR-ID-02 — Durable local write

After a broker-confirmed new order, terminal-side execution identity must be written and flushed before the trade is considered normally recoverable.

### PR-ID-03 — Cross-validation

Loaded local identity must validate ticket/magic/open-time/direction and its reverse hash->ticket relationship rather than trusting one unverified GlobalVariable.

### PR-ID-04 — Local-first duplicate lookup

Duplicate search must check durable local identity before relying on broker comment text.

### PR-ID-05 — Local-first recovery/history

Open-order recovery and execution-history reconstruction must prefer validated local identity, using broker compact/full comment only as fallback/migration evidence.

### PR-ID-06 — Broker blank comment tolerance

A valid locally persisted identity must remain usable if broker `OrderComment()` is blank or mutated.

### PR-ID-07 — No false normal state

If durable identity write/verification fails for a fresh order, recovery status must not be promoted to `REC_NORMAL` merely because the broker order exists.

### PR-ID-08 — Ambiguous timeout

MT4 error 128 must not be treated as an ordinary retryable failure. It must enter ambiguous reconciliation/fail-closed handling to prevent accidental duplicate execution.

## 10. Runtime evidence required before this matrix may execute

This regression matrix is not itself permission to integrate.

Issue #94 must first have broker/demo evidence from a fresh v4.59 order proving:

- immediate `[P3S5][EXEC_ID]` reports `Persist=PASS Local=Y`;
- broker comment may be blank without invalidating local identity;
- full EA/terminal restart recovers the same live ticket;
- the order does not become `REC_IDENTITY_MISSING_FROZEN` solely because broker comment is absent;
- same DecisionID/execution hash cannot produce a second live ticket.

If P0 runtime fails, return to the isolated defect branch; do not run canonical integration merely to see whether regression passes.

## 11. Evidence package for regression closure

The post-P0 integration closure audit must record at minimum:

- latest canonical base commit used to create integration branch;
- exact integrated commit SHA;
- integrated `BBMA_EA.mq4` Git blob SHA;
- exact MQ4 SHA-256;
- build marker and `#property version`;
- exact D1TPW/C044 gate defaults;
- reviewed diff classification summary (`P0_REQUIRED/P0_SUPPORTING/UNRELATED_EXPECTED/UNAUTHORIZED`);
- PS-01..PS-30 result table;
- official MetaEditor compile log/result;
- EX4 SHA-256;
- Issue #94 runtime evidence references;
- explicit statement that no protected BBMA strategy/MM/risk/lifecycle surface drifted unintentionally.

## 12. PASS / FAIL rule

### PASS

This matrix is PASS only if:

- P0 broker/runtime predecessor gate is already PASS;
- every protected surface PS-01..PS-30 is PASS or explicitly `NOT_APPLICABLE` with a documented reason;
- no diff hunk is `UNAUTHORIZED`;
- D1TPW and C044 remain OFF;
- N3 remains execution-firewalled;
- exact integrated source compiles 0 errors / 0 warnings;
- exact source/build/EX4 evidence identity is complete.

### FAIL

Any of the following is a hard FAIL:

- strategy/MM/risk/lifecycle drift unrelated to P0;
- ambiguous source lineage;
- missing or inconsistent build identity;
- lifecycle gate accidentally ON;
- error 128 blindly retryable again;
- broker comment restored as sole execution identity authority;
- local identity lost from duplicate/recovery/history path;
- duplicate execution possible for one durable identity;
- compile error or warning.

## 13. Canonicalization boundary after PASS

Only after this matrix PASS:

1. update `d1-owner-dev` to the reviewed integrated candidate;
2. record final source blob/SHA/build/EX4 identity in a dedicated P0 closure audit;
3. update `CURRENT.md` and `MASTER_QUEUE.md` only as necessary;
4. close Issue #94 with runtime + regression + compile evidence;
5. freeze the new post-P0 baseline;
6. re-baseline the runtime tooling to that exact canonical identity;
7. resume R1 -> R2 -> R3 -> R4 -> R5 -> R6.

Do not merge to `main` merely because P0 closes.

## 14. Preparation verdict

**POST-P0 PROTECTED-SURFACE REGRESSION MATRIX READY. EXECUTION REMAINS BLOCKED BY P0 #94 BROKER-RUNTIME ACCEPTANCE.**

No EA source, strategy rule, lifecycle gate or canonical branch was modified by this preparation record.
