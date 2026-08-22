from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
CONTRACT = Path('blueprint/contracts/M22_ORDER_EXECUTION_CONTRACT.md')
AUDIT = Path('blueprint/P3_OPPOSITE_DIRECTION_PAIR_INTEGRITY_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')

old_comment = 'input int      TradeLockMode                      = 0;          // TradeLockMode: 0=OFF, 1=SAME_DIRECTION, 2=ONE_POSITION'
new_comment = 'input int      TradeLockMode                      = 0;          // TradeLockMode: 0=OFF, 1=SAME_DIRECTION_ONLY, 2=ONE_POSITION'
if s.count(old_comment) != 1:
    raise SystemExit('TradeLock input comment anchor missing')
s = s.replace(old_comment, new_comment, 1)

old = '''   else if(TradeLockMode == LOCK_SAME_DIRECTION)\n   {\n      for(int i = 0; i < g_monitored_count; i++)\n      {\n         if(!IsLiveEAOwnedPortfolioTrade(i)) continue;\n         if(g_monitored_trades[i].pair == pair &&\n            g_monitored_trades[i].direction == decision.Direction)\n            return false;\n      }\n   }\n'''
new = '''   else if(TradeLockMode == LOCK_SAME_DIRECTION)\n   {\n      // Pair-direction lock: once this EA already has a live position on the\n      // pair, additional positions may only follow that same direction.\n      // The previous comparison was reversed: it blocked same-direction adds\n      // and allowed BUY+SELL coexistence, contradicting SAME_DIRECTION mode.\n      for(int i = 0; i < g_monitored_count; i++)\n      {\n         if(!IsLiveEAOwnedPortfolioTrade(i)) continue;\n         if(g_monitored_trades[i].pair == pair &&\n            g_monitored_trades[i].direction != decision.Direction)\n            return false;\n      }\n   }\n'''
if s.count(old) != 1:
    raise SystemExit(f'LOCK_SAME_DIRECTION implementation anchor expected once, found {s.count(old)}')
s = s.replace(old, new, 1)

# Static invariants.
if 'g_monitored_trades[i].direction != decision.Direction' not in s:
    raise SystemExit('opposite direction pair lock not installed')
if 'g_monitored_trades[i].direction == decision.Direction)\n            return false;' in s:
    raise SystemExit('legacy reversed SAME_DIRECTION lock still present')
if 'if(buyCount > 0 && sellCount > 0)' not in s or 'CONFLICT_DIRECTION_VIOLATION' not in s:
    raise SystemExit('M15 same-scan opposite candidate conflict guard missing')
if 'IsLiveEAOwnedPortfolioTrade(i)' not in s:
    raise SystemExit('EA-owned live trade filter missing')

SOURCE.write_text(s, encoding='utf-8')

contract = CONTRACT.read_text(encoding='utf-8')
old_contract = '''## Trade lock\nTrade-lock checks must consider only live EA-owned positions. Stale monitored entries or foreign/manual orders cannot create an M22 trade-lock rejection.\n'''
new_contract = '''## Trade lock\nTrade-lock checks must consider only live EA-owned positions. Stale monitored entries or foreign/manual orders cannot create an M22 trade-lock rejection.\n\nMode semantics are explicit:\n- `LOCK_OFF` / `TradeLockMode=0`: trade-lock itself imposes no pair-direction restriction; normal portfolio/strategy gates still apply.\n- `LOCK_SAME_DIRECTION` / `TradeLockMode=1`: if this EA already has a live position on the pair, a new position is allowed only in the **same direction**; an opposite BUY/SELL coexistence on that pair is rejected with `REJ_TRADE_LOCK`. Multiple same-direction positions remain subject to `MaxTradePerPair` and other portfolio limits.\n- `LOCK_ONE_POSITION` / `TradeLockMode=2`: any existing live EA-owned position on the pair blocks another position on that pair.\n\nThis is an EA execution-policy lock. It does not rewrite BBMA cycle direction. A later source-valid opposite cycle may become the strategy owner, but under mode 1 its new opposite order must wait until the old opposite live position is no longer open.\n'''
if old_contract not in contract:
    raise SystemExit('M22 trade-lock contract anchor missing')
contract = contract.replace(old_contract, new_contract, 1)
CONTRACT.write_text(contract, encoding='utf-8')

