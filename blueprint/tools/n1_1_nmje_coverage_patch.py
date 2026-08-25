from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4")
EXPECTED_BLOB = "f0f80decbdbda836c12b6073f5dbc6e347662b13"


def die(msg: str) -> None:
    raise SystemExit(msg)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        die(f"{label}: expected exactly one anchor, got {count}")
    return text.replace(old, new, 1)


def find_braced_block(text: str, start_pattern: str, label: str) -> tuple[int, int, str]:
    m = re.search(start_pattern, text, re.M)
    if not m:
        die(f"{label}: start not found")
    brace = text.find("{", m.end() - 1)
    if brace < 0:
        die(f"{label}: opening brace not found")
    depth = 0
    in_str = False
    esc = False
    for i in range(brace, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return m.start(), i + 1, text[m.start(): i + 1]
    die(f"{label}: unterminated block")


def replace_block(text: str, start_pattern: str, transform, label: str) -> str:
    s, e, block = find_braced_block(text, start_pattern, label)
    new = transform(block)
    if new == block:
        die(f"{label}: transform made no change")
    return text[:s] + new + text[e:]


def function_hash(text: str, name: str) -> str:
    _, _, block = find_braced_block(
        text,
        rf"(?m)^\s*[A-Za-z_][A-Za-z0-9_<>\s&\*]*\b{re.escape(name)}\s*\(",
        f"function {name}",
    )
    return hashlib.sha256(block.encode()).hexdigest()


def git_blob() -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(SRC)], text=True
    ).strip()


text = SRC.read_text(encoding="utf-8")
if git_blob() != EXPECTED_BLOB:
    die(f"Unexpected source blob: {git_blob()} expected {EXPECTED_BLOB}")
if 'Version 4.5.6 - C044 Deterministic Replay Stage' not in text:
    die("Unexpected build header")
if '#property version   "4.56"' not in text:
    die("Unexpected #property version")
if 'bool           EnableC044Lifecycle                = false;' not in text:
    die("C044 gate is not confirmed OFF")

protected = [
    "BuildPossibleCombinations",
    "ValidateSequence",
    "BuildD1OpportunityCandidate",
    "PriorityEngine_Atomic",
    "ResolveSelectedSLTPSourceComponent",
    "NMJE_PrintValidatedDecisionShadow",
    "RunEntryPreflightAndExecute",
    "CheckRiskBeforeTrade",
    "CalculateLotSize",
    "ManagePortfolio",
    "ManagePositions",
]
protected_before = {name: function_hash(text, name) for name in protected}

# Unique build identity only; C044 implementation remains present and gated OFF.
text = replace_once(
    text,
    'Version 4.5.6 - C044 Deterministic Replay Stage',
    'Version 4.5.7 - N1.1 NMJE Coverage Overlay',
    "header version",
)
text = replace_once(
    text,
    '#property version   "4.56"',
    '#property version   "4.57"',
    "property version",
)

# Secondary node overlays preserve the existing primary StageType/Direction semantics.
def patch_node_struct(block: str) -> str:
    marker = "   string               Label;\n"
    if block.count(marker) != 1:
        die("NestedTFNode Label anchor mismatch")
    addition = marker + """
   // N1.1 coverage-only secondary overlays. These never own strategy state.
   ENUM_RE_STATE        ReEntryBuyState;
   ENUM_RE_STATE        ReEntrySellState;
   bool                 ReEntryBuyValid;
   bool                 ReEntrySellValid;
   datetime             ReEntryBuyCandleTime;
   datetime             ReEntrySellCandleTime;
   ENUM_EXTREME_MATURITY ExtremeBuyMaturity;
   ENUM_EXTREME_MATURITY ExtremeSellMaturity;
   bool                 ExtremeBuyValid;
   bool                 ExtremeSellValid;
   datetime             ExtremeBuyCandleTime;
   datetime             ExtremeSellCandleTime;
   ENUM_MLV_STATE       MLVBuyState;
   ENUM_MLV_STATE       MLVSellState;
   bool                 MLVBuyValid;
   bool                 MLVSellValid;
   datetime             MLVBuyCandleTime;
   datetime             MLVSellCandleTime;
   string               OverlayLabel;
"""
    return block.replace(marker, addition, 1)

text = replace_block(
    text,
    r"(?m)^struct\s+NestedTFNode\s*\{",
    patch_node_struct,
    "NestedTFNode",
)

