# P3 Step 1 — Runtime Initialization & Startup Validation

Status: READY FOR RUNTIME TEST

## Objective
Validate that the P2-closed canonical EA starts cleanly in MT4 and reaches a stable operational state before strategy processing begins.

## Runtime scope
1. Attach the latest compiled EA to one chart.
2. Confirm `OnInit()` / `InitializeEA()` completes successfully.
3. Confirm all configured pairs are resolved to broker `actual_symbol` values and broker specs validate.
4. Confirm PairID and magic-number validation passes.
5. Confirm protection reference equity initializes to current account equity and is positive.
6. Confirm execution history rebuild and existing-order recovery complete without ownership/recovery errors.
7. Confirm the EA reaches `g_is_initialized=true` and logs successful initialization.
8. Confirm the first valid M15 closed-candle cycle can reach `OnTickMain()` / `ProcessPair()` without startup-state errors.

## Current static startup path
`InitializeEA()` enters a non-operational state first, resets transient risk cache, initializes broker information, loads/resolves pairs, validates PairID/magic ownership, resets histories/registry, establishes the equity protection baseline, rebuilds execution history, recovers existing orders, clears the in-memory emergency latch, then sets `g_is_initialized=true`.

## Test configuration
Use the current production candidate inputs initially. For visibility during P3 S1 set `DebugLevel=4` (FULL) temporarily. Do not change BBMA logic inputs for this test.

## Evidence required from MT4
Capture the `Experts` or `Journal` output from the moment the EA is attached until initialization settles. A screenshot is acceptable if all startup lines are visible; copied log text is better.

Minimum evidence to inspect:
- no `INIT_FAILED` / `INIT_PARAMETERS_INCORRECT` result;
- no `No valid pairs loaded`;
- no PairID or magic collision;
- no unresolved symbol / invalid broker specification errors for intended pairs;
- successful initialization line with expected pair count;
- no repeated startup loop / repeated recovery storm;
- if existing EA-owned trades are present, recovery does not report unexpected ownership or geometry corruption.

## PASS criteria
P3 S1 passes only when runtime evidence shows clean initialization and a stable initialized state. Compile 0E/0W alone is not sufficient.

## Failure handling
Any runtime startup error becomes P3 S1 Fix A/B etc. A code change is made only for a reproducible defect; broker/history/data availability problems are recorded separately and are not automatically treated as EA logic defects.