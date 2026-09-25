from pathlib import Path
import json, re, subprocess, hashlib, sys

repo = Path(__file__).resolve().parents[4]
source_path = repo / 'blueprint' / 'source' / 'BBMA_EA.mq4'
source = source_path.read_text(encoding='utf-8-sig').replace('\r\n','\n')
base = subprocess.check_output(
    ['git','show','origin/d1-owner-dev:blueprint/source/BBMA_EA.mq4'],
    cwd=repo).decode('utf-8-sig').replace('\r\n','\n')

def norm(text):
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return re.sub(r'\s+', ' ', text).strip()

def extract_function(text, name):
    rx = re.compile(r'(?m)^[ \t]*(?:[A-Za-z_][\w<>]*[ \t*&]+)+' + re.escape(name) + r'\s*\([^;{}]*\)\s*\{')
    m = rx.search(text)
    if not m: return None
    b = text.find('{', m.start()); depth = 0; i = b
    in_str = None; esc = False; linecom = False; blockcom = False
    while i < len(text):
        c = text[i]; n = text[i+1] if i+1 < len(text) else ''
        if linecom:
            if c == '\n': linecom = False
        elif blockcom:
            if c == '*' and n == '/': blockcom = False; i += 1
        elif in_str:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == in_str: in_str = None
        else:
            if c == '/' and n == '/': linecom = True; i += 1
            elif c == '/' and n == '*': blockcom = True; i += 1
            elif c in ('\"', "'"): in_str = c
            elif c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: return text[m.start():i+1]
        i += 1
    raise RuntimeError('unterminated '+name)

checks = {}
def check(name, cond, detail=''):
    checks[name] = {'pass': bool(cond), 'detail': detail}

check('version_512', '#property version   "5.12"' in source)
check('source_rev_003', 'NMJE_P2P3_SHADOW_003_20260925' in source)
check('runtime_build_identity_512', 'Build=5.12 BuildTag=' in source)
check('p2_definition_and_call_once', source.count('NMJE_P2_PrintEqualEligibilityShadow') == 2, str(source.count('NMJE_P2_PrintEqualEligibilityShadow')))
check('p3_definition_and_call_once', source.count('NMJE_P3_UpdateClosedM5Shadow') == 2, str(source.count('NMJE_P3_UpdateClosedM5Shadow')))
check('m5_latest_closed_binding', 'GetLatestClosedCandleTime(actual, PERIOD_M5)' in source)
check('forbidden_execution_gate_absent', all(x not in source for x in ['EnableNMJEExecutionGate','EnableNestedExecutionGate','N3_EXECUTION_POLICY','N3_POLICY_ACTIVE']))
p2 = extract_function(source, 'NMJE_P2_PrintEqualEligibilityShadow') or ''
p3 = extract_function(source, 'NMJE_P3_UpdateClosedM5Shadow') or ''
check('p2_no_order_score_reject_write', all(x not in p2 for x in ['PriorityTier =','Score =','DecisionState =','RejectionReason =','OrderSend(','RunEntryPreflightAndExecute(']))
check('p3_no_detector_or_execution', all(x not in p3 for x in ['DetectExtreme(','DetectCSM(','PriorityEngine_Atomic(','InvalidationEngine_Atomic(','OrderSend(','RunEntryPreflightAndExecute(','CheckRiskBeforeTrade(']))
check('p3_closed_data_guard', 'state.m5_data.is_valid' in p3 and 'state.m5_data.is_closed' in p3)
check('p3_only_nested_shadow_mutation', 'g_nested_journeys[pairIndex].M5ShadowPresent' in p3 and 'PairState state = g_pair_states[pairIndex];' in p3)

process = extract_function(source, 'ProcessPair') or ''
i_m5 = process.find('GetLatestClosedCandleTime(actual, PERIOD_M5)')
i_obs = process.find('UpdateNestedJourneyObservation(pairIndex)')
i_p3 = process.find('NMJE_P3_UpdateClosedM5Shadow(pairIndex)')
i_asm = process.find('for(int assembleDirIdx = 0; assembleDirIdx < 2; assembleDirIdx++)')
i_p2 = process.find('NMJE_P2_PrintEqualEligibilityShadow')
i_priority = process.find('PriorityEngine_Atomic(allCandidates')
check('p3_call_order', 0 <= i_m5 < i_obs < i_p3 < i_asm, f'{i_m5},{i_obs},{i_p3},{i_asm}')
check('p2_pre_priority_observer_order', 0 <= i_p2 < i_priority, f'{i_p2},{i_priority}')

protected = [
    'CompareCanonicalCandidates','PriorityEngine_Atomic','InvalidationEngine_Atomic',
    'ResolveApprovedInitialSLTP','CheckRiskBeforeTrade','RunEntryPreflightAndExecute',
    'IsSignalAllowed','SendOrderWithRetry','ResolveExecutionReferencePrice',
    'ResolveSelectedSLTPSourceComponent','IsApprovedSLTPSourceComponent'
]
protected_detail = {}
for name in protected:
    cur = extract_function(source, name) or ''
    old = extract_function(base, name) or ''
    same = bool(cur and old and norm(cur) == norm(old))
    protected_detail[name] = {
        'same': same,
        'current_nmje_refs': len(re.findall(r'\bNMJE_', cur)),
        'current_m5_refs': len(re.findall(r'\bM5\b|PERIOD_M5', cur)),
        'current_sha256': hashlib.sha256(norm(cur).encode()).hexdigest().upper() if cur else None,
        'base_sha256': hashlib.sha256(norm(old).encode()).hexdigest().upper() if old else None,
    }
check('protected_functions_exact', all(x['same'] for x in protected_detail.values()), json.dumps(protected_detail, sort_keys=True))
check('protected_functions_no_nmje_m5', all(x['current_nmje_refs']==0 and x['current_m5_refs']==0 for x in protected_detail.values()))

shared_nmje = ['NMJE_BuildJourneyID','NMJE_ResolveParent','UpdateNestedJourneyObservation','NMJE_PrintValidatedDecisionShadow','NMJE_PrintClosedOutcomeShadow']
shared_detail = {}
for name in shared_nmje:
    cur = extract_function(source, name) or ''
    old = extract_function(base, name) or ''
    same = bool(cur and old and norm(cur) == norm(old))
    shared_detail[name] = same
check('existing_nmje_helpers_preserved', all(shared_detail.values()), json.dumps(shared_detail, sort_keys=True))

result = {
    'schema':'NMJE_V2_P2_P3_TARGETED_REGRESSION_V1',
    'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest().upper(),
    'base_ref':'origin/d1-owner-dev',
    'checks': checks,
    'protected': protected_detail,
    'existing_nmje': shared_detail,
}
result['status'] = 'PASS' if all(v['pass'] for v in checks.values()) else 'FAIL'
out = Path(__file__).with_name('targeted_regression_result.json')
out.write_text(json.dumps(result, indent=2), encoding='utf-8')
print('NMJE_P2_P3_TARGETED_REGRESSION='+result['status'])
for k,v in checks.items():
    print(k, 'PASS' if v['pass'] else 'FAIL', v['detail'] if not v['pass'] else '')
print('RESULT='+str(out))
if result['status'] != 'PASS': sys.exit(1)