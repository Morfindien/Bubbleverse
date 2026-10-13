"""Finite adversarial controls for Q048 V7 guard/thermal continuation."""
import copy,json,tempfile,unittest
from unittest.mock import patch
from fractions import Fraction as F
from pathlib import Path
import q048_guard_continuation_v7 as e
import q048_guard_runner_v7 as r

class MathControls(unittest.TestCase):
 def test_identity_and_boundaries(self):
  s=e.settings();self.assertEqual(s['q'],'Q-048');self.assertEqual(s['program_id'],e.ID)
  self.assertEqual(F(s['thermal']['start_a']),F(1,4601))
  self.assertEqual(F(s['thermal']['switch_a']),F(1,3551));self.assertEqual(F(s['thermal']['end_a']),F(1,2871))
 def test_rational_voc_is_positive_and_sign_aware(self):
  current=e.m.I(F(1,10_000_000),F(2,10_000_000));c=e.m.I(F(1,100),F(2,100));d=e.m.I(1000,2000)
  x=e.rational_voc_control(current,c,d);self.assertGreater(x.lo,0);self.assertLess(x.lo,x.hi)
  # The independent lower bound drops the positive homogeneous term and is c_min/(1+d_max).
  # The proof backend then rounds outward onto its fixed rational lattice, so equality to the
  # unrounded mathematical fraction is neither required nor generally true.
  exact_lo=c.lo/(1+d.hi);exact_hi=current.hi/(1+d.lo)+c.hi/d.lo
  self.assertEqual(x.lo,e.m.down(exact_lo));self.assertEqual(x.hi,e.m.up(exact_hi))
  self.assertLessEqual(x.lo,exact_lo);self.assertGreaterEqual(x.hi,exact_hi)
  # Changing only the positive lower initial endpoint must not alter this deliberately looser
  # rational lower control, because its homogeneous contribution was safely discarded.
  changed=e.rational_voc_control(e.m.I(F(3,20_000_000),current.hi),c,d)
  self.assertEqual(changed.lo,x.lo)
 def test_direct_guard_margin_equivalence_shape(self):
  row=e.v6.config()['cases']['camspec-ede_n3'];t=e.p.parameters(row);initial,a,state=e.p.source_initial(row,t)
  g=e.direct_guard(e.m.I(a.lo),state,t);self.assertGreater(g['margin'].lo,0);self.assertGreater(g['ratio'].lo,0)
 def test_v6_positive_endpoints_and_hillipop_guard(self):
  for case in e.settings()['thermal']['cases']:
   x=e.v6.derive(case,e.v6.parent_checkpoint(case));self.assertGreater(F(x['phase']['endpoint'][0]),0)
  h=e.v6.derive('hillipop-ede_n3',e.v6.parent_checkpoint('hillipop-ede_n3'));self.assertEqual(h['energy']['full_transfer_source_guard'],'PASS')
 def test_comparison_growth_cap_requests_local_refinement(self):
  fake_cell={'t0':'0','t1':'1','predictor':[],'box':[]}
  with patch.object(e,'_predictor_and_box',return_value=(object(),fake_cell)):
   with patch.object(e.pre,'certify_cell',side_effect=ValueError('COMPARISON_GROWTH_CAP')):
    accepted,reason,cell,report,guard=e._guard_cell(F(1,2),F(2,3),[],None)
  self.assertIsNone(accepted);self.assertEqual(reason,'CERTIFICATE_COMPARISON_GROWTH_CAP')
  self.assertIs(cell,fake_cell);self.assertIsNone(report);self.assertIsNone(guard)
 def test_unexpected_certificate_error_remains_fail_closed(self):
  fake_cell={'t0':'0','t1':'1','predictor':[],'box':[]}
  with patch.object(e,'_predictor_and_box',return_value=(object(),fake_cell)):
   with patch.object(e.pre,'certify_cell',side_effect=ValueError('UNEXPECTED_CERTIFICATE_FAILURE')):
    with self.assertRaisesRegex(ValueError,'UNEXPECTED_CERTIFICATE_FAILURE'):
     e._guard_cell(F(1,2),F(2,3),[],None)

class ScopeControls(unittest.TestCase):
 def test_derive_never_upgrades_full_products_hillipop(self):
  x=e.derive('hillipop-ede_n3');self.assertEqual(x['actual_source_admission'],'UNRESOLVED');self.assertEqual(x['actual_event_redshift'],'NOT_COMPUTED')
  self.assertEqual(x['actual_xe_history_bounds'],'NOT_COMPUTED');self.assertEqual(x['actual_tau_T_bounds'],'NOT_COMPUTED');self.assertEqual(x['final_result_gate'],'UNRESOLVED')
 def test_wrong_case_rejected(self):
  with self.assertRaises(ValueError):e.derive('camspec-lcdm')
 def test_collection_missing_is_partial(self):
  with tempfile.TemporaryDirectory() as d:
   x=r.collect(d,full=False);self.assertEqual(x['job_completeness_gate'],'FAIL');self.assertEqual(x['execution_status'],'PARTIAL')

 def test_v7_worker_report_loader_is_separate_from_legacy_checkpoint_cap(self):
  payload={'schema':'Q048_GUARD_CASE_V7','configuration':'camspec-ede_n3'}
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'camspec-ede_n3_guard_v7.json';path.write_text(json.dumps(payload))
   with patch.object(r.old,'load',side_effect=ValueError('CHECKPOINT_SIZE_CAP')):
    self.assertEqual(r.load_worker_report(path),payload)
  self.assertGreater(r.V7_WORKER_REPORT_SIZE_CAP,32_000_000)
 def test_v7_worker_report_loader_remains_bounded(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'oversize_guard_v7.json';path.write_text('{\"x\":\"1234567890\"}')
   with patch.object(r,'V7_WORKER_REPORT_SIZE_CAP',10):
    with self.assertRaisesRegex(ValueError,'V7_WORKER_REPORT_SIZE_CAP'):
     r.load_worker_report(path)
 def test_report_tamper_rejected_without_heavy_recompute(self):
  case='hillipop-ede_n3';x=e.derive(case);rep=r.make_report(case,x);r.verify_report(rep,full=False)
  bad=copy.deepcopy(rep);bad['actual_source_admission']='PASS'
  with self.assertRaises(ValueError):r.verify_report(bad,full=False)

if __name__=='__main__':unittest.main()
