//+------------------------------------------------------------------+
//| V459 Runtime Observer                                            |
//| TEST/OBSERVABILITY ONLY - NO BROKER WRITE AUTHORITY              |
//+------------------------------------------------------------------+
#property strict
#property version   "1.10"

input int StrategyID = 1;
input int InstanceID = 0;
input int SnapshotSeconds = 5;          // Poll cadence; unchanged state is silent.
input int HistoryLookbackHours = 168;
input int ObserverDebugLevel = 0;       // 0=event-only, 1=verbose every poll.
input bool EmitInitialHistoryDetails = false;

#define MAGIC_BASE 100000
#define PAIR_ID_MIN 1
#define PAIR_ID_MAX 99

string g_last_environment = "";
string g_last_gv_records[];
string g_last_open_records[];
string g_last_history_records[];
string g_last_printed_record = "";
bool   g_first_poll = true;

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

void EmitLine(string record)
{
   // OBS-FIX-01: identical consecutive observer records are never repeated.
   if(record == g_last_printed_record) return;
   Print(record);
   g_last_printed_record = record;
}

string TaggedRecord(string tag, datetime now, string payload)
{
   string record = "[V459-OBS][" + tag + "] TS=" + IntegerToString((int)now);
   if(payload != "") record += " " + payload;
   return record;
}

void SortRecords(string &records[])
{
   int count = ArraySize(records);
   for(int i = 1; i < count; i++)
   {
      string key = records[i];
      int j = i - 1;
      while(j >= 0 && StringCompare(records[j], key) > 0)
      {
         records[j + 1] = records[j];
         j--;
      }
      records[j + 1] = key;
   }
}

bool RecordsEqual(string &left[], string &right[])
{
   int leftCount = ArraySize(left);
   int rightCount = ArraySize(right);
   if(leftCount != rightCount) return false;
   for(int i = 0; i < leftCount; i++)
      if(left[i] != right[i]) return false;
   return true;
}

bool ContainsRecord(string &records[], string value)
{
   int count = ArraySize(records);
   for(int i = 0; i < count; i++)
      if(records[i] == value) return true;
   return false;
}

void CopyRecords(string &source[], string &destination[])
{
   int count = ArraySize(source);
   ArrayResize(destination, count);
   for(int i = 0; i < count; i++)
      destination[i] = source[i];
}

void EmitAllRecords(string tag, datetime now, string &records[])
{
   int count = ArraySize(records);
   for(int i = 0; i < count; i++)
      EmitLine(TaggedRecord(tag, now, records[i]));
}

void EmitNewOrChangedRecords(string tag, datetime now,
                             string &current[], string &previous[])
{
   int count = ArraySize(current);
   for(int i = 0; i < count; i++)
      if(!ContainsRecord(previous, current[i]))
         EmitLine(TaggedRecord(tag, now, current[i]));
}

string EnvironmentRecord()
{
   string connected = IsConnected() ? "Y" : "N";
   string tradeAllowed = IsTradeAllowed() ? "Y" : "N";
   return "Connected=" + connected + " TradeAllowed=" + tradeAllowed;
}

void CollectGlobals(string &records[])
{
   ArrayResize(records, 0);
   int total = GlobalVariablesTotal();
   for(int i = 0; i < total; i++)
   {
      string name = GlobalVariableName(i);
      if(!IsRelevantGV(name)) continue;
      if(!GlobalVariableCheck(name)) continue;

      int size = ArraySize(records);
      ArrayResize(records, size + 1);
      records[size] = "Name=" + TokenSafe(name) +
                      " Value=" + DoubleToString(GlobalVariableGet(name), 8);
   }
   SortRecords(records);
}

string SelectedOpenOrderRecord()
{
   string symbol = OrderSymbol();
   int digits = (int)MarketInfo(symbol, MODE_DIGITS);
   return "Ticket=" + IntegerToString(OrderTicket()) +
          " Pair=" + TokenSafe(symbol) +
          " Type=" + OrderTypeText(OrderType()) +
          " Magic=" + IntegerToString(OrderMagicNumber()) +
          " OpenTime=" + IntegerToString((int)OrderOpenTime()) +
          " Open=" + DoubleToString(OrderOpenPrice(), digits) +
          " SL=" + DoubleToString(OrderStopLoss(), digits) +
          " TP=" + DoubleToString(OrderTakeProfit(), digits) +
          " Lots=" + DoubleToString(OrderLots(), 4) +
          " Comment=" + TokenSafe(OrderComment());
}

void CollectOpenOrders(string &records[])
{
   ArrayResize(records, 0);
   for(int pos = OrdersTotal() - 1; pos >= 0; pos--)
   {
      if(!OrderSelect(pos, SELECT_BY_POS, MODE_TRADES)) continue;
      int type = OrderType();
      if(type != OP_BUY && type != OP_SELL) continue;
      if(!IsOwnedMagic(OrderMagicNumber())) continue;

      int size = ArraySize(records);
      ArrayResize(records, size + 1);
      records[size] = SelectedOpenOrderRecord();
   }
   SortRecords(records);
}

