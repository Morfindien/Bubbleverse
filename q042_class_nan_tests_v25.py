"""Finite behavior tests: malformed, incomplete or unexpected traces never become science."""
import copy, importlib.util, json, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent

class TraceTests(unittest.TestCase):
    def setUp(self):
        p=HERE/'q042_class_nan_v25.py'
        self.assertTrue(p.is_file(),'Upstream boundary classifier is not implemented')
        s=importlib.util.spec_from_file_location('nan_v25',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)

    def sample(self,kind='first_nonfinite',inputs=None,outputs=None):
        # Removing validation of these explicit finite flags would accept corrupted telemetry.
        return dict(event='upstream',boundary='thermodynamics_derivs',phase='exit',kind=kind,trial=1,call=2,z=49.0,status=0,
                    inputs={'z':49.0,'D_Tmat':-110.0,'x_H':0.0002,'x_He':0.0},outputs={'dD_Tmat':'NaN'},
                    inputs_finite=True,outputs_finite=False,previous_finite={'call':1,'z':50.0,'inputs':{'D_Tmat':-100.0},'outputs':{'dD_Tmat':0.2}})

    def test_finite_input_nonfinite_output_is_a_boundary_not_global_root(self):
        result=self.m.classify_upstream([self.sample()])
        self.assertEqual(result['diagnosis'],'FINITE_INPUT_NONFINITE_OUTPUT_AT_OBSERVED_BOUNDARY')
        self.assertEqual(result['first_observed']['outputs']['dD_Tmat'],'NaN')
        self.assertFalse(result['global_first_nonfinite_established'])
        self.assertFalse(result['repair_ready'])

    def test_nonfinite_already_on_entry_is_not_creation_inside_function(self):
        x=self.sample();x.update(phase='entry',inputs={'z':49.0,'x_H':'NaN'},outputs={},inputs_finite=False,outputs_finite=True)
        result=self.m.classify_upstream([x])
        self.assertEqual(result['diagnosis'],'NONFINITE_PRESENT_ON_OBSERVED_ENTRY')

    def test_all_finite_is_preserved_as_unexpected_not_called_failure_of_physics(self):
        x=self.sample();x.update(kind='initial',outputs={'dD_Tmat':0.2},outputs_finite=True)
        r=self.m.classify_upstream([x]);self.assertEqual(r['diagnosis'],'NO_NONFINITE_OBSERVED_AT_INSTRUMENTED_BOUNDARIES');self.assertFalse(r['scientific_result'])

    def test_flag_cannot_hide_a_literal_nan(self):
        x=self.sample();x['outputs_finite']=True
        with self.assertRaises(ValueError):self.m.classify_upstream([x])

    def test_invalid_number_encoding_is_rejected(self):
        for value in [None,True,'0.1',float('nan')]:
            with self.subTest(value=value):
                x=self.sample();x['outputs']['dD_Tmat']=value
                with self.assertRaises(ValueError):self.m.classify_upstream([x])

    def test_unknown_boundary_and_out_of_order_calls_are_rejected(self):
        x=self.sample();x['boundary']='invented'
        with self.assertRaises(ValueError):self.m.classify_upstream([x])
        x=self.sample();y=copy.deepcopy(x);y['call']=1
        with self.assertRaises(ValueError):self.m.classify_upstream([x,y])

    def test_duplicate_first_nonfinite_is_rejected(self):
        x=self.sample();y=copy.deepcopy(x);y['call']=3
        with self.assertRaises(ValueError):self.m.classify_upstream([x,y])

    def test_empty_upstream_trace_does_not_pass_interception(self):
        with self.assertRaises(ValueError):self.m.classify_upstream([])

    def test_empty_snapshots_do_not_establish_a_successful_boundary(self):
        for field in ('inputs','outputs'):
            x=self.sample();x[field]={};x[field+'_finite']=True
            with self.assertRaises(ValueError):self.m.classify_upstream([x])

    def test_previous_finite_snapshot_must_really_be_finite_and_earlier(self):
        for change in ['nan','later']:
            x=self.sample()
            if change=='nan':x['previous_finite']['inputs']['D_Tmat']='NaN'
            else:x['previous_finite']['call']=3
            with self.assertRaises(ValueError):self.m.classify_upstream([x])

    def test_wrong_run_duplicate_or_changed_precision_fail_completeness(self):
        r=dict(q='Q-042',program_id='Q042-CLASSNAN-V25',github_run_id='12',execution_commit='abc',trace_gate='PASS',
               class_binary_sha256='df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf',
               class_commit='5a131c91d657dd9a7c6364cc45b038710f8d0d97',scientific_result=False,production_restart_authorized=False,precision_changed=False,new_bobyqa_starts=0)
        self.assertEqual(self.m.collect_records([r],'12','abc',[])['job_completeness_gate'],'PASS')
        for records,run in [([r,r],'12'),([r],'other'),([dict(r,precision_changed=True)],'12'),([], '12')]:
            self.assertEqual(self.m.collect_records(records,run,'abc',[])['job_completeness_gate'],'FAIL')
        self.assertFalse(self.m.collect_records([r],'12','abc',[])['scientific_result'])

if __name__=='__main__':unittest.main()
