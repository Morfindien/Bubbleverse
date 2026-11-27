"""V156 intake and bounded coverage inventory. Python 3.10+, mpmath 1.3.0.
python q052_audit_v156.py V155_DIR RAW_DIR RESULT_JSON
"""
from bisect import bisect_right
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json,subprocess,sys

def read(p):return json.loads(p.read_bytes())
def digest(p):return sha256(p.read_bytes()).hexdigest()
def binary(s):return F.from_float(float.fromhex(s))

def main(previous,raw,output):
    assert __debug__
    handoff=read(previous/'Q052_RESULTATINDTAG_OPGAVE_V155.json')
    fp=handoff.pop('fingerprint_sha256')
    canonical=json.dumps(handoff,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    assert sha256(canonical).hexdigest()==fp
    assert handoff['current_q']==handoff['target_q']=='Q052'
    assert handoff['source_state_version']=='V155' and handoff['target_state_version']=='V156'
    for entry in handoff['output_refs']:
        path=previous/entry['path']
        assert digest(path)==entry['sha256'] and path.stat().st_size==entry['size_bytes'],path
    cert=previous/handoff['result_ref']
    C=read(cert)
    assert handoff['result']['signed_uniform']==C['uniform_total_Mpc_inverse']
    assert handoff['result']['signed_relative']==C['uniform_relative']
    bins=C['bins']
    assert len(bins)==256 and all(a['z'][1]==b['z'][0] for a,b in zip(bins,bins[1:]))
    assert bins[0]['z'][0]==C['domain_z'][0] and bins[-1]['z'][1]=='810'
    for field,outer in [('total',C['uniform_total_Mpc_inverse']),('relative',C['uniform_relative'])]:
        lo,hi=map(F,outer)
        assert lo==min(F(b[field][0]) for b in bins)
        assert hi==max(F(b[field][1]) for b in bins)
    assert max(map(abs,map(F,C['uniform_relative'])))<F(5,100000)
    with TemporaryDirectory() as temp,ZipFile(previous/handoff['replay_ref']) as z:
        temp=Path(temp);z.extractall(temp)
        for entry in read(temp/'manifest.json')['entries']:
            p=temp/entry['path']
            assert digest(p)==entry['sha256'] and p.stat().st_size==entry['size_bytes']
        (temp/cert.name).unlink()
        subprocess.run([sys.executable,str(temp/'q052_verify_v155.py')],cwd=temp,check=True,stdout=subprocess.DEVNULL)
        assert (temp/cert.name).read_bytes()==cert.read_bytes()
        with ZipFile(next(temp.glob('*V105.zip'))) as z105:
            result=json.loads(z105.read('result_raw105.json'))
        cell=result['cells'][141]
        energy800=result['energy']
    top=F(C['domain_z'][0]);bottom=F(800)
    assert F(cell['a0'])<1/(1+top)<F(cell['a1'])==1/(1+bottom)
    measured={x['path']:x for x in read(raw/'measured-manifest.json')}
    hashes={}
    def pinned(name):
        p=raw/name;e=measured[name]
        assert p.stat().st_size==e['size'] and digest(p)==e['sha256']
        hashes[name]=e['sha256'];return p
    shared=None;arms={}
    for arm in 'LR':
        name=f'measured/{arm}/background_table_hex.jsonl'
        with pinned(name).open() as src:
            header=json.loads(src.readline())
            assert header['index_bg_H']==1
            table=list(map(json.loads,src))
        # First physical knot below 800 and its predecessor bracket the lower endpoint.
        lower=next(i for i,r in enumerate(table) if binary(r['z'])<=800)
        assert binary(table[lower]['z'])<800<binary(table[lower-1]['z'])
        assert binary(table[31688]['z'])==top
        rows=[{k:r[k] for k in ('i','z','loga')}|{'H':r['background'][1],'H_d2':r['d2background_dloga2'][1]} for r in table[31687:lower+2]]
        if shared is not None:assert shared==rows
        shared=rows
        count={};zs=set();selected=[]
        with pinned(f'measured/{arm}/fullstate_trace.jsonl').open() as src:
            for n,line in enumerate(src,1):
                r=json.loads(line);z=binary(r['z'])
                if bottom<=z<=top:
                    count[r['tag']]=count.get(r['tag'],0)+1
                    zs.add(z)
                    selected.append(dict(line=n,tag=r['tag'],z=r['z'],H=r['pvecback_normal'][1]))
        arms[arm]={'counts':count,'distinct_redshifts':len(zs),'has800':bottom in zs,'has_top':top in zs,'witnesses':selected}
    record={'case':'Q052','version':'V156','V155_sha256':digest(cert),'handoff_sha256':digest(previous/'Q052_RESULTATINDTAG_OPGAVE_V155.json'),'handoff_fingerprint':fp,'point_bound_005_percent_verified':True,'all256_bins_connected_and_hull_verified':True,'clean_replay_byte_match':True,'parent_output_files_verified':len(handoff['output_refs']),'next_domain_z':['800',str(top)],'V105_reference_cell':{'one_based':142,'a0':cell['a0'],'a1':cell['a1'],'entire_proposed_block_covered':True},'V105_energy800':energy800,'native_rows':shared,'row_indices':[r['i'] for r in shared],'lower800_bracket_indices':[lower-1,lower],'archived_samples_in_next_block':arms,'raw_member_hashes':hashes,'next_block_uniform_bound':None,'new_native_runs':0,'new_workflow_dispatches':0}
    output.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    print({k:record[k] for k in ('lower800_bracket_indices','row_indices')})
    print({a:v['counts'] for a,v in arms.items()})

if __name__=='__main__':main(*(Path(x).resolve() for x in sys.argv[1:]))
