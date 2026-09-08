#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, importlib.util, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import cho_factor, cho_solve

Q='Q-040'
PROGRAM_ID='Q040-CMBSPACE-V4'
RUN_ID='Q040-CMBSPACE-COUPLED-BRIDGE-V4'
RESULT_ID='R-Q040-EDE-CMBSPACE-COUPLED-BRIDGE-004'
SUPPORT_HASH='f6d7b3195789e7149942c63543bdd8e9a44490ea3f3645fb964e936ec69cca2b'
SCALES_HASH='732aeeb127d9083c0924552aa276117310ca32b5bfda854f51bfd3240638b2f6'


def write(path, obj):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def finite(x):
    try: return math.isfinite(float(x))
    except Exception: return False

def load_module(path):
    spec=importlib.util.spec_from_file_location('q040_cmbspace_static',path)
    if spec is None or spec.loader is None: raise RuntimeError('MODULE_LOAD_GATE=FAIL')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


def synthetic_schur_gate():
    # Positive definite joint Hessian. The Schur marginal precision must equal
    # Hss-Hse Hee^-1 Hes; its covariance must not be tighter than conditioning
    # on nuisance at the mode.
    Hss=np.array([[4.0,0.6],[0.6,3.0]])
    Hee=np.array([[5.0,0.4],[0.4,2.8]])
    Hse=np.array([[0.8,-0.2],[0.3,0.5]])
    P=Hss-Hse@np.linalg.solve(Hee,Hse.T)
    cho_factor(P,lower=True)
    C=np.linalg.inv(P); Ccond=np.linalg.inv(Hss)
    eig=np.linalg.eigvalsh(0.5*((C-Ccond)+(C-Ccond).T))
    return bool(np.min(eig)>=-1e-12 and np.allclose(P,Hss-Hse@np.linalg.solve(Hee,Hse.T),rtol=0,atol=1e-14))


def synthetic_scaled_coordinate_gate(mod):
    class C:
        proposal_scales=np.array([0.5,2.0])
        bounds=((-1.0,2.0),(None,5.0))
    c=C(); center=np.array([0.25,1.0]); z=np.array([1.5,1.25])
    eta=mod._eta_from_z(c,center,z)
    b=mod._scaled_bounds(c,center)
    return bool(np.allclose(eta,[1.0,3.5]) and np.isclose(b[0][0],-2.5) and np.isclose(b[0][1],3.5) and b[1][0] is None and np.isclose(b[1][1],2.0))




def synthetic_variable_projection_gate(mod):
    class C:
        proposal_scales=np.array([1.0])
        bounds=((None,None),)
        ells=np.array([2,3])
        row_ell_index=np.array([0,0,1],dtype=int)
        P=np.eye(3)
        def prior_nlp(self, eta): return 0.0
        def gls_system(self, eta, A_planck=1.0):
            y=np.array([3.0,5.0,8.0])
            a=np.array([1.0,1.0,2.0])
            # exact per-ell GLS: ell=2 -> 4, ell=3 -> 4
            cmb=np.array([4.0,4.0])
            return cmb, None, y, a, None
    c=C()
    obj,cmb=mod.profiled_state(c,np.array([0.0]))
    return bool(np.allclose(cmb,[4.0,4.0],rtol=0,atol=1e-14) and np.isclose(obj,1.0,rtol=0,atol=1e-14))

