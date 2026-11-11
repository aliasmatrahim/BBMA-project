# Signal-by-signal acceptance — 2026-11-10

User instruction: finish one signal before moving to the next; do no unrelated task. SIG-01 eCSD, SIG-02 CSA and SIG-03 CSAK/CSD have the bounded VERIFIED acceptances below. SIG-05 publication and branch were verified at d2e7e85c3f9fd0d2620361c175dbe0b71cea5fa7. SIG-06 MHV now has bounded canonical signal acceptance. SIG-07 MLV alias acceptance is verified. Current only Re-Entry Types 1–4. Shared historical production recovery remains HOLD. Shared-consumer regression is part of SIG-01, not development of another signal. Base328d33a0dd4824f4ff3dcb2a2b2823a69e12bc9b / Draft PR303 / feat/custom-mtf-v1-20261108.

## SIG-01 eCSD — VERIFIED (bounded canonical signal acceptance)

Spec: M10_DIRECTION_CLOSE_ONLY_USER_DECISION_20261110.md. BUY Close above MA5High and MA10High; SELL Close below MA5Low and MA10Low. Open is not read by this predicate. Relevant equality is rejected. Shift0/negative is rejected. M06 readiness still owns complete valid data, and raw direction is not execution authority.

Acceptance checklist:
- [x] Actual extracted baseline detector fails a valid Close-beyond-MAs case solely due Open (RED observed).
- [x] Small canonical eCSD patch and reusable close-pair helper; unique Build6.07 identity.
- [x] Nine protected CSD/MOM/owner/consumer function bodies unchanged. Caller signatures unchanged. No duplicate detector or M15 updater.
- [x] Cloud regression76/76 after change; runner/helper py_compile/diff checks.
- [x] Final native full EA/harness strict compile0 errors/0 warnings and190 checks PASS, including140 actual closed-history comparisons.
- [x] Final native eCSD harness: synthetic BUY/SELL/Open/equality/readiness cases, seven-TF140 actual closed-history comparisons, D1/M11/M12 consumer delegation/identity, no orders.
- [x] Affected source/native regression all pass and exact source/include/harness/binary hashes bound.
- [x] Actual M27/ProcessPair monitor OFF/ON parity bound to final source; intended old/new differences against frozen6.06 reviewed. Orders remain disabled/captured.
- [x] Evidence, branch/commit/checkpoint/Draft PR saved and verified before next signal.

This task does not add an eCSD input token to the approved11-signal custom grammar, alias the user's MidBB CSA to eCSD, activate custom admission, certify arbitrary history/session recovery or claim profitability.

The current helper migration is intentionally per signal: legacy CSD still uses its historical body-span code and will be addressed only in its own task. Thus Build6.07 is an intermediate signal migration, not full M10 Close-only acceptance or release-ready. Current same-candle precedence Momentum > CSD > eCSD remains in untouched consumers. Earlier same-signal observations can now qualify on more source candles; no new first-cross/colour/TTL filter is added, and later custom identity/admission gates remain OFF.

## Queue after SIG-01 acceptance

SIG-02 CSA (user MidBB direction) -> SIG-03 CSAK/CSD (MA pair+MidBB) -> MOM -> Extreme -> MHV -> MLV -> Re-Entry. MHV/MLV remain one canonical M09 engine with alias-specific acceptance, never duplicate detectors. Previously VERIFIED signal work is reused and only affected/unverified criteria are checked. Do not start a later signal if SIG-01 is PARTIAL/HOLD.

No unrelated queue task, merge, deployment or trading activation. All77 semantic availability cells/custom auto-entry OFF. Native/market-history scope limitations must be retained rather than promoted to universal seven-TF or execution acceptance.

Acceptance/source lineage, retained initial controller RED, final equal-state parity and limits: CUSTOM_MTF_ECSD_SIGNAL_ACCEPTANCE_20261110.md. Tested code commit3c14938b8e2c2ab79d47101e61a8d90362a94091; final publication SHA recorded in Draft PR303. SIG-02 not started before this publication.

## SIG-02 CSA — VERIFIED (bounded read-only source/context)

