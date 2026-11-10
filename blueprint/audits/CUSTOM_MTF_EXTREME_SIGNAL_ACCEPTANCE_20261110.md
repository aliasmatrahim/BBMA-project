# SIG-05 Extreme acceptance — 2026-11-10

Status: VERIFIED in bounded canonical RAW/maturity/source-readiness, affected handover and read-only projection scope. Custom execution availability, integrated T04 and deployment remain gated.

Branch feat/custom-mtf-v1-20261108; Draft PR303; tested codea4455117d62cd5fc34087416a9d9940c68afe9ac. Build6.11 / V611_EXTREME_SOURCE_READINESS_20261110 / EXTREME_SOURCE_READINESS_003_20261110. Source LF SHA256 a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb.

## Accepted meaning and source routing

SOURCE_INDEX -> accepted Core section5 -> Finale master/V04/V05 rules -> PDF-derived index -> F2 maturity, residual-HOLD closure, bounded repeated-Extreme, normal D1-TPW and standalone H1 execution-policy decisions -> M08/current source. Original cited source windows: primary PDF5–6; V04 27:23–31:55,34:56–38:26,40:28–42:42; V05 07:05–08:22,10:46–14:37,16:41–18:02. Historical broad HOLD/raw-only wording is superseded by the accepted later decisions; no new source rule is inferred from it.

RAW SELL requires MA5High or MA10High strictly above TopBB; RAW BUY requires MA5Low or MA10Low strictly below LowBB. Touch/equality is insufficient. RAW is not an executable component. Relevant outside-close or accepted directional Momentum voids before promotion. A later same-TF closed reversal-direction candle confirms component maturity; a later retest phase freezes the completed reversal-body anchor, and the first valid body-anchor or relevant MA5 interaction completes standalone retest maturity. No generic TTL, colour-flip, named pattern, fixed-N delay, dual-touch or altered combination signature.

Open remains necessary for reversal direction and body anchors; the user's Close-only CSA/CSAK decision does not remove it here. Exact reversal/anchor/retest formulas are accepted deterministic project mappings, not verbatim founder formulas. Normal TPW and separate approved H1 standalone execution policy remain unchanged; no execution expansion or repeated-Extreme/D1 exception is activated.

## Confirmed issue -> impact -> repair

CONFIRMED BUG: M08 duplicated Momentum arithmetic. With missing required Close9, canonical M10 returned unavailable while M08 returned Momentum=true and directly voided an owner. Native7TF RED:8 PASS/14 FAIL,0E0W. This is an actual M08 boundary proof, not a demonstrated broker/ProcessPair escape.

FIX: canonical M10 now supplies Momentum. ReadExtremeLifecycleInvalidation returns availability separately from its Boolean result. UpdateExtremeLifecycle performs that read once before direction/TF reset or owner mutation and reuses the proven invalidation result at both promotion sites.

CONFIRMED BUG: the affected M09 Extreme-supersession caller used a Boolean wrapper that mapped unavailable to false. Native28 direct handover cases plus7 actual M09 second-read revision cases failed. The revision begins after the first complete162-Close read, so it is not an initial-read failure.

FIX: TryAdvanceMHVSupersessionCandidate propagates sourceAvailable; all3 caller branches defer before candidate/parent/cursor changes. No new MHV detector or lifecycle semantics are created.

## Verification

- Current source/readiness/handover141/141; initial22/22 repair and retained expanded106/35 RED precede GREEN.
- Current RAW/reversal/retest/void/supersession/no-TTL/identity plus real-history suite716/716, including140 source-bar samples over7TF.
- Frozen6.10 runs the same716 valid lifecycle/history assertions successfully; changes target unavailable inputs.
-19 existing specialized native groups pass, including owner-projection10/10 and prior Momentum readiness167/167; with the2 new suites,21 current native groups. Full EA/current harnesses strict0 errors/0 warnings.
- Actual M15-owned controller:16 cycles,12224 scalar owner/decision rows per profile. OFF/ON/frozen6.10 exact parity; old/new differences0. ON observes630 combined CSA/CSAK/MOM views plus180 Extreme views over15 frames. Extreme views cover approved monitor TFs excluding M1 and remain non-executable. No valid decisions/order attempts.
- Final collector verifies23 current source/harness/binary bindings plus the separate frozen-baseline harness binding, all referenced source/test headers and3 complete traces. Source and compile identities are bound in ext611_final_summary.json / ext611_evidence.json.gz.
- Three targeted host functions and runner py_compile PASS;16 protected canonical helper/direction/Momentum functions unchanged. No full-pytest claim.
- Initial history-harness295/141 failure was a missing test processing clock; g_processing_time=TimeCurrent() corrected the fixture. Structural294 checks already passed. That RED is retained; no production rule was weakened.
- Independent review found no additional confirmed defect in the scoped M08 update, identified the handover availability window, and required summary-based PASS. The window was reproduced/fixed; runners assert failed=0 and exact716/history140 or141 counts rather than INIT_SUCCEEDED alone.

## Bounds and exit

GBPUSD engineering history; M30 is complete-bucket derived OHLC. Synthetic structural/source fault fixtures do not certify natural formation, authenticated session continuity, arbitrary restart epoch, live timer, positive entry or broker execution. No standalone SL/TP runtime revalidation or profitability claim. Existing session/epoch HOLD remains; all77 custom semantic/executable availability cells and auto-entry OFF. No merge/deployment.

SIG-05 closes only after final evidence publication is verified. Then SIG-06 MHV is the sole next signal; MLV remains an alias of the same M09 engine, not an independent detector.
