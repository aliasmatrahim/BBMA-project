# BBMA Entry Mode Contract

Status: **LOCKED FOR CURRENT BLUEPRINT DEVELOPMENT CYCLE**

## Purpose
This contract defines what `EntryMode` means in the BBMA Professional EA. It prevents the old ambiguity where `AllSignals` could be interpreted as "every detected BBMA signal may immediately open a trade."

## Source rule
BBMA source material distinguishes signals from setups and describes a lifecycle/cycle in which signals such as Extreme, CSD/eCSD and CSM provide context/confirmation, while actual entry eligibility depends on the relevant BBMA confirmation/retest/re-entry structure.

Therefore **raw detection is not equivalent to execution eligibility**.

## EntryMode 1 — RE_ENTRY_ONLY
Only fully validated BBMA Re-Entry opportunities are eligible for execution.

Requirements:
- Re-Entry must satisfy the applicable BBMA type contract.
- Re-Entry lifecycle must be authoritative and confirmed.
- Direction/trend requirements must follow the BBMA source for that Re-Entry type.
- Candidate/unconfirmed Re-Entry is not execution-eligible.
- Risk, SL/TP and execution validation still apply after BBMA eligibility.

Expected behavior: fewer, more selective trades.

## EntryMode 2 — ALL_VALIDATED_BBMA_ENTRIES
All BBMA entry opportunities that are explicitly valid under the BBMA source may be considered for execution.

This does **NOT** mean "all detected signals".

Rules:
- Extreme detection alone is not sufficient; the source-required confirmation/retest contract must be satisfied before entry eligibility.
- MLV is a setup/context structure and is not automatically a direct entry merely because it exists.
- CSD/eCSD are direction/intent information and do not automatically execute a trade merely because detected.
- CSM is momentum/context and does not automatically execute a trade merely because detected.
- Re-Entry is eligible only after its applicable BBMA type contract is satisfied.
- REM/RRE/REE are eligible only when their complete source-defined multi-timeframe combination contract is satisfied.
- Raw `Valid=true` at detector level must never bypass the entry-eligibility layer.

Expected behavior: more trades than EntryMode 1, but still only source-validated BBMA entries.

## Global prohibition
No generic rule such as "minimum 2 signals" or "any signal = entry" may be added unless explicitly supported by the BBMA source or explicitly approved as non-BBMA project logic.

## Architecture ownership
- M08–M12: detect and maintain source-defined signal/setup lifecycle.
- M13: collect/combine only; no execution authority.
- M14: validate source-defined sequence/combination contracts.
- M15: final signal/entry authority across eligible candidates.
- M16: conflict/invalidation authority.
- M17+: SL/TP, risk and execution validation after BBMA entry eligibility.
- M27: orchestrator only.

## Development consequence
The existing input comment `EntryMode: 1=ReEntryOnly, 2=AllSignals` is semantically deprecated. During the relevant blueprint repair it must be renamed/mapped to:

- `1 = RE_ENTRY_ONLY`
- `2 = ALL_VALIDATED_BBMA_ENTRIES`

No raw-signal execution path may remain when the blueprint is promoted to LOCKED status.

## Step 6 implementation status
P0 Step 6 implements this contract in M15/M27.

Current eligible execution-candidate set after Issue #175:
- Mode 1: confirmed H1 Re-Entry only;
- Mode 2: standalone H1 Extreme at `RETEST/ENTRY-READY`, confirmed H1 Re-Entry, plus validated REM/RRE/REE.

RAW Extreme and reversal-only standalone Extreme remain non-executable. MLV, CSD, eCSD and CSM also remain non-executable by themselves.

Issue #175 closes the previous standalone-Extreme execution gap with the user-approved H1-only project mapping in `blueprint/decisions/Q5_STANDALONE_EXTREME_EXECUTION_POLICY_DECISION_20260917.md`. The M08 Extreme lifecycle remains authoritative; Mode 2 does not create a raw-signal execution path.

M15 now sees BUY and SELL candidates in one atomic pair-level pool. If validated opposite-direction candidates coexist, no winner is invented and no final trade decision is created for that cycle.

Detailed implementation contract:
`blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`.
