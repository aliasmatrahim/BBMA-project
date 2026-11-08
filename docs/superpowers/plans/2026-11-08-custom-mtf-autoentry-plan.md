# BBMA Custom MTF Auto-Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for inline execution, or superpowers:subagent-driven-development only after the user selects delegation. Implement task-by-task with the verification gates below.

**Goal:** Melaksanakan reka bentuk v1 yang diluluskan pengguna pada 8 November 2026: signal tujuh TF, lima slot custom, tujuh komponen, AND/OR, auto-entry, tiga exit profile, per-slot sizing/symbols, hedging dan label.

**Architecture:** Peluaskan owners M01–M27 sedia ada; M15 kekal final authority. Canonical cadence/signatures dipelihara; CUSTOM menerima closed-bar trigger events melalui orchestrator tunggal. M12N kekal read-only.

**Tech Stack:** MT4, MQL4 strict, MetaEditor native compile, Python validation tools sedia ada dan GitHub scoped PR workflow. Tiada framework trading baharu.

**Spec:** [Approved Design v1](https://chatgpt.com/library?file_id=libfile_0f6f7b676384819198c7e68a3424ed56&account_id=personal). Filename `BBMA_Custom_MTF_Design_Draft_v1_2026-11-07.md`; kandungan v1 diluluskan dalam chat, walaupun header asal masih DRAFT. Laluan repo yang dicadangkan: `docs/superpowers/specs/2026-11-07-custom-mtf-autoentry-design.md`.

**Status:** PLAN FOR REVIEW; kod EA belum diubah. Approval design membenarkan penyediaan pelan ini; bukan bukti compile/runtime, merge atau activation. Semua task PENDING.

## Global Constraints

- Tujuh TF tepat: M1, M5, M15, M30, H1, H4, D1; lima slot; maksimum tujuh kemunculan atom aktif bagi satu slot.
- Formula `(Context) AND (Trigger)`; satu tahap kumpulan OR; tiada NOT atau arbitrary nesting; kedua-dua field wajib tidak kosong.
- D1 strategic gate kekal; hedging tidak memintasnya. Tiada semantik BBMA dicipta daripada engineering syntax.
- Canonical detector/lifecycle kekal satu owner; risk tidak mencipta signal; M22 tidak menafsir formula.
- Tiada generic TTL structural M12; eligibility entry berasingan daripada structural validity.
- Fixed lot invalid ditolak; risk lot floor ke lot step; tidak clamp min/max untuk memaksa entry.
- Fail-closed bagi identity, source, configuration atau broker state tidak sah; protective management posisi owned diteruskan.
- Tiada real-money activation, restart primary MT4, overwrite canonical files, merge atau force update diandaikan daripada approval design.

## Review Focus

1. D1/H4 dan M1 menutup pada timestamp sama: refresh tinggi→rendah sebelum satu immutable decision batch (T04/T06).
2. Formula mengandungi OR yang benar tetapi SL source berada dalam branch gagal: jangan pinjam source tersebut (T05/T08).
3. Timeout selepas order diterima broker: reservation kekal dan reconcile sebelum retry, termasuk selepas restart (T07/T10).
4. Pasangan simbol alias bertembung, CFD tick size berbeza Point, dan slot baru menggunakan event lama: tiada salah simbol/saiz/duplicate (T03/T07/T09).
5. Pengguna menukar input atau membuang simbol ketika posisi masih terbuka: frozen TradePlan dan ownership kekal (T10/T11).

## 1. Baseline dan status evidence

Pembacaan GitHub semasa menyediakan pelan mengembalikan owner `d1-owner-dev` head `459c0588e625d7f7630f0fb5612b7f04fda496de`, mesej merge PR #280. Source yang diperiksa pada sesi design mempunyai header 5.1.5. CURRENT/queue bertarikh September dan CURRENT menyebut 5.14; `EA_RELEASE_IDENTITY.json` pada head itu masih display 4.5.9/property 4.59. Ini menunjukkan **rekod lineage berbeza**, bukan kesimpulan bahawa file patut ditulis semula atau build terkini sudah ditemui.

T01 wajib menyemak active PR/branch/worktree/runtime dan resolve authoritative target. Jangan transplant kod terhadap snapshot September jika G40/PR lebih baharu terbukti current. Baseline hash pelan ialah observed input, bukan frozen implementation candidate. Tiada data/compile/runtime baharu dijalankan bagi pelan ini.

README meroute implementation ke `d1-owner-dev`, governance/tooling/Actions ke `main`; SOURCE_INDEX semasa termasuk workbook dan supplemental reconciliation. Gunakan retrieval chain itu bagi setiap mapping materially relevant. Jangan menerima definisi CSA/CSAK lama daripada nama enum semata-mata.

## 2. Fail dan pembahagian tanggungjawab

| File/path | Tindakan dan peranan |
| --- | --- |
| `blueprint/source/BBMA_EA.mq4` | Modify owner functions/structs mengikut task; kekalkan monolithic style, tiada refactor besar tanpa keperluan. |
| `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md` | Add scoped custom collector boundary tanpa mengubah signature rasmi. |
| `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md` | Add CUSTOM event cadence; canonical closed-M15 path kekal. |
| `blueprint/contracts/M17_ENTRY_SLTP_CONTRACT.md`, `M17_SLTP_EXIT_RESOLUTION_CONTRACT.md` | Reconcile active resolver sebelum scoped addendum untuk tiga custom profiles. |
| `blueprint/contracts/M21_MONEY_MANAGEMENT_CONTRACT.md` | Per-slot configuration menggunakan frozen sizing yang sama. |
| `blueprint/decisions/CUSTOM_MTF_V1_ARCHITECTURE_DECISION.md` | Create approval scope, clock, source and migration decision. |
| `blueprint/contracts/CUSTOM_MTF_V1_INTERFACE_CONTRACT.md` | Create schema/interface contract; tidak menggantikan module owners. |
| `blueprint/audits/CUSTOM_MTF_V1_BASELINE.md` | Create exact target/source/compile/runtime reconciliation. |
| `blueprint/tests/custom_mtf/` | Create targeted native harnesses, Python trace analyzer dan fixtures bagi authority baharu. Reuse equivalent existing tests jika dijumpai T01. |
| `blueprint/runtime/custom_mtf/` | Create acceptance matrix/manifest/presets selepas native command owner disahkan. |
| `docs/superpowers/plans/2026-11-08-custom-mtf-autoentry-plan.md` | Copy plan ke scoped branch ketika execution; bukan ditulis ke GitHub dalam sesi planning ini. |

Release metadata diubah hanya jika target identity owner disahkan T01; jangan promote shadow build kepada release. Setiap MQ4 change perlu build/patch identifier unik; Header Version left-aligned selepas `//|`.

## 3. Interface bersama yang dicadangkan

Nama baharu berikut ialah contract cadangan. T01 menyemak collision/helper equivalents dahulu; gunakan adapter kepada struct existing, bukan kedua-dua representation bebas. Jika rename diperlukan, ubah interface contract/callers/plan secara atomic.

| Type | Kandungan wajib |
| --- | --- |
| `CustomSlotConfig` | slot_id 1–5, enabled, name, symbols, context/trigger text+parsed groups, direction, priority, exit/sizing/limits. |
| `CustomFormula` | groups AND; alternatives OR bagi setiap group; resolved atom IDs; total atoms. |
| `CustomOwnerView` | immutable owner-produced symbol/TF/type/direction/lifecycle/event ID, maturity, structural validity, entry eligibility, closed bar time. |
| `CustomEventBatch` | symbol, closed-event watermark, observed time, owner views, new event IDs; bukan wall-clock-only identity. |
| `CustomWitness` | concrete components yang memenuhi formula, actual RE type, fresh anchor, all simultaneous eligible anchors. |
| `CustomCandidate` | slot/config revision, witness, D1 snapshot dan compatibility metadata untuk M15/M16. |
| `CustomTradePlan` | selected source identities, direction, entry/SL/TP, exit/lifecycle policy, frozen sizing inputs, initial R, slot attribution. |
| `CustomTriggerReservation` | physical anchor IDs, decision ID, state RESERVED/AMBIGUOUS/CONSUMED, broker reconciliation identity. |

Structs tidak memberi authority sendiri. Existing decision/risk snapshot/owned-order registry kekal authoritative downstream.

## 4. Dependency dan checkpoint

Urutan utama: **T01 → T02 → T03 → T04 → T05 → T06 → T07 → T08 → T09 → T10 → T11 → T12**. Owner/registry work dan state scheduling perlu siap sebelum execution. UI tidak menjadi dependency kepada correctness auto-entry, tetapi wajib siap sebelum release scope penuh.

Setiap task guna checkbox: evidence FAIL dahulu bagi expected missing behavior → minimal change → PASS dengan output sebenar → native compile jika MQ4 berubah → targeted regression → checkpoint commit. Satu task boleh mempunyai beberapa commits semasa iterasi; jangan label COMPLETE jika exit criteria belum lulus.

Checkpoint fields: task ID, issue/PR, owner/base SHA, branch/head SHA, source SHA/build ID, commands+exit codes, artifacts/hashes, verification level, remaining work, exact next action. Save selepas boundary mahal/berisiko; reuse evidence yang identity-nya masih sepadan.

## T01 — Pulihkan baseline dan rekod keputusan approved

**Files:** audit baseline, scoped architecture decision, copied approved spec/plan; baca README, CURRENT, MASTER_QUEUE, SOURCE_INDEX, relevant contracts, current source dan runtime manifests.

**Interfaces:** consumes live GitHub/G40 identities; produces frozen `baseline.json` metadata dalam `blueprint/runtime/custom_mtf/baseline.json` dengan branch, commit, MQ4/EX4/config hashes, actual compile command dan limitations.

- [ ] Resolve owner branch dari README, enumerate active PRs/branches dan inspect G40 worktree/processes read-only; jangan hentikan primary terminal.
- [ ] Bandingkan source header/build tag, release manifest, CURRENT/queue dan exact compile/runtime artifacts; classify perbezaan historical/shadow/current tanpa membuat pembetulan release automatik.
- [ ] Ikut SOURCE_INDEX dan retrieve accepted Core/evidence bagi registry. Susun coverage signal × TF × context/trigger; setiap row ada supported/verification-required/HOLD dengan owner dan evidence path.
- [ ] Semak tree/helper/test names untuk mengelakkan duplicate canonical parser/state/scheduler. Create isolated scoped worktree/branch daripada owner yang disahkan, bukan main.
- [ ] Simpan approved design+decision dalam scoped branch/Draft PR; jangan overwrite locked contracts terus. Daftarkan exact verification commands daripada native registry/workflow; commands yang belum terbukti ditanda unavailable, bukan direka.
- [ ] Commit checkpoint baseline. **Exit:** correct implementation target dan selected native commands disahkan; setiap missing runtime ditandakan NOT VERIFIED. Konflik target semantik yang tidak boleh resolved ialah gate sebelum T04 source edits.

## T02 — Registry, schema dan parser lima slot

**Files:** MQ4 input/struct/init sections, interface contract, `blueprint/tests/custom_mtf/CustomFormulaHarness.mq4`, `blueprint/tests/custom_mtf/formula_cases.json`.

**Interfaces:** `bool ParseCustomFormula(string text, CustomFormula &out, string &reason)`; `bool ValidateCustomSlot(CustomSlotConfig &slot, string &reason)`; registry consumes T01 coverage. Native `RunCustomFormulaCase` harness invokes production parser, bukan Python replacement.

- [ ] Add cases: five slots; Context two atoms + Trigger five atoms = accepted; 2+6 = rejected; nested OR/NOT/unknown TF rejected; OR top-level Trigger accepted; OR groups within AND accepted; whitespace/case normalized; exact duplicate in field rejected.
- [ ] Run native harness using T01 registered command; record expected missing parser FAIL. Jangan guna syntax error sebagai bukti behavioral red.
- [ ] Implement parser into explicit groups/alternatives, alias registry status checks dan stable config hash. Tidak ubah definisi signal.
- [ ] Wire ON/OFF TF/signal × TF matrix, protected dependency handling dan init validation. Slot OFF empty accepted; enabled invalid slot rejects init; disabled reference tidak dipadam daripada formula.
- [ ] Native parser cases PASS; strict compile 0E/0W jika policy memerlukannya; regression init lama. Commit.

## T03 — Universe simbol dan per-slot subset

**Files:** MQ4 existing symbol resolver/init/pair state, `blueprint/tests/custom_mtf/CustomSymbolHarness.mq4`, symbol fixtures dalam `formula_cases.json` atau fixture khusus jika saiz meningkat.

**Interfaces:** `bool ResolveCustomUniverse(string &reason)`; `bool CustomSlotUsesSymbol(int slotIndex, string actualSymbol)`; delegates suffix resolution kepada canonical resolver.

- [ ] Add red cases: ALL tepat universe utama, subset typo rejected, suffix unique accepted, ambiguous two matches rejected, alias duplicate collapses kepada satu actual symbol, MARKET_WATCH changes after init ignored until reinit.
- [ ] Implement CHART_ONLY/MARKET_WATCH/CUSTOM_LIST; freeze resolved universe; jangan guna fixed pair-ID mapping untuk simbol arbitrary tanpa extension collision audit.
- [ ] Ensure slot formula/sizing dikongsi merentas symbols tetapi detector/lifecycle state isolated.
- [ ] Native harness PASS; reload retaining owned positions test pin ke T10; compile dan commit. **Exit:** tiada arbitrary broker symbol dipilih atau scan duplicate.

## T04 — Closed-bar scheduler dan peluasan canonical owners

**Files:** MQ4 M06/M07/M08/M09/M10/M11/M12/M27 sections; M15 clock addendum; `blueprint/tests/custom_mtf/CustomClockHarness.mq4`, `blueprint/tests/custom_mtf/clock_expected.json`.

**Interfaces:** `bool BuildCustomEventBatch(int pairIndex, CustomEventBatch &batch, string &reason)`; `void UpdateCustomOwners(const CustomEventBatch &batch)`; outputs `CustomOwnerView` for T05. Existing owners remain source of view.

- [ ] Pin cases all seven TF, M1 at 10:06 without waiting 10:15, missing quote, history warm-up, duplicate timer/tick, simultaneous D1/H4/M1 close, weekend/reconnect.
- [ ] Extend owner state per symbol/TF using accepted T01 mapping; no M12N substitute detector. Unresolved row returns unavailable, never Valid=true.
- [ ] Add event batching tinggi→rendah, exact bar identity watermarks, reentrancy guard; timer cannot manufacture close. Preserve canonical M15 cadence.
- [ ] Keep structural validity/entry window distinct and source-owned. Add red-to-green case confirming RE remains structurally valid after entry window expires without entry eligibility.
- [ ] Trace native harness PASS; label each unvalidated TF/signal explicitly; compile/cross-module check/commit. **Exit:** owner calls once per event and no live-candle decision.

## T05 — Context/Trigger evaluator dan OR witness

**Files:** MQ4 M13/M14 custom adapter, collector contract addendum; `blueprint/tests/custom_mtf/CustomWitnessHarness.mq4`.

**Interfaces:** `bool EvaluateCustomSlot(const CustomSlotConfig &slot, const CustomEventBatch &batch, int direction, CustomWitness &witness, string &reason)`; consumes T02 formula/T04 views, outputs concrete satisfying components and fresh anchors.

- [ ] Red cases: stale context rejected; opposite direction cannot satisfy AND; OR selected branch only; trigger AND A+B accepted, A historical alone rejected; RE wildcard resolves concrete type; unsupported MHV/CSA alias cannot pass.
- [ ] Implement boolean evaluation without detector calls, ranking BBMA quality, hidden TTL or arbitrary component chronology.
- [ ] Multiple satisfying OR alternatives canonicalized by concrete owner IDs; preserve all simultaneous eligible fresh anchors for reservation. Fixed SLSource missing in a witness makes that witness unusable; do not borrow branch components.
- [ ] Native witness assertions PASS, including unmatched TP source; compile and commit. **Exit:** reproducible witness and no semantic mutation in combination engine.

## T06 — M15 final authority dan canonical/custom arbitration

**Files:** MQ4 M15/M16/M27, M15 contract; `blueprint/tests/custom_mtf/CustomAuthorityHarness.mq4`.

**Interfaces:** `bool CollectCustomCandidates(const CustomEventBatch &batch, CustomCandidate &items[])`; adapter to current M15 decision type; `bool RevalidateCustomCandidate(const CustomCandidate &candidate, string &reason)` inside M16 ownership.

- [ ] Cases engine CANONICAL/CUSTOM/BOTH; D1 confirmed same-side allows custom, unresolved/transition/opposite rejects; BOTH cannot execute two independent pipelines.
- [ ] Collect first, select once per symbol/batch; custom slot priority ascending then slot ID engineering tie-break; contradictory custom directions block batch. Canonical authority unchanged for historical config.
- [ ] Freeze D1/witness/config identity in decision and revalidate exact owners before downstream geometry.
- [ ] Compare selected canonical decisions against frozen reference using existing specialized regression; custom authority native cases PASS. Commit. **Exit:** detector/raw formula never becomes direct execution authority.

## T07 — Physical trigger reservation, dedup dan retry boundary

**Files:** MQ4 existing execution identity/persistence owners M15/M22/M24; `blueprint/tests/custom_mtf/CustomDedupHarness.mq4`.

**Interfaces:** `bool ReserveCustomTriggers(const CustomWitness &witness, string decisionId, CustomTriggerReservation &reservation, string &reason)`; `void ReconcileCustomReservation(string decisionId)` delegates broker reconciliation to M22; durable consume only on confirmed execution.

- [ ] Add exact cases: OR M1/M5 same batch one send; new M5 five minutes later eligible; duplicate slot/config rename not fresh; AND A+B then still-eligible A+C accepted only C new; A alone after restart rejected.
- [ ] Reserve all simultaneous eligible anchors of fulfilled formulas before send; pending send ambiguity locks anchors/risk reservation. Journal failure before reservation disallows send.
- [ ] Retry only after definitive no-fill reconciliation within original owner entry window; retain physical event ID across retry. Timeout/fill case must produce one broker ticket after restart.
- [ ] Native/model fault cases PASS with order-count assertions; compile/commit. **Exit:** at-most-one execution per physical reserved trigger set; no permanent consumption of parent context.

## T08 — Tiga exit profiles dan frozen TradePlan

**Files:** MQ4 M17 resolver sections, both active M17 contract addenda; `blueprint/tests/custom_mtf/CustomExitHarness.mq4`.

**Interfaces:** `bool ResolveCustomTradePlan(const CustomCandidate &candidate, CustomTradePlan &plan, string &reason)` under M17; produces approved Entry/SL/TP plus exact source IDs, exit policy and initial R for T09/T10.

- [ ] Native red cases BUY/SELL for three modes; structural source outside witness rejected; unavailable TP mapping rejected; tick size ≠ Point; wrong-side/stale destination rejected; no silent fallback.
- [ ] Implement BBMA_STRUCTURAL via current approved mapping; RR via final normalized structural SL; FIXED_DISTANCE via explicit POINTS/PRICE and direction-aware normalization. No pip heuristic for gold/CFD.
- [ ] Capture complete profile, initial R, lifecycle opt-ins and source provenance; code labels RR/fixed as management engineering, not founder rule.
- [ ] Run geometry/source native assertions; M17 canonical regression PASS; compile/commit. **Exit:** exact source remains traceable through actual decision and broker preflight.

## T09 — Per-slot sizing, gross exposure, caps dan hedging

**Files:** MQ4 M19/M20/M21/owned registry, M21 contract addendum; `blueprint/tests/custom_mtf/CustomRiskHarness.mq4`.

**Interfaces:** existing M21 calculation consumes CustomTradePlan through canonical frozen snapshot; `bool ValidateCustomExposure(const CustomTradePlan &plan, double lots, string &reason)` delegates M19/M20. No independent risk calculator in parser/UI.

- [ ] Cases risk percent per trade not per slot; round down; invalid fixed lot not normalized; min/max invalid rejects; frozen equity/spec stable; quote reference changes force owner preflight, not M21 SL edit.
- [ ] Add slot/symbol/portfolio counts including in-flight reservations; broker margin check account-wide; unknown owned risk HOLD. Gross BUY+SELL stop risk summed, not netted.
- [ ] Hedging OFF opposite owned position blocked; ON supported account+fresh event+caps required; M11 gate retained. Same-batch conflicting directions still blocked.
- [ ] Native risk cases and canonical M19/M21 regression PASS; compile/commit. **Exit:** no race consumes portfolio budget twice.

## T10 — Recovery, lifecycle, BE/trailing dan controlled execution

**Files:** MQ4 M22/M23/M24 persistence/lifecycle owners; `blueprint/tests/custom_mtf/CustomRecoveryHarness.mq4`; runtime fault matrix.

**Interfaces:** `bool RecoverCustomState(string &reason)` uses generation-atomic existing persistence; `void ManageCustomTradePlan(int ticket)` inside current lifecycle owner. Exact-owned TradePlan survives input/config changes.

- [ ] Inject restart before reserve/after reserve/after send-before-ticket/after consume; assert recovery sends no historical catch-up trigger and never loses known-owned management.
- [ ] Persist config revision, consumed events, frozen trade plan, source/initial R, reservation and schema/build identity. Corrupt/missing ownership blocks new exposure rather than guesses.
- [ ] BE/trailing default OFF; when enabled explicit initial-R trigger, offset/step, emergency→enabled lifecycle exit→BE→trailing, no SL loosening. Profiles do not silently inherit unrelated canonical closes.
- [ ] Remove symbol/change formula during open trade; assert original plan remains managed and chart toggle has no effect. Existing ambiguity/HOLD reconciles before further exposure.
- [ ] Compile, native fault/lifecycle cases PASS, isolated tester order trace PASS; checkpoint. **Exit:** auto-entry pipeline connected but deployment order switch remains OFF until acceptance settings authorized.

## T11 — Labels, Setup Monitor dan attribution

**Files:** MQ4 M25/M26 display sections, `blueprint/tests/custom_mtf/CustomDisplayHarness.mq4`, analyzer fixtures.

**Interfaces:** `void RenderCustomSnapshot()` consumes read-only decisions/owner snapshots, never calls EvaluateCustomSlot to manufacture eligibility. Reuse existing snapshot builder.

- [ ] Confirm labels include actual source TF/direction/status and formation/confirmation times; no backdated confirmed arrow. Chart symbol labels only; other symbols table.
- [ ] Filters chart TF/selected TF/signal/direction, object lookback/cap and namespace cleanup; removing EA must not delete unrelated chart objects.
- [ ] Monitor shows WAIT_DATA/CONTEXT/TRIGGER/READY/BLOCKED_RISK/BLOCKED_LIMIT/CONFLICT/EXECUTED/INVALID_CONFIG and reason. Primary attribution counted once; other matched slots not credited duplicate P&L.
- [ ] Compare order trace with labels ON versus OFF identical; config removal retains open-position management. Native/harness + visual tester proof PASS; commit.

## T12 — Integrated acceptance, documentation dan handoff

**Files:** `blueprint/tests/custom_mtf/verify_custom_mtf_trace.py`, `blueprint/runtime/custom_mtf/acceptance_matrix.json`, existing specialized regression map/traceability records where owner approves, user input reference, final evidence manifest.

**Interfaces:** analyzer CLI `python blueprint/tests/custom_mtf/verify_custom_mtf_trace.py --manifest MANIFEST --output SUMMARY`; exit 0 only when expected identity/timing/state/order assertions hold. Implement CLI when task begins; command is planned, not available/passed today.

- [ ] Write analyzer negative fixtures with duplicate send, unmatched witness, wrong build/config, look-ahead and missing required cases; all return nonzero. Golden valid fixture returns zero with counts and limitations.
- [ ] Register selected task-to-module regression scope using canonical selection tooling on main; don't create parallel CI authority. Retrieve exact native compiler/tester commands pinned T01; record full output and unique MQ4/EX4/config hashes.
- [ ] Run strict static/cross-module/native compile, targeted regression and Strategy Tester on approved existing dataset. Define symbol/month/data/cost identity before run. Reuse verified baseline outputs only if hashes and scope match.
- [ ] Run multi-symbol isolated demo acceptance with order switch/settings explicitly authorized; single-symbol MT4 tester/harness evidence alone cannot prove multi-symbol broker execution. G40 unavailable means NOT RUNTIME VERIFIED, not synthetic PASS.
- [ ] Demonstrate all R01–R11 rows below satisfied; list HOLD/unavailable registry cells openly. Full scope completion requires supported signal×TF target covered; partial registry is milestone only.
- [ ] Independent architecture/regression review before merge/release, resolve findings; source contract/release history updates reflect actual evidence. Do not mark release-ready without native/runtime results. No merge or activation without applicable explicit authorization.

## 5. Verification commands and scope honesty

At planning time, native command registry/G40 availability is **not yet reconciled**. T01 must bind exact observed compile and tester commands plus profile path; later tasks execute those recorded commands, not a guessed generic `MetaEditor` invocation. If the command cannot be resolved, engineering/task work may continue safely in monitor mode but native/runtime exit criteria remain BLOCKED.

README main documents regression selection:

```text
py -m tools.bbma_orchestrator select-tests --map config/bbma_regression_map.json --module-graph config/bbma_module_graph.json --traceability config/bbma_traceability.json --module M06
```

This selects eligible tests only; it is not a global PASS command or native compile. Extend selection per changed module as the current CLI supports. Native harness filenames above are **new planned files**; their actual compile/run commands are resolved against the existing native runner T01 and recorded in the task checkpoint.

## 6. Coverage dan delivery gates

| Requirement | Tasks | Acceptance |
| --- | --- | --- |
| R01 tujuh TF/signal switches | T01/T02/T04/T12 | Owner semantics+supported TF coverage; OFF/reference behavior clear. |
| R02 lima slot/tujuh atom | T02/T05 | Bounds and independent slot config tested. |
| R03/R04 format/AND/OR | T02/T05/T07 | Parser+witness+physical event dedup native proof. |
| R05 auto-entry | T04/T06/T07/T10/T12 | Closed event→approved decision→exact broker order trace. |
| R06 tiga exits | T08/T10 | Source mapping, RR/distance geometry, frozen lifecycle. |
| R07 sizing | T09 | Frozen risk input and invalid lot fail-closed. |
| R08 caps | T09/T10 | In-flight+owned exposure per slot/symbol/portfolio. |
| R09 hedging | T06/T09 | Broker support, gross risk, D1/conflict policy retained. |
| R10 symbols | T03/T04/T10/T12 | Suffix/universe/state isolation and multi-symbol runtime. |
| R11 labels | T11 | Read-only display/order parity. |

Milestone A: T01–T04 registry/config/data ready in monitor mode. Milestone B: T05–T07 deterministic setup/authority/dedup shadow verified. Milestone C: T08–T10 trade management/auto-entry pipeline tested. Milestone D: T11–T12 full integrated acceptance. Setiap milestone bukan kelulusan live trading.

## 7. Self-review dan exact next action

Semakan pelan: R01–R11 dipetakan; interface consumers sepadan; fail modes Review Focus mempunyai owning tasks; codebase style dikekalkan; planned harness menguji production MQL4, bukan model pengganti sahaja. Proposal file names/signatures jelas dibezakan daripada fail yang sudah wujud. Tiada task melabel PASS tanpa bukti.

**Next action selepas review pelan:** T01 read-only recovery dan scoped architecture checkpoint. Cadangan execution ialah inline/native supaya interface owner tunggal kekal konsisten; independent reviewer digunakan pada boundary major/final review. Delegation task-by-task hanya jika pengguna memilihnya. Tiada implementation dimulakan dalam sesi penyediaan pelan ini.
