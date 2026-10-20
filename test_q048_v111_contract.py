"""Synthetic validator controls only; never admit or execute an actual cell."""
import copy
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent



def control_fixture(m, a):
    p,t,g,i = (a[n] for n in (m.PARENT,m.THEOREM,m.GUARD,m.INGEST))
    row=g['evaluators'][0]['rows'][49]; th=t
    s=m.load(ROOT/m.SPEC)
    return {
        'schema':'bubbleverse.q048.v111.source_correct_actual_consumer.raw.v1',
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
            'primary_row_sha256':m.ROW_HASH,'index':49,'control_role':'GUARD_ONLY',
            'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],
            'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True},
        'candidate_actual':{'count':113,'frontier':950,
            'frontiers':dict(p['frontiers'],**{'hillipop-ede_n3':950}),
            'endpoint':s['endpoint_crosscheck'],'K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
        'task_authorization_sha256':m.PINS[m.TASKFILE],'theorem_postaccept_sha256':m.PINS[m.POST],'authorization_sha256':m.PINS[m.INGEST],'cell_z':[960,950],'cell_a':['1/961','1/951'],
        'new_actual_cells':1,'new_mathematical_proof_cells':0,'new_full_theorem_recomputations':0,
        'theorem_consumptions':1,'below950_work':False,'historical_record_modified':False,
        'historical_v101_v102_replayed':False,'scientific_state':'INCONCLUSIVE',
        'q_complete':False,'NativeP6':'UNRESOLVED','no_native_trajectory_claim':True,'no_physical_reset':True}

class AdmissionContract(unittest.TestCase):
    def test_actual_validator_rejects_semantic_mutations(self):
        path = ROOT / 'q048_v111_verify.py'
        self.assertTrue(path.exists(), 'V111 fresh-proof admission validator is missing')
        module_spec = importlib.util.spec_from_file_location('v109_verifier', path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        authorities = module.load_authorities(ROOT / 'inputs')
        # Fixture is explicitly synthetic and is never written as a scientific result.
        fixture = control_fixture(module, authorities)
        self.assertTrue(all(module.check_result(fixture, authorities).values()))
        for name, mutated in module.mutations(fixture).items():
            with self.subTest(mutation=name):
                checks = module.check_result(mutated, authorities)
                self.assertFalse(all(checks.values()), 'validator accepted ' + name)
        self.assertTrue(all(module.check_result(fixture, authorities).values()), 'mutation contaminated original')

    def test_wrong_authority_bytes_are_rejected(self):
        path = ROOT / 'q048_v111_verify.py'
        self.assertTrue(path.exists(), 'V111 byte pin enforcement is missing')
        module_spec = importlib.util.spec_from_file_location('v109_verifier', path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as d:
            for name in module.PINS:
                shutil.copyfile(ROOT / 'inputs' / name, pathlib.Path(d) / name)
            p = pathlib.Path(d) / module.PARENT
            p.write_bytes(p.read_bytes() + b' ')
            with self.assertRaisesRegex(ValueError, 'byte pin'):
                module.load_authorities(pathlib.Path(d))


if __name__ == '__main__':
    unittest.main()

class PostacceptControls(unittest.TestCase):
    def test_all_checkpoint_mutations_change_the_record(self):
        path=ROOT/'q048_v111_postaccept.py'
        module_spec=importlib.util.spec_from_file_location('v111_post',path)
        module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
        self.assertTrue(hasattr(module,'checkpoint_mutations'),'V111 checkpoint mutation generator is missing')
        c={'parent_sha256':'a'*64,'theorem_acceptance_sha256':'b'*64,'guard_primary_row_sha256':'c'*64,'no_physical_reset':True,'accepted_actual':{'count':113,'frontier':950},'endpoint':{'E':'2'},'new_actual_cells':1,'new_mathematical_proof_cells':0}
        muts=module.checkpoint_mutations(c)
        self.assertEqual(len(muts),8)
        for name,mut in muts.items():self.assertNotEqual(c,mut,name)
        self.assertEqual(muts['below950']['accepted_actual']['frontier'],940)
