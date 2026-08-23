from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
s = SOURCE.read_text(encoding='utf-8')

# Historical dispatcher retained as an idempotent integrity validator only.
# It must not mutate the current canonical EA build.
required = [
    'else if(TradeLockMode == LOCK_SAME_DIRECTION)',
    'g_monitored_trades[i].direction != decision.Direction',
    'if(buyCount > 0 && sellCount > 0)',
    'CONFLICT_DIRECTION_VIOLATION',
    'IsLiveEAOwnedPortfolioTrade(i)'
]
for token in required:
    if token not in s:
        raise SystemExit('pair-lock integrity invariant missing: ' + token)

legacy = 'g_monitored_trades[i].direction == decision.Direction)\n            return false;'
if legacy in s:
    raise SystemExit('legacy reversed SAME_DIRECTION predicate detected')

print('Pair-lock integrity validator PASS; no source mutation required.')
