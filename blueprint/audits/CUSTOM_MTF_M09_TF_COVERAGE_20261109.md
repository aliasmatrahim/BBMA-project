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
