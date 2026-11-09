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
