from pathlib import Path
import hashlib

ROOT = Path('.')
CORE = ROOT / 'docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md'
SAFE = ROOT / 'docs/references/BBMA_STRATEGY_CORE_V2X_WORKBOOK_SAFE_CLARIFICATIONS_20260825.md'
MAP = ROOT / 'docs/references/HOME_COURSE_19P_CANONICAL_ROW_MAP_20260825.md'
CURRENT = ROOT / 'blueprint/CURRENT.md'
QUEUE = ROOT / 'blueprint/MASTER_QUEUE.md'
EA = ROOT / 'blueprint/source/BBMA_EA.mq4'

F7_DOCS = [
    ROOT / 'blueprint/CORE_V2_F7_DETERMINISTIC_NO_MOMENTUM_EXIT_RESOLUTION_AUDIT_20260824.md',
    ROOT / 'blueprint/CORE_V2_F7_POST_MOMENTUM_REARM_FINAL_EXIT_RESOLUTION_AUDIT_20260824.md',
    ROOT / 'blueprint/CORE_V2_F7_COMBINATION_LIFECYCLE_EXIT_OWNERSHIP_AUDIT_20260824.md',
    ROOT / 'blueprint/CORE_V2_F7_M23_M24_LIFECYCLE_STATE_RESTART_RECOVERY_AUDIT_20260824.md',
    ROOT / 'blueprint/CORE_V2_F7_STATIC_TP_VS_LIFECYCLE_EXIT_COEXISTENCE_AUDIT_20260824.md',
]


def read(p):
    return p.read_text(encoding='utf-8')


def write(p, s):
    p.write_text(s, encoding='utf-8', newline='\n')


def insert_before_once(text, anchor, block, marker):
    if marker in text:
        return text
    if anchor not in text:
        raise RuntimeError(f'missing anchor for {marker}: {anchor!r}')
    return text.replace(anchor, block + '\n\n' + anchor, 1)


def insert_after_once(text, anchor, block, marker):
    if marker in text:
        return text
    if anchor not in text:
        raise RuntimeError(f'missing anchor for {marker}: {anchor!r}')
    return text.replace(anchor, anchor + '\n\n' + block, 1)


ea_before = hashlib.sha256(EA.read_bytes()).hexdigest()

# 1) Make authoritative Core self-contained for safe, non-executable Workbook clarifications.
core = read(CORE)
midbb_block = '''### 4.1 Mid-BB descriptive zones and slope context — non-executable clarification

Home Course terminology retained for completeness:
- area from Mid BB toward Top BB = `Buying Zone`;
- area from Mid BB toward Low BB = `Selling Zone`;
- Mid-BB slope up/down/horizontal is a same-timeframe descriptive trend guide.

Execution guard:
- zone membership is context only and is **not** standalone entry authority;
- Mid-BB slope alone is **not** a detector, entry filter, exit rule, TP/SL rule or timeframe-owner override;
- accepted eCSD/CSD, Re-Entry, Extreme, MHV/MLV, Momentum and exact REM/RRE/REE contracts remain unchanged.

Source/reconciliation basis: Home Course 19-page rows HC-P03-002 through HC-P03-007, constrained by `HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`.'''
core = insert_before_once(core, '\n---\n\n## 5. Extreme', midbb_block, '### 4.1 Mid-BB descriptive zones and slope context')

