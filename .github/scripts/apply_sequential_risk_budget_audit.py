from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/P3_SEQUENTIAL_RISK_BUDGET_ADMISSION_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')

required = {
    'cumulative risk function': 'double CalculateTotalRisk(string pair, double newLot, double newEntry, double newSL,',
    'existing trade loop': 'for(int i = 0; i < g_monitored_count; i++)',
    'existing risk sum': 'totalRisk += existingRisk;',
    'prospective new risk': 'double newRisk = CalculateTradeRiskMoney(pair, newLot, newEntry, newSL);',
    'new risk sum': 'totalRisk += newRisk;',
    'equity percentage limit': 'if(totalRisk / equity * 100.0 > MaxTotalRiskPercent)',
    'risk gate call': 'RiskStatus riskStatus = CheckRiskBeforeTrade(decision, snapshot, lot);',
    'registry add': 'AddToMonitoredTrades(info);',
    'sequential pair loop': 'for(int i = 0; i < g_pair_count; i++)',
    'scan serialization': 'if(g_is_scanning) return;',
    'scan latch': 'g_is_scanning = true;',
    'scan unlatch': 'g_is_scanning = false;',
}
missing = [name for name, token in required.items() if token not in s]
if missing:
    raise SystemExit('Sequential-risk invariant(s) missing: ' + ', '.join(missing))

# Ordering checks: risk must be checked before ProcessEntry, and successful
# registration must happen in the executor before the next pair can be scanned.
pre = s.find('RiskStatus riskStatus = CheckRiskBeforeTrade(decision, snapshot, lot);')
proc = s.find('ProcessEntry(decision, pair, snapshot, lot);', pre)
if pre < 0 or proc < 0 or pre >= proc:
    raise SystemExit('risk-before-execution ordering invalid')

add = s.find('AddToMonitoredTrades(info);')
mark = s.find('MarkDecisionExecuted(decision.DecisionID, ticket);', add)
if add < 0 or mark < 0 or add >= mark:
    raise SystemExit('confirmed execution is not registered before decision completion')

AUDIT.write_text('''# P3 — Sequential Cumulative Risk-Budget Admission Audit\n\nDate: 2026-08-22\nBranch: `blueprint-dev`\nStatus: **STATIC PASS — NO CODE FIX REQUIRED; METAEDITOR/RUNTIME MULTI-DECISION TRACE PENDING**\n\n## Question\nWhen several valid decisions are processed close together, does each newly executed trade consume the portfolio risk budget before the next decision is admitted?\n\n## Static result\n**PASS.** The current execution architecture is sequential and prospective:\n\n1. `OnTickMain()` serializes strategy scanning with `g_is_scanning` and iterates pairs one at a time.\n2. Each validated decision obtains its final lot before `CheckRiskBeforeTrade()`.\n3. `CalculateTotalRisk()` sums risk from the existing monitored live EA portfolio and then adds the proposed trade risk (`newRisk`).\n4. The prospective total is compared against `MaxTotalRiskPercent` using current equity.\n5. Only an allowed decision reaches `ProcessEntry()`.\n6. After a broker-confirmed execution, M22 immediately calls `AddToMonitoredTrades(info)` before marking the decision execution complete.\n7. Therefore the next pair processed in the same serialized scan sees the newly executed position in `g_monitored_count`, so its prospective risk calculation includes that consumed budget.\n\n## Failure behavior\nIf existing live-trade risk cannot be resolved safely, the risk calculation fails closed rather than silently treating unknown risk as zero. A rejected/failed order is not added as executed portfolio risk. Ambiguous execution remains governed by M22/M24 idempotency/recovery rules.\n\n## No fix required\nNo static race or stale-budget defect was found in the current single-threaded scan/admission path. Adding a separate reservation ledger would duplicate the already-sequential execution model and is not justified by current evidence.\n\n## Remaining runtime verification\nRun a controlled case where two or more pairs generate valid decisions in one scan window and capture:\n- equity and `MaxTotalRiskPercent`;\n- existing risk before decision A;\n- A proposed/final risk and execution result;\n- existing risk observed by decision B after A executes;\n- B prospective total and admit/reject result.\n\nExpected: if A consumes enough budget, B must reject with `REJ_TOTAL_RISK`; if A fails/does not execute, B must not reserve phantom risk.\n''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
old = '''### P1 — Sequential risk-budget admission\nPriority: HIGH\nStatus: QUEUED\nPurpose:\n- confirm that when multiple valid decisions compete, higher-authority/selected decision consumes prospective risk budget first;\n'''
if old in q:
    new = '''### P1 — Sequential risk-budget admission\nPriority: HIGH\nStatus: **STATIC PASS — NO CODE FIX REQUIRED; RUNTIME MULTI-DECISION TRACE PENDING**\nAudit record: `blueprint/P3_SEQUENTIAL_RISK_BUDGET_ADMISSION_AUDIT.md`\nPurpose:\n- confirm that when multiple valid decisions compete, higher-authority/selected decision consumes prospective risk budget first;\n'''
    q = q.replace(old, new, 1)
else:
    # tolerate queue wording expansion while still recording authoritative result
    marker = '### P1 — Sequential risk-budget admission\n'
    if marker not in q:
        raise SystemExit('sequential risk queue marker missing')
    q = q.replace(marker, marker + 'Status overlay: **STATIC PASS — NO CODE FIX REQUIRED; RUNTIME MULTI-DECISION TRACE PENDING**\nAudit record: `blueprint/P3_SEQUENTIAL_RISK_BUDGET_ADMISSION_AUDIT.md`\n', 1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
overlay = '''\n\n# 2026-08-22 Sequential Risk-Budget Admission Overlay\n- **Sequential cumulative risk-budget static audit: PASS; no code fix required.**\n- The scan is serialized; total risk includes existing live EA risk plus the proposed trade; a confirmed order is registered before the next pair is processed.\n- Runtime multi-decision risk-budget trace remains pending.\n- Record: `blueprint/P3_SEQUENTIAL_RISK_BUDGET_ADMISSION_AUDIT.md`.\n- **Next release gate is integrated native MetaEditor compile/runtime evidence for the current patched source.**\n'''
if '# 2026-08-22 Sequential Risk-Budget Admission Overlay' not in c:
    c += overlay
CURRENT.write_text(c, encoding='utf-8')