Build6.08, source LF SHA256 f317317f2ba7145990b66340aea6022a385e464e72da4e01be2d71f1c12e7e9c. Native154/154,140 actual closed-history comparisons,210 actual-controller CSA views,14 native regression groups and0E0W compile verified. OFF/ON/baseline6.07 full12,224-row traces identical over16 cycles; no orders. Five targeted cloud functions plus import assertions/py_compile PASS; full pytest not rerun. Final source/include/harness/binary/trace bindings verified. Initial147/7 test assertion failure retained and corrected using StringLen without production changes. Acceptance: CUSTOM_MTF_CSA_SIGNAL_ACCEPTANCE_20261110.md; evidence csa608_native_evidence.json. This closes source/context only, not executable availability, physical trigger dedup or integrated T04.

Next eligible after publication: SIG-03 CSAK/CSD. No later signal developed before SIG-02 closure. No merge/deployment; all77 availability/custom auto-entry OFF.

## SIG-03 CSAK/CSD — VERIFIED (bounded predicate/consumer/read-only context)

Build6.09 rev002, source LF SHA d74f41d0c85e8ec5e4afdd58728c4cfcaae5765adc128f4aefa849edbfb04c25. Canonical211/211, final context189/189, characterization141/141,17 native groups,0E0W. Actual-controller420 combined CSA/CSAK views,16 cycles/12224 scalar rows per case; OFF/ON exact parity. Frozen6.08 differs296 intended H4/M12 Type4 context rows and0 Decision rows; zero attempts.19 source/binary bindings and3 traces verified6212 exit0. Independent review found no material bug; explicit High-only revision test passed7TF. Six cloud test functions/import assertions/py_compile PASS; full pytest unavailable. Acceptance CUSTOM_MTF_CSAK_SIGNAL_ACCEPTANCE_20261110.md; next only SIG-04 MOM after final publication. All77/custom executable availability OFF; no merge/deployment. Historical paragraphs naming earlier active signals are retained chronology, not current scheduling authority.

## SIG-04 MOM — VERIFIED (bounded predicate/readiness/affected consumers)

Build6.10 rev003, LF SHA ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae. Native72 valid-data/1400 iBands comparisons and167 readiness/recovery/atomicity checks, all18 native groups, strict0E0W;20 bindings verified. Actual controller630 combined views,16 cycles/12224 scalar rows per case, OFF/ON/frozen6.09 exact parity, zero decisions/attempts. Confirmed partial-data false classification and unavailable-state propagation repaired; explicit REDs retained. Full evidence and limits: CUSTOM_MTF_MOM_SIGNAL_ACCEPTANCE_20261110.md. Next only SIG-05 Extreme after publication verification; no custom execution/merge/deployment promotion.

## SIG-05 Extreme — VERIFIED (bounded RAW/maturity/readiness/affected handover and projection)

Build6.11 rev003, source LF SHA a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb. Native141/716 and19 specialized groups, strict0E0W; frozen6.10 lifecycle716;23 bindings plus baseline harness verified12828 exit0. Actual controller180 non-executable EXT+630 M10 views,16 cycles/12224 rows per case; OFF/ON/frozen6.10 exact parity and zero attempts. Explicit M08 source8/14 and handover106/35 REDs retained. Accepted F2 RAW/reversal/retest and Open/body anchors unchanged; M10 is sole Momentum producer. Acceptance CUSTOM_MTF_EXTREME_SIGNAL_ACCEPTANCE_20261110.md. Next only SIG-06 MHV after publication verification. All77 availability/entry OFF; session/epoch/integrated execution gates unchanged.

## SIG-06 MHV — IN_PROGRESS / historical evidence HOLD

Accepted Core/F1 and current exact6.11 mechanics reviewed/reused. Fresh G40 check6256 exit0:4 provenance metadata files unchanged/reference-only; current controller first cycle has56 zero M08/M09 anchor fields, not authenticated NONE. Source-proven same-feed Extreme/TPW origin and session/UTC recovery evidence remain required before full MHV acceptance. No code change/new native PASS/alias activation. Current blockers and exact next action: CUSTOM_MTF_MHV_SIGNAL_PREFLIGHT_20261110.md. Do not advance to SIG-07 MLV or Re-Entry.