hold_block = '''### 11.1 Home Course 19-page completeness boundary — reviewed but not silently promoted

The 49-family revalidation is recorded in `HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`. All non-fully-covered families are intentionally visible rather than omitted.

Safe/context-only families remain bounded by their existing contracts. The following material is specifically **not universal executable Core authority** unless a later explicit source/strategy decision promotes it:
- detailed horizontal-BB wick/body/close -> Mid-BB reversion table;
- absolute 10–20 pip horizontal-BB breakout threshold;
- MA5 close / MA5-hugging-BB as an independent Momentum validity tier;
- Mid-BB break -> retest -> failure-to-recross as a universal standalone detector;
- deterministic MHV post-event Momentum/no-Momentum TP/hold/close rules;
- guaranteed Candle Arah outer-BB destination;
- pre-Re-Entry/post-direction outer-BB hold/no-TP exception;
- broad literal `D1 says Buy, H4 says Sell -> always follow D1` rule beyond the already approved scoped D1/MA50 strategic-owner contract;
- Double H1 Extreme -> deterministic H4 MHV inference;
- H4 MHV -> direct lower-TF Extreme execution shortcut;
- claim that valid H4 MHV means no further H1 MHV;
- deterministic next-day prediction from today's D1 close;
- universal Re-Entry -> no Momentum mandatory TP/reversal exit;
- `Extrem Magic` as independent executable detector/authority;
- unrestricted recursive lower-TF replay/add-on authority.

Precedence note: where historical 2026-08-24 F7 lifecycle audits describe post-Re-Entry no-Momentum/hold behavior as source/spec-level `RESOLVED`, executable promotion is superseded by the later 2026-08-25 cross-source reconciliation and this current authoritative Core, which retain the material behavior as HOLD. Historical evidence remains useful; it does not itself grant execution authority.'''
core = insert_before_once(core, '\n---\n\n## 12. Change-control rule', hold_block, '### 11.1 Home Course 19-page completeness boundary')
write(CORE, core)

# 2) Repair safe clarification companion omission: Mid-BB slope was reconciled safe but absent from the layer.
safe = read(SAFE)
slope_block = '''## V2.x-C1b — Mid-BB slope context

The Workbook describes Mid-BB slope (up/down/horizontal) as a same-timeframe trend guide.

Guard:
- slope is descriptive/context evidence only;
- Mid-BB slope alone is not a detector, entry gate, exit trigger, TP/SL rule, score, or owner-timeframe override;
- no existing eCSD/CSD, Re-Entry, Momentum, Extreme, MHV/MLV or combination condition is weakened or replaced.'''
safe = insert_before_once(safe, '\n## V2.x-C2 — Direction-strength hierarchy', slope_block, '## V2.x-C1b — Mid-BB slope context')
write(SAFE, safe)

# 3) Correct mechanically irreproducible canonical coverage counts.
mp = read(MAP)
old = '''Classification by family:
- Fully COVERED: **30**
- PARTIAL (including mixed covered/partial families): **8**
- MISSING/HOLD: **11**
- Total applicable canonical families: **49**

Strict full-coverage metric:

`30 / 49 = 61.22% fully covered`

Representation metric (COVERED + PARTIAL, without pretending PARTIAL is complete):

`(30 + 8) / 49 = 77.55% represented at least partially`'''
new = '''Classification by family under the strict heading-status rule:
- Fully COVERED (status exactly `COVERED`): **28**
- PARTIAL / mixed (any status containing `PARTIAL`, including `COVERED/PARTIAL` and `PARTIAL/HOLD`): **10**
- MISSING/HOLD: **11**
- Total applicable canonical families: **49**

Strict full-coverage metric:

`28 / 49 = 57.14% fully covered`

Partial/mixed metric:

`10 / 49 = 20.41% partial/mixed`

Representation metric (COVERED + PARTIAL/mixed, without pretending PARTIAL is complete):

`(28 + 10) / 49 = 77.55% represented at least partially`

Counting guard: a mixed heading such as `COVERED/PARTIAL` or `PARTIAL/HOLD` never counts as fully covered. This corrects the earlier 30/8 split while preserving the same represented-at-least-partially total of 38 families.'''
if old in mp:
    mp = mp.replace(old, new, 1)
elif '28 / 49 = 57.14% fully covered' not in mp:
    raise RuntimeError('canonical map metric block not found and correction marker absent')
write(MAP, mp)

