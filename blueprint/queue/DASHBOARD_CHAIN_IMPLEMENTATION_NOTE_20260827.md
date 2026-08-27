# Dashboard Compact Chain — Implementation Boundary

Date: 2026-08-27

Target format (locked by user):

`PAIR | ST | SETUP | CHAIN | POS`

Compact, minimalistic, vertically aligned. Fixed column X positions. Category separator is `|`; chain progression is `>`; direction uses `↑/↓`; setup completion uses `✓`; live broker position uses `POS↑/POS↓`; lifecycle status is limited to `IDL / ST / BLD / INV`.

Implementation scope:
- DASH-FIX-01 Active Trade Sync
- DASH-ENH-01 Cycle-Aware Signal Chain
- DASH-ENH-02 Auto Chain Lifecycle

Architecture boundary:
- M25 display/observability only.
- Read canonical M08/M09/M12/M13/M14/M15 state and exact-owned live broker orders.
- Never mutate canonical strategy owners, decisions, risk state, lot sizing, SL/TP, or execution state.
- Do not add any new entry filter or execution authority.
- Runtime frozen candidate remains untouched; implementation is isolated on a dashboard development branch until compile/static verification is complete.
