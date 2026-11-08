"""Isolated tester OHLC fixture only. No ticks, gap filling or coverage certification.
Create absent GBPUSD30.hst from complete 30-M1-bar buckets in existing GBPUSD1.hst.
"""
from pathlib import Path
import argparse,struct,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args()
root=a.root;src=root/'history/MetaQuotes-Demo/GBPUSD1.hst';dst=src.with_name('GBPUSD30.hst')
assert not dst.exists(), 'Never replace existing history'
b=src.read_bytes();assert struct.unpack_from('<i',b)[0]==401
assert b[68:80].split(b'\0')[0]==b'GBPUSD' and struct.unpack_from('<i',b,80)[0]==1
fmt=struct.Struct('<qddddqiq');assert (len(b)-148)%fmt.size==0
buckets={}
for row in fmt.iter_unpack(b[148:]):
 t=row[0];key=t-t%1800;buckets.setdefault(key,[]).append(row)
rows=[];skipped=0
for key,group in sorted(buckets.items()):
 group.sort(key=lambda r:r[0])
 if [r[0] for r in group]!=list(range(key,key+1800,60)):
  skipped+=1;continue
 rows.append((key,group[0][1],max(r[2] for r in group),min(r[3] for r in group),group[-1][4],sum(r[5] for r in group),max(r[6] for r in group),sum(r[7] for r in group)))
assert len(rows)>100
header=bytearray(b[:148]);struct.pack_into('<i',header,80,30)
result=bytes(header)+b''.join(fmt.pack(*row) for row in rows)
dst.write_bytes(result)
manifest={'scope':'derived OHLC test fixture; no synthesized ticks, filled missing bars, coverage or profitability claim','source':str(src),'source_sha256':hashlib.sha256(b).hexdigest(),'output':str(dst),'output_sha256':hashlib.sha256(result).hexdigest(),'complete_buckets':len(rows),'incomplete_buckets_omitted':skipped,'first':rows[0][0],'last':rows[-1][0]}
e=root/'evidence/custom598_producer';e.mkdir(parents=True,exist_ok=True);(e/'m30_fixture.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest),flush=True)
