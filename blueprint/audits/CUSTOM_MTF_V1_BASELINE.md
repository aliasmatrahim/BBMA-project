# Custom MTF v1 — T01 checkpoint

Issue #302; branch feat/custom-mtf-v1-20261108; observed owner 459c0588e625d7f7630f0fb5612b7f04fda496de.

## Verified observations
- Clean isolated clone from d1-owner-dev; EA source unchanged, Build 5.15.
- CURRENT Build 5.14 and release identity 4.59 describe different historical layers; do not rewrite the release marker as a new deployment.
- Source LF SHA 49da4fbf9aae347530dd45d47902f81e422600825438b62b80757435d69f8504; CRLF SHA b9f3876f61645b2f98009a4251a4142edc7644ed728e41edeca245ff1e243c45 exactly matches stored Build 5.15 evidence. This is line-ending normalization, not a source defect.
- G40 online; direct file access and command output recovered. Existing checkout uses historical branch and contains untracked files; left untouched.
- MetaEditor 5.0.0.2425 located under D:\BBMA\MT4_ReEntryTiming_515_20261107. No compile/run performed there.
- C044 generation model executed locally and passed its 145 normal/85 frozen operation matrix. This does not verify the new feature.
- Local pytest attempt failed because pytest is not installed; no suite PASS claim.

## Dependencies
- #301: EntryCandle window, Draft Build 5.16, afb206aac93e82322b3a33318e06fb0b0e6912c9.
- #299: MHV range intersection, Draft, 2f0c50f044cb40e32b8ec44a6fa5965c09a31270.
- #293: source/data audit, Draft, cdf8b78d23fa5505b36568e2f03f3748537bbd1f.
- #282: separate N3 active-selection research; no authority adopted.

## Remaining T01
Bind isolated native compiler/tester command and process/ownership inventory; complete per-signal maturity/eligibility evidence rows via SOURCE_INDEX, especially CSA/CSAK; verify deployment source/EX4 separately from this owner clone.

## Exact next action
Reuse baseline.json and this branch. Finish native runner binding without restarting the primary MT4 or changing historical checkout; then execute T02 native parser cases against production MQL4. Do not duplicate completed baseline hashes/audits. T02–T12 PENDING; no EA source changes, no activation, no native custom runtime proof.

## Native parser continuation — 2026-11-08
Dedicated root D:\BBMA\MT4_CustomMTF_302_Unit created from existing native binaries and copied history; no primary terminal restart, no account opened, offline proxy retained, ExpertsTrades=false. First launch was blocked by the account wizard and missing symbol metadata; dismissing initialization dialogs and supplying the existing MetaQuotes-Demo server metadata allowed the pure harness to run. Compiler 5.0.0.2425; terminal 1492.

Parser helper compiled 0E/0W, native 30/30 syntax cases PASS. Red phase was a test-only missing-capability adapter (17 rejected-input cases trivially pass, 6 accepted-input cases fail), not a production-core regression. Green phase uses the exact new header, with native/local file hashes matched. The canonical EA remains byte-identical. T02 is not complete: schema, aggregate Context+Trigger bounds, enable matrices and EA integration are pending.

Stored evidence excludes account/authentication log rows. Bar history only hosts the unit harness; no data coverage/profitability or broker-execution claim follows.
