from pathlib import Path
import json,hashlib,struct
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');dataset=Path(r'D:\BBMA\HistoricalData');manifest_path=dataset/'exports/mt4/synthetic_ny_close_v3/MANIFEST.json';profile_path=dataset/'profiles/synthetic_ny_close_test_profile.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig'));profile=json.loads(profile_path.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
for tf in [1,5,15,60,240,1440]:
 entry=next(x for x in manifest['files'] if x['pair']=='GBPUSD' and int(x['period'])==tf);current=r/'history/MetaQuotes-Demo'/('GBPUSD'+str(tf)+'.hst');original=dataset/entry['path'];b=current.read_bytes();records=(len(b)-148)//60
 if hashlib.sha256(b).hexdigest()==entry['sha256']:
  kind='EXACT_SYNTHETIC_V3_EXPORT_SHA_MATCH';payload=True;header=True
 else:
  with original.open('rb') as f:orig_header=f.read(148);f.seek(-records*60,2);tail=f.read()
  payload=b[148:]==tail;header=b[:148]==orig_header;kind='EXACT_SUFFIX_PAYLOAD_OF_SYNTHETIC_V3' if payload else 'NO_EXACT_EXPORT_OR_SUFFIX_BINDING'
 rows.append({'tf':tf,'current_path':str(current),'current_sha256':hashlib.sha256(b).hexdigest(),'source_v3_path':str(original),'source_manifest_sha256':entry['sha256'],'source_records':entry['records'],'current_records':records,'classification':kind,'source_tail_records_equal':payload,'source_header_equal':header})
out={'profile':profile,'profile_sha256':sha(profile_path),'v3_manifest_sha256':sha(manifest_path),'files':rows,'scope':'Byte identity or explicit tail-record identity. No new source download, calendar inference, price repair or broker authentication.'}
e=r/'evidence/sig06_mhv/source_profile_binding_20261111';assert not e.exists();e.mkdir()
(e/'manifest.json').write_text(json.dumps(out,indent=2));print(json.dumps(rows,indent=2),flush=True)
