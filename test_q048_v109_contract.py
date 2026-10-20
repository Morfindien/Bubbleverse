"""Synthetic validator controls only; never admit or execute an actual cell."""
import copy
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent



def control_fixture(m, a):
    p,t,g,i = (a[n] for n in (m.PARENT,m.THEOREM,m.GUARD,m.INGEST))
    row=g['evaluators'][0]['rows'][48]; th=t['retained_theorem']
    s=m.load(ROOT/m.SPEC)
    return {
        'schema':'bubbleverse.q048.v109.source_correct_actual_consumer.raw.v1',
        'q':'Q048','target_q':'Q048','task_id':m.TASK,'task_fingerprint':i['next_task_fingerprint'],
        'question_sha256':m.QUESTION_HASH,'exact_question':s['exact_question'],
        'spec_sha256':m.SPEC_HASH,'status':'PENDING_VALIDATION',
        'parent_authority':{'record':m.PARENT,'sha256':m.PINS[m.PARENT],
                            'actual':p['accepted_actual'],'endpoint':p['endpoint'],'frontiers':p['frontiers']},
        'theorem_authority':{'record':m.THEOREM,'sha256':m.PINS[m.THEOREM],
            'raw_sha256':m.PINS[m.RAW],'verification_sha256':m.PINS[m.VER],
            'correct_saha_fact':'3.016103031869581e21','thermal_domain':th['thermal_domain'],
            'K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
        'guard_binding':{'source_record':m.GUARD,'source_record_sha256':m.PINS[m.GUARD],
            'primary_row_sha256':m.ROW_HASH,'index':48,'control_role':'GUARD_ONLY',
            'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],
            'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True},
        'candidate_actual':{'count':112,'frontier':960,
            'frontiers':dict(p['frontiers'],**{'hillipop-ede_n3':960}),
            'endpoint':s['endpoint_crosscheck'],'K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
        'authorization_sha256':m.PINS[m.INGEST],'cell_z':[970,960],'cell_a':['1/971','1/961'],
        'new_actual_cells':1,'new_mathematical_proof_cells':0,'new_full_theorem_recomputations':0,
        'theorem_consumptions':1,'below960_work':False,'historical_record_modified':False,
        'historical_v101_v102_replayed':False,'scientific_state':'INCONCLUSIVE',
        'q_complete':False,'NativeP6':'UNRESOLVED','no_native_trajectory_claim':True,'no_physical_reset':True}

class AdmissionContract(unittest.TestCase):
    def test_actual_validator_rejects_semantic_mutations(self):
        path = ROOT / 'q048_v109_verify.py'
        self.assertTrue(path.exists(), 'V109 independent admission validator has not been implemented')
        module_spec = importlib.util.spec_from_file_location('v109_verifier', path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        authorities = module.load_authorities(ROOT / '../inputs')
        # Fixture is explicitly synthetic and is never written as a scientific result.
        fixture = control_fixture(module, authorities)
        self.assertTrue(all(module.check_result(fixture, authorities).values()))
        for name, mutated in module.mutations(fixture).items():
            with self.subTest(mutation=name):
                checks = module.check_result(mutated, authorities)
                self.assertFalse(all(checks.values()), 'validator accepted ' + name)
        self.assertTrue(all(module.check_result(fixture, authorities).values()), 'mutation contaminated original')

    def test_wrong_authority_bytes_are_rejected(self):
        path = ROOT / 'q048_v109_verify.py'
        self.assertTrue(path.exists(), 'V109 byte pin enforcement has not been implemented')
        module_spec = importlib.util.spec_from_file_location('v109_verifier', path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as d:
            for name in module.PINS:
                shutil.copyfile(ROOT / '../inputs' / name, pathlib.Path(d) / name)
            p = pathlib.Path(d) / module.PARENT
            p.write_bytes(p.read_bytes() + b' ')
            with self.assertRaisesRegex(ValueError, 'byte pin'):
                module.load_authorities(pathlib.Path(d))


if __name__ == '__main__':
    unittest.main()
