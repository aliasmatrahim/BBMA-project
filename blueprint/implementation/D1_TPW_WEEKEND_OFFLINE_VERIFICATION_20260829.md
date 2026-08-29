# D1TPW Weekend Offline Verification — 2026-08-29

## Boundary

Market-closed work used deterministic models and read-only broker-cached
history. Production build 4.71 was not activated. D1TPW and C044 stayed `OFF`.

Native MT4 Strategy Tester was intentionally not used: the installed terminal
contains only H4 `.hst` files and no complete D1/H1/M15/M5 tester cache. Running
the multi-timeframe EA against that incomplete cache would create misleading
evidence. The offline harness instead aggregates the broker H4 cache to D1 and
tests only the D1TPW lifecycle predicate/cursor contract; it is not a strategy-
performance or entry-quality backtest.

## Model evidence

- Checkpoint restart model: PASS
  - all 11 payload-only torn-write prefixes rejected before version commit;
  - wrong pair, cycle, execution, open-time, magic, version, cursor and
    impossible frozen-plus-latched states rejected;
  - five repeated restarts preserved the exact committed state;
  - same-pair tickets could not cross-load execution identity.
- M23 close-idempotency model: PASS across 9 scenarios:
  - first close success;
  - repeated call after close;
  - retryable failure followed by success;
  - restart after durable latch;
  - already-closed order cleanup;
  - unmanaged, frozen, unlatched, invalid-candle and identity-mismatch blocks.
- Synthetic historical replay firewall: PASS.

## Broker-cache historical replay

All four files are MT4 HST v401, period H4, range 2009-12-21 through
2021-05-06, with 12,077 H4 records aggregated to 2,225 D1 days per pair.

| Pair | SHA-256 | Trajectories | Completions | Restart checks | Max latency |
|---|---|---:|---:|---:|---:|
| EURUSD | `e780f8f18dcd3b23ac2202985cd8d097db8e4c12c7b58b57060372f6520e719c` | 4,430 | 4,430 | 11,339 | 22 days |
| GBPUSD | `824fb1d0290ec42af4df54a3f143ba9c4eacb91c907c94496d43426e2775c3f4` | 4,430 | 4,428 | 11,214 | 25 days |
| USDCHF | `e2571184da780d7e76c42ae0fc06a8699d57934746cd778355902922947259c4` | 4,430 | 4,429 | 11,703 | 24 days |
| USDJPY | `e4bbf16921dbd839428544d2d6e6d4f13f7bf3edd33576e7aae734181eaab931` | 4,430 | 4,430 | 11,609 | 22 days |
| **Total** | — | **17,720** | **17,717** | **45,865** | **25 days** |

Every restart check compared a resumed closed-D1 cursor with uninterrupted
forward replay and required the exact same first completion candle.

## Remaining manual evidence

Only broker/demo evidence remains: live tick scheduling, current spread/freeze
levels, durable terminal restart with a real demo ticket, broker `OrderClose`,
and post-close checkpoint cleanup. See the Monday demo checklist. No activation
is authorized by this weekend record.

