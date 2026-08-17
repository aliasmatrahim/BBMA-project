# P2 Step 14 — Broker Specification / Symbol Resolution Re-Audit

Status: PASS
Compile verification: 0 Errors / 0 Warnings (user-reported MetaEditor result)

## Re-Audit Result
The Step 14 defect is closed.

`FindActualSymbol()` now:
- trims and rejects empty requests;
- searches all broker symbols rather than only Market Watch;
- prefers an exact broker-symbol match;
- requires `SymbolSelect(..., true)` before accepting the exact match;
- permits a broker suffix/prefix variant only when exactly one candidate matches;
- returns an empty string for missing, ambiguous, or unselectable resolution.

`LoadPairs()` already rejects an empty resolved symbol before reading broker specifications, so unresolved/ambiguous symbols no longer flow into the broker-specification path.

No residual Step 14 defect was found in this scope. BBMA signal, entry, SL/TP and risk semantics remain unchanged.

Final: P2 Step 14 PASS (static re-audit + compile 0E/0W).