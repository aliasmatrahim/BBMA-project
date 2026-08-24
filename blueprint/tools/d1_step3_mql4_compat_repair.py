from pathlib import Path
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.')
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    src = root / 'blueprint/source/BBMA_EA.mq4'
    s = src.read_text(encoding='utf-8')

    old_ref = 'D1MajorTrendOwner &owner = state.d1_major_trend_owner;'
    count = s.count(old_ref)
    if count == 0:
        # Idempotent verification path.
        if s.count('D1MajorTrendOwner owner = state.d1_major_trend_owner;') < 2:
            raise SystemExit('D1-03 owner-copy declarations missing')
        if s.count('state.d1_major_trend_owner = owner;') < 2:
            raise SystemExit('D1-03 owner-copy writeback missing')
        print('D1_STEP3_MQL4_COMPAT=ALREADY_PASS')
        return
    if count != 2:
        raise SystemExit(f'expected 2 MQL4-incompatible local reference declarations, found {count}')

    s = s.replace(old_ref, 'D1MajorTrendOwner owner = state.d1_major_trend_owner;')

    set_tail = '''   owner.IsValid = false;
   owner.Reason = reason;
}

void TraceD1MajorTrendOwner'''
    set_new = '''   owner.IsValid = false;
   owner.Reason = reason;
   state.d1_major_trend_owner = owner;
}

void TraceD1MajorTrendOwner'''
    if s.count(set_tail) != 1:
        raise SystemExit('SetD1OwnerUnresolved writeback anchor not unique')
    s = s.replace(set_tail, set_new, 1)

    update_tail = '''   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";
   }

   TraceD1MajorTrendOwner(pair, state);
}

//+------------------------------------------------------------------+
//| MODULE 12: RE-ENTRY ENGINE'''
    update_new = '''   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";
   }

   state.d1_major_trend_owner = owner;
   TraceD1MajorTrendOwner(pair, state);
}

//+------------------------------------------------------------------+
//| MODULE 12: RE-ENTRY ENGINE'''
    if s.count(update_tail) != 1:
        raise SystemExit('UpdateD1MajorTrendOwner writeback anchor not unique')
    s = s.replace(update_tail, update_new, 1)

    if '&owner = state.d1_major_trend_owner' in s:
        raise SystemExit('MQL4 local reference remains')
    if s.count('D1MajorTrendOwner owner = state.d1_major_trend_owner;') < 2:
        raise SystemExit('owner-copy declarations not established')
    if s.count('state.d1_major_trend_owner = owner;') < 2:
        raise SystemExit('owner-copy writeback not established')

    src.write_text(s, encoding='utf-8')
    print('D1_STEP3_MQL4_COMPAT=PASS')


if __name__ == '__main__':
    main()
