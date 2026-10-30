"""Exact-source M12 -> M15 -> M16 stale-refresh regression probe.

This portable C++ probe executes the production function bodies with terminal,
market-data and logging stubs. Its preflight stub records entry only; no broker
API, OrderSend, or live trading function is called.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "blueprint/source/BBMA_EA.mq4"


def source_block(source, signature):
    start = source.index(signature)
    brace = source.index("{", start)
    depth = 0
    for end in range(brace, len(source)):
        depth += (source[end] == "{") - (source[end] == "}")
        if depth == 0:
            return source[start:end + 1]
    raise AssertionError(signature)


def optional_block(source, signature):
    return source_block(source, signature) if signature in source else ""


def portable_source(source):
    prelude = r'''
#include <iostream>
#include <string>
using string=std::string; using datetime=long long;
using ENUM_DIRECTION=int; using ENUM_RE_STATE=int; using ENUM_SIGNAL_TYPE=int;
enum {DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};
enum {PERIOD_M15=15,PERIOD_H1=60,PERIOD_H4=240,PERIOD_D1=1440};
enum {RE_STATE_NONE=0,RE_STATE_CANDIDATE=1,RE_STATE_CONFIRMED=2,RE_STATE_EXPIRED=3};
enum {RE_TYPE_1=1,RE_TYPE_2=2,RE_TYPE_3_CSM=3,RE_TYPE_4_CSD=4};
enum {TYPE1_CTX_NONE=0,TYPE1_CTX_DIRECTION_OWNER=1};
enum {SIGNAL_NONE=0,SIGNAL_RE_ENTRY=1,SIGNAL_CSM=2,SIGNAL_CSD=3,SIGNAL_ECSD=4,SIGNAL_MLV=5,SIGNAL_EXTREME=6,SIGNAL_REM=7,SIGNAL_RRE=8,SIGNAL_REE=9};
enum {H4_OWNER_NONE=0,H4_OWNER_ACTIVE=1};
enum {D1_OWNER_UNRESOLVED=0,D1_OWNER_BUY_CONFIRMED=1,D1_OWNER_SELL_CONFIRMED=2};
enum {D1_AUTH_NONE=0,D1_AUTH_STRATEGIC_OWNER=1,D1_AUTH_OPPORTUNITY=2};
enum {D1_OPP_EXTREME_TPW=1};
enum {TIER_NONE=0};
enum {DEC_CREATED=0,DEC_VALIDATED=1,DEC_INVALIDATED=2,DEC_EXPIRED=3};
enum {REJ_NONE=0,REJ_OPPOSITE_SIGNAL=1,REJ_SEQUENCE_BREAK=2,REJ_EXPIRED=3};
enum {CONFLICT_DIRECTION_VIOLATION=1,DBG_SIGNAL=2};
int EntryMode=1,DebugLevel=0,g_processing_time=5000,g_pair_count=1;
bool EnableRE_Type1=true;
int preflightCalls=0;
#define Print(...)
template<class T> void ZeroMemory(T &x){x=T{};}
string EnumToString(int){return "";}
string TimeToString(datetime){return "";}
string IntegerToString(int x){return std::to_string(x);}
string SHORT_HASH(string,int){return "HASH";}
void ObserverPrintChanged(string,string){}
struct TimeframeData {bool is_valid=false,is_closed=false;int timeframe=0,barIndex=0;datetime candle_time=0;double close=0;};
struct TimeframeSnapshot {datetime D1_CandleTime=0,H4_CandleTime=0,H1_CandleTime=0,M15_CandleTime=0;bool D1_IsClosed=false,H4_IsClosed=false,H1_IsClosed=false,M15_IsClosed=false;};
struct ReEntryData {int State=0,Direction=0,Timeframe=0,Type=0,Type1ContextState=0,LastUpdateBar=0,QualifyingCandles=0,MinCandlesRequired=0;bool IsValid=false;datetime LastUpdateCandleTime=0,ConfirmationCandle=0;double Type1PreviousClose=0,EntryPrice=0,MA5_Level=0,MA10_Level=0,MA50_Level=0,MID_BB=0;string Reason="";};
struct H4DirectionalOwner {int State=0,Direction=0;bool RecoveryComplete=false,IsValid=false;datetime LastProcessedH4CandleTime=0;string Reason="";};
struct ComponentIdentity {int ComponentType=0,Direction=0,Timeframe=0;datetime CandleTime=0;};
struct ValidatedSequenceCandidate {bool Valid=false,UsesD1Opportunity=false;int Direction=0,SequenceType=0,ComponentCount=0,PriorityTier=0,RequirementCompleteness=0,SequenceCompleteness=0,PatternStrength=0,SLTPSource=0;ComponentIdentity Components[3];datetime Expiry=0,SequenceStartTime=0;string SequenceHash="";int D1OpportunityFamily=0,D1OpportunityDirection=0,D1OpportunitySourceSignal=0;datetime D1OpportunitySourceCandleTime=0,D1OpportunityActivationTime=0;string D1OpportunityCycleID="";};
struct D1MajorTrendOwner {int State=0,Direction=0;bool IsValid=false;datetime SourceCandleTime=0;double Close1=0,MA50_1=0,MA50_2=0;};
struct PairState {string actual_symbol="TEST";ReEntryData re_h1_buy_state,re_h1_sell_state,re_h4_buy_state,re_h4_sell_state,re_d1_buy_state,re_d1_sell_state,re_m15_buy_state,re_m15_sell_state;H4DirectionalOwner h4_direction_owner;D1MajorTrendOwner d1_major_trend_owner;TimeframeData h1_data,h4_data,d1_data,m15_data;TimeframeSnapshot tf_snapshot;};
struct BBMA_Decision {bool Valid=false,SequenceValid=false,PatternValid=false,HasSLTPSourceComponent=false,D1OwnerSnapshotValid=false,D1OpportunitySnapshotValid=false;int Direction=0,SignalType=0,PriorityTier=0,ComponentCount=0,SLTPSource=0,DecisionState=0,RejectionReason=0,D1OwnerState=0,D1OwnerDirection=0,D1AuthorityMode=0,D1OpportunityFamily=0,D1OpportunityDirection=0,D1OpportunitySourceSignal=0;ComponentIdentity Components[3],SLTPSourceComponent;datetime CandidateExpiry=0,CandleTime=0,CycleStartTime=0,D1OwnerCandleTime=0,D1OpportunitySourceCandleTime=0,D1OpportunityActivationTime=0;double D1OwnerClose=0,D1OwnerMA50Current=0,D1OwnerMA50Previous=0;string SequenceHash="",DecisionID="",Pair="",D1OpportunityCycleID="";};
struct OppositeConflictPackage {bool Exists=false,BreaksSequence=false;int ConflictType=0;string ConflictReason="";datetime FrozenSnapshotTime=0;};
PairState g_pair_states[1];
template<class... A> void ResetReEntryState(A&&...){}
template<class... A> int DetectReEntryDirectionOwnerSignal(A&&...){return SIGNAL_NONE;}
template<class... A> bool IsReEntryMAClusterCloseSideFailure(A&&...){return false;}
template<class... A> bool TryStartSpecificReEntry(A&&...){return false;}
template<class... A> void ResetType1AndAdoptCurrentOwner(A&&...){}
template<class... A> void AdoptType1DirectionOwner(A&&...){}
template<class... A> bool IsType1StructuralRetraceEvidence(A&&...){return false;}
template<class... A> void BeginType1RangingCandidate(A&&...){}
template<class... A> bool HasReEntryMAClusterTouch(A&&...){return false;}
template<class... A> void ConfirmReEntryState(A&&...){}
template<class... A> void SetReEntrySnapshotLevels(A&&...){}
bool DetectReEntry_Type2(string,ENUM_DIRECTION,TimeframeData&,bool &b){b=false;return false;}
template<class... A> bool HasReEntryMA5OrMA50Touch(A&&...){return false;}
template<class... A> void ResetH4DirectionalOwner(A&&...){}
template<class... A> int ClassifyH4AuthoritativeSignal(A&&...){return SIGNAL_NONE;}
template<class... A> void ApplyH4AuthoritativeEvent(A&&...){}
template<class... A> void SaveH4OwnerCheckpoint(A&&...){}
template<class... A> void ClearH4OwnerCheckpoint(A&&...){}
template<class... A> bool IsD1OpportunityCandidateAuthorityReady(A&&...){return false;}
template<class... A> bool IsPersistentMLVComponentValid(A&&...){return false;}
template<class... A> bool IsPersistentExtremeComponentValid(A&&...){return false;}
template<class... A> bool ValidateDecisionD1OpportunitySnapshot(A&&...){return false;}
bool ResolveSelectedSLTPSourceComponent(ValidatedSequenceCandidate&,ComponentIdentity&){return false;}
datetime GetCandidateAnchorTime(ValidatedSequenceCandidate& c){return c.Components[0].CandleTime;}
string GenerateDecisionID(string,datetime,int,int,string){return "DECISION";}
int CompareCanonicalCandidates(ValidatedSequenceCandidate&,ValidatedSequenceCandidate&){return 0;}
bool FreezeD1OpportunitySnapshot(PairState&,ValidatedSequenceCandidate&,BBMA_Decision&){return false;}
string D1AuthorityModeText(int){return "";}
string D1OpportunityFamilyText(int){return "";}
'''
    helpers = "\n".join(
        optional_block(source, signature)
        for signature in (
            "bool IsCurrentClosedSourceSnapshot(",
            "bool IsCandidateSourceSnapshotReady(",
            "bool IsDecisionSourceSnapshotReady(",
        )
    )
    functions = [
        source_block(source, "ENUM_RE_STATE UpdateReEntryState("),
        source_block(source, "void UpdateRuntimeH4DirectionalOwner("),
        source_block(source, "void BuildConfirmedReEntryCandidate("),
        source_block(source, "bool IsEntryModeCandidateAllowed("),
        source_block(source, "bool IsCandidateEligible("),
        source_block(source, "bool IsD1MajorTrendOwnerExecutionReady("),
        source_block(source, "bool IsCandidateAllowedByD1Owner("),
        source_block(source, "bool FreezeD1OwnerSnapshot("),
        source_block(source, "void PriorityEngine_Atomic(").replace(
            "ValidatedSequenceCandidate &candidates[]",
            "ValidatedSequenceCandidate *candidates",
        ),
        source_block(source, "bool IsPersistentReEntryComponentValid("),
        source_block(source, "bool IsDecisionComponentOwnerValid("),
        source_block(source, "bool ValidateDecisionD1OwnerSnapshot("),
        source_block(source, "bool ValidateDecisionD1AuthoritySnapshot("),
        source_block(source, "bool ValidateDecisionOwnerSnapshot("),
        source_block(source, "void InvalidationEngine_Atomic("),
    ]
    module = helpers + "\n" + "\n".join(functions)
    driver = r'''
bool RunEntryPreflightAndExecute(BBMA_Decision&,string){preflightCalls++;return true;}
int main(int argc,char** argv){
 string scenario=argv[1];
 PairState &s=g_pair_states[0];
 s.d1_major_trend_owner.State=D1_OWNER_BUY_CONFIRMED;
 s.d1_major_trend_owner.Direction=DIR_BUY;
 s.d1_major_trend_owner.IsValid=true;
 s.d1_major_trend_owner.SourceCandleTime=4000;
 s.d1_major_trend_owner.Close1=1.2;
 s.d1_major_trend_owner.MA50_1=1.1;
 s.d1_major_trend_owner.MA50_2=1.0;
 s.h4_direction_owner.State=H4_OWNER_ACTIVE;
 s.h4_direction_owner.Direction=DIR_BUY;
 s.h4_direction_owner.IsValid=true;
 s.h4_direction_owner.RecoveryComplete=true;
 s.h4_direction_owner.LastProcessedH4CandleTime=1800;
 s.re_h1_buy_state.State=RE_STATE_CONFIRMED;
 s.re_h1_buy_state.IsValid=true;
 s.re_h1_buy_state.Direction=DIR_BUY;
 s.re_h1_buy_state.Timeframe=PERIOD_H1;
 s.re_h1_buy_state.Type=RE_TYPE_1;
 s.re_h1_buy_state.ConfirmationCandle=1200;
 s.re_h1_buy_state.EntryPrice=1.25;
 s.tf_snapshot.H1_CandleTime=2400;s.tf_snapshot.H1_IsClosed=true;
 s.tf_snapshot.H4_CandleTime=1800;s.tf_snapshot.H4_IsClosed=true;
 s.h1_data.timeframe=PERIOD_H1;s.h1_data.is_valid=true;s.h1_data.is_closed=true;s.h1_data.candle_time=2400;s.h1_data.barIndex=1;
 s.h4_data.timeframe=PERIOD_H4;s.h4_data.is_valid=true;s.h4_data.is_closed=true;s.h4_data.candle_time=1800;s.h4_data.barIndex=1;
 if(scenario=="invalid_h1"){s.h1_data.is_valid=false;s.h1_data.is_closed=false;s.h1_data.candle_time=0;}
 if(scenario=="invalid_h4"){s.h4_data.is_valid=false;s.h4_data.is_closed=false;s.h4_data.candle_time=0;}
 auto originalRE=s.re_h1_buy_state;
 auto originalH4=s.h4_direction_owner;
 UpdateReEntryState(s.re_h1_buy_state,"TEST",DIR_BUY,s.h1_data);
 UpdateRuntimeH4DirectionalOwner(0);
 bool retained=(s.re_h1_buy_state.State==originalRE.State&&s.re_h1_buy_state.ConfirmationCandle==originalRE.ConfirmationCandle);
 bool h4retained=(s.h4_direction_owner.State==originalH4.State&&s.h4_direction_owner.Direction==originalH4.Direction);
 ValidatedSequenceCandidate candidate{};
 BuildConfirmedReEntryCandidate(s.re_h1_buy_state,s.h4_direction_owner,candidate);
 BBMA_Decision decision{};OppositeConflictPackage conflict{};
 if(candidate.Valid){ValidatedSequenceCandidate candidates[1]={candidate};PriorityEngine_Atomic(candidates,1,s,decision,conflict);}
 if(decision.Valid&&decision.DecisionState==DEC_CREATED)InvalidationEngine_Atomic(0,decision,conflict);
 if(decision.DecisionState==DEC_VALIDATED)RunEntryPreflightAndExecute(decision,"TEST");
 int forcedM16=-1;
 if(scenario!="valid"){
   BBMA_Decision forced{};forced.Valid=true;forced.Pair="TEST";forced.Direction=DIR_BUY;
   forced.SignalType=SIGNAL_RE_ENTRY;forced.ComponentCount=1;forced.DecisionState=DEC_CREATED;
   forced.Components[0].ComponentType=SIGNAL_RE_ENTRY;forced.Components[0].Direction=DIR_BUY;
   forced.Components[0].Timeframe=PERIOD_H1;forced.Components[0].CandleTime=1200;
   FreezeD1OwnerSnapshot(s,forced);
   InvalidationEngine_Atomic(0,forced,conflict);
   forcedM16=(forced.DecisionState==DEC_VALIDATED);
 }
 std::cout<<"retained="<<retained<<" h4_retained="<<h4retained
          <<" candidate="<<candidate.Valid<<" m15="<<decision.Valid
          <<" m16="<<(decision.DecisionState==DEC_VALIDATED)
          <<" preflight="<<preflightCalls<<" forced_m16="<<forcedM16<<"\n";
}
'''
    return prelude + module + driver


class TestM12StaleOwnerRefresh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which("g++")
        if not compiler:
            raise RuntimeError("g++ required; do not simulate a PASS")
        cls.tempdir = tempfile.TemporaryDirectory(prefix="m12-stale-owner-refresh-")
        directory = Path(cls.tempdir.name)
        cls.executable = directory / "probe"
        cpp = directory / "probe.cpp"
        cpp.write_text(portable_source(SOURCE.read_text()))
        subprocess.run(
            [compiler, "-std=c++17", "-Wall", "-Wextra", "-Wno-unused-parameter",
             str(cpp), "-o", str(cls.executable)],
            check=True, capture_output=True, text=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def run_probe(self, scenario):
        fields = subprocess.check_output([str(self.executable), scenario], text=True).split()
        return {key: int(value) for key, value in (field.split("=") for field in fields)}

    def test_unreadable_refresh_cannot_reach_m15_m16_or_preflight(self):
        for scenario in ("invalid_h1", "invalid_h4"):
            with self.subTest(scenario=scenario):
                result = self.run_probe(scenario)
                self.assertEqual(result["retained"], 1,
                                 "M12 structural owner must persist; do not add age expiry")
                self.assertEqual(result["h4_retained"], 1,
                                 "H4 owner must not be destructively erased")
                self.assertEqual(result["candidate"], 1,
                                 "fixture must exercise the retained confirmed owner")
                self.assertEqual(result["m15"], 0,
                                 f"{scenario}: M15 admitted without readable current data")
                self.assertEqual(result["m16"], 0)
                self.assertEqual(result["preflight"], 0)

    def test_m16_rejects_a_precreated_decision_after_unreadable_refresh(self):
        for scenario in ("invalid_h1", "invalid_h4"):
            with self.subTest(scenario=scenario):
                result = self.run_probe(scenario)
                self.assertEqual(
                    result["forced_m16"], 0,
                    f"{scenario}: M16 accepted exact owner identity without current data",
                )

    def test_valid_closed_h1_h4_control_still_reaches_preflight(self):
        result = self.run_probe("valid")
        self.assertEqual(result["candidate"], 1)
        self.assertEqual(result["m15"], 1)
        self.assertEqual(result["m16"], 1)
        self.assertEqual(result["preflight"], 1)

    def test_preflight_chain_has_m17_risk_and_portfolio_gates_without_direct_send(self):
        source = SOURCE.read_text()
        process_pair = source_block(source, "void ProcessPair(")
        self.assertIn("if(decision.DecisionState == DEC_VALIDATED)", process_pair)
        self.assertIn("RunEntryPreflightAndExecute(decision, actual)", process_pair)
        preflight = source_block(source, "bool RunEntryPreflightAndExecute(")
        ordered = [
            "ResolveExecutionReferencePrice(",
            "ResolveApprovedInitialSLTP(",
            "ValidateSLTP(",
            "CheckRiskBeforeTrade(",
            "FinalPortfolioGuard(",
            "ProcessEntry(",
        ]
        positions = [preflight.index(token) for token in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("OrderSend(", preflight)


if __name__ == "__main__":
    unittest.main()
