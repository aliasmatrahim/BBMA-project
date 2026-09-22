# Q10 MetaQuotes-Demo Acceptance — Build 5.11

Issue: #109
Frozen candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

This tooling prepares and controls the final broker/demo acceptance programme. It does not modify the BBMA EA source and does not store, request or bypass broker credentials.

## Frozen identities

- candidate freeze commit: `78ddbd771853681de6628032701eea7231e05d61`
- canonical MQ4 SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`
- native EX4 SHA-256: `CFF8DA584C91AE177CA26E1C47518AA585A67F0E16C99295F932670E8CDEC6E1`
- approved final-integration settings SHA-256: `37BC585EB3AB5A73914FEC3C532023636D4FACCD7D3AAAF20B774269CF92DA70`
- demo identity probe EX4 SHA-256: `AD47BA707F35862239C4A29ACFC257220DC6CE9252C2F70C67AAC8B04FC888D8`

The runner also proves the current worktree has no EA-source diff after the frozen candidate commit.

## Safety sequence

1. Use a **dedicated MT4 installation/profile**, never the primary terminal path.
2. Authenticate that terminal manually to the approved MetaQuotes-Demo account. The runner never handles login/password data.
3. Place the exact compiled `Q10_DEMO_IDENTITY_PROBE.ex4` under the dedicated terminal's `MQL4/Experts`.
4. Generate the read-only probe startup configuration:
   `python blueprint/tools/q10_demo_acceptance.py generate-probe-launch ...`
5. The probe runs with `ExpertsTrades=false` and emits only:
   `Demo`, `Connected`, `TradeAllowed`, `Server`, `Company`, and terminal build.
   It does not log the account number.
6. Run `inspect-demo`. Formal Q10 remains `BLOCKED` unless:
   - `Demo=Y`;
   - `Connected=Y`;
   - server/company identifies the approved MetaQuotes demo provider.
7. Initialize resumable state with `init-state`. A PASS demo identity must come from a log under the same dedicated terminal root whose exact EX4/settings are bound into state; the primary-terminal guard is mandatory.
8. AUTO/formal stage order is locked:
   `R3 -> R4 -> R5 -> R6`.
9. A stage cannot be formally skipped. A `FAIL` blocks later formal promotion.
10. Runtime candidate launch generation requires the exact native EX4/settings hashes and an already-PASS demo-auth gate.

## Commands

Candidate identity:

```
python blueprint/tools/q10_demo_acceptance.py verify-candidate --repo-root .
```

Generate safe identity-probe launch config:

```
python blueprint/tools/q10_demo_acceptance.py generate-probe-launch \
  --terminal-root <dedicated-mt4-root> \
  --probe-ex4 <dedicated-mt4-root>/MQL4/Experts/Q10_DEMO_IDENTITY_PROBE.ex4 \
  --primary-terminal <primary-terminal.exe> \
  --output-ini <dedicated-mt4-root>/q10_probe.ini
```

Classify demo evidence:

```
python blueprint/tools/q10_demo_acceptance.py inspect-demo \
  --log <dedicated-terminal-experts-log> \
  --output <evidence>/demo_identity.json
```

Initialize state:

```
python blueprint/tools/q10_demo_acceptance.py init-state \
  --repo-root . \
  --demo-log <dedicated-terminal-experts-log> \
  --terminal-root <dedicated-mt4-root> \
  --native-ex4 <dedicated-mt4-root>/MQL4/Experts/<exact-build511>.ex4 \
  --settings <dedicated-mt4-root>/<approved-settings>.set \
  --primary-terminal <primary-terminal.exe> \
  --output <evidence>/state.json
