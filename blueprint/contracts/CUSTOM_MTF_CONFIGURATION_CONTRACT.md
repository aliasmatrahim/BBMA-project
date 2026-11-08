# Custom MTF configuration admission — Build 5.93

Scope: engineering configuration only, T02 and T03 preparation. This contract grants no BBMA detection, selection or execution authority. Canonical module owners and M15 processing authority remain unchanged.

## Admission

`ValidateInputParameters` calls `InitializeCustomInputs` before `InitializeEA`. Five slots default OFF. An enabled slot requires Context and Trigger, with at most seven atoms across both. Referencing a disabled TF/signal or an unavailable owner mapping rejects initialization. All custom owner availability cells remain false in this milestone. Syntax recognition is not semantic availability.

Every helper initialization clears the previous payload, fingerprint, parsed counts and resolved symbol scopes. Failed helper initialization leaves no published configuration identity. Slot/matrix helpers are preparatory state; only successful whole-EA initialization can admit further runtime work. These tests do not authorize recovery of an open trade from changed inputs.

## Identity

The exact `g_custom_config_payload` records parser/slot schema, the TF and per-TF signal/availability matrices, enabled slot IDs and parsed formula groups/alternatives. Case, whitespace and equivalent parentheses normalize through the existing parser. AND/OR changes alter identity. Group/alternative ordering is retained. Disabled formula text is excluded. Signal-list order and duplicate tokens normalize through the enable matrix.

Resolved universe and per-slot actual symbol sets are appended using length-prefixed names. Aliases resolving to the same ordered actual set have the same identity. All slots share the primary resolved universe and their own subset.

The existing `SHORT_HASH` supplies a diagnostic 64-bit fingerprint. Retain the exact payload: a short-hash match alone is not proof of exact configuration equality. Neither identity is a physical trigger ID or execution-consumption key. Future risk, exit, priority and lifecycle settings must extend identity before those features can be activated. Restart persistence and frozen TradePlan ownership remain T07/T10 work.

## Symbols

`CustomSymbolMode` selects CHART_ONLY, MARKET_WATCH or CUSTOM_LIST. `CustomSymbolList` supplies the explicit list. `Custom1_Symbols` through `Custom5_Symbols` accept ALL or a comma-separated subset. ALL means the resolved primary universe, not the broker catalog. Disabled slot subsets are ignored.

Canonical `FindActualSymbol` is the sole resolver. Exact broker names win; a non-exact supported suffix match must be unique. Explicit full broker names can select a particular prefix/suffix variant. No additional fuzzy/prefix detector is introduced here. Empty tokens, unresolved/ambiguous symbols, failed selection and out-of-universe subsets fail closed. Repeated aliases collapse to one actual symbol. MARKET_WATCH names are snapshotted before resolver selection can change visibility, then frozen until reinit.

Custom universe capacity is checked against canonical `MAX_PAIRS` without truncation. The new lists do not replace canonical `PairList`, allocate PairState, assign magic numbers or start additional scans in this milestone. Arbitrary-symbol PairState/magic collision binding, history/spec/quote readiness, retained owned-position management and multi-symbol execution require later owner integration and runtime evidence. UI must not present this configuration milestone as active custom trading.

## Validation

Native pure helper suites exercise parser, slot admission, canonicalized identity, symbol resolution with broker-I/O fixtures and repeated helper initialization. Resolver fixture text is extracted from the current EA by the runner; it is not a second production resolver. Fresh log markers and assertion results determine PASS; process termination alone is insufficient. Full EA compile and full EA tester startup are distinct evidence scopes. Multi-symbol broker execution and terminal detach/attach recovery are not established by helper tests.
