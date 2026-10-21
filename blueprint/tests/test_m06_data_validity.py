"""Execute exact M06 source bodies with deterministic market-data API fixtures.

This is a portable C++ behavioral probe, not native MT4/runtime evidence.
Only terminal APIs are substituted; no indicator/data-engine logic is copied.
Mutation caught: accepting a partial BB20 window or marking unavailable inputs valid.
"""
import math
from pathlib import Path
import shutil
import statistics
import subprocess

import pytest

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
#include <cmath>
#include <iostream>
#include <iomanip>
#include <string>
#include <algorithm>
using string = std::string;
using datetime = long long;
using ENUM_BB_STATE = int;
const int BB_NONE=0, BB_PERIOD=20, BB_DEVIATION=2;
const int MA5_HIGH_PERIOD=5, MA10_HIGH_PERIOD=10;
const int MA5_LOW_PERIOD=5, MA10_LOW_PERIOD=10, EMA50_PERIOD=50;
const int MODE_LWMA=3, MODE_EMA=1, PRICE_HIGH=2, PRICE_LOW=3, PRICE_CLOSE=0;
double prices[100], opens[100], highs[100], lows[100];
int bars=70;
double ma_value=1.2;
template<size_t N> void ArrayInitialize(double (&a)[N], double v) {std::fill(a,a+N,v);}
double MathPow(double x,double y){return std::pow(x,y);}
double MathSqrt(double x){return std::sqrt(x);}
double MathMax(double x,double y){return std::max(x,y);}
double MathMin(double x,double y){return std::min(x,y);}
bool MathIsValidNumber(double x){return std::isfinite(x);}
int iBars(string,int){return bars;}
double iClose(string,int,int i){return i>=0 && i<bars ? prices[i] : 0;}
double iOpen(string,int,int i){return i>=0 && i<bars ? opens[i] : 0;}
double iHigh(string,int,int i){return i>=0 && i<bars ? highs[i] : 0;}
double iLow(string,int,int i){return i>=0 && i<bars ? lows[i] : 0;}
double iMA(string,int,int,int,int,int,int){return ma_value;}
int iBarShift(string,int,datetime){return 1;}
datetime iTime(string,int,int){return 900;}
double GetPointSize(string){return 0.00001;}
int GetDigits(string){return 5;}
int GetTimeframeSeconds(int t){return t*60;}
bool IsCandleClosed(datetime,int){return true;}
'''
    structs = "\n".join(source_block(source, "struct " + name) + ";"
                        for name in ("BollingerBand", "MovingAverage", "TimeframeData"))
    module = source[source.index("//| MODULE 06:"):source.index("double GetHighestHigh(")]
    driver = r'''
int main(int argc,char** argv) {
  string scenario=argv[1];
  for(int i=0;i<100;i++) {
    prices[i]=1.0+i*0.01; opens[i]=prices[i];
    highs[i]=prices[i]+0.02; lows[i]=prices[i]-0.02;
  }
  if(scenario=="short_bb") bars=20;
  if(scenario=="short_ema") bars=50;
  if(scenario=="boundary") bars=51;
  if(scenario=="missing_close") prices[10]=0;
  if(scenario=="missing_ema_close") prices[40]=0;
  if(scenario=="missing_high") highs[5]=0;
  if(scenario=="bad_ohlc") opens[1]=highs[1]+0.01;
  if(scenario=="missing_ma") ma_value=0;
  if(scenario=="nan_ma") ma_value=NAN;
  if(scenario=="nan_close") prices[10]=NAN;
  if(scenario=="flat") for(int i=0;i<100;i++) {
    prices[i]=opens[i]=1.2; highs[i]=1.22; lows[i]=1.18;
  }
  BollingerBand band{};
  CalculateBollinger("TEST",60,1,band);
  TimeframeData data{};
  GetDataForTimeframe("TEST",60,900,data);
  std::cout << std::setprecision(17) << band.MID_BB << " " << band.Width
            << " " << data.is_valid << "\n";
}
'''
    return prelude + structs + source_block(source, "void InitTimeframeData(") + module + driver


@pytest.fixture(scope="module")
def probe(tmp_path_factory):
    compiler = shutil.which("g++")
    assert compiler, "g++ required for exact-body M06 probe; no simulated PASS"
    directory = tmp_path_factory.mktemp("m06")
    cpp, executable = directory / "probe.cpp", directory / "probe"
    cpp.write_text(portable_source(SOURCE.read_text()))
    subprocess.run([compiler, "-std=c++17", "-Wall", "-Wextra", "-Wno-unused-parameter",
                    str(cpp), "-o", str(executable)], check=True, capture_output=True, text=True)
    def run(scenario):
        output = subprocess.check_output([str(executable), scenario], text=True).split()
        return float(output[0]), float(output[1]), bool(int(output[2]))
    return run


def test_complete_bb20_matches_population_standard_deviation(probe):
    middle, width, valid = probe("complete")
    prices = [1 + i * .01 for i in range(1, 21)]
    assert middle == pytest.approx(statistics.mean(prices))
    assert width == pytest.approx(4 * statistics.pstdev(prices))
    assert valid


@pytest.mark.parametrize("scenario", ["short_bb", "missing_close", "nan_close"])
def test_incomplete_bb20_does_not_emit_a_band(probe, scenario):
    middle, width, valid = probe(scenario)
    assert (middle, width) == (0, 0), f"{scenario}: partial/nonfinite BB20 was emitted"
    assert not valid


@pytest.mark.parametrize("scenario", ["short_bb", "short_ema", "missing_close",
    "missing_ema_close", "missing_high", "bad_ohlc", "missing_ma", "nan_ma", "nan_close"])
def test_unavailable_indicator_inputs_cannot_mark_snapshot_valid(probe, scenario):
    assert not probe(scenario)[2], f"{scenario}: invalid history/snapshot marked valid"


@pytest.mark.parametrize("scenario", ["boundary", "flat"])
def test_minimum_complete_history_and_flat_prices_remain_valid(probe, scenario):
    middle, width, valid = probe(scenario)
    assert math.isfinite(middle) and valid
    if scenario == "flat":
        assert width == pytest.approx(0, abs=1e-12)
