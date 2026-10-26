from pathlib import Path
import csv, importlib.util, json, tempfile, unittest
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("q052",HERE/"q052_native_pair_v2.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Q052Tests(unittest.TestCase):
    def test_contract_freeze(self):
        c=m.package_gate()
        self.assertEqual(c["native_intervention"]["event_redshift"],810.0)
        self.assertFalse(c["native_intervention"]["reionization"]["tau_shooting"])
        self.assertEqual(c["native_intervention"]["arm_L_q_xHeII"],1e-6)
        self.assertEqual(c["native_intervention"]["arm_R_q_xHeII"],0.0)
        self.assertIn("arbitrary Q051 theorem-domain start",c["forbidden"])

    def test_static_semantics(self):
        x=m.static()
        self.assertEqual(x["package_gate"],"PASS")
        self.assertEqual(x["program_id_registry_gate"],"PENDING_INSTALL")

    def test_difference_helpers(self):
        a=[{"z":"0","eta_Mpc":"1","xe":"1","cumulative_tau_T":"0"},
           {"z":"1","eta_Mpc":"0","xe":"0.9","cumulative_tau_T":"0.1"}]
        b=[{"z":"0","eta_Mpc":"1","xe":"1","cumulative_tau_T":"0"},
           {"z":"1","eta_Mpc":"0","xe":"0.8","cumulative_tau_T":"0.08"}]
        m.common_grid(a,b)
        self.assertAlmostEqual(m.supabs(m.diff_series(a,b,"xe")),0.1)
        self.assertAlmostEqual(m.supabs(m.diff_series(a,b,"cumulative_tau_T")),0.02)

    def test_grid_mismatch_rejected(self):
        a=[{"z":"0","eta_Mpc":"1"}];b=[{"z":"0.1","eta_Mpc":"1"}]
        with self.assertRaises(ValueError):m.common_grid(a,b)

if __name__=="__main__":unittest.main()
