from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')

old_header = 'Version 4.5.1 - P3-M2-07B.1 Extreme Descendant Supersession'
new_header = 'Version 4.5.1 - P3-M2-07B.2 F1 Boundary Reconciliation'
if s.count(old_header) != 1:
    raise SystemExit(f'build header anchor count={s.count(old_header)}')
s = s.replace(old_header, new_header, 1)

bad = '''   // P3-M2-07B.1: once M08 marks this exact parent Extreme SUPERSEDED by a
   // newer reversal-confirmed opposite Extreme, every still-authoritative MHV/
   // MLV descendant of that parent loses cycle authority atomically. This is
   // strategy-state invalidation only; it never closes an already-open order.
   if(parent.Maturity == EXT_MAT_SUPERSEDED &&
      mlv.ParentConfirmationCandleTime > 0 &&
      parent.ConfirmationCandleTime == mlv.ParentConfirmationCandleTime &&
      mlv.State != MLV_VOID && mlv.State != MLV_SUPERSEDED)
   {
      MarkCanonicalMLVSuperseded(
         mlv, data,
         "MHV/MLV superseded because its exact parent Extreme lost cycle ownership");
      return mlv.State;
   }

'''
if s.count(bad) != 1:
    raise SystemExit(f'P3-M2-07B.1 gate count={s.count(bad)}')
s = s.replace(bad, '', 1)

# F1 owns MHV/MLV cycle termination through its own opposite-to-current-cycle
# reversal-confirmed Extreme transition. M08 parent-Extreme supersession must
# not retroactively erase already-established F1 provenance.
if 'parent.Maturity == EXT_MAT_SUPERSEDED' in s:
    raise SystemExit('stale cross-module descendant gate remains')
if s.count('{') != s.count('}'):
    raise SystemExit('brace imbalance')

p.write_text(s, encoding='utf-8')
print('P3-M2-07B.2 F1 boundary reconciliation applied')
