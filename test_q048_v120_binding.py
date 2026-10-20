"""Synthetic binding controls, not a scientific proof run."""
from pathlib import Path
import copy
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parent

class BindingContract(unittest.TestCase):
    def test_accepts_only_v119_row54_no_reset(self):
        path = ROOT / 'q048_v120_proof.py'
        self.assertTrue(path.exists(), 'V120 binding implementation is missing')
        s = importlib.util.spec_from_file_location('v120', path)
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        read = lambda n: json.loads((ROOT/'inputs'/n).read_bytes())
        p = read('Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
        t = read('Q048_V120_NEXT_MATHEMATICS_TASK_V1.json')
        g = read('q048_guard_local_v_result_v12.json')
        self.assertEqual(m.validate_binding(p,t,g)[0]['index'],54)
        bad = copy.deepcopy(p);bad['accepted_actual']['count']=111
        with self.assertRaisesRegex(ValueError,'PARENT'):m.validate_binding(bad,t,g)
        bad = copy.deepcopy(g);bad['evaluators'][0]['rows'][54]['source_state_reset']=True
        with self.assertRaisesRegex(ValueError,'STATE_RESET'):m.validate_binding(p,t,bad)
        bad = copy.deepcopy(p);bad['endpoint']['Y']='0'
        with self.assertRaisesRegex(ValueError,'GLUE'):m.validate_binding(bad,t,g)

    def test_rejects_wrong_cell_before_computation(self):
        path = ROOT / 'q048_v120_proof.py'
        self.assertTrue(path.exists(), 'V120 cell-binding implementation is missing')
        s=importlib.util.spec_from_file_location('v120',path)
        m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
        read=lambda n:json.loads((ROOT/'inputs'/n).read_bytes())
        p=read('Q048_V119_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
        t=read('Q048_V120_NEXT_MATHEMATICS_TASK_V1.json')
        g=read('q048_guard_local_v_result_v12.json')
        t['cell_z']=[900,900]
        with self.assertRaisesRegex(ValueError,'CELL'):m.validate_binding(p,t,g)

if __name__=='__main__':unittest.main()


class SourceBoundaryContract(unittest.TestCase):
    def modules(self):
        for kind in ['proof','verify']:
            path=ROOT/('q048_v120_'+kind+'.py')
            self.assertTrue(path.exists(),'V120 source-boundary implementation missing: '+kind)
            spec=importlib.util.spec_from_file_location('boundary_'+kind,path)
            m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
            self.assertTrue(hasattr(m,'source_boundary_certificate'),'V120 explicit endpoint-inclusive contract missing')
            yield m
    def test_exact_900_endpoint_accepted(self):
        from fractions import Fraction as F
        for m in self.modules():
            c=m.source_boundary_certificate(F(1,911),F(1,901),ROOT/'inputs',4)
            self.assertEqual(c['z_min'],'900');self.assertEqual(c['z_max'],'910')
            self.assertFalse(c['low_z_branch_active_anywhere'])
            self.assertEqual(c['Pion'],'1');self.assertEqual(c['PION_MAX'],'1/100')
    def test_any_below_900_domain_rejected(self):
        from fractions import Fraction as F
        for m in self.modules():
            with self.assertRaisesRegex(ValueError,'SOURCE_BOUNDARY'):
                m.source_boundary_certificate(F(1,911),F(1,900),ROOT/'inputs',4)
    def test_wrong_model_and_changed_source_rejected(self):
        from fractions import Fraction as F
        import tempfile,shutil
        for m in self.modules():
            with self.assertRaisesRegex(ValueError,'SOURCE_BOUNDARY'):
                m.source_boundary_certificate(F(1,911),F(1,901),ROOT/'inputs',3)
            with tempfile.TemporaryDirectory() as d:
                p=Path(d);(p/'source').mkdir()
                for n in ['hydrogen.c','hydrogen.h']:shutil.copyfile(ROOT/'inputs/source'/n,p/'source'/n)
                q=p/'source/hydrogen.c';q.write_bytes(q.read_bytes()+b' ')
                with self.assertRaisesRegex(ValueError,'SOURCE_BOUNDARY'):
                    m.source_boundary_certificate(F(1,911),F(1,901),p,4)
