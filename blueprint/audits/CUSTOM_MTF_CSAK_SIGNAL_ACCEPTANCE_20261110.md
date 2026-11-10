# SIG-03 CSAK/CSD acceptance — 2026-11-10

Status: VERIFIED for the canonical Close-only CSD predicate, existing consumers and bounded read-only CSAK source/context acceptance. This is not full Custom MTF execution acceptance or release readiness.

Base2a5ed3113cb76cddaedebaca48183139a21da623; tested codeb2b2250e9f3cb2d5410bd844d912b3571be760d6; branch feat/custom-mtf-v1-20261108, Draft PR #303.
Build6.09 / V609_CSAK_CLOSE_ONLY_20261110 / CSAK_CLOSE_ONLY_002_20261110.
Source LF SHA256 d74f41d0c85e8ec5e4afdd58728c4cfcaae5765adc128f4aefa849edbfb04c25. Final publication SHA is in PR #303.

## Rule and smallest change

Accepted user decision: a valid closed BUY Close exceeds MA5High, MA10High and MidBB; SELL Close is below MA5Low, MA10Low and MidBB. Open/body span, colour and previous-bar crossover are not direction conditions. Equality fails strict beyond-line comparison. Shift0/negative, invalid direction and invalid required values reject. This is the user-directed reconciliation, not a newly authenticated founder quotation.

DetectCSD composes the existing M10 Close-pair and MidBB helpers. Its signature is unchanged. Obsolete direction-body-only helpers have no remaining production caller and are removed. No unrelated Extreme/MHV body-anchor calculation changes. Canonical same-candle Momentum > CSD > eCSD precedence stays in unchanged consumers; raw predicates may overlap.

ReadM10CSAKSnapshot delegates to this canonical CSD predicate and the existing M06 MA functions. It reuses M10's finalized20-close MidBB input/fingerprint reader; it reads ten High/Low inputs for the relevant5/10 MAs and fences all20 closes/times and ten High/Low after classification. It recomputes MA values on every read, without a separate stale MA cache or alternate numeric classifier. Current/historical source-result slots are symbol/TF isolated. No lifecycle updater, candidate or execution owner is added.

CSA/CSAK share the existing read-only view branch. Context identity includes symbol, signal label, TF, direction and closed source-bar time. Priming does not emit a historical trigger; missing data aborts without consuming a batch. Views always retain recoveryOnly=true and closed entryWindowOpen/entryEligible/executionAvailable flags. Observation identities are not physical order reservations or completed T05–T07 dedup.

## Evidence

| Layer | Observed result |
|---|---|
| Baseline RED | Actual extracted6.08 CSD rejects Close beyond all3 lines solely because Open is on the wrong side |
| Host targeted |6 test functions plus module import assertions, extracted C++ comparisons and all custom Python py_compile PASS |
| Native compile | Full EA and current harnesses0 errors /0 warnings |
| Canonical CSD |211/211 across7TF; Open independence/no reads, strict required-line equality, missing/invalid/closed-shift and D1/M11/M12 consumer delegation |
| CSAK snapshot/context |189/189 across7TF; independent CSA identity, MA/Mid distinctions, revisions, unavailable data, symbol/TF isolation, prime/duplicate/retry and no orders |
| History |140 direction comparisons in canonical layer and140 in snapshot layer against finalized iMA/iClose; same bounded source sample, not280 independent bars |
| Existing characterization |141/141 with accepted Close-only expectations |
| Affected native regression | eCSD190, CSA154, MOM55, observer4/observer-M09 4, M09producer52/replay57, canonical47, MHV-TF238, producer22, recovery27, higher23, flow12, prefreeze61 PASS |
| Actual controller | GBPUSD Aug4 2026 02:00–06:00 chart time; actual OnTick/OnTimer → M27 → ProcessPair, M1 delivery/model2, canonical M15 clock |
| Source views |420 combined CSA/CSAK views across15 frames checked against closed iClose/iMA and read-only flags |
| OFF/ON | Identical full12,224-row scalar owner/decision traces over16 M15 cycles per case |
| Frozen6.08 comparison |296 changed owner/M12 lineage/Type4 rows; Decision-field differences0 in this window |
| Orders | Every profile valid decisions0, captured attempts0; no orders |
| Integrity |17 native manifests,19 current source/binary bindings, include/harness/source hashes and3 complete gzip traces verified; final process6212 exit0 |

Full pytest is unavailable in the resumed cloud environment and was not rerun; no new full77/77 claim is made. Native and targeted evidence are not silently promoted to whole-project/release acceptance.

## Review and retained failures

An independent code reviewer found no material confirmed defect. A small coverage gap for High/Low-only revision during MA read was identified. The final context harness mutates High while the platform MA is read and verifies unavailable/no-cache output across all7TF; all7 added cases pass. Only this affected context harness and final bindings were rerun. The exact-source regression/controller evidence was reused.

Initial rev001 native compile produced2 uninitialized-array warnings. Explicit array initialization and unique source rev002 resolved both before native acceptance. Source semantics were not changed to accommodate tests. Older observer fixtures had used CSAK as an unsupported row; with the accepted mapping now supported, they provide a complete M1 numeric fixture and assert a readable false/non-executable CSAK view. Historical Open-span characterization expectations are updated to the accepted Close-only witnesses; old source/evidence remain in earlier commits.

Nine protected consumer/clock bodies remain identical to the pre-migration lineage: eCSD, CSM, MOM classifier/snapshot, D1 owner, canonical M09 transaction, ProcessPair, OnTickMain and position management. No duplicate function name was found. No risk, sizing or execution patch is included.

## Intended old/new state effect

Full archived differences show H4 source classification strengthening from eCSD to CSD and M15/H1/H4 M12 Type4 precursor/context replacing NONE/Type1 where the old Open condition excluded CSD. The296 rows include corresponding M12 state/geometry/start/qualifying/reason fields. This is an intended consequence of the approved wider CSD predicate through unchanged consumers. It is not evidence that historical candidate sets, trades or profitability remain unchanged. No final Decision field changed in this particular window.

## Limits and sequence

M30 is the declared complete-bucket derived OHLC fixture. Seven-TF arithmetic/source reads do not authenticate session/market completeness. Timer callbacks are delivered by the harness; live wall-clock scheduling, arbitrary cold-start structural epoch, positive-entry/broker execution, multi-symbol trading and profitability remain unproved. Semantic availability/all77 and custom auto-entry remain OFF.

SIG-01 eCSD and SIG-02 CSA are reused. SIG-03 is complete only in this declared predicate/consumer/read-only context scope. Verify this publication before starting SIG-04 MOM. Overall T04-D/F, source/owner-epoch/session recovery and custom Context/Trigger/selection/dedup/risk/execution remain separate pending gates. No merge, deployment or primary-terminal restart.
