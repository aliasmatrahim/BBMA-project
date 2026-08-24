from pathlib import Path
import subprocess

SRC = Path("blueprint/source/BBMA_EA.mq4")
EXPECTED_BLOB = "1a8252e7544ae5f54c5ed12de2e92212fab80141"


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def extract_function(text: str, name: str) -> str:
    needle = name + "("
    pos = text.find(needle)
    if pos < 0:
        raise RuntimeError(f"function not found: {name}")
    line_start = text.rfind("\n", 0, pos) + 1
    brace = text.find("{", pos)
    if brace < 0:
        raise RuntimeError(f"opening brace not found: {name}")
    depth = 0
    i = brace
    in_string = False
    escape = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[line_start:i + 1]
        i += 1
    raise RuntimeError(f"unterminated function: {name}")


if not SRC.exists():
    raise SystemExit("source missing")

actual_blob = git_blob(SRC)
if actual_blob != EXPECTED_BLOB:
    raise SystemExit(f"unexpected baseline source blob: {actual_blob}")

text = SRC.read_text(encoding="utf-8")
if "MODULE 12N: NESTED MTF JOURNEY ENGINE" in text:
    raise SystemExit("NMJE observer already present; refusing duplicate patch")

critical_names = [
    "CollectSignalSnapshots",
    "BuildPossibleCombinations",
    "ValidateSequence",
    "PriorityEngine_Atomic",
    "InvalidationEngine_Atomic",
    "ResolveApprovedInitialSLTP",
]
critical_before = {name: extract_function(text, name) for name in critical_names}
append_count_before = text.count("AppendValidatedCandidate(")

# ------------------------------------------------------------------
# N1-03A: enum overlay. Observation metadata only.
# ------------------------------------------------------------------
enum_anchor = """enum ENUM_D1_OWNER_STATE
{
   D1_OWNER_UNRESOLVED,
   D1_OWNER_BUY_CONFIRMED,
   D1_OWNER_SELL_CONFIRMED,
   D1_TRANSITION
};
"""
if text.count(enum_anchor) != 1:
    raise SystemExit("D1 owner enum anchor not unique")

enum_insert = enum_anchor + """
// N1-03: observation-only nested MTF relationship states.
enum ENUM_NESTED_RELATION
{
   NESTED_NOT_APPLICABLE,
   NESTED_BUILDING,
   NESTED_SUPPORTING,
   NESTED_ALIGNED,
   NESTED_CONFLICT,
   NESTED_UNRESOLVED
};

enum ENUM_NESTED_PARENT_KIND
{
   NESTED_PARENT_NONE,
   NESTED_PARENT_H4_RE,
   NESTED_PARENT_H4_OWNER,
   NESTED_PARENT_D1_RE,
   NESTED_PARENT_D1_OWNER
};
"""
text = text.replace(enum_anchor, enum_insert, 1)

# ------------------------------------------------------------------
# N1-03B: immutable observation payloads.
# ------------------------------------------------------------------
struct_anchor = """struct TimeframeSnapshot
{
"""
if text.count(struct_anchor) != 1:
    raise SystemExit("TimeframeSnapshot anchor not unique")

struct_insert = """// N1-03: read-only observation node. It never owns BBMA strategy state.
struct NestedTFNode
{
   int                  Timeframe;
   ENUM_SIGNAL_TYPE     StageType;
   ENUM_DIRECTION       Direction;
   int                  StateCode;
   datetime             CandleTime;
   bool                 Valid;
   bool                 Resolved;
   string               Label;
};

// N1-03: one pair-level nested journey observation per closed-M15 cycle.
struct NestedJourneyState
{
   string                  Pair;
   string                  JourneyID;
   ENUM_NESTED_PARENT_KIND ParentKind;
   int                     ParentTimeframe;
   ENUM_SIGNAL_TYPE        ParentSignal;
   ENUM_DIRECTION          ParentDirection;
   datetime                ParentCandleTime;
   ENUM_DIRECTION          StrategicDirection;
   ENUM_NESTED_RELATION    Relation;
   bool                    Resolved;
   bool                    Valid;
   datetime                UpdateCandleTime;
   string                  Reason;
   NestedTFNode            D1Node;
   NestedTFNode            H4Node;
   NestedTFNode            H1Node;
   NestedTFNode            M15Node;
};

""" + struct_anchor
text = text.replace(struct_anchor, struct_insert, 1)

