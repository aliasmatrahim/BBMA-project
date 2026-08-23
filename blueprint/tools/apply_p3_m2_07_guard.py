from pathlib import Path

# One-shot M2-07 patch helper; this branch update triggers the verified PR workflow carrier.
p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')
before = s

def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s = s.replace(old, new, 1)

rep('Version 4.5.1 - PATCHED 2.1',
    'Version 4.5.1 - P3-M2-07 OPPOSITE GUARD',
    'header build id')

rep('#property version   "4.51"\n#property strict',
    '#property version   "4.51"\n#property description "P3-M2-07 Cycle Direction Guard"\n#property strict',
    'about build id')

rep('''   if(decision.Pair != pair || pair == "" || magicNumber <= 0 || decision.DecisionID == "")
      return false;
   
   if(TradeLockMode == LOCK_ONE_POSITION)
''','''   if(decision.Pair != pair || pair == "" || magicNumber <= 0 || decision.DecisionID == "")
      return false;

   // P3-M2-07 SOURCE-DERIVED CYCLE DIRECTION GUARD:
   // Multiple distinct same-direction BBMA entries may coexist, but a fresh
   // opposite-direction entry must not create BUY+SELL coexistence on the
   // same EA-owned pair while the earlier opposite position is still live.
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(!IsLiveEAOwnedPortfolioTrade(i)) continue;
      if(g_monitored_trades[i].pair != pair) continue;
      if(g_monitored_trades[i].direction != decision.Direction)
         return false;
   }
   
   if(TradeLockMode == LOCK_ONE_POSITION)
''','hard opposite guard')

if s == before:
    raise SystemExit('No source changes produced')
if s.count('{') != s.count('}'):
    raise SystemExit('Brace imbalance after patch')

for anchor in [
    'bool IsSignalAllowed(BBMA_Decision &decision, string pair, int magicNumber)',
    'int SendOrderWithRetry(',
    'void ProcessEntry(',
    'void PriorityEngine_Atomic(',
    'void InvalidationEngine_Atomic('
]:
    if before.count(anchor) != 1 or s.count(anchor) != 1:
        raise SystemExit('Critical anchor changed: ' + anchor)

p.write_text(s, encoding='utf-8')

Path('blueprint/P3_M2_07_CYCLE_DIRECTION_GUARD_PATCH.md').write_text(
    '# P3-M2-07 Cycle Direction Guard Patch\n\n'
    'Status: PATCH APPLIED; NATIVE METAEDITOR 0E0W REQUIRED BEFORE MERGE.\n\n'
    'Build identifier: `P3-M2-07 Cycle Direction Guard`.\n\n'
    'Behavior: blocks a fresh opposite-direction EA entry when an EA-owned live position already exists on the same pair. Distinct same-direction BBMA add-on decisions remain allowed subject to duplicate, risk, portfolio, and MaxTradePerPair controls. No forced close, scoring, relative-quality ranking, SL/TP change, or BBMA detector change is introduced.\n',
    encoding='utf-8'
)

# Remove this one-shot patch helper from the final branch diff.
Path(__file__).unlink()
