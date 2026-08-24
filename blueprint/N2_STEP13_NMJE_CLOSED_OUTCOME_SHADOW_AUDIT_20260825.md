# N2-13 — NMJE Closed-Outcome Shadow Native Compile Audit

Date: 2026-08-25  
Branch: `d1-owner-dev`  
Build: `Version 4.5.1 - N2-13 Closed Outcome Shadow`

## Result
**PASS — closed-outcome shadow materialized / native MT4 MetaEditor 0 errors / 0 warnings.**

Baseline source blob: `eb55cd82f0c8c00b09f7191394fedae8f80c37c2`  
N2-13 source blob: `33dbf8d89ef79b6d7700d00a5380c74238cbf9c8`  
N2-13 source SHA-256: `081141f597b8bac688030293b70946ff1d2f9b52361ef0abd6773424e1e4da22`

The hook is read-only and runs only when `CompactMonitoredTrades()` has selected a monitored ticket and confirmed `OrderCloseTime()!=0`. It emits at most one `[N2-NMJE-OUT]` record before that registry row is discarded. No entry, exit, SL/TP, risk, REM/RRE/REE, M15 or M16 strategy semantics were changed.
