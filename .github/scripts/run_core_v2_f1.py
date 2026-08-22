from pathlib import Path

patcher = Path('.github/scripts/apply_core_v2_f1.py').read_text(encoding='utf-8')

# DoubleTop/DoubleBottom helper names also exist legitimately in M10 as generic
# utilities. F1 only removes the synthetic M09 formula, so do not reject those
# names globally after M09 has been replaced.
patcher = patcher.replace(
    "    'DoubleTop',\n    'DoubleBottom',\n",
    ""
)

exec(compile(patcher, '.github/scripts/apply_core_v2_f1.py', 'exec'))
