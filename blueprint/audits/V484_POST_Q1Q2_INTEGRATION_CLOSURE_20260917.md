# Build 4.84 Q5 Standalone Extreme Post-Q1/Q2 Integration Closure

Scope: Issue #175 / PR #182 reconciled onto owner `d1-owner-dev@193735e2079936003e87bfd0db39ba6585757aa3`.

Status: BRANCH-LEVEL VERIFIED / INTEGRATION PENDING.

Integration resolution:
- retained Q2 F7/C044 infrastructure and Q1 NMJE read-only authority from current owner;
- reapplied the exact #175 standalone H1 Extreme semantic delta on top of owner Build 4.83;
- preserved Mode 2 admission only at `EXT_MAT_RETEST_READY` for H1 standalone Extreme;
- preserved M16 exact lifecycle identity revalidation;
- preserved M17 RAW->RETEST structural wick window with exact 3.0-pip project-policy buffer;
- preserved normal Extreme TP-Wajib first opposite MA5/MA10 edge mapping;
- advanced all visible/runtime build identity to 4.84.

Final MQ4 SHA-256: `F8E4497DBCAB27909E23C75FCFC022F11BCF25CCCEE7049B350C40819F775E85`.
Final EX4 SHA-256: `8044EA930F8E3021AD4490BFFB683643D7E8CCE83BF548A39ADDA120E8D95C30`.
Native MetaEditor: 0 errors / 0 warnings, 756 ms.

Regression:
- #175 + Q1 + Q2 focused pytest: 16/16 PASS;
- C044 deterministic model: 145 normal + 85 frozen failure points PASS;
- cross-module direct guards: 13/13 PASS;
- NMJE execution gate/rejection markers absent from source;
- Build 4.84 identity consistency guard covers header/property, build/source tags, `[F7-BUILD]` and visible init string;`r`n- diff hygiene PASS.
Exact-binary broker smoke:
- deployed hashes matched the final candidate exactly;
- broker spec / PairID / Magic / EA init PASS;
- `[F7-BUILD] Build=4.84` and current tags emitted;
- `[F7-TELEM] Init=1 Connected=1`;
- live `[N1-NMJE] REL=BUILDING` observation remained active while legacy NMJE block inputs were true;
- `[NMJE-GATE]`, `OrderSend`, `DEC_EXECUTED` counts = 0;
- graceful deinitialization.

Historical #175 mechanism evidence from the pre-integration candidate remains reusable because the standalone Extreme semantic delta is unchanged: natural EURUSD BUY covered RETEST_READY -> M15 -> M16 -> M17 -> simulated execution, exact RAW->RETEST wick reconstruction, 3.0-pip SL, TP-Wajib and DecisionID dedup.

Residuals intentionally remain:
- natural standalone SELL runtime coverage is not yet observed;
- exact broker-side standalone Extreme `OrderSend` remains pending a genuine demo event;
- therefore this is not a release-readiness or profitability claim.

Primary MT4 was not restarted or modified.
