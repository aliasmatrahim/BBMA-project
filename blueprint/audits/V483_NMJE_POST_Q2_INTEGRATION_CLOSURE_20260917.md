# Build 4.83 NMJE Post-Q2 Integration Closure

Scope: Issue #141 / PR #142 after Q2 Build 4.82 merged to `d1-owner-dev` as `30ac09675734da7bf4a23dae6b12faec8138f506`.

Classification: CONFIRMED AUTHORITY VIOLATION -> repaired on scoped feature branch. NMJE remains observation/read-only and cannot create, reject, rank, or execute.

Integration resolution:
- current owner Build 4.82 retained as the source base;
- removed `NMJE_PassExecutionGate` and `REJ_NMJE_RELATION` preflight rejection authority;
- preserved N1/N2/N3 observation telemetry;
- legacy `BlockNMJEConflict` / `BlockNMJEBuilding` inputs remain compatibility-only and inactive;
- Build identity advanced to 4.83, including `[F7-BUILD]`, build/source tags, and visible initialization log;
- Q2 F7 exact-ticket and C044 generation-atomic logic retained.

Final source SHA-256: `4AB7AA3D13AAE1B2D02BF44F7449E6F7390DFA4C5A4C2D47FFC51EBEE9C60894`.
Final EX4 SHA-256: `3F80DED35FAF24156F1FBDCF251F89C7F679AE6541B3D179EFCDE36B907DFF95`.
Native MetaEditor: 0 errors / 0 warnings, 751 ms.

Final runtime used the exact hashes above in the isolated `MT4_NMJE_141_Demo` clone with trading disabled and zero trade caps.
Runtime evidence:
- `[F7-BUILD] Build=4.83` emitted before ordinary initialization telemetry;
- broker spec / PairID / Magic / EA init passed;
- `N1-NMJE REL=BUILDING` observed while both legacy block inputs were `true`;
- `[F7-TELEM] Init=1 Connected=1`;
- `[NMJE-GATE]` rows = 0;
- `OrderSend` rows = 0;
- `DEC_EXECUTED` rows = 0;
- graceful deinitialization and terminal shutdown.

Regression boundary:
- Q1 authority tests cover removal of execution rejection and preservation of observation telemetry;
- Q2 F7 guard is integration-safe and no longer hard-codes historical Build 4.82 or the removed NMJE gate as a section boundary;
- C044 deterministic failure model and current cross-module guards remain required in the final completion gate.

Primary MT4 was not restarted or modified. This record does not claim production activation or profitability.
Runtime note: the first launch of the final bytes hit a transient MT4 EventSetTimer(1) failure with error 0 and INIT_FAILED; after clean shutdown, one bounded retry with the exact same MQ4/EX4 hashes passed timer/init, N1 observation, connected heartbeat and graceful shutdown. No code change was made for this environment-only transient timer failure.
