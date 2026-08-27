from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4')
text = SRC.read_text(encoding='utf-8')
start = text.index('//| MODULE 25: DASHBOARD ENGINE')
end = text.index('//| MODULE 26: INITIALIZATION & CLEANUP')
prefix_start = text.rfind('//+------------------------------------------------------------------+', 0, start)
prefix_end = text.rfind('//+------------------------------------------------------------------+', 0, end)

new_block = r'''//+------------------------------------------------------------------+
//| MODULE 25: DASHBOARD ENGINE                                      |
//| LEVEL: BEGINNER                                                  |
//+------------------------------------------------------------------+

#define DASH_PREFIX "BBMA_DASH_"

string DashArrow(ENUM_DIRECTION direction)
{
   if(direction == DIR_BUY) return "↑";
   if(direction == DIR_SELL) return "↓";
   return "";
}

color DashDirectionColor(ENUM_DIRECTION direction)
{
   if(direction == DIR_BUY) return clrLime;
   if(direction == DIR_SELL) return clrRed;
   return clrSilver;
}

bool DashREConfirmed(ReEntryData &state, ENUM_DIRECTION direction)
{
   return (state.IsValid && state.State == RE_STATE_CONFIRMED &&
           state.Direction == direction && state.ConfirmationCandle > 0);
}

bool DashExtremeReady(ExtremeLifecycleData &state, ENUM_DIRECTION direction)
{
   if(!state.IsValid || state.Direction != direction) return false;
   return (state.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           state.Maturity == EXT_MAT_RETEST_PHASE ||
           state.Maturity == EXT_MAT_RETEST_READY);
}

bool DashMLVReady(MLVData &state, ENUM_DIRECTION direction)
{
   if(state.Direction != direction) return false;
   return (state.State == MLV_FORMATION_ESTABLISHED ||
           state.State == MLV_RETEST_COMPLETE ||
           state.State == MLV_DIRECTION_TAKEN);
}

string DashLivePosition(int pairIndex, ENUM_DIRECTION &direction)
{
   direction = DIR_NONE;
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int selectedPairIndex = -1;
      if(!IsExactEAOwnedSelectedOrder(selectedPairIndex)) continue;
      if(selectedPairIndex != pairIndex) continue;
      int type = OrderType();
      if(type == OP_BUY)
      {
         direction = DIR_BUY;
         return "POS↑";
      }
      if(type == OP_SELL)
      {
         direction = DIR_SELL;
         return "POS↓";
      }
   }
   return "";
}

int CountDashboardLiveEAOwnedTrades()
{
   int count = 0;
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int pairIdx = -1;
      if(IsExactEAOwnedSelectedOrder(pairIdx)) count++;
   }
   return count;
}

string DashSignalText(ENUM_SIGNAL_TYPE signalType)
{
   if(signalType == SIGNAL_REM) return "REM";
   if(signalType == SIGNAL_RRE) return "RRE";
   if(signalType == SIGNAL_REE) return "REE";
   if(signalType == SIGNAL_RE_ENTRY) return "RE";
   return "-";
}

bool DashDecisionComplete(PairState &state)
{
   if(!state.last_decision.Valid) return false;
   return (state.last_decision.DecisionState == DEC_VALIDATED ||
           state.last_decision.DecisionState == DEC_EXECUTED);
}

void DashBuildDirectionChain(PairState &state, ENUM_DIRECTION direction,
                             string &setup, string &chain, string &status,
                             int &rank)
{
   setup = "-";
   chain = "-";
   status = "IDL";
   rank = 0;

   ReEntryData d1re, h4re, h1re;
   ExtremeLifecycleData h4ext, h1ext;
   MLVData m15mlv;
   ZeroMemory(d1re); ZeroMemory(h4re); ZeroMemory(h1re);
   ZeroMemory(h4ext); ZeroMemory(h1ext); ZeroMemory(m15mlv);

   if(direction == DIR_BUY)
   {
      d1re = state.re_d1_buy_state;
      h4re = state.re_h4_buy_state;
      h1re = state.re_h1_buy_state;
      h4ext = state.extreme_h4_buy_lifecycle;
      h1ext = state.extreme_h1_buy_lifecycle;
      m15mlv = state.mlv_buy_state;
   }
   else
   {
      d1re = state.re_d1_sell_state;
      h4re = state.re_h4_sell_state;
      h1re = state.re_h1_sell_state;
      h4ext = state.extreme_h4_sell_lifecycle;
      h1ext = state.extreme_h1_sell_lifecycle;
      m15mlv = state.mlv_sell_state;
   }

   string arrow = DashArrow(direction);

   // REM exact signature prefix: H4 RE > H1 EXT > M15 MHV/MLV.
   if(DashREConfirmed(h4re, direction))
   {
      setup = "REM";
      chain = "H4:RE" + arrow;
      status = "ST";
      rank = 10;
      if(DashExtremeReady(h1ext, direction))
      {
         chain += ">H1:EXT" + arrow;
         status = "BLD";
         rank = 20;
         if(DashMLVReady(m15mlv, direction))
         {
            chain += ">M15:MHV" + arrow;
            rank = 30;
         }
      }
   }

   // RRE exact signature prefix: D1 RE > H4 RE > H1 EXT.
   if(DashREConfirmed(d1re, direction))
   {
      string rreChain = "D1:RE" + arrow;
      int rreRank = 11;
      string rreStatus = "ST";
      if(DashREConfirmed(h4re, direction))
      {
         rreChain += ">H4:RE" + arrow;
         rreRank = 21;
         rreStatus = "BLD";
         if(DashExtremeReady(h1ext, direction))
         {
            rreChain += ">H1:EXT" + arrow;
            rreRank = 31;
         }
      }
      if(rreRank > rank)
      {
         setup = "RRE";
         chain = rreChain;
         status = rreStatus;
         rank = rreRank;
      }

      // REE exact signature prefix: D1 RE > H4 EXT > H1 EXT.
      string reeChain = "D1:RE" + arrow;
      int reeRank = 12;
      string reeStatus = "ST";
      if(DashExtremeReady(h4ext, direction))
      {
         reeChain += ">H4:EXT" + arrow;
         reeRank = 22;
         reeStatus = "BLD";
         if(DashExtremeReady(h1ext, direction))
         {
            reeChain += ">H1:EXT" + arrow;
            reeRank = 32;
         }
      }
      if(reeRank > rank)
      {
         setup = "REE";
         chain = reeChain;
         status = reeStatus;
         rank = reeRank;
      }
   }

   // Standalone H1 Re-Entry remains visible when it is the only active setup.
   if(rank == 0 && DashREConfirmed(h1re, direction))
   {
      setup = "RE";
      chain = "H1:RE" + arrow;
      status = "ST";
      rank = 9;
   }

   // M15 remains authoritative for setup completion/invalidation display.
   if(state.last_decision.Valid && state.last_decision.Direction == direction)
   {
      string finalSetup = DashSignalText(state.last_decision.SignalType);
      if(finalSetup != "-") setup = finalSetup;
      if(DashDecisionComplete(state))
      {
         setup += "✓";
         if(rank < 40) rank = 40;
      }
      else if(state.last_decision.DecisionState == DEC_REJECTED ||
              state.last_decision.DecisionState == DEC_EXPIRED)
      {
         status = "INV";
      }
   }
}

void DashBuildPairRow(int pairIndex, string &status, string &setup,
                      string &chain, string &position,
                      ENUM_DIRECTION &rowDirection,
                      ENUM_DIRECTION &positionDirection)
{
   PairState state = g_pair_states[pairIndex];
   string buySetup, buyChain, buyStatus;
   string sellSetup, sellChain, sellStatus;
   int buyRank = 0, sellRank = 0;

   DashBuildDirectionChain(state, DIR_BUY, buySetup, buyChain, buyStatus, buyRank);
   DashBuildDirectionChain(state, DIR_SELL, sellSetup, sellChain, sellStatus, sellRank);

   rowDirection = DIR_NONE;
   status = "IDL";
   setup = "-";
   chain = "-";

   if(buyRank > 0 || sellRank > 0)
   {
      if(buyRank >= sellRank)
      {
         rowDirection = DIR_BUY;
         status = buyStatus;
         setup = buySetup;
         chain = buyChain;
      }
      else
      {
         rowDirection = DIR_SELL;
         status = sellStatus;
         setup = sellSetup;
         chain = sellChain;
      }
   }

   position = DashLivePosition(pairIndex, positionDirection);
}

color DashStatusColor(string status)
{
   if(status == "INV") return clrRed;
   if(status == "BLD") return clrAqua;
   if(status == "ST") return clrYellow;
   return clrSilver;
}

void DashSetLabel(string key, string text, int x, int y, color textColor, int fontSize)
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
   // Display-only: dashboard reads current canonical state directly.
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

   string summary = "BBMA EA 4.5.9 | Bal " + DoubleToString(AccountBalance(), 2) +
                    " | Eq " + DoubleToString(AccountEquity(), 2) +
                    " | Live " + IntegerToString(CountDashboardLiveEAOwnedTrades());
   DashSetLabel("TITLE", summary, 8, 6, clrWhite, 8);

   // Fixed X positions keep every category vertically aligned.
   DashSetLabel("H_PAIR",  "PAIR",  8,   25, clrAqua, 8);
   DashSetLabel("S1",      "|",     67,  25, clrSilver, 8);
   DashSetLabel("H_ST",    "ST",    76,  25, clrAqua, 8);
   DashSetLabel("S2",      "|",     99,  25, clrSilver, 8);
   DashSetLabel("H_SETUP", "SETUP", 108, 25, clrAqua, 8);
   DashSetLabel("S3",      "|",     151, 25, clrSilver, 8);
   DashSetLabel("H_CHAIN", "CHAIN", 160, 25, clrAqua, 8);
   DashSetLabel("S4",      "|",     430, 25, clrSilver, 8);
   DashSetLabel("H_POS",   "POS",   439, 25, clrAqua, 8);

   int row = 0;
   for(int i = 0; i < g_pair_count; i++)
   {
      if(!g_pair_states[i].pair_enabled) continue;
      int y = 40 + row * 14;
      string suffix = IntegerToString(i);

      string status, setup, chain, position;
      ENUM_DIRECTION rowDirection = DIR_NONE;
      ENUM_DIRECTION positionDirection = DIR_NONE;
      DashBuildPairRow(i, status, setup, chain, position, rowDirection, positionDirection);

      DashSetLabel("P_" + suffix, g_pair_states[i].actual_symbol, 8, y, clrWhite, 8);
      DashSetLabel("R1_" + suffix, "|", 67, y, clrSilver, 8);
      DashSetLabel("ST_" + suffix, status, 76, y, DashStatusColor(status), 8);
      DashSetLabel("R2_" + suffix, "|", 99, y, clrSilver, 8);
      DashSetLabel("SU_" + suffix, setup, 108, y, DashDirectionColor(rowDirection), 8);
      DashSetLabel("R3_" + suffix, "|", 151, y, clrSilver, 8);
      DashSetLabel("CH_" + suffix, chain, 160, y, DashDirectionColor(rowDirection), 8);
      DashSetLabel("R4_" + suffix, "|", 430, y, clrSilver, 8);
      DashSetLabel("PO_" + suffix, position, 439, y, DashDirectionColor(positionDirection), 8);
      row++;
   }

   WindowRedraw();
}

void RefreshDashboardLiveTradeCount()
{
   if(!ShowDashboard) return;
   // Timer refresh keeps both chain lifecycle and live broker position in sync.
   UpdateDashboard();
   g_dashboard_needs_update = false;
}

'''

text = text[:prefix_start] + new_block + text[prefix_end:]
SRC.write_text(text, encoding='utf-8')
print('DASHBOARD_COMPACT_CHAIN_M25=APPLIED')
