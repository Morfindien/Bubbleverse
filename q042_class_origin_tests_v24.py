import copy, unittest
from q042_class_origin_v24 import summarize_trace

def observed_events():
    # Explicit test observations, not a computed cosmological result.
    return [
      {'event':'input','reio_z_or_tau':1,'tau_reio':0.022146719553358576},
      {'event':'tau_enter','requested_tau':0.022146719553358576},
      {'event':'get_tau','call':1,'status':0,'computed_tau':'NaN'},
      {'event':'get_tau','call':2,'status':0,'computed_tau':'NaN'},
      {'event':'tau_exit','status':0},
      {'event':'final','tau_calls':1,'get_tau_calls':2,'source_calls':6,'trace_overflow':False},
    ]

class TraceGateTests(unittest.TestCase):
    def test_nonfinite_optical_depth_is_preserved_as_a_usable_trace(self):
        r=summarize_trace(observed_events(),0.022146719553358576)
        self.assertEqual(r['trace_gate'],'PASS')
        self.assertEqual(r['tau_bracket'],['NaN','NaN'])
        self.assertEqual(r['bracket_finite'],False)
        self.assertEqual(r['bisection_iterations'],0)
        self.assertIs(r['scientific_result'],False)
        self.assertIs(r['production_restart_authorized'],False)

    def test_inactive_interposition_cannot_claim_a_trace(self):
        e=observed_events();e[-1]['tau_calls']=0
        with self.assertRaises(ValueError):summarize_trace(e,0.022146719553358576)

    def test_missing_lower_trial_cannot_claim_complete_bracket(self):
        e=observed_events();del e[3]
        with self.assertRaises(ValueError):summarize_trace(e,0.022146719553358576)

    def test_changed_requested_tau_is_rejected(self):
        e=observed_events();e[0]['tau_reio']=0.05
        with self.assertRaises(ValueError):summarize_trace(e,0.022146719553358576)

    def test_finite_bracket_is_not_reclassified_as_nan(self):
        e=observed_events();e[2]['computed_tau']=0.2;e[3]['computed_tau']=0.001
        r=summarize_trace(e,0.022146719553358576)
        self.assertIs(r['bracket_finite'],True)
        self.assertEqual(r['tau_bracket'],[0.2,0.001])
        self.assertIs(r['scientific_result'],False)

    def test_truncated_observation_is_rejected(self):
        e=observed_events();e[-1]['trace_overflow']=True
        with self.assertRaises(ValueError):summarize_trace(e,0.022146719553358576)

if __name__=='__main__':unittest.main()