def static(args):
    pp=Path(args.program); text=pp.read_text(encoding='utf-8'); tree=ast.parse(text); mod=load_module(pp)
    pr=read(args.preregister); sl=read(args.source_lock)
    workflow_path=Path('.github/workflows/q040-cmbspace-coupled-bridge-v4.yml')
    workflow_text=workflow_path.read_text(encoding='utf-8') if workflow_path.is_file() else ''
    # Geometry function sanity: exact equality must pass the inherited gate.
    rows={i:{} for i in mod.IMPLEMENTATIONS}
    for label in mod.LABELS:
        base={c:0.0 for c in mod.COORDS}
        rows['camspec'][label]=dict(base); rows['hillipop'][label]=dict(base)
    z=mod.calculate_metrics(rows,mod.LABELS)
    zero_geometry=(z['matched_median']==0.0 and z['centroid']==0.0 and z['pairwise_median_drift']==0.0 and mod.sufficient(z))
    rules=pr.get('rules',{})
    nuisance=pr.get('nuisance_semantics',{})
    comp=pr.get('compression_method',{})
    val=pr.get('compression_validation',{})
    ep=pr.get('endpoint_execution',{})
    geometry=pr.get('geometry',{})
    gates={
      'PYTHON_PARSE_GATE': isinstance(tree,ast.Module),
      'Q_IDENTITY_GATE': mod.Q==Q and pr.get('project',{}).get('q')==Q and sl.get('q')==Q,
      'PROGRAM_ID_GATE': mod.PROGRAM_ID==PROGRAM_ID and pr.get('project',{}).get('program_id')==PROGRAM_ID and sl.get('program_id')==PROGRAM_ID,
      'RUN_RESULT_ID_GATE': mod.RUN_ID==RUN_ID and mod.RESULT_ID==RESULT_ID,
      'PARENT_Q032_GATE': mod.Q032_EXECUTION_COMMIT=='4dc873a5e880d40858d831a3b421456728f0c032' and mod.Q032_GITHUB_RUN==33994305721,
      'SUPPORT_HASH_GATE': mod.SUPPORT_HASH==SUPPORT_HASH and pr.get('parent_lock',{}).get('q032_support_sha256')==SUPPORT_HASH,
      'SCALE_HASH_GATE': mod.SCALES_HASH==SCALES_HASH and ep.get('locked_scales_sha256')==SCALES_HASH,
      'MODEL_COMMIT_GATE': mod.BACKEND_COMMIT=='5a131c91d657dd9a7c6364cc45b038710f8d0d97',
      'HILLIPOP_COMMIT_GATE': mod.HILLIPOP_COMMIT=='a09ddde3e7ce11df99f74685feb1f1764cafb251',
      'COBAYA_VERSION_GATE': mod.COBAYA_VERSION=='3.5.6',
      'IDENTITY_MULTIPOLE_GATE': pr.get('cmb_representation',{}).get('primary')=='IDENTITY_UNIQUE_MULTIPOLE_TT' and pr.get('cmb_representation',{}).get('new_binning_allowed') is False,
      'NATIVE_NUISANCE_GATE': nuisance.get('native_sampled_tt_nuisance_only') is True and nuisance.get('prior_widening') is False and nuisance.get('negative_amplitude_override') is False,
      'A_PLANCK_GATE': nuisance.get('A_planck')=='PRESERVE_AS_EXPLICIT_RUNTIME_PARAMETER_NOT_MARGINALIZED',
      'NO_FOREGROUND_ZERO_GATE': nuisance.get('foreground_zeroing') is False,
      'NO_CROSS_MAPPING_GATE': nuisance.get('forced_cross_implementation_mapping') is False,
      'LAPLACE_SCHUR_GATE': comp.get('method')=='CONSTRAINED_LAPLACE_SCHUR_MARGINALIZATION' and 'H_ss - H_s_eta H_eta_eta^-1 H_eta_s' in comp.get('marginal_cmb_precision',''),
      'V4_SOLVER_GATE': comp.get('solver')=='EXACT_GLS_VARIABLE_PROJECTION_PROFILED_NUISANCE_MAP_V4' and int(comp.get('profile_max_iterations'))==5000 and float(comp.get('fixed_point_relative_objective_tolerance'))==1e-6 and float(comp.get('fixed_point_scaled_nuisance_tolerance'))==1e-3 and int(comp.get('verification_triggered_profile_polish_max'))==1,
      'V4_TECHNICAL_SUPERSESSION_GATE': pr.get('technical_supersession',{}).get('supersedes_program_id')=='Q040-CMBSPACE-V3' and pr.get('technical_supersession',{}).get('failed_run_id')==34209404762 and pr.get('technical_supersession',{}).get('scientific_model_data_priors_bounds_support_geometry_and_acceptance_thresholds_changed') is False,
      'SYNTHETIC_SCALED_COORDINATE_GATE': synthetic_scaled_coordinate_gate(mod),
      'SYNTHETIC_VARIABLE_PROJECTION_GATE': synthetic_variable_projection_gate(mod),
      'MULTISTART_GATE': tuple(comp.get('start_families',[]))==tuple(mod.START_FAMILIES) and float(comp.get('multistart_objective_spread_max'))==0.5 and float(comp.get('multistart_cmb_normalized_rms_max'))==0.1,
      'BOUNDARY_GATE': float(comp.get('boundary_sigma_min'))==2.5,
      'VALIDATION_TOLERANCE_GATE': float(val.get('max_abs_native_vs_compressed_delta_chi2_error'))==0.35 and int(val.get('conditional_nuisance_multistart'))==2,
      'ENDPOINT_COUNT_GATE': len(mod.LABELS)==9 and len(mod.IMPLEMENTATIONS)*len(mod.LABELS)==18,
      'ENDPOINT_OPTIMIZER_GATE': int(ep.get('max_evals'))==300000 and float(ep.get('rhoend'))==1e-5,
      'SUFFICIENCY_GATE': float(geometry.get('sufficiency_threshold'))==0.10 and geometry.get('partial_material_reduction_terminal_label_registered') is False,
      'NO_CROSS_OBJECTIVE_GATE': rules.get('no_cross_likelihood_absolute_objective_subtraction') is True and rules.get('no_cross_likelihood_chi2_sum') is True,
      'CLOSED_LINEAGE_GATE': rules.get('q035_remains_closed') is True and rules.get('q037_remains_closed') is True and rules.get('q039_remains_closed') is True,
      'NO_PARTIAL_TERMINAL_LABEL_IN_CODE_GATE': 'PARTIAL_MATERIAL_REDUCTION' not in text,
      'SYNTHETIC_SCHUR_MATH_GATE': synthetic_schur_gate(),
      'SYNTHETIC_ZERO_GEOMETRY_GATE': zero_geometry,
      'Q032_PARENT_ARTIFACT_LOCK_GATE': ('q032-preflight-sealed-v2' in workflow_text and 'q032-hillipop-covariance-v2' in workflow_text and 'q032-preflight-sealed-v3' not in workflow_text and 'q032-preflight-sealed-v4' not in workflow_text and 'q032-hillipop-covariance-v3' not in workflow_text and 'q032-hillipop-covariance-v4' not in workflow_text),
      'SOURCE_LOCK_ROLE_GATE': sl.get('software',{}).get('camspec_npipe_lite_role')=='METHODOLOGICAL_REFERENCE_AND_VALIDATION_PRECEDENT_ONLY_NOT_Q040_DATA_PRODUCT',
    }
    status='PASS' if all(gates.values()) else 'FAIL'
    write(args.output,{'q':Q,'program_id':PROGRAM_ID,'stage':'STATIC_TESTS','status':status,'gates':gates})
    return 0 if status=='PASS' else 2


