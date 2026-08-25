# BBMA Home Course 19-Page — Canonical Row Normalization Map

Status: MECHANICAL NORMALIZATION GATE COMPLETE
Date: 2026-08-25
Source ledger: `HOME_COURSE_19P_ATOMIC_LEDGER_20260825.md`
Parent mapping gate: `HOME_COURSE_19P_CORE_V2_MAPPING_GATE_20260825.md`
Target: `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`

## Purpose

This gate normalizes the 189 provenance rows into canonical semantic families so the Workbook audit can move from qualitative mapping to a reproducible coverage calculation. Provenance rows are never deleted: repeated summary/restatement rows point to the same canonical family rather than inflating the denominator.

## Normalization contract

Each source row receives these logical fields:

`source_row | canonical_rule_id | duplicate_of | applicability | core_v2_mapping | status`

Applicability:
- `A` = Strategy-Core applicable evidence.
- `N` = NON_CORE evidence excluded from denominator.
- `H` = applicable evidence requiring reconciliation; remains in denominator but cannot be counted COVERED.
- `D` = provenance duplicate/corroboration; points to an existing canonical family and does not create a new denominator item.

Statuses:
- `COVERED`
- `PARTIAL`
- `MISSING/HOLD`
- `NON_CORE`
- `DUPLICATE/CORROBORATION`

## Canonical family map

### C001 — BB indicator/structure contract — COVERED
Rows: HC-P01-005, HC-P01-008, HC-P01-009, HC-P01-010; Mid/outer BB structural restatements.
Core: §2, §4.

### C002 — BB state/shape semantics — COVERED
Rows: HC-P01-006, 007, 011, 012, 013, HC-P02-001, HC-P02-010.
Core: §4.

### C003 — Directional outside-BB Momentum/CSM — COVERED
Rows: HC-P02-007, 008, 011; HC-P04-009; HC-P08-005, 006, 007, 011, 012 and summary restatements.
Core: §4.

### C004 — Horizontal BB non-directional Momentum distinction — COVERED
Rows: horizontal-vs-directional BB interpretation excluding the explicit reversion table.
Core: §4.

### C005 — Horizontal-BB reversion behavior table — MISSING/HOLD
Rows: HC-P02-002, 003, 004, 005.
Reason: full wick/body/close -> Mid-BB behavioral table is not canonical Core.

### C006 — Absolute 10–20 pip horizontal-BB breakout claim — MISSING/HOLD
Row: HC-P02-009.
Reason: absolute pip/predictive wording.

### C007 — Mid-BB Buying/Selling Zone names — PARTIAL
Rows: HC-P03-002, 004, 005 and summary restatements.
Core has Mid-BB structure but not named-zone execution contract.

### C008 — Mid-BB zone opportunity instruction — PARTIAL
Rows: HC-P03-003, 006.
Reason: source instructs looking for entries by zone; Core does not make zone alone entry authority.

### C009 — Mid-BB slope same-TF trend guide — PARTIAL
Row: HC-P03-007.

### C010 — MA5 High/Low indicator contract — COVERED
Rows: HC-P04-003, 005.
Core: §2.

### C011 — MA5 structural position in falling market — COVERED
Rows: HC-P04-007, 008.

### C012 — MA5-close Momentum strength semantics — MISSING/HOLD
Rows: HC-P04-010, 011.
Reason: Core validity is outer-BB + accepted BB state; MA5 relationship may be strength context rather than independent Momentum validity.

### C013 — MA10 High/Low indicator contract — COVERED
Rows: HC-P05-001, HC-P06-001.
Core: §2.

### C014 — Direction candle MA10/Mid-BB ladder — COVERED/PARTIAL
Rows: HC-P05-004, 005, 006, 007; HC-P11-001, 002, 004 and summary restatements.
Core covers eCSD/CSD distinction; Workbook's complete strength ladder remains PARTIAL.

### C015 — MA5/MA10 ordering/transition structure — COVERED
Rows: HC-P06-003, 004, 005, 006; HC-P07-005, 006.

### C016 — MA50 indicator/trend reference — COVERED
Rows: HC-P07-001, 003, 004; structural restatements.
Core: §2 and higher structural/trend sections.

### C017 — BBMA basic laws / Extreme raw role — COVERED
Rows: HC-P08-001, 002, 003, 004; HC-P09-001, 002 and summary restatements.
Core: §5.

