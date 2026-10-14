"""Execute the frozen Q048 P3 V2 changed-arithmetic operator admission."""
from q048_p3_scaled_kernel_v2 import *
from q048_p3_scaled_arithmetic_v2 import (
    table_log_union, primary_exp_point, control_exp_point,
    scaled_mul, scaled_recip, unit_scaled, encode_scaled
)
import time, datetime, traceback, platform, sys, json, hashlib
from pathlib import Path

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    cfg=json.loads((HERE/'q048_p3_scaled_config_v2.json').read_text())
    verify_inputs(cfg)
    result={
      'schema':'bubbleverse.builder.local_result','schema_version':'UNVALIDATED_LOCAL_CONTRACT',
      'result_id':cfg['result_id'],'task_id':cfg['task_id'],'candidate_id':cfg['candidate_id'],
      'scope':'BOUNDED_CONDITIONAL_SOURCE_REAL_P3_OPERATOR_ADMISSION_V2',
      'question_sha256':cfg['question_sha256'],
      'config_sha256':digest(HERE/'q048_p3_scaled_config_v2.json'),
      'spec_sha256':digest(HERE/'Q048_P3_SCALED_FROZEN_SPEC_V2.md'),
      'module_sha256':digest(HERE/'q048_p3_scaled_kernel_v2.py'),
      'arithmetic_sha256':digest(HERE/'q048_p3_scaled_arithmetic_v2.py'),
      'driver_sha256':digest(Path(__file__)),
      'start_utc':utc(),'python':platform.python_version(),'platform':platform.platform(),
      'native_P6':'UNRESOLVED','x_e_tau_T_first_event':'UNRESOLVED',
      'proofcells':0,'table_node_transforms':0,'checks':[]
    }
    start=time.monotonic()
    def guard():
        if time.monotonic()-start>cfg['budget_seconds']:raise TimeoutError('PROOF_COMPUTE_CAP')
        if result['proofcells']>cfg['budget_proofcells']:raise ValueError('PROOFCELL_CAP')
    def check(name,ok,evidence=None):
        result['checks'].append({'name':name,'pass':bool(ok),'evidence':encode(evidence) if evidence is not None else None})
        if not ok: raise ValueError('FAIL_FAST:'+name)
        guard()
    try:
        norm=norm_certificate(); result['norm_certificate']=norm; result['proofcells']+=15
        check('exact_Lagrange_source_polynomial_identity',basis_polynomials()==lagrange_polynomials())
        check('signed_primary_whole_domain_norm_2',norm['primary_norm']==2)
        check('separate_product_control_norm_finite',0<norm['control_norm']<4)

        cap=json.loads((ROOT/'p3deps/q048_prefix_config_v1.json').read_text())
        old=json.loads((ROOT/'p3deps/q048_builder_admission_result_v1.json').read_text())
        init=initialize_cases(cap,old); result['initialized_cases']=init
        check('four_case_capture_and_retained_earliest_source_init',len(init)==4)

        transformed={}
        flat={}
        controls=[]
        # Predeclared deterministic controls: endpoints/extrema + 64 equispaced indices/table.
        for name,count in [('Alpha_inf.dat',16000),('R_inf.dat',100)]:
            tokens=load_tokens(ROOT/'p3deps'/name)
            check(name+'_loader_count_bound_to_v2_transform',len(tokens)==count)
            values=[]; meta=[]
            for k,s in enumerate(tokens):
                rec=table_log_union(s)
                v=I(rec['lo'],rec['hi']); values.append(v)
                meta.append((rec['qlo'],rec['qhi']))
                if k%251==0: guard()
            result['table_node_transforms']+=len(values)
            flat[name]=values
            transformed[name]={
              'order':'Alpha token=(i*40+j)*4+l; R token=i',
              'log_scale_bits':384,'log_slack_bits':180,
              'log_bounds_integer':[
                [str(v.lo*(1<<384)),str(v.hi*(1<<384))] for v in values
              ]
            }
            idx=set([0,count-1,min(range(count),key=lambda i:values[i].lo),max(range(count),key=lambda i:values[i].hi)])
            idx.update(i*(count-1)//63 for i in range(64))
            for k in sorted(idx):
                qlo,qhi=meta[k]; log=values[k]
                pL=primary_exp_point(log.lo); pU=primary_exp_point(log.hi)
                cL=control_exp_point(log.lo); cU=control_exp_point(log.hi)
                check(name+'_v2_primary_inverse_lower_'+str(k),pL.hi_fraction<qlo)
                check(name+'_v2_primary_inverse_upper_'+str(k),pU.lo_fraction>qhi)
                check(name+'_v2_control_inverse_lower_'+str(k),cL.hi_fraction<qlo)
                check(name+'_v2_control_inverse_upper_'+str(k),cU.lo_fraction>qhi)
                controls.append({'table':name,'token_index':k,
                    'primary_lower':v2_encode_scaled(pL),'primary_upper':v2_encode_scaled(pU),
                    'control_lower':v2_encode_scaled(cL),'control_upper':v2_encode_scaled(cU),
                    'input_lower':str(qlo),'input_upper':str(qhi)})
        # Mandatory serialization happens before any later admission can fail.
        transformed_path=HERE/'q048_p3_scaled_transformed_log_tables_v2.json'
        transformed_path.write_text(json.dumps(transformed,separators=(',',':'))+'\n')
        result['transformed_tables_sha256']=digest(transformed_path)
        result['inverse_controls']=controls
        check('serialized_exactly_16100_changed_arithmetic_transforms',
              result['table_node_transforms']==16100 and transformed_path.exists())

        # Specific MATH018 R0 discriminator, now evaluated in the generalized V2 path.
        r0=table_log_union(load_tokens(ROOT/'p3deps/R_inf.dat')[0])
        pL=primary_exp_point(r0['lo']);pU=primary_exp_point(r0['hi'])
        cL=control_exp_point(r0['lo']);cU=control_exp_point(r0['hi'])
        check('R0_primary_inverse_lower_strict',pL.hi_fraction<r0['qlo'])
        check('R0_primary_inverse_upper_strict',pU.lo_fraction>r0['qhi'])
        check('R0_control_inverse_lower_strict',cL.hi_fraction<r0['qlo'])
        check('R0_control_inverse_upper_strict',cU.lo_fraction>r0['qhi'])
        # Downstream scaled unit product + reciprocal roundtrip on R0 lower endpoint.
        cert=pL; unit=unit_scaled(cert.p); prod=scaled_mul(cert,unit); recip=scaled_recip(cert); rt=scaled_recip(recip)
        check('R0_scaled_unit_product_positive_identity',prod.lo>0 and prod.lo_fraction<=cert.lo_fraction and prod.hi_fraction>=cert.hi_fraction)
        check('R0_scaled_reciprocal_positive',recip.lo>0)
        check('R0_scaled_reciprocal_roundtrip_contains',rt.lo_fraction<=cert.lo_fraction and rt.hi_fraction>=cert.hi_fraction)

        alpha=loader_alpha(flat['Alpha_inf.dat']); rr=flat['R_inf.dat']; atomic={}
        for l in range(4): atomic['Alpha_channel_'+str(l)]=global_log_admission(alpha[l],norm,2)
        for l in range(2): atomic['Alpha_eq_'+str(l)]=global_log_admission(alpha[l][39],norm,1)
        atomic['R2p2s']=global_log_admission(rr,norm,1)
        result['proofcells']+=7; result['atomic_global_admission']=atomic
        check('all_seven_global_atomic_primary_ranges_strictly_positive_finite',all(v['rate_range'].lo>0 for v in atomic.values()))
        check('all_seven_global_atomic_control_ranges_strictly_positive_finite',all(v['control_rate_range'].lo>0 for v in atomic.values()))

        grid={'DlogTR':(log_i(const('.4'))-log_i(const('.004')))/99,'DT_RATIO':(const('1')-const('.1'))/39}
        result['grid']=grid
        check('source_grid_spacings_positive',all(v.lo>0 for v in grid.values()))
        result['atomic_global_derivatives']={k:{'dlog_dlogTR_abs_upper':v['dlog_dnormalized_coordinate_abs_upper']/grid['DlogTR'].lo,
              'dlog_dT_RATIO_abs_upper':v['dlog_dnormalized_coordinate_abs_upper']/grid['DT_RATIO'].lo if k.startswith('Alpha_channel') else None}
              for k,v in atomic.items()}

        fit=load_fit(ROOT/'p3deps/fit_swift.dat'); result['fit_cases']={}
        for name,p in init.items():
            record=fit_admission(fit,p,norm); result['fit_cases'][name]=record; result['proofcells']+=2
            check(name+'_primary_1_plus_DK_positive',record['primary_denominator'].lo>0,record['primary_denominator'])
            check(name+'_separate_column_control_1_plus_DK_positive',record['control_denominator'].lo>0,record['control_denominator'])

        for TR,r in [(F('.004'),F('.1')),(F('.4'),F(1)),(F('.1'),F(2)),(F('.02'),F(10))]:
            output=interpolate_atomic(alpha,rr,I(TR),I(r))
            check('implemented_lookup_'+str(TR)+'_'+str(r),
                  all(v.lo>0 for k,vs in output.items() if k!='DAlpha' for v in (vs if isinstance(vs,list) else [vs])))

        check('full_domain_stencil_endpoints',stencil(F(0),100)==(1,F(-1)) and stencil(F(99),100)==(97,F(2)))
        check('proofcells_exact_frozen_plan',result['proofcells']==cfg['planned_proofcells'])

        result['status']='PASS_BOUNDED_COMPONENT'
        result['stop_reason']='BOUNDED_P3_V2_OPERATOR_ADMISSION_QUALIFIED'
        result['limitations']=[
          'Conditional source-real operator admission only; not native parser/libm/P6.',
          'Caller must still prove actual TR/ratio state domains, radiation identity and active branch over the later state tube.',
          'No complete Beta/C-factor/Jacobian, closed hydrogen/thermal denominator tube, hybrid first event E1-E3 or complete histories.',
          'Full post-frec P4 and native P6 remain open; no physical theory confirmation/falsification or model promotion.'
        ]
    except Exception as exc:
        result['status']='STOPPED_OBSTRUCTION_OR_CAP'
        result['stop_reason']='FIRST_NEW_MATERIAL_OBSTRUCTION_OR_CAP'
        result['obstruction']={'exception':repr(exc),'traceback':traceback.format_exc()}
    result['end_utc']=utc(); result['proof_compute_seconds']=time.monotonic()-start
    result['within_compute_cap']=result['proof_compute_seconds']<=cfg['budget_seconds']
    out=HERE/'q048_p3_scaled_raw_result_v2.json'
    out.write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','stop_reason','start_utc','end_utc','proof_compute_seconds','proofcells','table_node_transforms','within_compute_cap']},indent=2))
    return 0 if result['status']=='PASS_BOUNDED_COMPONENT' else 1

if __name__=='__main__': raise SystemExit(main())