### SIG06 milestone — 2026-11-11 (still PARTIAL)

Natural-history diagnostic4200 bars/57 candidates/23 four-hypothesis convergences. Strong reset/origin witness plus physical isolated terminal restart passes M1/M5/M15/H1:136 checks,96 post-reload bars/102 fields perstate,8 processes,0E0W; all source/HST/snapshot hashes bound4500 exit0. First inadequate M15 candidate retained as RED, no criterion weakened. This is not global source-epoch/session acceptance. M30/H4/D1 remain HOLD; no MLV/Re-Entry. Details CUSTOM_MTF_MHV_NATURAL_ORIGIN_RESTART_20261111.md; mhv611_natural_origin_restart_summary.json.


2026-11-11 SIG06 fixture/profile milestone: M30 alternate complete-M15-pair fixture34/34 plus H4/D1 synthetic-NY-calendar72/72 now pass; prior4TF136 reused, combined242 restart assertions/168 reloaded source bars/102 fields.200 separate native MA adapter comparisons. Collector3712 exit0; all source-HST hashes/production EA unchanged. Exact4TF synthetic-v3 SHA and M1/M5 exact suffix+header binding correct prior unknown-server attribution. Approved isolated reference only, not broker-session authority. Independent review confirms direct source-engine tests do NOT certify production replay admission. Full SIG06/T04B/E historical session/owner-epoch acceptance remains HOLD; no MLV/Re-Entry or availability promotion. Report CUSTOM_MTF_MHV_FIXTURE_PROFILE_MILESTONE_20261111.md; exact next: accepted same-feed boundary + source-proven epoch, then full production-admission continuous/recovered comparison. Retain original exits.


2026-11-11 SIG06 actual production admission milestone:340/340 native checks,24 cases over6 existing H4/D1 boundaries, zero/two-bar prefixes and initially-held/previously-unheld owners. Direct replay and actual requested-owner router/canonical storage preserve full structural/data state, activate/retain recovery HOLD and block both MHV views. Strict harness0E0W, terminal6904/driver8456 exit0. Initial148/12 fixture RED retained: historical target violated latest-only router contract; v2 uses actual latest target, no production change. Existing242 successful bounded restart checks are separate; this milestone does not certify successful gap recovery. Independent diagnostic review no material issue. Report CUSTOM_MTF_MHV_PRODUCTION_ADMISSION_20261111.md. Original same-feed production boundary/owner-epoch and successful recovery exits remain HOLD; SIG06 PARTIAL, no MLV/Re-Entry or other task/activation.


2026-11-11 SIG06 availability propagation bounded VERIFIED on Build6.13 source43470ff9795b18e44844bb815deceee778072a004b8815666e18e8ffa584d15c. Native caller RED197/98 → GREEN295/295;112 inner-status cases785/785; candidate323/323 preserved. All14 groups PASS5100 exit0; initial momready166/1 fixture scope defect corrected and retry PASS, no source change. Ordinary+seeded controller OFF/ON/frozen6.12 12224 rows/16 cycles per case exact parity, zero attempts. Collector6584 exit0,14 binaries/unchanged HST verified; evidence archive dabc0aa4f454ec8ee1bdfdc48841fd639340a0672a899821200daf14d0ff88aa. FullSIG06 stillPARTIAL: G40 deployment broker profile UNRESOLVED and original session/owner-epoch/successful production gap recovery gates remain. No MLV/Re-Entry or execution promotion. See mhv613_checkpoint.json and CUSTOM_MTF_MHV_AVAILABILITY_PROPAGATION_20261111.md.


## SIG-06 MHV — VERIFIED for the canonical signal and read-only projection

