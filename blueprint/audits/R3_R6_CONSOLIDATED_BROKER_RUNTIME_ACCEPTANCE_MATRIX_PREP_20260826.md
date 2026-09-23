# R3–R6 Consolidated Broker Runtime Acceptance Matrix — PREP ONLY

Date: 2026-08-26  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / EXECUTION ORDER LOCKED R1 -> R2 -> R3 -> R4 -> R5 -> R6 / NOT AUTHORIZED TO SKIP P0 OR PREDECESSOR GATES**

## 1. Purpose

Prepare one exact broker/demo acceptance matrix for the remaining runtime closure sequence after R1 D1 TP-Wajib and R2 C044:

- **R3** — D1 strategic-owner matrix + D1 Opportunity identity/dedup;
- **R4** — validation-candle -> broker-order timing + M17 live structural-SL geometry;
- **R5** — TradeLock + cumulative prospective risk + P3 live Tests B/C/D + execution ambiguity/portfolio controls;
- **R6** — N1/N2 real-forward DecisionID/hash/outcome chain, with N3 execution-policy firewall intact.

This record is documentation/test preparation only. It does not modify `blueprint/source/BBMA_EA.mq4`, does not change strategy, SL/TP, MM/risk, execution or lifecycle semantics, does not activate D1TPW/C044/N3, and does not merge anything into `d1-owner-dev` or `main`.

## 2. Hard predecessor gates

R3–R6 execution remains blocked until the runtime lineage is trustworthy.

Mandatory predecessor order:

1. P0 EXEC_ID Issue #94 passes on a fresh post-fix broker/demo order, including durable local identity, restart recovery and no duplicate execution;
2. accepted P0 delta is integrated onto the latest canonical `d1-owner-dev` history;
3. exact integrated source is compiled by official MT4 MetaEditor at 0 errors / 0 warnings;
4. post-P0 runtime builder/analyzer/observer/collector package is re-baselined to that exact integrated source identity and self/native gates pass;
5. R1 is processed according to its acceptance matrix;
6. R2 is processed according to its acceptance matrix;
7. only then may R3 be formally closed, followed by R4, R5 and R6.

Evidence may be collected opportunistically in the same authenticated demo session where safe, but **later-stage evidence must not be promoted to formal closure ahead of the predecessor stage**.

## 3. Required evidence identity for every R3–R6 bundle

Every attributable runtime bundle must carry at minimum:

- canonical commit SHA;
- canonical MQ4 Git blob SHA;
- exact MQ4 SHA-256;
- build string and `#property version`;
- exact EX4 SHA-256;
- test profile and lifecycle-gate states;
- broker/server and demo/authenticated-session classification;
- terminal restart epoch where applicable;
- pair, ticket, magic, direction, open time and close time where applicable;
- DecisionID / execution hash for executable decisions;
- exact raw log filenames used by analyzer assertions.

Hosted/disconnected/unauthenticated sessions are `BLOCKED`, never PASS.

## 4. Global evidence status vocabulary

Use only:

- `PASS` — exact required behavior is positively demonstrated;
- `FAIL` — contradictory, unsafe, identity-invalid or semantically wrong behavior is observed;
- `INCOMPLETE` — authenticated runtime exists but required scenario/evidence has not occurred;
- `BLOCKED` — authenticated broker/demo runtime or a predecessor gate is unavailable.

Never convert `INCOMPLETE` or `BLOCKED` into PASS.

---

# R3 — D1 Strategic Owner + D1 Opportunity Identity/Dedup

## R3 objective

Prove the live D1 owner states and ensure D1 Opportunity attribution cannot mutate the executable identity or direction of the underlying fresh lower-timeframe decision.

The current runtime runbook requires attributable D1 BUY, SELL and UNRESOLVED evidence plus D1O identity/dedup telemetry. **R3-03 TRANSITION is the exception to natural-occurrence coverage:** after the 2026-09-23 #248 reconciliation, the immediate EMA(Close) transition safety may be proven deterministically by construction because the old non-equality transition examples are mathematically unreachable under the canonical adjacent-bar mapping. Tactical `EXT_TPW` must remain distinct from ordinary strategic-owner-aligned families.

## R3 matrix

