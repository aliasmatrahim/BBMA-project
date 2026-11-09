# T04-E — M09 TF coverage preflight

Classification: VERIFICATION REQUIRED / implementation gap; not a new signal rule.

SOURCE_INDEX retrieval: accepted Core section6 requires same-source-TF/cycle Extreme provenance, actual normal TP-Wajib, structural loss, frozen body, retest and stage-bounded invalidation. F1 lifecycle decision Decisions1–12 fixes this single owner model; C040 accepts higher-TF MHV as bounded nested context and explicitly preserves exact REM. Generic MHV context is not restricted to M15 by the accepted source; exact REM still requires M15.

Current implementation inspected at Build6.01:
- ResetMLVState hardcodes M15; AttachCanonicalMHVParent calls it without restoring data.timeframe.
- UpdateCanonicalMLVState compares owner TF with data TF, then calls that M15 reset. Directly feeding H1/H4/etc would repeatedly reset the owner.
- ExportCanonicalMHVSignal and ProjectCustomMHVView explicitly reject non-M15.
- PairState has one buy/sell M09 owner pair for M15; ProcessPair advances those owners. Custom-only M15 source advancement currently advances M08/M12, not M09.
- Therefore current read-only M15 fixture8/8 is projection evidence only. It must not be described as seven-TF M09 producer acceptance or custom-only M15 lifecycle proof.

Required safe sequence: parameterize owner reset/attachment by source TF while preserving canonical M15 wrappers; prove same-TF parent and closed-data identity; reuse the same UpdateCanonicalMLVState engine for additional isolated owner pairs; include M09 in staged chronological replay and all owner equality/control tests; reuse existing M15 owner slots instead of cloning them. Then exercise full parent→TP→loss→formation→retest→direction/void/supersession trajectories and M15 regression in native tests. No data.timeframe relabeling or duplicate DetectMHV is allowed.

Missing producer/recovery evidence leaves all extra MHV/MLV rows unavailable. No new executable owner or admission flag is enabled by this audit. T04-E remains pending implementation/acceptance, not source-rejected. T04-B full cold-start/session proof remains a separate blocking gate for executable availability.

## T04-E/1 implementation boundary — Build6.02

The first atomic change removes M15 hardcoding from owner reset/attachment and source-parent maturity checks. The UpdateCanonicalMLVState entry point remains the same engine. Parent TF must equal data TF, and parent direction must oppose the MHV direction. Existing callers of ResetMLVState/IsMHVParentExtremeMature keep an M15 default. ExportSourceMHVSignal exposes source identity; ExportCanonicalMHVSignal remains an explicit M15-only wrapper, preserving exact REM. Unknown TFs and TFs above D1 are rejected by the existing timeframe-seconds mapping and limit.

This foundation does not allocate new per-TF owners, wire extra producers, alter ProjectCustomMHVView admission or prove cold-start recovery. Existing production M09 calls are still canonical M15 only. The initial210-check native fixture deliberately feeds deterministic synthetic structural candles through the actual engine, in both directions on each of7TF. Baseline6.01:64 pass/146 fail; candidate6.02 initial run210/210. Final fixture includes28 extra new-parent atomic supersession/next-cycle attachment checks and passes238/238. Targeted native M15 projection8/8, M10 snapshot55/55, callbacks12/12, clock14/14, actual startup4/4 and full-EA compile0/0 also pass. Full local pytest73/73. Source/hash/binary binding is recorded in *602_evidence.json. Fixture prices are not broker-history or profitability evidence.

Next atomic stage T04-E/2: maintain one M09 owner pair for each supported symbol/TF, reuse existing M15 slots, include M09 in staged chronological source replay and all-field equality, use the existing M10 direction calculations for stage takeover, and then project only refreshed/proven source rows. Common pipeline order must preserve M08→M09→M12. Canonical-role symbols must not advance their existing M08/M12 owners twice. A failed provenance/recovery check hides the view; it must not silently reset structural state or invent a historical trigger. Full E acceptance remains pending this wiring and source-chain evidence.

