# Custom MTF inputs — configuration milestone Build 5.93

| Input | Function |
| --- | --- |
| `CustomTF_M1` … `CustomTF_D1` | Enable selection of components from that TF. |
| `CustomSignals_M1` … `CustomSignals_D1` | Comma-separated enabled shortforms for that TF; empty means none. Example: `MOM, RE`. |
| `Custom1_Enable` … `Custom5_Enable` | Enable the corresponding slot; defaults OFF. |
| `CustomN_Context`, `CustomN_Trigger` | Required formula fields for an enabled slot; at most seven atoms across both. |
| `CustomSymbolMode` | `CUSTOM_CHART_ONLY`, `CUSTOM_MARKET_WATCH` or `CUSTOM_LIST`. |
| `CustomSymbolList` | Primary list when mode is CUSTOM_LIST. Exact broker names may be used. |
| `Custom1_Symbols` … `Custom5_Symbols` | `ALL` of primary universe or a comma-separated subset. |

Example symbol configuration: mode CUSTOM_LIST, primary list `XAUUSD,GBPUSD,EURUSD`; slot 1 `ALL`, slot 2 `XAUUSD`, slot 3 `GBPUSD,EURUSD`. ALL does not expand to every broker symbol. MARKET_WATCH is frozen on initialization; reinitialize to refresh. Unknown, ambiguous or out-of-universe names are rejected. Exact broker names select a particular suffix/prefix variant; inferred suffix matching must be unique.

Formula examples remain `D1:RE AND H4:RE` for Context and `M1:MOM OR M5:MOM` for Trigger. These are syntax examples, not active trading presets. All semantic availability cells remain closed in this build, so an enabled formula is rejected as unavailable until its owner mapping is connected and validated.

Parsed configuration and resolved symbols contribute to an exact payload. A diagnostic hash reuses the existing hash helper; input formatting alone does not create a new signal event. No physical event dedup, custom auto-entry, custom PairState allocation or multi-symbol broker execution is activated by these inputs yet. Canonical PairList remains separate at this milestone. Full startup/recovery evidence is recorded independently from pure helper test results.
