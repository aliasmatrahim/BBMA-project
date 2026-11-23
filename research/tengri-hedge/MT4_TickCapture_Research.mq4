#property strict
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_color1 clrNONE
#property description "Demo-only HFM MT4 Bid/Ask tick logger. Contains no trade functions."

input string ExpectedServer = "HFMarketsSV-Demo Server";
input string ExpectedSymbolPrefix = "EURUSD";
input string OutputFolder = "MT4RawTicks";

double HiddenBuffer[];
int fileHandle = INVALID_HANDLE;
string activeFile = "";
bool readyToCapture = false;

bool IsExpectedSymbol(const string actual, const string expectedPrefix)
{
   string a = actual;
   string e = expectedPrefix;
   StringToUpper(a);
   StringToUpper(e);
   return StringFind(a, e, 0) == 0;
}

string UtcIso(const datetime value)
{
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02dZ",
                       TimeYear(value), TimeMonth(value), TimeDay(value),
                       TimeHour(value), TimeMinute(value), TimeSeconds(value));
}

string ServerDayKey(const datetime value)
{
   return StringFormat("%04d%02d%02d", TimeYear(value), TimeMonth(value), TimeDay(value));
}

bool OpenDailyFile(const datetime serverTime)
{
   string fileName = OutputFolder + "\\" + Symbol() + "_" + ServerDayKey(serverTime) + ".csv";
   if(fileName == activeFile && fileHandle != INVALID_HANDLE)
      return true;

   if(fileHandle != INVALID_HANDLE)
      FileClose(fileHandle);
   activeFile = fileName;

   fileHandle = FileOpen(fileName, FILE_CSV | FILE_READ | FILE_WRITE | FILE_SHARE_READ | FILE_SHARE_WRITE, ',');
   if(fileHandle == INVALID_HANDLE)
   {
      Print("MT4TickCapture: FileOpen failed, error=", GetLastError(), " file=", fileName);
      return false;
   }

   if(FileSize(fileHandle) == 0)
   {
      FileWrite(fileHandle, "timestamp_utc", "server_time", "server_utc_offset_seconds",
                "bid", "ask", "symbol", "server", "company", "platform",
                "terminal_build", "is_demo");
   }
   FileSeek(fileHandle, 0, SEEK_END);
   return true;
}

int OnInit()
{
   SetIndexBuffer(0, HiddenBuffer);
   SetIndexStyle(0, DRAW_NONE);
   ArraySetAsSeries(HiddenBuffer, true);

   if(IsTesting())
   {
      Print("MT4TickCapture: refuses Strategy Tester; capture must come from a connected terminal.");
      return INIT_FAILED;
   }
   if(!IsDemo())
   {
      Print("MT4TickCapture: refuses non-demo accounts.");
      return INIT_FAILED;
   }
   if(AccountServer() != ExpectedServer)
   {
      Print("MT4TickCapture: wrong server. Expected '", ExpectedServer, "', got '", AccountServer(), "'.");
      return INIT_FAILED;
   }
   if(!IsExpectedSymbol(Symbol(), ExpectedSymbolPrefix))
   {
      Print("MT4TickCapture: wrong symbol. Expected prefix '", ExpectedSymbolPrefix, "', got '", Symbol(), "'.");
      return INIT_FAILED;
   }
   FolderCreate(OutputFolder);
   readyToCapture = true;
   Print("MT4TickCapture: ready; demo-only quote logging for ", Symbol(), " on ", AccountServer(), ".");
   return INIT_SUCCEEDED;
}

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   if(!readyToCapture || rates_total < 1 || !IsDemo() || AccountServer() != ExpectedServer)
      return rates_total;

   datetime serverTime = TimeCurrent();
   datetime utcNow = TimeGMT();
   int offsetSeconds = (int)MathRound((double)(serverTime - utcNow) / 1800.0) * 1800;
   if(offsetSeconds != 7200 && offsetSeconds != 10800)
   {
      Print("MT4TickCapture: quote skipped; unexpected HFM UTC offset ", offsetSeconds,
            " seconds. Check the PC clock and server identity.");
      return rates_total;
   }

   double bid = MarketInfo(Symbol(), MODE_BID);
   double ask = MarketInfo(Symbol(), MODE_ASK);
   if(bid <= 0 || ask < bid)
      return rates_total;

   if(!OpenDailyFile(serverTime))
      return rates_total;

   datetime utcStamp = serverTime - offsetSeconds;
   FileWrite(fileHandle,
             UtcIso(utcStamp),
             TimeToString(serverTime, TIME_DATE | TIME_SECONDS),
             offsetSeconds,
             DoubleToString(bid, Digits),
             DoubleToString(ask, Digits),
             Symbol(),
             AccountServer(),
             AccountCompany(),
             "MT4",
             (int)TerminalInfoInteger(TERMINAL_BUILD),
             "true");
   FileFlush(fileHandle);
   return rates_total;
}

void OnDeinit(const int reason)
{
   readyToCapture = false;
   if(fileHandle != INVALID_HANDLE)
   {
      FileFlush(fileHandle);
      FileClose(fileHandle);
      fileHandle = INVALID_HANDLE;
   }
}
