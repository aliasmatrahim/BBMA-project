# NMJE / M12N Architecture Documentation Sync Audit — 2026-08-25

Status: **CLOSED / PASS / DOCUMENTATION-ONLY**

## Finding
The live M12N contract and M27 end-to-end contract already defined NMJE as a read-only logical layer between M12 and M13, but top-level governance/current-state documentation and the M13 routing narrative were not fully synchronized. `CURRENT.md` still displayed `M06-M12 -> M13`, and M13 routing did not name the intervening NMJE observation step.

## Reconciliation
- `PROJECT_INSTRUCTIONS.md`: records M12N as logical/non-number-consuming between M12 and M13.
- `blueprint/CURRENT.md`: adds the M12N contract and canonical `M06-M12 -> M12N NMJE (read-only) -> M13 -> ...` pipeline.
- `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`: records M27-coordinated NMJE observation before M13 while preserving immutable owner snapshots.
- `blueprint/MASTER_QUEUE.md`: records docs closure without changing runtime/strategy priority.

## Preserved invariants
M01–M27 numbering, M27 orchestration ownership, M12N read-only authority, exact REM/RRE/REE, D1 watch-only boundary, M15/M16 authority, SL/TP, risk, money management and broker execution are unchanged.

## Source guard
`blueprint/source/BBMA_EA.mq4` was not edited. Expected/post-sync Git blob: `4ccd444a96a34b494653143a7560516a4147b5bc`.

No native MetaEditor compile is required because this reconciliation is documentation-only.
