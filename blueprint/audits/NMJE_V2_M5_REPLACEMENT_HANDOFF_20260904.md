# NMJE v2 / M5 Replacement Workstream Handoff — 2026-09-04

## Status
**PREPARED / ISOLATED / DRAFT-ONLY / NO MERGE / NO ACTIVATION**

Replacement branch:
`nmje-v2-m5-rebuild-dev`

Stack base:
`nmje-n3-hardening-dev@415a936aecb06855cafff8814c758351f8ff6111`

Locked reconciled EA source lineage:
- source-bearing baseline commit: `13f6a95c5065a00e4e451503171eca7e700864c6`;
- baseline relock commit: `415a936aecb06855cafff8814c758351f8ff6111` (docs-only);
- EA Git blob: `4184ca0e03d9a40cc1aba89c05dadb8b08caeeb1`;
- repository SHA-256: `21634e5557f41f3e5e15e87039151eccd08b4fab67b84e71d04f7f107c4d7354`;
- visible build: `Version 4.6.2 - N3 D1 Epoch + F7 Reconcile` / `#property version "4.62"`.

This preparation commit does **not** modify `blueprint/source/BBMA_EA.mq4`; therefore no new build identifier is required yet.

## Authority firewall
- D1 remains strategic owner.
- H4 remains higher owner / journey context.
- H1 remains setup context.
- M15 remains sole processing and final-decision clock.
- M5 is closed-candle lower-TF context/refinement only.
- M5 may not create, reject, independently rank, delay, risk-approve or execute a trade.
- M22 remains sole `OrderSend` owner.
- NMJE execution policy remains `NONE` / inactive.
- `EnableD1TPWLifecycle=false` remains mandatory for this workstream.
- `EnableC044Lifecycle=false` remains mandatory for this workstream.
- No W1, M30 or primary M1 authority is introduced.

## Superseded / quarantined lineage
Existing PR #102 / branch `nmje-v2-m5-dev` is retained as evidence only and is **not** the continuation base.

Validated corruption boundary from Issue #101:
- P9 `2ea3b450bae9e93d288e4ecd2a1b1b135dd68d61` = last demonstrated native-compile-clean point in the old sequence;
- P10 `d50178abcb74d2c9e8275c4010a8eb25cf111eb8` = first structurally corrupted source (`MODULE 17` truncation boundary);
- later old-lineage commits may inherit that corruption even if they carry restoration/test changes.

Rule for this replacement branch:
- do not merge PR #102 into this branch;
- do not cherry-pick old source-bearing commits blindly;
- old P1-P9 commits are reference/provenance only;
- rematerialize each intended change against the v4.62 baseline with smallest-diff review;
- reconstruct P10 only after the replacement P1-P9 state is clean;
- apply P11 only after reconstructed P10 passes all gates.

## Old clean-sequence reference map
Reference-only commits before the corruption boundary:
`1eb1350 -> be0b485 -> ed88b1c -> 2d13c9f -> 8476ce6 -> 1423af4 -> cd1fe90 -> 610142a -> 22849c5 -> e72354e -> d5cdcde -> e128061 -> 2ea3b45`.

These commits describe the previous Stage A / M5 lineage / closed-M5 acquisition / shadow classification / attribution / conflict / maturity / density / exact provenance / P9 audit sequence. They do not override the new baseline.
## Replacement implementation order
1. Re-establish Stage-A authority/lineage regressions on the v4.62 baseline.
2. Materialize M5 schema/data only on the existing M15 processing clock.
3. Add closed-M5 shadow relation/context without entry authority.
4. Re-establish durable shadow attribution and exact parent provenance.
5. Re-establish conflict subtype, journey maturity and structural-density metadata as descriptive/shadow state.
6. Re-run P9 SL semantic-source audit without changing approved geometry by accidental processing order.
7. Reconstruct P10 entry-displacement telemetry from the clean replacement source; research-only, no hard filter.
8. Reconstruct P11 first/continuation/new-journey lineage only after P10 is clean.

## Mandatory validation per source-bearing step
- source/module integrity and duplicate-owner check;
- relevant NMJE v2 stage selftest;
- N3 static guard;
- N3 authority / identity / recovery / replay regressions;
- native MT4 MetaEditor compile at 0 errors / 0 warnings;
- targeted regression proving M15/M16/M17/M19/M20/M21/M22 authority boundaries unchanged;
- runtime evidence only when the stage actually requires runtime proof.

Any EA source change must receive a new unique visible build/header identifier. Do not reuse `4.62` for a changed EA source.

## Python tooling
Python is available on the authorized laptop through `py -3.14` (Python 3.14.7). Use it for materializers, static/selftests, source-integrity checks, deterministic regression tooling and log/evidence analysis. Native MQL4 compilation remains MetaEditor-owned.

## Handoff invariant
This branch is the only intended continuation lineage for Issue #101 after the 2026-09-04 baseline relock. PR #102 remains quarantined evidence. No change in this handoff authorizes NMJE execution authority, D1TPW, C044, merge to `d1-owner-dev`, or any change to `main`.

## 2026-09-07 v4.63 baseline-sync overlay
This overlay supersedes the v4.62 continuation references above; the 2026-09-04 text remains historical provenance.

- Current stacked base: `nmje-n3-hardening-dev@ddf0742c81645a440fb2fdb86f594e158ff15ab3`.
- v4.63 source-bearing baseline commit: `cdb2f64246634944e310a88dc2cc361da4e057dc`.
- N3 evidence/CI head inherited from base: `ddf0742c81645a440fb2fdb86f594e158ff15ab3`.
- Replacement sync merge commit: `7aa2d880a5a9fb51f56b095335710ba78ead8d19`.
- EA Git blob: `56921997843e9f5e8680b0fd15c7b81f27d10de3`.
- EA SHA-256: `e2407559332c1b213e318dc2e4c06d64103b83cec49bae38bf3991302e6a2f4f`.
- Visible build: `Version 4.6.3 - N3 F7 Telemetry Reconcile` / `#property version "4.63"`.
- C044 remains OFF; D1TPW remains OFF; NMJE execution authority remains NONE/inactive.
- M15 remains sole processing/final-decision clock; M22 remains sole OrderSend owner.

The sync does not introduce a replacement-branch EA delta relative to its current stacked base, so no additional build bump is required for the sync itself. All future source-bearing P1+ rematerialization must advance the visible build identifier again.

Continuation order remains unchanged except every reference to the old v4.62 baseline now means this locked v4.63 baseline. PR #102 remains quarantined evidence only.
