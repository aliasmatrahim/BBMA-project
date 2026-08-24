from pathlib import Path
import argparse


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 anchor, found {count}")
    return text.replace(old, new, 1)


def source_paths(root: Path):
    return (
        root / "blueprint/source/BBMA_EA.mq4",
        root / "blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md",
        root / "blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md",
        root / "blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md",
        root / "blueprint/D1_STEP3_M11_SNAPSHOT_ATOMICITY_IMPLEMENTATION_AUDIT_20260824.md",
    )


def static_check(src: Path) -> None:
    s = src.read_text(encoding="utf-8")

    required = [
        "//| Version 4.5.1 - D1-03 M11 Snapshot Atomicity",
        "double               Close1;",
        "double               MA50_1;",
        "double               MA50_2;",
        "owner.Close1 = state.d1_data.close;",
        "owner.MA50_1 = currentMA50;",
        "owner.MA50_2 = previousMA50;",
        "decision.D1OwnerClose = owner.Close1;",
        "decision.D1OwnerMA50Current = owner.MA50_1;",
        "decision.D1OwnerMA50Previous = owner.MA50_2;",
        "decision.D1OwnerClose != owner.Close1",
        "decision.D1OwnerMA50Current != owner.MA50_1",
        "decision.D1OwnerMA50Previous != owner.MA50_2",
        "[D1-03][OWNER]",
        "[D1-03][M15_D1_BLOCK]",
        "[D1-03][M16_D1_REJECT]",
        "BBMA EA V4.5.1 D1-03 initialized successfully",
        "=== BBMA EA V4.5.1 D1-03 ===",
    ]
    for item in required:
        if item not in s:
            raise SystemExit(f"missing D1-03 anchor: {item}")

    forbidden = [
        "state.d1_major_trend_owner.IsValid &&\n      state.d1_major_trend_owner.LastProcessedD1CandleTime == state.d1_data.candle_time",
        "decision.D1OwnerClose = pairState.d1_data.close;",
        "decision.D1OwnerMA50Current = pairState.current_daily_ema50;",
        "decision.D1OwnerMA50Previous = pairState.prev_daily_ema50;",
        "decision.D1OwnerClose != state.d1_data.close",
        "decision.D1OwnerMA50Current != state.current_daily_ema50",
        "decision.D1OwnerMA50Previous != state.prev_daily_ema50",
        "[D1-01][OWNER]",
        "[D1-02][M15_D1_BLOCK]",
        "[D1-02][M16_D1_REJECT]",
        "=== BBMA EA V4.5.1 D1-01 ===",
        "BBMA EA V4.5.1 D1-02 initialized successfully",
    ]
    for item in forbidden:
        if item in s:
            raise SystemExit(f"stale/split D1 identity remains: {item}")

    # Source formula remains the canonical closed-D1 price-side + MA50-slope rule.
    if s.count("owner.Close1 > owner.MA50_1 && owner.MA50_1 > owner.MA50_2") != 1:
        raise SystemExit("canonical D1 BUY predicate missing or duplicated")
    if s.count("owner.Close1 < owner.MA50_1 && owner.MA50_1 < owner.MA50_2") != 1:
        raise SystemExit("canonical D1 SELL predicate missing or duplicated")

    # M15 strategic filtering must remain before the atomic opposite-direction check.
    d1_filter = s.index("if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;")
    atomic_conflict = s.index("if(buyCount > 0 && sellCount > 0)")
    if d1_filter > atomic_conflict:
        raise SystemExit("D1 filter moved after atomic surviving-direction check")

    # M16 D1 snapshot revalidation must remain before structural owner revalidation.
    d1_verify = s.index("if(!ValidateDecisionD1OwnerSnapshot(pairIndex, decision))")
    structural_verify = s.index("if(!ValidateDecisionOwnerSnapshot(pairIndex, decision, ownerExpired))")
    if d1_verify > structural_verify:
        raise SystemExit("M16 D1 verification moved after structural revalidation")

    # D1 owner must be the sole numeric identity source downstream.
    freeze_start = s.index("bool FreezeD1OwnerSnapshot(")
    freeze_end = s.index("bool IsEntryModeCandidateAllowed(", freeze_start)
    freeze = s[freeze_start:freeze_end]
    for split_source in ["pairState.d1_data.close", "pairState.current_daily_ema50", "pairState.prev_daily_ema50"]:
        if split_source in freeze:
            raise SystemExit(f"M15 freeze still reads split source: {split_source}")

    verify_start = s.index("bool ValidateDecisionD1OwnerSnapshot(")
    verify_end = s.index("bool ValidateDecisionOwnerSnapshot(", verify_start)
    verify = s[verify_start:verify_end]
    for split_source in ["state.d1_data.close", "state.current_daily_ema50", "state.prev_daily_ema50"]:
        if split_source in verify:
            raise SystemExit(f"M16 verification still reads split source: {split_source}")

    # No strategy scope creep.
    m11_start = s.index("//| MODULE 11: TREND FUNCTIONS")
    m17_start = s.index("//| MODULE 17: SL/TP VALIDATION")
    window = s[m11_start:m17_start]
    for forbidden_filter in ["NewsFilter", "SessionFilter", "ADX", "Stochastic"]:
        if forbidden_filter in window:
            raise SystemExit(f"forbidden filter introduced: {forbidden_filter}")

    for module in range(1, 28):
        marker = f"MODULE {module:02d}:"
        if marker not in s:
            raise SystemExit(f"missing module marker {marker}")

    header_line = next((line for line in s.splitlines() if "Version 4.5.1 - D1-03" in line), "")
    if not header_line.startswith("//| Version 4.5.1 - D1-03"):
        raise SystemExit("D1-03 build header is not left-aligned immediately after //| ")

    if s.count("{") != s.count("}"):
        raise SystemExit("brace imbalance")
    if s.count("(") != s.count(")"):
        raise SystemExit("parenthesis imbalance")

    print("D1_STEP3_STATIC=PASS")