# ------------------------------------------------------------------
# N1-03C: dedicated global observation storage, kept outside PairState.
# ------------------------------------------------------------------
global_anchor = """PairState            g_pair_states[MAX_PAIRS];
datetime             g_processed_candle_time[MAX_PAIRS];
"""
if text.count(global_anchor) != 1:
    raise SystemExit("pair globals anchor not unique")
global_insert = """PairState            g_pair_states[MAX_PAIRS];
NestedJourneyState   g_nested_journeys[MAX_PAIRS]; // N1 observation only; never entry authority
datetime             g_processed_candle_time[MAX_PAIRS];
"""
text = text.replace(global_anchor, global_insert, 1)

# ------------------------------------------------------------------
# N1-03D: M12N read-only engine. Insert logically before M13.
# ------------------------------------------------------------------
module13_pos = text.find("//| MODULE 13:")
if module13_pos < 0:
    raise SystemExit("MODULE 13 marker not found")
module13_start = text.rfind("//+------------------------------------------------------------------+", 0, module13_pos)
if module13_start < 0:
    raise SystemExit("MODULE 13 heading start not found")

m12n_code = r'''//+------------------------------------------------------------------+
//| MODULE 12N: NESTED MTF JOURNEY ENGINE (N1 OBSERVATION ONLY)     |
//| LEVEL: INTERMEDIATE                                              |
//+------------------------------------------------------------------+

string NMJE_DirText(ENUM_DIRECTION direction)
{
   if(direction == DIR_BUY) return "B";
   if(direction == DIR_SELL) return "S";
   return "-";
}

string NMJE_RelationText(ENUM_NESTED_RELATION relation)
{
   if(relation == NESTED_BUILDING) return "BUILDING";
   if(relation == NESTED_SUPPORTING) return "SUPPORTING";
   if(relation == NESTED_ALIGNED) return "ALIGNED";
   if(relation == NESTED_CONFLICT) return "CONFLICT";
   if(relation == NESTED_UNRESOLVED) return "UNRESOLVED";
   return "N/A";
}

string NMJE_ParentText(ENUM_NESTED_PARENT_KIND kind)
{
   if(kind == NESTED_PARENT_H4_RE) return "H4_RE";
   if(kind == NESTED_PARENT_H4_OWNER) return "H4_OWNER";
   if(kind == NESTED_PARENT_D1_RE) return "D1_RE";
   if(kind == NESTED_PARENT_D1_OWNER) return "D1_OWNER";
   return "NONE";
}

string NMJE_REStateText(ENUM_RE_STATE state)
{
   if(state == RE_STATE_CANDIDATE) return "C";
   if(state == RE_STATE_CONFIRMED) return "F";
   if(state == RE_STATE_EXPIRED) return "X";
   return "N";
}

string NMJE_ExtremeStateText(ENUM_EXTREME_MATURITY state)
{
   if(state == EXT_MAT_RAW) return "R";
   if(state == EXT_MAT_REVERSAL_CONFIRMED) return "REV";
   if(state == EXT_MAT_RETEST_PHASE) return "RT";
   if(state == EXT_MAT_RETEST_READY) return "RDY";
   if(state == EXT_MAT_VOID) return "V";
   if(state == EXT_MAT_SUPERSEDED) return "S";
   return "N";
}

string NMJE_MLVStateText(ENUM_MLV_STATE state)
{
   if(state == MLV_PARENT_READY) return "P";
   if(state == MLV_TP_COMPLETE) return "TP";
   if(state == MLV_LOSS_DEVELOPING) return "L";
   if(state == MLV_FORMATION_ESTABLISHED) return "F";
   if(state == MLV_RETEST_COMPLETE) return "RT";
   if(state == MLV_DIRECTION_TAKEN) return "T";
   if(state == MLV_VOID) return "V";
   if(state == MLV_SUPERSEDED) return "S";
   return "N";
}

void NMJE_ResetNode(NestedTFNode &node, int timeframe)
{
   ZeroMemory(node);
   node.Timeframe = timeframe;
   node.StageType = SIGNAL_NONE;
   node.Direction = DIR_NONE;
   node.StateCode = 0;
   node.CandleTime = 0;
   node.Valid = false;
   node.Resolved = false;
   node.Label = "-";
}

bool NMJE_IsConfirmedRE(ReEntryData &state)
{
   return (state.State == RE_STATE_CONFIRMED && state.IsValid &&
           (state.Direction == DIR_BUY || state.Direction == DIR_SELL) &&
           state.ConfirmationCandle > 0);
}

bool NMJE_IsCandidateRE(ReEntryData &state)
{
   return (state.State == RE_STATE_CANDIDATE && state.IsValid &&
           (state.Direction == DIR_BUY || state.Direction == DIR_SELL));
}

bool NMJE_IsExtremeActive(ExtremeLifecycleData &state)
{
   if(!state.IsValid) return false;
   return (state.Maturity == EXT_MAT_RAW ||
           state.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           state.Maturity == EXT_MAT_RETEST_PHASE ||
           state.Maturity == EXT_MAT_RETEST_READY);
}

bool NMJE_IsExtremeSupporting(ExtremeLifecycleData &state)
{
   if(!state.IsValid) return false;
   return (state.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           state.Maturity == EXT_MAT_RETEST_PHASE ||
           state.Maturity == EXT_MAT_RETEST_READY);
}

bool NMJE_IsMLVActive(MLVData &state)
{
   if(!state.IsValid) return false;
   return (state.State != MLV_NONE &&
           state.State != MLV_VOID &&
           state.State != MLV_SUPERSEDED);
}

bool NMJE_IsMLVSupporting(MLVData &state)
{
   if(!state.IsValid) return false;
   return (state.State == MLV_FORMATION_ESTABLISHED ||
           state.State == MLV_RETEST_COMPLETE ||
           state.State == MLV_DIRECTION_TAKEN);
}

bool NMJE_SelectConfirmedRE(ReEntryData &buyState, ReEntryData &sellState,
                            ReEntryData &selected, bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = NMJE_IsConfirmedRE(buyState);
   bool sellValid = NMJE_IsConfirmedRE(sellState);
   ambiguous = (buyValid && sellValid);
   if(ambiguous || (!buyValid && !sellValid)) return false;
   if(buyValid) selected = buyState;
   else selected = sellState;
   return true;
}

bool NMJE_SelectCandidateRE(ReEntryData &buyState, ReEntryData &sellState,
                            ReEntryData &selected, bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = NMJE_IsCandidateRE(buyState);
   bool sellValid = NMJE_IsCandidateRE(sellState);
   ambiguous = (buyValid && sellValid);
   if(ambiguous || (!buyValid && !sellValid)) return false;
   if(buyValid) selected = buyState;
   else selected = sellState;
   return true;
}

void NMJE_SetRENode(NestedTFNode &node, ReEntryData &state, bool resolved)
{
   node.StageType = SIGNAL_RE_ENTRY;
   node.Direction = state.Direction;
   node.StateCode = (int)state.State;
   node.CandleTime = (state.ConfirmationCandle > 0)
      ? state.ConfirmationCandle : state.StartCandleTime;
   node.Valid = state.IsValid;
   node.Resolved = resolved;
   node.Label = "RE:" + NMJE_REStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}

void NMJE_SetExtremeNode(NestedTFNode &node, ExtremeLifecycleData &state)
{
   node.StageType = SIGNAL_EXTREME;
   node.Direction = state.Direction;
   node.StateCode = (int)state.Maturity;
   node.CandleTime = (state.ConfirmationCandleTime > 0)
      ? state.ConfirmationCandleTime : state.RawCandleTime;
   node.Valid = state.IsValid;
   node.Resolved = false; // Extreme is pre-direction context for N1 lineage.
   node.Label = "EXT:" + NMJE_ExtremeStateText(state.Maturity) + "/" + NMJE_DirText(state.Direction);
}

void NMJE_SetMLVNode(NestedTFNode &node, MLVData &state)
{
   node.StageType = SIGNAL_MLV;
   node.Direction = state.Direction;
   node.StateCode = (int)state.State;
   node.CandleTime = (state.ConfirmationCandleTime > 0)
      ? state.ConfirmationCandleTime : state.LastUpdateCandleTime;
   node.Valid = state.IsValid;
   node.Resolved = false; // MHV/MLV is setup/context, not final direction authority.
   node.Label = "MHV:" + NMJE_MLVStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}

void NMJE_BuildD1Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_D1);
   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_d1_buy_state, state.re_d1_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(node, selected, true);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:AMB";
      return;
   }

   if((state.d1_major_trend_owner.State == D1_OWNER_BUY_CONFIRMED ||
       state.d1_major_trend_owner.State == D1_OWNER_SELL_CONFIRMED) &&
      state.d1_major_trend_owner.IsValid)
   {
      node.Direction = state.d1_major_trend_owner.Direction;
      node.CandleTime = state.d1_major_trend_owner.SourceCandleTime;
      node.Valid = true;
      node.Resolved = true;
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }

   if(state.d1_major_trend_owner.State == D1_TRANSITION)
   {
      node.Valid = true;
      node.Resolved = true;
      node.Label = "TRANSITION";
      return;
   }

   node.Label = "UNRESOLVED";
}

void NMJE_BuildH4Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_H4);
   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(node, selected, true);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:AMB";
      return;
   }

   if(NMJE_SelectCandidateRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(node, selected, false);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:C:AMB";
      return;
   }

   if(state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
      state.h4_direction_owner.IsValid &&
      (state.h4_direction_owner.Direction == DIR_BUY ||
       state.h4_direction_owner.Direction == DIR_SELL))
   {
      node.StageType = state.h4_direction_owner.SourceSignal;
      node.Direction = state.h4_direction_owner.Direction;
      node.CandleTime = state.h4_direction_owner.SourceCandleTime;
      node.Valid = true;
      node.Resolved = true;
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }

   bool buyExtreme = NMJE_IsExtremeActive(state.extreme_h4_buy_lifecycle);
   bool sellExtreme = NMJE_IsExtremeActive(state.extreme_h4_sell_lifecycle);
   if(buyExtreme != sellExtreme)
   {
      if(buyExtreme) NMJE_SetExtremeNode(node, state.extreme_h4_buy_lifecycle);
      else NMJE_SetExtremeNode(node, state.extreme_h4_sell_lifecycle);
   }
   else if(buyExtreme && sellExtreme)
      node.Label = "EXT:AMB";
}

void NMJE_BuildH1Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_H1);
   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_h1_buy_state, state.re_h1_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(node, selected, true);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:AMB";
      return;
   }

   if(NMJE_SelectCandidateRE(state.re_h1_buy_state, state.re_h1_sell_state,
                             selected, ambiguous))
   {
      NMJE_SetRENode(node, selected, false);
      return;
   }
   if(ambiguous)
   {
      node.Label = "RE:C:AMB";
      return;
   }

   bool buyExtreme = NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle);
   bool sellExtreme = NMJE_IsExtremeActive(state.extreme_h1_sell_lifecycle);
   if(buyExtreme != sellExtreme)
   {
      if(buyExtreme) NMJE_SetExtremeNode(node, state.extreme_h1_buy_lifecycle);
      else NMJE_SetExtremeNode(node, state.extreme_h1_sell_lifecycle);
   }
   else if(buyExtreme && sellExtreme)
      node.Label = "EXT:AMB";
}

void NMJE_BuildM15Node(PairState &state, NestedTFNode &node)
{
   NMJE_ResetNode(node, PERIOD_M15);
   bool buyMLV = NMJE_IsMLVActive(state.mlv_buy_state);
   bool sellMLV = NMJE_IsMLVActive(state.mlv_sell_state);
   if(buyMLV != sellMLV)
   {
      if(buyMLV) NMJE_SetMLVNode(node, state.mlv_buy_state);
      else NMJE_SetMLVNode(node, state.mlv_sell_state);
   }
   else if(buyMLV && sellMLV)
      node.Label = "MHV:AMB";
}

bool NMJE_ResolveParent(PairState &state,
                        ENUM_NESTED_PARENT_KIND &kind,
                        int &timeframe,
                        ENUM_SIGNAL_TYPE &signalType,
                        ENUM_DIRECTION &direction,
                        datetime &anchor,
                        string &reason)
{
   kind = NESTED_PARENT_NONE;
   timeframe = 0;
   signalType = SIGNAL_NONE;
   direction = DIR_NONE;
   anchor = 0;
   reason = "NO_PARENT";

   ReEntryData selected;
   bool ambiguous = false;
   if(NMJE_SelectConfirmedRE(state.re_h4_buy_state, state.re_h4_sell_state,
                             selected, ambiguous))
   {
      kind = NESTED_PARENT_H4_RE;
      timeframe = PERIOD_H4;
      signalType = SIGNAL_RE_ENTRY;
      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      reason = "H4_RE_PARENT";
      return true;
   }
   if(ambiguous)
   {
      reason = "H4_RE_AMBIGUOUS";
      return false;
   }

   if(state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
      state.h4_direction_owner.IsValid &&
      (state.h4_direction_owner.Direction == DIR_BUY ||
       state.h4_direction_owner.Direction == DIR_SELL))
   {
      kind = NESTED_PARENT_H4_OWNER;
      timeframe = PERIOD_H4;
      signalType = state.h4_direction_owner.SourceSignal;
      direction = state.h4_direction_owner.Direction;
      anchor = state.h4_direction_owner.SourceCandleTime;
      reason = "H4_OWNER_PARENT";
      return true;
   }

   if(NMJE_SelectConfirmedRE(state.re_d1_buy_state, state.re_d1_sell_state,
                             selected, ambiguous))
   {
      kind = NESTED_PARENT_D1_RE;
      timeframe = PERIOD_D1;
      signalType = SIGNAL_RE_ENTRY;
      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      reason = "D1_RE_PARENT";
      return true;
   }
   if(ambiguous)
   {
      reason = "D1_RE_AMBIGUOUS";
      return false;
   }

   if((state.d1_major_trend_owner.State == D1_OWNER_BUY_CONFIRMED ||
       state.d1_major_trend_owner.State == D1_OWNER_SELL_CONFIRMED) &&
      state.d1_major_trend_owner.IsValid)
   {
      kind = NESTED_PARENT_D1_OWNER;
      timeframe = PERIOD_D1;
      signalType = SIGNAL_NONE;
      direction = state.d1_major_trend_owner.Direction;
      anchor = state.d1_major_trend_owner.SourceCandleTime;
      reason = "D1_OWNER_PARENT";
      return true;
   }

   return false;
}

bool NMJE_HasChildActivity(PairState &state)
{
   if(NMJE_IsCandidateRE(state.re_h1_buy_state) || NMJE_IsCandidateRE(state.re_h1_sell_state)) return true;
   if(NMJE_IsConfirmedRE(state.re_h1_buy_state) || NMJE_IsConfirmedRE(state.re_h1_sell_state)) return true;
   if(NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle) || NMJE_IsExtremeActive(state.extreme_h1_sell_lifecycle)) return true;
   if(NMJE_IsMLVActive(state.mlv_buy_state) || NMJE_IsMLVActive(state.mlv_sell_state)) return true;
   return false;
}

string NMJE_BuildJourneyID(string pair, ENUM_NESTED_PARENT_KIND kind,
                           int timeframe, ENUM_SIGNAL_TYPE signalType,
                           ENUM_DIRECTION direction, datetime anchor)
{
   return pair + "|" + NMJE_ParentText(kind) + "|" +
          IntegerToString(timeframe) + "|" + EnumToString(signalType) + "|" +
          NMJE_DirText(direction) + "|" + IntegerToString((int)anchor);
}

void UpdateNestedJourneyObservation(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;

   NestedJourneyState journey;
   ZeroMemory(journey);
   journey.Pair = g_pair_states[pairIndex].actual_symbol;
   journey.Relation = NESTED_NOT_APPLICABLE;
   journey.ParentKind = NESTED_PARENT_NONE;
   journey.ParentSignal = SIGNAL_NONE;
   journey.ParentDirection = DIR_NONE;
   journey.StrategicDirection = DIR_NONE;
   journey.UpdateCandleTime = g_pair_states[pairIndex].m15_data.candle_time;
   journey.Reason = "NO_ACTIVE_JOURNEY";

   NMJE_BuildD1Node(g_pair_states[pairIndex], journey.D1Node);
   NMJE_BuildH4Node(g_pair_states[pairIndex], journey.H4Node);
   NMJE_BuildH1Node(g_pair_states[pairIndex], journey.H1Node);
   NMJE_BuildM15Node(g_pair_states[pairIndex], journey.M15Node);

   ENUM_D1_OWNER_STATE d1State = g_pair_states[pairIndex].d1_major_trend_owner.State;
   if(d1State == D1_OWNER_BUY_CONFIRMED || d1State == D1_OWNER_SELL_CONFIRMED)
      journey.StrategicDirection = g_pair_states[pairIndex].d1_major_trend_owner.Direction;

   if(d1State == D1_OWNER_UNRESOLVED)
   {
      journey.Relation = NESTED_UNRESOLVED;
      journey.Reason = "D1_OWNER_UNRESOLVED";
      g_nested_journeys[pairIndex] = journey;
      Print("[N1-NMJE] ", journey.Pair, " REL=UNRESOLVED P=NONE J=- D1=", journey.D1Node.Label,
            " H4=", journey.H4Node.Label, " H1=", journey.H1Node.Label,
            " M15=", journey.M15Node.Label, " R=", journey.Reason);
      return;
   }

   ENUM_NESTED_PARENT_KIND parentKind;
   int parentTF = 0;
   ENUM_SIGNAL_TYPE parentSignal = SIGNAL_NONE;
   ENUM_DIRECTION parentDirection = DIR_NONE;
   datetime parentAnchor = 0;
   string parentReason = "";
   bool hasParent = NMJE_ResolveParent(g_pair_states[pairIndex], parentKind, parentTF,
                                       parentSignal, parentDirection, parentAnchor,
                                       parentReason);

   if(!hasParent)
   {
      if(g_pair_states[pairIndex].h4_direction_owner.State == H4_OWNER_RECOVERY_UNRESOLVED ||
         NMJE_HasChildActivity(g_pair_states[pairIndex]))
      {
         journey.Relation = NESTED_UNRESOLVED;
         journey.Reason = (parentReason != "NO_PARENT") ? parentReason : "PARENT_PROVENANCE_MISSING";
      }
      else
      {
         journey.Relation = NESTED_NOT_APPLICABLE;
         journey.Reason = "NO_PARENT_NO_CHILD";
         journey.Resolved = true;
      }
      g_nested_journeys[pairIndex] = journey;
      Print("[N1-NMJE] ", journey.Pair, " REL=", NMJE_RelationText(journey.Relation),
            " P=NONE J=- D1=", journey.D1Node.Label, " H4=", journey.H4Node.Label,
            " H1=", journey.H1Node.Label, " M15=", journey.M15Node.Label,
            " R=", journey.Reason);
      return;
   }

   journey.ParentKind = parentKind;
   journey.ParentTimeframe = parentTF;
   journey.ParentSignal = parentSignal;
   journey.ParentDirection = parentDirection;
   journey.ParentCandleTime = parentAnchor;
   journey.JourneyID = NMJE_BuildJourneyID(journey.Pair, parentKind, parentTF,
                                            parentSignal, parentDirection, parentAnchor);
   journey.Valid = true;
   journey.Resolved = true;

   if(d1State == D1_TRANSITION)
   {
      journey.Relation = NESTED_BUILDING;
      journey.Reason = "D1_TRANSITION";
   }
   else if((journey.StrategicDirection == DIR_BUY || journey.StrategicDirection == DIR_SELL) &&
           parentTF == PERIOD_H4 && parentDirection != journey.StrategicDirection)
   {
      // A local H4 journey may be counter to D1 while a retracement develops.
      // N1 does not call this an autonomous reversal and does not gate it.
      journey.Relation = NESTED_BUILDING;
      journey.Reason = "H4_LOCAL_OPPOSES_D1";
   }
   else
   {
      ReEntryData h1Confirmed;
      bool h1Ambiguous = false;
      if(NMJE_SelectConfirmedRE(g_pair_states[pairIndex].re_h1_buy_state,
                                g_pair_states[pairIndex].re_h1_sell_state,
                                h1Confirmed, h1Ambiguous))
      {
         if(h1Confirmed.Direction == parentDirection)
         {
            journey.Relation = NESTED_ALIGNED;
            journey.Reason = "H1_RE_ALIGNED_WITH_PARENT";
         }
         else
         {
            journey.Relation = NESTED_CONFLICT;
            journey.Reason = "CONFIRMED_H1_RE_OPPOSES_PARENT";
         }
      }
      else if(h1Ambiguous)
      {
         journey.Relation = NESTED_UNRESOLVED;
         journey.Resolved = false;
         journey.Reason = "H1_RE_AMBIGUOUS";
      }
      else
      {
         bool supporting =
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_buy_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_sell_lifecycle) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_buy_state) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_sell_state);

         if(supporting)
         {
            journey.Relation = NESTED_SUPPORTING;
            journey.Reason = "LTF_STRUCTURE_SUPPORTING_PARENT";
         }
         else if(NMJE_HasChildActivity(g_pair_states[pairIndex]))
         {
            journey.Relation = NESTED_BUILDING;
            journey.Reason = "LTF_STRUCTURE_BUILDING";
         }
         else if(parentKind == NESTED_PARENT_D1_OWNER &&
                 g_pair_states[pairIndex].h4_direction_owner.State == H4_OWNER_ACTIVE &&
                 g_pair_states[pairIndex].h4_direction_owner.IsValid)
         {
            if(g_pair_states[pairIndex].h4_direction_owner.Direction == parentDirection)
            {
               journey.Relation = NESTED_ALIGNED;
               journey.Reason = "H4_OWNER_ALIGNED_WITH_D1";
            }
            else
            {
               journey.Relation = NESTED_BUILDING;
               journey.Reason = "H4_LOCAL_OPPOSES_D1";
            }
         }
         else
         {
            journey.Relation = NESTED_BUILDING;
            journey.Reason = "PARENT_WAITING_FOR_CHILD";
         }
      }
   }

   g_nested_journeys[pairIndex] = journey;
   Print("[N1-NMJE] ", journey.Pair,
         " REL=", NMJE_RelationText(journey.Relation),
         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " J=", journey.JourneyID,
         " D1=", journey.D1Node.Label,
         " H4=", journey.H4Node.Label,
         " H1=", journey.H1Node.Label,
         " M15=", journey.M15Node.Label,
         " R=", journey.Reason);
}

'''
text = text[:module13_start] + m12n_code + text[module13_start:]