```

Query next formal stage:

```
python blueprint/tools/q10_demo_acceptance.py next-stage --state <evidence>/state.json
```

Generate runtime launch only after demo PASS:

```
python blueprint/tools/q10_demo_acceptance.py generate-launch \
  --state <evidence>/state.json \
  --stage R3 \
  --terminal-root <dedicated-mt4-root> \
  --native-ex4 <dedicated-mt4-root>/MQL4/Experts/<exact-build511>.ex4 \
  --settings <dedicated-mt4-root>/<approved-settings>.set \
  --primary-terminal <primary-terminal.exe> \
  --output-ini <dedicated-mt4-root>/q10_r3.ini
```

Collect attributable markers:

```
python blueprint/tools/q10_demo_acceptance.py collect-log \
  --state <evidence>/state.json \
  --stage R3 \
  --log <runtime-log> \
  --output-dir <evidence>/R3
```

Formal case analysis requires explicit case assertions. Marker presence alone cannot create PASS. PASS/FAIL evidence references must resolve to files registered in the collected stage bundle and must still match their recorded SHA-256:

```
python blueprint/tools/q10_demo_acceptance.py analyze-bundle \
  --stage R3 \
  --bundle <evidence>/R3/R3_bundle.json \
  --assertions <evidence>/R3/assertions.json \
  --output <evidence>/R3/analysis.json
```

Promote the formal stage only from that validated analysis artifact:

```
python blueprint/tools/q10_demo_acceptance.py record-stage \
  --state <evidence>/state.json \
  --stage R3 \
  --status PASS \
  --evidence <evidence>/R3/analysis.json
```

`record-stage` rejects missing/mismatched analysis schema, stage, status, candidate source or build identity.

## Status vocabulary

Only `PASS`, `FAIL`, `INCOMPLETE`, and `BLOCKED` are accepted.

- `BLOCKED`: demo authentication/environment unavailable.
- `INCOMPLETE`: authenticated runtime exists but mandatory evidence is not complete.
- `FAIL`: contradictory or unsafe evidence exists.
- `PASS`: every mandatory case for that stage is positively demonstrated.

No `BLOCKED` or `INCOMPLETE` result may be promoted to PASS.

## Current Build 5.11 bindings

- M15 remains sole processing clock.
- Strategy Core remains closed-candle.
- TradeLock:
  - `LOCK_OFF=0`;
  - `LOCK_SAME_DIRECTION=1`: existing exact-owned pair position permits same-direction additions and blocks opposite direction;
  - `LOCK_ONE_POSITION=2`: any existing exact-owned pair position blocks another on that pair.
- M12N remains observation/read-only.
- N3 execution policy remains `NONE`.

The case matrix is stored in `FINAL_BUILD511_STAGE_MATRIX.json`.

## Current environment

Per the explicit user decision on 2026-09-23, Q10 final demo-runtime acceptance uses MetaQuotes-Demo rather than requiring HFM. The original Issue #109 only requires attributable demo-account evidence; broker-specific HFM validation is not required to close this generic runtime gate. Q10 remains `BLOCKED / AUTH` until a dedicated MetaQuotes-Demo terminal is freshly authenticated and the read-only probe proves it.

## Clean restart helper

`q10_demo_clean_restart.ps1` validates the dedicated terminal/config plus the persisted Q10 state, requires `demo_auth.status=PASS` and a PASS candidate identity, requests `CloseMainWindow()`, waits for full exit/log flush, refuses forced termination by default, snapshots logs before/after close, then restarts only the dedicated terminal.

Dry-run validation without touching MT4:

```
powershell -NoProfile -ExecutionPolicy Bypass -File \
  blueprint/runtime/q10_demo_acceptance/q10_demo_clean_restart.ps1 \
  -TerminalPath <dedicated-mt4-root>/terminal.exe \
  -ConfigPath <dedicated-mt4-root>/q10_r3.ini \
  -EvidenceDir <evidence>/restart \
  -StatePath <evidence>/state.json \
  -PrimaryTerminalPath <primary-terminal.exe> \
  -DryRun
```

The helper never force-kills the terminal. If graceful close is not accepted or does not complete within the configured grace period, it returns `BLOCKED` and does not restart.
