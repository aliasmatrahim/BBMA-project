# Dashboard Compact Chain Format — 2026-08-27

Status: **LOCKED FOR NEXT DASHBOARD CODE UPDATE**
Scope: `DASH-FIX-01`, `DASH-ENH-01`, `DASH-ENH-02`
Design rule: **simple, minimalistic, compact**.

## Locked row format

```text
PAIR | ST | SETUP | CHAIN | POS
```

Category separator:
- `|` = separator between dashboard categories.

Chain progression separator:
- `>` = progression inside the same canonical signal cycle/chain.

Direction markers:
- `↑` = BUY direction.
- `↓` = SELL direction.

Completion / live-position markers:
- `✓` = setup complete/validated.
- `POS↑` = actual EA-owned BUY position is live.
- `POS↓` = actual EA-owned SELL position is live.
- Do not add separate `RDY` or `LIVE` lifecycle states because `✓` and `POS↑/POS↓` already communicate those facts.

## Pair lifecycle status codes
Use only the compact lifecycle status codes below:
- `IDL` = Idle; no active valid canonical setup cycle.
- `ST` = Started; a new canonical cycle has started.
- `BLD` = Building; the canonical chain is actively progressing.
- `INV` = Invalid; the current canonical cycle/chain has been invalidated and is awaiting lifecycle reset/clear or replacement.

Lifecycle status describes the setup/cycle, not broker execution state.

## Example target display

```text
PAIR    | ST  | SETUP | CHAIN                                  | POS
EURUSD  | BLD | REM✓  | H4:RE↑ > H1:EXT↑ > M15:MHV↑           | POS↑
GBPUSD  | BLD | RRE   | D1:RE↓ > H4:RE↓                       |
USDJPY  | BLD | REE✓  | D1:RE↑ > H4:EXT↑ > H1:EXT↑            |
USDCHF  | IDL | -     | -                                      |
USDCAD  | ST  | REM   | H4:RE↓                                 |
AUDUSD  | BLD | RRE   | D1:RE↑ > H4:RE↑                       |
NZDUSD  | INV | REE   | D1:RE↑ > H4:EXT↑                      |
```

## Dashboard behavior rules
1. Show one compact row per enabled pair.
2. Show only the current canonical cycle/chain; do not mix stale or superseded signals into the row.
3. Raw/internal module states that do not belong to the current valid setup journey must not clutter the dashboard.
4. The chain may grow automatically as canonical components mature, e.g. `H4:RE↑` -> `H4:RE↑ > H1:EXT↑` -> `H4:RE↑ > H1:EXT↑ > M15:MHV↑`.
5. When the setup becomes complete, append `✓` to the setup code instead of creating a separate READY status.
6. When a real EA-owned order opens, populate `POS↑` or `POS↓` instead of creating a separate LIVE status.
7. `DASH-FIX-01` must source POS/live trade state from actual current EA-owned broker-side orders, not stale lifecycle state.
8. `DASH-ENH-01` must keep the displayed chain cycle-aware and prevent cross-cycle/stale signal mixing.
9. `DASH-ENH-02` must automatically start, build, invalidate, clear and replace the displayed chain according to the canonical lifecycle.
10. If a cycle becomes invalid, `INV` may temporarily retain the last relevant chain for observability, then auto-clear/reset to `IDL | - | -` when the lifecycle resets or a new canonical cycle replaces it.
11. Keep the dashboard display-only. It must not alter signal, entry, risk, SL/TP, execution or lifecycle authority.
12. Prefer compact abbreviations and avoid redundant words/columns. The target is immediate readability on an MT4 chart, including when many pairs are enabled.

## Queue linkage
Target all three items for the same next dashboard code update:
- `DASH-FIX-01 — Active Trade Sync`
- `DASH-ENH-01 — Cycle-Aware Signal Chain`
- `DASH-ENH-02 — Auto Chain Lifecycle`

This file is the locked visual/behavior format for those dashboard items unless a later explicit user decision supersedes it.