| Case | Scenario | Required evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| R3-00 | Authenticated baseline identity | BASELINE profile in broker/demo session | exact build/blob/SHA/profile verified before D1 assertions | identity mismatch, unauthenticated session, wrong profile |
| R3-01 | D1 BUY confirmed | runtime D1 owner telemetry on a fully closed D1 candle | canonical owner reports BUY only when the current source-defined BUY conditions are satisfied | BUY owner appears from forming D1 data or unsupported fallback |
| R3-02 | D1 SELL confirmed | runtime D1 owner telemetry on a fully closed D1 candle | canonical owner reports SELL only when current source-defined SELL conditions are satisfied | SELL owner appears from forming D1 data or unsupported fallback |
| R3-03 | D1 TRANSITION | deterministic proof of canonical EMA50/PRICE_CLOSE immediate-bar reachability + transition fail-closed branch; natural equality sample optional | non-equality transition is proven unreachable by construction, any transition branch carries DIR_NONE, and new-entry readiness accepts only confirmed BUY/SELL | source/formula contradicts the reachability proof, transition gains executable direction, or readiness accepts transition |
| R3-04 | D1 UNRESOLVED | missing/invalid D1 history or equivalent source-defined unresolved condition | new strategy entry fails closed; no fabricated D1 owner | EA guesses BUY/SELL or falls back to H4/LTF authority |
| R3-05 | H4 same-direction under D1 owner | confirmed D1 + compatible H4 setup/owner | downstream eligibility may proceed subject to all other gates | H4 is ignored where contract requires it |
| R3-06 | H4 opposite D1 | confirmed D1 with otherwise-valid opposite H4 direction | new entry is blocked; H4 cannot override D1 | opposite H4 direction executes against D1 owner |
| R3-07 | H4 no-owner where H4 ownership is required | confirmed D1 but source-defined H4 owner absent | affected standalone H1 path fails closed; no D1-only fallback | D1 alone authorizes a path that still requires H4 |
| R3-08 | D1O DecisionID attribution | one valid D1 Opportunity execution candidate | D1O family/source attribution is recorded without changing the canonical fresh decision identity rules | D1 attribution creates an unrelated/mutated execution identity |
| R3-09 | Stable execution hash across non-executable D1 attribution changes | same fresh LTF identity observed through eligible D1O attribution/telemetry changes that do not create a new executable decision | same executable DecisionID maps to one stable execution hash | same DecisionID produces multiple hashes without a new decision identity |
| R3-10 | Direction invariance | track one DecisionID/hash through D1O telemetry | one execution hash never changes BUY<->SELL direction | same hash appears with contradictory directions |
| R3-11 | D1O dedup | repeated processing/restart of same executable D1O identity | no second broker ticket for same execution hash/DecisionID | duplicate ticket appears for same identity |
| R3-12 | D1O restart continuity | restart while D1O-origin trade/identity remains relevant | exact persisted identity remains attributable to same ticket/decision | restart invents a new D1O identity or loses durable identity |
| R3-13 | Tactical `D1_OPP_EXTREME_TPW` separation | capture EXT_TPW family evidence | tactical TPW family remains distinct from ordinary strategic-owner-aligned decision families | EXT_TPW is merged/relabelled as normal aligned family |
| R3-14 | No D1-close side effect | observe owner transition/update with existing live trade | D1 owner transition alone does not create an unapproved live-position close | D1 state change directly closes live trade without approved lifecycle/emergency authority |
| R3-15 | Fully closed D1 only | compare forming vs completed D1 behavior | executable owner update uses fully closed D1 state under existing M15 processing clock | forming D1 candle changes executable owner |

## R3 closure rule

R3 is `CLOSED / PASS` only after authenticated evidence covers all four D1 owner classes and proves DecisionID/hash/direction stability plus D1O dedup. If one owner class has not naturally appeared, R3 remains `INCOMPLETE`.

---

# R4 — Validation-to-Order Timing + M17 Live Structural SL Geometry

## R4 objective

Prove the actual broker order is opened after the closed validation candle and that M17 hard-SL geometry matches the approved structural-range implementation with live broker specifications.

Runtime coverage must include BUY and SELL plus at least one JPY pair and one non-JPY pair where practical.

## R4 matrix

