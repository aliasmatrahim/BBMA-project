from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')

old_header = 'Version 4.5.1 - P3-M2-07B Opposite Extreme Supersession'
new_header = 'Version 4.5.1 - P3-M2-07B.1 Extreme Descendant Supersession'
if s.count(old_header) != 1:
    raise SystemExit(f'build header anchor count={s.count(old_header)}')
s = s.replace(old_header, new_header, 1)

anchor = '''   bool parentMature = IsMHVParentExtremeMature(parent);

   if(mlv.State == MLV_NONE)
'''
replacement = '''   bool parentMature = IsMHVParentExtremeMature(parent);

   // P3-M2-07B.1: once M08 marks this exact parent Extreme SUPERSEDED by a
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

   if(mlv.State == MLV_NONE)
'''
if s.count(anchor) != 1:
    raise SystemExit(f'MLV parent maturity anchor count={s.count(anchor)}')
s = s.replace(anchor, replacement, 1)

if 'parent.Maturity == EXT_MAT_SUPERSEDED' not in s:
    raise SystemExit('descendant supersession gate missing')
if s.count('{') != s.count('}'):
    raise SystemExit('brace imbalance')

p.write_text(s, encoding='utf-8')
print('P3-M2-07B.1 descendant supersession patch applied')
