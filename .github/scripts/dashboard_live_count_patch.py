from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4')
CONTRACT = Path('blueprint/contracts/M25_M26_DASHBOARD_INITIALIZATION_CONTRACT.md')

src = SRC.read_text(encoding='utf-8')
if 'P2-DASHCOUNT-01' in src:
    print('DASHBOARD_LIVE_COUNT_ALREADY_APPLIED=PASS')
    raise SystemExit(0)
if 'P2-LOTDIAG-01' not in src:
    raise RuntimeError('expected LOTDIAG baseline missing')

old_dashboard = '''void BuildDashboardSnapshot()\n{\n   g_dashboard_snapshot = "";\n   g_dashboard_snapshot += "=== BBMA EA V4.5.1 D1-09 ===\\n";\n   g_dashboard_snapshot += "Time: " + TimeToString(TimeCurrent()) + "\\n";\n   g_dashboard_snapshot += "Balance: " + DoubleToString(AccountBalance(), 2) + "\\n";\n   g_dashboard_snapshot += "Equity: " + DoubleToString(AccountEquity(), 2) + "\\n";\n   g_dashboard_snapshot += "Trades: " + IntegerToString(g_monitored_count) + "\\n";\n   g_dashboard_snapshot += "Protection Ref: " + DoubleToString(g_protection_reference_equity, 2) + "\\n";'''
new_dashboard = '''int CountDashboardLiveEAOwnedTrades()\n{\n   int count = 0;\n   int total = OrdersTotal();\n   for(int i = 0; i < total; i++)\n   {\n      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;\n\n      int pairIdx = -1;\n      if(IsExactEAOwnedSelectedOrder(pairIdx))\n         count++;\n   }\n   return count;\n}\n\nvoid BuildDashboardSnapshot()\n{\n   // P2-DASHCOUNT-01: broker live-order pool + exact symbol/magic ownership is\n   // the display source of truth. No registry compaction or lifecycle mutation.\n   int liveTradeCount = CountDashboardLiveEAOwnedTrades();\n\n   g_dashboard_snapshot = "";\n   g_dashboard_snapshot += "=== BBMA EA V4.5.1 D1O-07 ===\\n";\n   g_dashboard_snapshot += "Time: " + TimeToString(TimeCurrent()) + "\\n";\n   g_dashboard_snapshot += "Balance: " + DoubleToString(AccountBalance(), 2) + "\\n";\n   g_dashboard_snapshot += "Equity: " + DoubleToString(AccountEquity(), 2) + "\\n";\n   g_dashboard_snapshot += "Trades: " + IntegerToString(liveTradeCount) + "\\n";\n   g_dashboard_snapshot += "Protection Ref: " + DoubleToString(g_protection_reference_equity, 2) + "\\n";'''
if old_dashboard not in src:
    raise RuntimeError('dashboard snapshot anchor missing')
src = src.replace(old_dashboard, new_dashboard, 1)

old_update = '''void UpdateDashboard()\n{\n   if(!ShowDashboard) return;\n   Comment(g_dashboard_snapshot);\n}\n'''
new_update = '''void UpdateDashboard()\n{\n   if(!ShowDashboard) return;\n   Comment(g_dashboard_snapshot);\n}\n\nvoid RefreshDashboardLiveTradeCount()\n{\n   if(!ShowDashboard) return;\n\n   static int lastDisplayedLiveCount = -1;\n   int currentLiveCount = CountDashboardLiveEAOwnedTrades();\n   if(currentLiveCount == lastDisplayedLiveCount) return;\n\n   BuildDashboardSnapshot();\n   UpdateDashboard();\n   g_dashboard_needs_update = false;\n   lastDisplayedLiveCount = currentLiveCount;\n}\n'''
if old_update not in src:
    raise RuntimeError('UpdateDashboard anchor missing')
src = src.replace(old_update, new_update, 1)

old_timer = '''   if(!IsTerminalConnected()) return;\n   OnTickMain();\n}\n\n//+------------------------------------------------------------------+\n//| END OF EXPERT ADVISOR'''
new_timer = '''   if(!IsTerminalConnected()) return;\n   OnTickMain();\n\n   // P2-DASHCOUNT-01: refresh presentation only when live exact-owned count\n   // changes. Timer cadence prevents stale closed-trade rows on the display.\n   RefreshDashboardLiveTradeCount();\n}\n\n//+------------------------------------------------------------------+\n//| END OF EXPERT ADVISOR'''
if old_timer not in src:
    raise RuntimeError('OnTimer tail anchor missing')
src = src.replace(old_timer, new_timer, 1)

for needle in [
    'int CountDashboardLiveEAOwnedTrades()',
    'IsExactEAOwnedSelectedOrder(pairIdx)',
    'int liveTradeCount = CountDashboardLiveEAOwnedTrades();',
    'IntegerToString(liveTradeCount)',
    'void RefreshDashboardLiveTradeCount()',
    'static int lastDisplayedLiveCount = -1;',
    'RefreshDashboardLiveTradeCount();',
    '=== BBMA EA V4.5.1 D1O-07 ==='
]:
    if needle not in src:
        raise RuntimeError('missing dashboard guard: ' + needle)

if 'Trades: " + IntegerToString(g_monitored_count)' in src:
    raise RuntimeError('stale raw monitored count remains in dashboard')

SRC.write_text(src, encoding='utf-8', newline='\n')

contract = CONTRACT.read_text(encoding='utf-8')
old = 'The current dashboard may display signal type, direction, decision state, rejection reason, account balance/equity, monitored-trade count and protection reference as observability only.'
new = '''The current dashboard may display signal type, direction, decision state, rejection reason, account balance/equity, **live exact-owned open-trade count**, and protection reference as observability only.\n\n### P2-DASHCOUNT-01 live-count rule\nThe displayed `Trades` value must not use raw `g_monitored_count`, because the registry may legitimately retain a closed row until a later compaction path. The dashboard scans the current broker `MODE_TRADES` pool and counts only orders accepted by `IsExactEAOwnedSelectedOrder()`: open BUY/SELL orders whose symbol and magic exactly match a configured EA pair owner.\n\nA timer-side display refresh may rebuild the dashboard when this live count changes. That refresh is presentation-only: it must not compact the monitored registry, mutate recovery/lifecycle state, create broker actions, or alter strategy/risk/MM authority.'''
if old in contract:
    contract = contract.replace(old, new, 1)
elif '### P2-DASHCOUNT-01 live-count rule' not in contract:
    raise RuntimeError('M25 count contract anchor missing')
CONTRACT.write_text(contract, encoding='utf-8', newline='\n')

print('DASHBOARD_LIVE_COUNT_PATCH=PASS')
