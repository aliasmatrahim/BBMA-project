from pathlib import Path
from collections import Counter, deque
import ast
import csv
import datetime as dt
import json
import re
import os
import sys
import numpy as np

ROOT=Path(__file__).resolve().parent
STRUCT_GEN=ROOT/"hedge_structure_retest_test_20261121.py"
STAGED_GEN=ROOT/"tengri_hedge_high_layer_staged_replay_20261123.py"
diagnostics=[]
warmup_counts={"EURUSD":[],"USDCHF":[]}

def assignment_value(source,name):
    tree=ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            return ast.literal_eval(node.value)
    raise RuntimeError(f"Missing assignment {name}")

def replace_assignment(source,name,value):
    tree=ast.parse(source)
    lines=source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            lines[node.lineno-1:node.end_lineno]=[f"{name} = {value!r}"]
            return "\n".join(lines)+"\n"
    raise RuntimeError(f"Missing assignment {name}")

# Extend the prior closed-candle H4/H1 swing-retest features with Mid-BB(20), ADX(14), and DI.
gen_text=STRUCT_GEN.read_text(encoding="utf-8")
feature_impl=assignment_value(gen_text,"feature_impl")
old_state='''return dict(key=None,mark=None,high=None,low=None,bars=deque(maxlen=1000),
                true_ranges=deque(maxlen=14),prev_close=None,atr=0.,
                direction=0,pivot_high=None,pivot_low=None,
                high_broken=False,low_broken=False,event=0,
                last_break_level=0.,break_time=0,
                closed_high=0.,closed_low=0.,closed_close=0.,
                closed_atr=0.,closed_time=0)'''
new_state='''return dict(key=None,mark=None,high=None,low=None,bars=deque(maxlen=1000),
                true_ranges=deque(maxlen=14),prev_close=None,atr=0.,
                direction=0,pivot_high=None,pivot_low=None,
                high_broken=False,low_broken=False,event=0,
                last_break_level=0.,break_time=0,
                closed_high=0.,closed_low=0.,closed_close=0.,
                closed_atr=0.,closed_time=0,
                closes=deque(maxlen=20),mid_side=0,mid_cross=0,
                adx_prev=None,adx_n=0,tr_sum=0.,plus_sum=0.,minus_sum=0.,
                dx_seed=[],adx_value=None,adx=0.,pdi=0.,mdi=0.)'''
