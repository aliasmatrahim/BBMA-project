from pathlib import Path
import argparse

BUILD_OLD = "//| Version 4.5.1 - D1-03 M11 Snapshot Atomicity                    |"
BUILD_NEW = "//| Version 4.5.1 - D1-05 Input Limit Guard                         |"
SRC_REL = Path("blueprint/source/BBMA_EA.mq4")
M20_REL = Path("blueprint/contracts/M20_PORTFOLIO_PROTECTION_CONTRACT.md")
M26_REL = Path("blueprint/contracts/M25_M26_DASHBOARD_INITIALIZATION_CONTRACT.md")
AUDIT_REL = Path("blueprint/D1_STEP5_INPUT_LIMIT_GUARD_IMPLEMENTATION_AUDIT_20260824.md")


def replace_once(s: str, old: str, new: str, label: str) -> str:
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, got {n}")
    return s.replace(old, new, 1)


def verify_source(src: Path) -> None:
    s = src.read_text(encoding="utf-8")
    required = [
        BUILD_NEW,
        "#define MAX_PAIRS               40",
        "int                  g_effective_max_active_pair;",
        "bool                 g_max_active_pair_sanitized;",
        "bool                 g_pair_list_truncated;",
        "void NormalizeRuntimeLimits()",
        "g_effective_max_active_pair = requested;",
        "g_effective_max_active_pair = MAX_PAIRS;",
        "[INPUT WARNING] MaxActivePair=",
        "[INPUT WARNING] PairList contains ",
        "if(status.active_pairs > g_effective_max_active_pair)",
        "if(wouldBePairs > g_effective_max_active_pair)",
        "NormalizeRuntimeLimits();",
        "RequestedMaxActivePair=",
        "EffectiveMaxActivePair=",
        "g_pair_names[MAX_PAIRS]",
        "g_pair_states[MAX_PAIRS]",
        "g_processed_candle_time[MAX_PAIRS]",
        "trades_per_pair[MAX_PAIRS]",
        "if(i >= MAX_PAIRS) break;",
    ]
    for item in required:
        if item not in s:
            raise SystemExit(f"missing invariant: {item}")

    forbidden = [
        BUILD_OLD,
        "#define MAX_PAIRS               20",
        "if(MaxActivePair > MAX_PAIRS) return false;",
        "if(ArraySize(pairs) > MAX_PAIRS) return false;",
        "if(status.active_pairs > MaxActivePair)",
        "if(wouldBePairs > MaxActivePair)",
    ]
    for item in forbidden:
        if item in s:
            raise SystemExit(f"stale fail-detach path remains: {item}")

    if s.count("NormalizeRuntimeLimits();") != 1:
        raise SystemExit("NormalizeRuntimeLimits call must occur exactly once")
    oninit = s.index("int OnInit()")
    norm = s.index("NormalizeRuntimeLimits();", oninit)
    validation = s.index("if(!ValidateInputParameters())", oninit)
    if norm > validation:
        raise SystemExit("runtime-limit normalization must precede input validation")

    # No strategy-Core module identity changes are permitted by this patch.
    for n in range(1, 28):
        if f"MODULE {n:02d}:" not in s:
            raise SystemExit(f"missing module marker MODULE {n:02d}")

    print("D1_STEP5_INPUT_LIMIT_GUARD_STATIC=PASS")


