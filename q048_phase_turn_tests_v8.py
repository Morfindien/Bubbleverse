"""Finite adversarial and binding controls for Q048 V8."""
import copy,os,tempfile,unittest
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch
import q048_phase_turn_v8 as e
import q048_phase_turn_runner_v8 as r

PARENT_ENV='Q048_V7_PARENT'

class StaticMathControls(unittest.TestCase):
    def test_identity_and_scope(self):
        s=e.settings();self.assertEqual(s['q'],'Q-048');self.assertEqual(s['program_id'],'Q048-PHASETURN-V8')
        self.assertEqual(s['math_result_id'],'I-PROPOSED-Q048-MATHEMATICS-008')
        self.assertEqual(s['phase_turn']['method'],'source_root_phase_energy_first_turn_guard_v1')
        self.assertEqual(s['phase_turn']['state_coordinates'],['theta=lambda*phi','y=-X'])
        self.assertEqual(F(s['thermal']['start_a']),F(1,4601));self.assertEqual(F(s['thermal']['end_a']),F(1,2871))

    def test_phase_constants_and_energy_identity_shape(self):
        row=e.v6.config()['cases']['camspec-ede_n3'];t=e.p.parameters(row);c=e.phase_constants(t)
        self.assertGreater(c['lambda'].lo,0);self.assertGreater(c['A'].lo,0);self.assertGreaterEqual(c['floor'].lo,0)
        # y=-X is signed and globally smooth; scalar energy uses y^2 and is invariant under sign.
        th=e.m.I(F(1,10));yp=e.m.I(2);yn=e.m.I(-2)
        up,_,_=e.theta_potential(th,t)
        ep=e.pre.square(yp)/2+up;en=e.pre.square(yn)/2+up
        self.assertEqual((ep.lo,ep.hi),(en.lo,en.hi))

    def test_phase_values_guard_margin_equivalent_shape(self):
        row=e.v6.config()['cases']['camspec-ede_n3'];t=e.p.parameters(row)
        th=e.m.I(F(1,10));y=e.m.I(1);a=e.m.I(F(1,9000))
        v=e.phase_values(a,[th,y],t)
        self.assertGreater(v['H'].lo,0);self.assertGreater(v['e'].lo,0)
        # Direct ratio and algebraic margin are evaluated from the same exact-real state.
        self.assertGreater(v['guard_ratio'].lo,0)

    def test_unexpected_certificate_error_remains_fail_closed(self):
        fake={'t0':'0','t1':'1','predictor':[['0','0'],['1','0']],'box':[['-1','1'],['0','2']]}
        with patch.object(e,'_phase_predictor_and_box',return_value=(object(),fake)):
            with patch.object(e.pre,'certify_cell',side_effect=ValueError('UNEXPECTED_CERTIFICATE_FAILURE')):
                with self.assertRaisesRegex(ValueError,'UNEXPECTED_CERTIFICATE_FAILURE'):
                    e._phase_cell(F(1,10),F(11,100),[e.m.I(0),e.m.I(1)],None)

    def test_comparison_growth_cap_requests_refinement(self):
        fake={'t0':'0','t1':'1','predictor':[['0','0'],['1','0']],'box':[['-1','1'],['0','2']]}
        with patch.object(e,'_phase_predictor_and_box',return_value=(object(),fake)):
            with patch.object(e.pre,'certify_cell',side_effect=ValueError('COMPARISON_GROWTH_CAP')):
                accepted,reason,cell,report,vals=e._phase_cell(F(1,10),F(11,100),[e.m.I(0),e.m.I(1)],None)
        self.assertIsNone(accepted);self.assertEqual(reason,'CERTIFICATE_COMPARISON_GROWTH_CAP');self.assertIsNone(report);self.assertIsNone(vals)

class ParentBindingControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=os.environ.get(PARENT_ENV)
        if not cls.path or not Path(cls.path).is_file():raise unittest.SkipTest('official V7 parent artifact not supplied')
        cls.parent=e.load_parent(cls.path)

    def test_official_parent_identity(self):
        self.assertEqual(self.parent['program_id'],'Q048-GUARDCONT-V7')
        self.assertEqual(self.parent['job_completeness_gate'],'PASS')
        self.assertEqual(self.parent['final_result_gate'],'UNRESOLVED')

    def test_exact_splice_reverification_and_transform_gate(self):
        sp,state,t,row=e.verify_splice(self.parent)
        self.assertEqual(sp['gate'],'PASS_REVERIFIED_V7_SPLICE')
        self.assertGreater(F(sp['y_endpoint'][0]),0)
        self.assertGreater(F(sp['theta_endpoint'][0]),0)
        self.assertLess(F(sp['theta_endpoint'][1]),e.m.C['pi'].lo)
        self.assertGreater(F(sp['kinetic_gap_rectangular'][0]),0)
        self.assertLess(F(sp['e_endpoint'][1]),8*F(sp['A'][0]))

    def test_parent_scope_cannot_be_upgraded_by_binding(self):
        bad=copy.deepcopy(self.parent);bad['actual_source_admission']='PASS'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';e.proof.write(p,bad)
            with self.assertRaises(ValueError):e.load_parent(p)

class RunnerControls(unittest.TestCase):
    def test_collection_requires_one_worker(self):
        if not os.environ.get(PARENT_ENV):raise unittest.SkipTest('official V7 parent artifact not supplied')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'JOB_COMPLETENESS'):
                r.collect(d,os.environ[PARENT_ENV],full=False)

if __name__=='__main__':unittest.main()
