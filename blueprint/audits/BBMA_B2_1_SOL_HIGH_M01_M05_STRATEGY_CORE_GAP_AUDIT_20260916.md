# B2.1 â€” Strategy-Core Gap Audit M01â€“M05

Date: 2026-09-16
Model route: Sol High
Status: AUDIT COMPLETE / VALIDATION PASS
Issue: #168
Predecessor: B1.4 CLOSED/PASS, commit `6a40a78e37a8dbf08bf63312f2bffb95cdcf3b2d`

## A. Scope and hard boundary

This task audits M01â€“M05 only, including material cross-module consumers of authority defined in those modules. B phase is classification-only: no EA, Core, contract, risk, execution or runtime mutation is authorized.

Live implementation authority at audit start: `d1-owner-dev@ea4c48262c4bb058e375fb9a1b564fa132ba578b`.
Canonical EA: `blueprint/source/BBMA_EA.mq4`, blob `6e629128f37c3fd482dd49e275360503f73fee68`, SHA-256 `3BE02985A6A3DF9E001FB441BEED3B8F8DA2755C2ECE2F78B43879C6E635311C`.
Accepted Core blob: `923483602d89d775576e8def988958aff8f5fe75`.

## B. Source Autonomy route

The audit followed live `SOURCE_INDEX.md` before interpreting code: accepted Core â†’ Finale master/episode evidence â†’ primary PDF â†’ secondary PDF â†’ conflict/gap registers â†’ decisions/contracts â†’ canonical EA.

Material evidence used for the lifetime question included primary `Oma ally BBMA - AL.pdf` page 10, secondary `BBMA technique.pdf` pages 35â€“36, Finale V05/V06 extracted evidence, M12 contract, and `P3_FINAL_DELTA_R1_LIFETIME_SOURCE_RESOLUTION.md`.

Zero-result source search was not treated as proof of absence. The existing R1 resolution supplies the decisive accepted project authority for fixed-age lifetime.
## C. Findings

### B21-01 â€” M01 NMJE inputs still authorize execution rejection
**Classification: CONFIRMED BUG / EXISTING OWNER Q1**

ISSUE â†’ M01 exposes `BlockNMJEConflict` and `BlockNMJEBuilding`; `NMJE_PassExecutionGate()` consumes them and rejects an otherwise validated Re-Entry with `REJ_NMJE_RELATION`.

IMPACT â†’ Active M12N/NMJE authority is read-only observation/context. The canonical v4.61 path therefore gives NMJE reject authority it does not own.

FIX â†’ No B2.1 patch. Existing Q1 / Issue #141 / Draft PR #142 owns the minimal removal of execution gating. Preserve N1/N2/N3 telemetry/context only unless a later explicit authority decision changes this.

### B21-02 â€” M01 fixed Type 2/3/4 Re-Entry lifetime remains executable
**Classification: CONFIRMED BUG**

ISSUE â†’ `MaxWaitBars_ReEntry = 5` is assigned to Type 2/3/4 candidate expiry and `IsReEntryIntrinsicExpired()` transitions candidate/confirmed state to EXPIRED by elapsed time.

IMPACT â†’ The accepted R1 lifetime resolution explicitly rejects generic `MaxWaitBars_ReEntry` expiry for Types 2/3/4. It requires structural owner/invalidation/supersession rather than an unrelated five-bar timer.

FIX â†’ No B2.1 patch. Later repair must remove fixed-age Strategy-Core validity for Type 2/3/4, preserve structural invalidation, and must not replace `5` with another tuned number.
### B21-03 â€” M01 Extreme age window still invalidates downstream component authority
**Classification: CONFIRMED BUG**

ISSUE â†’ `MaxWaitBars_Extreme = 5` remains exported into Extreme component metadata and M16 `IsExtremeStateExpired()` rejects the component after elapsed timeframe bars.

IMPACT â†’ R1 explicitly rejects generic fixed-age Extreme expiry and states that M16 must not add an independent age-based Strategy-Core death rule. M08 structural VOID/SUPERSEDED ownership is authoritative.

FIX â†’ No B2.1 patch. Audit/repair ownership crosses M01â†’M08â†’M16; later implementation must remove age as strategy invalidation while preserving structural provenance and fail-closed exact-owner verification.

### B21-04 â€” M02 decision lifecycle conflates validation, risk approval and entry-ready
**Classification: CONFIRMED BUG / ARCHITECTURE-LIFECYCLE**

ISSUE â†’ `ENUM_DECISION_STATE` has CREATED/VALIDATED/INVALIDATED/REJECTED/EXECUTED/EXPIRED only. After M15 selection and M16/M17 validation, M21 sizing, M19 risk approval and M20 portfolio admission all execute while the authoritative decision remains `DEC_VALIDATED`; success then proceeds directly to M22/`DEC_EXECUTED`.

IMPACT â†’ Live project governance defines separate pipeline stages `Combination/Selection â†’ Validation â†’ Risk Approval â†’ Execution`. The current state model cannot authoritatively distinguish a merely validated decision from a risk-approved/entry-ready decision, weakening lifecycle ownership, restart reasoning and telemetry attribution even though sequential guards currently fail closed on rejection.

FIX â†’ No B2.1 patch. Later architecture repair must materialize distinct authoritative approval/readiness state without letting risk create a signal or execution redefine Strategy Core.
### B21-05 â€” M03 pair/global state ownership
**Classification: NO FIX**

