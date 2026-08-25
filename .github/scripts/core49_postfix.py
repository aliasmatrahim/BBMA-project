from pathlib import Path

p = Path('docs/references/HOME_COURSE_19P_CANONICAL_ROW_MAP_20260825.md')
text = p.read_text(encoding='utf-8')
old = '''## Next gate

Do not modify executable strategy from the HOLD families automatically. Next safe work is cross-source reconciliation of PARTIAL/MISSING families against the primary operational PDF, secondary PDF, Finale evidence and existing conflict register. Non-conflicting descriptive clarifications may be proposed for Core V2.x; execution-authority changes remain strategy-decision gates.'''
new = '''## Post-reconciliation status

The cross-source reconciliation requested by the former `Next gate` has now been completed in `HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`, and all 21 non-fully-covered families are revalidated in `HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`.

Do not modify executable strategy from HOLD families automatically. Safe descriptive clarifications may enter Core only with explicit non-execution guards; any execution-authority promotion from a HOLD remains a strategy-decision gate.'''
if old in text:
    text = text.replace(old, new, 1)
elif '## Post-reconciliation status' not in text:
    raise RuntimeError('stale Next gate block not found')
p.write_text(text, encoding='utf-8', newline='\n')
print('CORE49_POSTFIX=PASS')
