"""Synthetic direct/dense tests. Calls no CLASS solver or nominal experiment."""
import argparse
import ctypes as C
from pathlib import Path
import re
import subprocess
import tempfile

from q052_validate_v149 import ROWS, check_records, first_difference, replay_pair

def inputs():
    run_id='Q052-V149-SIMPLE-FIXTURE'
    start=-32.0
    steps=[]
    events=[{'type':'header','schema':'Q052_NDF15_BACKGROUND_STEPS_V149','run_id':run_id,'arm':'L','target_rows':[2,34]}]
    for seq,i in enumerate(ROWS,1):
        lo=start+(seq-1)/1024
        hi=start+seq/1024
        order=1+i%5
        a=[3.0,2.3e-27]
        b=[3.1,2.1e-27]
        dif=[[(-1)**j*0.013/(j+1) for j in range(order)],
             [(-1)**j*0.0001e-27/(j+1) for j in range(order)]]
        base={'type':'step','accepted_id':3*seq,'lo':lo.hex(),'hi':hi.hex(),'h':(hi-lo).hex(),
              'k':order,'neq':2,'err_estimate':float(1e-12).hex(),'rtol':float(1e-10).hex(),
              'left':list(map(float.hex,a)),'right':list(map(float.hex,b))}
        spot=hi if i%2==0 else hi-(hi-lo)*0.375
        r={'type':'row','row':i,'u':spot.hex(),'accepted_id':3*seq,
           'branch':'direct' if i%2==0 else 'dense','dense_inputs':None,
           'rounding':{'mxcsr':0x1f80,'x87_control':0x037f}}
        if i%2:
            r['dense_inputs']={'dif':[list(map(float.hex,d)) for d in dif],'row':i,'accepted_id':3*seq,'u':spot.hex()}
        steps.append((base,r))
    return run_id,events,steps


def interp_source(cls):
    src=(cls/'tools/evolver_ndf15.c').read_text()
    start=src.index('\nint interp_from_dif(double tinterp,')
    stop=src.index('\nint adjust_stepsize(',start)
    return '#define _TRUE_ 1\n#define _SUCCESS_ 0\n'+src[start:stop]


def compiled_refs(func, step, row):
    vec=C.c_double*3
    ptr=C.POINTER(C.c_double)
    y=vec(0,*(float.fromhex(x) for x in step['right']))
    out,dout,unused=vec(),vec(),vec()
    differences=[(C.c_double*(step['k']+1))(0,*(float.fromhex(x) for x in d)) for d in row['dense_inputs']['dif']]
    dif=(ptr*3)(ptr(),*differences)
    mask=(C.c_int*3)(0,1,1)
    assert func(float.fromhex(row['u']),float.fromhex(step['hi']),y,float.fromhex(step['h']),dif,step['k'],
                out,dout,unused,mask,2,2)==0
    return [out[i].hex() for i in (1,2)]


def run(cls):
    run_id,events,steps=inputs()
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        c=tmp/'interp.c'
        lib=tmp/'interp.so'
        c.write_text(interp_source(cls))
        subprocess.run(['gcc','-O2','-fno-fast-math','-ffp-contract=off','-frounding-math','-shared','-fPIC',str(c),'-o',str(lib)],check=True)
        func=C.CDLL(str(lib)).interp_from_dif
        ptr=C.POINTER(C.c_double)
        func.argtypes=[C.c_double,C.c_double,ptr,C.c_double,C.POINTER(ptr),C.c_int,
                       ptr,ptr,ptr,C.POINTER(C.c_int),C.c_int,C.c_int]
        func.restype=C.c_int
        tested=set()
        for step,row in steps:
            expected=step['right'] if row['branch']=='direct' else compiled_refs(func,step,row)
            if row['branch']=='dense':
                tested.add(step['k'])
            assert replay_pair(step,row)==expected
            row['incoming']=expected
            row['stored']={'a':float(1e-14).hex(),'H':float(1e22).hex(),'phi':expected[0],'pi':expected[1]}
            events.extend([step,row])
    assert tested==set(range(1,6))
    footer={'type':'finish','status':'COMPLETE','rows':ROWS,'steps':33,'issues':[]}
    events.append(footer)
    assert len(check_records(events,run_id,'L')[0])==33
    for case in (events[:-2],events[:3]+events[5:],events[:-1]+[{**footer,'steps':1}]):
        try:
            check_records(case,run_id,'L')
        except ValueError:
            pass
        else:
            raise AssertionError('A malformed observation was accepted')
    assert first_difference(b'abc',b'axc')=={'offset':1,'baseline_byte':98,'observed_byte':120}
    assert first_difference(b'x',b'xx')=={'offset':1,'baseline_byte':None,'observed_byte':120}
    assert first_difference(b'x',b'x') is None
    print('PASS: 33 synthetic rows, direct and dense, C replay orders 1–5, three incomplete stream cases, byte comparison')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('class_source',type=Path)
    run(p.parse_args().class_source)