| Case | Scenario | Required evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| R4-00 | Exact validation provenance | selected executable decision with source timeframe and validation/confirmation candle timestamp | analyzer can identify exact source candle and decision before broker execution | order cannot be tied to a unique validation candle |
| R4-01 | Order opens after validation candle | broker `OrderOpenTime()` + validation timestamp | order open time is strictly later than the validation candle timestamp and occurs only in the intended following live source-TF opportunity | order opens on/before validation timestamp or after an unintended extra full-candle delay caused by EA timing |
| R4-02 | No forming-candle validation | live source candle still forming | no execution authority is derived from unclosed validation candle | forming candle directly validates/executes |
| R4-03 | BUY structural window | M12 lifecycle `StartCandleTime..ConfirmationCandle` + lows | structural BUY anchor is the minimum Low over the exact approved window | arbitrary lookback/fractal/BB/ATR/session anchor substitutes the owner window |
| R4-04 | BUY final hard SL | BUY structural low and broker SL | final BUY hard SL = approved structural low minus one Point, with **no spread buffer** | spread is added to BUY SL or SL is inside the approved structural boundary |
| R4-05 | SELL structural window | exact M12 owner window + highs | structural SELL anchor is the maximum High over the approved window | wrong timeframe/window or arbitrary swing substitute |
| R4-06 | SELL structural SL before broker buffer | structural high + one Point | structural SELL coordinate is reconstructed exactly before execution normalization | buffer is mixed into the structural provenance itself |
| R4-07 | SELL spread buffer | frozen preflight spread + final broker SL | added buffer is `max(2.0 pips, ceil(frozen raw spread pips))` and final SL is not inside structural SL | live/chasing spread is used after freeze, buffer < required minimum, or wrong rounding |
| R4-08 | Frozen snapshot consistency | M17/M21 preflight snapshot values | M17 geometry and M21 sizing use the same frozen execution snapshot | risk sizing uses a different later spread/SL snapshot |
| R4-09 | AutoLot reacts to final SL | valid AutoLot trade | lot is sized from final hard SL distance; wider valid SL naturally reduces lot subject to broker constraints | AutoLot uses pre-buffer/pre-normalized SL distance |
| R4-10 | FixedLot unaffected by AutoLot formula | FixedLot scenario | fixed lot stays fixed while normal risk/portfolio gates remain authoritative | FixedLot is silently rescaled by AutoLot path |
| R4-11 | JPY geometry | one JPY pair with valid execution | pip/point conversion and BUY/SELL SL geometry remain correct under JPY digits/specs | 10x/0.1x pip scaling or malformed buffer appears |
| R4-12 | non-JPY geometry | one non-JPY FX pair | same approved geometry is correct under non-JPY broker specs | inconsistent pip/point scaling |
| R4-13 | Broker stop/freeze-level handling | live broker spec + accepted/rejected preflight | final order respects broker geometry without inventing a new strategy SL | EA moves structural owner arbitrarily instead of fail/normalize per approved execution rules |
| R4-14 | Targetless lifecycle payload guard | any R1/R2 lifecycle-managed evidence reused only if exact identity applies | targetless managed trade retains hard SL and broker TP=0 | static TP is reintroduced into lifecycle-managed payload |
| R4-15 | RR non-manufacture | case with changed final SELL SL | reward/TP is not stretched merely to preserve an old RR number | TP is moved solely to manufacture MinRR |
| R4-16 | Source-owner mismatch fail-closed | deliberately or naturally unresolved exact M12 range | affected execution is rejected/frozen rather than guessed | M17 substitutes another timeframe/window silently |

## R4 closure rule

Formal R4 PASS requires:

- at least one attributable BUY and SELL execution;
- at least one JPY and one non-JPY runtime geometry case where practical;
- validation timestamp -> broker open-time proof;
- exact structural-window reconstruction;
- BUY no-spread-buffer proof;
- SELL frozen-spread buffer proof;
- no unauthorized TP/RR compensation.

Missing coverage is `INCOMPLETE`, not PASS.

---

# R5 — TradeLock + Cumulative Risk + P3 B/C/D + Execution Ambiguity

## R5 objective

Prove live execution controls remain sequential, idempotent and fail-closed under portfolio/risk constraints after the P0 execution-identity repair.

