from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "tengri_hedge_bbma_exit_comparison_20261122.py"
src = TEMPLATE.read_text(encoding="utf-8")

# Replace the fixed four-variant list with the locked high-layer ladder,
# separate Type 1-4 arms, H4 control exits, and Type 3 fixed-ratio sensitivity.
a = src.index("# Fixed variants:")
b = src.index("\napproved_counts", a)
variant_block = """
# Locked high-layer variants. Sizing is relative to current net Tengri lots.
old = 'variants={"MidBB25":("MidBB",25),"ADX20_25":("ADX20",25),"ADX25_25":("ADX25",25)}'
new = 'variants={"ADX25_STAGE":("ADX25","STAGED"),"ADX25_STAGE_REEXIT":("ADX25","STAGED"),"RE1_STAGE_REEXIT":("RE1","STAGED"),"RE2_STAGE_REEXIT":("RE2","STAGED"),"RE3_STAGE_REEXIT":("RE3","STAGED"),"RE4_STAGE_REEXIT":("RE4","STAGED"),"RE3_R25_REEXIT":("RE3",25),"RE3_R50_REEXIT":("RE3",50),"RE3_R75_REEXIT":("RE3",75),"RE3_R100_REEXIT":("RE3",100)}'
replace_once(old, new)
"""
src = src[:a] + variant_block + src[b:]
a=src.index("# Campaign accounting:")
b=src.index("# Keep one-pip base-cost equity stats",a)
src=src[:a] + "# Custom execute_h4 handles campaign accounting and staged sizing.\n\n" + src[b:]
a=src.index("replace_once(\n    'reason=\"exit_core\"")
b=src.index("\nos.chdir(ROOT)",a)
src=src[:a] + src[b:]

