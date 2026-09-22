//+------------------------------------------------------------------+
//| Q10_DEMO_IDENTITY_PROBE.mq4                                      |
//| Read-only demo/account-classification probe for Issue #109.       |
//| No trading functions. No account number or credentials logged.    |
//+------------------------------------------------------------------+
#property strict

int OnInit()
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
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   Print("[Q10-DEMO-ID]|DeinitReason=", IntegerToString(reason));
}

void OnTick()
{
   // Read-only by design.
}
//+------------------------------------------------------------------+
