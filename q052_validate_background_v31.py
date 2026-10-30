#!/usr/bin/env python3
"""Independent C-expression and Decimal checks of the V31 certificate.

Usage: python q052_validate_background_v31.py V30.zip RECEIPT.json
The adjacent pinned C source is compiled locally; this is not a native CLASS run.
"""
import ctypes as C, decimal, hashlib, json, math, platform, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from fractions import Fraction as Q
import q052_background_transfer_v31 as m

root=Path(__file__).resolve().parent
zf=zipfile.ZipFile(sys.argv[1]);receipt=json.loads(Path(sys.argv[2]).read_text())
raw=zf.read(m.PREFIX+'background_table_hex.jsonl');assert m.sha(raw)==m.TABLE_SHA
selected={}
for line in raw.splitlines()[1:]:
    d=json.loads(line)
    if d['i'] in (31687,31688,31689):selected[d['i']]=d
cc=shutil.which('gcc') or shutil.which('clang');assert cc
source=root/'q052_spline_kernel_pinned_v31.c'
count=0;max_error=Q(0);decimal_checks=0
with tempfile.TemporaryDirectory() as tmp:
    so=Path(tmp)/'kernel.so'
    command=[cc,'-O2','-std=c99','-shared','-fPIC','-fno-fast-math','-ffp-contract=off',str(source),'-o',str(so)]
    subprocess.run(command,check=True,capture_output=True)
    lib=C.CDLL(str(so));fun=lib.array_interpolate_spline;D=C.POINTER(C.c_double)
    fun.argtypes=[D,C.c_int,D,D,C.c_int,C.c_double,C.POINTER(C.c_int),D,C.c_int,C.c_char_p]
    fun.restype=C.c_int
    for seg in receipt['segments']:
        a,b=selected[seg['left_row']],selected[seg['right_row']]
        x0,x1=map(float.fromhex,[a['loga'],b['loga']])
        xa=(C.c_double*2)(x0,x1)
        ys=(C.c_double*64)(*[float.fromhex(v) for row in [a,b] for v in row['background']])
        ms=(C.c_double*64)(*[float.fromhex(v) for row in [a,b] for v in row['d2background_dloga2']])
        xx=[x0,x1,math.nextafter(x0,x1),math.nextafter(x1,x0)]
        xx += [x0+(x1-x0)*j/32 for j in range(1,32)]
        for x in xx:
            last=C.c_int();result=(C.c_double*32)();err=C.create_string_buffer(2048)
            assert fun(xa,2,ys,ms,32,x,C.byref(last),result,32,err)==0
            assert last.value==0
            t=(Q(x)-Q(x0))/(Q(x1)-Q(x0));aa=1-t;h=Q(x1)-Q(x0)
            for j in range(32):
                y0,y1=m.fq(a['background'][j]),m.fq(b['background'][j])
                m0,m1=m.fq(a['d2background_dloga2'][j]),m.fq(b['d2background_dloga2'][j])
                exact=aa*y0+t*y1+((aa**3-aa)*m0+(t**3-t)*m1)*h*h/6
                error=abs(Q(result[j])-exact);max_error=max(max_error,error)
                allowed=m.fq(seg['columns'][j]['fp_arithmetic_abs_error_upper']['hex'][1])
                assert error<=allowed,(seg['left_row'],j,x,error,allowed)
                count+=1
    # Decimal supplies an independent high-precision diagnostic for transcendentals.
    # The directed MPFR enclosure remains the proof-producing backend.
    with decimal.localcontext() as ctx:
        ctx.prec=100
        for x in (811.0,1.0+m.Z_LO):
            value=decimal.Decimal.from_float(x).ln()
            lo=m.directed_transcendental('log',x,False);hi=m.directed_transcendental('log',x,True)
            cv=lambda q:decimal.Decimal(q.numerator)/decimal.Decimal(q.denominator)
            assert cv(lo)<value<cv(hi);decimal_checks+=1
        identity=json.loads(zf.read(m.PREFIX+'effective_identity.json'))['fields']
        rho0=m.fq(identity['H0'])**2*m.fq(identity['Omega0_g'])
        allowed=m.fq(receipt['reference_photon_error_to_analytic_target']['hex'][1])
        for seg in receipt['segments']:
            a,b=selected[seg['left_row']],selected[seg['right_row']]
            x0,x1=m.fq(a['loga']),m.fq(b['loga']);h=x1-x0
            for k in range(17):
                t=Q(k,16);x=x0+h*t;c=m.spline(a,b,3)
                discrepancy=abs(cv(m.poly_value(c,t))-cv(rho0)*(-4*cv(x)).exp())
                assert discrepancy<=cv(allowed);decimal_checks+=1
out={'schema':'Q052_BACKGROUND_TRANSFER_VALIDATION_V31','status':'PASS',
 'C_comparisons_against_exact_rational_reference':count,
 'C_max_sampled_absolute_error_all_columns':m.bound(0,max_error),
 'Decimal100_transcendental_and_photon_checks':decimal_checks,
 'compiler':subprocess.check_output([cc,'--version'],text=True).splitlines()[0],
 'compile_flags':command[1:7],'C_source_sha256':m.sha(source.read_bytes()),
 'receipt_sha256':m.sha(Path(sys.argv[2]).read_bytes()),
 'validation_program_sha256':m.sha(Path(__file__).read_bytes()),
 'scope':'Finite independent C/Decimal checks support implementation correctness; exact interval/rational derivation supplies whole-interval bounds. Not the historical classy.so execution.'}
(root/'Q052_BACKGROUND_TRANSFER_VALIDATION_V31.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
