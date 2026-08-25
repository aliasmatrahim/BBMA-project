#!/usr/bin/env python3
from pathlib import Path
import csv
import importlib.util
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

corr = load('d1o_corr', ROOT / 'blueprint/tools/n2_nmje_decision_correlator.py')
attr = load('d1o_attr', ROOT / 'blueprint/tools/n2_nmje_outcome_attributor.py')

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    log = td / 'expert.log'
    did_opp = 'EURUSD|2026.08.25 01:15|1|7|OPPSEQ'
    did_legacy = 'GBPUSD|2026.08.25 01:30|2|7|LEGSEQ'
    did_opp_token = did_opp.replace(' ', '~')
    did_legacy_token = did_legacy.replace(' ', '~')
    log.write_text('\n'.join([
        '[N1-NMJE] EURUSD REL=SUPPORTING P=H4_OWNER/B J=J1 D1=OWN/B H4=OWN/B H1=RE:F/B M15=RE:F/B R=LTF_STRUCTURE_SUPPORTING_PARENT',
        f'[N2-NMJE-DEC] EURUSD SIG=SIGNAL_RE_ENTRY DIR=B REL=SUPPORTING P=H4_OWNER/B J=J1 DID={did_opp_token} DIDH=HOPP AUTH=OPP OFAM=CSD OC=CYCLE1',
        '[N1-NMJE] GBPUSD REL=ALIGNED P=H4_OWNER/S J=J2 D1=OWN/S H4=OWN/S H1=RE:F/S M15=- R=H1_RE_ALIGNED_WITH_PARENT',
        f'[N2-NMJE-DEC] GBPUSD SIG=SIGNAL_RE_ENTRY DIR=S REL=ALIGNED P=H4_OWNER/S J=J2 DID={did_legacy_token} DIDH=HLEG AUTH=STRAT OFAM=NONE OC=-',
    ]), encoding='utf-8')

    obs, decisions = corr.iter_records([log])
    report = corr.correlate(obs, decisions)
    assert report['n2_decision_count'] == 2, report
    assert report['decision_authority_counts'] == {'OPP': 1, 'STRAT': 1}, report
    assert report['decision_opportunity_family_counts'] == {'CSD': 1, 'NONE': 1}, report
    assert decisions[0].opportunity_cycle == 'CYCLE1', decisions[0]
    assert decisions[0].decision_id == did_opp, decisions[0]

    csv_path = td / 'outcomes.csv'
    with csv_path.open('w', encoding='utf-8', newline='') as handle:
        w = csv.DictWriter(handle, fieldnames=['decision_id', 'net_profit', 'ticket'])
        w.writeheader()
        w.writerow({'decision_id': did_opp, 'net_profit': '8.5', 'ticket': '101'})
        w.writerow({'decision_id': did_legacy, 'net_profit': '-2.0', 'ticket': '102'})

    outcomes, dup = attr.load_outcomes(csv_path)
    attributed = attr.attribute(report, outcomes, dup)
    assert attributed['matched_outcomes'] == 2, attributed
    assert attributed['by_authority']['OPP']['trades'] == 1, attributed
    assert attributed['by_authority']['STRAT']['trades'] == 1, attributed
    assert attributed['by_opportunity_family']['CSD']['net_profit'] == 8.5, attributed
    assert attributed['by_opportunity_family']['NONE']['net_profit'] == -2.0, attributed

print('D1O-04 opportunity telemetry parser/attribution synthetic self-test PASS')
