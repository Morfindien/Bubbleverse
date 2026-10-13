import copy, json, math, os, unittest
from fractions import Fraction as F
from pathlib import Path

import q048_threshold_anchor_v9 as e

ROOT=Path(__file__).resolve().parent


def parent_path(env_name,default):
    return Path(os.environ.get(env_name,default))


class ThresholdAnchorV9Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        e.validate_sources()
        cls.p6=e.load_v6(parent_path('Q048_V6_PARENT','v6_parent/q048_structural_final_v6.json'))
        cls.p7=e.load_v7(parent_path('Q048_V7_PARENT','v7_parent/q048_guard_final_v7.json'))
        cls.p8=e.load_v8(parent_path('Q048_V8_PARENT','v8_parent/q048_phase_turn_final_v8.json'))
        cls.witness,cls.t,cls.row=e.reverify_witness(cls.p7,cls.p8)
        cls.constants=e.threshold_constants(cls.p6,cls.t)

    def test_001_identity_and_scope(self):
        s=e.settings()
        self.assertEqual(s['program_id'],'Q048-THRESHOLD-V9')
        self.assertEqual(s['q'],'Q-048')
        self.assertEqual(s['source_commit'],e.SOURCE)
        self.assertEqual(s['final_result_gate'],'UNRESOLVED')
        self.assertEqual(s['actual_xe_history_bounds'],'NOT_COMPUTED')
        self.assertEqual(s['actual_tau_T_bounds'],'NOT_COMPUTED')

    def test_010_official_parent_chain(self):
        gate=e.verify_artifact_chain(self.p6,self.p7,self.p8)
        self.assertEqual(gate['gate'],'PASS_OFFICIAL_V6_V7_V8_CHAIN')

    def test_020_v8_cell27_recomputed_and_first(self):
        w=self.witness
        self.assertEqual(w['gate'],'PASS_REVERIFIED_V8_WITNESS')
        self.assertEqual(w['cell_index_zero_based'],27)
        self.assertLess(F(w['theta_endpoint'][1]),F(2))
        self.assertGreater(F(w['y_endpoint'][0]),0)

    def test_030_positive_negative_theta_source_sign(self):
        # q047's validated trig enclosure is midpoint-Taylor plus a
        # derivative<=1 radius term.  A very wide [0.1,2] tube is therefore
        # intentionally too loose to separate sin(theta)'s sign even though
        # the exact Mathematics-009 theorem does.  Use narrow finite controls
        # here to verify the implementation's source-sign orientation without
        # pretending this numerical sanity check reproves the theorem.
        up,dup,_=e.v8.theta_potential(e.m.I(F(1,10),F(1,5)),self.t)
        un,dun,_=e.v8.theta_potential(e.m.I(F(-1,5),F(-1,10)),self.t)
        self.assertGreater(dup.lo,0)
        self.assertLess(dun.hi,0)
        self.assertGreaterEqual(up.lo,0)
        self.assertGreaterEqual(un.lo,0)

    def test_040_static_threshold_gates(self):
        g=e.static_threshold_gates(self.constants,self.t)
        self.assertEqual(g['gate'],'PASS_STATIC_THRESHOLD_GATES')
        self.assertTrue(all(F(v['margin_lower'])>0 for v in g['values'].values()))

    def test_050_energy_map_32_passes(self):
        E0=F(self.witness['splice']['e_endpoint'][1])
        r=e.energy_map(self.constants,self.t,E0)
        self.assertEqual(r['gate'],'PASS_ENERGY_MAP')
        self.assertLess(F(r['final_E_upper']),F(r['T_lower']))
        self.assertGreater(F(r['margin_lower']),0)
        self.assertEqual(r['bins_requested'],32)

    def test_060_timing_sum_32_passes(self):
        r=e.timing_sum(self.constants,self.witness,self.t)
        self.assertEqual(r['gate'],'PASS_TIMING_SUM')
        self.assertLess(F(r['J_upper']),F(r['delta_u_safe_lower']))
        self.assertGreater(F(r['margin_lower']),0)

    def test_070_refinement_direction(self):
        E0=F(self.witness['splice']['e_endpoint'][1])
        a=e.energy_map(self.constants,self.t,E0,32)
        b=e.energy_map(self.constants,self.t,E0,64)
        ta=e.timing_sum(self.constants,self.witness,self.t,32)
        tb=e.timing_sum(self.constants,self.witness,self.t,64)
        self.assertLessEqual(F(b['final_E_upper']),F(a['final_E_upper']))
        self.assertLessEqual(F(tb['J_upper']),F(ta['J_upper']))

    def test_080_finite_certificate_passes(self):
        c,_,_,_=e.finite_certificate(self.p6,self.p7,self.p8)
        self.assertEqual(c['status'],'PASS_CONDITIONAL_THRESHOLD_ANCHOR_GUARD')
        self.assertEqual(c['theorem_gate'],'PASS_THRESHOLD_OR_TURN_EXISTENCE_BEFORE_V6_SAFE_HORIZON')
        self.assertEqual(c['guard_consequence'],'PASS_CONDITIONAL_SOURCE_GUARD_TO_Z2870')

    def test_090_log_lower_positive_series_control(self):
        r=e.timing_sum(self.constants,self.witness,self.t)
        ratio=F(r['ratio'])
        n=e.settings()['certificate']['log_series_terms']
        low=e._log_lower_gt_one(ratio,n)
        tighter=e._log_lower_gt_one(ratio,n+1)
        # Positive-term atanh series: every finite partial sum is a strict
        # lower bound and adding the next positive term must increase it.
        self.assertGreater(low,0)
        self.assertGreater(tighter,low)
        self.assertEqual(str(low),r['delta_u_safe_lower'])

    def test_100_witness_mutation_fails(self):
        bad=copy.deepcopy(self.p8)
        bad['camspec_record']['extension']['phase_turn']['cells'][27]['certificate']['endpoint'][0][1]='3'
        with self.assertRaises(ValueError):
            e.reverify_witness(self.p7,bad)

    def test_110_full_derive_and_recompute(self):
        obj=e.derive(self.p6,self.p7,self.p8)
        self.assertEqual(obj['certificate']['status'],'PASS_CONDITIONAL_THRESHOLD_ANCHOR_GUARD')
        self.assertEqual(obj['thermal']['status'],'PASS_CONDITIONAL_TO_H_ENTRY')
        self.assertNotEqual(obj['thermal']['h_entry_q'],'NOT_COMPUTED')
        self.assertEqual(obj['actual_event_redshift'],'NOT_COMPUTED')
        self.assertEqual(obj['actual_xe_history_bounds'],'NOT_COMPUTED')
        self.assertEqual(obj['actual_tau_T_bounds'],'NOT_COMPUTED')
        v=e.verify_extension(obj,self.p6,self.p7,self.p8)
        self.assertEqual(v['gate'],'PASS_RECOMPUTED_V9_EXTENSION')


if __name__=='__main__':
    unittest.main()