assert feature_impl.count(old_state)==1
feature_impl=feature_impl.replace(old_state,new_state)
adx_helper='''
def _step_adx(state,high,low,close,period=14):
    prev=state["adx_prev"]
    state["adx_prev"]=(high,low,close)
    if prev is None:
        return None,None,None
    ph,pl,pc=prev
    tr=max(high-low,abs(high-pc),abs(low-pc))
    up=high-ph
    down=pl-low
    plus=up if up>down and up>0 else 0.
    minus=down if down>up and down>0 else 0.
    if state["adx_n"]<period:
        state["tr_sum"]+=tr
        state["plus_sum"]+=plus
        state["minus_sum"]+=minus
        state["adx_n"]+=1
    else:
        state["tr_sum"]=state["tr_sum"]-state["tr_sum"]/period+tr
        state["plus_sum"]=state["plus_sum"]-state["plus_sum"]/period+plus
        state["minus_sum"]=state["minus_sum"]-state["minus_sum"]/period+minus
    if state["adx_n"]<period:
        return None,None,None
    pdi=100.*state["plus_sum"]/state["tr_sum"] if state["tr_sum"] else 0.
    mdi=100.*state["minus_sum"]/state["tr_sum"] if state["tr_sum"] else 0.
    dx=100.*abs(pdi-mdi)/(pdi+mdi) if pdi+mdi else 0.
    if state["adx_value"] is None:
        state["dx_seed"].append(dx)
        if len(state["dx_seed"])>=period:
            state["adx_value"]=float(sum(state["dx_seed"][-period:])/period)
    else:
        state["adx_value"]=(state["adx_value"]*(period-1)+dx)/period
    return state["adx_value"],pdi,mdi
'''
assert feature_impl.count("def _close_structure_bar(state,close_time,tf_ms):")==1
feature_impl=feature_impl.replace("def _close_structure_bar(state,close_time,tf_ms):",adx_helper+"\ndef _close_structure_bar(state,close_time,tf_ms):",1)
needle='    state["closed_atr"],state["closed_time"]=state["atr"],int(close_time)\n'
addon='''    state["closed_atr"],state["closed_time"]=state["atr"],int(close_time)
    state["closes"].append(close)
    previous_mid=int(state["mid_side"])
    mid_side=0
    if len(state["closes"])==20:
        mid=float(sum(state["closes"])/20.0)
        mid_side=1 if close>mid else (-1 if close<mid else 0)
    state["mid_side"]=mid_side
    state["mid_cross"]=mid_side if previous_mid and mid_side and mid_side!=previous_mid else 0
    adx,pdi,mdi=_step_adx(state,high,low,close)
    state["adx"]=float(adx) if adx is not None else 0.0
    state["pdi"]=float(pdi) if pdi is not None else 0.0
    state["mdi"]=float(mdi) if mdi is not None else 0.0
'''
assert feature_impl.count(needle)==1
feature_impl=feature_impl.replace(needle,addon,1)
needle='        "closed_time":np.zeros(len(t),dtype=np.int64),\n'
addon='''        "closed_time":np.zeros(len(t),dtype=np.int64),
        "mid_side":np.zeros(len(t),dtype=np.int8),
        "mid_cross":np.zeros(len(t),dtype=np.int8),
        "adx":np.zeros(len(t),dtype=float),
        "pdi":np.zeros(len(t),dtype=float),
        "mdi":np.zeros(len(t),dtype=float),
'''
assert feature_impl.count(needle)==1
feature_impl=feature_impl.replace(needle,addon,1)
needle='''        out["event"][lo]=state["event"]
        state["event"]=0
'''
addon='''        out["event"][lo]=state["event"]
        state["event"]=0
        out["mid_side"][lo:hi]=state["mid_side"]
        out["adx"][lo:hi]=state["adx"]
        out["pdi"][lo:hi]=state["pdi"]
        out["mdi"][lo:hi]=state["mdi"]
        out["mid_cross"][lo]=state["mid_cross"]
        state["mid_cross"]=0
'''
assert feature_impl.count(needle)==1
feature_impl=feature_impl.replace(needle,addon,1)

# Extract the common high-layer execution routine and add a structured event trace.
fn=assignment_value(STAGED_GEN.read_text(encoding="utf-8"),"fn")
fn=fn.replace(
 "def execute_h4(state,t,bid,ask,rows,signal,entry_signal,symbol,size_rule):",
 "def execute_h4(state,t,bid,ask,rows,signal,entry_signal,symbol,size_rule,raw_entry_signal=None,gate_reason=None,strategy=''):",1)
old='''(np.diff(signal)!=0) | (np.diff(entry_signal)!=0))+1,len(t)]'''
new='''(np.diff(signal)!=0) | (np.diff(entry_signal)!=0) | (np.diff(raw_entry_signal)!=0))+1,len(t)]'''
assert fn.count(old)==1
fn=fn.replace(old,new,1)
needle='''    state.setdefault("_reversal_pending",False)

    def qty_now():'''
addon='''    state.setdefault("_reversal_pending",False)
    state.setdefault("_strategy",strategy)

    def emit(kind,i,row,layers,status="",reason="",signal_dir=None,lots_before=None,lots_after=None):
        net=float(row[0]-row[4])
        diagnostics.append({
            "strategy":strategy,"symbol":symbol,"event":kind,"time_ms":int(t[i]),
            "signal_direction":signal_dir,"tengri_direction":int(np.sign(net)),
            "tengri_net_lots":round(net,2),"tengri_layer":int(layers),
            "hedge_direction":int(direction),
            "hedge_lots_before":None if lots_before is None else round(float(lots_before),2),
            "hedge_lots_after":round(float(qty_now()),2) if lots_after is None else round(float(lots_after),2),
            "decision":status,"reason":reason,
            "reentry_number":int(state.get("reentries",0))
        })

    def qty_now():'''
assert fn.count(needle)==1
fn=fn.replace(needle,addon,1)
needle='''        state["direction"]=direction
        return amount

    def open_piece(amount,i,kind):'''
