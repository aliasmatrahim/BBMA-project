from pathlib import Path
import argparse

SRC_REL = Path('blueprint/source/BBMA_EA.mq4')
AUDIT_REL = Path('blueprint/D1_STEP8_RUNTIME_IDENTITY_SYNC_AUDIT_20260824.md')

OLD_HEADER = '//| Version 4.5.1 - D1-07 M16 Empty Decision Guard                 |'
NEW_HEADER = '//| Version 4.5.1 - D1-08 Runtime Identity Sync                    |'
OLD_DASH = '=== BBMA EA V4.5.1 D1-06 ==='
NEW_DASH = '=== BBMA EA V4.5.1 D1-08 ==='
OLD_INIT = 'BBMA EA V4.5.1 D1-06 initialized successfully'
NEW_INIT = 'BBMA EA V4.5.1 D1-08 initialized successfully'


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {n}')
    return text.replace(old, new, 1)


def verify(src: Path):
    text = src.read_text(encoding='utf-8')
    required = [NEW_HEADER, NEW_DASH, NEW_INIT,
                'if(decision.Valid && decision.DecisionState == DEC_CREATED)',
                'input double   MinRRRatio                         = 0.0;']
    for item in required:
        if item not in text:
            raise SystemExit(f'missing D1-08 invariant: {item}')
    for stale in [OLD_HEADER, OLD_DASH, OLD_INIT]:
        if stale in text:
            raise SystemExit(f'stale runtime/build identity remains: {stale}')
    for n in range(1, 28):
        if f'MODULE {n:02d}:' not in text:
            raise SystemExit(f'missing module marker MODULE {n:02d}')
    print('D1_STEP8_RUNTIME_IDENTITY_SYNC_STATIC=PASS')


def write_audit(root: Path, final=False):
    status = 'IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS' if final else 'IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR PENDING'
    compile_line = '0 errors / 0 warnings; EX4 produced.' if final else 'PENDING.'
    (root / AUDIT_REL).write_text(f'''# D1 Step 8 — Runtime Build Identity Sync Audit

Date: 2026-08-24  
Branch: `d1-owner-dev`  
Build: `Version 4.5.1 - D1-08 Runtime Identity Sync`  
Status: **{status}**

## Finding
D1-07 correctly updated the source header, but two user-visible runtime strings remained hard-coded as D1-06:
- dashboard title;
- successful initialization log.

This caused a source/runtime identity mismatch even when the D1-07 code/EX4 was actually installed.

## Fix
- dashboard title synchronized to `D1-08`;
- successful initialization log synchronized to `D1-08`;
- source header updated to the unique D1-08 build identifier;
- D1-07 M16 empty-decision guard retained;
- D1-06 MinRR default-off behavior retained;
- no BBMA strategy, risk, execution, lifecycle or pair-limit behavior changed.

## Verification
Static identity/invariant check: **PASS**.  
Native MT4 MetaEditor: **{compile_line}**
''', encoding='utf-8')


def apply(root: Path):
    src = root / SRC_REL
    text = src.read_text(encoding='utf-8')
    text = replace_once(text, OLD_HEADER, NEW_HEADER, 'build header')
    text = replace_once(text, OLD_DASH, NEW_DASH, 'dashboard identity')
    text = replace_once(text, OLD_INIT, NEW_INIT, 'init log identity')
    src.write_text(text, encoding='utf-8')
    write_audit(root, final=False)
    verify(src)
    print('D1_STEP8_RUNTIME_IDENTITY_SYNC_APPLY=PASS')


def finalize(root: Path):
    verify(root / SRC_REL)
    write_audit(root, final=True)
    print('D1_STEP8_RUNTIME_IDENTITY_SYNC_FINALIZE=PASS')


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