def apply(root: Path) -> None:
    src, m11, m15, m16, audit = source_paths(root)
    s = src.read_text(encoding="utf-8")

    if "Version 4.5.1 - D1-03 M11 Snapshot Atomicity" in s:
        static_check(src)
        print("D1-03 already applied")
        return

    s = replace_once(
        s,
        "//| Version 4.5.1 - D1-02 M15-M16 Strategic Gate                    |",
        "//| Version 4.5.1 - D1-03 M11 Snapshot Atomicity                    |",
        "build header",
    )

    s = replace_once(
        s,
        """struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   datetime             LastProcessedD1CandleTime;
   bool                 IsValid;
   string               Reason;
};""",
        """struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   datetime             LastProcessedD1CandleTime;
   double               Close1;
   double               MA50_1;
   double               MA50_2;
   bool                 IsValid;
   string               Reason;
};""",
        "D1 owner struct",
    )

    s = replace_once(
        s,
        """   state.d1_major_trend_owner.State = D1_OWNER_UNRESOLVED;
   state.d1_major_trend_owner.Direction = DIR_NONE;
   state.d1_major_trend_owner.SourceCandleTime = 0;
   state.d1_major_trend_owner.LastProcessedD1CandleTime = 0;
   state.d1_major_trend_owner.IsValid = false;
   state.d1_major_trend_owner.Reason = \"D1 owner not evaluated\";""",
        """   state.d1_major_trend_owner.State = D1_OWNER_UNRESOLVED;
   state.d1_major_trend_owner.Direction = DIR_NONE;
   state.d1_major_trend_owner.SourceCandleTime = 0;
   state.d1_major_trend_owner.LastProcessedD1CandleTime = 0;
   state.d1_major_trend_owner.Close1 = 0.0;
   state.d1_major_trend_owner.MA50_1 = 0.0;
   state.d1_major_trend_owner.MA50_2 = 0.0;
   state.d1_major_trend_owner.IsValid = false;
   state.d1_major_trend_owner.Reason = \"D1 owner not evaluated\";""",
        "D1 owner init",
    )

    old_m11 = """void SetD1OwnerUnresolved(PairState &state, string reason)
{
   state.d1_major_trend_owner.State = D1_OWNER_UNRESOLVED;
   state.d1_major_trend_owner.Direction = DIR_NONE;
   state.d1_major_trend_owner.IsValid = false;
   state.d1_major_trend_owner.SourceCandleTime = state.d1_data.candle_time;
   state.d1_major_trend_owner.LastProcessedD1CandleTime = state.d1_data.candle_time;
   state.d1_major_trend_owner.Reason = reason;
}

void TraceD1MajorTrendOwner(string pair, PairState &state)
{
   if(DebugLevel < DBG_SIGNAL) return;

   Print(\"[D1-01][OWNER] Pair=\", pair,
         \" Candle=\", TimeToString(state.d1_major_trend_owner.SourceCandleTime),
         \" State=\", EnumToString(state.d1_major_trend_owner.State),
         \" Dir=\", EnumToString(state.d1_major_trend_owner.Direction),
         \" Close=\", DoubleToString(state.d1_data.close, state.d1_data.digits),
         \" MA50=\", DoubleToString(state.current_daily_ema50, state.d1_data.digits),
         \" PrevMA50=\", DoubleToString(state.prev_daily_ema50, state.d1_data.digits));
}

void UpdateD1MajorTrendOwner(string pair, PairState &state)
{
   // D1-01 is producer-only. M15/M16 consumption is a later dependency step.
   if(!state.d1_data.is_valid ||
      !state.d1_data.is_closed ||
      state.d1_data.timeframe != PERIOD_D1 ||
      state.d1_data.candle_time <= 0 ||
      state.d1_data.barIndex < 1)
   {
      SetD1OwnerUnresolved(state, \"Invalid/incomplete closed D1 snapshot\");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   if(state.d1_major_trend_owner.IsValid &&
      state.d1_major_trend_owner.LastProcessedD1CandleTime == state.d1_data.candle_time)
      return;

   double currentMA50 = state.d1_data.ma[4];
   double previousMA50 = EMA(pair, PERIOD_D1, EMA50_PERIOD,
                             state.d1_data.barIndex + 1);

   state.current_daily_ema50 = currentMA50;
   state.prev_daily_ema50 = previousMA50;
   state.d1_major_trend_owner.SourceCandleTime = state.d1_data.candle_time;
   state.d1_major_trend_owner.LastProcessedD1CandleTime = state.d1_data.candle_time;

   if(state.d1_data.close <= 0.0 || currentMA50 <= 0.0 || previousMA50 <= 0.0)
   {
      SetD1OwnerUnresolved(state, \"Required closed D1 MA50 history unavailable\");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   state.d1_major_trend_owner.IsValid = true;

   if(state.d1_data.close > currentMA50 && currentMA50 > previousMA50)
   {
      state.d1_major_trend_owner.State = D1_OWNER_BUY_CONFIRMED;
      state.d1_major_trend_owner.Direction = DIR_BUY;
      state.d1_major_trend_owner.Reason = \"Closed D1 above MA50 with rising MA50\";
   }
   else if(state.d1_data.close < currentMA50 && currentMA50 < previousMA50)
   {
      state.d1_major_trend_owner.State = D1_OWNER_SELL_CONFIRMED;
      state.d1_major_trend_owner.Direction = DIR_SELL;
      state.d1_major_trend_owner.Reason = \"Closed D1 below MA50 with falling MA50\";
   }
   else
   {
      state.d1_major_trend_owner.State = D1_TRANSITION;
      state.d1_major_trend_owner.Direction = DIR_NONE;
      state.d1_major_trend_owner.Reason =
         \"Closed D1 price-side and MA50 slope do not confirm one direction\";
   }

   TraceD1MajorTrendOwner(pair, state);
}"""

    new_m11 = """void SetD1OwnerUnresolved(PairState &state, string reason)
{
   D1MajorTrendOwner &owner = state.d1_major_trend_owner;
   owner.State = D1_OWNER_UNRESOLVED;
   owner.Direction = DIR_NONE;
   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;
   owner.Close1 = (state.d1_data.close > 0.0) ? state.d1_data.close : 0.0;
   owner.MA50_1 = (state.d1_data.ma[4] > 0.0) ? state.d1_data.ma[4] : 0.0;
   owner.MA50_2 = 0.0;
   owner.IsValid = false;
   owner.Reason = reason;
}

void TraceD1MajorTrendOwner(string pair, PairState &state)
{
   if(DebugLevel < DBG_SIGNAL) return;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   Print(\"[D1-03][OWNER] Pair=\", pair,
         \" Candle=\", TimeToString(owner.SourceCandleTime),
         \" State=\", EnumToString(owner.State),
         \" Dir=\", EnumToString(owner.Direction),
         \" Close=\", DoubleToString(owner.Close1, state.d1_data.digits),
         \" MA50=\", DoubleToString(owner.MA50_1, state.d1_data.digits),
         \" PrevMA50=\", DoubleToString(owner.MA50_2, state.d1_data.digits));
}

void UpdateD1MajorTrendOwner(string pair, PairState &state)
{
   // D1-03: M11 produces one atomic closed-D1 owner snapshot consumed by M15/M16.
   // Re-evaluate on every M15 processing cycle so refreshed broker history cannot
   // create a hybrid identity from cached owner state plus newer raw D1 values.
   if(!state.d1_data.is_valid ||
      !state.d1_data.is_closed ||
      state.d1_data.timeframe != PERIOD_D1 ||
      state.d1_data.candle_time <= 0 ||
      state.d1_data.barIndex < 1)
   {
      SetD1OwnerUnresolved(state, \"Invalid/incomplete closed D1 snapshot\");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   double currentMA50 = state.d1_data.ma[4];
   double previousMA50 = EMA(pair, PERIOD_D1, EMA50_PERIOD,
                             state.d1_data.barIndex + 1);

   D1MajorTrendOwner &owner = state.d1_major_trend_owner;
   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;
   owner.Close1 = state.d1_data.close;
   owner.MA50_1 = currentMA50;
   owner.MA50_2 = previousMA50;

   // Compatibility mirrors only. Downstream D1 identity authority is owner.*.
   state.current_daily_ema50 = owner.MA50_1;
   state.prev_daily_ema50 = owner.MA50_2;

   if(owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
   {
      SetD1OwnerUnresolved(state, \"Required closed D1 MA50 history unavailable\");
      TraceD1MajorTrendOwner(pair, state);
      return;
   }

   owner.IsValid = true;

   if(owner.Close1 > owner.MA50_1 && owner.MA50_1 > owner.MA50_2)
   {
      owner.State = D1_OWNER_BUY_CONFIRMED;
      owner.Direction = DIR_BUY;
      owner.Reason = \"Closed D1 above MA50 with rising MA50\";
   }
   else if(owner.Close1 < owner.MA50_1 && owner.MA50_1 < owner.MA50_2)
   {
      owner.State = D1_OWNER_SELL_CONFIRMED;
      owner.Direction = DIR_SELL;
      owner.Reason = \"Closed D1 below MA50 with falling MA50\";
   }
   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         \"Closed D1 price-side and MA50 slope do not confirm one direction\";
   }

   TraceD1MajorTrendOwner(pair, state);
}"""
    s = replace_once(s, old_m11, new_m11, "M11 atomic owner producer")

    old_ready = """bool IsD1MajorTrendOwnerExecutionReady(PairState &pairState)
{
   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;

   if(!pairState.d1_data.is_valid || !pairState.d1_data.is_closed ||
      pairState.d1_data.timeframe != PERIOD_D1 ||
      pairState.d1_data.candle_time <= 0 || pairState.d1_data.close <= 0.0)
      return false;

   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.SourceCandleTime != pairState.d1_data.candle_time)
      return false;

   if(pairState.current_daily_ema50 <= 0.0 || pairState.prev_daily_ema50 <= 0.0)
      return false;

   if(owner.State == D1_OWNER_BUY_CONFIRMED)
      return (owner.Direction == DIR_BUY);

   if(owner.State == D1_OWNER_SELL_CONFIRMED)
      return (owner.Direction == DIR_SELL);

   return false;
}"""
    new_ready = """bool IsD1MajorTrendOwnerExecutionReady(PairState &pairState)
{
   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;

   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
      return false;

   if(owner.State == D1_OWNER_BUY_CONFIRMED)
      return (owner.Direction == DIR_BUY);

   if(owner.State == D1_OWNER_SELL_CONFIRMED)
      return (owner.Direction == DIR_SELL);

   return false;
}"""
    s = replace_once(s, old_ready, new_ready, "M15 D1 readiness")

    old_freeze = """bool FreezeD1OwnerSnapshot(PairState &pairState, BBMA_Decision &decision)
{
   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;

   decision.D1OwnerState = pairState.d1_major_trend_owner.State;
   decision.D1OwnerDirection = pairState.d1_major_trend_owner.Direction;
   decision.D1OwnerCandleTime = pairState.d1_major_trend_owner.SourceCandleTime;
   decision.D1OwnerClose = pairState.d1_data.close;
   decision.D1OwnerMA50Current = pairState.current_daily_ema50;
   decision.D1OwnerMA50Previous = pairState.prev_daily_ema50;
   decision.D1OwnerSnapshotValid = true;
   return true;
}"""
    new_freeze = """bool FreezeD1OwnerSnapshot(PairState &pairState, BBMA_Decision &decision)
{
   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;

   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;
   decision.D1OwnerState = owner.State;
   decision.D1OwnerDirection = owner.Direction;
   decision.D1OwnerCandleTime = owner.SourceCandleTime;
   decision.D1OwnerClose = owner.Close1;
   decision.D1OwnerMA50Current = owner.MA50_1;
   decision.D1OwnerMA50Previous = owner.MA50_2;
   decision.D1OwnerSnapshotValid = true;
   return true;
}"""
    s = replace_once(s, old_freeze, new_freeze, "M15 atomic freeze")

    old_verify = """bool ValidateDecisionD1OwnerSnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(!decision.D1OwnerSnapshotValid) return false;

   PairState state = g_pair_states[pairIndex];
   if(!IsD1MajorTrendOwnerExecutionReady(state)) return false;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   if(decision.D1OwnerState != owner.State) return false;
   if(decision.D1OwnerDirection != owner.Direction) return false;
   if(decision.Direction != owner.Direction) return false;
   if(decision.D1OwnerCandleTime != owner.SourceCandleTime) return false;
   if(decision.D1OwnerClose != state.d1_data.close) return false;
   if(decision.D1OwnerMA50Current != state.current_daily_ema50) return false;
   if(decision.D1OwnerMA50Previous != state.prev_daily_ema50) return false;

   return true;
}"""
    new_verify = """bool ValidateDecisionD1OwnerSnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(!decision.D1OwnerSnapshotValid) return false;

   PairState state = g_pair_states[pairIndex];
   if(!IsD1MajorTrendOwnerExecutionReady(state)) return false;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   if(decision.D1OwnerState != owner.State) return false;
   if(decision.D1OwnerDirection != owner.Direction) return false;
   if(decision.Direction != owner.Direction) return false;
   if(decision.D1OwnerCandleTime != owner.SourceCandleTime) return false;
   if(decision.D1OwnerClose != owner.Close1) return false;
   if(decision.D1OwnerMA50Current != owner.MA50_1) return false;
   if(decision.D1OwnerMA50Previous != owner.MA50_2) return false;

   return true;
}"""
    s = replace_once(s, old_verify, new_verify, "M16 atomic verification")

    # Observability/build identity belongs to the source revision actually running.
    s = s.replace("[D1-02][M15_D1_BLOCK]", "[D1-03][M15_D1_BLOCK]")
    s = s.replace("[D1-02][M16_D1_REJECT]", "[D1-03][M16_D1_REJECT]")
    s = replace_once(
        s,
        'g_dashboard_snapshot += "=== BBMA EA V4.5.1 D1-01 ===\\n";',
        'g_dashboard_snapshot += "=== BBMA EA V4.5.1 D1-03 ===\\n";',
        "dashboard build identity",
    )
    s = replace_once(
        s,
        'Log(DBG_FULL, "BBMA EA V4.5.1 D1-02 initialized successfully");',
        'Log(DBG_FULL, "BBMA EA V4.5.1 D1-03 initialized successfully");',
        "OnInit build identity",
    )

    src.write_text(s, encoding="utf-8")
    static_check(src)

    # Contract reconciliation is implementation-status/ownership only; no BBMA rule changes.
    m11_text = m11.read_text(encoding="utf-8")
    m11_text = m11_text.replace(
        "Status: **CANONICAL SPECIFICATION — IMPLEMENTATION PENDING / NO EA SOURCE CHANGE**",
        "Status: **CANONICAL SPECIFICATION — IMPLEMENTED ON ISOLATED `d1-owner-dev` / CANONICAL INTEGRATION PENDING**",
        1,
    )
    marker = "## D1-03 implementation record — atomic M11 snapshot"
    if marker not in m11_text:
        m11_text = m11_text.rstrip() + """

## D1-03 implementation record — atomic M11 snapshot
Build `Version 4.5.1 - D1-03 M11 Snapshot Atomicity` on isolated `d1-owner-dev` closes the M11 snapshot-interface ownership gap without changing the accepted D1 formula.

- M11 now owns `Close1`, `MA50_1`, and `MA50_2` inside `D1MajorTrendOwner` together with state/direction/candle/validity/reason.
- M11 re-evaluates the latest fully closed D1 snapshot on every M15 processing cycle; it does not freeze a same-candle classification across a refreshed broker-history snapshot.
- `current_daily_ema50` / `prev_daily_ema50` remain compatibility mirrors only and are not downstream D1 identity authority.
- M15 freezes only the M11-owned atomic snapshot; M16 verifies only against the current M11-owned atomic snapshot.
- BUY/SELL/TRANSITION/UNRESOLVED semantics and exact REM/RRE/REE signatures are unchanged.
- `blueprint-dev` remains unchanged; canonical integration still requires explicit release of the P3 freeze.
""" + "\n"
    m11.write_text(m11_text, encoding="utf-8")

    m15_text = m15.read_text(encoding="utf-8")
    marker15 = "## D1-03 atomic snapshot ownership overlay"
    if marker15 not in m15_text:
        m15_text = m15_text.rstrip() + """

## D1-03 atomic snapshot ownership overlay
M15 continues the D1-02 gate order, but its frozen D1 identity now comes exclusively from the M11-owned `D1MajorTrendOwner` atomic snapshot (`state`, `direction`, closed-D1 candle, `Close1`, `MA50_1`, `MA50_2`). M15 no longer mixes raw `d1_data` fields with separate PairState MA mirrors when freezing a decision. Strategy semantics and candidate signatures are unchanged.
""" + "\n"
    m15.write_text(m15_text, encoding="utf-8")

    m16_text = m16.read_text(encoding="utf-8")
    marker16 = "## D1-03 atomic snapshot ownership overlay"
    if marker16 not in m16_text:
        m16_text = m16_text.rstrip() + """

## D1-03 atomic snapshot ownership overlay
M16 continues to revalidate D1 before structural component freshness, but the comparison now uses only the current M11-owned atomic D1 snapshot. It no longer compares frozen decision identity against split raw `d1_data` / PairState MA mirror fields. No D1 trend formula is duplicated and no live-position exit authority is added.
""" + "\n"
    m16.write_text(m16_text, encoding="utf-8")

    audit.write_text("""# D1 Step 3 — M11 Snapshot Atomicity Implementation Audit

Date: 2026-08-24  
Branch: `d1-owner-dev`  
Build: `Version 4.5.1 - D1-03 M11 Snapshot Atomicity`  
Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**

## Finding fixed
D1-02 correctly applied the strategic D1 gate, but the numeric identity frozen by M15 was split across `d1_data.close` and separate PairState MA mirrors while the M11 owner itself stored only state/direction/candle/validity. M11 also cached an already-valid classification for the same D1 candle. That could permit a refreshed broker-history snapshot to coexist with cached owner state and create a hybrid downstream identity.

This was an implementation/snapshot-ownership defect against the already-locked M11/M15/M16 contracts, not a change to BBMA strategy semantics.

## D1-03 correction
- `D1MajorTrendOwner` now owns `Close1`, `MA50_1`, `MA50_2` atomically with state/direction/candle/validity/reason.
- M11 re-evaluates the fully closed D1 snapshot on each M15 processing cycle.
- M15 freezes only M11-owned D1 identity values.
- M16 verifies only against the current M11-owned D1 identity values.
- PairState MA doubles remain compatibility mirrors only.
- M15 D1 filter ordering and M16 pre-structural revalidation ordering remain unchanged.
- D1 BUY/SELL predicates are unchanged.
- REM/RRE/REE signatures, risk, SL/TP, lifecycle and execution logic are unchanged.
- Runtime build identity is updated consistently to D1-03.
- `blueprint-dev` is untouched.

## Verification
Focused static integrity: **PASS**.  
Native MT4 MetaEditor: **PENDING**.  
Real broker verification: **OUT OF SCOPE FOR GITHUB CI / USER FINAL STEP**.
""", encoding="utf-8")

    print("D1_STEP3_APPLY=PASS")


def finalize(root: Path) -> None:
    src, _m11, _m15, _m16, audit = source_paths(root)
    static_check(src)
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
    print("D1_STEP3_FINALIZE=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if args.finalize:
        finalize(root)
    else:
        apply(root)


if __name__ == "__main__":
    main()