addon='''        state["direction"]=direction
        emit("hedge_exit" if not p else "hedge_trim",i,row,layers,
             "closed" if not p else "trimmed",reason,lots_before=total)
        return amount

    def open_piece(amount,i,kind):'''
assert fn.count(needle)==1
fn=fn.replace(needle,addon,1)
needle='''        side=-int(np.sign(rows[i,0]-rows[i,4]))
        if side==0:'''
addon='''        opening_campaign=not p
        before_qty=qty_now()
        side=-int(np.sign(rows[i,0]-rows[i,4]))
        if side==0:'''
assert fn.count(needle)==1
fn=fn.replace(needle,addon,1)
needle='''        state["cost_h4"]=cost
        return True

    def monitor(start,stop,row,layers):'''
addon='''        state["cost_h4"]=cost
        emit("hedge_entry" if opening_campaign else "hedge_add",i,rows[i],layers,
             "accepted",kind,signal_dir=side,lots_before=before_qty)
        return True

    def monitor(start,stop,row,layers):'''
assert fn.count(needle)==1
fn=fn.replace(needle,addon,1)
needle='''        if layers>=7:
            state["eligible_sec"]+=float(durations[lo:hi].sum())
        # Core flattening or side change invalidates the current hedge.'''
addon='''        if layers>=7:
            state["eligible_sec"]+=float(durations[lo:hi].sum())
        if raw_entry_signal is not None and raw_entry_signal[lo]:
            cand=int(raw_entry_signal[lo])
            gate=str(gate_reason[lo] or "") if gate_reason is not None else ""
            if gate:
                decision,why="blocked",gate
            elif desired==0:
                decision,why="blocked","no_tengri_exposure"
            elif cand!=desired:
                decision,why="blocked","signal_not_adverse_to_tengri"
            elif layers<7:
                decision,why="blocked","tengri_layer_below_7"
            elif p and state["_reversal_pending"]:
                decision,why="accepted","fresh_adverse_signal_cancels_exit_pending"
            elif p:
                decision,why="accepted","active_hedge_rebalanced_to_layer_size"
            else:
                decision,why="accepted","eligible_fresh_entry"
            emit("entry_signal",lo,row,layers,decision,why,signal_dir=cand)
        if signal[lo]:
            if p and int(signal[lo])==-direction:
                emit("exit_signal",lo,row,layers,"received","exit_toward_tengri",signal_dir=int(signal[lo]))
            elif p:
                emit("exit_signal",lo,row,layers,"ignored","exit_signal_not_toward_tengri",signal_dir=int(signal[lo]))
            else:
                emit("exit_signal",lo,row,layers,"blocked","no_hedge_open",signal_dir=int(signal[lo]))
        # Core flattening or side change invalidates the current hedge.'''
assert fn.count(needle)==1
fn=fn.replace(needle,addon,1)
fn=re.sub(
 r'(?m)^([ \t]*)state\["spread_blocked"\]=state.get\("spread_blocked",0\)\+1$',
 lambda m:m.group(0)+"\n"+m.group(1)+'emit("spread_blocked",lo,row,layers,"blocked","spread_above_3_pips",signal_dir=int(entry_signal[lo]))',
 fn)

