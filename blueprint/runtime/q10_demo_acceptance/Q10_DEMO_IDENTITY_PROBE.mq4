//+------------------------------------------------------------------+
//| Q10_DEMO_IDENTITY_PROBE.mq4                                      |
//| Read-only demo/account-classification probe for Issue #109.       |
//| No trading functions. No account number or credentials logged.    |
//+------------------------------------------------------------------+
#property strict

bool g_connected_identity_emitted = false;

void EmitIdentity()
{
   string demo = IsDemo() ? "Y" : "N";
   string connected = IsConnected() ? "Y" : "N";
   string tradeAllowed = IsTradeAllowed() ? "Y" : "N";
   string server = AccountServer();
   string company = AccountCompany();
   int build = (int)TerminalInfoInteger(TERMINAL_BUILD);

   Print("[Q10-DEMO-ID]|Demo=", demo,
         "|Connected=", connected,
         "|TradeAllowed=", tradeAllowed,
         "|Server=", server,
         "|Company=", company,
         "|TerminalBuild=", IntegerToString(build));
}

int OnInit()
{
   EventSetTimer(2);
   EmitIdentity();
   if(IsConnected())
   {
      g_connected_identity_emitted = true;
      EventKillTimer();
   }
   return(INIT_SUCCEEDED);
}

void OnTimer()
{
   if(!g_connected_identity_emitted && IsConnected())
   {
      EmitIdentity();
      g_connected_identity_emitted = true;
      EventKillTimer();
   }
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   Print("[Q10-DEMO-ID]|DeinitReason=", IntegerToString(reason));
}

void OnTick()
{
   // Read-only by design.
}
//+------------------------------------------------------------------+