This matrix intentionally adapts historical P3 Tests B/C/D to the post-P0 contract: **local durable execution identity is authoritative; broker `OrderComment()` is secondary and may be blank/replaced**.

## R5 matrix

| Case | Scenario | Required evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| R5-00 | TradeLock mode attribution | log exact configured TradeLock mode for each claimed test | analyzer binds verdict to exact current source-defined mode semantics | test claims a mode behavior without recording the active mode |
| R5-01 | TradeLock allow case | pair/direction state permitted by configured mode | eligible decision reaches later gates normally | allowed trade is blocked by stale/wrong lock predicate |
| R5-02 | TradeLock block case | pair/direction state prohibited by configured mode | decision rejects before OrderSend with attributable lock reason | prohibited concurrent exposure executes |
| R5-03 | Opposite-direction integrity | same-pair/opposite-direction condition relevant to configured mode | behavior matches current corrected source predicate and cannot create contradictory unintended exposure | reversed predicate or unintended opposite execution reappears |
| R5-04 | Sequential risk decision A | first valid decision in multi-pair same scan window | proposed/final risk is recorded and A outcome is attributable | A risk cannot be reconciled to executed/rejected state |
| R5-05 | Decision B sees A consumed budget | second valid decision after A executes in serialized scan | existing risk for B includes A immediately | B calculates against stale pre-A portfolio risk |
| R5-06 | `REJ_TOTAL_RISK` arithmetic | A consumes enough budget that B prospective total exceeds `MaxTotalRiskPercent` | B rejects and raw arithmetic supports the rejection | rejection marker exists but arithmetic does not, or B is admitted above cap |
| R5-07 | No phantom reservation | A fails/does not execute, B follows | B does not count A as live consumed risk | failed A reserves phantom risk against B |
| R5-08 | Existing-risk resolution fail-closed | a live trade's risk cannot be safely resolved | new admission fails closed; unknown risk is never treated as zero | unresolved live risk is ignored |
| R5-09 | Portfolio limit positive rejection | configured portfolio cap naturally reached | next otherwise-valid decision rejects with attributable portfolio evidence | order executes beyond configured cap |
| R5-10 | P3 Test B — frozen-state log suppression | legacy/frozen recovery condition plus multiple subsequent cycles | recovery/freeze diagnostic is reconstruction-scoped and does not spam every cycle | repeated recovery-freeze spam persists each cycle |
| R5-11 | P3 Test C — fresh post-P0 EXEC_ID | genuine fresh M22 execution from accepted integrated build | `[P3S5][EXEC_ID]` proves `Persist=PASS` and durable local identity (`Local=Y` or exact post-P0 equivalent); broker hash/comment may be present or absent as secondary evidence | local persistence fails or broker comment is still sole authority |
| R5-12 | P3 Test D — restart after fresh persisted trade | keep R5-11 ticket open, restart EA/terminal | same exact ticket recovers without identity-missing freeze caused solely by blank comment; no duplicate ticket | durable identity is lost or duplicate execution occurs |
| R5-13 | Execution hash uniqueness | aggregate live/history evidence | one execution hash maps to one broker ticket for a single execution identity | same hash maps to multiple tickets without an approved new identity |
| R5-14 | Broker comment stripped/blank | fresh accepted build trade where server returns blank/replaced comment | identity/recovery remains valid from local persistence | order freezes/duplicates solely because comment is blank |
| R5-15 | Error 128 timeout ambiguity | controlled/safe occurrence or deterministic existing test evidence | timeout is treated as ambiguous and reconciliation fails closed unless exact server result is proven | error 128 is blindly retried and may duplicate order |
| R5-16 | Other retryable errors | safe broker/demo occurrence where current source classifies retryable | retry behavior follows exact current classification and remains idempotent | retry class drifts or creates duplicate ticket |
| R5-17 | Ambiguous-result reconciliation | broker result cannot be proven accepted/rejected immediately | EA refuses to claim a second execution until exact result reconciliation proves state | uncertainty becomes an automatic second OrderSend |
| R5-18 | Hard-invalid recovery separation | naturally available invalid geometry/lot case or deterministic test fixture | hard-invalid remains distinct from identity-only frozen/recoverable states | invalid trade is fabricated into normal recovery |
| R5-19 | Emergency precedence over frozen/normal management | safe demo/test facility only | M20 emergency authority can still liquidate exact-owned risk before lower normal lifecycle/recovery freeze blocks it | normal lifecycle/recovery lock prevents authorized emergency close |
| R5-20 | Dashboard/registry exact-owned consistency | compare actual exact-owned open tickets to internal active count during R5 runs | active count equals current exact-owned broker positions after compaction/recovery | stale closed/frozen registry inflates active count |