M03 keeps `PairState`, nested-journey context and processed-candle cursors in pair-indexed arrays. The audited M01â€“M05 state declarations do not expose a shared cross-symbol Strategy-Core owner that would merge pair lifecycle state. Consumer-edge coverage remains PARTIAL in the verified module graph, so absence of an undocumented dependency is not claimed.

### B21-06 â€” M04/M05 closed-candle and processing-clock boundary
**Classification: NO FIX**

`GetLatestClosedCandleTime()` starts at shift 1, `g_processing_time` is frozen once per scan, M27 admits strategy processing only on a new closed M15 candle, and `ProcessPair()` retrieves D1/H4/H1/M15 data by exact closed-candle time. No shift-0 Strategy-Core OHLC read was found in M01â€“M05.

This aligns with the active M27 contract: M15 closed-candle processing is the sole strategy clock. Tick-driven portfolio/position lifecycle remains downstream operational behavior, not a second Strategy-Core clock.

### B21-07 â€” M04 `IsNear()` two-point Type 2 collision tolerance
**Classification: NO FIX / ENGINEERING MAPPING ALREADY DISCLOSED**

M04 represents line collision as `< 2 broker points`. M12 contract explicitly labels `IsNear()` as the project numerical representation of MA/Mid-BB collision and states that the source gives no numeric tolerance. It is not an Oma Ally rule and remains a validation/backtest-able engineering mapping; no duplicate detector or new threshold is authorized here.
## D. Register and duplication review

Finale conflict/gap registers do not already own B21-02/B21-03/B21-04. CF-05/IG-08 remain the separate Re-Entry validation/next-candle timing verification and are not changed by this audit. CF-06/IG-07 remain close-side corroboration/verification.

GitHub issue search found no existing issue keyed to `MaxWaitBars_ReEntry`, `MaxWaitBars_Extreme`, fixed-age expiry or risk-approval state. B21-01 is already owned by Q1/#141/#142 and must not be duplicated.

Declaration-only sweep: MaxWaitBars_MLV, MaxWaitBars_CSD, MaxWaitBars_Combined, MaxWaitBars_Global, SignalMode and ScoreDisplayThresholdManual each have no executable consumer beyond their declaration in the canonical source; they are not promoted to runtime findings in B2.1.

## E. B2.1 result

Confirmed bugs: 4 (`B21-01` through `B21-04`).
No-fix/aligned findings: 3 (`B21-05` through `B21-07`).
Source conflict: 0.
New Strategy-Core rule: 0.
EA/Core/contract mutation: 0.

No compile/runtime claim is made because B2.1 is a read-only architecture/Strategy-Core audit. Existing branch-specific compile/runtime evidence retains its original scope.

## F. Validation evidence

- Live implementation owner re-read: `d1-owner-dev@ea4c48262c4bb058e375fb9a1b564fa132ba578b`; canonical EA blob remains `6e629128f37c3fd482dd49e275360503f73fee68`.
- B21-01: active M12N contract is N1 observation-only/read-only and explicitly forbids candidate rejection or execution authority; Draft PR #142 remains the existing scoped Q1 owner.
- B21-02/B21-03: `blueprint/P3_FINAL_DELTA_R1_LIFETIME_SOURCE_RESOLUTION.md` explicitly rejects generic fixed-age Extreme and Type 2/3/4 Re-Entry expiry and authorizes removal from active Strategy-Core validity.
- B21-04: `ENUM_DECISION_STATE` exposes only CREATED/VALIDATED/INVALIDATED/REJECTED/EXECUTED/EXPIRED. Live preflight keeps `DEC_VALIDATED` through M21 sizing, M19 risk acceptance and M20 portfolio acceptance, then calls M22. M22 contract explicitly requires M19/M20 approval state, confirming that the approval/readiness stage is not materialized as distinct authoritative decision state.
- B21-05: pair-owned Strategy-Core state is held in `g_pair_states[MAX_PAIRS]`, `g_nested_journeys[MAX_PAIRS]` and `g_processed_candle_time[MAX_PAIRS]`; no shared cross-symbol Strategy-Core owner was found in M01-M05.
- B21-06: `GetLatestClosedCandleTime()` begins at shift 1; M04-M05 scan found no direct shift-0 Strategy-Core OHLC read; `IsNewCandle()` gates `ProcessPair()` on the latest closed M15 candle.
- B21-07: `IsNear()` is line 1237 inside M04 and uses `< 2 broker points`; M12 contract explicitly labels it a project numerical representation because the PDF supplies no numeric collision tolerance.
- Conflict/gap register review found no existing owner for B21-02/B21-03/B21-04. CF-05/IG-08 and CF-06/IG-07 remain separate timing/close-side verification items.
- Exact GitHub issue searches for `MaxWaitBars_ReEntry`, `MaxWaitBars_Extreme`, and `DEC_VALIDATED` + risk returned no existing scoped issue. B21-01 remains deduplicated to Q1/#141/#142.
- No EA/Core/contract/runtime artifact was modified by this audit.

## G. Next safe action

1. Save this report as a report-only remote checkpoint.
2. Carry B21-02/B21-03/B21-04 forward to B3 genuine-mismatch confirmation and B5 prioritisation before opening implementation-owner work; do not duplicate Q1 for B21-01.
3. Continue roadmap B2.2 â€” audit M06â€“M10 â€” from the B2.1 VERIFIED checkpoint.
4. Do not implement any B2 findings until B3 confirms genuine Core/code mismatch and B5 prioritises confirmed gaps.
