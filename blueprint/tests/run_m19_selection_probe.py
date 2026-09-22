#!/usr/bin/env python3
"""Actual M19 bodies against broker selection fault stubs; requires g++.
No terminal, broker connection or production test seam.
Catches unknown exposure being skipped and unnecessary order reselection.
"""
from pathlib import Path
import subprocess, sys, tempfile
PREFIX = "// Read-only diagnostic. Exact Build 5.03 function bodies; mocked broker only.\n#include <cmath>\n#include <iostream>\n#include <string>\nusing std::string;\nconst int SELECT_BY_TICKET=1, LOCK_OFF=0, LOCK_SAME_DIRECTION=1, LOCK_ONE_POSITION=2;\nconst int DEC_VALIDATED=1, DIR_BUY=1, DIR_SELL=2;\nstruct TradeInfo { int ticket=1, magic_number=1001, direction=DIR_BUY; string pair=\"GBPUSD\"; double remaining_lot=1, entry_price=100, current_sl=80; };\nstruct Pair { int magic_number=1001; };\nstruct RiskValidationSnapshot {};\nstruct BBMA_Decision { string DecisionID=\"D\", Pair=\"GBPUSD\"; int DecisionState=DEC_VALIDATED, Direction=DIR_BUY; };\nTradeInfo g_monitored_trades[2]; Pair g_pair_states[1]; int g_monitored_count=1, TradeLockMode=0;\nint select_calls=0, fail_select=0, live_magic=1001, closed=0;\ndouble g_protection_reference_equity=1000;\nbool OrderSelect(int,int) { ++select_calls; return fail_select==-1 ? false : select_calls!=fail_select; }\nint OrderCloseTime() { return closed; }\nint OrderMagicNumber() { return live_magic; }\nint FindPairStateIndex(string p) { return p==\"GBPUSD\" ? 0 : -1; }\ndouble GetTickValue(string) { return 1; }\ndouble GetTickSize_Price(string) { return 1; }\ndouble MathAbs(double x) { return std::abs(x); }\nvoid ResetLastError() {}\ndouble OrderProfit() { return -10; }\ndouble OrderSwap() { return -1; }\ndouble OrderCommission() { return -2; }\nbool IsDecisionExecuted(string) { return false; }\n"
TAIL = "\nvoid reset() { select_calls=0; fail_select=0; live_magic=1001; closed=0; g_monitored_trades[0]=TradeInfo(); g_monitored_count=1; }\nint main() {\n RiskValidationSnapshot snap; bool valid; int failures=0;\n auto risk=[&](){return CalculateTotalRisk(\"GBPUSD\",1,100,95,snap,valid);};\n auto check=[&](string name,double got,double want,bool ok,bool wanted){std::cout<<name<<\" risk=\"<<got<<\" valid=\"<<ok<<\" expected=\"<<want<<\"/\"<<wanted<<\"\\n\"; if(std::abs(got-want)>1e-8 || ok!=wanted) ++failures;};\n reset(); double x=risk(); check(\"owned\",x,25,valid,true);\n reset(); closed=1; x=risk(); check(\"closed\",x,5,valid,true);\n reset(); live_magic=2002; x=risk(); check(\"foreign\",x,5,valid,true);\n reset(); g_monitored_trades[0].magic_number=2002; x=risk(); check(\"registry_foreign\",x,5,valid,true);\n reset(); g_monitored_trades[0].current_sl=100; x=risk(); check(\"breakeven\",x,5,valid,true);\n reset(); g_monitored_count=0; x=risk(); check(\"empty\",x,5,valid,true);\n reset(); g_monitored_trades[0].current_sl=0; x=risk(); check(\"unknown_sl\",x,0,valid,false);\n reset(); fail_select=1; x=risk(); check(\"transient_first_selection_failure\",x,0,valid,false);\n reset(); fail_select=-1; x=risk(); check(\"persistent_selection_failure\",x,0,valid,false);\n reset(); x=risk(); std::cout<<\"single_selection calls=\"<<select_calls<<\" expected=1\\n\"; if(select_calls!=1)++failures;\n std::cout<<\"SAFETY_ASSERTION_FAILURES=\"<<failures<<\"\\n\"; return failures?1:0;\n}\n"
def body(src, signature):
    start = src.index(signature)
    brace = src.index("{", start)
    depth = 0
    for pos in range(brace, len(src)):
        depth += (src[pos] == "{") - (src[pos] == "}")
        if depth == 0:
            return src[start:pos + 1]
    raise AssertionError(signature)
def main():
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "blueprint/source/BBMA_EA.mq4")
    src = source.read_text(encoding="utf-8")
    signatures = ["bool IsLiveEAOwnedPortfolioTrade(", "double CalculateTradeRiskMoney(", "double CalculateTotalRisk("]
    with tempfile.TemporaryDirectory() as tmp:
        cpp, exe = Path(tmp)/"probe.cpp", Path(tmp)/"probe"
        cpp.write_text(PREFIX + "\n\n".join(body(src, s) for s in signatures) + TAIL)
        subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", "-Wno-unused-parameter", str(cpp), "-o", str(exe)], check=True)
        return subprocess.run([str(exe)]).returncode
if __name__ == "__main__":
    raise SystemExit(main())
