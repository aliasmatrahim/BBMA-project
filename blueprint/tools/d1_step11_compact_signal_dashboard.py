from pathlib import Path
import argparse

OLD = r'''void BuildDashboardSnapshot()
{
   g_dashboard_snapshot = "";
   g_dashboard_snapshot += "=== BBMA EA V4.5.1 D1-09 ===\n";
   g_dashboard_snapshot += "Time: " + TimeToString(TimeCurrent()) + "\n";
   g_dashboard_snapshot += "Balance: " + DoubleToString(AccountBalance(), 2) + "\n";
   g_dashboard_snapshot += "Equity: " + DoubleToString(AccountEquity(), 2) + "\n";
   g_dashboard_snapshot += "Trades: " + IntegerToString(g_monitored_count) + "\n";
   g_dashboard_snapshot += "Protection Ref: " + DoubleToString(g_protection_reference_equity, 2) + "\n";
   
   g_dashboard_snapshot += "\n--- SIGNALS ---\n";
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      g_dashboard_snapshot += g_pair_states[i].actual_symbol + ": ";
      if(g_pair_states[i].last_decision.Valid)
      {
         g_dashboard_snapshot += EnumToString(g_pair_states[i].last_decision.SignalType) + " ";
         g_dashboard_snapshot += EnumToString(g_pair_states[i].last_decision.Direction) + " ";
         g_dashboard_snapshot += "State:" + EnumToString(g_pair_states[i].last_decision.DecisionState);
         if(g_pair_states[i].last_decision.RejectionReason != REJ_NONE)
            g_dashboard_snapshot += " (" + EnumToString(g_pair_states[i].last_decision.RejectionReason) + ")";
      }
      else
      {
         g_dashboard_snapshot += "No Signal";
      }
      g_dashboard_snapshot += "\n";
   }
}

void UpdateDashboard()
{
   if(!ShowDashboard) return;
   Comment(g_dashboard_snapshot);
}
'''

