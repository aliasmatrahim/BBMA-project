# V4.60 Re-Entry Profitability Hardening — 2026-09-04

Status: IMPLEMENTED / COMPILE PASS

Trigger: deep diagnosis of seven genuine v4.59 NMJE forward outcomes; all seven closed by stop-loss and all seven were SIGNAL_RE_ENTRY.

Changes:
- Block RE_ENTRY when NMJE relation is CONFLICT.
- Block RE_ENTRY when NMJE relation is BUILDING.
- Enforce MinReEntrySLPips=5.0 while preserving any wider structural SL.
- Enforce MinReEntryRRRatio=1.0 for deterministic-TP RE_ENTRY trades.
- Add REJ_NMJE_RELATION and [NMJE-GATE] rejection telemetry.
- Preserve global MinRRRatio=0.0 and do not alter targetless lifecycle behavior.
- Version bumped from 4.59 to 4.60 to avoid mixing validation identity.

Compile validation:
- MetaEditor: C:\Program Files (x86)\MetaTrader 4\metaeditor.exe
- Temporary compile source: BBMA_EA_v460_profitfix.mq4
- Result: 0 errors, 0 warnings.

Scope note: no live MT4 deployment/restart was performed. Runtime profitability remains unverified until new v4.60 forward outcomes are collected.