# T04-E/4 native acceptance — 2026-11-10

Task: C+1 / T04-E/4 shared pre-freeze M09 parent transaction.
Branch: feat/custom-mtf-v1-20261108. Issue302 / Draft PR303.
Tested source commit: 6fa4aafa8fa8b4ad0b193a4af89d1ea04f2e932f.
Pre-publication head: f4a30242bf9b292cb8fef783ac8ecada514d3cd5.
Build6.06 / V606_M09_PREFREEZE_TRANSACTION_20261109.
Source LF SHA256: 0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e.
No EA/include/production behavior changes in this evidence checkpoint.
Publication commit is recorded in Draft PR303 and branch history.

## Ruling

E/4 VERIFIED only for bounded native transaction/controller mechanics below.
T04-E overall PARTIAL. T04-B session/epoch and T04-D CSA/CSAK mapping remain unresolved.
T04-F and dependent T05+ cannot advance. All77 semantic availability cells and custom auto-entry remain OFF.
No merge, deployment, primary-terminal restart or trading activation.

| Exit criterion | Actual evidence | Ruling |
|---|---|---|
| Strict MQL4 compilation | Full EA and all affected native harnesses: 0 errors / 0 warnings, source/include/EX4 identities bound in native606_evidence.json | PASS |
| Atomic pre-freeze owner transaction | 61/61 native checks, both directions D1/H4/H1, duplicate reuse, phase fence, symbol isolation, post-cycle reuse, gap/future-anchor HOLD | PASS for trusted fixtures |
| Actual controller wiring | Actual OnTick/OnTimer -> M27 -> ProcessPair, 16 M15 cycles per trace, 764 serialized scalar values per cycle | PASS for this tester window |
| Positive parent handover | Explicit trusted pending-owner fixtures on existing OHLC: D1/H4/H1 3/3, full M08/M09 snapshots match shared engine after actual ProcessPair | PASS for seeded integration; not natural formation |
| Monitor independence | OFF/ON full 12,224-row traces identical in both unseeded and seeded profiles; ON15 observer frames vs OFF0 | PASS within window |
| Negative control | Frozen6.05 seeded baseline handovers0/3, MQL ok=false EXPECTED; candidate3/3, ok=true. Driver correctly accepts the expected negative control | Distinguishes old/new behavior |
| Affected regression | canonical47, observer-M094, M09producer52/replay57, producer22, recovery27, higher23, owner10, MOM55, TF238, observer4, MHV8, flow12, clock14 | PASS, separate scopes retained |
| Startup | Actual OnInit: defaults, changed inputs, invalid formula rejection, unavailable-signal rejection: 4/4 | PASS; not live reattachment |
| Cloud | 75/75 pytest, py_compile and diff check observed earlier in this session, before final test-only timestamp fixture revision; final revised fixture native-tested | Prior cloud proof; no fresh final cloud rerun after environment loss |
| Orders/entry | Every controller case valid decisions0 and captured OrderSend attempts0 | No positive selected-entry, execution or profitability proof |
| Recovery/session | HST identities unchanged; authenticated historical session/UTC/owner epoch absent | HOLD; not closed by contiguous/seeded tests |

## Actual controller experiment

GBPUSD, 2026-08-04 02:00-06:00 chart/source time. Test delivery M1/model2; canonical processing clock remains M15.
Timer callbacks are deliberately delivered by the harness; no wall-clock timer scheduling claim.
M30 is the already declared derived complete-bucket OHLC fixture. Other HST files are installed broker-format files, not session authentication.
Numeric scalars serialize at16 decimal places; this is not a universal bitwise-float guarantee.
Unseeded OFF/ON rows are identical; comparison with6.05 differs288 rows in higher-TF M09 direction/parent-direction/timeframe initialization fields.
Seeded OFF/ON rows are identical; comparison with6.05 differs936 rows. This is expected behavior change, not a claim of unchanged legacy decisions.
No natural higher-TF parent handover appeared in the unseeded window.
Seeded fixtures use actual earlier iTime source bars and a trusted owner epoch; they do not prove historical formation or reconstruction across missing sessions.
The test-only OrderSend capture returns -1; all custom slots and ExpertsTrades are disabled.

Final harness LF SHA256: 520aa81547710cdccda35a1dfae454677b1a7130ef4709e5bfb164665f9336c2.
Baseline harness prepends CONTROLLER_BASELINE605 to the same fixture; LF SHA25697e560db8245f5bd58bf37178de72da72b128d4204f7668fe9a26d476b8c773a.
Driver LF SHA256a49b23cc651110181162a20440b677e07b5cba5c29b2fd00c2a170d5e7758517.
Frozen6.05 source LF SHA2564247b5aa6babc62d7680fcb71e8859a74452638ba60c9c0fa084fae7f6f78415.
Native final controller driver PID4672 exit0; suite PID12392 exit0; manifest/binary collector PID4760 exit0.
The two final controller manifests bind all six full traces; compressed traces are archived beside them.

## Failures diagnosed rather than hidden