# ------------------------------------------------------------------
# N1-03E: one shadow observation call after both directional owner
# updates / M13-M14 assembly, but before M15 final authority.
# Existing ProcessPair interleaves owner updates and assembly, so N1 avoids
# a risky pipeline refactor. This call cannot alter allCandidates.
# ------------------------------------------------------------------
call_anchor = """   BBMA_Decision decision;
   OppositeConflictPackage conflict;
"""
if text.count(call_anchor) != 1:
    raise SystemExit("pre-M15 call anchor not unique")
call_insert = """   // N1-03 NMJE shadow observation: all BUY/SELL owner states are current.
   // Intentionally read-only and excluded from allCandidates / M15 authority.
   UpdateNestedJourneyObservation(pairIndex);

""" + call_anchor
text = text.replace(call_anchor, call_insert, 1)

# Build identity only; strategy semantics unchanged.
text = text.replace("Version 4.5.1 - D1-09 Default 20 Pair Universe",
                    "Version 4.5.1 - N1-03 NMJE Observer", 1)
text = text.replace("BBMA EA V4.5.1 D1-09 initialized successfully",
                    "BBMA EA V4.5.1 N1-03 initialized successfully", 1)

# ------------------------------------------------------------------
# Static invariants.
# ------------------------------------------------------------------
for name in critical_names:
    after = extract_function(text, name)
    if after != critical_before[name]:
        raise SystemExit(f"critical strategy function changed unexpectedly: {name}")