### C018 — Mid-BB direction confirmation/retest family — PARTIAL
Rows: HC-P08-014, 015, 016.
Core structurally uses Mid BB/eCSD/CSD but does not expose the exact break-retest-failure rule as a standalone universal contract.

### C019 — Extreme reversal-confirmed lifecycle — COVERED
Rows: HC-P09-003, 004, 005.
Core: §5.4.

### C020 — Extreme retest / standalone entry-ready lifecycle — COVERED
Row: HC-P09-006 and restatements.
Core: §5.1, §5.4.

### C021 — Extreme TP-Wajib — COVERED
Rows: HC-P09-007 and summary restatements.
Core: §5.2; Core refinement preserves opposite MA5/10 as first objective and Mid BB as farther context.

### C022 — MHV terminology/provenance after Extreme — COVERED
Rows: HC-P10-001, 002, 003, 006.
Core: §6.1–6.3.

### C023 — MHV marked-body/retest lifecycle — COVERED
Rows: HC-P10-004, 005 and summary restatements.
Core: §6.3–6.4.

### C024 — MHV post-event management based on Momentum/no-Momentum — PARTIAL/HOLD
Rows: HC-P10-007, 008, 009, 010.
Core models stage progression but not every deterministic TP/hold instruction.

### C025 — Direction signal is context, not direct entry authority — COVERED
Rows: HC-P12-012, 013, 014.
Core: §3 and Re-Entry contract.

### C026 — Re-Entry MA5/MA10 non-exceedance — COVERED
Rows: HC-P12-002, 010; HC-P13-015 and summary restatements.

### C027 — Powerful Re-Entry MA5+MA10+Mid-BB confluence — COVERED
Rows: HC-P12-003, 004, 015; HC-P13-018 and summary restatements.

### C028 — Re-Entry minimum three-candle wording — COVERED
Rows: HC-P12-004, 015; HC-P13-001 and summary restatements.
Core contains source-supported minimum-three-candle wording.

### C029 — Re-Entry principal/add-on entry role — COVERED
Rows: HC-P12-001, 005, 014; HC-P13-009 and summary restatements.

### C030 — Sideways/ranging -> Re-Entry structure — COVERED
Row: HC-P12-007 and summary restatements.

### C031 — Opposite/new Extreme -> TP/new cycle — COVERED
Row: HC-P12-009 and lifecycle restatements.
Core new-cycle supersession rules cover the canonical structural meaning.

### C032 — Nested MTF lower-TF replay inside HTF Re-Entry window — PARTIAL
Rows: HC-P13-002, 003, 004, 005, 006, 007, 008.
Core covers MTF scaling/alignment and exact REM/RRE/REE signatures, but not unrestricted Workbook replay/add-on authority.

### C033 — Follow major trend / HTF alignment — COVERED
Rows: HC-P13-010, 014, 017; HC-P14-002 and compatible restatements.

### C034 — Candle Arah outer-BB destination — PARTIAL/HOLD
Rows: HC-P13-011, 012, 016.
Direction intent is represented; guaranteed universal outer-BB destination is not.

### C035 — Direction reaches outer BB before Re-Entry/no Momentum -> hold — MISSING/HOLD
Rows: HC-P11-005, HC-P13-013, HC-P14-001 and equivalent summary restatements.
Material execution/TP exception.

### C036 — Direction must be followed by Re-Entry — COVERED
Row: HC-P11-006 and cycle restatements.

### C037 — MA50/D1 major-trend ownership context — PARTIAL
Rows: HC-P14-003, 004, 005, 011, 012, 013, 015.
Core has higher structural ownership but Workbook's broad D1/MA50 wording is stronger.

### C038 — Universal D1 precedence over H4 — MISSING/HOLD
Row: HC-P14-014 and equivalent summary wording.
Reason: may conflict with explicit project owner contract.

### C039 — Double H1 Extreme -> H4 MHV inference — MISSING/HOLD
Rows: HC-P14-006, 007, 009.
No canonical deterministic detector in Core.

### C040 — Valid H4 MHV -> lower-TF Extreme shortcut — MISSING/HOLD
Row: HC-P14-008.
Would expand execution authority.

### C041 — Valid H4 MHV means no further H1 MHV — MISSING/HOLD
Row: HC-P14-010.
Absolute wording not canonical.

### C042 — D1 predictive next-day wording — MISSING/HOLD
Workbook rows asserting today's D1 close determines tomorrow's movement.
Directional context is not promoted into guaranteed prediction.