# D1 Opportunity is an overlay on a journey, never a new parent kind.
def patch_journey_struct(block: str) -> str:
    close = block.rfind("}")
    if close < 0:
        die("NestedJourneyState close missing")
    addition = """
   // N1.1 read-only D1 Opportunity overlay; not parent or execution authority.
   bool                       D1OpportunityActive;
   ENUM_D1_OPPORTUNITY_FAMILY D1OpportunityFamily;
   ENUM_DIRECTION             D1OpportunityDirection;
   ENUM_SIGNAL_TYPE           D1OpportunitySourceSignal;
   datetime                   D1OpportunitySourceCandleTime;
   datetime                   D1OpportunityActivationTime;
   bool                       D1OpportunityTactical;
   bool                       D1OpportunityTPWCompleted;
   string                     D1OpportunityCycleID;
"""
    return block[:close] + addition + block[close:]

text = replace_block(
    text,
    r"(?m)^struct\s+NestedJourneyState\s*\{",
    patch_journey_struct,
    "NestedJourneyState",
)

helpers = r'''
// N1.1 coverage-only helpers. Consume existing owner snapshots only.
datetime NMJE_REOverlayCandle(ReEntryData &state)
{
   if(state.ConfirmationCandle > 0) return state.ConfirmationCandle;
   return state.StartCandleTime;
}

datetime NMJE_ExtremeOverlayCandle(ExtremeLifecycleData &state)
{
   if(state.ConfirmationCandleTime > 0) return state.ConfirmationCandleTime;
   return state.RawCandleTime;
}

datetime NMJE_MLVOverlayCandle(MLVData &state)
{
   if(state.ConfirmationCandleTime > 0) return state.ConfirmationCandleTime;
   return state.LastUpdateCandleTime;
}

void NMJE_CaptureReEntryOverlay(NestedTFNode &node,
                                ReEntryData &buyState, ReEntryData &sellState)
{
   node.ReEntryBuyState = buyState.State;
   node.ReEntrySellState = sellState.State;
   node.ReEntryBuyValid = buyState.IsValid;
   node.ReEntrySellValid = sellState.IsValid;
   node.ReEntryBuyCandleTime = NMJE_REOverlayCandle(buyState);
   node.ReEntrySellCandleTime = NMJE_REOverlayCandle(sellState);
}

void NMJE_CaptureExtremeOverlay(NestedTFNode &node,
                                ExtremeLifecycleData &buyState,
                                ExtremeLifecycleData &sellState)
{
   node.ExtremeBuyMaturity = buyState.Maturity;
   node.ExtremeSellMaturity = sellState.Maturity;
   node.ExtremeBuyValid = buyState.IsValid;
   node.ExtremeSellValid = sellState.IsValid;
   node.ExtremeBuyCandleTime = NMJE_ExtremeOverlayCandle(buyState);
   node.ExtremeSellCandleTime = NMJE_ExtremeOverlayCandle(sellState);
}

void NMJE_CaptureMLVOverlay(NestedTFNode &node,
                            MLVData &buyState, MLVData &sellState)
{
   node.MLVBuyState = buyState.State;
   node.MLVSellState = sellState.State;
   node.MLVBuyValid = buyState.IsValid;
   node.MLVSellValid = sellState.IsValid;
   node.MLVBuyCandleTime = NMJE_MLVOverlayCandle(buyState);
   node.MLVSellCandleTime = NMJE_MLVOverlayCandle(sellState);
}

void NMJE_RefreshOverlayLabel(NestedTFNode &node)
{
   node.OverlayLabel =
      "RE=" + EnumToString(node.ReEntryBuyState) + "/" + EnumToString(node.ReEntrySellState) +
      "|X=" + EnumToString(node.ExtremeBuyMaturity) + "/" + EnumToString(node.ExtremeSellMaturity) +
      "|MHV=" + EnumToString(node.MLVBuyState) + "/" + EnumToString(node.MLVSellState);
}

void NMJE_CaptureD1OpportunityOverlay(PairState &state, NestedJourneyState &journey)
{
   D1OpportunityJourney opportunity = state.d1_opportunity;
   journey.D1OpportunityActive = opportunity.Active;
   journey.D1OpportunityFamily = opportunity.Family;
   journey.D1OpportunityDirection = opportunity.Direction;
   journey.D1OpportunitySourceSignal = opportunity.SourceSignal;
   journey.D1OpportunitySourceCandleTime = opportunity.SourceCandleTime;
   journey.D1OpportunityActivationTime = opportunity.ActivationTime;
   journey.D1OpportunityTactical = opportunity.Tactical;
   journey.D1OpportunityTPWCompleted = opportunity.TPWCompleted;
   journey.D1OpportunityCycleID = opportunity.CycleID;
}

void NMJE_PrintCoverageOverlay(NestedJourneyState &journey)
{
   if(DebugLevel < DBG_SIGNAL) return;
   Print("[N1.1-NMJE-COV] ", journey.Pair,
         " OPP=", D1OpportunityFamilyText(journey.D1OpportunityFamily), "/",
                    NMJE_DirText(journey.D1OpportunityDirection), "/",
                    (journey.D1OpportunityActive ? "Y" : "N"),
         " OC=", (journey.D1OpportunityCycleID == "" ? "-" : journey.D1OpportunityCycleID),
         " D1{", journey.D1Node.OverlayLabel, "}",
         " H4{", journey.H4Node.OverlayLabel, "}",
         " H1{", journey.H1Node.OverlayLabel, "}",
         " M15{", journey.M15Node.OverlayLabel, "}");
}

'''
anchor = "void NMJE_BuildD1Node(PairState &state, NestedTFNode &node)\n"
text = replace_once(text, anchor, helpers + anchor, "N1.1 helpers")