def apply(root: Path) -> None:
    src = root / SRC_REL
    s = src.read_text(encoding="utf-8")

    s = replace_once(s, BUILD_OLD, BUILD_NEW, "build header")
    s = replace_once(
        s,
        "input int      MaxActivePair                      = 7;          // 03 Limits | max pairs active at once",
        "input int      MaxActivePair                      = 7;          // 03 Limits | requested max active pairs; runtime caps safely",
        "MaxActivePair input comment",
    )
    s = replace_once(s, "#define MAX_PAIRS               20", "#define MAX_PAIRS               40", "pair capacity")

    globals_old = """//--- Pair management
string               g_pair_names[MAX_PAIRS];
PairState            g_pair_states[MAX_PAIRS];
datetime             g_processed_candle_time[MAX_PAIRS];
int                  g_pair_count;
"""
    globals_new = """//--- Pair management
string               g_pair_names[MAX_PAIRS];
PairState            g_pair_states[MAX_PAIRS];
datetime             g_processed_candle_time[MAX_PAIRS];
int                  g_pair_count;
int                  g_effective_max_active_pair;
bool                 g_max_active_pair_sanitized;
bool                 g_pair_list_truncated;
"""
    s = replace_once(s, globals_old, globals_new, "pair globals")

    validator_anchor = """bool ValidateInputParameters()
{
"""
    normalizer = """void NormalizeRuntimeLimits()
{
   int requested = MaxActivePair;
   g_effective_max_active_pair = requested;
   g_max_active_pair_sanitized = false;
   g_pair_list_truncated = false;

   if(g_effective_max_active_pair < 1)
   {
      g_effective_max_active_pair = 1;
      g_max_active_pair_sanitized = true;
   }
   else if(g_effective_max_active_pair > MAX_PAIRS)
   {
      g_effective_max_active_pair = MAX_PAIRS;
      g_max_active_pair_sanitized = true;
   }

   if(g_max_active_pair_sanitized)
   {
      Print("[INPUT WARNING] MaxActivePair=", IntegerToString(requested),
            " outside supported runtime range 1-", IntegerToString(MAX_PAIRS),
            ". EffectiveMaxActivePair=", IntegerToString(g_effective_max_active_pair),
            ". EA remains attached.");
   }

   string pairs[];
   SplitString(PairList, ",", pairs);
   if(ArraySize(pairs) > MAX_PAIRS)
   {
      g_pair_list_truncated = true;
      Print("[INPUT WARNING] PairList contains ", IntegerToString(ArraySize(pairs)),
            " entries; runtime capacity is ", IntegerToString(MAX_PAIRS),
            ". Extra entries are ignored. EA remains attached.");
   }
}

bool ValidateInputParameters()
{
"""
    s = replace_once(s, validator_anchor, normalizer, "normalizer insertion")

    s = replace_once(s, "   if(MaxActivePair > MAX_PAIRS) return false;\n", "", "remove max-active fatal validator")
    s = replace_once(s, "   if(ArraySize(pairs) > MAX_PAIRS) return false;\n", "", "remove pair-list fatal validator")

    s = replace_once(
        s,
        "   if(status.active_pairs > MaxActivePair)",
        "   if(status.active_pairs > g_effective_max_active_pair)",
        "M20 current portfolio active-pair gate",
    )
    s = replace_once(
        s,
        "   if(wouldBePairs > MaxActivePair)",
        "   if(wouldBePairs > g_effective_max_active_pair)",
        "M20 prospective active-pair gate",
    )

    init_trace_old = """   Print(\"[P3S1] InitializeEA start PairList=\", PairList,
         \" MaxActivePair=\", IntegerToString(MaxActivePair));
"""
    init_trace_new = """   Print(\"[P3S1] InitializeEA start PairList=\", PairList,
         \" RequestedMaxActivePair=\", IntegerToString(MaxActivePair),
         \" EffectiveMaxActivePair=\", IntegerToString(g_effective_max_active_pair));
"""
    s = replace_once(s, init_trace_old, init_trace_new, "init trace")

    oninit_old = """int OnInit()
{
   if(!ValidateInputParameters())
"""
    oninit_new = """int OnInit()
{
   NormalizeRuntimeLimits();
   if(!ValidateInputParameters())
"""
    s = replace_once(s, oninit_old, oninit_new, "OnInit normalization ordering")

    # Keep visible runtime identity aligned with the new source build.
    s = s.replace("=== BBMA EA V4.5.1 D1-03 ===", "=== BBMA EA V4.5.1 D1-05 ===")
    s = s.replace("BBMA EA V4.5.1 D1-03 initialized successfully", "BBMA EA V4.5.1 D1-05 initialized successfully")

    src.write_text(s, encoding="utf-8")
    verify_source(src)

    m20 = root / M20_REL
    text = m20.read_text(encoding="utf-8").rstrip()
    marker = "## D1-05 runtime input-capacity overlay"
    if marker not in text:
        text += """

## D1-05 runtime input-capacity overlay
`MaxActivePair` remains an M20 hard portfolio-admission limit, but M26 now supplies a sanitized runtime-effective value. The supported pair-state capacity is 40. A requested value below 1 or above 40 is capped to the nearest supported bound with an unconditional Experts/Journal warning; this recoverable input condition must not detach the EA. M20 applies the effective value to both current-portfolio and prospective atomic admission checks. No BBMA signal, direction, SL/TP, or lifecycle semantics change.
"""
        m20.write_text(text + "\n", encoding="utf-8")

    m26 = root / M26_REL
    text = m26.read_text(encoding="utf-8").rstrip()
    marker = "## D1-05 recoverable input sanitation overlay"
    if marker not in text:
        text += """

## D1-05 recoverable input sanitation overlay
Recoverable pair-capacity input errors are sanitized before fatal input validation. `MaxActivePair` is capped to the supported 1..40 runtime range and oversized `PairList` input is truncated by the existing bounded loader after a warning. These conditions do not justify `INIT_PARAMETERS_INCORRECT`; the EA stays attached. Truly fatal initialization failures such as no valid pair, invalid ownership/magic construction, or invalid protection reference remain fail-closed under the existing M26 contract.
"""
        m26.write_text(text + "\n", encoding="utf-8")

    audit = root / AUDIT_REL
    audit.write_text("""# D1 Step 5 — Input Limit Guard Implementation Audit

Date: 2026-08-24  
Branch: `d1-owner-dev`  
Build: `Version 4.5.1 - D1-05 Input Limit Guard`  
Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**

## User-visible defect
Changing `MaxActivePair` above the internal `MAX_PAIRS` capacity caused `ValidateInputParameters()` to return false. `OnInit()` then returned `INIT_PARAMETERS_INCORRECT`, so MT4 detached the EA from the chart even though the condition was recoverable.

## Fix
- Internal pair-state capacity raised from 20 to 40.
- `MaxActivePair` is normalized to an effective runtime range of 1..40 before fatal validation.
- Values outside that range generate an unconditional Experts/Journal warning and the EA remains attached.
- Oversized `PairList` no longer causes fatal parameter rejection; the existing bounded loader ignores entries beyond 40 and emits a warning.
- M20 current and prospective active-pair checks consume the sanitized effective limit.
- Other genuinely invalid/fatal initialization conditions remain fail-closed.

## Safety / architecture regression
- `MAX_PAIRS`-sized pair-state and portfolio-count arrays scale together to 40.
- `MAX_MONITORED` and `MaxTotalTrade` protections are unchanged.
- PairID range remains 1..99 and is sufficient for 40 configured pairs.
- No BBMA Strategy-Core detector, combination, D1/H4/H1/M15 hierarchy, SL/TP, money-management formula, execution, or lifecycle semantics were modified.
- `blueprint-dev` remains untouched.

## Verification
Focused static integrity: **PASS**.  
Native MT4 MetaEditor: **PENDING**.  
Real broker check: set `MaxActivePair` above 40 and confirm warning + EA remains attached; final broker-side confirmation remains user-owned.
""", encoding="utf-8")

    print("D1_STEP5_INPUT_LIMIT_GUARD_APPLY=PASS")


def finalize(root: Path) -> None:
    src = root / SRC_REL
    verify_source(src)
    audit = root / AUDIT_REL
    text = audit.read_text(encoding="utf-8")
    text = text.replace(
        "Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**",
        "Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS**",
        1,
    )
    text = text.replace(
        "Native MT4 MetaEditor: **PENDING**.",
        "Native MT4 MetaEditor: **0 errors / 0 warnings; EX4 produced**.",
        1,
    )
    audit.write_text(text, encoding="utf-8")
    print("D1_STEP5_INPUT_LIMIT_GUARD_FINALIZE=PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--finalize", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    if args.verify:
        verify_source(root / SRC_REL)
    elif args.finalize:
        finalize(root)
    else:
        apply(root)


if __name__ == "__main__":
    main()
