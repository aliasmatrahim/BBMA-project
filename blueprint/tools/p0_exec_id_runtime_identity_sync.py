from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {n}')
    return text.replace(old, new, 1)


def main() -> None:
    text = SRC.read_text(encoding='utf-8')
    text = replace_once(
        text,
        '=== BBMA EA V4.5.8 D1 TP-Wajib Lifecycle Stage ===',
        '=== BBMA EA V4.5.9 P0 EXEC_ID Persistence Fix ===',
        'dashboard build identity')
    text = replace_once(
        text,
        'BBMA EA V4.5.8 D1 TP-Wajib Lifecycle Stage initialized successfully',
        'BBMA EA V4.5.9 P0 EXEC_ID Persistence Fix initialized successfully',
        'init log build identity')

    required = [
        'Version 4.5.9 - P0 Execution Identity Persistence Fix',
        '#property version   "4.59"',
        '=== BBMA EA V4.5.9 P0 EXEC_ID Persistence Fix ===',
        'BBMA EA V4.5.9 P0 EXEC_ID Persistence Fix initialized successfully',
        'SaveExecutionIdentityHash',
        'TARGETLESS_DURABLE_IDENTITY_REQUIRED',
    ]
    for marker in required:
        if marker not in text:
            raise SystemExit(f'missing final P0 invariant: {marker}')
    if 'BBMA EA V4.5.8 D1 TP-Wajib Lifecycle Stage' in text:
        raise SystemExit('stale V4.5.8 runtime identity remains')

    SRC.write_text(text, encoding='utf-8')
    print('P0_EXEC_ID_RUNTIME_IDENTITY_SYNC=PASS')


if __name__ == '__main__':
    main()
