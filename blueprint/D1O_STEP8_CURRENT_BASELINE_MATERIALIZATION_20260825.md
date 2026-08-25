# D1O Step 8 — Current-Baseline Materialization Closure

Date: 2026-08-25
Branch: `d1-owner-dev`
Build: `Version 4.5.1 - D1O-07 Canonical LTF Dedup`

Status: **MATERIALIZED / STATIC CONTRACT PASS**

The D1O-07 canonical LTF dedup patch was re-materialized directly on the current owner baseline using the guarded `d1o_current_baseline_materialize.py` tool.

Locked invariants preserved:
- fresh LTF Re-Entry owns executable opportunity identity;
- D1 cycle/family remains attribution metadata;
- H1 owns the anchor when H1+M15 fresh Re-Entry coexist;
- approved REM/RRE/REE signatures are unchanged;
- SL/TP source selection and entry preflight anchors remain present;
- no Workbook HOLD rule is promoted into executable behavior.

Native MT4 compilation remains a separate validation gate; prior Windows installer acquisition was infrastructure-blocked and is not treated as source failure.
