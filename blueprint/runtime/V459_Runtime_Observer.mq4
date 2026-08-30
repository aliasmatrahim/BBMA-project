//+------------------------------------------------------------------+
//| V459 Runtime Observer                                            |
//| TEST/OBSERVABILITY ONLY - NO BROKER WRITE AUTHORITY              |
//+------------------------------------------------------------------+
#property strict
#property version   "1.10"

input int StrategyID = 1;
input int InstanceID = 0;
input int SnapshotSeconds = 5;
input int HistoryLookbackHours = 168;

#define MAGIC_BASE 100000
#define PAIR_ID_MIN 1
#define PAIR_ID_MAX 99

string TokenSafe(string value)
{
   StringReplace(value, " ", "~");
   StringReplace(value, "\t", "~");
   return value;
}

string OrderTypeText(int type)
{
   if(type == OP_BUY)  return "BUY";
   if(type == OP_SELL) return "SELL";
   return "OTHER";
}

int MinOwnedMagic()
{
   return MAGIC_BASE + StrategyID * 10000 + InstanceID * 100 + PAIR_ID_MIN;
}

int MaxOwnedMagic()
{
   return MAGIC_BASE + StrategyID * 10000 + InstanceID * 100 + PAIR_ID_MAX;
}

bool IsOwnedMagic(int magic)
{
   return (magic >= MinOwnedMagic() && magic <= MaxOwnedMagic());
}

bool IsRelevantGV(string name)
{
   string d1Prefix = "D1TPW|S" + IntegerToString(StrategyID) + "|I" + IntegerToString(InstanceID) + "|T";
   string c044Prefix = "C044|S" + IntegerToString(StrategyID) + "|I" + IntegerToString(InstanceID) + "|T";
   string hashPrefix = "BBXH|S" + IntegerToString(StrategyID) + "|I" + IntegerToString(InstanceID) + "|H";
   string ticketPrefix = "BBXT|S" + IntegerToString(StrategyID) + "|I" + IntegerToString(InstanceID) + "|T";
   return (StringFind(name, d1Prefix, 0) == 0 ||
           StringFind(name, c044Prefix, 0) == 0 ||
           StringFind(name, hashPrefix, 0) == 0 ||
           StringFind(name, ticketPrefix, 0) == 0);
}

void PrintEnvironment(datetime now)
{
   Print("[V459-OBS][ENV] TS=", (int)now,
         " Demo=", (IsDemo() ? "Y" : "N"),
         " Connected=", (IsConnected() ? "Y" : "N"),
         " TradeAllowed=", (IsTradeAllowed() ? "Y" : "N"));
}

void PrintGlobals(datetime now)
{
   int total = GlobalVariablesTotal();
   for(int i = 0; i < total; i++)
   {
      string name = GlobalVariableName(i);
      if(!IsRelevantGV(name)) continue;
      if(!GlobalVariableCheck(name)) continue;
      double value = GlobalVariableGet(name);
      Print("[V459-OBS][GV] TS=", (int)now,
            " Name=", TokenSafe(name),
            " Value=", DoubleToString(value, 8));
   }
}

void PrintOpenOrders(datetime now)
{
   for(int pos = OrdersTotal() - 1; pos >= 0; pos--)
   {
      if(!OrderSelect(pos, SELECT_BY_POS, MODE_TRADES)) continue;
      int type = OrderType();
      if(type != OP_BUY && type != OP_SELL) continue;
      if(!IsOwnedMagic(OrderMagicNumber())) continue;
      Print("[V459-OBS][OPEN] TS=", (int)now,
            " Ticket=", OrderTicket(),
            " Pair=", TokenSafe(OrderSymbol()),
            " Type=", OrderTypeText(type),
            " Magic=", OrderMagicNumber(),
            " OpenTime=", (int)OrderOpenTime(),
            " Open=", DoubleToString(OrderOpenPrice(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " SL=", DoubleToString(OrderStopLoss(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " TP=", DoubleToString(OrderTakeProfit(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " Lots=", DoubleToString(OrderLots(), 4),
            " Comment=", TokenSafe(OrderComment()));
   }
}

void PrintRecentHistory(datetime now)
{
   int hours = HistoryLookbackHours;
   if(hours < 1) hours = 1;
   datetime cutoff = now - hours * 3600;
   for(int pos = OrdersHistoryTotal() - 1; pos >= 0; pos--)
   {
      if(!OrderSelect(pos, SELECT_BY_POS, MODE_HISTORY)) continue;
      int type = OrderType();
      if(type != OP_BUY && type != OP_SELL) continue;
      if(!IsOwnedMagic(OrderMagicNumber())) continue;
      if(OrderCloseTime() <= 0 || OrderCloseTime() < cutoff) continue;
      double net = OrderProfit() + OrderSwap() + OrderCommission();
      Print("[V459-OBS][HIST] TS=", (int)now,
            " Ticket=", OrderTicket(),
            " Pair=", TokenSafe(OrderSymbol()),
            " Type=", OrderTypeText(type),
            " Magic=", OrderMagicNumber(),
            " OpenTime=", (int)OrderOpenTime(),
            " CloseTime=", (int)OrderCloseTime(),
            " Open=", DoubleToString(OrderOpenPrice(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " Close=", DoubleToString(OrderClosePrice(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " SL=", DoubleToString(OrderStopLoss(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " TP=", DoubleToString(OrderTakeProfit(), (int)MarketInfo(OrderSymbol(), MODE_DIGITS)),
            " Lots=", DoubleToString(OrderLots(), 4),
            " Net=", DoubleToString(net, 2),
            " Comment=", TokenSafe(OrderComment()));
   }
}

void EmitSnapshot()
{
   datetime now = TimeCurrent();
   PrintEnvironment(now);
   PrintGlobals(now);
   PrintOpenOrders(now);
   PrintRecentHistory(now);
   Print("[V459-OBS][SNAP_END] TS=", (int)now);
}

int OnInit()
{
   int seconds = SnapshotSeconds;
   if(seconds < 1) seconds = 1;
   Print("[V459-OBS][START] TS=", (int)TimeCurrent(),
         " StrategyID=", StrategyID,
         " InstanceID=", InstanceID,
         " MagicMin=", MinOwnedMagic(),
         " MagicMax=", MaxOwnedMagic());
   EventSetTimer(seconds);
   EmitSnapshot();
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   EmitSnapshot();
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   Print("[V459-OBS][STOP] TS=", (int)TimeCurrent(), " Reason=", reason);
}

void OnTick()
{
   // Intentionally empty. Observation is timer-driven.
}