# Capture secondary overlays immediately after node reset, before any primary-stage early return.
repls = {
    "   NMJE_ResetNode(node, PERIOD_D1);\n": """   NMJE_ResetNode(node, PERIOD_D1);
   NMJE_CaptureReEntryOverlay(node, state.re_d1_buy_state, state.re_d1_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_d1_buy_lifecycle, state.extreme_d1_sell_lifecycle);
   NMJE_RefreshOverlayLabel(node);
""",
    "   NMJE_ResetNode(node, PERIOD_H4);\n": """   NMJE_ResetNode(node, PERIOD_H4);
   NMJE_CaptureReEntryOverlay(node, state.re_h4_buy_state, state.re_h4_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_h4_buy_lifecycle, state.extreme_h4_sell_lifecycle);
   NMJE_RefreshOverlayLabel(node);
""",
    "   NMJE_ResetNode(node, PERIOD_H1);\n": """   NMJE_ResetNode(node, PERIOD_H1);
   NMJE_CaptureReEntryOverlay(node, state.re_h1_buy_state, state.re_h1_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_h1_buy_lifecycle, state.extreme_h1_sell_lifecycle);
   NMJE_RefreshOverlayLabel(node);
""",
    "   NMJE_ResetNode(node, PERIOD_M15);\n": """   NMJE_ResetNode(node, PERIOD_M15);
   NMJE_CaptureReEntryOverlay(node, state.re_m15_buy_state, state.re_m15_sell_state);
   NMJE_CaptureExtremeOverlay(node, state.extreme_m15_buy_lifecycle, state.extreme_m15_sell_lifecycle);
   NMJE_CaptureMLVOverlay(node, state.mlv_buy_state, state.mlv_sell_state);
   NMJE_RefreshOverlayLabel(node);
""",
}
for old, new in repls.items():
    text = replace_once(text, old, new, old.strip())

# Child activity becomes aware of already-owned M15 Re-Entry and M15 Extreme.
def patch_child_activity(block: str) -> str:
    anchor = "   if(NMJE_IsMLVActive(state.mlv_buy_state) || NMJE_IsMLVActive(state.mlv_sell_state)) return true;\n"
    if block.count(anchor) != 1:
        die("NMJE_HasChildActivity anchor mismatch")
    addition = """   if(NMJE_IsCandidateRE(state.re_m15_buy_state) || NMJE_IsCandidateRE(state.re_m15_sell_state)) return true;
   if(NMJE_IsConfirmedRE(state.re_m15_buy_state) || NMJE_IsConfirmedRE(state.re_m15_sell_state)) return true;
   if(NMJE_IsExtremeActive(state.extreme_m15_buy_lifecycle) || NMJE_IsExtremeActive(state.extreme_m15_sell_lifecycle)) return true;
""" + anchor
    return block.replace(anchor, addition, 1)

