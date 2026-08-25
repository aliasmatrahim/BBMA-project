# P2 — REJ_INVALID_LOT Diagnostics Audit / Closure

Date: 2026-08-25
Branch: `d1-owner-dev`
Build lineage: `Version 4.5.1 - D1O-07 Canonical LTF Dedup`
Status: **CLOSED / PASS / OBSERVABILITY-ONLY / NATIVE METAEDITOR 0E0W**

## Scope

Improve observability for M21 lot-sizing rejection without changing sizing, risk, admission or broker execution semantics.

The downstream trading rejection remains `REJ_INVALID_LOT`.

## Implementation

Marker: `P2-LOTDIAG-01`.

Added post-failure diagnostics:
- `DiagnoseInvalidLotReason(...)`;
- `PrintInvalidLotDiagnostic(...)`;
- log prefix `[LOT_DIAG][REJ_INVALID_LOT]`.

Approved reason tags include:
- `BROKER_SNAPSHOT_INVALID`;
- `BELOW_MIN`;
- `ABOVE_MAX`;
- `STEP_MISMATCH`;
- `MAXAUTOLOT_BELOW_MIN`;
- `FIXEDLOT_INVALID`;
- additional explanatory tags for invalid decision/payload/MM configuration/SL/risk inputs and unclassified failure.

Diagnostic payload captures frozen values including raw/normalized lot, MinLot, MaxLot, effective maximum lot, LotStep, LotDigits, TickValue, TickSize, Point, SL distance, Entry, SL, Equity, AutoLotPercent, MaxAutoLot, FixedLot and MMMode.

## Hard authority guard

`CalculateLotSize()` remains the sole sizing authority and was deliberately left unchanged.

The materialization gate compared the entire `CalculateLotSize()` block before/after the patch and recorded:

`CALCULATE_LOT_SIZE_SHA256=1da0ca371acc452cea0abd61f753bad6695d0ca225ae06e1985b4bd689c3e770`

Diagnostics run only after the original call has already failed:

`double lot = CalculateLotSize(decision, snapshot, lotValid);`

They do not re-query live account/broker state, normalize a rejected trade into acceptance, change lot, change MM mode, change risk percentage, or replace `REJ_INVALID_LOT` with a new trading decision.

## Materialization evidence

GitHub Actions materialization run: `32822172138`
Job: `97722423292`
Conclusion: **success**

Materialized source/contract commit: `f994222` — `P2: add REJ_INVALID_LOT observability diagnostics`.

## Final combined native compile evidence

The final owner source containing both LOTDIAG and dashboard live-count changes was compiled in official MT4 MetaEditor.

GitHub Actions run: `32823122900`
Job: `97725322914`
Conclusion: **success**

EA SHA-256 compiled:
`2fd43ecda4edee45e641463215be70d1c043b36941906a7507946b606cc3826b`

MetaEditor result:
- errors: **0**;
- warnings: **0**;
- compile elapsed: 120 ms;
- `P2_OBSERVABILITY_NATIVE_METAEDITOR=PASS`.

Artifact:
- name: `p2-observability-native-compile-evidence`;
- artifact ID: `9554031975`;
- artifact digest: `sha256:c95048cb6cd584f84efaaa2e52365c30505e1dacf1c286a0987146157119425d`.

## Verdict

**PASS.** `REJ_INVALID_LOT` is now diagnostically actionable while M21 lot sizing/risk semantics remain unchanged.