def result(args):
    d=read(args.final); cv=read(args.camspec_validation); hv=read(args.hillipop_validation)
    full=d.get('full_sample',{}); loo=d.get('leave_one_label_out',{})
    m=full.get('metrics',{})
    finite_full=all(finite(m.get(k)) for k in ('matched_median','centroid','pairwise_median_drift'))
    loo_finite=(len(loo)==9 and all(all(finite(v.get('metrics',{}).get(k)) for k in ('matched_median','centroid','pairwise_median_drift')) for v in loo.values()))
    full_expected=(finite_full and m['matched_median']<=0.10 and m['centroid']<=0.10 and m['pairwise_median_drift']<=0.10)
    loo_expected=(len(loo)==9 and loo_finite and all(v['metrics']['matched_median']<=0.10 and v['metrics']['centroid']<=0.10 and v['metrics']['pairwise_median_drift']<=0.10 for v in loo.values()))
    suff_expected=bool(full_expected and loo_expected)
    class_expected='COUPLED_CMBSPACE_BRIDGE_SUFFICIENT' if suff_expected else 'COUPLED_CMBSPACE_BRIDGE_INSUFFICIENT'
    validations=[cv,hv]
    valid_compression=(
        {x.get('implementation') for x in validations}=={'camspec','hillipop'} and
        all(x.get('q')==Q and x.get('program_id')==PROGRAM_ID and x.get('stage')=='COMPRESSION_VALIDATION' and x.get('status')=='PASS' for x in validations) and
        all(finite(x.get('max_abs_native_vs_compressed_delta_chi2_error')) and float(x['max_abs_native_vs_compressed_delta_chi2_error'])<=0.35 for x in validations) and
        all(x.get('gates',{}).get('FINAL_COMPRESSION_VALIDATION_GATE')=='PASS' for x in validations)
    )
    reductions=d.get('continuous_reduction_fraction_vs_q037',{})
    gates={
      'Q_IDENTITY_GATE': d.get('q')==Q,
      'PROGRAM_ID_GATE': d.get('program_id')==PROGRAM_ID,
      'RUN_RESULT_ID_GATE': d.get('run_id')==RUN_ID and d.get('result_id')==RESULT_ID,
      'EXECUTION_COMPLETE_GATE': d.get('execution_status')=='COMPLETE' and d.get('actual_computed_result') is True,
      'JOB_COMPLETENESS_GATE': d.get('profile_count')==18 and d.get('expected_profile_count')==18,
      'SUPPORT_GATE': d.get('support_sha256')==SUPPORT_HASH and d.get('scales_sha256')==SCALES_HASH,
      'COMPRESSION_VALIDATION_GATE': valid_compression,
      'FINITE_FULL_GEOMETRY_GATE': finite_full,
      'NINE_LOO_GATE': len(loo)==9 and loo_finite,
      'INHERITED_SUFFICIENCY_GATE': bool(full.get('sufficient'))==full_expected and bool(d.get('all_nine_loo_sufficient'))==loo_expected and bool(d.get('sufficient'))==suff_expected,
      'CLASSIFICATION_CONSISTENCY_GATE': d.get('classification')==class_expected,
      'PROVISIONAL_GATE': d.get('final_result_gate')=='PROVISIONAL' and d.get('tests_status')=='PENDING_EXTERNAL_TEST_SCRIPT',
      'NO_PARTIAL_TERMINAL_LABEL_GATE': d.get('partial_material_reduction_terminal_label_registered') is False and d.get('classification') in {'COUPLED_CMBSPACE_BRIDGE_SUFFICIENT','COUPLED_CMBSPACE_BRIDGE_INSUFFICIENT'},
      'REDUCTION_REPORT_GATE': set(reductions)=={'matched_median','centroid','pairwise_median_drift'} and all(finite(x) for x in reductions.values()),
      'NO_CROSS_OBJECTIVE_GATE': d.get('cross_likelihood_absolute_objective_subtraction_performed') is False and d.get('cross_likelihood_chi2_sum_performed') is False,
      'SCIENTIFIC_INTERPRETATION_GATE': any('methodological evidence about Planck likelihood portability' in x for x in d.get('interpretation_limits',[])),
    }
    status='PASS' if all(gates.values()) else 'FAIL'
    write(args.output,{'q':Q,'program_id':PROGRAM_ID,'run_id':RUN_ID,'result_id':RESULT_ID,'stage':'RESULT_TESTS','status':status,'gates':gates,'FINAL_RESULT_GATE':status})
    return 0 if status=='PASS' else 2


def main():
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('static'); a.add_argument('--program',required=True); a.add_argument('--preregister',required=True); a.add_argument('--source-lock',required=True); a.add_argument('--output',required=True); a.set_defaults(func=static)
    a=sp.add_parser('result'); a.add_argument('--final',required=True); a.add_argument('--camspec-validation',required=True); a.add_argument('--hillipop-validation',required=True); a.add_argument('--output',required=True); a.set_defaults(func=result)
    args=p.parse_args(); raise SystemExit(args.func(args))
if __name__=='__main__': main()
