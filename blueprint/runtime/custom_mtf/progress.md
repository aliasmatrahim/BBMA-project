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

Slot schema milestone: native 11/11 PASS, compile 0E/0W (MetaEditor 2425, MT4 1492). Missing-capability adapter baseline 8 pass/3 fail.
Implemented CustomSlotConfig, IDs 1–5, aggregate Context+Trigger <=7, nonempty enabled fields, disabled-empty acceptance, TF/signal/user-enable and semantic availability matrix rejection. Parsed fields staged locally and committed only on full validation.
Fresh review: no important correctness bug. Per-cell indexing/output publication reviewed statically; native harness asserts return values only.
T02 remains PARTIAL: EA input integration/config hash/initialization regression not complete. Core EA unchanged and auto-entry OFF.
Exact next action: integrate five-slot inputs with canonical initializer under a unique EA build identity; availability remains fail-closed until owner mappings verified.

M10 reconciliation checkpoint: Build 5.90 shared MA-pair helper now applied on custom branch. Numeric equivalence 19683/19683; full native compile 0E0W, 999ms; independent review no new fix required. Native EA runtime NOT RUN. CSA must not alias eCSD; source terminology findings and consumer map: CUSTOM_MTF_M10_DIRECTION_RECONCILIATION_20261108.md. Prior blanket source-conflict diagnosis superseded by alias verification scope. T02 input integration and T03–T12 remain pending/partial. No merge or trading activation.

Build 5.91 input admission checkpoint: five Enable/Context/Trigger inputs and seven TF flags with per-TF signal lists integrated before InitializeEA. Defaults OFF; owner availability deliberately false. Native full compile 0 errors/0 warnings (1077ms); input helper harness compile 0E0W and 3/3 admission cases pass. Static wiring RED/GREEN and M10 19683-case equivalence pass. Fresh review: no new fix required. Full EA runtime NOT RUN; global pytest unavailable. T02 remains partial: configuration identity and broader init/reinit regression pending. No custom auto-entry activation. Evidence: input591_evidence.json.

Build 5.92: canonical parsed payload + existing SHORT_HASH diagnostic fingerprint; native 11/11 identity assertions and full native compile 0E0W (699ms). Exact payload retained; fingerprint never becomes physical event authority. Evidence identity592_evidence.json.

Build 5.93: CHART_ONLY/MARKET_WATCH/CUSTOM_LIST universe and per-slot ALL/subset admission, canonical resolver reused, alias collapse, ambiguity/out-of-universe rejection, frozen watch snapshot; configuration only, no custom PairState/scan/execution. Fixed ignored MQL4 trim return values (native red then green). Native parser30/slot11/identity11/symbol13 assertions pass; six repeated-helper-init cases pass with complete presets and exact reason assertions. Initial runner contamination was detected and corrected. Full native compile 0E0W 1101ms; matching source/includes/harness hashes. Independent review no new fix required. Actual EA negative OnInit cases PASS; valid startup blocked SYMBOL_UNRESOLVED:GBPUSD. Native broker probe confirms catalog all29/selected23, SymbolSelect false error4059, chart Point=0.00001. Full positive runtime NOT VERIFIED. Global pytest unavailable. T01–T03 remain partial; T04–T12 pending; all semantic availability closed. Next: minimum canonical chart-only tester resolver compatibility fix, then repeat actual startup; do not bypass non-chart ambiguity/spec gates. No merge/activation.