Initial M15 open-price delivery advanced the current M5 bucket ahead of quote time (02:29:59 quote vs02:30:00 current-open), producing monitor frames0.
The observer correctly waited on the future boundary. Only test delivery changed to M1/model2; no production timing guard was weakened.
An earlier cloud test invocation from the parent directory raised16 collection FileNotFoundErrors. Running from the repository root passed75/75; no production patch was required.
Final fixture revision replaced nominal older timestamps with actual source-bar iTime values. The final six native profiles were rerun against the final exact harness.
A recovery check detected stale seeded gzip blob references. Publication uses regenerated final trace blobs verified against current native trace hashes.

## C source review

Read-only local original V05/V06 videos were recovered on G40 and decoded using the installed ffmpeg.
Seven time-aligned frames extracted; five archived. Video/frame hashes are in source_frames606_evidence.json.
V05 at1801 seconds: written close beyond MA5/10 Hi/Low, CS Awal.
V05 at2062 seconds (34:22), six seconds after the routed33:44-34:16 strong-direction window: completed definition close beyond MA5/10 Hi/Low plus MidBB, CS Kukuh. Frame has a dissolve transition; text corroboration only.
V05 at1869 and V06 at1035/1211 show chart context; none decisively determines the open-side rule when the candle already opens beyond one required line.
Original V05 subtitles755-768 and V06 routed17:07-17:45 /20:07-20:18 corroborate close-side wording.
This strengthens source evidence but does NOT choose body-cross vs close-side engineering mapping, alias CSA to MA-only eCSD, or promote any executable capability.
Existing canonical engineering mapping remains unchanged pending deterministic reconciliation.
Video provenance is corroborated by the existing download references; independent official authorship authentication is not established.

## Checkpoint integrity and exact next action

The cloud execution environment became unavailable during final publication. Recovered full manifests, test source and final traces were revalidated through G40 and GitHub; no native test was restarted without cause.
This checkpoint is reconstructed from those exact artifacts through GitHub APIs, rather than claiming an unavailable local working-tree commit.
Unpublished local documentation edits may still exist if that workspace returns; reconcile them with this commit and do not blindly republish stale seeded trace references.
No final cloud rerun or local-vs-API tree-equality claim is made after workspace loss.
The frozen EA header retains its historical WIP text; this dated acceptance supersedes native-mechanics status only, not release readiness.

Next: retrieve a source-discriminating CSA/CSAK open-side example under current SOURCE_INDEX and document an explicit source/engineering mapping decision; separately obtain same-feed historical session/UTC and trusted owner-epoch evidence for T04-B/E reconstruction.
Then run targeted cold-start/gap reconstruction checks against those authenticated boundaries. Unknown owners stay unavailable.
Only after B/D/E exit criteria pass may T04-F integrated acceptance and dependent T05 advance.


## T04-E/4 checkpoint reconciliation — 2026-11-10

Recovered live Draft PR303 head bd3367b0a1747fb239ec8615a8b5343c3ba5b94c on feat/custom-mtf-v1-20261108; owner d1-owner-dev459c0588e625d7f7630f0fb5612b7f04fda496de unchanged. G40 online. CURRENT/MASTER_QUEUE/SOURCE_INDEX on owner match the local copies exactly. Local interrupted documentation and stale seeded gzip references were preserved in a temporary backup and reconciled to the published evidence before validation. Four previously unpublished native/source/contract/plan addenda are now included in the same checkpoint lineage.

Fresh final cloud command from repository root: PYTHONPATH=/workspace/scratch/f5ddfbd6f6f6/pytest-deps python -m pytest -q -> exit0,75 passed in0.98s. Final controller driver py_compile and git diff --check PASS. All six gzip traces decompress to their published SHA256/12,224-row manifests; monitor OFF/ON bytes match in both profiles. Final harness/source identities, five JPEG hashes, native manifest pass flags and startup4/4 bindings rechecked. This closes the previously missing final cloud rerun, not any new native/live acceptance. No native tests or compile were rerun because production source and final native harness are unchanged from verified artifacts.

Confirmed documentation error corrected: V05 frame2062 is34:22, six seconds AFTER routed33:44-34:16, not inside it. Text corroboration only; no candle-geometry inference or CSA/CSAK predicate is promoted. Existing six-second source-window error had no executable effect. Earlier dated evidence remains historical; this addendum supersedes only final-cloud/reconciliation status.

Source stays Build6.06/SHA0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e. E/4 bounded native mechanics VERIFIED; B session/owner epoch HOLD, D mapping PARTIAL, E overall PARTIAL, F BLOCKED. Auto-entry and all77 availability cells OFF. No merge/deployment/primary-terminal restart.

Exact next action: continue C under current SOURCE_INDEX with a labelled CSA/CSAK candle example distinguishing open-side interpretations; separately obtain same-feed authenticated historical session/UTC and trusted owner-epoch evidence before B/E cold-start/gap validation. Do not use the seeded handovers as historical reconstruction evidence. No downstream dependency is waived. Publication SHA is recorded in Draft PR303.
