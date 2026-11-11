# SIG06 MHV — fixture/profile milestone, 2026-11-11

Status: **PARTIAL / full acceptance HOLD**. Only SIG06 was advanced. SIG07 MLV and Re-Entry remain unstarted.
Base: e3c3af4234071f7c72df52fb78a29e4613bc752d, feat/custom-mtf-v1-20261108, Draft PR303.
Production EA unchanged: Build6.11, LF SHA256 a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb.
No Core, risk, execution, production replay admission or HST file was changed.

## Evidence and classification

| Issue | Impact | Result |
|---|---|---|
| VERIFICATION REQUIRED: installed M30 omits active buckets | The M1-completeness derivation cannot support the selected contiguous replay | Read-only comparison identifies35 omitted buckets; all35 have complete exact M15 pairs, while M1 is incomplete.600 overlapping OHLC rows agree within1e-9. Original HST retained. |
| ENGINEERING IMPROVEMENT: bounded alternate M30 fixture | Permits testing actual M08/M09 engines without repairing history or inventing prices | Test-only CSV adapter from2000 complete M15 pairs. Every pair is t and t+900, closed, ordered, range-valid. Native iMAOnArray implements the same M06 MA modes;100 native-M15 API comparisons per process agree within1e-12. |
| VERIFICATION REQUIRED: source profile attribution | Folder MetaQuotes-Demo is insufficient to identify actual source/session | M15/H1/H4/D1 SHA exactly matches synthetic_ny_close_v3 export. M1/M5512000-record payloads exactly match suffixes of full v3 files, headers identical. Binding proves engineering provenance, not deployment-broker sessions. |
| HOLD-UNRESOLVED: full recovery acceptance | A direct source-engine test cannot certify production replay admission | NY-calendar harness calls actual M08/M09 source engines across declared fixture weekends. Production nominal continuity guard remains unchanged and is not certified by these tests. Original global owner/session and T04B exits remain open. |

The profile BBMA_SYNTHETIC_NY_CLOSE_TEST_V1 explicitly permits isolated tester reference only, maps NY17:00 to synthetic00:00 with IANA DST, and sets canonicalStrategyRule=false/deploymentBrokerCanonical=false.
This corrects earlier unknown-MetaQuotes/server attribution for these exact files. Prior reports remain historical; “native HST” describes the MT4 file/API mechanism and does not imply broker-native data.
Synthetic volume is constant1 and not tick accurate. M30 completeness is complete M15 pairs, not complete ticks or per-minute coverage.

## Native results

| TF / scope | Producer | Fresh consumer | Reloaded source bars | Terminal PIDs |
|---|---:|---:|---:|---|
| M1/M5/M15/H1, prior installed-HST proofs reused | 24 | 112 |96| Prior8 processes, no rerun |
| M30 alternate M15-derived fixture |6/6|28/28|24|8976 /588|
| H4 synthetic NY reference calendar |7/7|29/29|24|4512 /5880|
| D1 synthetic NY reference calendar |7/7|29/29|24|3164 /4572|

Combined:242 restart assertions,168 post-reload bar states,102 fields per state; new M30 MA comparisons200 separately.
H4 selected anchor1777392000 BUY; D1 anchor1761091200 SELL. These integers are synthetic chart epochs.
Each persisted snapshot has2553 unique CSV keys:3 identity keys plus25 states×102 fields.
H4/D1 bridge checks admit Saturday/Sunday synthetic-wall-clock slots only; any weekday omission is rejected. Driver independently checks no actual M15 source row is skipped.12 producer/consumer bridge observations; these are repeated observations, not12 unique boundaries.
All7 original source-HST hashes unchanged. Orders remain absent in every new native case.
New M30 and H4/D1 harnesses compile strict0 errors/0 warnings. This does not claim a fresh production-EA compile or full regression suite.
First NY compile0 errors/1 shadow warning is retained under origin_ny_calendar_v6; renamed test local variable, final v7 strict0/0. No v6 native test ran.
Collector3712 exited0 and verified source/harness/binary/codec/equality/profile/HST/snapshot bindings, snapshots, native summaries and Python syntax.
Archive SHA256 d50ae0d6f0a7854023b5e019a6b76295e9f708a9fb4745cd80ca6fd34ed9d85b;110324 bytes.

## Review and remaining exits

Independent review found no material M30 aggregation/MA adapter defect. It identified the important acceptance boundary: direct AdvanceOrigin source-engine parity does not exercise production ReplayCustomAuxOwnerSource admission. That boundary is retained, not treated as a fix or waived.
Four seeded initial-state stress hypotheses converge at the selected origin; this is not universal proof over all unknown historical states.
No complete seven-TF production-controller, arbitrary epoch reconstruction, broker session, profitability or executable availability claim is made.

Required next:
1. Accepted same-feed historical boundary/session authority suitable for production recovery.
2. Source-proven owner epoch beyond the bounded stress hypotheses.
3. Continuous versus recovered full-owner comparison through production admission across that accepted non-nominal boundary.

Until those original exits pass: SIG06 PARTIAL; T04B/E full recovery HOLD; T04F/T05+ blocked. All77 semantic/custom execution availability and auto-entry OFF. No later signal, merge or deployment.

Evidence: mhv611_fixture_profile_summary_20261111.json, mhv611_fixture_profile_evidence_20261111.zip, source_profile_binding_20261111.json, and mhv611_checkpoint.json.
Primary API reference: https://docs.mql4.com/indicators/imaonarray (series-array semantics and native API). History Center limitations: https://www.metatrader4.com/en/trading-platform/help/service/history_center. Actual provenance comes from byte/hash binding, not those generic documents.