if text.count("AppendValidatedCandidate(") != append_count_before:
    raise SystemExit("candidate append call count changed")

if text.count("UpdateNestedJourneyObservation(pairIndex);") != 1:
    raise SystemExit("NMJE must be called exactly once in ProcessPair")

block_start = text.find("//| MODULE 12N: NESTED MTF JOURNEY ENGINE")
block_end = text.find("//| MODULE 13:", block_start)
if block_start < 0 or block_end < 0:
    raise SystemExit("NMJE module bounds missing")
nmje_block = text[block_start:block_end]
for forbidden in [
    "DetectExtreme(", "DetectMHV(", "DetectCSD(", "DetectECSD(", "DetectCSM(",
    "UpdateReEntryState(", "BuildPossibleCombinations(", "ValidateSequence(",
    "PriorityEngine_Atomic(", "InvalidationEngine_Atomic(", "OrderSend("
]:
    if forbidden in nmje_block:
        raise SystemExit(f"forbidden NMJE ownership call: {forbidden}")

for signature in [
    "REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV",
    "RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme",
    "REE = D1 Re-Entry + H4 Extreme + H1 Extreme",
]:
    # These exact prose strings live in contracts, not source; source invariants
    # are checked through unchanged BuildPossibleCombinations/ValidateSequence.
    pass

SRC.write_text(text, encoding="utf-8", newline="\n")
print("N1 NMJE observer patch applied")
print("baseline_blob=", actual_blob)
print("new_blob=", git_blob(SRC))
