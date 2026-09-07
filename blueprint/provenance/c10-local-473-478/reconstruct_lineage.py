#!/usr/bin/env python3
from pathlib import Path
import base64,gzip,hashlib,json,sys

def sha256(b): return hashlib.sha256(b).hexdigest().upper()
def decode_b64_gzip(path): return gzip.decompress(base64.b64decode(Path(path).read_text(encoding='ascii')))
def apply_patch(old, patch_raw):
    p=json.loads(patch_raw.decode('utf-8'))
    if p.get('format')!='BBMA-LINE-PATCH-v1': raise RuntimeError('unsupported patch format')
    if sha256(old)!=p['from_sha256']: raise RuntimeError(f"from hash mismatch {p['from_build']}")
    lines=old.splitlines(keepends=True); out=[]
    for op in p['ops']:
        tag=op[0]
        if tag=='=': out.extend(lines[op[1]:op[2]])
        elif tag=='-': pass
        elif tag in ('insert','replace'): out.append(base64.b64decode(op[3]))
        else: raise RuntimeError(f'unknown op {tag}')
    new=b''.join(out)
    if sha256(new)!=p['to_sha256']: raise RuntimeError(f"to hash mismatch {p['to_build']}")
    return new,p

def main():
    here=Path(__file__).resolve().parent
    cur=decode_b64_gzip(here/'NATIVE_BUILD472_BASE.mq4.gz.b64')
    expected='0F461312D7D26D724C9738EDDF88F1A226148F01EAE894CE52D942E963F31E99'
    if sha256(cur)!=expected: raise RuntimeError('Build 4.72 base hash mismatch')
    outdir=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else here/'reconstructed'
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/'BBMA_EA_BUILD472.mq4').write_bytes(cur)
    for n in range(72,78):
        raw=decode_b64_gzip(here/f'PATCH_{n}_TO_{n+1}.json.gz.b64')
        cur,p=apply_patch(cur,raw)
        (outdir/f'BBMA_EA_BUILD4{n+1}.mq4').write_bytes(cur)
        print(f"{p['to_build']} {sha256(cur)}")
if __name__=='__main__': main()