string SelectedHistoryRecord()
{
   string symbol = OrderSymbol();
   int digits = (int)MarketInfo(symbol, MODE_DIGITS);
   double net = OrderProfit() + OrderSwap() + OrderCommission();
   return "Ticket=" + IntegerToString(OrderTicket()) +
          " Pair=" + TokenSafe(symbol) +
          " Type=" + OrderTypeText(OrderType()) +
          " Magic=" + IntegerToString(OrderMagicNumber()) +
          " OpenTime=" + IntegerToString((int)OrderOpenTime()) +
          " CloseTime=" + IntegerToString((int)OrderCloseTime()) +
          " Open=" + DoubleToString(OrderOpenPrice(), digits) +
          " Close=" + DoubleToString(OrderClosePrice(), digits) +
          " SL=" + DoubleToString(OrderStopLoss(), digits) +
          " TP=" + DoubleToString(OrderTakeProfit(), digits) +
          " Lots=" + DoubleToString(OrderLots(), 4) +
          " Net=" + DoubleToString(net, 2) +
          " Comment=" + TokenSafe(OrderComment());
}

void CollectRecentHistory(datetime now, string &records[])
{
   ArrayResize(records, 0);
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

      int size = ArraySize(records);
      ArrayResize(records, size + 1);
      records[size] = SelectedHistoryRecord();
   }
   SortRecords(records);
}

bool PollObservableState()
{
   datetime now = TimeCurrent();
   bool verbose = (ObserverDebugLevel > 0);
   bool changed = false;

   string environment = EnvironmentRecord();
   if(g_first_poll || environment != g_last_environment || verbose)
   {
      EmitLine(TaggedRecord("ENV", now, environment));
      if(g_first_poll || environment != g_last_environment) changed = true;
   }

   string gvRecords[];
   CollectGlobals(gvRecords);
   bool gvChanged = !RecordsEqual(gvRecords, g_last_gv_records);
   if(g_first_poll || gvChanged || verbose)
   {
      EmitLine(TaggedRecord("GV_CHANGE", now,
               "Count=" + IntegerToString(ArraySize(gvRecords)) +
               " Prev=" + IntegerToString(ArraySize(g_last_gv_records))));
      if(verbose || g_first_poll)
         EmitAllRecords("GV", now, gvRecords);
      else
         EmitNewOrChangedRecords("GV", now, gvRecords, g_last_gv_records);
      if(g_first_poll || gvChanged) changed = true;
   }

   string openRecords[];
   CollectOpenOrders(openRecords);
   bool openChanged = !RecordsEqual(openRecords, g_last_open_records);
   if(g_first_poll || openChanged || verbose)
   {
      EmitLine(TaggedRecord("OPEN_CHANGE", now,
               "Count=" + IntegerToString(ArraySize(openRecords)) +
               " Prev=" + IntegerToString(ArraySize(g_last_open_records))));
      if(verbose || g_first_poll)
         EmitAllRecords("OPEN", now, openRecords);
      else
         EmitNewOrChangedRecords("OPEN", now, openRecords, g_last_open_records);
      if(g_first_poll || openChanged) changed = true;
   }

   string historyRecords[];
   CollectRecentHistory(now, historyRecords);
   bool historyChanged = !RecordsEqual(historyRecords, g_last_history_records);
   if(g_first_poll || historyChanged || verbose)
   {
      string baselineFlag = g_first_poll ? "Y" : "N";
      EmitLine(TaggedRecord("HIST_CHANGE", now,
               "Count=" + IntegerToString(ArraySize(historyRecords)) +
               " Prev=" + IntegerToString(ArraySize(g_last_history_records)) +
               " Baseline=" + baselineFlag));

      if(verbose || (g_first_poll && EmitInitialHistoryDetails))
         EmitAllRecords("HIST", now, historyRecords);
      else if(!g_first_poll)
         EmitNewOrChangedRecords("HIST", now, historyRecords, g_last_history_records);

      if(g_first_poll || historyChanged) changed = true;
   }

   if(g_first_poll)
      EmitLine(TaggedRecord("BASELINE_END", now, "State=READY"));
   else if(changed)
      EmitLine(TaggedRecord("CHANGE_END", now, "State=CHANGED"));
   else if(verbose)
      EmitLine(TaggedRecord("POLL_END", now, "State=UNCHANGED"));

   g_last_environment = environment;
   CopyRecords(gvRecords, g_last_gv_records);
   CopyRecords(openRecords, g_last_open_records);
   CopyRecords(historyRecords, g_last_history_records);
   g_first_poll = false;
   return changed;
}

int OnInit()
{
   int seconds = SnapshotSeconds;
   if(seconds < 1) seconds = 1;

   EmitLine(TaggedRecord("START", TimeCurrent(),
            "StrategyID=" + IntegerToString(StrategyID) +
            " InstanceID=" + IntegerToString(InstanceID) +
            " MagicMin=" + IntegerToString(MinOwnedMagic()) +
            " MagicMax=" + IntegerToString(MaxOwnedMagic()) +
            " PollSeconds=" + IntegerToString(seconds) +
            " DebugLevel=" + IntegerToString(ObserverDebugLevel)));

   EventSetTimer(seconds);
   PollObservableState();
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   // Event-only mode is silent when environment/GV/open/history state is unchanged.
   PollObservableState();
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   EmitLine(TaggedRecord("STOP", TimeCurrent(),
            "Reason=" + IntegerToString(reason)));
}

void OnTick()
{
   // Intentionally empty. Observation is timer-polled but event-emitted.
}
