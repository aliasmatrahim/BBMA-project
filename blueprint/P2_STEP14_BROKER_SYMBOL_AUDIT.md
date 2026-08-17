# P2 Step 14 — Broker Specification / Symbol Resolution Audit

Status: FAIL — Fix A required

## Finding
`FindActualSymbol()` is not fail-closed. It scans Market Watch symbols and returns the first symbol whose name starts with the requested base. If no match exists it returns the original requested string rather than an explicit failure sentinel.

This creates two defects:
1. Ambiguous prefix matches can silently bind a configured pair to the wrong broker symbol when multiple names share the same prefix.
2. The `LoadPairs()` check `if(actual == "")` cannot detect a missing symbol because `FindActualSymbol()` falls back to `symbol`.

`LoadPairs()` then reads broker specifications from that resolved value and may spend retries validating an unresolved/nonexistent symbol. Symbol selection is not made authoritative before broker-spec reads.

## Required Fix A
Make symbol resolution deterministic and fail-closed:
- prefer exact selected/all-symbol match;
- otherwise allow a suffix/prefix broker variant only when exactly one candidate matches the configured base;
- call `SymbolSelect(candidate, true)` before accepting it;
- return empty string on missing, ambiguous, or unselectable resolution;
- keep `LoadPairs()` rejection on empty resolution.

No BBMA signal, entry, SL/TP, or risk-formula semantics should change.