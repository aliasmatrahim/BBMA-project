# SDD ledger — plan: docs/superpowers/plans/2026-11-08-custom-mtf-autoentry-plan.md

Approval: user approved design v1 and continued inline execution on 2026-11-08.
T01: IN PROGRESS; baseline.json and baseline audit record exact observations.
T02–T12: PENDING.
Pre-flight T02→T05: parsed groups and atom identities must be shared; interface consistent.
Pre-flight T04→T05/T06: CustomOwnerView must separate structural validity from entry eligibility.
Pre-flight T05→T07/T08: witness physical anchor and selected source components must remain exact.
Pre-flight T08→T09/T10: approved normalized geometry and initial R freeze before sizing/lifecycle.
Ruling: work in a clean scoped clone of observed owner, leaving dirty G40 historical checkout untouched — preserves user work — deployment identity still requires separate binding.
Ruling: document historical status/release layers without overwriting their canonical files — prevents false release promotion — current-status reconciliation remains separate.
Ruling: no parser production change before the native harness/eligibility mappings are established — respects native TDD/semantic gates — feature remains pending.
Evidence: C044 generation model PASS locally; pytest unavailable locally; no native custom compile/runtime run.

2026-11-08 continuation: native parser milestone only.
T01: native unit compiler/tester binding resolved; semantic availability mapping and deployment identity still partial.
T02: SYNTAX PARSER VERIFIED (native 30/30); slot aggregate bound, five-slot init and enable-matrix integration PENDING.
Evidence: parser_native_evidence.json; local/native parser and harness SHA-256 identities equal.
Ruling: isolate syntax parsing in one shared CustomFormula.mqh so the harness exercises exactly the reusable production parser — no detector split or duplicated parsing — costs one include integration in subsequent T02 steps.
Ruling: continue pure syntax milestone while CSA/CSAK/MHV/MLV mapping remains VERIFICATION REQUIRED — no signal evaluation or execution enabled — risk is limited to future availability gate integration, which remains mandatory.
Baseline red harness uses a test-only missing-capability adapter returning unavailable; 6 positive cases fail before parser exists, 17 rejection cases pass vacuously. Green harness calls real parser; 30/30 pass. This is not a failing production Strategy-Core regression.
Full local pytest cannot run (module unavailable); C044 generation model PASS; no global regression PASS claimed.
Exact next action: add aggregate Context+Trigger seven-atom validation, fixed five-slot schema and per-TF/signal availability checks, with native RED/GREEN tests, then integrate inputs under a new EA build identity.

Fresh parser review: no confirmed parser bugs; seven structural/state assertions added and run native, final 30/30 PASS. Full feature still incomplete.
