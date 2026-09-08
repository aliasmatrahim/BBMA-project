# C10 Issue #122 / #123 Acceptance Matrix — 2026-09-08

Status basis: exact Build 4.81 successor for #122 plus inherited Build 4.80 writer-namespace repair for #123. No canonical activation.

## Issue #122
| Acceptance criterion | Status | Evidence |
| --- | --- | --- |
| deterministic lagged-M5 regression | PASS | `validate_122.ps1`: `C10_122_LAGGED_M5_MODEL=PASS` |
| no pre-enrollment candle can produce outcome | PASS (deterministic) | `C10_122_PREENTRY_REPLAY_MODEL=PASS`; exact enrollment guards retained |
| active checkpoint recoverable across physical restart | **PENDING** | fresh broker-clock Build 4.81 ACTIVE has not yet appeared |
| corrupt/missing history fail-closed | PASS | zero/regressed/missing-history models PASS; live missing-enrollment cases produce UNKNOWN |
| native MetaEditor compile 0E/0W | PASS | 464 ms verification compile; 419 ms exact deployment-name compile |
| live/isolated runtime with 0 broker actions + Authority=NONE | PASS so far | live Build 4.81: no broker markers / no ledger disable; tester Total trades=0 |

Issue #122 remains OPEN solely because the physical ACTIVE restart criterion is not yet directly evidenced.
## Issue #123
| Acceptance criterion | Status | Evidence |
| --- | --- | --- |
| deterministic concurrent-instance regression | PASS | Build 4.80 #123 namespace/reporter checks PASS |
| two evidence instances initialize/write without file-open race | PASS (observed) | mixed broker-connected Build 4.74 + 4.80 owner-separated runtime evidence |
| no malformed/interleaved rows, duplicate IDs, cross-build contamination | PASS for reviewed evidence | provenance-domain audit + reporter fixture PASS |
| checkpoint ownership remains correct | PASS | checkpoint remains instance/config namespaced; #123 change did not alter checkpoint owner model |
| native MetaEditor compile 0E/0W | PASS | exact Build 4.80 native compile 0E/0W; Build 4.81 successor also 0E/0W |
| restart reaches recovery path instead of ledger-open failure | **PENDING final live successor proof** | latest accepted successor Build 4.81 still waiting for fresh ACTIVE physical restart |
| 0 broker actions; trading authority unchanged | PASS so far | Authority=NONE evidence; zero broker-action markers |

Build 4.81 source diff changes #123 writer ownership only by the required new BuildID/SourceHash identity; writer-namespace algorithm itself is unchanged. Therefore the pending physical restart should be performed on Build 4.81 rather than reactivating stale Build 4.80, but Issue #123 stays OPEN until that successor evidence is reviewed against the original acceptance wording.