NEW = r'''#define DASH_PREFIX "BBMA_DASH_"

color DashboardDirectionColor(ENUM_DIRECTION direction)
{
   if(direction == DIR_BUY) return clrLime;
   if(direction == DIR_SELL) return clrRed;
   return clrSilver;
}

string DashboardSignalShort(ENUM_SIGNAL_TYPE type)
{
   if(type == SIGNAL_EXTREME) return "EXT";
   if(type == SIGNAL_MHV) return "MHV";
   if(type == SIGNAL_MLV) return "MLV";
   if(type == SIGNAL_CSD) return "CSD";
   if(type == SIGNAL_ECSD) return "eCSD";
   if(type == SIGNAL_CSM) return "CSM";
   if(type == SIGNAL_RE_ENTRY) return "RE";
   if(type == SIGNAL_REM) return "REM";
   if(type == SIGNAL_RRE) return "RRE";
   if(type == SIGNAL_REE) return "REE";
   return "-";
}

int DashboardRERank(ENUM_RE_STATE state)
{
   if(state == RE_STATE_CONFIRMED) return 3;
   if(state == RE_STATE_CANDIDATE) return 2;
   return 0;
}

string DashboardRECode(ENUM_RE_STATE state)
{
   if(state == RE_STATE_CONFIRMED) return "RE:F";
   if(state == RE_STATE_CANDIDATE) return "RE:C";
   return "-";
}

bool DashboardFormatRE(ReEntryData &buyState, ReEntryData &sellState,
                       string &text, ENUM_DIRECTION &direction)
{
   int buyRank = DashboardRERank(buyState.State);
   int sellRank = DashboardRERank(sellState.State);
   if(buyRank == 0 && sellRank == 0)
   {
      text = "-";
      direction = DIR_NONE;
      return false;
   }

   if(buyRank > sellRank ||
      (buyRank == sellRank && buyState.LastUpdateCandleTime >= sellState.LastUpdateCandleTime))
   {
      text = DashboardRECode(buyState.State);
      direction = DIR_BUY;
   }
   else
   {
      text = DashboardRECode(sellState.State);
      direction = DIR_SELL;
   }
   return true;
}

int DashboardExtremeRank(ENUM_EXTREME_MATURITY maturity)
{
   if(maturity == EXT_MAT_RETEST_READY) return 4;
   if(maturity == EXT_MAT_RETEST_PHASE) return 3;
   if(maturity == EXT_MAT_REVERSAL_CONFIRMED) return 2;
   if(maturity == EXT_MAT_RAW) return 1;
   return 0;
}

string DashboardExtremeCode(ENUM_EXTREME_MATURITY maturity)
{
   if(maturity == EXT_MAT_RETEST_READY) return "EXT:RDY";
   if(maturity == EXT_MAT_RETEST_PHASE) return "EXT:RT";
   if(maturity == EXT_MAT_REVERSAL_CONFIRMED) return "EXT:REV";
   if(maturity == EXT_MAT_RAW) return "EXT:R";
   return "-";
}

bool DashboardFormatExtreme(ExtremeLifecycleData &buyState,
                            ExtremeLifecycleData &sellState,
                            string &text, ENUM_DIRECTION &direction)
{
   int buyRank = DashboardExtremeRank(buyState.Maturity);
   int sellRank = DashboardExtremeRank(sellState.Maturity);
   if(buyRank == 0 && sellRank == 0)
   {
      text = "-";
      direction = DIR_NONE;
      return false;
   }

   if(buyRank > sellRank ||
      (buyRank == sellRank && buyState.LastUpdateCandleTime >= sellState.LastUpdateCandleTime))
   {
      text = DashboardExtremeCode(buyState.Maturity);
      direction = DIR_BUY;
   }
   else
   {
      text = DashboardExtremeCode(sellState.Maturity);
      direction = DIR_SELL;
   }
   return true;
}

int DashboardMLVRank(ENUM_MLV_STATE state)
{
   if(state == MLV_DIRECTION_TAKEN) return 6;
   if(state == MLV_RETEST_COMPLETE) return 5;
   if(state == MLV_FORMATION_ESTABLISHED) return 4;
   if(state == MLV_LOSS_DEVELOPING) return 3;
   if(state == MLV_TP_COMPLETE) return 2;
   if(state == MLV_PARENT_READY) return 1;
   return 0;
}

string DashboardMLVCode(ENUM_MLV_STATE state)
{
   if(state == MLV_DIRECTION_TAKEN) return "MHV:T";
   if(state == MLV_RETEST_COMPLETE) return "MHV:RT";
   if(state == MLV_FORMATION_ESTABLISHED) return "MHV:F";
   if(state == MLV_LOSS_DEVELOPING) return "MHV:L";
   if(state == MLV_TP_COMPLETE) return "MHV:TP";
   if(state == MLV_PARENT_READY) return "MHV:P";
   return "-";
}

bool DashboardFormatM15(MLVData &buyState, MLVData &sellState,
                        string &text, ENUM_DIRECTION &direction)
{
   int buyRank = DashboardMLVRank(buyState.State);
   int sellRank = DashboardMLVRank(sellState.State);
   if(buyRank == 0 && sellRank == 0)
   {
      text = "-";
      direction = DIR_NONE;
      return false;
   }

   if(buyRank > sellRank ||
      (buyRank == sellRank && buyState.LastUpdateCandleTime >= sellState.LastUpdateCandleTime))
   {
      text = DashboardMLVCode(buyState.State);
      direction = DIR_BUY;
   }
   else
   {
      text = DashboardMLVCode(sellState.State);
      direction = DIR_SELL;
   }
   return true;
}

void DashboardD1Cell(PairState &state, string &text, ENUM_DIRECTION &direction)
{
   if(DashboardFormatRE(state.re_d1_buy_state, state.re_d1_sell_state, text, direction))
      return;
   text = "-";
   direction = DIR_NONE;
}

void DashboardH4Cell(PairState &state, string &text, ENUM_DIRECTION &direction)
{
   if(DashboardFormatRE(state.re_h4_buy_state, state.re_h4_sell_state, text, direction))
      return;

   if(DashboardFormatExtreme(state.extreme_h4_buy_lifecycle,
                             state.extreme_h4_sell_lifecycle,
                             text, direction))
      return;

   if(state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
      state.h4_direction_owner.IsValid &&
      state.h4_direction_owner.SourceSignal != SIGNAL_NONE)
   {
      text = DashboardSignalShort(state.h4_direction_owner.SourceSignal);
      direction = state.h4_direction_owner.Direction;
      return;
   }

   text = "-";
   direction = DIR_NONE;
}

void DashboardH1Cell(PairState &state, string &text, ENUM_DIRECTION &direction)
{
   if(DashboardFormatRE(state.re_h1_buy_state, state.re_h1_sell_state, text, direction))
      return;

   if(DashboardFormatExtreme(state.extreme_h1_buy_lifecycle,
                             state.extreme_h1_sell_lifecycle,
                             text, direction))
      return;

   text = "-";
   direction = DIR_NONE;
}

void DashboardM15Cell(PairState &state, string &text, ENUM_DIRECTION &direction)
{
   if(DashboardFormatM15(state.mlv_buy_state, state.mlv_sell_state, text, direction))
      return;
   text = "-";
   direction = DIR_NONE;
}

void DashboardFinalCell(PairState &state, string &text, ENUM_DIRECTION &direction)
{
   if(!state.last_decision.Valid)
   {
      text = "-";
      direction = DIR_NONE;
      return;
   }

   text = DashboardSignalShort(state.last_decision.SignalType);
   if(state.last_decision.DecisionState == DEC_VALIDATED) text += ":V";
   else if(state.last_decision.DecisionState == DEC_EXECUTED) text += ":E";
   else if(state.last_decision.DecisionState == DEC_REJECTED) text += ":X";
   else if(state.last_decision.DecisionState == DEC_CREATED) text += ":C";
   else if(state.last_decision.DecisionState == DEC_EXPIRED) text += ":X";

   direction = state.last_decision.Direction;
}

bool DashboardOwnsMagic(int magic)
{
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      if(g_pair_states[i].magic_number == magic) return true;
   }
   return false;
}

int DashboardLiveTradeCount()
{
   int count = 0;
   for(int pos = OrdersTotal() - 1; pos >= 0; pos--)
   {
      if(!OrderSelect(pos, SELECT_BY_POS, MODE_TRADES)) continue;
      int type = OrderType();
      if(type != OP_BUY && type != OP_SELL) continue;
      if(!DashboardOwnsMagic(OrderMagicNumber())) continue;
      count++;
   }
   return count;
}

void DashboardSetLabel(string key, string text, int x, int y, color textColor, int fontSize)
{
   string name = DASH_PREFIX + key;
   if(ObjectFind(name) < 0)
      ObjectCreate(name, OBJ_LABEL, 0, 0, 0);

   ObjectSet(name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSet(name, OBJPROP_XDISTANCE, x);
   ObjectSet(name, OBJPROP_YDISTANCE, y);
   ObjectSet(name, OBJPROP_SELECTABLE, false);
   ObjectSetText(name, text, fontSize, "Consolas", textColor);
}

void ClearDashboardObjects()
{
   for(int i = ObjectsTotal() - 1; i >= 0; i--)
   {
      string name = ObjectName(i);
      if(StringFind(name, DASH_PREFIX, 0) == 0)
         ObjectDelete(name);
   }
}

void BuildDashboardSnapshot()
{
   // Object-label dashboard reads live state directly in UpdateDashboard().
   g_dashboard_snapshot = "";
}

void UpdateDashboard()
{
   if(!ShowDashboard)
   {
      ClearDashboardObjects();
      Comment("");
      return;
   }

   Comment("");

   DashboardSetLabel("TITLE", "BBMA EA 4.5.1", 8, 6, clrWhite, 9);
   string summary = "Bal " + DoubleToString(AccountBalance(), 2) +
                    "  Eq " + DoubleToString(AccountEquity(), 2) +
                    "  Live " + IntegerToString(DashboardLiveTradeCount()) +
                    "  Ref " + DoubleToString(g_protection_reference_equity, 2);
   DashboardSetLabel("SUMMARY", summary, 8, 22, clrSilver, 8);

   DashboardSetLabel("H_PAIR", "PAIR", 8, 42, clrAqua, 8);
   DashboardSetLabel("H_D1", "D1", 78, 42, clrAqua, 8);
   DashboardSetLabel("H_H4", "H4", 150, 42, clrAqua, 8);
   DashboardSetLabel("H_H1", "H1", 222, 42, clrAqua, 8);
   DashboardSetLabel("H_M15", "M15", 294, 42, clrAqua, 8);
   DashboardSetLabel("H_FINAL", "FINAL", 378, 42, clrAqua, 8);

   int row = 0;
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;

      int y = 58 + row * 14;
      string suffix = IntegerToString(i);
      DashboardSetLabel("P_" + suffix, g_pair_states[i].actual_symbol, 8, y, clrWhite, 8);

      string d1Text, h4Text, h1Text, m15Text, finalText;
      ENUM_DIRECTION d1Dir, h4Dir, h1Dir, m15Dir, finalDir;
      d1Dir = DIR_NONE; h4Dir = DIR_NONE; h1Dir = DIR_NONE;
      m15Dir = DIR_NONE; finalDir = DIR_NONE;

      DashboardD1Cell(g_pair_states[i], d1Text, d1Dir);
      DashboardH4Cell(g_pair_states[i], h4Text, h4Dir);
      DashboardH1Cell(g_pair_states[i], h1Text, h1Dir);
      DashboardM15Cell(g_pair_states[i], m15Text, m15Dir);
      DashboardFinalCell(g_pair_states[i], finalText, finalDir);

      DashboardSetLabel("D1_" + suffix, d1Text, 78, y, DashboardDirectionColor(d1Dir), 8);
      DashboardSetLabel("H4_" + suffix, h4Text, 150, y, DashboardDirectionColor(h4Dir), 8);
      DashboardSetLabel("H1_" + suffix, h1Text, 222, y, DashboardDirectionColor(h1Dir), 8);
      DashboardSetLabel("M15_" + suffix, m15Text, 294, y, DashboardDirectionColor(m15Dir), 8);
      DashboardSetLabel("F_" + suffix, finalText, 378, y, DashboardDirectionColor(finalDir), 8);
      row++;
   }

   WindowRedraw();
}
'''

