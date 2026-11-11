from pathlib import Path
import struct,json,hashlib,csv,datetime
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');e=r/'evidence/sig06_mhv/m30_derivation_audit_20261111';assert not e.exists();e.mkdir(parents=True)
fmt=struct.Struct('<qddddqiq');hist=r/'history/MetaQuotes-Demo';data={};meta={}
inputs=r/'evidence/sig06_mhv/origin_inventory_v1/sig06_mhv_origin_inputs_v1_20261111.csv'
with inputs.open() as f:seen=[x for x in csv.DictReader(f,delimiter=';') if x['tf']=='30']
lo=min(int(x['time']) for x in seen);hi=max(int(x['time']) for x in seen)
for tf in [1,5,15,30,60,240,1440]:
 p=hist/('GBPUSD'+str(tf)+'.hst');b=p.read_bytes();assert struct.unpack_from('<i',b)[0]==401
 data[tf]={x[0]:x for x in fmt.iter_unpack(b[148:]) if lo<=x[0]<hi+1800};meta[str(tf)]={'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'records':(len(b)-148)//fmt.size}
inputs=r/'evidence/sig06_mhv/origin_inventory_v1/sig06_mhv_origin_inputs_v1_20261111.csv'
with inputs.open() as f:seen=[x for x in csv.DictReader(f,delimiter=';') if x['tf']=='30']
lo=min(int(x['time']) for x in seen);hi=max(int(x['time']) for x in seen);missing=[];comparisons=0;different=[]
for t in range(lo,hi+1,1800):
 if t not in data[30]:
  mins=[s for s in range(t,t+1800,60) if s in data[1]];m15=[s for s in [t,t+900] if s in data[15]]
  if mins or m15:missing.append({'chart_epoch':t,'chart_label':datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),'M1_count':len(mins),'missing_M1_offsets':[s-t for s in range(t,t+1800,60) if s not in data[1]],'M15_count':len(m15),'M5_count':sum(s in data[5] for s in range(t,t+1800,300)),'classification':'DERIVATION_OMISSION_FROM_INCOMPLETE_M1_BUCKET_NOT_SESSION_PROOF'})
 elif t in data[15] and t+900 in data[15]:
  a=data[15][t];b=data[15][t+900];ohlc=(a[1],max(a[2],b[2]),min(a[3],b[3]),b[4]);old=data[30][t][1:5];comparisons+=1
  if any(abs(x-y)>1e-9 for x,y in zip(ohlc,old)):different.append({'time':t,'M1_derived':old,'M15_derived':ohlc,'max_difference':max(abs(x-y) for x,y in zip(ohlc,old))})
summary={'source_files':meta,'window_chart_epoch':[lo,hi],'missing_active_source_buckets':len(missing),'omitted_with_two_native_M15_bars':sum(x['M15_count']==2 for x in missing),'omitted_with_incomplete_M1':sum(x['M1_count']<30 for x in missing),'overlap_comparisons':comparisons,'overlap_OHLC_differences':len(different),'missing_buckets':missing,'differences_first20':different[:20],'scope':'Read-only comparison of existing same-terminal HST. Complete M15 aggregation is an alternate engineering fixture only; native M15 identity does not certify per-minute ticks/coverage or authenticate sessions.'}
(e/'manifest.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k not in ['source_files','missing_buckets','differences_first20']},indent=2));print(json.dumps(missing[:3],indent=2));print(json.dumps(different[:3],indent=2))