AUDIT.write_text('''# P3 — Opposite-Direction / Same-Pair Cycle Integrity Audit + TradeLock Fix\n\nDate: 2026-08-22\nBranch: `blueprint-dev`\nStatus: **BUG CONFIRMED / FIX IMPLEMENTED / STATIC REGRESSION PASS — METAEDITOR + RUNTIME TRACE PENDING**\n\n## Trigger\nRuntime observation showed BUY and SELL positions coexisting on one pair while `TradeLockMode=1`.\n\n## Static audit\n### Strategy decision layer\nM15 already fails closed when eligible BUY and SELL candidates coexist in the **same atomic scan**: it creates `CONFLICT_DIRECTION_VIOLATION` rather than choosing an invented winner. Therefore the observed coexistence is not explained by same-scan M15 candidate selection.\n\nAcross later candles/cycles, a source-valid opposite BBMA cycle may legitimately become the new strategy owner while an older broker position is still open. Whether a new opposite order may coexist is therefore an **execution-policy** question owned by TradeLock, not a reason to corrupt the BBMA cycle state.\n\n### Confirmed implementation defect\n`LOCK_SAME_DIRECTION` previously rejected an existing trade when:\n`existing.direction == decision.Direction`.\n\nThat behavior did the opposite of the mode name: it blocked same-direction additions while allowing an opposite position on the same pair. This directly explains BUY+SELL coexistence under mode 1.\n\n## Fix\nFor `TradeLockMode=1`, M22 now rejects when:\n`existing.direction != decision.Direction`.\n\nResult:\n- same-direction additions are permitted, subject to `MaxTradePerPair` and all other gates;\n- opposite-direction coexistence for the same EA/pair is blocked;\n- mode 2 continues to block any second position on the pair;\n- mode 0 remains unrestricted by TradeLock.\n\nOnly live EA-owned monitored positions participate, preserving the locked M22 ownership contract.\n\n## Boundary\nNo BBMA signal, direction, owner handover, F1-F6 lifecycle, EntryMode signature, SL/TP or risk calculation was changed. A valid opposite cycle may still become strategy-authoritative; mode 1 simply prevents its broker order from hedging against an older still-open EA position.\n\n## Static regression\n- M15 same-scan BUY/SELL conflict guard remains present;\n- `LOCK_SAME_DIRECTION` now checks `existing.direction != decision.Direction`;\n- legacy reversed comparison is absent;\n- `LOCK_ONE_POSITION` behavior is unchanged;\n- only live EA-owned positions are considered.\n\n## Remaining verification\n1. Native MetaEditor: **0 errors / 0 warnings**.\n2. Runtime mode 1: BUY open + new BUY valid -> may pass TradeLock (subject to other gates).\n3. Runtime mode 1: BUY open + new SELL valid -> `REJ_TRADE_LOCK`.\n4. Runtime mode 2: any existing pair trade -> `REJ_TRADE_LOCK`.\n5. Runtime mode 0: opposite coexistence is not blocked by TradeLock itself.\n''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
old_q = '''### P1 — Opposite-direction / same-pair cycle integrity\nPriority: HIGH\nStatus: QUEUED; dependency/overlap with P3-M1\nProblem statement:\n- runtime observation can show BUY and SELL positions on the same pair;\n- determine whether this is a valid cycle transition with an older position still open, or opposite-direction leakage from one active authoritative cycle.\nAudit path:\n`M13 -> M14 -> M15 -> M16 -> M20/M22`\nEvidence fields:\n`Pair`, `Direction`, `CycleStartTime`, `DecisionID`, `SequenceHash`, decision state, cycle state, existing position direction.\nExpected invariant to verify: one active authoritative BBMA cycle per pair must not simultaneously authorize contradictory directions unless an explicit, source-backed cycle transition has occurred.\n'''
new_q = '''### P1 — Opposite-direction / same-pair cycle integrity\nPriority: HIGH\nStatus: **BUG CONFIRMED / FIX IMPLEMENTED / STATIC REGRESSION PASS — METAEDITOR + RUNTIME TRACE PENDING**\nAudit record: `blueprint/P3_OPPOSITE_DIRECTION_PAIR_INTEGRITY_AUDIT.md`\nFinding: M15 already rejects contradictory eligible BUY/SELL candidates in one atomic scan. The observed BUY+SELL coexistence under `TradeLockMode=1` came from a reversed M22 lock predicate: mode 1 blocked same-direction adds and allowed opposite-direction orders.\nFix: `LOCK_SAME_DIRECTION` now means same-direction-only coexistence on the pair; an existing live EA-owned opposite direction rejects the new order with `REJ_TRADE_LOCK`. Mode 0 and mode 2 semantics remain unchanged.\nNext action: native compile + focused TradeLock runtime trace; proceed to sequential cumulative risk-budget admission audit.\n'''
if old_q not in q:
    raise SystemExit('opposite-direction queue block not found')
q = q.replace(old_q, new_q, 1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
overlay = '''\n\n# 2026-08-22 Opposite-Direction Pair Integrity Overlay\n- **TradeLockMode=1 opposite-direction bug confirmed and fixed; static regression PASS.**\n- M15 already blocks simultaneous contradictory eligible directions in one scan.\n- M22 `LOCK_SAME_DIRECTION` was reversed; it now allows same-direction adds and blocks opposite-direction coexistence for the same EA/pair.\n- Audit: `blueprint/P3_OPPOSITE_DIRECTION_PAIR_INTEGRITY_AUDIT.md`.\n- Native MetaEditor/runtime verification remains pending.\n- **Next engineering gate: sequential cumulative risk-budget admission audit.**\n'''
if '# 2026-08-22 Opposite-Direction Pair Integrity Overlay' not in c:
    c += overlay
CURRENT.write_text(c, encoding='utf-8')
