# Build 4.86 Structural Lifetime Authority Repair — 2026-09-17

Issue: #173
Branch: `fix/q5-lifetime-173`
Owner baseline: `d1-owner-dev@0d8c8ac71aeb9947d48f89239f46a88c31981182`
Status: **SOURCE / TDD / NATIVE COMPILE / BOUNDED RUNTIME VERIFIED — DRAFT INTEGRATION ONLY**

## Source resolution
`P3_FINAL_DELTA_R1_LIFETIME_SOURCE_RESOLUTION.md` rejects generic fixed-age Strategy-Core death authority for Extreme and Re-Entry Type 2/3/4. Core lifetime remains structural: valid owner state survives until source-owned invalidation, reset, supersession or owner handover.

## Confirmed defect
Current owner still failed the focused guard 4/4:
- M16 used `IsExtremeStateExpired()` / `MaxWaitBars_Extreme`;
- M12 assigned `MaxWaitBars_ReEntry` expiry to Type 2/3/4;
- downstream candidate/component paths rejected expired metadata;
- common structural MA5/MA10 close-side invalidation was not the sole lifetime authority.

## Repair
- Remove fixed-age Extreme checks from M16 validity.
- Keep M08 structural Extreme VOID/supersession authoritative.
- Set Type 2/3/4 legacy expiry metadata to zero.
- Remove generic Re-Entry intrinsic expiry/downstream expiry rejection.
- Retain structural MA5/MA10 close-side invalidation and opposite owner transfer.
- Keep Type 2 confluence-break reset and Type 3/4 precursor/retrace semantics unchanged.
- `MaxWaitBars_Extreme` / `MaxWaitBars_ReEntry` remain legacy diagnostic inputs only.

Build 4.84 identity was superseded before PR creation because #175 already owns Build 4.84. Final unique candidate identity is **4.86**.
## TDD / regression
- Fresh RED on current owner: **4 failed / 0 passed** on the intended lifetime defects.
- Final candidate: **5/5 PASS**, including unique Build 4.86 identity.
- Cross-module direct guards: **13/13 PASS**.
- `git diff --check`: PASS before final staging.

## Native compile
- MetaEditor: **0 errors / 0 warnings**, 765 ms.
- MQ4 SHA-256: `4F5227E98FD223141CD8AF63F61B42639C2BD31610690A348A3A33B3FC807D58`.
- EX4 SHA-256: `8DB1D56B8961D8D10757BA75B03AF203829DFF1A684C3D8EFF211EE508B9C1D5`.
- Compile log: `V486_METAEDITOR_COMPILE_20260917.log`.

## Bounded historical runtime
Tester-only harness changes only symbol/connection/timer infrastructure plus `AgeBars` diagnostics; no M08/M12/M15/M16 strategy semantics are changed.
- Mode 1: 73 Re-Entry owner rows; 26 survive >5 bars; max 15 bars.
- Type 3: 11 rows >5 bars, max 15; Type 4: 15 rows >5 bars, max 10.
- Extreme: 276 owner rows; 169 survive >5 bars; max 20.75 bars across H1/H4.
- Mode 2: same owner survival plus **47 standalone Re-Entry selections older than 5 hours; 47/47 M16 PASS**.
- Legacy Re-Entry/Extreme expiry reason count: 0 in both runs.
- Broker order markers: 0 in both runs.
- Type 2 did not naturally occur in this bounded window; its shared no-TTL start/confirmed path is covered by focused TDD/static proof and is not synthetically fabricated.
## Exact Build 4.86 broker smoke
Isolated `MetaQuotes-Demo` clone used the exact canonical MQ4/EX4 hashes with `ExpertsTrades=false`, zero trade caps and `TradeLockMode=2`.
- broker login / symbol resolution / broker specification: PASS;
- EA initialized successfully;
- D1/NMJE state processing observed;
- `[F7-TELEM] Init=1 Connected=1` observed;
- graceful deinitialization completed;
- no production/primary MT4 restart or trading enablement.

Exact-binary broker smoke proves candidate attribution/initialization, while the bounded tester harness proves the >5-bar lifetime mechanism.

## Boundary
No replacement timer, tuned age threshold, detector change, entry-universe expansion, risk change or execution rule is introduced. #175/#174/#180 remain separate workstreams. Merge/production activation is not included in this repair.
