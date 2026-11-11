# Custom MTF remaining-gate evidence review — 2026-11-09

Branch: feat/custom-mtf-v1-20261108. Base remote: 3018af9b2bfe403ba3e1ec9cf6030fd22c3b7b43. EA remains Build6.05; LF SHA256 4247b5aa6babc62d7680fcb71e8859a74452638ba60c9c0fa084fae7f6f78415. This is additional validation, not T04 acceptance or a new EA build.

## Completed evidence subtasks

T04-B/provenance-review: retrieved four existing G40 metadata files with byte counts and SHA256 in provenance_review605_evidence.json. The MetaQuotes clock audit explicitly reports HISTORICAL_POLICY_NON_STATIONARY and reference-only status. Its sampled August2026 best-fit UTC+2 is correlation evidence, not authentication of each historical session. The separate Dukascopy GBPUSD BID manifest covers through September1 2026 and lists six2026 TF files; its classification explicitly excludes broker-canonical authority. It records repair overlays, exclusions and32 tick-empty/H1 conflict hours. Those aggregate historical counts are not proof that the July31/August3 window itself is defective.

Ruling: do not substitute a Dukascopy/NewYork session boundary or fitted UTC+2 for the installed MetaQuotes HST provenance. Cost if wrong: conservative unavailable periods; accepting it without proof risks dropping real bars or treating absent history as a closed session. No HST rewrite, data download, synthetic fill or primary-terminal restart occurred. This metadata retrieval subtask is complete; full T04-B remains HOLD.

T04-D/native-characterization: new CustomDirectionHarness includes the actual current EA, renames callbacks and substitutes synthetic iOpen/iClose reads only inside the test translation unit. It directly invokes existing DetectCSD/DetectECSD. Ten cases ×seven TF arguments ×two detectors plus no-orders assertion =141/141. BUY/SELL full spans, open already beyond Mid, Mid-only movement, an incomplete MA pair, exact Mid close and invalid direction are covered. Native EA and harness strict compilation each0 errors/0 warnings; isolated tester process20264 exited0. Full cloud regression73/73. Source, harness and include hashes match native manifest.

Ruling: this is characterization of the accepted engineering body-span mapping, not RED→GREEN feature implementation, original-source adjudication or live seven-TF data coverage. No CSA classifier, CSAK alias or availability flag is introduced. In the open-already-beyond-Mid cases, canonical CSD=false although the close lies beyond MA5/10 and Mid; the real native detector now corroborates the earlier four-case extracted sensitivity result. Mid-only cases also show why CSA cannot alias eCSD. Cost of retaining the gate: CSA/CSAK unavailable until exact mapping is reconciled.

## T04-E parent handover dependency

Current ProcessPair updates canonical M08 owners, exports H1/H4 persistent Extreme snapshots, updates M15 M09/M12, observes M12N, then assembles M13/M14 from frozen owners. InstallMHVSupersessionParent resets/replaces the referenced Extreme owner; it is not a read-only M09 update. Therefore allowing ObserveCanonicalMHVSource to commit that parent after ProcessPair would change an owner already consumed by canonical assembly. A private cloned persistent parent would instead duplicate ownership.

Ruling: keep WAIT_CANONICAL_M09_PARENT_HANDOVER and its existing47/47 bounded proof. Any future full integration must place the shared parent transaction before the affected persistent exports and frozen consumers, cover both directions atomically, and prove that enabling/disabling diagnostic requests cannot change legacy execution decisions. No new detector, post-freeze parent write or M15 bypass is admitted. This is an architecture dependency analysis, not verified implementation.

## Exit audit and exact next actions

| Task | Current status | Evidence still required |
| --- | --- | --- |
| T04-B | HOLD | Same-feed historical session/quote-vs-missing classification bound to installed HST hashes, plus trusted owner epoch/snapshot or source-proven reconstruction; arbitrary cold-start NONE is not established. |
| T04-D | PARTIAL | Exact CSA/CSAK body-cross/close-side alias decision through accepted source reconciliation, then shared materialization and Context/Trigger maturity/admission evidence. Native characterization alone does not close it. |
| T04-E | PARTIAL | Pre-freeze canonical parent transaction and regression evidence, non-contiguous recovery and source-epoch admission. |
| T04-F | BLOCKED | B/D/E acceptance, entry-window and full reinit/timer/isolation proofs. |
| T05–T12 | PENDING | Required T04 authority interfaces; do not begin downstream acceptance through unavailable owners. |

Exact next action: retrieve broker-bound history/session evidence for the installed MetaQuotes GBPUSD July31→August3 boundary, and a trusted source-owner epoch; reconcile the two M10 candle interpretations before alias admission. The supplied user definition settles CSA as MidBB direction, not its exact open/close numerical interpretation. Existing evidence does not authorize guessing that interpretation. Independently, a future canonical pre-freeze handover patch needs the ownership proof above; no such patch is claimed here.

All77 semantic availability cells and five slots retain their previous OFF defaults. No merge, orders, release readiness, wall-clock timer, arbitrary cold-start or live custom-entry claim. Old startup/binary evidence remains tied to its frozen6.05 artifacts; this run's newly compiled EA binary was compile evidence, not a new deployment/startup acceptance.

