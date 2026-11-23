"""Validate Q052 V149 observations and replay the exact operation order for dense output."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import json
import math

FIRST, LAST = 2, 34
ROWS = list(range(FIRST,LAST+1))
HEX_COLS = {'a':0,'H':1,'phi':9,'pi':10}
ROW_NAMES = ('phi','pi')
SHA_V146 = '44ca52f0030fabef0c69484879f1dd1f3bfbb1cca23ec3c681131ebd941bc175'


def number(v):
    f=float.fromhex(v)
    if not math.isfinite(f):
        raise ValueError(f'Nonfinite value {v}')
    return f


def replay_pair(step, row):
    if row['branch']=='direct':
        if number(row['u']) != number(step['hi']) or row['dense_inputs'] is not None:
            raise ValueError('Direct row does not equal the right step coordinate')
        return step['right'][:]
    if row['branch']!='dense':
        raise ValueError('Unknown output branch')
    dense=row['dense_inputs']
    if (dense['row'],dense['accepted_id'],dense['u'])!=(row['row'],step['accepted_id'],row['u']):
        raise ValueError('Dense record does not identify its parent')
    k=step['k']
    dif=dense['dif']
    if len(dif)!=2 or any(len(v)!=k for v in dif):
        raise ValueError('Wrong backward difference dimensions')
    u,left,right,h=map(number,(row['u'],step['lo'],step['hi'],step['h']))
    if not left<u<right:
        raise ValueError('Target is outside the open interpolation interval')
    s=(u-right)/h
    product,factor=1.0,1.0
    weights=[]
    for j in range(k):
        product *= s+j
        factor *= j+1
        weights.append(product/factor)
    values=[]
    for y,coeffs in zip(step['right'],dif,strict=True):
        total=0.0
        for w,d in zip(weights,coeffs,strict=True):
            total += w*number(d)
        values.append((total+number(y)).hex())
    return values


def expected_bytes(evidence):
    raw=evidence.read_bytes()
    if sha256(raw).hexdigest()!=SHA_V146:
        raise ValueError('V146 reference digest mismatch')
    rows={}
    for rec in json.loads(raw)['batch']['common_rows']:
        b=rec['original_utf8'].encode()
        if sha256(b).hexdigest()!=rec['sha256'] or json.loads(b)['i']!=rec['i']:
            raise ValueError('Bad reference row identity')
        rows[rec['i']]=b
    if list(rows)!=ROWS:
        raise ValueError('Reference target rows missing')
    return rows


def first_difference(expected, found):
    for offset,(want,got) in enumerate(zip(expected,found)):
        if want!=got:
            return {'offset':offset,'baseline_byte':want,'observed_byte':got}
    if len(expected)!=len(found):
        i=min(len(expected),len(found))
        return {'offset':i,'baseline_byte':expected[i] if i<len(expected) else None,
                'observed_byte':found[i] if i<len(found) else None}
    return None


def check_records(records, expected_run, arm):
    steps,rows={},{}
    if not records or records[0].get('schema')!='Q052_NDF15_BACKGROUND_STEPS_V149':
        raise ValueError('Missing observer header')
    if (records[0]['run_id'],records[0]['arm'],records[0]['target_rows'])!=(expected_run,arm,[FIRST,LAST]):
        raise ValueError('Observer provenance failure')
    footer=None
    last_step_hi=None
    for event in records[1:]:
        typ=event['type']
        if footer:
            raise ValueError('Unexpected data after footer')
        if typ=='step':
            ident=event['accepted_id']
            lo,hi,h,err,rtol=map(number,(event['lo'],event['hi'],event['h'],event['err_estimate'],event['rtol']))
            if (type(ident) is not int or ident<=max(steps,default=0)
                    or not (lo<hi and hi-lo==h and 0<=err<=rtol and rtol>0)
                    or not 1<=event['k']<=5 or not 2<=event['neq']<=64):
                raise ValueError('Invalid accepted step')
            if last_step_hi is not None and lo < last_step_hi:
                raise ValueError('Accepted output-bearing steps overlap')
            for v in (event['left'],event['right']):
                if len(v)!=2:
                    raise ValueError('Accepted scalar endpoint has wrong size')
                for item in v:
                    number(item)
            steps[ident]=event
            last_step_hi=hi
        elif typ=='row':
            i=event['row']
            if i!=FIRST+len(rows) or i>LAST or event['accepted_id']!=max(steps,default=0):
                raise ValueError('Missing, duplicate or wrong accepted step for row')
            if event['rounding']['mxcsr'] & 0xe040 or event['rounding']['x87_control'] & 0x0c00:
                raise ValueError('Unexpected native rounding mode')
            if event['incoming']!=replay_pair(steps[event['accepted_id']],event):
                raise ValueError(f'Binary64 interpolation replay differs at row {i}')
            stored=event['stored']
            if set(stored)!=set(HEX_COLS) or min(number(stored[k]) for k in ('a','H'))<=0:
                raise ValueError('Bad stored fields')
            if [stored[k] for k in ROW_NAMES]!=event['incoming']:
                raise ValueError('Observer scalar row mismatch')
            rows[i]=event
        elif typ=='finish':
            footer=event
        else:
            raise ValueError('Unknown record type')
    if list(rows)!=ROWS or not footer or footer.get('status')!='COMPLETE' or footer.get('issues'):
        missing=next((i for i in ROWS if i not in rows),None)
        raise ValueError(f'Incomplete observation, first missing row {missing}, footer {footer}')
    if footer['rows']!=ROWS or footer['steps']!=len(steps) or set(steps)!={r['accepted_id'] for r in rows.values()}:
        raise ValueError('Footer/observation coverage mismatch')
    return rows,steps


def compare_arm(folder, run_id, arm, reference):
    records=[json.loads(x) for x in (folder/'ndf15_steps_v149.jsonl').read_bytes().splitlines()]
    rows,steps=check_records(records,run_id,arm)
    mismatch=None
    with (folder/'background_table_hex.jsonl').open('rb') as f:
        header=json.loads(f.readline())
        if header['arm']!=arm or header['run_id']!=run_id or header['bt_size']!=40000:
            raise ValueError('Wrong archived native table identity')
        for i in range(LAST+1):
            raw=f.readline()
            if i<FIRST:
                continue
            measured=json.loads(raw)
            record=rows[i]
            if measured['i']!=i or float.fromhex(measured['loga']).hex()!=record['u']:
                raise ValueError(f'Observer vs exported coordinate mismatch at row {i}')
            for name,col in HEX_COLS.items():
                if number(measured['background'][col]).hex()!=record['stored'][name]:
                    raise ValueError(f'Observer vs exported field mismatch at row {i}, {name}')
            if mismatch is None:
                diff=first_difference(reference[i],raw)
                if diff: mismatch={'row':i,**diff}
    return {'rows':len(rows),'steps':len(steps),'first_step':min(steps),'last_step':max(steps),
            'dense_rows':sum(x['branch']=='dense' for x in rows.values()),
            'first_target_row_byte_divergence_vs_V141':mismatch}


def main():
    p=ArgumentParser(description=__doc__)
    p.add_argument('measured',type=Path)
    p.add_argument('reference',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--run-id',required=True)
    a=p.parse_args()
    baseline=expected_bytes(a.reference)
    results={}
    for arm in 'LR':
        try:
            results[arm]={'status':'PASS',**compare_arm(a.measured/arm,a.run_id,arm,baseline)}
        except (OSError,ValueError,KeyError,TypeError,IndexError) as error:
            results[arm]={'status':'INCOMPLETE_OR_REPLAY_MISMATCH','detail':str(error)}
    # V141 launcher already records original history/public/background-body hashes.
    prior=a.measured/'result.json'
    overlap=json.loads(prior.read_bytes()).get('overlap',{}) if prior.is_file() else {}
    passes=all(x['status']=='PASS' for x in results.values())
    identical=passes and all(x['first_target_row_byte_divergence_vs_V141'] is None for x in results.values())
    complete_overlap=set(overlap)=={'L','R'} and all(set(q)=={'history.csv','public_table_hex.jsonl','background_body'} and all(q.values()) for q in overlap.values())
    status='TARGETS_AND_HISTORICAL_EXPORTS_MATCH' if identical and complete_overlap else 'TARGETS_CAPTURED_HISTORICAL_DIVERGENCE_OR_UNVERIFIED' if passes else 'INCOMPLETE_OR_REPLAY_MISMATCH'
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps({'run_id':a.run_id,'status':status,'arms':results,
                                    'historic_overlap_digest_checks':overlap},indent=2)+'\n')
    return 0 if passes else 1

if __name__=='__main__':
    raise SystemExit(main())