DEINIT_OLD = r'''   if(ShowDashboard)
      Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));'''

DEINIT_NEW = r'''   ClearDashboardObjects();
   Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));'''

TIMER_OLD = r'''   if(!IsTerminalConnected()) return;
   OnTickMain();
}'''

TIMER_NEW = r'''   if(!IsTerminalConnected()) return;
   OnTickMain();

   static datetime lastDashboardRefresh = 0;
   datetime dashboardNow = TimeCurrent();
   if(ShowDashboard && dashboardNow - lastDashboardRefresh >= 5)
   {
      UpdateDashboard();
      lastDashboardRefresh = dashboardNow;
   }
}'''


def apply(text: str) -> str:
    if '#define DASH_PREFIX "BBMA_DASH_"' in text:
        return text
    if OLD not in text:
        raise SystemExit('Module 25 baseline block not found')
    if DEINIT_OLD not in text:
        raise SystemExit('OnDeinit baseline block not found')
    if text.count(TIMER_OLD) != 1:
        raise SystemExit(f'OnTimer tail anchor count={text.count(TIMER_OLD)}')
    text = text.replace(OLD, NEW, 1)
    text = text.replace(DEINIT_OLD, DEINIT_NEW, 1)
    text = text.replace(TIMER_OLD, TIMER_NEW, 1)
    return text


