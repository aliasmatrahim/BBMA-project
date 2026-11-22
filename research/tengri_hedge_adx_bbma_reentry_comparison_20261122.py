import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_RUNNER = ROOT / "hedge_adx_filter_replay_20261121.py"
runner_text = BASE_RUNNER.read_text(encoding="utf-8")


def replace_once(old, new):
    global runner_text
    count = runner_text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match for patch, got {count}: {old[:120]!r}")
    runner_text = runner_text.replace(old, new, 1)


# Fixed variants: current H4 control and Build 5.16 H1 Re-Entry,
# with D1/H4 approved events additionally requiring the same live H4 ADX25 context.
old = 'variants={"MidBB25":("MidBB",25),"ADX20_25":("ADX20",25),"ADX25_25":("ADX25",25)}'
new = 'variants={"ADX25_25":("ADX25",25),"RE1_ADX25":("RE1",25),"RE2_ADX25":("RE2",25),"RE3_ADX25":("RE3",25),"RE4_ADX25":("RE4",25)}'
replace_once(old, new)

approved_counts = defaultdict(lambda: defaultdict(int))
context_counts = defaultdict(lambda: defaultdict(int))
events_by_symbol = defaultdict(list)
event_file = ROOT.parent / "BBMA516_SourceAudit" / "BBMA516_signal_events.csv"
with event_file.open(newline="", encoding="utf-8-sig") as fh:
    for row in csv.DictReader(fh):
        if row.get("d1_h4_m15_approved", "").strip().lower() != "true":
            continue
        event_time = dt.datetime.strptime(row["first_m15"], "%Y.%m.%d %H:%M").replace(tzinfo=dt.UTC)
        kind = int(row["type"].split("_")[2])
        direction = 1 if row["direction"] == "DIR_BUY" else -1
        ev = {"time": int(event_time.timestamp() * 1000), "kind": kind,
              "direction": direction, "hash": row["hash"]}
        events_by_symbol[row["symbol"]].append(ev)
        approved_counts[row["symbol"]][kind] += 1
for pair in events_by_symbol:
    events_by_symbol[pair].sort(key=lambda e: e["time"])

# Add pair identity to the H4 state, then pulse the H1 event only on a fresh quote
# and only while the identical H4 Mid-BB/ADX25/DI context is active.
replace_once(
    'h4_state={s:dict(key=None,mark=None,high=None,low=None,closes=deque(maxlen=20),bars=[]) for s in symbols}',
    'h4_state={s:dict(symbol=s,key=None,mark=None,high=None,low=None,closes=deque(maxlen=20),bars=[]) for s in symbols}'
)
replace_once(
    'return {"MidBB":closed,"ADX20":adx20,"ADX25":adx25}',
    '''out={"MidBB":closed,"ADX20":adx20,"ADX25":adx25}
    for kind in (1,2,3,4):
        out["RE"+str(kind)]=np.zeros(len(t),dtype=np.int8)
    pair=state["symbol"]
    for ev in events_by_symbol.get(pair,()):
        if len(t) and int(t[0])<=ev["time"]<=int(t[-1]):
            j=int(np.searchsorted(t,ev["time"],side="left"))
            if j<len(t) and int(t[j])-ev["time"]<=300000 and out["ADX25"][j]==ev["direction"]:
                out["RE"+str(ev["kind"])][j]=ev["direction"]
                context_counts[pair][ev["kind"]]+=1
    return out'''
)

# Campaign accounting: use the same quote fills and fixed 25% target as the H4 control.
replace_once(
    '    p=state["positions"]\n    direction=state["direction"]',
    '    p=state["positions"]\n    state.setdefault("_campaigns",[])\n    direction=state["direction"]'
)
replace_once(
    '            state["realized"]+=direction*(mark-price)*cut*conv[i]\n            cost+=.0001*cut*conv[i]',
    '''            raw=direction*(mark-price)*cut*conv[i]
            fixed=.0001*cut*conv[i]
            spread=cut*conv[i]*(ask[i]-bid[i])*0.5
            state["realized"]+=raw
            cost+=fixed
            state["_campaign_raw"]=state.get("_campaign_raw",0.0)+raw
            state["_campaign_fixed"]=state.get("_campaign_fixed",0.0)+fixed
            state["_campaign_spread"]=state.get("_campaign_spread",0.0)+spread
            state["spread_h4"]=state.get("spread_h4",0.0)+spread'''
)
replace_once(
    '    for lo,hi in zip(changes[:-1],changes[1:]):',
    '''        if not p and state.get("_campaign_open_ms") is not None:
            raw=state.get("_campaign_raw",0.0)
            fixed=state.get("_campaign_fixed",0.0)
            state["_campaigns"].append({
                "opened":state["_campaign_open_ms"],"closed":int(t[i]),
                "net_base":raw-fixed,"net_stress":raw-2.0*fixed,
                "raw_pnl":raw,"fixed_cost":fixed,
                "spread_estimate":state.get("_campaign_spread",0.0)})
            state["_campaign_open_ms"]=None
    for lo,hi in zip(changes[:-1],changes[1:]):'''
)
replace_once(
    '        if qty>target+.005:\n            reduce(qty-target,lo)',
    '        if qty>target+.005:\n            state["trims"]=state.get("trims",0)+1\n            reduce(qty-target,lo)'
)
replace_once(
    '            if not p:\n                state["opens"]+=1\n            direction=desired\n            p.append((qty_added,ask[i] if direction>0 else bid[i]))\n            cost+=qty_added*conv[i]*.0001',
    '''            if not p:
                state["opens"]+=1
                state["_campaign_open_ms"]=int(t[i])
                state["_campaign_raw"]=0.0
                state["_campaign_fixed"]=0.0
                state["_campaign_spread"]=0.0
            else:
                state["adds"]=state.get("adds",0)+1
            direction=desired
            p.append((qty_added,ask[i] if direction>0 else bid[i]))
            fixed_open=qty_added*conv[i]*.0001
            spread_open=qty_added*conv[i]*(ask[i]-bid[i])*0.5
            cost+=fixed_open
            state["_campaign_fixed"]+=fixed_open
            state["_campaign_spread"]+=spread_open
            state["spread_h4"]=state.get("spread_h4",0.0)+spread_open'''
)

