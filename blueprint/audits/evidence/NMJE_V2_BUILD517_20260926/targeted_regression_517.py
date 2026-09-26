from pathlib import Path
import hashlib, json, subprocess

root=Path(r"D:\BBMA\Workspace\q9-nmje-v2-build516-forward-m5-prep-101")
src_path=root/'blueprint/source/BBMA_EA.mq4'
s=src_path.read_text(encoding='utf-8')

def body(text,name):
    needle=name+'('
    pos=text.find(needle)
    while pos>=0:
        start=text.rfind('\n',0,pos)+1
        end=text.find('\n',pos)
        if end<0: end=len(text)
        line=text[start:end]
        if line and not line[0].isspace() and not line.startswith('//') and needle in line:
            brace=text.find('{',end)
            if brace<0: raise AssertionError('missing brace '+name)
            depth=0
            for i in range(brace,len(text)):
                if text[i]=='{': depth+=1
                elif text[i]=='}':
                    depth-=1
                    if depth==0: return text[start:i+1]
            raise AssertionError('unclosed '+name)
        pos=text.find(needle,pos+len(needle))
    raise AssertionError('missing function '+name)

checks={}
checks['version_517'] = '#property version   "5.17"' in s
checks['build_tag'] = 'V517_NMJE_ACTIVE_SELECTION_POLICY_20260926' in s
checks['selection_default_off'] = 'EnableNMJESelectionPolicy          = false;' in s
priority=body(s,'PriorityEngine_Atomic')
checks['multi_candidate_only'] = 'sameDirectionEligible >= 2' in priority
checks['positive_context_required'] = 'NMJE_IsPositiveSelectionContext(pairState, targetDirection)' in priority
checks['legacy_baseline_frozen_first'] = 'int baselineIdx = -1;' in priority
checks['p5_no_hard_conflict_reason'] = 'M5_CONFIRMED_RE_OPPOSES_PARENT_UNRESOLVED_NO_HARD_CONFLICT' in s
p3=body(s,'NMJE_P3_UpdateClosedM5Shadow')
checks['p3_no_nested_conflict_assignment'] = 'NESTED_CONFLICT' not in p3
active=body(s,'NMJE_IsPositiveSelectionContext')+'\n'+body(s,'NMJE_CompareActiveSelectionCandidates')
forbidden=('OrderSend(','OrderClose(','CheckRiskBeforeTrade(','CalculateLotSize(','FinalPortfolioGuard(','ProcessEntry(')
checks['n3_no_risk_broker_authority'] = not any(x in active for x in forbidden)
checks['sole_ordersend_owner'] = s.count('OrderSend(')==1

base=subprocess.check_output(['git','-C',str(root),'show','9733fe91f8f23120ea4e7a475dd3c103800adc53:blueprint/source/BBMA_EA.mq4'],text=True,encoding='utf-8')
protected=['InvalidationEngine_Atomic','CheckRiskBeforeTrade','IsSignalAllowed','ResolveExecutionReferencePrice','ResolveSelectedSLTPSourceComponent','IsApprovedSLTPSourceComponent','SendOrderWithRetry','RunEntryPreflightAndExecute']
protected_result={}
for name in protected:
    a=hashlib.sha256(body(base,name).encode()).hexdigest().upper()
    b=hashlib.sha256(body(s,name).encode()).hexdigest().upper()
    protected_result[name]={'base':a,'current':b,'same':a==b}
checks['protected_downstream_exact']=all(v['same'] for v in protected_result.values())

def choose(cands,enabled,positive):
    baseline=max(cands,key=lambda c:c['legacy'])
    if not enabled or len(cands)<2 or not positive: return baseline['id']
    return max(cands,key=lambda c:(c['prefix'],c['stages'],c['legacy']))['id']
checks['model_single_unchanged']=choose([{'id':'A','prefix':0,'stages':1,'legacy':9}],True,True)=='A'
two=[{'id':'A','prefix':1,'stages':3,'legacy':9},{'id':'B','prefix':3,'stages':4,'legacy':1}]
checks['model_disabled_legacy']=choose(two,False,True)=='A'
checks['model_nonpositive_legacy']=choose(two,True,False)=='A'
checks['model_positive_richer_wins']=choose(two,True,True)=='B'
tie=[{'id':'A','prefix':3,'stages':4,'legacy':9},{'id':'B','prefix':3,'stages':4,'legacy':1}]
checks['model_density_tie_legacy']=choose(tie,True,True)=='A'

result={'schema':'NMJE_V2_BUILD517_TARGETED_REGRESSION_V1','source_sha256':hashlib.sha256(src_path.read_bytes()).hexdigest().upper(),'checks':checks,'protected':protected_result,'pass':all(checks.values())}
out=Path(r"D:\BBMA\Workspace\q9-nmje-v2-build516-forward-m5-prep-101\blueprint\audits\evidence\NMJE_V2_BUILD517_20260926")
out.mkdir(parents=True,exist_ok=True)
(out/'targeted_regression_517.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['pass'] else 1)