def verify(text: str) -> None:
    required = [
        '#define DASH_PREFIX "BBMA_DASH_"',
        'void DashboardD1Cell(',
        'void DashboardH4Cell(',
        'void DashboardH1Cell(',
        'void DashboardM15Cell(',
        'void DashboardFinalCell(',
        'int DashboardLiveTradeCount()',
        'void ClearDashboardObjects()',
        'DashboardSetLabel("H_PAIR", "PAIR"',
        'DashboardSetLabel("H_D1", "D1"',
        'DashboardSetLabel("H_H4", "H4"',
        'DashboardSetLabel("H_H1", "H1"',
        'DashboardSetLabel("H_M15", "M15"',
        'DashboardSetLabel("H_FINAL", "FINAL"',
        'dashboardNow - lastDashboardRefresh >= 5',
    ]
    for item in required:
        if item not in text:
            raise SystemExit(f'missing: {item}')
    if 'Trades: " + IntegerToString(g_monitored_count)' in text:
        raise SystemExit('legacy monitored-count dashboard still present')
    if text.count('void UpdateDashboard()') != 1:
        raise SystemExit('UpdateDashboard duplicated')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', required=True)
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    path = Path(args.repo_root) / 'blueprint/source/BBMA_EA.mq4'
    text = path.read_text(encoding='utf-8')
    if args.verify:
        verify(text)
        print('D1-11 compact signal dashboard verified.')
        return
    new_text = apply(text)
    verify(new_text)
    path.write_text(new_text, encoding='utf-8')
    print('D1-11 compact signal dashboard applied.')


if __name__ == '__main__':
    main()
