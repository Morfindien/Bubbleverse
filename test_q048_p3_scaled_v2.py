import unittest, json, hashlib, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from q048_p3_scaled_arithmetic_v2 import *
from q048_p3_scaled_kernel_v2 import *

class TestP3ScaledV2(unittest.TestCase):
    def test_pinned_table_hashes(self):
        cfg=json.loads((HERE/'q048_p3_scaled_config_v2.json').read_text())
        for rel,rec in cfg['inputs'].items():
            p=ROOT/rel
            self.assertTrue(p.exists(),rel)
            self.assertEqual(len(p.read_bytes()),rec['bytes'])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),rec['sha256'])
    def test_r0_math018_generalized(self):
        tok=(ROOT/'p3deps/R_inf.dat').read_text().split()[0]
        rec=table_log_union(tok)
        pL=primary_exp_point(rec['lo']);pU=primary_exp_point(rec['hi'])
        cL=control_exp_point(rec['lo']);cU=control_exp_point(rec['hi'])
        self.assertLess(pL.hi_fraction,rec['qlo']);self.assertGreater(pU.lo_fraction,rec['qhi'])
        self.assertLess(cL.hi_fraction,rec['qlo']);self.assertGreater(cU.lo_fraction,rec['qhi'])
    def test_dynamic_sub_1e120_positive(self):
        for x in [F(-1000),F(-621),F(-400),F(-30),F(0),F(300)]:
            p=primary_exp_point(x);c=control_exp_point(x)
            self.assertGreater(p.lo,0);self.assertGreater(c.lo,0)
    def test_scaled_product_recip(self):
        a=primary_exp_point(F(-621)); u=unit_scaled(a.p)
        b=scaled_mul(a,u); self.assertGreater(b.lo,0)
        r=scaled_recip(a); rr=scaled_recip(r)
        self.assertGreater(r.lo,0)
        self.assertLessEqual(rr.lo_fraction,a.lo_fraction)
        self.assertGreaterEqual(rr.hi_fraction,a.hi_fraction)
    def test_basis_and_norm(self):
        self.assertEqual(basis_polynomials(),lagrange_polynomials())
        n=norm_certificate();self.assertEqual(n['primary_norm'],2);self.assertTrue(0<n['control_norm']<4)
    def test_stencil_endpoints(self):
        self.assertEqual(stencil(F(0),100),(1,F(-1)))
        self.assertEqual(stencil(F(99),100),(97,F(2)))
    def test_table_shapes(self):
        self.assertEqual(len(load_tokens(ROOT/'p3deps/Alpha_inf.dat')),16000)
        self.assertEqual(len(load_tokens(ROOT/'p3deps/R_inf.dat')),100)
        self.assertEqual(len(load_tokens(ROOT/'p3deps/fit_swift.dat')),1325)
    def test_all_four_init_and_fit_loader(self):
        cap=json.loads((ROOT/'p3deps/q048_prefix_config_v1.json').read_text())
        old=json.loads((ROOT/'p3deps/q048_builder_admission_result_v1.json').read_text())
        init=initialize_cases(cap,old);self.assertEqual(len(init),4)
        rows=load_fit(ROOT/'p3deps/fit_swift.dat');self.assertEqual(len(rows),265)

if __name__=='__main__': unittest.main(verbosity=2)
