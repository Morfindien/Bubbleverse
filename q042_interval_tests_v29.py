"""Finite Q-042 arithmetic/branch/source checks. No cosmological validation."""
import math, unittest
from fractions import Fraction as F
from q042_interval_v29 import I, BackendError, cells, spline_piece

class Arithmetic(unittest.TestCase):
    def enclosed(self, iv, exact):
        self.assertLessEqual(F(iv.lo), exact)
        self.assertGreaterEqual(F(iv.hi), exact)

    def test_directed_rational_operations(self):
        values=[0.,-0.,1.,-1.,.1,-.3,1e-100,1e100,math.nextafter(1.,2.),math.ulp(0.)]
        for a in values:
            for b in values:
                for iv,exact in [(I(a)+b,F(a)+F(b)),(I(a)-b,F(a)-F(b))]: self.enclosed(iv,exact)
                if abs(a*b)!=math.inf: self.enclosed(I(a)*b,F(a)*F(b))
                if b and abs(a/b)!=math.inf: self.enclosed(I(a)/b,F(a)/F(b))

    def test_transcendental_known_values_and_inverses(self):
        self.assertEqual(I(0).exp().pair(),[1.,1.])
        self.assertEqual(I(1).log().pair(),[0.,0.])
        self.assertEqual(I(4).sqrt().pair(),[2.,2.])
        self.assertEqual(I(0).tanh().pair(),[0.,0.])
        for x in [.0001,.1,1.,3.,30.]:
            self.assertTrue(I(x).log().exp().contains(x))
            self.assertTrue((I(x).sqrt()*I(x).sqrt()).contains(x))
        self.assertEqual(I(-1000).exp().lo,0.)
        self.assertGreater(I(-1000).exp().hi,0.)
        self.assertTrue(I(-2,3).tanh().lo<0<I(-2,3).tanh().hi)

    def test_rejected_domains(self):
        for fn in [lambda:I(-1,1).log(),lambda:I(-1,1).sqrt(),lambda:I(1)/I(-1,1),lambda:I(float('nan')),lambda:I(2,1)]:
            with self.assertRaises(BackendError): fn()

    def test_all_intersected_clamped_cells(self):
        self.assertEqual([i for i,q in cells(I(-.1,2.1),5)],[1,2])
        self.assertEqual([i for i,q in cells(I(1.9,3.1),6)],[1,2,3])
        self.assertEqual([i for i,q in cells(I(90,110),100)],[*range(89,98)]) # boundary closure included

    def test_cubic_detects_interior_negative_despite_positive_nodes(self):
        self.assertLess(spline_piece(I(.5),0.,1.,1.,1.,12.,12.).hi,0.)
        for t in [0.,.125,.5,.875,1.]:
            got=spline_piece(I(t),0.,1.,2.,5.,0.,0.)
            self.enclosed(got,F(2)+3*F(t))

if __name__=='__main__': unittest.main()