### C043 — Momentum -> Re-Entry continuation lifecycle — COVERED
Workbook Momentum/Re-Entry lesson and summary rows.
Core: §3 cycle and Re-Entry progression.

### C044 — Re-Entry -> no Momentum => mandatory TP/reversal expectation — MISSING/HOLD
Workbook lifecycle rows and summary restatements.
Core does not currently grant universal deterministic exit authority from this statement.

### C045 — First-candle validation / later entry wording — COVERED
Workbook first-candle/second-candle entry wording.
Core represents this through accepted Re-Entry lifecycle constraints rather than raw first-touch execution.

### C046 — Most-powerful Re-Entry including MA50 — COVERED
Workbook MA5+MA10+Mid BB+MA50 strength wording.
Core has accepted powerful/most-powerful Re-Entry confluence.

### C047 — Nested smaller-TF setup generated by larger-TF sideways/replay — PARTIAL
Workbook nested replay/sideways wording.
Core contains structural MTF scaling but only approved executable signatures.

### C048 — Extrem Magic MA5+MA10 both outside BB — MISSING/HOLD
Workbook special rare structure.
No accepted universal detector/authority exists in Core V2.

### C049 — Canonical BBMA cycle summary — COVERED
Workbook final cycle: Extreme -> TP Wajib -> MHV -> Direction -> Re-Entry -> Momentum -> Re-Entry.
Core: §3.

## NON_CORE canonical buckets

N001 — MT4 menu/navigation instructions.
N002 — chart colors/line thickness cosmetics.
N003 — example EUR/USD instrument choice.
N004 — small-lot/large-lot/`lot besar` wording and discretionary position sizing.
N005 — news-event trading instructions.
N006 — account splitting/growth/withdrawal workflow.
N007 — emotional-trading/account-purpose material.
N008 — marketing/guaranteed wording where it cannot be converted to deterministic source-supported behavior.

All ledger rows in these buckets are excluded from Strategy-Core coverage denominator.

## Duplicate/corroboration normalization

The Workbook summary pages repeatedly restate earlier lessons. These repetitions remain provenance evidence but map back to C001–C049 rather than creating new canonical rules. Explicit ledger rows already marked `[D]`, such as HC-P04-009, HC-P12-010, HC-P12-015 and HC-P13-005, are duplicate/corroboration rows. Equivalent summary restatements are normalized the same way.

This prevents the summary section from artificially increasing either the denominator or the coverage numerator.

## Mechanical coverage result

After semantic deduplication and NON_CORE exclusion, the Workbook yields **49 canonical Strategy-Core families**.

Classification by family:
- Fully COVERED: **30**
- PARTIAL (including mixed covered/partial families): **8**
- MISSING/HOLD: **11**
- Total applicable canonical families: **49**

Strict full-coverage metric:

`30 / 49 = 61.22% fully covered`

Representation metric (COVERED + PARTIAL, without pretending PARTIAL is complete):

`(30 + 8) / 49 = 77.55% represented at least partially`

Unresolved material families:

`11 / 49 = 22.45% MISSING/HOLD`

Important: these are **canonical-family coverage metrics**, not raw-row coverage. Raw 189-row percentages would be misleading because the Workbook contains duplicates, summary restatements and NON_CORE rows.

## Gate conclusion

The mechanical normalization gate is complete. Core V2 captures the majority of the Workbook's canonical BBMA structure, but the forensic audit does **not** support claiming near-100% Workbook coverage.

The largest unresolved execution-sensitive gaps remain:
1. universal D1-over-H4 precedence;
2. Double H1 Extreme -> H4 MHV inference;
3. H4 MHV -> direct lower-TF Extreme shortcut;
4. post-direction/pre-Re-Entry hold behavior;
5. Re-Entry -> no Momentum mandatory TP/reversal behavior.

Nested MTF is confirmed **PARTIAL**, not absent: Core already contains MTF scaling/alignment and REM/RRE/REE architecture, while the Workbook describes a broader recursive lower-TF replay model.

## Next gate

Do not modify executable strategy from the HOLD families automatically. Next safe work is cross-source reconciliation of PARTIAL/MISSING families against the primary operational PDF, secondary PDF, Finale evidence and existing conflict register. Non-conflicting descriptive clarifications may be proposed for Core V2.x; execution-authority changes remain strategy-decision gates.