# Rewrite the existing structure experiment into the three frozen variants.
new_variants='variants={"STRUCTURE_ONLY":None,"INDICATOR_ONLY":None,"HYBRID":None}'
gen_text=replace_assignment(gen_text,"new_variants",new_variants)
gen_text=replace_assignment(gen_text,"feature_impl",feature_impl)
new_calls='''        raw_struct=retest_pulses(a,tf_today[symbol],retest_state[symbol]["STRUCTURE_ONLY"],("H4",),"H1")
        raw_hybrid=retest_pulses(a,tf_today[symbol],retest_state[symbol]["HYBRID"],("H4",),"H1")
        exit_struct=tf_today[symbol]["H1"]["event"]
        exit_indicator=tf_today[symbol]["H1"]["mid_cross"]
        gate_struct=np.full(len(t),"",dtype=object)
        gate_hybrid=np.full(len(t),"",dtype=object)
        gate_indicator=np.full(len(t),"",dtype=object)
        allow_hybrid=raw_hybrid.copy()
        raw_indicator=tf_today[symbol]["H4"]["mid_cross"].copy()
        allow_indicator=raw_indicator.copy()
        for j in np.flatnonzero(raw_hybrid):
            d=int(raw_hybrid[j])
            h4=tf_today[symbol]["H4"]
            aligned=(float(h4["adx"][j])>25.0 and
                     ((d>0 and float(h4["pdi"][j])>float(h4["mdi"][j])) or
                      (d<0 and float(h4["mdi"][j])>float(h4["pdi"][j]))))
            if not aligned:
                allow_hybrid[j]=0
                gate_hybrid[j]="h4_adx_di_not_aligned_at_retest"
        for j in np.flatnonzero(raw_indicator):
            d=int(raw_indicator[j])
            h4=tf_today[symbol]["H4"]
            aligned=(float(h4["adx"][j])>25.0 and
                     ((d>0 and float(h4["pdi"][j])>float(h4["mdi"][j])) or
                      (d<0 and float(h4["mdi"][j])>float(h4["pdi"][j]))))
            if not aligned:
                allow_indicator[j]=0
                gate_indicator[j]="h4_adx_di_filter"
        ret["STRUCTURE_ONLY"]=execute_h4(states["STRUCTURE_ONLY"][symbol],t,bid,ask,rows,
            exit_struct,raw_struct,symbol,"STAGED",raw_entry_signal=raw_struct,
            gate_reason=gate_struct,strategy="STRUCTURE_ONLY")
        ret["INDICATOR_ONLY"]=execute_h4(states["INDICATOR_ONLY"][symbol],t,bid,ask,rows,
            exit_indicator,allow_indicator,symbol,"STAGED",raw_entry_signal=raw_indicator,
            gate_reason=gate_indicator,strategy="INDICATOR_ONLY")
        ret["HYBRID"]=execute_h4(states["HYBRID"][symbol],t,bid,ask,rows,
            exit_struct,allow_hybrid,symbol,"STAGED",raw_entry_signal=raw_hybrid,
            gate_reason=gate_hybrid,strategy="HYBRID")
'''
gen_text=replace_assignment(gen_text,"new_calls",new_calls)
new_exec='''    execute_h4=execute_h4,features=features,init_tf_state=init_tf_state,
    init_retest_state=init_retest_state,retest_pulses=retest_pulses,
    timeframe_ms=timeframe_ms,deque=deque,variants=variants,
    diagnostics=diagnostics,warmup_counts=warmup_counts,print=quiet_print))'''
gen_text=replace_assignment(gen_text,"new_exec",new_exec)
# Pass shared trace and quiet output into the generated source environment.
old_final='exec(compile(text,str(base_path),"exec"),{"__file__":str(base_path),"__name__":"__main__"})'
new_final='exec(compile(text,str(base_path),"exec"),{"__file__":str(base_path),"__name__":"__main__","execute_h4":execute_h4,"diagnostics":diagnostics,"warmup_counts":warmup_counts,"quiet_print":quiet_print})'
if gen_text.count(old_final)!=1:
    raise RuntimeError("Structure generator final exec anchor missing")
gen_text=gen_text.replace(old_final,new_final,1)
# Instrument warm-up quote availability while preserving the prior 15-calendar-day warm-up.
old_replacement=assignment_value(gen_text,"replacement")
new_replacement='''tf_state={s:{tf:init_tf_state() for tf in timeframe_ms} for s in symbols}
retest_state={s:{n:init_retest_state() for n in variants} for s in symbols}
for warm in range(16,1,-1):
    for symbol in symbols:
        day=dt.date.fromisoformat(first)-dt.timedelta(days=warm)
        a=quotes(symbol,day)
        if a is not None and len(a):
            warmup_counts[symbol].append({"day":day.isoformat(),"ticks":int(len(a))})
            for tf,ms in timeframe_ms.items():
                features(a,tf_state[symbol][tf],ms)'''
gen_text=replace_assignment(gen_text,"replacement",new_replacement)