### TradeLock evidence rule

This preparation record does not redefine or invent TradeLock enum semantics. The post-P0 analyzer must bind each R5-00..R5-03 verdict to the exact enum/value and predicate present in the final integrated source. If a mode has not been exercised, that mode remains `INCOMPLETE`.

### P3 post-P0 reinterpretation rule

Historical P3 Test C expected broker comment persistence. That expectation is superseded for the accepted P0 lineage. For the post-P0 build:

- durable terminal-side local identity is the primary acceptance requirement;
- broker comment/hash is fallback/secondary evidence;
- blank broker comment is not a failure by itself;
- restart recovery and duplicate protection are the decisive runtime outcomes.

## R5 closure rule

R5 PASS requires attributable TradeLock allow/block evidence for the active claimed modes, cumulative-risk arithmetic across at least two sequential decisions, post-P0 P3 Tests B/C/D, no duplicate identity, and fail-closed broker ambiguity handling. Unsafe emergency cases may remain `INCOMPLETE` if no safe controlled demo evidence exists; never manufacture loss merely to force a PASS.

---

# R6 — N1/N2 Real-Forward Identity/Outcome Chain + N3 Firewall

## R6 objective

Prove the research telemetry chain can follow a real broker-connected decision from observation to validated decision shadow to closed outcome without becoming trading authority.

Required runtime markers:

`[N1-NMJE] -> [N2-NMJE-DEC] -> [N2-NMJE-OUT]`

N3 remains `execution_policy=NONE` and must not influence entry, sizing, SL/TP, lifecycle close or broker execution.

## R6 matrix

| Case | Scenario | Required evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| R6-00 | N1 observation present | broker-connected strategy journey produces `[N1-NMJE]` | observation is timestamped/attributable and read-only | N1 itself changes executable decision |
| R6-01 | N2 validated decision shadow | executable/validated decision produces `[N2-NMJE-DEC]` | shadow carries reconcilable DecisionID/hash/pair/direction/source identity | shadow cannot reconcile to the actual decision |
| R6-02 | N2 closed outcome shadow | same tracked broker position later closes | `[N2-NMJE-OUT]` reconciles to exact ticket/DecisionID/hash and actual close outcome | outcome is assigned to wrong ticket/identity |
| R6-03 | End-to-end one-ticket chain | one complete forward lifecycle | N1 -> N2 DEC -> broker execution -> N2 OUT can be traced without identity ambiguity | chain breaks or changes identity midstream |
| R6-04 | Direction invariance | track DecisionID/hash through N1/N2/outcome | direction remains invariant for same execution identity | same hash is observed as BUY and SELL |
| R6-05 | Duplicate decision observation | repeated N1/N2 observation of same decision | telemetry may repeat observations as designed but cannot create another broker execution | research observation causes duplicate order |
| R6-06 | Restart continuity | restart while tracked position remains live | N2 attribution resumes against exact persisted execution identity | restart creates new shadow identity for same ticket without provenance |
| R6-07 | Closed-history reconciliation | position closes by TP/SL/lifecycle/emergency/manual external path as supported by analyzer scope | close classification is taken from actual broker history and linked to exact ticket | synthetic/guessed outcome replaces broker history |
| R6-08 | Identity ambiguity fail-closed | deliberately malformed fixture or naturally conflicting identity evidence | analyzer/runtime telemetry marks ambiguity invalid/fail-closed | ambiguous identity is silently assigned to a trade |
| R6-09 | Multiple simultaneous tracked trades | two+ exact-owned positions with N2 shadows | each ticket retains separate DecisionID/hash/outcome chain | outcomes cross-link between tickets |
| R6-10 | N3 execution policy is NONE | inspect runtime markers/config/build | no active N3 execution policy exists | `N3_POLICY_ACTIVE` or `N3_EXECUTION_POLICY` appears without approved activation |
| R6-11 | N3 cannot alter entry | compare executable decisions with N3 research state | N3 research metadata does not create/block/redirect broker entries | N3 relation becomes entry authority |
| R6-12 | N3 cannot alter sizing/risk | compare M21/M19 values to N3 state | lot/risk result remains owned by approved EA risk pipeline | N3 changes lot/risk budget |
| R6-13 | N3 cannot alter SL/TP/lifecycle | inspect M17/M23/lifecycle state | N3 does not alter hard SL, TP, targetless lifecycle state or close reason | research policy changes strategy/risk exit behavior |
| R6-14 | Observer remains read-only | static/runtime observer evidence | observer has no OrderSend/OrderClose/OrderModify/state-mutating authority | observer can trade or mutate EA-owned runtime GlobalVariables |
| R6-15 | Bundle assertion integrity | analyzer `assertions.json` or successor references | every assertion resolves to actual raw evidence in bundle | assertion cites missing/nonexistent raw evidence |
| R6-16 | Forward sample incompleteness handling | insufficient naturally closed tracked trades | analyzer returns `INCOMPLETE`, not fabricated PASS | small/no outcome sample is promoted to PASS |

