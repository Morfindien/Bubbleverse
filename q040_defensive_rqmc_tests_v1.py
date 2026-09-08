#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json, math, tempfile
from pathlib import Path
import numpy as np
from scipy.integrate import quad

Q='Q-040'; PROGRAM_ID='Q040-RQMC-V1'; RESULT_ID='R-Q040-EDE-DEFENSIVE-RQMC-CMB-MARGINAL-001'
ALLOWED_FINAL={'DEFENSIVE_CMB_MARGINAL_BRIDGE_SUFFICIENT','DEFENSIVE_CMB_MARGINAL_BRIDGE_INSUFFICIENT'}


def readj(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def writej(p,d): Path(p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def gate(g,name,cond,detail=None):
    g[name]='PASS' if cond else 'FAIL'
    if not cond: raise AssertionError(f'{name}=FAIL'+(f' {detail}' if detail else ''))

def static(args):
    import q040_defensive_rqmc_v1 as q
    g={}
    src=Path(args.program).read_text(encoding='utf-8'); tree=ast.parse(src)
    pr=readj(args.preregister); sl=readj(args.source_lock); wf=Path(args.workflow).read_text(encoding='utf-8')
    gate(g,'Q_IDENTITY_GATE',q.Q==Q and q.PROGRAM_ID==PROGRAM_ID and q.RESULT_ID==RESULT_ID)
    gate(g,'PYTHON_AST_GATE',isinstance(tree,ast.Module))
    gate(g,'PREREGISTRATION_IDENTITY_GATE',pr['project']['q']==Q and pr['project']['program_id']==PROGRAM_ID and pr['project']['result_id']==RESULT_ID)
    gate(g,'SOURCE_LOCK_IDENTITY_GATE',sl['q']==Q and sl['program_id']==PROGRAM_ID and sl['result_id']==RESULT_ID)
    gate(g,'PARENT_Q032_GATE',pr['parent_lock']['q032_run_id']==33994305721 and pr['parent_lock']['q032_support_sha256']=='f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b')
    gate(g,'MODEL_COMMIT_GATE',pr['model_lock']['backend_commit']=='5a131c91d657dd9a7c6364cc45b038710f8d0d97')
    gate(g,'HILLIPOP_COMMIT_GATE',pr['model_lock']['hillipop_commit']=='a09ddde3e7ce11df99f74685feb1f1764cafb251')
    gate(g,'COBAYA_VERSION_GATE',pr['model_lock']['cobaya_version']=='3.5.6')
    gate(g,'NO_HIDDEN_BINNING_GATE',pr['cmb_representation']['primary']=='IDENTITY_UNIQUE_MULTIPOLE_TT' and pr['cmb_representation']['new_binning_allowed'] is False)
    gate(g,'A_PLANCK_PRESERVATION_GATE',pr['nuisance_semantics']['A_planck']=='PRESERVE_AS_EXPLICIT_RUNTIME_PARAMETER_NOT_MARGINALIZED')
    rq=pr['rqmc']
    gate(g,'RQMC_SCHEDULE_GATE',(rq['m_min'],rq['m_max'],rq['replicates'])==(9,16,4) and rq['hard_cap_nodes_per_replicate']==393216)
    gate(g,'DEFENSIVE_MIXTURE_SPEC_GATE',rq['proposal']=='q=0.5*pi + (q1+q2+q3)/6' and abs(rq['weight_ratio_max']-2.0)<1e-15)
    gate(g,'STUDENT_T_GATE',rq['student_t_df']==5.0 and rq['hard_bound_handling'].startswith('exact truncated'))
    gate(g,'INTEGRATION_THRESHOLD_GATE',rq['integration_delta_chi2_tolerance']==0.05 and rq['bank_A_B_delta_chi2_tolerance']==0.05)
    gate(g,'CORESET_TIGHTER_THAN_INTEGRATION_GATE',rq['coreset_probe_max_abs_delta_chi2_error']==0.01 < rq['integration_delta_chi2_tolerance'])
    gate(g,'SCIENCE_THRESHOLD_GATE',pr['geometry']['sufficiency_threshold']==0.1)
    gate(g,'ENDPOINT_BANK_THRESHOLD_GATE',pr['endpoint_execution']['bank_endpoint_scaled_distance_max']==0.05)
    gate(g,'TERMINAL_OUTCOME_GATE',set(pr['terminal_outcomes'])=={'DEFENSIVE_CMB_MARGINAL_BRIDGE_SUFFICIENT','DEFENSIVE_CMB_MARGINAL_BRIDGE_INSUFFICIENT','DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL'})
    gate(g,'SOURCE_K057_GATE','K-057' in sl['sources'] and sl['sources']['K-057'].get('doi')=='10.1080/00401706.1995.10484303')
    gate(g,'SOURCE_K058_GATE','K-058' in sl['sources'] and sl['sources']['K-058'].get('doi')=='10.1006/jcom.1998.0487')
    gate(g,'UNRESOLVED_CAMSPEC_ID_GATE',sl['sources']['CAMSPEC_2021_ID_UNRESOLVED']['bubbleverse_k_id']=='NOT_DOCUMENTED_DO_NOT_INVENT')
    gate(g,'WORKFLOW_PROGRAM_GATE','PROGRAM_ID: Q040-RQMC-V1' in wf and 'default: Q040-RQMC-V1' in wf)
    gate(g,'WORKFLOW_LAUNCH_INPUT_GATE','workflow_dispatch:' in wf and 'program_id:' in wf)
    gate(g,'WORKFLOW_Q032_ARTIFACT_LOCK_GATE','q032-preflight-sealed-v2' in wf and 'q032-hillipop-covariance-v2' in wf and 'q032-preflight-sealed-v3' not in wf)
    gate(g,'WORKFLOW_V4_MAP_LOCK_GATE',"34211073134" in wf and 'q040-map-*' in wf)
    gate(g,'NO_LAPLACE_SCIENCE_PATH_GATE','build-compression' not in wf and 'validate-compression' not in wf)
    gate(g,'WORKFLOW_RESULT_TEST_GATE','q040_defensive_rqmc_tests_v1.py result' in wf)
    gate(g,'WORKFLOW_FAILURE_SEAL_GATE','seal-failure' in wf and 'DEFENSIVE_MARGINALIZATION_NUMERICAL_VALIDATION_FAIL' in src)
    gate(g,'MATRIX_LIMIT_GATE',max(2*q.shard_count_for_m(m) for m in range(q.RQMC_M_MIN,q.RQMC_M_MAX+1))<=256)
    gate(g,'CORESET_DIVISIBILITY_GATE',all(k%6==0 for k in q.CORESET_K))
    # Nested scrambled Sobol sequence: a larger level must keep the lower prefix for a fixed seed/stratum.
    a=q.sobol_points(3,12345,0,64); b=q.sobol_points(3,12345,0,128)
    gate(g,'RQMC_NESTED_PREFIX_GATE',np.array_equal(a,b[:64]))
    gate(g,'RQMC_SHELL_GATE',q.shell_range(9)==(0,512) and q.shell_range(10)==(512,1024) and sum(q.shell_range(m)[1]-q.shell_range(m)[0] for m in range(9,17))==65536)
    # Analytic defensive-weight inequality on a concrete proper 1-D prior/proposal context.
    class C: pass
    c=C(); c.nuisance_names=('x',); c.priors=({'min':0.0,'max':1.0},); c.proposal_scales=np.array([0.15])
    centers=np.array([[0.1],[0.5],[0.9]])
    x=np.linspace(0,1,2001)[:,None]
    lp,lq=q.defensive_logq(c,centers,x); ratio=np.exp(lp-lq)
    gate(g,'DEFENSIVE_WEIGHT_SYNTHETIC_GATE',np.all(ratio<=2+1e-12) and np.all(ratio>=0))
    # Local truncated Student-t samples remain inside the native support without clipping.
    u=np.linspace(1e-9,1-1e-9,1001)
    xx=q._local_t_ppf_1d({'min':0.0,'max':50.0},50.0,1.0,u)
    gate(g,'BOUNDARY_TRUNCATED_T_GATE',float(xx.min())>=0 and float(xx.max())<=50)
    # Numerical check that q integrates to one for the concrete mixture.
    def qdens(z):
        lp,lq=q.defensive_logq(c,centers,np.array([[z]],float)); return math.exp(float(lq[0]))
    integ=quad(qdens,0,1,epsabs=2e-8,limit=200)[0]
    gate(g,'DEFENSIVE_MIXTURE_NORMALIZATION_GATE',abs(integ-1.0)<2e-6,integ)
    # Frozen thresholds and no post-hoc relaxation in code constants.
    gate(g,'FROZEN_THRESHOLD_CONSTANT_GATE',q.INTEGRATION_DELTA_CHI2_TOL==0.05 and q.ENDPOINT_BANK_TOL==0.05 and q.THRESHOLD==0.1)
    out={'q':Q,'program_id':PROGRAM_ID,'stage':'STATIC_TESTS','status':'PASS','FINAL_STATIC_GATE':'PASS','gates':g}
    writej(args.output,out); print(f'Q040_RQMC_STATIC_TESTS=PASS gates={len(g)}'); return 0


def result(args):
    g={}; p=readj(args.provisional); b=readj(args.bank_stability); i=readj(args.integration_state); c=readj(args.coreset_gate)
    pr=readj(args.preregister); sl=readj(args.source_lock)
    gate(g,'RESULT_IDENTITY_GATE',p.get('q')==Q and p.get('program_id')==PROGRAM_ID and p.get('result_id')==RESULT_ID)
    gate(g,'INTEGRATION_CONVERGENCE_GATE',i.get('q')==Q and i.get('program_id')==PROGRAM_ID and i.get('converged') is True)
    gate(g,'BANK_A_B_PROBE_STABILITY_GATE',all(v.get('bankA_B_pass') is True for v in i.get('implementations',{}).values()))
    gate(g,'CORESET_GATE',c.get('q')==Q and c.get('program_id')==PROGRAM_ID and c.get('proceed_to_endpoints') is True)
    gate(g,'MARGINAL_ENDPOINT_NUMERICAL_STABILITY_GATE',b.get('q')==Q and b.get('program_id')==PROGRAM_ID and b.get('proceed_to_production') is True and all(x.get('pass') is True for x in b.get('rows',{}).values()))
    gate(g,'JOB_COMPLETENESS_GATE',len(p.get('endpoint_provenance',{}))==18)
    gate(g,'FINAL_CLASSIFICATION_GATE',p.get('classification') in ALLOWED_FINAL)
    fs=p.get('full_sample',{}); loo=p.get('leave_one_label_out',{})
    gate(g,'NINE_LOO_GATE',len(loo)==9 and p.get('all_nine_loo_sufficient')==all(v.get('sufficient') for v in loo.values()))
    for metrics in [fs.get('metrics',{})]+[v.get('metrics',{}) for v in loo.values()]:
        gate(g,'FINITE_GEOMETRY_GATE_'+str(len(g)), all(k in metrics and math.isfinite(float(metrics[k])) for k in ('matched_median','centroid','pairwise_median_drift')))
    rule=lambda m: float(m['matched_median'])<=0.1 and float(m['centroid'])<=0.1 and float(m['pairwise_median_drift'])<=0.1
    expected_suff=rule(fs['metrics']) and all(rule(v['metrics']) for v in loo.values())
    gate(g,'FROZEN_SCIENCE_RULE_GATE',bool(p.get('sufficient'))==expected_suff and ((p['classification']=='DEFENSIVE_CMB_MARGINAL_BRIDGE_SUFFICIENT')==expected_suff))
    gate(g,'NO_CROSS_OBJECTIVE_ARITHMETIC_GATE',p.get('cross_likelihood_chi2_sum_performed') is False and p.get('cross_likelihood_absolute_objective_subtraction_performed') is False)
    gate(g,'SOURCE_CONTEXT_GATE','K-057' in sl['sources'] and 'K-058' in sl['sources'])
    gate(g,'PREREG_CONTEXT_GATE',pr['geometry']['sufficiency_threshold']==0.1 and pr['endpoint_execution']['bank_endpoint_scaled_distance_max']==0.05)
    out={'q':Q,'program_id':PROGRAM_ID,'result_id':RESULT_ID,'stage':'MANDATORY_RESULT_TESTS','status':'PASS','FINAL_RESULT_GATE':'PASS','gates':g}
    writej(args.output,out); print(f'Q040_RQMC_RESULT_TESTS=PASS gates={len(g)}'); return 0


def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('static'); a.add_argument('--program',required=True);a.add_argument('--preregister',required=True);a.add_argument('--source-lock',required=True);a.add_argument('--workflow',required=True);a.add_argument('--output',required=True);a.set_defaults(func=static)
    a=sp.add_parser('result');a.add_argument('--provisional',required=True);a.add_argument('--bank-stability',required=True);a.add_argument('--integration-state',required=True);a.add_argument('--coreset-gate',required=True);a.add_argument('--preregister',required=True);a.add_argument('--source-lock',required=True);a.add_argument('--output',required=True);a.set_defaults(func=result)
    args=p.parse_args(); raise SystemExit(args.func(args))
if __name__=='__main__': main()