# Compile and execute the structure generator against the locked full sample.
fn_env={"np":np,"deque":deque,"diagnostics":diagnostics,"dt":dt}
exec(compile(fn,STAGED_GEN.name,"exec"),fn_env)
execute_h4=fn_env["execute_h4"]

def quiet_print(*args,**kwargs):
    return None

env={"__file__":str(STRUCT_GEN),"__name__":"__main__",
     "execute_h4":execute_h4,"execute_mtf":execute_h4,
     "diagnostics":diagnostics,"warmup_counts":warmup_counts,
     "quiet_print":quiet_print}
sys.argv=[str(STRUCT_GEN),"full"]
os.chdir(ROOT)
exec(compile(gen_text,str(STRUCT_GEN),"exec"),env)

summary={}
for name in ("STRUCTURE_ONLY","INDICATOR_ONLY","HYBRID"):
    evs=[x for x in diagnostics if x.get("strategy")==name]
    entries=[x for x in evs if x.get("event")=="entry_signal"]
    blocked=Counter(x.get("reason") for x in entries if x.get("decision")=="blocked")
    layer_counts=Counter(("7-8" if x.get("tengri_layer",0) in (7,8) else
                          "9" if x.get("tengri_layer",0)==9 else
                          "10+" if x.get("tengri_layer",0)>=10 else "below7")
                         for x in entries)
    exits=Counter(x.get("reason") for x in evs if x.get("event")=="hedge_exit")
    summary[name]={
        "entry_signal_count":len(entries),
        "accepted_signal_count":sum(x.get("decision")=="accepted" for x in entries),
        "blocked_signal_reasons":dict(blocked),
        "entry_signals_by_layer":dict(layer_counts),
        "hedge_entries":sum(x.get("event")=="hedge_entry" for x in evs),
        "hedge_adds":sum(x.get("event")=="hedge_add" for x in evs),
        "hedge_exits":sum(x.get("event")=="hedge_exit" for x in evs),
        "hedge_trims":sum(x.get("event")=="hedge_trim" for x in evs),
        "reentries":sum(x.get("event")=="hedge_entry" and int(x.get("reentry_number",0))>0 for x in evs),
        "exit_reasons":dict(exits),
        "exit_signal_count":sum(x.get("event")=="exit_signal" for x in evs)
    }
for row in diagnostics:
    row["time_utc"]=dt.datetime.fromtimestamp(int(row.pop("time_ms"))/1000,dt.UTC).isoformat(timespec="milliseconds")
warm_summary={}
for symbol,items in warmup_counts.items():
    warm_summary[symbol]={"days_attempted":15,"days_with_ticks":len(items),
                          "ticks_loaded":sum(x["ticks"] for x in items),
                          "available_days":[x["day"] for x in items]}
result={"status":"diagnostic_only","sample_utc":["2026-05-01","2026-11-18"],
        "symbols":["EURUSD","USDCHF"],"warmup":warm_summary,
        "data_source":"local tick NPZ plus Tengri statement ledger/snapshots",
        "mt4_hfm_server_identity":"unverified",
        "shared_policy":{"layer_gate":7,"size_pct_by_layer":{"7":25,"8":50,"9":75,"10+":100},
          "max_spread_pips":3,"fixed_cost_pips_per_action":1,
          "safety_close":"Tengri flat or net direction change",
          "exit_pending":"signal exit waits for net BE; BE floor closes at net BE after reaching +1 study unit",
          "reentry":"fresh adverse signal after hedge close",
          "performance_metrics":"not reported"},
        "strategies":summary,"event_count":len(diagnostics)}
out_json=ROOT/"tengri_hedge_three_strategy_diagnostics_20261123.json"
out_csv=ROOT/"tengri_hedge_three_strategy_diagnostics_20261123.csv"
out_json.write_text(json.dumps({"summary":result,"events":diagnostics},indent=2),encoding="utf-8")
fields=sorted({k for row in diagnostics for k in row})
with out_csv.open("w",newline="",encoding="utf-8-sig") as fh:
    writer=csv.DictWriter(fh,fieldnames=fields or ["strategy","symbol","event"])
    writer.writeheader()
    writer.writerows(diagnostics)
print("DIAGNOSTIC_RESULT",json.dumps(result,ensure_ascii=False),flush=True)