# Replace the previous quantity/exit routine with the user's rule:
# dynamically track Tengri exposure, close on profitable reversal, hold to BE if needed,
# preserve a BE floor after a positive run, and allow re-entry only on a fresh adverse event.
fn = r'''
def execute_h4(state,t,bid,ask,rows,signal,entry_signal,symbol,size_rule):
    conv=100000/np.maximum(bid,1e-5) if symbol=="USDCHF" else np.full(len(t),100000.)
    changes=np.r_[0,np.flatnonzero(
        np.any(np.diff(rows,axis=0)!=0,axis=1) |
        (np.diff(signal)!=0) | (np.diff(entry_signal)!=0))+1,len(t)]
    f=np.zeros(len(t)); r=np.zeros(len(t)); c=np.zeros(len(t))
    durations=np.r_[np.minimum(np.diff(t),60000),0]/1000.0
    p=state["positions"]
    direction=state["direction"]
    direction=int(direction)
    realized=float(state.get("realized",0.0))
    cost=float(state.get("cost_h4",0.0))
    for k,v in {
        "opens":0,"adds":0,"exits":0,"trims":0,"exit_h4":0,"exit_bbma_re":0,
        "exit_core":0,"exit_be":0,"exit_reversal":0,"exit_pending":0,
        "reentries":0,"max_hedge":0.0,"cost_h4":cost,"spread_h4":0.0,
        "eligible_sec":0.0,"covered_sec":0.0,"offset_eligible_seconds":0.0,
        "offset_positive_seconds":0.0,"offset_full_seconds":0.0,
        "offset_weighted_cover_seconds":0.0,"offset_max_cover_ratio":0.0,
        "offset_exit_samples":0,"offset_full_exits":0,"offset_exit_cover_sum":0.0,
    }.items():
        state.setdefault(k,v)
    state.setdefault("_campaigns",[])
    state.setdefault("_campaign_raw",0.0)
    state.setdefault("_campaign_fixed",0.0)
    state.setdefault("_campaign_spread",0.0)
    state.setdefault("_campaign_open_ms",None)
    state.setdefault("_campaign_peak_net",-1e99)
    state.setdefault("_reversal_pending",False)

    def qty_now():
        return float(sum(q for q,_ in p))

    def rows_core_float(row,start,stop):
        # Ledger row format: long lots/weighted price at 0/1; short lots/weighted at 4/5.
        return ((bid[start:stop]*float(row[0])-float(row[1])) +
                (float(row[5])-ask[start:stop]*float(row[4]))) * conv[start:stop]

    def hedge_float(start,stop):
        if not p or direction==0:
            return np.zeros(stop-start,dtype=float)
        qty=qty_now()
        weighted=sum(q*price for q,price in p)
        px=bid[start:stop] if direction>0 else ask[start:stop]
        return direction*(px*qty-weighted)*conv[start:stop]

    def mark(start,stop):
        if stop<=start:
            return
        f[start:stop]=hedge_float(start,stop)
        r[start:stop]=realized
        c[start:stop]=cost

    def record_offset(start,stop,row,layers):
        if stop<=start or layers<7:
            return
        cf=rows_core_float(row,start,stop)
        loss=-cf
        eligible=loss>0
        if not eligible.any():
            return
        hf=hedge_float(start,stop)
        q=qty_now()
        est_close=q*conv[start:stop]*0.0001
        hedge_net=realized-cost+hf-est_close
        sec=durations[start:stop]
        sec=sec[eligible]
        loss=loss[eligible]
        hedge_net=hedge_net[eligible]
        state["offset_eligible_seconds"]+=float(sec.sum())
        state["offset_positive_seconds"]+=float(sec[hedge_net>0].sum())
        state["offset_full_seconds"]+=float(sec[hedge_net>=loss].sum())
        state["offset_weighted_cover_seconds"]+=float((np.clip(hedge_net/loss,0.,1.)*sec).sum())
        state["offset_max_cover_ratio"]=max(
            state["offset_max_cover_ratio"],
            float(np.max(np.maximum(hedge_net/loss,0.0))))

    def close_piece(amount,i,reason,row,layers):
        nonlocal realized,cost,direction
        total=qty_now()
        amount=min(total,max(0.0,float(amount)))
        amount=np.floor((amount+1e-10)*100.0)/100.0
        if amount<0.01:
            return 0.0
        coref=float(rows_core_float(row,i,i+1)[0])
        hf=float(hedge_float(i,i+1)[0])
        projected_total=realized-cost+hf-amount*conv[i]*0.0001
        if layers>=7 and coref<0:
            loss=-coref
            state["offset_exit_samples"]+=1
            ratio=max(0.0,projected_total/loss)
            state["offset_exit_cover_sum"]+=ratio
            if projected_total>=loss:
                state["offset_full_exits"]+=1
        side=direction
        close_price=bid[i] if side>0 else ask[i]
        remain=amount
        raw=0.0
        while remain>=0.01-1e-9 and p:
            q,price=p[-1]
            cut=min(q,remain)
            raw+=(close_price-price)*side*cut*conv[i]
            q=round(q-cut,8)
            remain=round(remain-cut,8)
            if q<0.01-1e-9:
                p.pop()
            else:
                p[-1]=(q,price)
        fixed=amount*conv[i]*0.0001
        spread=amount*conv[i]*(ask[i]-bid[i])*0.5
        realized+=raw
        cost+=fixed
        state["_campaign_raw"]+=raw
        state["_campaign_fixed"]+=fixed
        state["_campaign_spread"]+=spread
        state["spread_h4"]+=spread
        if amount < total-0.005:
            state["trims"]+=1
        if not p:
            state["exits"]+=1
            if reason=="be_floor":
                state["exit_be"]+=1
            elif reason.startswith("confirmed_reverse") or reason=="reversal_be":
                state["exit_reversal"]+=1
                state[state.get("exit_reason","exit_h4")]+=1
            elif reason=="core_safety":
                state["exit_core"]+=1
            else:
                state[state.get("exit_reason","exit_h4")]+=1
            camp_raw=float(state["_campaign_raw"])
            camp_fixed=float(state["_campaign_fixed"])
            state["_campaigns"].append({
                "opened":state["_campaign_open_ms"],"closed":int(t[i]),
                "raw_pnl":camp_raw,"fixed_cost":camp_fixed,
                "spread_estimate":float(state["_campaign_spread"]),
                "net_base":camp_raw-camp_fixed,"net_stress":camp_raw-2.0*camp_fixed,
                "exit_reason":reason})
            state["_campaign_open_ms"]=None
            state["_campaign_raw"]=0.0
            state["_campaign_fixed"]=0.0
            state["_campaign_spread"]=0.0
            state["_campaign_peak_net"]=-1e99
            state["_reversal_pending"]=False
            direction=0
        state["realized"]=realized
        state["cost_h4"]=cost
        state["direction"]=direction
        return amount

    def open_piece(amount,i,kind):
        nonlocal cost,direction
        amount=np.floor((float(amount)+1e-10)*100.0)/100.0
        if amount<0.01:
            return False
        side=-int(np.sign(rows[i,0]-rows[i,4]))
        if side==0:
            return False
        if p and direction!=side:
            raise RuntimeError("mixed hedge side attempted")
        if not p:
            if state["_campaigns"]:
                state["reentries"]+=1
            state["opens"]+=1
            state["_campaign_open_ms"]=int(t[i])
            state["_campaign_raw"]=0.0
            state["_campaign_fixed"]=0.0
            state["_campaign_spread"]=0.0
            state["_campaign_peak_net"]=-1e99
            state["_reversal_pending"]=False
        else:
            state["adds"]+=1
        direction=side
        price=ask[i] if side>0 else bid[i]
        p.append((amount,price))
        fixed=amount*conv[i]*0.0001
        spread=amount*conv[i]*(ask[i]-bid[i])*0.5
        cost+=fixed
        state["_campaign_fixed"]+=fixed
        state["_campaign_spread"]+=spread
        state["spread_h4"]+=spread
        state["max_hedge"]=max(state["max_hedge"],qty_now())
        state["direction"]=direction
        state["cost_h4"]=cost
        return True

    def monitor(start,stop,row,layers):
        if stop<=start:
            return False
        if not p or direction==0:
            mark(start,stop)
            record_offset(start,stop,row,layers)
            return False
        hf=hedge_float(start,stop)
        q=qty_now()
        close_cost=q*conv[start:stop]*0.0001
        campaign_net=(float(state["_campaign_raw"])-float(state["_campaign_fixed"])
                      +hf-close_cost)
        peak=float(state["_campaign_peak_net"])
        running=np.maximum.accumulate(np.maximum(campaign_net,peak))
        hit=None
        if state["_reversal_pending"]:
            ix=np.flatnonzero(campaign_net>=0.0)
            if len(ix):
                hit=start+int(ix[0])
                reason="reversal_be"
        elif peak>=1.0:
            ix=np.flatnonzero(campaign_net<=0.0)
            if len(ix):
                hit=start+int(ix[0])
                reason="be_floor"
        else:
            ix=np.flatnonzero((running>=1.0)&(campaign_net<=0.0))
            if len(ix):
                hit=start+int(ix[0])
                reason="be_floor"
        if hit is not None:
            mark(start,hit)
            record_offset(start,hit,row,layers)
            close_piece(qty_now(),hit,reason,row,layers)
            mark(hit,stop)
            record_offset(hit,stop,row,layers)
            return True
        mark(start,stop)
        record_offset(start,stop,row,layers)
        state["_campaign_peak_net"]=max(peak,float(np.max(campaign_net)))
        return False

    def acceptable_fill(start,stop):
        ix=np.flatnonzero(ask[start:stop]-bid[start:stop]<=0.00030+1e-10)
        return None if not len(ix) else start+int(ix[0])

    for lo,hi in zip(changes[:-1],changes[1:]):
        if hi<=lo:
            continue
        row=rows[lo]
        net=round(float(row[0]-row[4]),2)
        desired=-int(np.sign(net))
        layers=int(row[2] if net>0 else row[6]) if net!=0 else 0
        if layers>=7:
            state["eligible_sec"]+=float(durations[lo:hi].sum())
        # Core flattening or side change invalidates the current hedge.
        if p and (desired==0 or desired!=direction):
            close_piece(qty_now(),lo,"core_safety",row,layers)
        # A fresh adverse confirmation cancels a pending reversal exit.
        if p and desired!=0 and direction==desired and entry_signal[lo]==direction:
            state["_reversal_pending"]=False
        # Confirmed return toward Tengri: close at net profit, or wait to net BE.
        if p and signal[lo]==-direction:
            if not state["_reversal_pending"]:
                state["exit_pending"]+=1
            state["_reversal_pending"]=True
        elif p and signal[lo]==direction and state["_reversal_pending"]:
            state["_reversal_pending"]=False
        if p and state["_reversal_pending"]:
            monitor(lo,hi,row,layers)
            continue
        # If an active hedge is open, continuously rebalance it to current Tengri lots.
        if p:
            if desired==0:
                monitor(lo,hi,row,layers)
                continue
            if direction!=desired:
                monitor(lo,hi,row,layers)
                continue
            if size_rule=="STAGED":
                factor=1.00 if layers>=10 else (0.75 if layers>=9 else (0.50 if layers>=8 else 0.25))
            else:
                factor=float(size_rule)/100.0
            target=np.floor((abs(net)*factor+1e-10)*100.0)/100.0
            held=qty_now()
            if target+0.005<held:
                close_piece(held-target,lo,"basket_shrank",row,layers)
                held=qty_now()
            if target>held+0.005:
                fill=acceptable_fill(lo,hi)
                if fill is None:
                    state["spread_blocked"]=state.get("spread_blocked",0)+1
                    monitor(lo,hi,row,layers)
                    continue
                closed=monitor(lo,fill,row,layers)
                if not closed and p and not state["_reversal_pending"]:
                    open_piece(target-qty_now(),fill,"dynamic rebalance")
                    monitor(fill,hi,row,layers)
                else:
                    monitor(fill,hi,row,layers)
            else:
                monitor(lo,hi,row,layers)
            continue
        # New campaigns start only on a fresh adverse signal once Tengri reaches layer 7.
        eligible=desired!=0 and layers>=7
        if eligible and entry_signal[lo]==desired:
            if size_rule=="STAGED":
                factor=1.00 if layers>=10 else (0.75 if layers>=9 else (0.50 if layers>=8 else 0.25))
            else:
                factor=float(size_rule)/100.0
            target=np.floor((abs(net)*factor+1e-10)*100.0)/100.0
            fill=acceptable_fill(lo,hi)
            if fill is not None and target>=0.01:
                open_piece(target,fill,"entry signal")
                monitor(fill,hi,row,layers)
            else:
                state["spread_blocked"]=state.get("spread_blocked",0)+1
                mark(lo,hi)
                record_offset(lo,hi,row,layers)
        else:
            monitor(lo,hi,row,layers)

    state.update(direction=direction,realized=realized,cost_h4=cost)
    return f,r,c
'''
needle = 'runner_text = BASE_RUNNER.read_text(encoding="utf-8")'
inject = (needle + "\n_fnstart=runner_text.index('def execute_h4(')\n" +
          "_fnend=runner_text.index('\\nfirst,last=',_fnstart)\n" +
          "runner_text=runner_text[:_fnstart] + " + repr(fn) + " + runner_text[_fnend:]")