# Keep one-pip base-cost equity stats and add a two-pip stress equity series.
replace_once(
    'stress_stats={n:dict(peak=opening,dd=0.,minimum=opening,last=opening) for n in variants}',
    'base_cost_stats={n:dict(peak=opening,dd=0.,minimum=opening,last=opening) for n in variants}\nstress2_stats={n:dict(peak=opening,dd=0.,minimum=opening,last=opening) for n in variants}'
)
replace_once(
    '''if n in variants and valid.any():
            z=stress_stats[n]
            h=(eq4000-costs_total[n])[valid]
            rp=np.maximum.accumulate(np.maximum(h,z["peak"]))
            z.update(peak=float(rp[-1]),dd=max(z["dd"],float(np.max(100*(rp-h)/rp))),
                     last=float(h[-1]),minimum=min(z["minimum"],float(h.min())))''',
    '''if n in variants and valid.any():
            for z,multiplier in ((base_cost_stats[n],1.0),(stress2_stats[n],2.0)):
                h=(eq4000-multiplier*costs_total[n])[valid]
                rp=np.maximum.accumulate(np.maximum(h,z["peak"]))
                z.update(peak=float(rp[-1]),dd=max(z["dd"],float(np.max(100*(rp-h)/rp))),
                         last=float(h[-1]),minimum=min(z["minimum"],float(h.min())))'''
)
replace_once(
    'm[n]["stress"]=stress_stats[n]\n        m[n]["by_symbol"]={s:{k:states[n][s].get(k,0) for k in ("opens","exits","exit_h4","exit_core","max_hedge","cost_h4","covered_sec","eligible_sec","realized")} for s in symbols}',
    '''m[n]["base_cost_equity"]=base_cost_stats[n]
        m[n]["stress2_equity"]=stress2_stats[n]
        m[n]["by_symbol"]={s:{k:states[n][s].get(k,0) for k in ("opens","adds","exits","trims","exit_h4","exit_core","max_hedge","cost_h4","spread_h4","covered_sec","eligible_sec","realized")} for s in symbols}
        total_fixed=sum(states[s][n].get("cost_h4",0.0) for s in symbols)
        total_spread=sum(states[s][n].get("spread_h4",0.0) for s in symbols)
        m[n]["pnl_after_1pip_USC"]=m[n]["pnl"]-total_fixed
        m[n]["pnl_after_2pip_USC"]=m[n]["pnl"]-2.0*total_fixed
        m[n]["costs_USC"]={"fixed_base_1pip":total_fixed,"fixed_stress_2pip":2.0*total_fixed,
                           "spread_estimate_included_in_quote_PnL":total_spread}
        camps=[c for s in symbols for c in states[s][n].get("_campaigns",[])]
        vals=[float(c["net_base"]) for c in camps]
        wins=[v for v in vals if v>0]
        losses=[v for v in vals if v<0]
        m[n]["hedge_campaigns"]={
            "closed":len(vals),"wins":len(wins),"losses":len(losses),
            "open_at_end":sum(bool(states[s][n]["positions"]) for s in symbols),
            "expectancy_after_1pip_USC":None if not vals else sum(vals)/len(vals),
            "profit_factor_after_1pip":None if not losses and not wins else
                (sum(wins)/abs(sum(losses)) if losses else "infinite_no_losses"),
            "net_closed_after_1pip_USC":sum(vals),
            "average_holding_hours":None if not camps else
                sum((c["closed"]-c["opened"])/3600000.0 for c in camps)/len(camps)}
        m[n]["exit_reasons"]={k:sum(states[s][n].get(k,0) for s in symbols)
                              for k in ("exit_h4","exit_core","trims")}'''
)
replace_once(
    'exec(compile(source,str(source_path),"exec"),dict(__file__=str(source_path),__name__="__main__",\n    execute_h4=execute_h4,bands=bands,deque=deque,variants=variants))',
    'exec(compile(source,str(source_path),"exec"),dict(__file__=str(source_path),__name__="__main__",\n    execute_h4=execute_h4,bands=bands,deque=deque,variants=variants,\n    events_by_symbol=events_by_symbol,approved_counts=approved_counts,context_counts=context_counts,\n    base_cost_stats=base_cost_stats,stress2_stats=stress2_stats))'
)
replace_once(
    'print("H4_RESULT",json.dumps(dict(window=[first,last],coverage=coverage,metrics=m,monthly=monthly)),flush=True)',
    'print("H4_RESULT",json.dumps(dict(window=[first,last],coverage=coverage,approved_events={s:{str(k):v for k,v in d.items()} for s,d in approved_counts.items()},events_with_adx_context={s:{str(k):v for k,v in d.items()} for s,d in context_counts.items()},metrics=m),separators=(",",":")),flush=True)'
)

os.chdir(ROOT)
sys.argv=[str(BASE_RUNNER),"full"]
namespace={"__file__":str(BASE_RUNNER),"__name__":"__main__",
           "events_by_symbol":events_by_symbol,"approved_counts":approved_counts,
           "context_counts":context_counts}
exec(compile(runner_text,str(BASE_RUNNER),"exec"),namespace)
