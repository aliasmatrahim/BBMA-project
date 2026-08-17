# P3 Step 5 — Final MT4 Runtime Closure Checklist

## Purpose
This checklist is the final evidence gate for P3 Step 5 after Fix B and S5C source/compile validation.

Canonical S5C source commit:
`0b57f042c4c90a5a00531c152252c1e53332eb3f`

S5C native MetaEditor compile:
- Workflow run: `32026948381`
- Compile job: `95378287873`
- Result: `0 errors, 0 warnings`
- Marker: `P3_S5C_NATIVE_MT4_COMPILE=PASS`

## Test A — Restart recovery of existing missing-H orders
After deploying/re-attaching the latest S5C build, inspect MT4 Experts immediately after initialization.

For an exact-owned open order with valid Entry/SL/TP geometry and valid live lot but no observable `BBMA|H:` prefix, require exactly one line equivalent to:

`[P3S5][RECOVERY] Ticket=<ticket> Pair=<pair> State=REC_IDENTITY_MISSING_FROZEN Cause=MISSING_EXECUTION_HASH HashFound=N FullMeta=N`

PASS conditions:
- state is `REC_IDENTITY_MISSING_FROZEN`;
- cause is `MISSING_EXECUTION_HASH`;
- order remains present in monitored/risk/portfolio ownership;
- no fabricated hash/tombstone is created.

## Test B — Frozen-state log suppression
Leave the EA running through multiple ticks/timer cycles.

PASS condition:
- recovery diagnostic appears during reconstruction only;
- there is no repeated `corrupted, frozen` or equivalent recovery-freeze log on every cycle.

## Test C — Fresh M22 execution identity persistence
Wait for one genuine validated M22 execution from the latest S5C build. Do not create a manual surrogate order.

Require:

`[P3S5][EXEC_ID] Ticket=<ticket> Pair=<pair> Persist=PASS HashFound=Y HashMatch=Y ExpectedHash=<hash> PersistedHash=<same hash> ... RawComment=<BBMA|H:...>`

PASS conditions:
- `Persist=PASS`;
- `HashFound=Y`;
- `HashMatch=Y`;
- broker-returned comment begins with `BBMA|H:`;
- `TradeInfo.execution_hash` is populated only from the matching broker-returned hash.

If `Persist=FAIL`, stop closure: broker comment persistence remains unresolved.

## Test D — Restart after fresh hashed trade
While the fresh S5C order remains open, restart/re-attach the EA.

PASS conditions:
- recovery observes the execution hash;
- the order does not become `REC_IDENTITY_MISSING_FROZEN` solely due to comment loss;
- no duplicate order is created for the same execution identity.

## Test E — Hard-invalid separation
If a genuine hard-invalid recovery case is naturally available, verify it remains `REC_RECOVERY_INVALID`.

Hard-invalid examples:
- invalid directional Entry/SL/TP geometry;
- non-positive live lot;
- invalid broker lot step.

Do not manufacture or damage a live trade solely to create this test case. Static/source classification plus any naturally observed runtime case may be used as evidence.

## Test F — Emergency-close precedence
A frozen exact-owned trade must remain eligible for M20/M23 emergency portfolio liquidation because emergency-close handling is before recovery freeze.

Do not deliberately force a loss condition on a live account solely to test this. Use safe/demo/runtime evidence when available.

## Evidence to capture
Capture the smallest Experts-log window containing:
1. EA initialization;
2. `[P3S5][RECOVERY]` for existing no-H orders;
3. enough subsequent cycles to prove no log spam;
4. one `[P3S5][EXEC_ID]` from a fresh S5C execution;
5. restart recovery of that fresh order.

## Closure rule
P3 Step 5 may be marked PASS only after Tests A-D are directly evidenced and safety invariants E-F remain satisfied. Until then, status remains:

`IN PROGRESS — SOURCE/COMPILE PASS; LIVE MT4 RUNTIME CLOSURE PENDING`
