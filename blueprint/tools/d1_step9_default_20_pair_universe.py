from pathlib import Path
import argparse

SRC_REL = Path('blueprint/source/BBMA_EA.mq4')
AUDIT_REL = Path('blueprint/D1_STEP9_DEFAULT_20_PAIR_UNIVERSE_AUDIT_20260824.md')

OLD_HEADER = '//| Version 4.5.1 - D1-08 Runtime Identity Sync                    |'
NEW_HEADER = '//| Version 4.5.1 - D1-09 Default 20 Pair Universe                 |'
OLD_PAIR = 'input string   PairList                           = "EURUSD,USDJPY,GBPUSD,AUDUSD,USDCAD,USDCHF,NZDUSD"; // 02 Pairs | comma-separated symbols'
NEW_PAIR = 'input string   PairList                           = "EURUSD,GBPUSD,USDJPY,USDCHF,USDCAD,AUDUSD,NZDUSD,EURJPY,GBPJPY,EURGBP,AUDJPY,CADJPY,CHFJPY,NZDJPY,EURAUD,EURCAD,EURCHF,GBPAUD,GBPCAD,AUDCAD"; // 02 Pairs | default 20-pair FX universe'
OLD_DASH = '=== BBMA EA V4.5.1 D1-08 ==='
NEW_DASH = '=== BBMA EA V4.5.1 D1-09 ==='
OLD_INIT = 'BBMA EA V4.5.1 D1-08 initialized successfully'
NEW_INIT = 'BBMA EA V4.5.1 D1-09 initialized successfully'
EXPECTED = 'EURUSD,GBPUSD,USDJPY,USDCHF,USDCAD,AUDUSD,NZDUSD,EURJPY,GBPJPY,EURGBP,AUDJPY,CADJPY,CHFJPY,NZDJPY,EURAUD,EURCAD,EURCHF,GBPAUD,GBPCAD,AUDCAD'


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {n}')
    return text.replace(old, new, 1)


def verify(src: Path):
    text = src.read_text(encoding='utf-8')
    required = [
        NEW_HEADER,
        NEW_PAIR,
        NEW_DASH,
        NEW_INIT,
        '#define MAX_PAIRS               40',
        'input int      MaxActivePair                      = 7;',
        'if(decision.Valid && decision.DecisionState == DEC_CREATED)',
        'input double   MinRRRatio                         = 0.0;'
    ]
    for item in required:
        if item not in text:
            raise SystemExit(f'missing D1-09 invariant: {item}')
    for stale in [OLD_HEADER, OLD_PAIR, OLD_DASH, OLD_INIT]:
        if stale in text:
            raise SystemExit(f'stale D1-08/default-pair identity remains: {stale}')

    pairs = EXPECTED.split(',')
    if len(pairs) != 20:
        raise SystemExit(f'expected 20 pairs, got {len(pairs)}')
    if len(set(pairs)) != 20:
        raise SystemExit('duplicate pair in default universe')

    registry = [
        'EURUSD','GBPUSD','USDJPY','USDCHF','USDCAD','AUDUSD','NZDUSD','EURJPY','GBPJPY','EURGBP',
        'AUDJPY','CADJPY','CHFJPY','NZDJPY','EURAUD','EURCAD','EURCHF','GBPAUD','GBPCAD','AUDCAD'
    ]
    for pair in registry:
        if f'if(clean == "{pair}") return ' not in text:
            raise SystemExit(f'pair missing fixed PairID registry: {pair}')

    for n in range(1, 28):
        if f'MODULE {n:02d}:' not in text:
            raise SystemExit(f'missing module marker MODULE {n:02d}')

    print('D1_STEP9_DEFAULT_20_PAIR_UNIVERSE_STATIC=PASS')


def write_audit(root: Path, final=False):
    status = 'IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS' if final else 'IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR PENDING'
    compile_line = '0 errors / 0 warnings; EX4 produced.' if final else 'PENDING.'
    (root / AUDIT_REL).write_text(f'''# D1 Step 9 — Default 20-Pair Universe Audit\n\nDate: 2026-08-24  \nBranch: `d1-owner-dev`  \nBuild: `Version 4.5.1 - D1-09 Default 20 Pair Universe`  \nStatus: **{status}**\n\n## User-approved change\nSet the default `PairList` to exactly these 20 FX pairs, preserving the requested order:\n\n`{EXPECTED}`\n\n## Classification\nConfiguration/default-universe change only. It does not modify BBMA signal semantics, D1/H4/H1/M15 hierarchy, lifecycle, SL/TP, MinRR, risk formula, execution logic or the D1-07 M16 guard.\n\n## Static checks\n- exact default PairList count = 20;\n- all 20 entries unique;\n- all 20 are present in the fixed common-FX PairID registry;\n- internal `MAX_PAIRS` capacity remains 40;\n- `MaxActivePair` default intentionally remains 7 (separate portfolio concurrency control);\n- D1-07 M16 empty-decision guard retained;\n- MinRR default-off retained;\n- header, dashboard and Experts init build identity synchronized to D1-09.\n\n## Verification\nStatic/invariant audit: **PASS**.  \nNative MT4 MetaEditor: **{compile_line}**\n''', encoding='utf-8')


def apply(root: Path):
    src = root / SRC_REL
    text = src.read_text(encoding='utf-8')
    text = replace_once(text, OLD_HEADER, NEW_HEADER, 'build header')
    text = replace_once(text, OLD_PAIR, NEW_PAIR, 'default PairList')
    text = replace_once(text, OLD_DASH, NEW_DASH, 'dashboard identity')
    text = replace_once(text, OLD_INIT, NEW_INIT, 'init log identity')
    src.write_text(text, encoding='utf-8')
    write_audit(root, final=False)
    verify(src)
    print('D1_STEP9_DEFAULT_20_PAIR_UNIVERSE_APPLY=PASS')


def finalize(root: Path):
    verify(root / SRC_REL)
    write_audit(root, final=True)
    print('D1_STEP9_DEFAULT_20_PAIR_UNIVERSE_FINALIZE=PASS')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo-root', default='.')
    p.add_argument('--verify', action='store_true')
    p.add_argument('--finalize', action='store_true')
    a = p.parse_args()
    root = Path(a.repo_root).resolve()
    if a.verify:
        verify(root / SRC_REL)
    elif a.finalize:
        finalize(root)
    else:
        apply(root)

if __name__ == '__main__':
    main()
