import unittest,importlib.util
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
class SourceBoundary(unittest.TestCase):
 def module(self):
  p=ROOT/'q048_v122_diagnostic.py';self.assertTrue(p.exists(),'V122 diagnostic implementation is missing')
  s=importlib.util.spec_from_file_location('diagnostic',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
 def test_exact900_uses_initial_one(self):
  m=self.module();self.assertEqual(m.point_dispatch(F(900),F(1,100),F(1),F(1),F(8),'READY')['Pion'],'1')
 def test_below900_evaluates_probability(self):
  m=self.module();r=m.point_dispatch(F(899),F(1,100),F(1),F(1),F(8),'READY');self.assertEqual(r['Pion'],'1/309');self.assertEqual(r['dispatch'],'HMLA')
 def test_threshold_equality_uses_otherwise(self):
  m=self.module();r=m.point_dispatch(F(899),F(3,91),F(1),F(1),F(8),'READY');self.assertEqual(r['Pion'],'1/100');self.assertEqual(r['dispatch'],'SWIFT')
 def test_changed_source_and_wrong_model_rejected(self):
  m=self.module();c=(ROOT/'inputs/source/hydrogen.c').read_bytes();h=(ROOT/'inputs/source/hydrogen.h').read_bytes();m.check_source(c,h,4)
  with self.assertRaises(ValueError):m.check_source(c+b' ',h,4)
  with self.assertRaises(ValueError):m.check_source(c,h,3)
 def test_missing_h_premise_explicitly_unresolved(self):
  m=self.module();self.assertEqual(m.reachable_tube_status(None),'UNRESOLVED_NO_CONNECTED_H_LOWER')
  with self.assertRaises(ValueError):m.point_dispatch(F(899),F(0),F(1),F(1),F(8),'READY')
 def test_threshold_straddling_cover_keeps_both(self):
  m=self.module();self.assertEqual(m.interval_cover(F(1,100),F(1,10),F(1),F(1),F(1),F(1),F(8),F(8)),['HMLA','SWIFT_SUBJECT_TO_TEMPERATURE_GATE'])
 def test_neutral_h_definition_conflicts_with_canonical_proton_h(self):
  m=self.module();import json
  t=json.loads((ROOT/'inputs/Q048_V122_NEXT_MATHEMATICS_TASK_V1.json').read_bytes())
  k=(ROOT/'inputs/q048_full_tube_reuse_v1.py').read_text()
  self.assertEqual(m.variable_identity(t,k,'h=xHII')['status'],'CONFLICT')
if __name__=='__main__':unittest.main()
