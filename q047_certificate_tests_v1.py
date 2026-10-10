"""Mandatory numerical and fail-closed Q047 checker tests; no physical fixture."""
import importlib.util
import json
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent

class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('q047_certificate_v1'),
                             'Q047 certificate implementation is required')
        import q047_certificate_v1 as c
        self.c=c

    def test_signed_comparison_preserves_damping(self):
        c=self.c
        E,J=c.comparison_matrices([[F(-2),F(0)],[F(0),F(-3)]],F(1))
        for i,rate in enumerate([F(-2),F(-3)]):
            e=c.math.exp_i(c.math.I(rate))
            self.assertLessEqual(E[i][i].lo,e.lo)
            self.assertGreaterEqual(E[i][i].hi,e.hi)
            self.assertLess(E[i][i].hi,F(1))
            self.assertGreater(J[i][i].lo,F(0))
        self.assertEqual(E[0][1].hi,F(0))

    def test_comparison_handles_repeated_eigenvalue(self):
        c=self.c
        E,J=c.comparison_matrices([[F(-2),F(3)],[F(0),F(-2)]],F(1))
        e=c.math.exp_i(c.math.I(-2))
        self.assertLessEqual(E[0][1].lo,(3*e).lo)
        self.assertGreaterEqual(E[0][1].hi,(3*e).hi)
        self.assertGreater(J[0][1].lo,F(0))

    def test_comparison_zero_and_growth_limits(self):
        c=self.c
        E,J=c.comparison_matrices([[F(0),F(0)],[F(0),F(0)]],F(2))
        self.assertEqual(E[0][0].lo,F(1))
        self.assertEqual(J[0][0].hi,F(2))
        E,J=c.comparison_matrices([[F(2),F(0)],[F(0),F(-2)]],F(1))
        self.assertGreater(E[0][0].lo,F(7))
        with self.assertRaises(ValueError):
            c.comparison_matrices([[F(-2),F(-1)],[F(1),F(-2)]],F(1))

    def test_primitive_enclosures_and_rejected_json(self):
        c=self.c;m=c.math
        for a,b in [(F(1,7),F(2,13)),(F(-17,19),F(31,37))]:
            for got,exact in [(m.I(a)+b,a+b),(m.I(a)*b,a*b),(m.I(a)/b,a/b)]:
                self.assertLessEqual(got.lo,exact);self.assertGreaterEqual(got.hi,exact)
        self.assertEqual(m.exp_i(m.I(0)).lo,F(1))
        self.assertLessEqual(m.sqrt_i(m.I(2)).lo**2,F(2))
        self.assertGreaterEqual(m.sqrt_i(m.I(2)).hi**2,F(2))
        with self.assertRaises(ValueError):c.loads('{"q":1,"q":2}')
        with self.assertRaises(ValueError):c.loads('{"x":NaN}')
        with self.assertRaises(ValueError):c.rational(True)
        with self.assertRaises(ValueError):c.rational(0.1)

    def test_polynomial_controls_detect_interior_excursion(self):
        c=self.c
        got=c.poly_range([F(1),F(-4),F(4)])
        self.assertLessEqual(got.lo,F(0))
        self.assertGreaterEqual(got.hi,F(1))
        self.assertEqual(c.poly_at([F(1),F(-4),F(4)],F(1,2)),F(0))

    def test_inherited_data_never_admits_actual_cases(self):
        c=self.c
        report=c.input_admission(c.load(ROOT/'q047_targets_v1.json'))
        self.assertEqual(set(report),set(c.CASES))
        for case,v in report.items():
            self.assertEqual(v['gate'],'FAIL')
            self.assertEqual(v['actual_applicability'],'INSUFFICIENT_EVIDENCE')
            self.assertIn('qualified_pre_onset_temperature',v['missing_objects'])
            self.assertIn('source_continuum_background_enclosure',v['missing_objects'])

    def test_manufactured_local_upper_event_is_only_conditional(self):
        c=self.c
        packet=c.local_fixture(ROOT/'q047_control_input_v1.json')
        report=c.check_upper_packet(packet)
        self.assertEqual(report['conditional_event_gate'],'PASS',report)
        self.assertEqual(report['scope'],'CONDITIONAL_LOCAL_UPPER_IVP')
        self.assertEqual(report['final_result_gate'],'UNRESOLVED')
        self.assertEqual(report['actual_applicability'],'INSUFFICIENT_EVIDENCE')
        self.assertTrue(report['segments'][0]['invariant_radius_gate'])
        self.assertLess(F(report['segments'][0]['Q_upper']),F(0))

    def test_checker_rejects_forged_qualification_and_wrong_target(self):
        c=self.c
        packet=c.local_fixture(ROOT/'q047_control_input_v1.json')
        packet['actual_reference_qualified']=True
        with self.assertRaisesRegex(ValueError,'UNSUPPORTED_ACTUAL_QUALIFICATION'):
            c.check_upper_packet(packet)
        packet.pop('actual_reference_qualified');packet['source_commit']='main'
        with self.assertRaisesRegex(ValueError,'SOURCE_COMMIT'):
            c.check_upper_packet(packet)

    def test_checker_rejects_gap_and_unsafe_domain(self):
        c=self.c
        packet=c.local_fixture(ROOT/'q047_control_input_v1.json')
        packet['segments'].append(dict(packet['segments'][0]))
        with self.assertRaisesRegex(ValueError,'PARTITION'):
            c.check_upper_packet(packet)
        packet=c.local_fixture(ROOT/'q047_control_input_v1.json')
        packet['segments'][0]['domain'][0]=['-1','1']
        with self.assertRaisesRegex(ValueError,'REGULAR_DOMAIN'):
            c.check_upper_packet(packet)

    def test_native_stopped_predictor_cannot_pass_as_upper_flow(self):
        c=self.c
        packet=c.local_fixture(ROOT/'q047_control_input_v1.json')
        packet['segments'][0]['predictor'][0][1]='0'
        result=c.check_upper_packet(packet)
        self.assertNotEqual(result['conditional_event_gate'],'PASS')

    def test_negative_neighborhood_cannot_shorten_proof_domain(self):
        c=self.c
        packet=c.local_fixture(ROOT/'q047_control_input_v1.json')
        packet['segments'][0]['right_neighborhood']='-0.00000001'
        with self.assertRaisesRegex(ValueError,'RIGHT_NEIGHBORHOOD'):
            c.check_upper_packet(packet)

    def test_optimized_python_cannot_disable_regional_assertions(self):
        import subprocess,sys
        result=subprocess.run([sys.executable,'-O',str(ROOT/'q047_math_v1.py')],capture_output=True)
        self.assertNotEqual(result.returncode,0)

    def test_coupled_matrix_matches_independent_closed_form(self):
        c=self.c
        E,J=c.comparison_matrices([[F(-2),F(1)],[F(1),F(-2)]],F(1))
        e1=c.math.exp_i(c.math.I(-1));e3=c.math.exp_i(c.math.I(-3))
        for got,want in [(E[0][0],(e1+e3)/2),(E[0][1],(e1-e3)/2)]:
            self.assertLessEqual(got.lo,want.lo)
            self.assertGreaterEqual(got.hi,want.hi)

    def test_transcendental_work_cap_is_failure_not_clipping(self):
        with self.assertRaisesRegex(ValueError,'EXP_RANGE_CAP'):
            self.c.math.exp_i(self.c.math.I(401))

    def test_hydrogen_root_encloses_nearly_ionized_onset_without_false_singularity(self):
        m=self.c.math
        h,r,T=m.hydrogen(m.I('.0812','.0816'),m.I('0','.01'),m.I(2870),m.I('2.7254','2.7256'),m.I('.188','.1889'))
        self.assertGreater(h.lo,F(0))
        self.assertLess(h.hi,F(1))
        self.assertGreater((h*(h+m.I('.0812','.0816'))/r).lo,F(0))

if __name__=='__main__':unittest.main(verbosity=2)
