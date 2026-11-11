# SIG06 MHV — source availability propagation, 2026-11-11

Scope: bounded fix for consumed-candle availability propagation. Full MHV historical recovery remains PARTIAL/HOLD.
Code checkpoint 47ca63a287efa1d7e78c78f30b606de69e3e0484; Build 6.13 / MHV_AVAILABILITY_PROPAGATION_001_20261111.
EA LF SHA256: 43470ff9795b18e44844bb815deceee778072a004b8815666e18e8ffa584d15c.

## Issue → impact → fix

Build 6.12 could return an unchanged M09 enum after a failed inner read while the shared caller reported success. An enclosing source router could commit the latest candle cursor. The stale view watermark blocked projection, but the committed cursor could skip the same-bar retry and leave an invalidating candle unprocessed.

The canonical M09 body now exposes explicit availability separately from its lifecycle state. Loss and continuation readers also separate readiness from their predicates. Guarded updates stage the M09/parent pair and verify source input identity before commit; the shared two-direction path stages all four owners. Actual M15 and pre-freeze callers honor a false availability result. The compatibility entry point delegates to the same engine. No signal formula, clock, expiry, risk or order logic changed. Static diff: 460 unchanged function bodies, five scoped changed bodies, four added helper/overload bodies, zero deleted.

## Native verification

| Check | Result |
|---|---|
| Frozen 6.12 caller RED | 197 PASS / 98 FAIL; a single missing Close9 recovers before subsequent reads but availability is lost by the old caller. |
| Build 6.13 caller GREEN | 295/295; 42 cases over shared helper, auxiliary advancement and actual source router, BUY/SELL and seven TF. Failed read preserves owner/cursor; same-bar retry consumes the invalidating bar exactly on success. |
| Explicit inner-read status | 785/785; 112 cases over eight branch locations, all seven TFs and both directions. A transient inner failure is reported and staged owner/parent are preserved; retry succeeds. |
| Candidate invalidation regression | 323/323 on the same Build 6.13 source. |
| Affected native regression | 14 groups PASS. Ordinary and seeded controller OFF/ON/frozen 6.12 traces match exactly: 12,224 rows, 16 M15 cycles and zero attempts per case. Seeded controller exercised three parent handovers per case. |
| Compilation and identity | Strict full EA/harness compilation: 0 errors, 0 warnings. Collector PID 6584 exit 0 verified 14 final binary bindings and all source/header/trace/HST identities. |

The first Momentum readiness regression had 166 PASS / 1 FAIL. Its direct ProcessPair fixture omitted the canonical-scope flag required by the actual M27 dispatch. Set that flag in the fixture; retry passes with the same production source. Initial logs and state are retained; completed candidate verification was not rerun by the resume driver.

Production source, native harnesses, binary identities, headers and traces are recorded in the evidence archive. Staged transition messages are diagnostic; acceptance uses authoritative committed state, cursor and decision traces. No standalone full-repository pytest result is claimed.

## Remaining signal acceptance

Earlier bounded restart and safe gap rejection evidence remains bound to its exact builds. The propagation fix does not admit arbitrary history gaps or prove historical owner epoch. G40 deployment-broker profile is still UNRESOLVED (broker, server and session/offset rules unset).
Full SIG06 still requires accepted same-feed historical boundary/session authority, a source-proven owner epoch, and successful production continuous/recovered parity across that boundary. No MLV/Re-Entry, merge, deployment or auto-entry promotion.

Evidence: mhv613_availability_evidence.tar.xz, SHA256 dabc0aa4f454ec8ee1bdfdc48841fd639340a0672a899821200daf14d0ff88aa, 41676 bytes. Archive readback checked every object. file_index.json maps logical files to SHA256-keyed objects; identical controller traces are stored once.
