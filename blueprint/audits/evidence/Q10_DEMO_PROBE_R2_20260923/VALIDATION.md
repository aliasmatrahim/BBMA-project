# Q10 Demo Identity Probe R2 Validation

Issue: #109
Date: 2026-09-23

Result: **PASS**

The read-only identity probe now tolerates MT4 login occurring after EA `OnInit()`: it emits the initial identity, then a timer re-emits once when `IsConnected()` becomes true.

- Native MetaEditor: 0 errors / 0 warnings.
- No `OrderSend`, `OrderClose`, `OrderModify`, or `OrderDelete`.
- No account number or credential logging.
- Targeted Q10 pytest: 13/13 PASS.
- Full pytest: 35/35 PASS.
- Build 5.11 candidate verification: PASS.
- EA source diff: zero.