## R6 closure rule

R6 formal PASS requires at least one complete authenticated real-forward N1 -> N2 decision -> exact broker ticket -> N2 outcome chain with unique DecisionID/hash reconciliation, restart/identity safety where applicable, and positive proof that N3 remains firewalled at `execution_policy=NONE`.

R6 is evidence-pipeline closure only. It is **not** approval to activate any N3 trading policy.

---

# 5. Cross-stage regression invariants

The following invariants apply to every R3–R6 run:

1. P0 local durable execution identity remains authoritative; broker comment is secondary only.
2. Same DecisionID/execution hash must not create duplicate broker tickets across restart or ambiguous server responses.
3. M15 remains final new-entry authority under the current architecture.
4. Existing detector ownership remains unchanged; runtime validators/analyzers do not recreate strategy formulas.
5. M17 owns approved hard-SL resolution/validation; M21 sizes from final SL; M19/M20 retain risk/emergency authority.
6. R1/R2 lifecycle gates must match the selected test profile; never accidentally run both ON in a normal acceptance profile.
7. N3 remains activation-firewalled at `execution_policy=NONE`.
8. No production/real-risk account needs to be endangered to force an otherwise rare negative or emergency case. Safe demo evidence or deterministic existing test fixtures are acceptable; otherwise retain `INCOMPLETE`.

# 6. Recommended post-P0 package analyzer expansion

When the v4.59/post-P0 tooling package is materialized, extend the analyzer with explicit case IDs from this document:

- `R3-00..R3-15`;
- `R4-00..R4-16`;
- `R5-00..R5-20`;
- `R6-00..R6-16`.

The analyzer should aggregate per-case status without weakening fail-closed identity rules. A stage may only be called PASS when all mandatory cases for that stage are positively demonstrated; optional/safety cases can remain `INCOMPLETE` only where the canonical closure rule explicitly permits it.

# 7. Execution handoff sequence

After P0 acceptance/integration and post-P0 tooling re-baseline:

1. run R1 D1TPW profile and close/incomplete/fail it honestly;
2. run R2 C044 profile and close/incomplete/fail it honestly;
3. return to BASELINE for R3–R6 unless a specific already-approved test profile is required to collect a lifecycle-related control;
4. run R3 owner/D1O matrix;
5. run R4 timing/M17 geometry;
6. run R5 TradeLock/risk/P3 controls;
7. run R6 N1/N2 forward outcome chain with N3 firewall checks;
8. create one dedicated closure audit per stage tied to exact source/EX4/bundle identities.

Do not merge to `main` merely to collect runtime evidence.

# 8. Preparation verdict

**R3–R6 CONSOLIDATED BROKER RUNTIME ACCEPTANCE MATRIX READY. EXECUTION REMAINS BLOCKED BY P0 #94 AND THE LOCKED PREDECESSOR ORDER.**

No EA source patch, lifecycle activation, N3 activation, canonical merge or strategy-semantic change is performed by this preparation record.
