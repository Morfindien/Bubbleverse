"""Finite regression/reference checks for the Q048 prefix component."""
import copy, json, unittest, tempfile
from fractions import Fraction as F
from pathlib import Path
import q047_math_v1 as m

class PrefixTests(unittest.TestCase):
    def engine(self):
        import q048_prefix_v1 as p
        return p

    def test_component_exists_and_does_not_claim_full_history(self):
        self.assertTrue((Path(__file__).parent/'q048_prefix_v1.py').is_file(),
                        'Required continuous prefix component is not implemented')
        self.assertEqual(self.engine().FINAL_SCOPE,'CONDITIONAL_SOURCE_REAL_PREFIX')

    def test_exact_input_rejects_binary_float_and_nonfinite(self):
        p=self.engine()
        for v in (True,0.1,float('nan')):
            with self.assertRaises(ValueError):p.exact(v)
        self.assertEqual(p.exact('1/3'),F(1,3))

    def test_analytic_decay_is_enclosed_by_residual_certificate(self):
        p=self.engine();cell={'t0':'0','t1':'1/10','predictor':[['1','-1/10']],
                              'box':[['4/5','6/5']]}
        report=p.certify(cell,[m.I(1)],lambda t,y:[-y[0]])
        self.assertTrue(report['closed'])
        end=m.exp_i(m.I(-F(1,10)));lo,hi=map(F,report['endpoint'][0])
        self.assertLessEqual(lo,end.lo);self.assertGreaterEqual(hi,end.hi)

    def test_bad_tube_is_rejected_even_with_forged_pass(self):
        p=self.engine();cell={'t0':'0','t1':'1/10','predictor':[['1','-1/10']],
                              'box':[['1','1']],'certificate':{'closed':True}}
        self.assertFalse(p.certify(cell,[m.I(1)],lambda t,y:[-y[0]])['closed'])

    def test_nonmonotone_step_is_rejected(self):
        p=self.engine()
        with self.assertRaises(ValueError):
            p.certify({'t0':'1','t1':'0','predictor':[['1']],
                       'box':[['0','2']]},[m.I(1)],lambda t,y:[-y[0]])

    def test_lower_cost_trigonometry_encloses_independent_reference(self):
        p=self.engine()
        self.assertTrue(hasattr(p,'trig32'),'Proved lower-cost primitive is missing')
        for cosine in (False,True):
            box=m.I('2999/1000','3001/1000')
            a=p.trig32(box,cosine);b=p.PINNED_TRIG(box,cosine)
            self.assertLessEqual(a.lo,b.lo);self.assertGreaterEqual(a.hi,b.hi)
        y=p.trig32(m.A(m.I(0),[m.I(1),m.I(0)]))
        self.assertEqual(y.v.lo,0);self.assertEqual(y.v.hi,0)
        self.assertLessEqual(y.d[0].lo,1);self.assertGreaterEqual(y.d[0].hi,1)

    def test_captured_neutrinos_are_not_analytically_replaced(self):
        p=self.engine();c=json.loads((Path(__file__).parent/'q048_prefix_config_v1.json').read_text())
        t=p.parameters(c['cases']['camspec-lcdm'])
        self.assertEqual(t['neutrinos'][0]['reference'],'FINITE_NATIVE')
        self.assertEqual(len(t['neutrinos'][0]['nodes']),11)

    def test_no_boolean_can_admit_actual_scientific_result(self):
        p=self.engine()
        with self.assertRaises(ValueError):p.validate_config({'actual_reference_qualified':True})

    def test_missing_jobs_cannot_be_merged_as_complete(self):
        import q048_prefix_merge_v1 as merge
        config=json.loads((Path(__file__).parent/'q048_prefix_config_v1.json').read_text())
        with tempfile.TemporaryDirectory() as d:
            r=merge.collect(d,config)
        self.assertEqual(r['execution_status'],'PARTIAL')
        self.assertEqual(r['job_completeness_gate'],'FAIL')
        self.assertEqual(r['final_result_gate'],'UNRESOLVED')
        self.assertEqual(set(r['missing_jobs']),set(self.engine().CASES))

    def test_forged_final_pass_cannot_enter_merge(self):
        import q048_prefix_merge_v1 as merge
        p=self.engine();config=json.loads((Path(__file__).parent/'q048_prefix_config_v1.json').read_text())
        case=p.CASES[0]
        report={'q':p.Q,'program_id':p.ID,'version':'v1','configuration':case,
                'source_commit':p.SOURCE,'scope':p.FINAL_SCOPE,
                'scientific_question':config['scientific_question'],
                'source_input_hashes':config['cases'][case]['source_input_hashes'],
                'final_result_gate':'PASS','actual_source_admission':'PASS'}
        with tempfile.TemporaryDirectory() as d:
            Path(d,'forged_prefix_v1.json').write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError,'UNSUPPORTED_SCIENTIFIC_PASS'):merge.collect(d,config)

    def test_package_checker_exists(self):
        self.assertTrue((Path(__file__).parent/'q048_prefix_package_check_v1.py').is_file(),
                        'Package/source binding checker missing')

if __name__=='__main__':unittest.main(verbosity=2)
