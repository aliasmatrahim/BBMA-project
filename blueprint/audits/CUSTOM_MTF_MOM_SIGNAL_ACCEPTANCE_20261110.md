# SIG-04 MOM acceptance — 2026-11-10

Status: VERIFIED for bounded canonical predicate, source readiness and affected owner/controller behavior. This is not executable Custom MTF availability or production release acceptance.

Branch feat/custom-mtf-v1-20261108; Draft PR303; tested code0da572057bc009b0108b98745b617041fc06fa18 plus explicit complete-history test fixtures. Build6.10 / V610_MOMENTUM_READINESS_20261110 / MOMENTUM_READINESS_003_20261110. Source LF SHA256 ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae.

## Finding and repair

CONFIRMED BUG → missing required Close9 yielded ready=false but raw/buy=true through partial Bollinger arithmetic; downstream unavailable data could also be interpreted as no Momentum, consume cursors, lose a recovery checkpoint or partially mutate auxiliary owners.

FIX → M10 rejects incomplete/revised inputs before publishing classifications; final-fence failure clears both directions/cache readiness. DetectCSM honors availability. One source-identity adapter validates closed time/Close before affected M09/M11/M12/C044/M27 state and cursor changes. M15 defers without consuming its processing cycle. H4 recovery distinguishes unavailable from proven invalid, preserves unavailable checkpoint lineage, stops at interior unavailable bars and retries through the existing M15 path. The warm-up start excludes only the leading bars lacking the required21-input indicator window. Auxiliary owner advancement commits atomically. C044 retains its existing freeze policy.

The accepted predicate is unchanged: strict closed price outside the relevant outer BB, expanding width and directional Mid/outer BB movement. These slopes/width comparisons are the existing deterministic engineering mapping of vertical/expanding BB. No Open, candle-colour, three-candle body threshold, new indicator, TTL, risk or execution authority is introduced. All77 custom availability cells and auto-entry remain OFF.

## Evidence

- Native valid-data Momentum72/72, including literal flat/equality/expansion/direction and1400 native iBands comparisons.
- Actual full-EA controlled readiness suite167/167. Corrected baseline1 PASS/159 FAIL; retry extension164/1; checkpoint/atomicity review165/2; each observed RED precedes its GREEN.
- All18 native groups pass, including the readiness suite; exact group counts in mom610_final_summary.json. Full EA/current harness compiles strict0 errors/0 warnings. Collector9520 exit0 verifies20 unique source/harness/binary bindings, current source/includes and referenced test headers.
- Actual M27/ProcessPair controller:16 M15 cycles and12224 scalar owner/decision rows per profile. Monitor ON materializes630 combined CSA/CSAK/MOM views over15 frames. OFF/ON and frozen6.09 traces are identical; baseline differences0. Valid decisions0 and order attempts0.
- Six targeted host test functions plus import assertions/py_compile passed; full pytest unavailable and not claimed.
- Older synthetic structural tests that overwrote Data.close without complete matching source history initially failed the new guard. The test-only complete-flat-Close fixture and observer timestamp/history fixture now satisfy the declared dependencies through actual M10. Production readiness was not bypassed. Initial canonical-MHV fixture failure is archived.

Evidence archive mom610_evidence.json.gz includes all native manifests, controller manifest, binding verification and retained RED manifests. Three full traces under controller610 have identical verified hashes; each retains its own case path. mom610_final_summary.json contains their raw/gzip hashes. Collector script is retained for reproducibility.

## Limits and serial exit

GBPUSD engineering history only; M30 is complete-bucket derived OHLC. No authenticated market-session coverage, arbitrary cold-start owner epoch, wall-clock timer, positive entry, broker fill, profitability or live deployment claim. H4 checkpoint unavailable behavior uses controlled source fixtures. C044 uses its shadow replay policy and does not certify terminal persistence. Valid-data trace parity does not exercise the unavailable-input failure; the separate167-case suite does.

No merge/deployment/activation. SIG-01 eCSD, SIG-02 CSA and SIG-03 CSAK remain accepted in their documented bounds. SIG-04 closes only after this evidence publication is verified; next signal SIG-05 Extreme. Session/epoch and integrated T04-F/T05+ gates remain unresolved.