if src.count(needle) != 1:
    raise RuntimeError("template runner load anchor mismatch")
src = src.replace(needle, inject, 1)

src = src.replace(
    'variant_names=("ADX25_25","ADX25_REEXIT","RE3_ADX25","RE3_ADX25_REEXIT")',
    'variant_names=("ADX25_STAGE","ADX25_STAGE_REEXIT","RE1_STAGE_REEXIT","RE2_STAGE_REEXIT","RE3_STAGE_REEXIT","RE4_STAGE_REEXIT","RE3_R25_REEXIT","RE3_R50_REEXIT","RE3_R75_REEXIT","RE3_R100_REEXIT")'
)
src = src.replace(
    '("opens","adds","exits","trims","exit_h4","exit_core","max_hedge","cost_h4","spread_h4","covered_sec","eligible_sec","realized")',
    '("opens","adds","exits","trims","exit_h4","exit_bbma_re","exit_core","exit_be","exit_reversal","exit_pending","reentries","max_hedge","cost_h4","spread_h4","covered_sec","eligible_sec","offset_eligible_seconds","offset_positive_seconds","offset_full_seconds","offset_weighted_cover_seconds","offset_max_cover_ratio","offset_exit_samples","offset_full_exits","offset_exit_cover_sum","realized")'
)
src = src.replace(
    'for k in ("exit_h4","exit_bbma_re","exit_core","trims")',
    'for k in ("exit_h4","exit_bbma_re","exit_core","exit_be","exit_reversal","exit_pending","trims")'
)

namespace={"__file__":str(TEMPLATE),"__name__":"__main__"}
exec(compile(src,str(TEMPLATE),"exec"),namespace)