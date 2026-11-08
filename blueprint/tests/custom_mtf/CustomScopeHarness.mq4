#property strict
// Test the actual M27 dispatch loop; replace side effects below its routing boundary.
struct ScopePair {bool pair_enabled;bool is_processing;string actual_symbol;};
struct ScopeAmbiguity {bool Active;};
ScopePair g_pair_states[2];ScopeAmbiguity g_execution_ambiguity;
bool g_is_initialized=true,g_is_scanning=false,g_portfolio_emergency_close_requested=false,g_dashboard_needs_update=false;
bool g_pair_canonical_scope[2];int g_pair_count=2;datetime g_processing_time;int calls[2];
void ManagePortfolio(){}void ManagePositions(){}void CompactMonitoredTrades(){}void ReconcileExecutionAmbiguityHold(){}void UpdateDashboard(){}
datetime GetProcessingTime(){return TimeCurrent();}
bool IsNewCandle(string symbol,int index){return true;} // Both symbols have an eligible closed M15 event.
void ProcessPair(int index){calls[index]++;} // Counter only: no detector, risk or order call.
#include "CanonicalDispatchFixture.mqh"
int OnInit()
{
 int passed=0,failed=0;for(int i=0;i<2;i++){g_pair_states[i].pair_enabled=true;g_pair_states[i].is_processing=false;}
 g_pair_canonical_scope[0]=true;g_pair_canonical_scope[1]=false;ArrayInitialize(calls,0);OnTickMain();
 bool first=calls[0]==1 && calls[1]==0 && !g_is_scanning;if(first)passed++;else failed++;
 g_pair_canonical_scope[0]=false;ArrayInitialize(calls,0);OnTickMain();
 bool second=calls[0]==0 && calls[1]==0;if(second)passed++;else failed++;
 g_pair_canonical_scope[0]=true;g_pair_canonical_scope[1]=true;ArrayInitialize(calls,0);OnTickMain();
 bool third=calls[0]==1 && calls[1]==1;if(third)passed++;else failed++;
 Print("[SCOPE-ROUTING] custom_blocked=",first," all_custom_blocked=",second," canonical_preserved=",third);
 Print("[SCOPE-ROUTING-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
