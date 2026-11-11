# MT4 tester chart-symbol compatibility — scoped candidate Build 5.94

Classification: CONFIRMED BUG in tester compatibility, not a BBMA rule change.

Build 5.93 actual EA OnInit rejected valid default and changed-input cases with `SYMBOL_UNRESOLVED:GBPUSD`. The separate native probe found GBPUSD in the tester environment (`SymbolsTotal(false)=29`, selected=23, Point=0.00001), while `SymbolSelect(Symbol(),true)` returned false with error 4059. The canonical resolver required that unsupported tester operation even for the existing chart symbol. Native helper fixtures did not establish this real API behavior; the real EA tests exposed it.

Minimum engineering fix: inside canonical `FindActualSymbol`'s existing exact-name branch, return the catalog-confirmed chart symbol when `IsTesting()` is true and its Point is positive. Broker specification checks in LoadPairs remain mandatory. Live symbol selection, non-chart selection, exact-name precedence and ambiguous inferred suffix rejection remain on their existing paths. No separate resolver, detector, signal authority or broker-spec fallback is introduced.

The failing actual Build 5.93 startup cases are the RED evidence. Build 5.94 must separately prove native compile, actual chart resolution, the existing 13 non-chart symbol cases and actual whole-EA startup. These results are recorded in `blueprint/runtime/custom_mtf/compatibility594_evidence.json` and `startup594_evidence.json` once observed; this document alone makes no PASS claim.

Ruling: a tester-only exact-chart adapter is appropriate here because the test engine already supplies that symbol and the broker catalog confirms its exact identity. It cannot select an arbitrary external symbol or weaken suffix ambiguity/specification gates. Cost if wrong: tester-only chart admission could reach downstream broker preflight; no live selection bypass is permitted.

Full auto-entry/custom owner mapping, terminal parameter-change reattachment, open-position recovery, multi-symbol broker execution and profitability remain outside this compatibility proof. No merge or activation is authorized by these results.

## Subsequent native finding and Build 5.95

Build 5.94 resolved the actual chart and passed BrokerSpec/PairID/Magic/InitializeEA checks, but EventSetTimer then failed with 4059 and the overall OnInit returned failure. Startup evidence was corrected to VERIFICATION_REQUIRED; the earlier intermediate-success classifier is not retained as PASS. The verifier now requires the final build-tagged OnInit success log and absence of initialization failure.

Build 5.95 registers/cancels the timer only outside IsTesting. It retains the existing tester OnTick path without claiming timer-housekeeping or trading parity. This is an engineering startup adapter; it introduces no processing clock or new entry authority. Ruling: omit the unsupported tester timer registration to allow startup validation — live registration/failure handling stays intact — timer lifecycle equivalence must be validated separately before any strategy-runtime claim. Actual results and exact source/EX4 hashes: compatibility595_evidence.json and startup595_evidence.json.