Build 6.13 at `15a96f6b1ba9b72154dbcf0e8a50c1e1db379d90`, source LF SHA `43470ff9795b18e44844bb815deceee778072a004b8815666e18e8ffa584d15c`. The bounded serial acceptance covers source-valid Extreme/TP Wajib lineage, formation/invalidation/supersession, both owner directions, read-only projection and exact closed-bar readiness/retry. Existing native manifests were independently read back from the published archive: 51 logical files, 47 unique hash-verified objects; structural 238/238, producer 52/52, anchored replay 57/57, canonical 47/47, observer 4/4, pre-freeze 61/61, caller 295/295, inner status 785/785 and candidate 323/323. Ordinary and seeded traces each have 12,224 identical OFF/ON/frozen rows and zero order attempts. The earlier seven-TF reference restart and negative production gap-admission proofs retain their original exact-build and fixture bounds.

This supersedes the serial scheduling restriction in the earlier SIG-06 entries. The signal audit had included the shared T04-B/E deployment recovery gate. The approved plan permits eligible independent work while T04-B is HOLD. The full T04-B/E historical session and owner-epoch acceptance retains all three exits: authenticated same-feed boundary, source-proven historical owner epoch and successful production continuous/recovered parity across that boundary. G40 broker/server/UTC/DST/week rules remain unresolved. The current replay correctly rejects non-nominal spacing; future admission needs a verified source policy and end-to-end evidence. T04-F/T05+ stay gated, and no executable availability, deployment or orders are authorized.

Next serial signal is SIG-07 MLV read-only alias acceptance. Reuse the shared M09 mechanics. Re-Entry follows MLV acceptance.


## SIG-07 MLV — VERIFIED for the read-only alias

Build 6.13. Core V2 §6, Finale V05 and the F1 decision resolve MHV/MLV as names for the same M09 setup. Both names route through the same symbol/timeframe/direction owner, current closed-candle and recovery checks and `ProjectCustomMHVView`. They share one event identity. The projection disables entry window, entry eligibility and execution availability. M09 lifecycle and BUY/SELL coverage are reused from SIG-06.

Independent readback of the published Build 6.13 evidence verified all seven producer alias identity rows (M1/M5/M15/M30/H1/H4/D1) plus all three canonical higher-timeframe rows (H1/H4/D1). The published projection header SHA `2cbb1a1c062053e2162037e58096aec194e36409dcb911865eed6dd1fba1a38e` matches both manifests. The accepted native cases use the previously declared trusted owner/history fixtures. The existing moving-bar monitor run is 12/12 with zero orders. No executable MLV availability or production session recovery is inferred. No EA code change or new native run.

Next serial signal: Re-Entry Types 1–4. T04-B/E historical production recovery remains HOLD.


## Re-Entry Types 1–4 — IN PROGRESS

Core V2 §8 and current M12/standalone paths reviewed. Confirmed canonical H1 late-admission gap on Build 6.13; complete builder body matches owner 5.15, while the existing gate and targeted evidence are on unmerged Draft PR #301 Build 5.16. See `CUSTOM_MTF_REENTRY_SIGNAL_PREFLIGHT_20261111.md`. Re-Entry is the only active serial audit.

Re-Entry EntryCandle milestone: exact Build 6.13 native reproduction 34 PASS/24 FAIL → isolated 6.14 58/58, both sides and Types 1–4, strict EA/harness 0E0W and zero orders. Timing admission verified on seeded owners only. Exact-build market-driven lifecycle/controller and order timing remain pending. See `reentry614_entrycandle_probe.json`.

Actual isolated GBPUSD August 2026 M15 controller replay completed: Build 6.13 emits 16 late candidate admission rows for one Type 3 confirmation; isolated 6.14 emits zero. The 1,296 RE_EVAL rows are identical. Both runs have zero orders; no timely H4-aligned window and no market Type 2 confirmation were observed. Re-Entry remains IN PROGRESS. See `reentry614_market_replay.json`.

Re-Entry Build 6.14 positive market timing verified in G40 Strategy Tester. EURUSD August 2026: 8 orders; USDJPY August 2026: 6 orders. All 14 have one matching admission, M15 selection, M16 pass, tester open event and OrderOpenTime in the next actual H1 source candle; 2 Type 1, 4 Type 3, 8 Type 4. No late admissions or orders over the five extension profiles. Type 2 formation remains the only open signal-evidence item. See `reentry614_positive_order_trace.json`.
