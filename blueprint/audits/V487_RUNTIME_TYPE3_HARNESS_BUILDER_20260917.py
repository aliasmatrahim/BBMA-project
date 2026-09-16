from pathlib import Path
import subprocess

W = Path(r"D:\BBMA\Workspace\q5-type3-close-side-180")
R = Path(r"D:\BBMA\MT4_TesterRunner_Diag")
FIXED = (W / "blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8-sig")
OWNER = subprocess.check_output(["git", "-C", str(W), "show", "origin/d1-owner-dev:blueprint/source/BBMA_EA.mq4"]).decode("utf-8-sig")

def infra(src, label, version):
    src = src.replace(src.splitlines()[2], f"//| Version {version} - Q5 Type3 Runtime Harness            |", 1)
    old_ver = '#property version   "4.87"' if label == "FIXED" else '#property version   "4.61"'
    src = src.replace(old_ver, f'#property version   "{version}"', 1)
    src = src.replace('if(requested == "") return "";\n', 'if(requested == "") return "";\n   if(IsTesting() && requested == Symbol()) return Symbol();\n', 1)
    src = src.replace('bool IsTerminalConnected()\n{\n   return IsConnected();\n}', 'bool IsTerminalConnected()\n{\n   if(IsTesting()) return true;\n   return IsConnected();\n}', 1)
    old = 'ResetLastError();\n   if(!EventSetTimer(1))\n   {\n      int timerError = GetLastError();\n      g_is_initialized = false;\n      Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));\n      return INIT_FAILED;\n   }'
    new = 'if(!IsTesting())\n   {\n      ResetLastError();\n      if(!EventSetTimer(1))\n      {\n         int timerError = GetLastError();\n         g_is_initialized = false;\n         Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));\n         return INIT_FAILED;\n      }\n   }'
    return src.replace(old, new, 1)
def add_diag(src, label):
    needle = 'if(!HasReEntryMA5OrMA50Touch(data, direction)) return RE_STATE_CANDIDATE;\n'
    diag = needle + f'         double q5ma5=0, q5ma10=0;\n         bool q5cluster=GetReEntryMACluster(data, direction, q5ma5, q5ma10);\n         bool q5fail=(!q5cluster || data.close <= 0 ||\n                     (direction == DIR_BUY && data.close < MathMin(q5ma5, q5ma10)) ||\n                     (direction == DIR_SELL && data.close > MathMax(q5ma5, q5ma10)));\n         if(IsTesting()) Print("[Q5T3][RETRACE] Variant={label} Dir=", EnumToString(direction),\n                              " TF=", data.timeframe, " Candle=", TimeToString(data.candle_time),\n                              " Close=", DoubleToString(data.close, Digits),\n                              " MA5=", DoubleToString(q5ma5, Digits),\n                              " MA10=", DoubleToString(q5ma10, Digits),\n                              " MA50=", DoubleToString(data.ma[4], Digits),\n                              " FullClusterFailure=", q5fail ? "Y" : "N");\n'
    src = src.replace(needle, diag, 1)
    if label == "OWNER":
        marker = '         ConfirmReEntryState(reEntry, data,\n            "Type3 confirmed: post-CSM retrace to MA5 or MA50");'
        src = src.replace(marker, '         if(IsTesting()) Print("[Q5T3][CONFIRM] Variant=OWNER Failure=", q5fail ? "Y" : "N", " Candle=", TimeToString(data.candle_time));\n\n' + marker, 1)
    else:
        marker = '         if(IsReEntryMAClusterCloseSideFailure(data, direction)) return RE_STATE_CANDIDATE;\n\n         ConfirmReEntryState(reEntry, data,'
        repl = '         if(IsReEntryMAClusterCloseSideFailure(data, direction)) return RE_STATE_CANDIDATE;\n         if(IsTesting()) Print("[Q5T3][CONFIRM] Variant=FIXED Failure=", q5fail ? "Y" : "N", " Candle=", TimeToString(data.candle_time));\n\n         ConfirmReEntryState(reEntry, data,'
        src = src.replace(marker, repl, 1)
    return src
owner = add_diag(infra(OWNER, "OWNER", "4.872"), "OWNER")
fixed = add_diag(infra(FIXED, "FIXED", "4.871"), "FIXED")

assert "Variant=OWNER" in owner and "FullClusterFailure=" in owner
assert "Variant=FIXED" in fixed and "FullClusterFailure=" in fixed
assert "IsReEntryMAClusterCloseSideFailure(data, direction)) return RE_STATE_CANDIDATE" not in owner
assert "IsReEntryMAClusterCloseSideFailure(data, direction)) return RE_STATE_CANDIDATE" in fixed

out = R / "MQL4/Experts"
out.mkdir(parents=True, exist_ok=True)
owner_path = out / "BBMA_EA_Q5_180_OWNER_HARNESS.mq4"
fixed_path = out / "BBMA_EA_Q5_180_V487_HARNESS.mq4"
owner_path.write_text(owner, encoding="utf-8")
fixed_path.write_text(fixed, encoding="utf-8")
print(owner_path)
print(fixed_path)
