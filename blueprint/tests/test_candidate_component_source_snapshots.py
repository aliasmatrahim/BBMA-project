"""Exact-source regression for M15/M16 component source freshness.

The portable C++ probe extracts the production admission helpers and M16 owner
validator. It stops before execution APIs; no broker call or live trading runs.
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


def portable_source(source):
    prelude = r'''
#include <iostream>
#include <string>
using string=std::string; using datetime=long long;
using ENUM_DIRECTION=int; using ENUM_SIGNAL_TYPE=int;
enum {DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};
enum {PERIOD_M15=15,PERIOD_H1=60,PERIOD_H4=240,PERIOD_D1=1440};
enum {SIGNAL_NONE=0,SIGNAL_EXTREME=1,SIGNAL_MLV=2,SIGNAL_RE_ENTRY=3,SIGNAL_REM=4,SIGNAL_REE=5};
enum {H4_OWNER_NONE=0,H4_OWNER_ACTIVE=1};
enum {D1_AUTH_NONE=0,D1_AUTH_STRATEGIC_OWNER=1,D1_AUTH_OPPORTUNITY=2};
enum {D1_OPP_NONE=0,D1_OPP_EXTREME_TPW=1};
struct TimeframeData {int timeframe=0;bool is_valid=false,is_closed=false;datetime candle_time=0;};
struct TimeframeSnapshot {datetime D1_CandleTime=0,H4_CandleTime=0,H1_CandleTime=0,M15_CandleTime=0;bool D1_IsClosed=false,H4_IsClosed=false,H1_IsClosed=false,M15_IsClosed=false;};
struct H4DirectionalOwner {int State=0,Direction=0;bool RecoveryComplete=false,IsValid=false;};
struct ComponentIdentity {int ComponentType=0,Direction=0,Timeframe=0;datetime CandleTime=0;};
struct ValidatedSequenceCandidate {int SequenceType=0,Direction=0,ComponentCount=0;ComponentIdentity Components[3];bool UsesD1Opportunity=false;int D1OpportunityFamily=0;};
struct BBMA_Decision {int ComponentCount=0,SignalType=0,Direction=0,D1AuthorityMode=0,D1OpportunityFamily=0;ComponentIdentity Components[3];};
struct PairState {TimeframeData d1_data,h4_data,h1_data,m15_data;TimeframeSnapshot tf_snapshot;H4DirectionalOwner h4_direction_owner;};
PairState g_pair_states[1]; int g_pair_count=1;
bool IsDecisionComponentOwnerValid(PairState&,ComponentIdentity&,bool& expired){expired=false;return true;}
'''
    helpers = "\n".join(
        source_block(source, signature)
        for signature in (
            "bool IsCurrentClosedSourceSnapshot(",
            "bool IsCandidateSourceSnapshotReady(",
            "bool IsDecisionSourceSnapshotReady(",
            "bool ValidateDecisionOwnerSnapshot(",
        )
    )
    driver = r'''
void set_source(PairState &s,int timeframe,datetime stamp,bool valid=true) {
   TimeframeData *data=nullptr; datetime *snap=nullptr; bool *closed=nullptr;
   if(timeframe==PERIOD_D1){data=&s.d1_data;snap=&s.tf_snapshot.D1_CandleTime;closed=&s.tf_snapshot.D1_IsClosed;}
   if(timeframe==PERIOD_H4){data=&s.h4_data;snap=&s.tf_snapshot.H4_CandleTime;closed=&s.tf_snapshot.H4_IsClosed;}
   if(timeframe==PERIOD_H1){data=&s.h1_data;snap=&s.tf_snapshot.H1_CandleTime;closed=&s.tf_snapshot.H1_IsClosed;}
   if(timeframe==PERIOD_M15){data=&s.m15_data;snap=&s.tf_snapshot.M15_CandleTime;closed=&s.tf_snapshot.M15_IsClosed;}
   data->timeframe=timeframe;data->is_valid=valid;data->is_closed=valid;data->candle_time=valid?stamp:0;
   *snap=stamp;*closed=true;
}
bool run(const std::string &scenario,int &m15,int &m16) {
   PairState &s=g_pair_states[0];
   set_source(s,PERIOD_D1,100);set_source(s,PERIOD_H4,200);set_source(s,PERIOD_H1,300);set_source(s,PERIOD_M15,400);
   s.h4_direction_owner={H4_OWNER_ACTIVE,DIR_BUY,true,true};
   ValidatedSequenceCandidate c{};c.Direction=DIR_BUY;
   if(scenario=="stale_h1_extreme") {
      c.SequenceType=SIGNAL_EXTREME;c.ComponentCount=1;
      c.Components[0]={SIGNAL_EXTREME,DIR_BUY,PERIOD_H1,280};
      set_source(s,PERIOD_H1,300,false);
   } else if(scenario=="stale_m15_mlv") {
      c.SequenceType=SIGNAL_REM;c.ComponentCount=3;
      c.Components[0]={SIGNAL_RE_ENTRY,DIR_BUY,PERIOD_H4,190};
      c.Components[1]={SIGNAL_EXTREME,DIR_BUY,PERIOD_H1,280};
      c.Components[2]={SIGNAL_MLV,DIR_BUY,PERIOD_M15,380};
      set_source(s,PERIOD_M15,400,false);
   } else if(scenario=="stale_h4_extreme") {
      c.SequenceType=SIGNAL_REE;c.ComponentCount=3;
      c.Components[0]={SIGNAL_RE_ENTRY,DIR_BUY,PERIOD_D1,90};
      c.Components[1]={SIGNAL_EXTREME,DIR_BUY,PERIOD_H4,180};
      c.Components[2]={SIGNAL_EXTREME,DIR_BUY,PERIOD_H1,280};
      set_source(s,PERIOD_H4,200,false);
   } else {
      c.SequenceType=SIGNAL_REM;c.ComponentCount=3;
      c.Components[0]={SIGNAL_RE_ENTRY,DIR_BUY,PERIOD_H4,190};
      c.Components[1]={SIGNAL_EXTREME,DIR_BUY,PERIOD_H1,280};
      c.Components[2]={SIGNAL_MLV,DIR_BUY,PERIOD_M15,380};
   }

   m15=IsCandidateSourceSnapshotReady(c,s);
   BBMA_Decision d{};d.ComponentCount=c.ComponentCount;d.Direction=c.Direction;
   d.SignalType=c.SequenceType;d.D1AuthorityMode=D1_AUTH_STRATEGIC_OWNER;
   for(int i=0;i<c.ComponentCount;i++)d.Components[i]=c.Components[i];
   bool expired=false;
   m16=ValidateDecisionOwnerSnapshot(0,d,expired);
   return m15 && m16;
}
int main(int argc,char **argv) {
   std::string scenario=argv[1];int m15=0,m16=0;
   bool preflight=run(scenario,m15,m16);
   std::cout<<"m15="<<m15<<" m16="<<m16<<" preflight="<<preflight<<"\n";
}
''' 
    return prelude + helpers + "\n" + driver


class TestAllComponentSnapshots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which("g++")
        if not compiler:
            raise RuntimeError("g++ required; do not simulate a PASS")
        cls.tempdir = tempfile.TemporaryDirectory(prefix="bbma-component-snapshot-")
        cls.executable = Path(cls.tempdir.name) / "probe"
        cpp = Path(cls.tempdir.name) / "probe.cpp"
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

    def test_unreadable_component_source_blocks_m15_m16_and_preflight(self):
        for scenario in ("stale_h1_extreme", "stale_m15_mlv", "stale_h4_extreme"):
            with self.subTest(scenario=scenario):
                result = self.run_probe(scenario)
                self.assertEqual(result["m15"], 0, f"{scenario}: M15 admitted stale component")
                self.assertEqual(result["m16"], 0, f"{scenario}: M16 admitted stale component")
                self.assertEqual(result["preflight"], 0,
                                 f"{scenario}: stale component reached preflight")

    def test_all_current_component_sources_pass_control(self):
        result = self.run_probe("valid")
        self.assertEqual(result, {"m15": 1, "m16": 1, "preflight": 1})

