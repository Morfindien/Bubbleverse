"""Synthetic binding controls, not a scientific proof run."""
from pathlib import Path
import copy
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parent

class BindingContract(unittest.TestCase):
    def test_accepts_only_v113_row51_no_reset(self):
        path = ROOT / 'q048_v114_proof.py'
        self.assertTrue(path.exists(), 'V114 binding implementation is missing')
        s = importlib.util.spec_from_file_location('v114', path)
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        read = lambda n: json.loads((ROOT/'inputs'/n).read_bytes())
        p = read('Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
        t = read('Q048_V114_NEXT_MATHEMATICS_TASK_V1.json')
        g = read('q048_guard_local_v_result_v12.json')
        self.assertEqual(m.validate_binding(p,t,g)[0]['index'],51)
        bad = copy.deepcopy(p);bad['accepted_actual']['count']=111
        with self.assertRaisesRegex(ValueError,'PARENT'):m.validate_binding(bad,t,g)
        bad = copy.deepcopy(g);bad['evaluators'][0]['rows'][51]['source_state_reset']=True
        with self.assertRaisesRegex(ValueError,'STATE_RESET'):m.validate_binding(p,t,bad)
        bad = copy.deepcopy(p);bad['endpoint']['Y']='0'
        with self.assertRaisesRegex(ValueError,'GLUE'):m.validate_binding(bad,t,g)

    def test_rejects_wrong_cell_before_computation(self):
        path = ROOT / 'q048_v114_proof.py'
        self.assertTrue(path.exists(), 'V114 cell-binding implementation is missing')
        s=importlib.util.spec_from_file_location('v114',path)
        m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
        read=lambda n:json.loads((ROOT/'inputs'/n).read_bytes())
        p=read('Q048_V113_SOURCE_CORRECT_ACTUAL_CONSUMER_ACCEPTED_CHECKPOINT_V1.json')
        t=read('Q048_V114_NEXT_MATHEMATICS_TASK_V1.json')
        g=read('q048_guard_local_v_result_v12.json')
        t['cell_z']=[930,930]
        with self.assertRaisesRegex(ValueError,'CELL'):m.validate_binding(p,t,g)

if __name__=='__main__':unittest.main()
