# T04-E / SIG-06 upstream and M16/T07 prerequisite reassessment

Date: 2026-11-14  
Task ID: `T04E-SIG06-UPSTREAM-M16-T07-REASSESS-01`  
Status: **AUDIT COMPLETE; SIG-06/T04-E HOLD; T06 overall HOLD; M16/T07 custom integration not eligible**  
Auto-entry custom: **OFF**. Merge/trading activation: **not performed**.

## Live repository state

- Repository: `aliasmatrahim/BBMA-project`.
- Draft PR #303 branch at audit start: `feat/custom-mtf-v1-20261108`, head `a2f23b40be331c96f5ebddf30b8196ef020efb35`.
- Live implementation owner: `d1-owner-dev`, head `7567af7dfbfaafff35a37c1d307b387e96273c78` (merged PR #301).
- PR #303 remains open/Draft/unmerged and GitHub reports `mergeable=false`. Compare reports the feature branch is 132 commits ahead of the owner while the owner is 3 commits ahead of the feature branch. Keep the two lines unreconciled; this audit does not rebase or merge.
- `blueprint/CURRENT.md` still records owner head `459c0588e625d7f7630f0fb5612b7f04fda496de`; the live branch ref above is the current authority.

## T04-E / SIG-06 owner epoch and recovery

**Finding: full acceptance remains HOLD.** The Build 6.13 M09 availability-propagation fix and bounded restart/rejection checks are reusable verified work; they do not prove a source-valid M08/M09 epoch across an authenticated session/history gap.

Evidence and limits:

- `source_epoch_followup606_inventory.json` scanned 3,904 names and hashed 210 candidates across four named roots. This is bounded discovery, not a G40-wide absence claim. It found no accepted actual M08/M09 cycle-origin checkpoint. The reviewed M11 Epoch_R1 and Q10 snapshot are different owners/builds and cannot substitute.
- A later read-only HFM capture identifies the test feed as `HFMarketsSV-Demo Server` / GBPUSD. The primary deployment profile remains `BBMA_PRIMARY_BROKER_UNRESOLVED` because no accepted project decision binds that demo server to the target deployment profile. The capture is not an exhaustive broker tick archive, and no authenticated historical quote-vs-missing boundary is yet bound to the installed HST hashes.
- SIG-06 requires an origin tied to the same symbol/feed/history revision, source TF and source candle/cursor, full M08 and both M09 owners (M12 where applicable), parent-cycle/TPW origin, and intervening accepted events. Then bind that snapshot before controlled restart and compare full continuous versus recovered owner state across the authenticated boundary. An arbitrary `NONE`, another feed's calendar, fitted UTC offset, or synthetic fill cannot satisfy it.
- Reusable bounded evidence: Build 6.13 availability propagation has native RED/GREEN and regression records, including strict 0-error/0-warning compile, 295/295 caller checks, 785/785 inner-status checks, 323/323 expanded candidate checks, and 14 native regression groups. The natural-origin restart audit covers M1/M5/M15/H1 only; its report explicitly leaves full session/origin acceptance HOLD. The 340/340 production-admission checks prove safe refusal on unavailable recovery input, not successful recovery.
- Do not repeat those verified suites. No new compile/regression/runtime was run for this documentation-only audit.

References: [source/epoch retrieval](CUSTOM_MTF_SOURCE_EPOCH_RETRIEVAL_20261110.md), [SIG-06 preflight](CUSTOM_MTF_MHV_SIGNAL_PREFLIGHT_20261110.md), [availability propagation](CUSTOM_MTF_MHV_AVAILABILITY_PROPAGATION_20261111.md), [natural-origin restart](CUSTOM_MTF_MHV_NATURAL_ORIGIN_RESTART_20261111.md), [production admission](CUSTOM_MTF_MHV_PRODUCTION_ADMISSION_20261111.md), and [bounded inventory](../runtime/custom_mtf/source_epoch_followup606_inventory.json).

### Newer same-server HFM probes and live capture (2026-11-14)

The newer artifacts narrow the gap, but do not close it:

- `t04be_hfm_forward_capture_20261112.json` identifies the test feed as `HFMarketsSV-Demo Server` / GBPUSD; terminal AutoTrading was false. The recorder's own scope says the quote stream is terminal-observed and not an exhaustive broker tick archive.
- A read-only G40 inspection of the active capture `MQL4/Files/BBMA_HFM_GBPUSD_SESSION_1794417276.csv` found the last `TICK` at UTC epoch `1794607198` (2026-11-13 21:59:58Z), with server/quote labels `1794614398` (23:59:58 at GMT+2). Heartbeats continued through `1794626329` (2026-11-14 03:18:49Z) with `connected=1`, while the server/quote labels remained frozen and the last quote remained cached. This establishes a no-new-quote interval of at least 3h18m51s during the observed weekend closure, not the Monday reopen or a complete historical boundary. The terminal remained running; no restart or order action was performed.
- HFM's current trading-hours page states server time is winter GMT+2 / summer GMT+3 and publishes a November table with Forex Friday trading to 23:58 GMT+2. The observed final quote label is 23:59:58 GMT+2; the page also distinguishes trading hours from rate refresh/quote availability. Therefore published trading hours alone do not certify the exact quote-delivery boundary. Preserve this as HOLD pending observed same-server close/reopen classification. Source: [HFM trading hours](https://www.hfm.com/int/en/trading-instruments/trading-hours).
- The H1 archive probe replays 2,528 HFM archive rows through a test-only series adapter. August and November cases retain `hold=true`; chart labels do not authenticate UTC or historical session state.
- The H1 origin probe compares six exact M08/M09/M12 owner states against a zero-initialized 120-bar baseline and matches 1/6. The H1 seed probe has bounded convergence on the July sample, but the October pre-gap case does not converge to an exact M09/full owner. These are diagnostic initial-state hypotheses, not an independently witnessed/source-proven owner epoch.
- HFM archive/origin/seed probes therefore remain T04-B/E HOLD: first post-weekend quote, independently source-proven pre-gap epoch, and production continuous-versus-recovered parity are still missing.

This evidence identifies the test server and provides a real read-only closure sample. It does not establish that the HFM Demo is the deployment profile, nor does it prove the full session boundary or trusted owner epoch.

## Remaining fresh-event upstream

| Signal | Current implementation/evidence | Remaining gate |
|---|---|---|
| RE / RE1–RE4 | Read-only fresh adapter resolves concrete subtype and ties the physical event to the owner EntryCandle/continuous boundary. | Owner availability and entry gates remain OFF; persistent reservation/consumption is T07. No Custom M15/M16 execution acceptance follows from the adapter. |
| EXT | Read-only event maps to exact M08 retest-completion candle and actual next observed source open. | Availability remains OFF; this is not an authority expansion of standalone H1 Extreme. |
| MHV/MLV | One M09 owner emits a read-only formation/setup receipt. MHV/MLV is not an entry Trigger. | Full SIG-06 source epoch/session recovery is HOLD; all availability gates remain OFF. |
| MOM | Read-only per-closed-candle receipt uses source-bar identity. | Recovery-only/execution-unavailable; no Trigger/Context authority or persistent T07 consumption. |
| CSA/CSAK | Accepted close-only predicates and read-only per-candle snapshots exist. | No fresh-event adapter is authorized. Repeated true predicates do not establish a fresh event; neither a prior-cross edge nor reset/TTL/expiry is defined. This is event identity/consumption HOLD, not an open-price or predicate gap. |

Source: `CustomFreshEvents.mqh` revision `CUSTOM_FRESH_EVENTS_DRAFT_004_20261113` and [T05 draft interface](../contracts/CUSTOM_MTF_T05_DRAFT_INTERFACE.md). The current evaluator still requires owner availability and entry gates; all 77 signal×TF availability cells remain OFF. Frame-local duplicate-ID filtering is not persistent reservation.

## M16 prerequisite assessment

The canonical M16 path exists in the current owner EA and validates the frozen M11 D1 authority plus exact canonical decision-owner snapshots. Custom M15 is a separate read-only receipt path: `CustomM15AuthorityReceipt` carries the selected witness, selected anchor, config/batch identity and frozen D1 owner, sets `m16RevalidationRequired=true`, and always sets `executionAuthority=false`. It has no call into M16 and is not a canonical `BBMA_Decision`.

Before connecting it, the custom handoff needs an explicit adapter that lets M16 revalidate the exact frozen M11 identity and every selected component against its current canonical owner state, failing closed on stale/missing/transition/mismatched owners. It must preserve M16's existing ownership and must not recompute BBMA rules or add a generic TTL. Current closed signal gates and unresolved SIG-06/CSA-CSAK events mean there is no eligible custom decision to advance. **M16 custom integration/acceptance stays HOLD.**

## T07 prerequisite assessment

No Custom MTF T07 contract/module/test path exists on the current PR branch. The T06 contract assigns T07 persistent reservation/consumption of the exact T05 snapshot plus matching batch/config revision; simultaneous same-anchor slot attribution and alternative fresh anchors are already retained in the T06 receipt/witness. T07 still needs its own contract for atomic reservation, deterministic duplicate handling, idempotent retry and restart persistence. Do not invent expiry/release semantics or promote availability while signal event identity is unresolved.

**Disposition:** targeted T05/T06 validation on source commit `2bab3ccb2f69211b958e68934e6add6e5ed0d253` is recorded as PASS in [the 2026-11-14 manifest](../tests/custom_mtf/T06_M15_AUTHORITY_VALIDATION_20261114.json), but overall T06 remains HOLD. The scheduler subset is not broker-session or owner-epoch recovery evidence. Auto-entry and all 77 availability cells remain OFF.

## Exact next action

1. Keep SIG-06/T04-E on HOLD. Continue the existing AutoTrading-off HFM Demo capture through the first post-weekend quote, compare UTC/server/quote labels against the HFM schedule, and classify the observed close/reopen. The test server is known, but it is not promoted to the project deployment profile without an explicit binding decision. Then bind a source-valid M08/M09 origin and run continuous/recovered owner parity.
2. In parallel, resolve the CSA/CSAK fresh-event identity/consumption contract without changing their accepted close predicates or inventing a cross/reset/TTL rule.
3. Only after upstream gates pass, implement and validate the Custom M16 adapter; then define/implement T07 reservation and retry. Keep PR #303 Draft; no merge or trading activation.
