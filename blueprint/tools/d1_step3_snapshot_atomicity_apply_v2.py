from pathlib import Path
import argparse
import importlib.util

HERE = Path(__file__).resolve().parent
BASE = HERE / 'd1_step3_snapshot_atomicity_apply.py'
spec = importlib.util.spec_from_file_location('d1_step3_base', BASE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def robust_static_check(src: Path) -> None:
    s = src.read_text(encoding='utf-8')
    required = [
        '//| Version 4.5.1 - D1-03 M11 Snapshot Atomicity',
        'double               Close1;',
        'double               MA50_1;',
        'double               MA50_2;',
        'owner.Close1 = state.d1_data.close;',
        'owner.MA50_1 = currentMA50;',
        'owner.MA50_2 = previousMA50;',
        'owner.Close1 > owner.MA50_1 && owner.MA50_1 > owner.MA50_2',
        'owner.Close1 < owner.MA50_1 && owner.MA50_1 < owner.MA50_2',
        'decision.D1OwnerClose = owner.Close1;',
        'decision.D1OwnerMA50Current = owner.MA50_1;',
        'decision.D1OwnerMA50Previous = owner.MA50_2;',
        'decision.D1OwnerClose != owner.Close1',
        'decision.D1OwnerMA50Current != owner.MA50_1',
        'decision.D1OwnerMA50Previous != owner.MA50_2',
        '[D1-03][OWNER]',
        '[D1-03][M15_D1_BLOCK]',
        '[D1-03][M16_D1_REJECT]',
        'BBMA EA V4.5.1 D1-03 initialized successfully',
        '=== BBMA EA V4.5.1 D1-03 ===',
    ]
    for item in required:
        if item not in s:
            raise SystemExit(f'missing D1-03 invariant: {item}')

    forbidden = [
        'state.d1_major_trend_owner.IsValid &&\n      state.d1_major_trend_owner.LastProcessedD1CandleTime == state.d1_data.candle_time',
        'decision.D1OwnerClose = pairState.d1_data.close;',
        'decision.D1OwnerMA50Current = pairState.current_daily_ema50;',
        'decision.D1OwnerMA50Previous = pairState.prev_daily_ema50;',
        'decision.D1OwnerClose != state.d1_data.close',
        'decision.D1OwnerMA50Current != state.current_daily_ema50',
        'decision.D1OwnerMA50Previous != state.prev_daily_ema50',
        '[D1-01][OWNER]',
        '[D1-02][M15_D1_BLOCK]',
        '[D1-02][M16_D1_REJECT]',
        '=== BBMA EA V4.5.1 D1-01 ===',
        'BBMA EA V4.5.1 D1-02 initialized successfully',
    ]
    for item in forbidden:
        if item in s:
            raise SystemExit(f'stale/split D1 identity remains: {item}')

    if s.count('owner.Close1 > owner.MA50_1 && owner.MA50_1 > owner.MA50_2') != 1:
        raise SystemExit('canonical D1 BUY predicate missing or duplicated')
    if s.count('owner.Close1 < owner.MA50_1 && owner.MA50_1 < owner.MA50_2') != 1:
        raise SystemExit('canonical D1 SELL predicate missing or duplicated')

    d1_filter = s.index('if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;')
    atomic_conflict = s.index('if(buyCount > 0 && sellCount > 0)')
    if d1_filter > atomic_conflict:
        raise SystemExit('D1 filter moved after atomic direction check')

    d1_verify = s.index('if(!ValidateDecisionD1OwnerSnapshot(pairIndex, decision))')
    structural_verify = s.index('if(!ValidateDecisionOwnerSnapshot(pairIndex, decision, ownerExpired))')
    if d1_verify > structural_verify:
        raise SystemExit('M16 D1 verification moved after structural revalidation')

    freeze_start = s.index('bool FreezeD1OwnerSnapshot(')
    freeze_end = s.index('bool IsEntryModeCandidateAllowed(', freeze_start)
    freeze = s[freeze_start:freeze_end]
    for split in ['pairState.d1_data.close', 'pairState.current_daily_ema50', 'pairState.prev_daily_ema50']:
        if split in freeze:
            raise SystemExit(f'M15 freeze still reads split source: {split}')

    verify_start = s.index('bool ValidateDecisionD1OwnerSnapshot(')
    verify_end = s.index('bool ValidateDecisionOwnerSnapshot(', verify_start)
    verify = s[verify_start:verify_end]
    for split in ['state.d1_data.close', 'state.current_daily_ema50', 'state.prev_daily_ema50']:
        if split in verify:
            raise SystemExit(f'M16 verification still reads split source: {split}')

    header = next((line for line in s.splitlines() if 'Version 4.5.1 - D1-03' in line), '')
    if not header.startswith('//| Version 4.5.1 - D1-03'):
        raise SystemExit('D1-03 build header is not left-aligned')

    for n in range(1, 28):
        if f'MODULE {n:02d}:' not in s:
            raise SystemExit(f'missing module marker MODULE {n:02d}')

    print('D1_STEP3_ROBUST_STATIC=PASS')


def normalize_outputs(root: Path) -> None:
    """Keep generated text artifacts git-diff clean without changing semantics."""
    paths = [
        root / 'blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md',
        root / 'blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md',
        root / 'blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md',
        root / 'blueprint/D1_STEP3_M11_SNAPSHOT_ATOMICITY_IMPLEMENTATION_AUDIT_20260824.md',
    ]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        path.write_text(text.rstrip() + '\n', encoding='utf-8')


mod.static_check = robust_static_check


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    ap.add_argument('--finalize', action='store_true')
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    src = root / 'blueprint/source/BBMA_EA.mq4'
    if args.verify:
        robust_static_check(src)
    elif args.finalize:
        mod.finalize(root)
        normalize_outputs(root)
        robust_static_check(src)
    else:
        mod.apply(root)
        normalize_outputs(root)
        robust_static_check(src)


if __name__ == '__main__':
    main()
