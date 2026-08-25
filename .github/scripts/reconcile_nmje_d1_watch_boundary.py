from pathlib import Path

# M12N: explicit D1 watch-only / non-execution-authority boundary.
p = Path('blueprint/contracts/M12N_NESTED_MTF_JOURNEY_ENGINE_CONTRACT.md')
s = p.read_text(encoding='utf-8')
if '## D1 watch-only / non-execution-authority boundary' not in s:
    anchor = '## M13/M14 boundary\n'
    block = (
        '## D1 watch-only / non-execution-authority boundary\n'
        'The following D1-origin states are deliberately context-only for NMJE and may never become a shortcut to lower-timeframe execution:\n'
        '- **D1 MHV/MLV = WATCH ONLY / CONTEXT ONLY.** It may be represented in diagnostics or node history, but it must not be selected as an executable D1 parent, install a D1 opportunity family, create an M15 candidate, or authorize an LTF entry.\n'
        '- **D1 eCSD = WATCH ONLY / DIRECTION-STAGE CONTEXT ONLY.** It may be observed/logged, but it must not install a D1 opportunity family, create an M15 candidate, or authorize an LTF entry.\n'
        '- **D1 CSD remains a direction signal, not a direct entry.** The separately approved D1 Opportunity Journey may use confirmed D1 CSD only as opportunity context and still requires approved fresh lower-timeframe Re-Entry readiness.\n'
        '- For D1-origin N1 parent selection, only the already-approved **D1 Re-Entry** parent and **D1 strategic owner** broad context are eligible parent kinds. D1 MHV/MLV and D1 eCSD are not parent kinds.\n'
        '- No `higher-TF MHV/MLV -> direct lower-TF entry` shortcut is authorized.\n\n'
        'This boundary is consistent with the canonical Core distinction `MHV/MLV = setup/context`, `eCSD/CSD = direction`, `Re-Entry = entry/setup zone`, exact REM/RRE/REE signatures, and the D1 Opportunity decision record.\n\n'
    )
    if anchor not in s:
        raise SystemExit('M12N anchor missing')
    p.write_text(s.replace(anchor, block + anchor, 1), encoding='utf-8')

# M27: synchronize top-level canonical architecture with logical M12N.
p = Path('blueprint/contracts/M27_ORCHESTRATOR_END_TO_END_CONTRACT.md')
s = p.read_text(encoding='utf-8')
old = (
    '1. M06-M12 owner detectors/state engines produce frozen source snapshots.\n'
    '2. M13 collects snapshots only.\n'
    '3. M14 validates REM/RRE/REE only.\n'
    '4. M15 performs one pair-level atomic final-authority pass after BUY and SELL candidates have both been collected.\n'
    '5. M16 invalidates conflicts only.\n'
    '6. M17 resolves and validates the source-owned BBMA TP destination and protective structural SL.\n'
    '7. M21 calculates one deterministic lot from the frozen risk snapshot.\n'
    '8. M19 evaluates live spread/drawdown/basket/EA-wide prospective risk using that proposed lot.\n'
    '9. M20 performs the final prospective portfolio/protection gate.\n'
    '10. M22 executes the immutable approved payload once, with idempotent ambiguous-result handling.\n'
)
new = (
    '1. M06-M12 owner detectors/state engines produce frozen source snapshots.\n'
    '2. M12N NMJE reads the already-owned snapshots as a read-only nested context/lineage layer; it cannot create/reject/rank candidates or alter execution authority.\n'
    '3. M13 collects snapshots only.\n'
    '4. M14 validates REM/RRE/REE only.\n'
    '5. M15 performs one pair-level atomic final-authority pass after BUY and SELL candidates have both been collected.\n'
    '6. M16 invalidates conflicts only.\n'
    '7. M17 resolves and validates the source-owned BBMA TP destination and protective structural SL.\n'
    '8. M21 calculates one deterministic lot from the frozen risk snapshot.\n'
    '9. M19 evaluates live spread/drawdown/basket/EA-wide prospective risk using that proposed lot.\n'
    '10. M20 performs the final prospective portfolio/protection gate.\n'
    '11. M22 executes the immutable approved payload once, with idempotent ambiguous-result handling.\n'
)
if old in s:
    p.write_text(s.replace(old, new, 1), encoding='utf-8')
elif 'M12N NMJE reads the already-owned snapshots' not in s:
    raise SystemExit('M27 pipeline anchor missing')

