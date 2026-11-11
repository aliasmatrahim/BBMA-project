# SIG06 MHV candidate invalidation — bounded fix acceptance, 2026-11-11

Classification: CONFIRMED BUG -> minimum shared M09 repair.
Code checkpoint0875886ec22c57a106142f523a8f9c04ddd4f2ab; source Build6.12 / MHV_CANDIDATE_INVALIDATION_001_20261111.
LF SHA256900744561bd5e5c5abaef754478a055fcf600bf178fe3174da2d484dd840f2e8.
Full SIG06 remains PARTIAL; this report closes the specific stale-candidate defect only after the evidence below passes.

## ISSUE -> IMPACT -> FIX

FORMATION_ESTABLISHED / RETEST_COMPLETE could become VOID on applicable Momentum before the pending opposite Extreme candidate passed its canonical invalidation rule.
The pending candidate's active/raw fields survived. A later reversal in VOID could call InstallMHVSupersessionParent using that invalidated raw timestamp.
This also supplies a counterexample to treating a single Momentum as universal historical-state erasure.

Added one ClearMHVSupersessionCandidate helper, reused by existing TryAdvanceMHVSupersessionCandidate and the affected early-return branch.
Before MarkCanonicalMLVVoid, an active candidate is evaluated with ReadExtremeLifecycleInvalidation using its parent direction.
Unavailable input freezes the M09 owner and parent. A confirmed invalid candidate clears only its three pending-candidate fields.
A generic MarkVoid reset would be wrong: an outer-only MHV continuation break is on the opposite side from the candidate's relevant outer break, and may leave that candidate valid. No generic reset was added.
Frozen marked body, historical parent lineage and parent owner are not changed by the clear helper. No detector, expiry, combination, risk, execution or clock rule added.

## Evidence

Native v1: frozen6.11 RED239 PASS/56 FAIL, patched6.12 GREEN295/295. Expanded v2: frozen6.11 RED239 PASS/84 FAIL; patched6.12 GREEN323/323. Native terminal PIDs13116/6108/8972/2736 all exit0; all harnesses strict0 errors/0 warnings. Collector6592 exit0 verifies source, archived harness/binary, headers, HST, traces and20 final compiled binary bindings.

Test inputs are explicit synthetic platform-series fixtures; actual native M08/M09/M10 code is exercised. This proves the lifecycle contract and guard behaviour, not frequency or occurrence on a broker history.
Original295 checks cover sevenTF×BUY/SELL×FORMATION/RETEST×Momentum/outer-only scenarios plus initial-unavailable controls and no orders.
Expanded323 adds28 checks over14 cases for failure during the new extra read after initial readiness succeeded.
The revision test measures the initial canonical input read with cache disabled, injects missing Close9 only after that read, asserts injection was reached and compares all M09/parent fields to the original state.
Summary failed=0 is required; INIT_SUCCEEDED/terminal exit alone is never accepted.

All22 specialized native groups PASS, including source141, M08 lifecycle716, Momentum/readiness, direction, M09 TF/producer/replay, canonical observation, recovery, flow, higher-TF and pre-freeze. Actual controller OFF/ON/frozen6.11 traces exactly match in both ordinary and seeded profiles:16 M15 cycles and12224 scalar rows per case,0 baseline differences,0 attempts. Seeded profile exercises3 seeds/3 parent handovers per case. Monitor ON exposes630 direction/Momentum plus180 Extreme views. Full EA strict compile0E0W confirmed by specialized runners.

Cloud: six available test functions, two import assertion scripts and2187 shared-pair numeric comparisons PASS on exact900744 source. python -m pytest could not run because pytest is absent on cloud and G40. No full repository pytest claim.
Independent review found no remaining material patch issue after extra-read source-revision coverage was added. Native evidence was separately read and bound, not inferred from review.

## Historical/session evidence and original acceptance limits

Prior6.11 bounded restart242 checks and fail-frozen340 checks stay bound to a626...; they are not relabelled as fresh6.12 runs.
The strict production gap-admission policy is unchanged. No new broker calendar, source repair or unknown-state NONE is inferred from this bug fix.
Current official Dukascopy Trading Sessions lists GBP/USD's currency families under NY17:00 sessions (https://wiki.dukascopy.com/en/manuals/jforex4-desktop/trading-sessions).
Its Candle Formation documentation explicitly describes JForex4v4.9+ logic (https://wiki.dukascopy.com/en/manuals/jforex4-desktop/trading-sessions-logic); it is current platform documentation, not historical MT4 dataset certification.
A dated3Nov2025 bulletin corroborates the2Nov2025 switch of system opening/settlement to22:00GMT (https://www.dukascopy.com/swiss/english/about/ournews/daylight-savings-time-ends-in-us-dbl203230).
These support vendor context only; they do not authorize deployment-broker historical session policy or resolve every source gap.
G40 profiles/broker_profile.json remains BBMA_PRIMARY_BROKER_UNRESOLVED with broker/server/offset/DST/week rules null; synthetic_ny_close_test_profile remains isolated-reference-only.
F1 semantics are resolved; remaining historical recovery authority is not an Open-price or MHV formula ambiguity.

Remaining original exits:
- accepted same-feed historical production boundary/session authority;
- source-proven owner epoch beyond the bounded initial-state hypotheses;
- successful production continuous/recovered parity through the accepted non-nominal boundary.

All77 custom availability/auto-entry OFF. No later signal, merge or deployment.
Full evidence: mhv612_candidate_fix_evidence.zip.xz (XZ wraps complete original ZIP, roundtrip verified). XZ SHA256d4203d1b92fc1413a97c5073dcda0a13aae7c32c7b2f23e5e7c67287ec5a1a2e;210632 bytes. Original ZIP SHA2563e68cca85ee23a8047ffa6f9046b2540a6be6379e8b6220913349f138318eefb;474259 bytes.


## Follow-up finding — availability propagation, still open
Source review identifies an additional existing defect exposed by the new inner-read path: M09 can freeze after an unavailable inner read, while AdvanceMHVSourceOwners still returns true and callers commit lastClosed/observed. The stale MHV view is blocked by its watermark; no stale readable authority is claimed. However the consumed cursor can suppress same-bar retry. This needs explicit source-availability propagation and staged caller handling, with transient inner-read native RED/GREEN before claiming closure. It is the next same-SIG06 task; no later signal is authorized.