## T04-E/2 — Build6.03 producer/replay checkpoint

The common updater now advances M08→M09→M12, with M09 state included in every staged replay copy. Auxiliary TFs keep their single owner pair in CustomAuxLifecycle; D1/H4/H1 custom-only symbols have three isolated owner pairs; M15 reuses existing canonical slots. The read-only view shares MHV/MLV identity and rejects stale/recovering owners. Canonical higher-TF M09 remains unavailable; adding its parent-Extreme installation after the canonical controller is not admitted by this monitor patch.

Verification: initial native6.02 wiring fixture24 pass/28 expected fail; native6.03 producer52/52. Seven-TF actual source-snapshot replay against continuous control57/57, using explicitly trusted completed-owner anchors. Equality covers31 MLV +31 RE +20 Extreme fields in both directions; future M09 watermarks hold without reset. Real moving M1 tester callback integration12/12 now requests MHV/MLV/MOM only on M1 (RE/EXT request flags false), proving scheduler admission reaches the shared producer. M30 remains the declared derived OHLC fixture. Native full EA compile0/0, startup4/4 and the targeted native regression suite pass; full local pytest73/73. Detailed bindings/counts are in regression603_evidence.json and the individual manifests.

T04-E remains PARTIAL. Next: audit canonical D1/H4/H1 M09 parent installation inside the canonical pre-freeze producer order, then implement only a source/ownership-consistent path with regression evidence. No private duplicate parent or silent post-controller lifecycle mutation is allowed. Final source-chain, gap and cold-start admission remains subject to T04-B.


## T04-E/3 — bounded canonical monitor and transaction-log boundary

The accepted monitor boundary now stages canonical D1/H4/H1 M09 only from current cached closed data and a completed canonical M15 cycle. Temporary parent snapshots must remain identical in all20 fields. Only new M09 state/progress commits; canonical M08/M12/decision/clock stays untouched. A dedicated producer-proof stamp prevents unobserved/foreign owner state from being projected. Parent handover, future timestamps and non-contiguous observations stay unavailable/HOLD; no canonical history or private Extreme owner is guessed.

Build6.03 missing-feature baseline29 pass/18 fail; observer baseline3 pass/1 fail. Build6.04 state47/47 and observer4/4 passed, but an added log probe reproduced3 uncommitted MLV_SUPERSEDE events alongside3 direct canonical default-control events. That candidate is preserved as WIP, not accepted. The cause was callee logging before caller commit/discard. Build6.05 adds default-preserving internal telemetry policy and disables emission only during the guarded temporary stage. Detailed final evidence is recorded in *605_evidence.json after native acceptance.

Full T04-E remains PARTIAL: unrestricted canonical parent installation, historical session/owner-epoch reconstruction and final executable admission are not proved by trusted source/owner/producer-stamp fixtures. Auto-entry remains OFF.


## User C+1 / T04-E/4 — Build6.06 WIP, NOT NATIVE VERIFIED

The user authorized preparing the shared parent transaction before frozen M13 consumers. ProcessPair now calls D1/H4/H1 advancement after the canonical M08 updates and before persistent Extreme exports. One shared transaction validates phase/source/anchors, stages both directions and commits existing canonical owner slots; late observations keep the6.05 parent-read-only guard. No requested-signal flag gates canonical advancement; M15 is excluded from this additional producer. Existing gap/epoch HOLD is not lifted.

Cloud transaction tests use actual extracted transaction logic with explicit M09-stage/platform fixtures: baseline timing and missing-wiring checks RED, candidate2/2 GREEN with12 behavior assertions; full pytest75/75. The prepared native harness expects61 assertions on trusted trajectories across both directions/D1/H4/H1, but none ran because G40 is offline. Full strict compile, actual ProcessPair request ON/OFF decision parity, old/new canonical differences, native regression and startup remain NOT VERIFIED. This code is a reviewable candidate, not E/4 acceptance, deployment or permission to activate trading.