# 4) Put a non-destructive precedence banner on historical F7 documents that depend on lifecycle-exit promotion.
notice = '''> **2026-08-25 EXECUTABLE-PRECEDENCE NOTICE**
> This document is retained as historical/provisional evidence reconstruction. Where it treats post-Re-Entry no-Momentum, re-arm, hold/no-TP, or related lifecycle-close behavior as executable/source-spec `RESOLVED`, that promotion is superseded by `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`, `docs/references/HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`, and the current authoritative Strategy Core. Those material lifecycle behaviors remain HOLD unless a later explicit strategy decision reopens them. No EA execution authority may be derived from the superseded conclusion alone.
'''
for p in F7_DOCS:
    txt = read(p)
    if '2026-08-25 EXECUTABLE-PRECEDENCE NOTICE' not in txt:
        lines = txt.splitlines()
        if not lines or not lines[0].startswith('# '):
            raise RuntimeError(f'unexpected markdown header: {p}')
        txt = lines[0] + '\n\n' + notice + '\n' + '\n'.join(lines[1:]).lstrip('\n')
        write(p, txt)

# 5) Top-level status overlays: append only once.
current_overlay = '''## 2026-08-25 Core 49-family revalidation overlay — PASS / DOCS-ONLY

- Mechanical canonical count corrected to **28 fully covered + 10 partial/mixed + 11 MISSING/HOLD = 49**.
- Strict full coverage = **57.14%**; represented at least partially = **77.55%**; unresolved hard HOLD = **22.45%**.
- All 21 non-fully-covered families are explicitly accounted for in `docs/references/HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`.
- Safe Mid-BB zone/slope context is visible in authoritative Core with non-execution guards.
- Historical F7 lifecycle-exit promotion is precedence-guarded by the 2026-08-25 reconciliation; no no-Momentum execution rule is silently enabled.
- D1 MHV/MLV and D1 eCSD remain watch/context-only in NMJE/D1 Opportunity execution paths.
- **EA source unchanged by this revalidation.**'''
cur = read(CURRENT)
if '## 2026-08-25 Core 49-family revalidation overlay' not in cur:
    cur = cur.rstrip() + '\n\n---\n\n' + current_overlay + '\n'
    write(CURRENT, cur)

queue_overlay = '''## Core 49-Family Revalidation Closure — CLOSED / PASS / DOCS-ONLY

- Correct canonical-family strict split: **28 COVERED / 10 PARTIAL-MIXED / 11 MISSING-HOLD**.
- All non-full families are retained by ID in the 2026-08-25 revalidation audit.
- Safe descriptive clarifications are documented; material strategy HOLDs remain non-executable.
- Historical F7 no-Momentum lifecycle conclusions are precedence-guarded against accidental future promotion.
- No MQL4 strategy change; no native compile required for this docs-only correction. Future strategy promotion from a HOLD still requires an explicit decision gate.'''
q = read(QUEUE)
if '## Core 49-Family Revalidation Closure' not in q:
    q = q.rstrip() + '\n\n---\n\n' + queue_overlay + '\n'
    write(QUEUE, q)

# 6) Hard guards.
ea_after = hashlib.sha256(EA.read_bytes()).hexdigest()
if ea_before != ea_after:
    raise RuntimeError('EA source changed during docs-only revalidation')

checks = {
    CORE: ['Buying Zone', 'Selling Zone', 'Mid-BB slope', 'Extrem Magic', 'universal Re-Entry -> no Momentum mandatory TP/reversal exit',
           'REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV',
           'RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme',
           'REE = D1 Re-Entry + H4 Extreme + H1 Extreme'],
    MAP: ['28 / 49 = 57.14% fully covered', '10 / 49 = 20.41% partial/mixed', '(28 + 10) / 49 = 77.55%'],
    SAFE: ['V2.x-C1b — Mid-BB slope context'],
    CURRENT: ['Core 49-family revalidation overlay — PASS / DOCS-ONLY'],
    QUEUE: ['Core 49-Family Revalidation Closure — CLOSED / PASS / DOCS-ONLY'],
}
for p, needles in checks.items():
    txt = read(p)
    for needle in needles:
        if needle not in txt:
            raise RuntimeError(f'missing guard in {p}: {needle}')

if '30 / 49 = 61.22% fully covered' in read(MAP):
    raise RuntimeError('stale strict coverage metric remains in canonical map')

for p in F7_DOCS:
    if '2026-08-25 EXECUTABLE-PRECEDENCE NOTICE' not in read(p):
        raise RuntimeError(f'missing F7 precedence notice: {p}')

print('CORE49_DOCS_REVALIDATION=PASS')
print('EA_SHA256=' + ea_after)
