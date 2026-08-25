# D1 TP-Wajib v4.58 Hosted MT4 Runtime Probe — 2026-08-26

Status: **HOSTED_ENVIRONMENT_UNCLASSIFIED_NO_FATAL_SIGNATURE**

Evidence:
- workflow run: `32909061219`
- job: `97999302151`
- artifact: `9586321060`
- artifact ZIP SHA-256: `fd75858147a299779603f05c25db3aea67cd71f11d2716c923d2e480db2042a8`

Source identity verified by the runner:
- EA blob: `a166ffb23aba5e6b4011a28d9de8896cd00e33a1`
- canonical SHA-256: `ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc`
- build: `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage`
- `#property version "4.58"`

Safety gates during probe:
- `EnableD1TPWLifecycle=false`
- `EnableC044Lifecycle=false`
- Expert trading disabled.

Native environment:
- official MetaTrader 4 build 1478
- native MetaEditor compile: **0 errors / 0 warnings**

Runtime observation:
- MT4 launched successfully in portable mode;
- no fatal runtime signature was detected;
- hosted environment did not provide enough broker/symbol/session evidence to positively prove EA attach/initialization semantics;
- therefore the probe is not promoted to broker-runtime PASS.

This record is startup/environment evidence only. It does not validate D1 TP-Wajib lifecycle close behavior, checkpoint restart, replay, C044 interaction, M20 precedence, order execution, or N2 real closed-outcome evidence.

Authenticated broker/demo MT4 remains the required boundary for those tests.
