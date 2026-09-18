# Build 4.81 C10 runtime progress — 2026-09-08

Status: **IN PROGRESS / NOT RUNTIME CLOSED**

## Exact runtime identity
- BuildID: `4.81`
- C10 SourceHash: `D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D`
- ConfigFingerprint: `E376D23AA953085D`
- Owner namespace: `O8960472FCDF1`
- InstanceID: `81`
- `ExpertsTrades=false`
- `MaxTradePerPair=0`
- `MaxTotalTrade=0`
- C10 authority: `NONE`

## Fresh broker-connected observations
The isolated Build 4.81 session has produced six C10 signal-event rows across three DecisionIDs.
- `REJ_INVALID_LOT`: 5 rows.
- `REJ_INVALID_SL`: 1 row.
- C10 shadow outcomes: 3 rows.
- `EXPIRY_UNPROVABLE`: 2 rows.
- `M5_ENROLLMENT_HISTORY_UNPROVABLE`: 1 row.

The NZDJPY shadow therefore exercised the corrected conservative enrollment-history behavior in a real broker-connected session: missing/unprovable exact M5 enrollment history became `UNKNOWN / M5_ENROLLMENT_HISTORY_UNPROVABLE`; it did not create a fabricated TP/SL/EXPIRED result and did not disable the C10 ledger.

## Safety/runtime marker audit
Filtered Build 4.81 expert log rows: `1253`.
- `OrderSend=0`
- `OrderClose=0`
- `OrderModify=0`
- `OrderDelete=0`
- `DEC_EXECUTED=0`
- `LEDGER_DISABLED=0`

Current checkpoint snapshot contains three `SEEN` rows and zero `ACTIVE` rows. This is not physical-restart acceptance evidence.

## M5 history state after warm-up
A direct HST freshness audit found all 20 configured M5 histories present and advanced through broker-time `2026-09-08 00:45`. The earlier NZDJPY enrollment failure was therefore transient/provenance-sensitive at the enrollment instant rather than justification to relax the exact-history requirement.

No history file was edited. No strategy, risk, execution or lifecycle setting was changed to force an ACTIVE row.

## Remaining acceptance gate
Wait for one genuine fresh geometry-valid C10 shadow whose expiry is still future and whose exact enrollment/prior M5 anchors are provable. The detached watcher must then capture the ACTIVE row, physically stop and restart the same isolated terminal, and run the hardened Build 4.81 verifier.

Required final PASS remains: exact frozen identity recovery, post-restart `SHADOW_RECOVERY Active=1`, no pre-enrollment outcome, no ledger disable, duplicate-free exact provenance domain, `Authority=NONE`, and zero broker actions.

Artifacts in this directory are progress evidence only; they do not close Issue #122 or authorize merge/promotion.
