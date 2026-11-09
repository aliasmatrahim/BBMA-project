"""Read-only HST401 gap inventory; source timestamps do not authenticate broker sessions."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, struct

p=argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--symbol', required=True)
p.add_argument('--before', required=True, help='Source/chart date YYYY-MM-DD')
p.add_argument('--after', required=True, help='Source/chart date YYYY-MM-DD')
p.add_argument('--derived-tf30', action='store_true')
p.add_argument('--output', type=Path, required=True)
a=p.parse_args()
# UTC is a reproducible conversion convention for raw HST integers, not a broker-offset claim.
cut1=int(datetime.strptime(a.before,'%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
cut2=int(datetime.strptime(a.after,'%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
assert cut2>cut1
rows=[]
for tf in [1,5,15,30,60,240,1440]:
    path=a.root/'history/MetaQuotes-Demo'/(a.symbol+str(tf)+'.hst')
    raw=path.read_bytes()
    assert struct.unpack_from('<i',raw)[0]==401 and struct.unpack_from('<i',raw,80)[0]==tf
    times=[r[0] for r in struct.iter_unpack('<qddddqiq',raw[148:])]
    before=max(t for t in times if t<cut1)
    after=min(t for t in times if t>=cut2)
    label=lambda value: datetime.fromtimestamp(value,timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    rows.append({'tf_minutes':tf,'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),
                 'period_header':tf,'last_before_gap_source_time':label(before),
                 'first_after_gap_source_time':label(after),'before_raw_hst_time':before,
                 'after_raw_hst_time':after,'nominal_seconds':tf*60,'observed_delta_seconds':after-before,
                 'source_kind':'derived complete-bucket OHLC fixture' if tf==30 and a.derived_tf30 else 'installed broker-format HST; historical session provenance not established'})
manifest={'task':'T04-B','status':'HOLD','symbol':a.symbol,
          'scope':'read-only installed HST inventory; labels are source/chart time, not authenticated UTC broker sessions',
          'date_window':[a.before,a.after],'historical_broker_session_metadata':'not established by this inventory',
          'cold_start_owner_epoch_proof':'not established by this inventory',
          'ruling':'HST timestamps prove observed source bars, not that missing intervals were closed sessions; no fill/skip or fresh-trigger authority',
          'rows':rows}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':manifest['status'],'periods':len(rows),'output':str(a.output)}),flush=True)
