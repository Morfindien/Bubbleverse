"""Behavior tests for the finite CLASS attribution diagnostic."""
import importlib.util
from pathlib import Path
import unittest, tempfile, json

P=Path(__file__).with_name('q042_class_diagnostic_v23.py')

class Tests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.is_file(), 'Attribution implementation is missing')
        s=importlib.util.spec_from_file_location('diagnostic_v23',P)
        self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)

    def test_positive_nodes_can_have_negative_spline(self):
        # f(t)=1-8t(1-t); f(0)=f(1)=1, f(1/2)=-1, f''=16.
        self.assertEqual(self.m.spline_value(0,1,1,1,16,16,0.5),-1)
        self.assertEqual(self.m.classify(1,1,-1,'spline'),'INTERPOLATION_OVERSHOOT')

    def test_negative_node_is_preserved(self):
        self.assertEqual(self.m.classify(-2,1,-1,'spline'),'NEGATIVE_TABLE_NODE')

    def test_linear_negative_is_not_called_spline_overshoot(self):
        self.assertEqual(self.m.classify(1,1,-1,'linear'),'INCONSISTENT_LINEAR_RESULT')

    def test_finite_positive_result_is_unresolved(self):
        self.assertEqual(self.m.classify(1,1,0.2,'spline'),'NEGATIVE_VALUE_NOT_REPRODUCED')

    def test_nonfinite_input_is_rejected(self):
        with self.assertRaises(ValueError):self.m.classify(1,1,float('nan'),'spline')

    def test_collector_rejects_other_run_and_retains_failure(self):
        record={'q':'Q-042','program_id':'Q042-CLASSCAUSE-V23','github_run_id':'wrong','execution_commit':'abc','diagnostic_gate':'PASS','scientific_result':False}
        result=self.m.collect_records([record],'123','abc')
        self.assertEqual(result['job_completeness_gate'],'FAIL')
        self.assertFalse(result['scientific_result'])

    def test_collector_rejects_duplicate_and_cannot_promote_science(self):
        record={'q':'Q-042','program_id':'Q042-CLASSCAUSE-V23','github_run_id':'123','execution_commit':'abc','diagnostic_gate':'PASS','scientific_result':False,'class_binary_sha256':'df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf','class_commit':'5a131c91d657dd9a7c6364cc45b038710f8d0d97','production_restart_authorized':False,'precision_changed':False,'new_bobyqa_starts':0}
        self.assertEqual(self.m.collect_records([record,record],'123','abc')['job_completeness_gate'],'FAIL')
        good=self.m.collect_records([record],'123','abc')
        self.assertEqual(good['job_completeness_gate'],'PASS')
        self.assertEqual(good['final_result_gate'],'UNRESOLVED')
        self.assertFalse(good['production_restart_authorized'])

    def test_table_attribution_preserves_negative_raw_values(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'native_meta.json').write_text(json.dumps({'tt_size':2,'reionization_z_start_max':50}))
            (p/'native_probe.json').write_text(json.dumps({'last_index':0,'method':'spline','z':0.5,'xe':-1,'dkappa':-2}))
            (p/'native_nodes.csv').write_text('z,xe,dkappa,d2xe_dz2,d2dkappa_dz2\n0,1,2,16,32\n1,1,2,16,32\n')
            (p/'native_extrema.csv').write_text('interval,column,z,xe,dkappa\n0,xe,0.5,-1,-2\n')
            result=self.m.inspect_tables(p)
            self.assertEqual(result['causal_gate'],'PASS')
            self.assertEqual(result['details']['xe']['native_value'],-1)
            self.assertFalse(result['class_blocker_resolved'])
            self.assertTrue(result['precision_candidate_gate'].startswith('BLOCKED'))

    def test_collector_cannot_accept_repaired_precision_as_frozen(self):
        record={'q':'Q-042','program_id':'Q042-CLASSCAUSE-V23','github_run_id':'123','execution_commit':'abc','diagnostic_gate':'PASS','scientific_result':False,'class_binary_sha256':'df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf','class_commit':'5a131c91d657dd9a7c6364cc45b038710f8d0d97','production_restart_authorized':False,'precision_changed':True,'new_bobyqa_starts':0}
        self.assertEqual(self.m.collect_records([record],'123','abc')['job_completeness_gate'],'FAIL')

if __name__=='__main__':unittest.main()
