"""Read-only GDB observer for the pinned CLASS library. Load after V141's startup probe."""
import gdb
import json
import math
import os
from pathlib import Path

# Reuse base, record, final_call, ptr, scalar, field, rounding and value from observe.py.
FIRST = 2
LAST = 34
sites = {'accept': 0x1ade2, 'dense': 0x1aee9, 'emit': 0x67f20, 'row': 0x67fc3}
return_branches = {0x1ae51: 'direct', 0x1af24: 'dense'}

def reg_int(name):
    return int(value('$' + name))

def xmm(name):
    return float(value(f'${name}.v2_double[0]'))

def stack(offset, kind):
    return value(f'*({kind}*)($rsp+{offset})')

def state_pair(pba, vec, length):
    if not int(vec):
        raise ValueError('Null scalar integration vector')
    indices = [int(field(pba, 'index_bi_' + name)) for name in ('phi_scf', 'phi_prime_scf')]
    if len(set(indices)) != 2 or not all(0 <= i < length for i in indices):
        raise ValueError('Scalar integration indices outside active state')
    return [finite_hex(vec[i]) for i in indices]

def finite_hex(v):
    number = float(v)
    if not math.isfinite(number):
        raise ValueError('Non-finite measurement')
    return number.hex()


class StepObserver:
    def __init__(self):
        self.ordinal = 0
        self.last_hi = None
        self.current = None
        self.dense = None
        self.pending = None
        self.rows = []
        self.steps = {}
        self.errors = []
        self.pba = None
        self.active = False
        self.path = Path(os.environ['Q052_NATIVE_OUT']) / 'ndf15_steps_v149.jsonl'
        self.log = self.path.open('x', encoding='utf-8', buffering=1)
        self.write({'type':'header', 'schema':'Q052_NDF15_BACKGROUND_STEPS_V149',
                    'run_id':record['run_id'], 'arm':record['arm'],
                    'accepted_ordinal_origin':'1-based, every successful step in final background invocation',
                    'target_rows':[FIRST,LAST]})
        self.probes = [StepProbe(self, name, offset) for name,offset in sites.items()]

    def write(self, data):
        self.log.write(json.dumps(data, allow_nan=False, sort_keys=True) + '\n')
        self.log.flush()

    def eligible(self):
        return (int(stack(0x178,'unsigned long')) == base + sites['emit']
                and int(stack(0x60,'unsigned long')) == base + 0x67a50)

    def accepted(self):
        if not self.eligible():
            return
        if not self.active:
            if not final_call():
                return
            self.active = True
        workspace = ptr(stack_expr(0x58),'struct background_parameters_and_workspace')
        pba = field(workspace,'pba')
        if self.pba is None:
            self.pba = int(pba)
        if self.pba != int(pba):
            raise ValueError('Background instance changed')
        self.ordinal += 1
        following_grid = reg_int('r12d')
        self.current = None
        if not 0 <= following_grid <= int(field(pba,'bt_size')):
            raise ValueError('Out-of-range next background row')
        if following_grid > LAST:
            self.finish('INCOMPLETE')
            return
        lo,hi,h = (float(stack(i,'double')) for i in (0xc0,0x40,0xb8))
        if not (math.isfinite(lo) and math.isfinite(hi) and lo < hi and (self.last_hi is None or self.last_hi == lo)):
            raise ValueError('Accepted step is not contiguous with its predecessor')
        self.last_hi=hi
        if hi < float(field(pba,'loga_table')[max(FIRST,following_grid)]):
            return
        k,neq = reg_int('r13d'), int(stack(0x08,'int'))
        err,rtol = xmm('xmm5'),float(stack(0x98,'double'))
        if not (math.isfinite(lo) and math.isfinite(hi) and lo < hi and hi-lo == h
                and 1 <= k <= 5 and 2 <= neq <= 64 and neq == int(field(pba,'bi_size'))
                and 0 <= err <= rtol and math.isfinite(rtol) and rtol > 0):
            raise ValueError(f'Accepted-step register invariant failed at next row {following_grid}')
        y = ptr(stack_expr(0xa8),'double')
        ynew = ptr('$r15','double')
        if not int(y):
            raise ValueError('Null one-based accepted-left vector')
        self.current = {'type':'step','accepted_id':self.ordinal,'lo':finite_hex(lo),'hi':finite_hex(hi),
                        'h':finite_hex(h),'k':k,'neq':neq,'err_estimate':finite_hex(err),'rtol':finite_hex(rtol),
                        'left':state_pair(pba,y+1,neq),'right':state_pair(pba,ynew,neq)}

    def interpolation(self):
        # At the call instruction rsp already includes three pushed arguments and alignment.
        if self.current is None or not self.active:
            return
        i=reg_int('ebp')
        if not FIRST <= i <= LAST:
            return
        if self.dense is not None or self.pending is not None:
            raise ValueError('Unconsumed interpolation record')
        pba=ptr(hex(self.pba),'struct background')
        k=reg_int('edx')
        arg_neq=int(stack(8,'int'))
        step=self.current
        if (k != step['k'] or arg_neq != step['neq'] or int(stack(16,'int')) != 2
                or finite_hex(xmm('xmm1')) != step['hi'] or finite_hex(xmm('xmm2')) != step['h']):
            raise ValueError('NDF15 interpolation arguments differ from accepted step')
        incoming=xmm('xmm0')
        if not float.fromhex(step['lo']) < incoming < float.fromhex(step['hi']):
            raise ValueError('Dense output coordinate outside accepted step interior')
        mask=stack(0,'int*')
        differences=value('(double **)$rsi')
        right=value('(double *)$rdi')
        if not all(map(int,(mask,differences,right))):
            raise ValueError('Null interpolation argument')
        if state_pair(pba,right+1,arg_neq)!=step['right']:
            raise ValueError('Dense right-state pointer differs from accepted right state')
        dif=[]
        for name in ('phi_scf','phi_prime_scf'):
            ii=int(field(pba,'index_bi_'+name))+1
            if int(mask[ii])!=1 or not int(differences[ii]):
                raise ValueError(f'Unselected scalar component {name}')
            dif.append([finite_hex(differences[ii][j]) for j in range(1,k+1)])
        self.dense={'row':i,'accepted_id':step['accepted_id'],'u':finite_hex(incoming),'dif':dif}

    def emitted_state(self):
        if not self.active or self.current is None:
            return
        i=reg_int('edx')
        if not FIRST <= i <= LAST:
            return
        callback_workspace=ptr('$rcx','struct background_parameters_and_workspace')
        pba=field(callback_workspace,'pba')
        if self.pba!=int(pba) or self.pending is not None:
            raise ValueError('Unexpected background output invocation')
        branch=return_branches.get(int(stack(0,'unsigned long'))-base)
        if not branch or i != FIRST+len(self.rows):
            raise ValueError(f'Unexpected output branch or row ordering at {i}')
        u=finite_hex(xmm('xmm0'))
        if u != finite_hex(field(pba,'loga_table')[i]):
            raise ValueError('Callback and output grid coordinates differ')
        step=self.current
        if branch=='dense':
            if not self.dense or (self.dense['row'],self.dense['accepted_id'],self.dense['u'])!=(i,step['accepted_id'],u):
                raise ValueError('Output has no matching dense input')
        elif self.dense is not None or u!=step['hi']:
            raise ValueError('Invalid direct output coordinate')
        pair=state_pair(pba,ptr('$rdi','double'),step['neq'])
        if branch=='direct' and pair!=step['right']:
            raise ValueError('Direct output differs from accepted endpoint')
        modes=rounding()
        if modes['mxcsr'] & 0x8040:
            raise ValueError('Flush-to-zero or denormals-are-zero enabled')
        self.pending={'type':'row','row':i,'u':u,'accepted_id':step['accepted_id'],
                      'branch':branch,'incoming':pair,'dense_inputs':self.dense,
                      'rounding':modes}
        self.dense=None

    def stored_row(self):
        if self.pending is None:
            return
        if reg_int('eax')!=0 or reg_int('rbx')!=self.pending['row'] or reg_int('rbp')!=self.pba:
            raise ValueError('background_functions failed or returned unexpected row')
        pba=ptr('$rbp','struct background')
        n=int(field(pba,'bg_size'))
        vec=ptr('$r12','double')
        names={'a':'index_bg_a','H':'index_bg_H','phi':'index_bg_phi_scf','pi':'index_bg_phi_prime_scf'}
        indices={name:int(field(pba,key)) for name,key in names.items()}
        if n!=32 or not int(vec) or indices!={'a':0,'H':1,'phi':9,'pi':10}:
            raise ValueError('Unexpected background row layout')
        expected=field(pba,'background_table')+n*self.pending['row']
        if int(vec)!=int(expected):
            raise ValueError('Unexpected row data pointer')
        self.pending['stored']={name:finite_hex(vec[i]) for name,i in indices.items()}
        if [self.pending['stored'][k] for k in ('phi','pi')]!=self.pending['incoming']:
            raise ValueError('Stored scalar pair differs from callback input')
        ident=self.current['accepted_id']
        if ident not in self.steps:
            self.steps[ident]=self.current
            self.write(self.current)
        self.write(self.pending)
        self.rows.append(self.pending['row'])
        self.pending=None
        if self.rows[-1]==LAST:
            self.finish('COMPLETE')

    def finish(self,status):
        if self.log.closed:
            return
        self.write({'type':'finish','status':status,'rows':self.rows,'steps':len(self.steps),
                    'first_missing':next((i for i in range(FIRST,LAST+1) if i not in self.rows),None),
                    'issues':self.errors})
        self.log.close()
        for b in self.probes:
            b.enabled=False


def stack_expr(offset):
    return f'*(void**)($rsp+{offset})'


class StepProbe(gdb.Breakpoint):
    def __init__(self, observer, name, offset):
        super().__init__(f'*{base+offset:#x}',type=gdb.BP_HARDWARE_BREAKPOINT,internal=True)
        self.observer=observer
        self.name=name

    def stop(self):
        try:
            action={'accept':self.observer.accepted,'dense':self.observer.interpolation,
                    'emit':self.observer.emitted_state,'row':self.observer.stored_row}
            action[self.name]()
        except Exception as exc:
            self.observer.errors.append({'site':self.name,'message':str(exc)})
            self.observer.finish('INCOMPLETE')
        return False


observer149=StepObserver()
