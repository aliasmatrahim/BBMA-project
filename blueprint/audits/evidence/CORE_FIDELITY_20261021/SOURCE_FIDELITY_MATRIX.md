# Core fidelity traceability — task #292 (incremental, not full coverage)

Owner baseline: `459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.
Retrieval authority: `docs/references/SOURCE_INDEX.md` at this same SHA; CP01 source recovery reused.
The rows below cover the current atomic task only. F1–F6 tooling and 49/49 historical family closure are not the denominator of executable rules.

| ID | Source rule / authority class | Contract → module → exact code | Test case / evidence | Classification and verification |
|---|---|---|---|---|
| A-BB20 | EXPLICIT SOURCE: primary PDF p1, Rule Index p1. ACCEPTED CORE: Core V2 §2, BB20 / deviation2 / Close. | M06 MA Source Contract, Bollinger section → M06 `SMA`, `StandardDeviation`, `CalculateBollinger` | `test_m06_data_validity.py`: complete population-SD control; short19/missing/nonfinite close cases. `m06_red.log` | CONFIRMED BUG: unavailable closes are skipped and divisor reduced; result is not BB20. Portable exact-body behavior VERIFIED; native/live impact NOT TESTED. |
| A-SNAPSHOT | ACCEPTED CORE: same indicator set, closed source data. ENGINEERING MAPPING: period availability, finite positive input/output and internally consistent OHLC required before snapshot validity; these are data-integrity checks, not Oma Ally entry rules. | M06 MA Source Contract; M27 frozen-source ordering; M11 missing-history fail-closed → M06 `GetDataForTimeframe` | Same test: insufficient50, missing input, invalid OHLC, zero/NaN native-output fixture; boundary50 and flat controls | CONFIRMED BUG: `is_valid=true` before history/indicator checks. Terminal API fixtures isolate consumer logic; do not certify native iMA calculations. |
| B-FRESHNESS | ACCEPTED CORE: source-owned structural invalidation; M15 clock, exact closed snapshots. ENGINEERING MAPPING under review: unreadable refresh must not prove owner remains executable. | M12 `UpdateReEntryState`; H4 owner updater → M15 `BuildConfirmedReEntryCandidate` → M16 `IsPersistentReEntryComponentValid` / `ValidateDecisionOwnerSnapshot` | CP01 preliminary trace only. Full decision/preflight reproduction pending. | VERIFICATION REQUIRED. Do not erase structural owners or add TTL on this evidence. |

Scope exclusions: HOLD/source-conflict rules remain non-executable. No indicator period/method, entry signature, expiry, exit, risk, execution or M12N-policy change is authorized by these findings.

CP03 update: A-BB20 and A-SNAPSHOT repaired in Build 5.20 (`V520_M06_COMPLETE_DATA_20261022`). Full-period input checks and post-calculation validity now reject the failing fixtures. Exact-body tests 15/15; complete repository pytest 87/87; native strict compile 0 errors / 0 warnings. See `build520_manifest.json`. Both rows remain **NOT RUNTIME VERIFIED**; no eligible historical Strategy Tester or end-to-end order replay has certified the repair. B-FRESHNESS is unchanged and still pending reproduction.

Atomic repair exit: expected failing probes become green on the smallest source change, complete-data controls remain unchanged, unique build identity, native strict compile and scope regression evidence captured. Qualified Strategy Tester and source-to-runtime validation remain separate mandatory gates; a blocked gate is not PASS.