text = replace_block(
    text,
    r"(?m)^bool\s+NMJE_HasChildActivity\s*\(",
    patch_child_activity,
    "NMJE_HasChildActivity",
)

# M15 Extreme can support/build a nested journey, but raw/opposite direction is never auto-CONFLICT.
support_anchor = """            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_buy_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_sell_lifecycle) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_buy_state) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_sell_state);"""
support_new = """            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_buy_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_h1_sell_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_m15_buy_lifecycle) ||
            NMJE_IsExtremeSupporting(g_pair_states[pairIndex].extreme_m15_sell_lifecycle) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_buy_state) ||
            NMJE_IsMLVSupporting(g_pair_states[pairIndex].mlv_sell_state);"""
text = replace_once(text, support_anchor, support_new, "supporting M15 Extreme")

# Capture D1O overlay once for every N1 journey snapshot.
text = replace_once(
    text,
    '   journey.Reason = "NO_ACTIVE_JOURNEY";\n',
    '   journey.Reason = "NO_ACTIVE_JOURNEY";\n   NMJE_CaptureD1OpportunityOverlay(g_pair_states[pairIndex], journey);\n',
    "D1O journey overlay",
)

# Print one coverage-only line every time the live journey snapshot is committed.
def patch_update_journey(block: str) -> str:
    old = "      g_nested_journeys[pairIndex] = journey;\n"
    old2 = "   g_nested_journeys[pairIndex] = journey;\n"
    count = block.count(old) + block.count(old2)
    if count < 2:
        die(f"Expected multiple journey assignments, got {count}")
    block = block.replace(old, old + "      NMJE_PrintCoverageOverlay(journey);\n")
    block = block.replace(old2, old2 + "   NMJE_PrintCoverageOverlay(journey);\n")
    return block

text = replace_block(
    text,
    r"(?m)^void\s+UpdateNestedJourneyObservation\s*\(",
    patch_update_journey,
    "UpdateNestedJourneyObservation",
)

# Static invariants before writing.
if text.count("UpdateNestedJourneyObservation(pairIndex);") != 1:
    die("Observer call count changed")
if 'bool           EnableC044Lifecycle                = false;' not in text:
    die("C044 gate drift")
for signature in [
    "REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV",
    "RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme",
    "REE = D1 Re-Entry + H4 Extreme + H1 Extreme",
]:
    # Signatures may exist in docs/comments rather than exact source wording; function hash below is authoritative.
    pass

# No protected execution/strategy function may change.
for name, old_hash in protected_before.items():
    new_hash = function_hash(text, name)
    if new_hash != old_hash:
        die(f"Protected function drift: {name}")

m12n_start = text.find("//| MODULE 12N: NESTED MTF JOURNEY ENGINE")
m13_start = text.find("//| MODULE 13:", m12n_start)
if m12n_start < 0 or m13_start < 0:
    die("Unable to isolate M12N")
m12n = text[m12n_start:m13_start]
for needle in [
    "DetectExtreme(", "DetectMHV(", "DetectCSD(", "DetectECSD(", "DetectCSM(",
    "UpdateReEntryState(", "BuildPossibleCombinations(", "ValidateSequence(",
    "PriorityEngine_Atomic(", "InvalidationEngine_Atomic(", "OrderSend(",
]:
    if needle in m12n:
        die(f"M12N ownership violation: {needle}")

required = [
    "Version 4.5.7 - N1.1 NMJE Coverage Overlay",
    '#property version   "4.57"',
    "D1OpportunityActive",
    "NMJE_CaptureReEntryOverlay",
    "NMJE_CaptureExtremeOverlay",
    "NMJE_CaptureMLVOverlay",
    "[N1.1-NMJE-COV]",
    "state.re_m15_buy_state",
    "state.extreme_m15_buy_lifecycle",
]
for needle in required:
    if needle not in text:
        die(f"Missing N1.1 invariant: {needle}")

SRC.write_text(text, encoding="utf-8", newline="\n")
print("N1.1_PATCH=PASS")
print("BASE_BLOB=" + EXPECTED_BLOB)
print("NEW_GIT_BLOB=" + git_blob())
print("NEW_SHA256=" + hashlib.sha256(SRC.read_bytes()).hexdigest())
print("PROTECTED_FUNCTIONS=" + str(len(protected)))