# Dedicated reconciliation record.
audit = Path('blueprint/NMJE_D1_WATCH_ONLY_BOUNDARY_RECONCILIATION_20260825.md')
audit.write_text(
    '# NMJE D1 Watch-Only / Non-Execution-Authority Boundary Reconciliation\n\n'
    'Date: 2026-08-25\n'
    'Branch: `d1-owner-dev`\n'
    'Status: **PASS / DOCUMENTATION GAP CLOSED / NO EA SOURCE CHANGE**\n\n'
    '## Revalidated boundary\n'
    'D1 MHV/MLV and D1 eCSD may be observed as context, but they may not be used by NMJE as a higher-timeframe trigger/parent that directly authorizes a lower-timeframe entry.\n\n'
    '## Source/Core basis\n'
    '- MHV/MLV is setup/context rather than standalone direct execution authority.\n'
    '- eCSD/CSD is direction intent; raw direction is not direct entry authority and the taught execution setup is Re-Entry.\n'
    '- Exact executable MTF signatures remain REM = H4 RE + H1 Extreme + M15 MHV/MLV; RRE = D1 RE + H4 RE + H1 Extreme; REE = D1 RE + H4 Extreme + H1 Extreme.\n'
    '- Home Course cross-source reconciliation keeps `higher-TF MHV -> direct lower-TF entry` as HOLD.\n'
    '- Forum evidence is corroborating only and provides no higher-precedence authority for a D1 MHV/eCSD -> direct LTF shortcut.\n\n'
    '## D1 Opportunity boundary\n'
    'The approved D1 Opportunity Journey explicitly keeps **D1 MHV/MLV and D1 eCSD WATCH ONLY**. Active D1 opportunity families remain the separately approved Extreme->TPW tactical context, confirmed CSD context, confirmed D1 Re-Entry, and Momentum/CSM retrace context, each subject to its own LTF readiness/authority rules.\n\n'
    '## Current-source verification\n'
    '- `ENUM_D1_OPPORTUNITY_FAMILY` has no D1 MHV/MLV or eCSD executable family.\n'
    '- D1 eCSD is handled by a watch helper and only logs `Action=WATCH_ONLY`; it never installs a D1 opportunity family.\n'
    '- NMJE parent kinds include D1 Re-Entry and D1 strategic owner, but no D1 MHV/MLV or D1 eCSD parent kind.\n'
    '- M12N remains read-only and M15 remains sole final new-entry authority.\n\n'
    '## Locked guard\n'
    '`D1 MHV/MLV or D1 eCSD -> NMJE context only -> NO direct LTF execution authority.`\n\n'
    'Any future promotion requires separate source reconciliation and explicit strategy approval.\n',
    encoding='utf-8'
)

# Status overlays preserve historical records and only append current reconciliation.
current = Path('blueprint/CURRENT.md')
s = current.read_text(encoding='utf-8').rstrip()
if '# 2026-08-25 NMJE D1 Watch-Only Boundary Overlay' not in s:
    s += (
        '\n\n# 2026-08-25 NMJE D1 Watch-Only Boundary Overlay\n'
        '- `M12N` is the logical read-only Nested MTF Journey Engine between M12 owner state and M13/M14/M15 processing.\n'
        '- **D1 MHV/MLV and D1 eCSD are WATCH ONLY / non-execution-authority states for NMJE.** They cannot act as executable D1 parents, create M15 candidates, or directly authorize LTF entries.\n'
        '- D1 CSD remains direction context, not raw direct entry; approved D1 Opportunity use still requires fresh LTF Re-Entry readiness.\n'
        '- Exact REM/RRE/REE signatures remain unchanged.\n'
        '- Record: `blueprint/NMJE_D1_WATCH_ONLY_BOUNDARY_RECONCILIATION_20260825.md`.\n'
        '- Documentation-only reconciliation; EA source/trading behavior unchanged.\n'
    )
current.write_text(s.rstrip() + '\n', encoding='utf-8')

queue = Path('blueprint/MASTER_QUEUE.md')
s = queue.read_text(encoding='utf-8').rstrip()
if '## 2026-08-25 — NMJE D1 Watch-Only Boundary Closure' not in s:
    s += (
        '\n\n## 2026-08-25 — NMJE D1 Watch-Only Boundary Closure\n'
        'Status: **CLOSED / PASS / DOCUMENTATION-ONLY**\n'
        '- D1 MHV/MLV and D1 eCSD are locked as NMJE watch/context-only states with no direct LTF execution authority.\n'
        '- No higher-TF MHV/MLV -> direct LTF entry shortcut is authorized.\n'
        '- M12N contract and M27 canonical pipeline are synchronized with this boundary.\n'
        '- Exact REM/RRE/REE and D1 Opportunity execution contracts remain unchanged.\n'
        '- Audit: `blueprint/NMJE_D1_WATCH_ONLY_BOUNDARY_RECONCILIATION_20260825.md`.\n'
    )
queue.write_text(s.rstrip() + '\n', encoding='utf-8')

print('NMJE D1 watch-only reconciliation PASS')
