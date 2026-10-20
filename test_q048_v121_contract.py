"""Synthetic validator controls only; never admit or execute an actual cell."""
import copy
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent



def control_fixture(m, a):
    p,t,g,i = (a[n] for n in (m.PARENT,m.THEOREM,m.GUARD,m.INGEST))
    row=g['evaluators'][0]['rows'][54]; th=t
    s=m.load(ROOT/m.SPEC)
    return {
        'schema':'bubbleverse.q048.v121.source_correct_actual_consumer.raw.v1',
        'source_boundary_certificate':copy.deepcopy(t['source_boundary_certificate']),'proof_validation_requirements':copy.deepcopy(a[m.TASKFILE]['theorem_authority']['validation_requirements']),
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
            'primary_row_sha256':m.ROW_HASH,'index':54,'control_role':'GUARD_ONLY',
            'E_input_left':row['E_input_left'],'Y_left':row['Y_left'],'V_previous':row['V_previous'],
            'source_state_reset':False,'whole_cell_qualified':True,'accepted':True,'committed':True},
        'candidate_actual':{'count':118,'frontier':900,
            'frontiers':dict(p['frontiers'],**{'hillipop-ede_n3':900}),
            'endpoint':s['endpoint_crosscheck'],'K_upper':th['K_upper'],'connected_lower':th['connected_lower']},
        'task_authorization_sha256':m.PINS[m.TASKFILE],'theorem_postaccept_sha256':m.PINS[m.POST],'authorization_sha256':m.PINS[m.INGEST],'cell_z':[910,900],'cell_a':['1/911','1/901'],
        'new_actual_cells':1,'new_mathematical_proof_cells':0,'new_full_theorem_recomputations':0,
        'theorem_consumptions':1,'below900_work':False,'historical_record_modified':False,
        'historical_v101_v102_replayed':False,'scientific_state':'INCONCLUSIVE',
        'q_complete':False,'NativeP6':'UNRESOLVED','no_native_trajectory_claim':True,'no_physical_reset':True}

class AdmissionContract(unittest.TestCase):
    def test_actual_validator_rejects_semantic_mutations(self):
        path = ROOT / 'q048_v121_verify.py'
        self.assertTrue(path.exists(), 'V121 fresh-proof admission validator is missing')
        module_spec = importlib.util.spec_from_file_location('v119_verifier', path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        authorities = module.load_authorities(ROOT / 'inputs')
        # Fixture is explicitly synthetic and is never written as a scientific result.
        fixture = control_fixture(module, authorities)
        self.assertTrue(all(module.check_result(fixture, authorities).values()))
        for name, mutated in module.mutations(fixture).items():
            with self.subTest(mutation=name):
                checks = module.check_result(mutated, authorities)
                self.assertNotEqual(fixture,mutated,name)
                self.assertFalse(all(checks.values()), 'validator accepted ' + name)
        self.assertIn('wrong_raw_schema',module.mutations(fixture))
        authority_controls=module.authority_mutations(authorities)
        self.assertIn('wrong_theorem_schema',authority_controls)
        for name,mutated_sources in authority_controls.items():
            self.assertNotEqual(authorities,mutated_sources,name)
            self.assertFalse(all(module.check_result(fixture,mutated_sources).values()),name)
        self.assertTrue(all(module.check_result(fixture, authorities).values()), 'mutation contaminated original')

    def test_wrong_authority_bytes_are_rejected(self):
        path = ROOT / 'q048_v121_verify.py'
        self.assertTrue(path.exists(), 'V121 byte pin enforcement is missing')
        module_spec = importlib.util.spec_from_file_location('v119_verifier', path)
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
        path=ROOT/'q048_v121_postaccept.py'
        self.assertTrue(path.exists(), 'V121 checkpoint implementation is missing')
        module_spec=importlib.util.spec_from_file_location('v121_post',path)
        module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
        self.assertTrue(hasattr(module,'checkpoint_mutations'),'V121 checkpoint mutation generator is missing')
        c={'source_boundary_certificate':copy.deepcopy(json_boundary()),'proof_validation_requirements':{'verification_checks':31,'semantic_mutations_rejected':18,'postaccept_checks':21,'delivery_checks':35,'preflight_binding_tests':5},'parent_sha256':'a'*64,'theorem_acceptance_sha256':'b'*64,'guard_primary_row_sha256':'c'*64,'no_physical_reset':True,'accepted_actual':{'count':118,'frontier':900},'endpoint':{'E':'2'},'new_actual_cells':1,'new_mathematical_proof_cells':0}
        muts=module.checkpoint_mutations(c)
        self.assertEqual(len(muts),10)
        for name,mut in muts.items():self.assertNotEqual(c,mut,name)
        self.assertEqual(muts['below900']['accepted_actual']['frontier'],890)


def json_boundary():
    import json
    return json.loads((ROOT/'inputs/Q048_V120_SOURCE_CORRECT_PROOF_ACCEPTANCE_V1.json').read_bytes())['source_boundary_certificate']

class BoundaryContract(unittest.TestCase):
    def load_validator(self):
        path=ROOT/'q048_v121_verify.py'
        self.assertTrue(path.exists(),'V121 endpoint900 certificate validator is missing')
        ms=importlib.util.spec_from_file_location('v121_boundary_verify',path)
        m=importlib.util.module_from_spec(ms);ms.loader.exec_module(m)
        a=m.load_authorities(ROOT/'inputs');return m,a,control_fixture(m,a)

    def test_inclusive900_certificate_and_named_boundary_controls(self):
        m,a,r=self.load_validator()
        self.assertTrue(all(m.check_result(r,a).values()))
        controls=m.authority_mutations(a)
        for name in ['boundary_missing','boundary_changed_source','boundary_below900','boundary_cell_mismatch']:
            with self.subTest(name=name):
                self.assertIn(name,controls)
                self.assertNotEqual(a,controls[name])
                self.assertFalse(all(m.check_result(r,controls[name]).values()))
        self.assertEqual(r['source_boundary_certificate']['z_min'],'900')
        self.assertEqual(r['cell_a'][-1],'1/901')

    def test_old_proof_counts_and_delivery_record_are_rejected(self):
        m,a,r=self.load_validator();controls=m.authority_mutations(a)
        for name in ['wrong_proof_verification_count','wrong_proof_mutation_count','wrong_proof_postaccept_count','wrong_proof_delivery_count']:
            with self.subTest(name=name):
                self.assertIn(name,controls)
                self.assertNotEqual(a,controls[name])
                self.assertFalse(all(m.check_result(r,controls[name]).values()))
