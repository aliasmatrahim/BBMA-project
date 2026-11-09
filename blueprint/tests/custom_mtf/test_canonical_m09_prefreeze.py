"""Actual transaction body with explicit owner/stage I/O fixtures; not native MQL4."""
from pathlib import Path
import re
import subprocess

SOURCE = Path('blueprint/source/BBMA_EA.mq4')


def function(source, name):
    match = re.search(r'(?:bool|void) ' + name + r'\s*\(', source)
    assert match, name + ' missing'
    start = source.index('{', match.start())
    depth, end = 1, start + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[match.start():end]


def test_pre_freeze_transaction_with_stage_fault_fixtures(tmp_path):
    source = SOURCE.read_text()
    if 'bool UpdateCanonicalMHVSource(' in source:
        body = function(source, 'UpdateCanonicalMHVSource')
    else:
        # Baseline adapter changes only the name/signature, not its behavior.
        body = function(source, 'ObserveCanonicalMHVSource').replace(
            'ObserveCanonicalMHVSource(int pairIndex,int tf,datetime latest)',
            'UpdateCanonicalMHVSource(int pairIndex,int tf,datetime latest,bool beforeFreeze)')
    prelude = r'''
#include <string>
#include <iostream>
using string=std::string;using datetime=long long;
template<class T>void ZeroMemory(T &value){value=T();}
const int PERIOD_M15=15,DIR_BUY=1,DIR_SELL=2;
struct TimeframeData {int timeframe=60;double bollinger[3]={2,1.5,1};};
struct BollingerBand {double TOP_BB,MID_BB,LOW_BB,Width;};
struct ExtremeLifecycleData {int Timeframe=60,Direction=1,id=7;datetime LastUpdateCandleTime=36000;};
struct MLVData {datetime LastUpdateCandleTime=32400;int version=4;};
struct Progress {datetime lastClosed=0,contextOnlyThrough=0;bool recoveryRequired=false;string recoveryReason;};
struct CustomAuxLifecycle:Progress {ExtremeLifecycleData extremeBuy,extremeSell;MLVData mhvBuy,mhvSell;int reBuy=77,reSell=88;};
struct Pair {string actual_symbol="GBPUSD";bool is_processing=true;bool canonical_mhv_observed[3]={false,false,false};Progress custom_canonical[4];MLVData custom_higher_mhv_buy[3],custom_higher_mhv_sell[3];struct {datetime M15_CandleTime=38700;}tf_snapshot;};
Pair g_pair_states[2];int g_pair_count=2;bool g_pair_canonical_scope[2]={true,true};datetime g_processed_candle_time[2]={0,0};
CustomAuxLifecycle persisted[2];bool sourceReady=true,mutate=true;int updates=0,stores=0;
int CustomCanonicalTFIndex(int tf){return tf==60?2:-1;}
datetime GetLatestClosedCandleTime(string symbol,int tf){return tf==15?38700:36000;}
int GetTimeframeSeconds(int tf){return tf*60;}
int StringLen(string s){return s.size();}
bool IsCustomClosedSourceReady(TimeframeData &d,int tf,datetime latest){return sourceReady;}
bool LoadCustomCanonicalSource(int p,int tf,TimeframeData &d,CustomAuxLifecycle &o){o=persisted[p];Progress &r=g_pair_states[p].custom_canonical[2];o.recoveryRequired=r.recoveryRequired;o.recoveryReason=r.recoveryReason;return true;}
void StoreCustomCanonicalSource(int p,int tf,TimeframeData &d,CustomAuxLifecycle &o){stores++;persisted[p]=o;g_pair_states[p].custom_canonical[2]=o;g_pair_states[p].custom_higher_mhv_buy[2]=o.mhvBuy;g_pair_states[p].custom_higher_mhv_sell[2]=o.mhvSell;}
bool SameExtremeOwnerSnapshot(ExtremeLifecycleData &a,ExtremeLifecycleData &b){return a.id==b.id;}
void AdvanceMHVSourceOwners(string s,TimeframeData &d,BollingerBand &b,ExtremeLifecycleData &buy,ExtremeLifecycleData &sell,MLVData &mb,MLVData &ms,bool log){updates++;if(mutate){buy.id=19;sell.id=23;}mb.version++;ms.version++;}
void reset(){for(int p=0;p<2;p++){g_pair_states[p]=Pair();persisted[p]=CustomAuxLifecycle();persisted[p].extremeSell.Direction=DIR_SELL;g_processed_candle_time[p]=0;}sourceReady=true;mutate=true;updates=0;stores=0;}
int checks=0;bool check(bool ok,const char* label){checks++;if(!ok)std::cerr<<label<<" failed\n";return ok;}
'''
    cases = r'''
int main(){
 reset();
 if(!check(UpdateCanonicalMHVSource(0,60,36000,true),"pre-freeze runs before completed-cycle stamp"))return 1;
 if(!check(persisted[0].extremeBuy.id==19 && persisted[0].extremeSell.id==23 && persisted[0].mhvBuy.version==5 && persisted[0].mhvSell.version==5,"both parent/child directions commit"))return 1;
 if(!check(persisted[0].reBuy==77 && persisted[0].reSell==88 && g_processed_candle_time[0]==0,"RE and processing clock unchanged"))return 1;
 if(!check(persisted[1].extremeBuy.id==7 && persisted[1].mhvBuy.version==4,"symbol isolation"))return 1;
 if(!check(UpdateCanonicalMHVSource(0,60,36000,true) && updates==1 && stores==1,"duplicate does not advance twice"))return 1;
 g_processed_candle_time[0]=38700;
 if(!check(UpdateCanonicalMHVSource(0,60,36000,false) && updates==1,"post-cycle reuses pre-freeze result"))return 1;
 reset();g_pair_states[0].is_processing=false;
 if(!check(!UpdateCanonicalMHVSource(0,60,36000,true) && updates==0,"inactive processing phase rejected"))return 1;
 reset();g_pair_states[0].tf_snapshot.M15_CandleTime=37800;
 if(!check(!UpdateCanonicalMHVSource(0,60,36000,true) && updates==0,"stale M15 snapshot rejected"))return 1;
 reset();g_processed_candle_time[0]=38700;
 if(!check(UpdateCanonicalMHVSource(0,60,36000,false) && stores==0 && persisted[0].extremeBuy.id==7 && g_pair_states[0].custom_canonical[2].recoveryReason=="WAIT_CANONICAL_M09_PARENT_HANDOVER","post-cycle parent mutation discarded"))return 1;
 reset();persisted[0].lastClosed=28800;
 if(!check(UpdateCanonicalMHVSource(0,60,36000,true) && updates==0 && stores==0 && g_pair_states[0].custom_canonical[2].recoveryRequired,"non-contiguous source stays HOLD"))return 1;
 reset();persisted[0].mhvBuy.LastUpdateCandleTime=39600;
 if(!check(UpdateCanonicalMHVSource(0,60,36000,true) && updates==0 && stores==0,"future owner anchor stays HOLD"))return 1;
 reset();sourceReady=false;
 if(!check(!UpdateCanonicalMHVSource(0,60,36000,true) && updates==0,"unready source not consumed"))return 1;
 std::cout<<"CANONICAL_M09_TRANSACTION checks="<<checks<<" PASS\n";
}
'''
    path = tmp_path / 'transaction.cpp'
    path.write_text(prelude + body + cases)
    subprocess.run(['g++', '-std=c++17', str(path), '-o', str(tmp_path / 'transaction')], check=True)
    result = subprocess.run([str(tmp_path / 'transaction')], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'checks=12 PASS' in result.stdout


def test_pre_freeze_calls_precede_persistent_exports():
    body = function(SOURCE.read_text(), 'ProcessPair')
    export = body.index('Signal resolvedH1BuyExtreme')
    m08_end = body.index('ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_h4')
    for tf in ('D1', 'H4', 'H1'):
        call = f'AdvanceCanonicalMHVBeforeFreeze(pairIndex,PERIOD_{tf},'
        assert body.count(call) == 1, tf + ' requires one canonical pre-freeze producer'
        assert m08_end < body.index(call) < export
