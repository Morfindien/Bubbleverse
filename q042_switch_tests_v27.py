"""Finite V27 behavior gates: missing/wrong identity, nonfinite samples and unsafe launch."""
import copy, importlib.util, pathlib, unittest
P=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('controller',P/'q042_switch_probe_v27.py')
m=None
if (P/'q042_switch_probe_v27.py').exists():
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Gates(unittest.TestCase):
 def test_missing_native_samples_cannot_complete(self):
  self.assertIsNotNone(m,'V27 sample gate not implemented')
  with self.assertRaises(ValueError):m.validate_samples([], 'RUN', 'CFG', ['UPPER','LOWER'])
 def test_complete_forward_reverse_samples_and_detect_corruption(self):
  self.assertIsNotNone(m,'V27 sample gate not implemented')
  rows=[]
  for t in ['UPPER','LOWER']:
   for order in [0,1]:
    for i,e in enumerate([1e-6,1e-8,1e-10]):
     for side in [-1,1]:
      rows.append(dict(q='Q-042',program_id='Q042-SWITCHPROBE-V27',run_id='RUN',config_sha256='CFG',trial=t,branch_id=t,order=order,epsilon_index=i,epsilon=e,side=side,z=16.031010835587164+side*e,model=0 if side==-1 else 4,hmla_calls=0 if side==-1 else 1,tla_calls=1 if side==-1 else 0,kernel_calls=1,kernel_error=0,status=0,dy=[1.,0.,2.],y=[-2.,1.2261504557092879e-5,.0002],TR_eV=.003999999 if side==-1 else .004000001,T_ratio=.9))
  m.validate_samples(rows,'RUN','CFG',['UPPER','LOWER'])
  for change in ['nonfinite','duplicate','wrongmodel','wrongrun','missing']:
   bad=copy.deepcopy(rows)
   if change=='nonfinite':bad[0]['dy'][2]=float('nan')
   if change=='duplicate':bad.append(copy.deepcopy(bad[0]))
   if change=='wrongmodel':bad[0]['model']=4
   if change=='wrongrun':bad[0]['run_id']='OTHER'
   if change=='missing':bad.pop()
   with self.assertRaises(ValueError,msg=change):m.validate_samples(bad,'RUN','CFG',['UPPER','LOWER'])
 def test_unit_jump_fingerprint_independently_derived(self):
  self.assertIsNotNone(m,'V27 analysis not implemented')
  # one interval H=1, transition theta=.375; RK4 weights at 0,.5,1.
  self.assertAlmostEqual(m.jump_weight_error('RK4',1,.375,1),5/6-5/8)
  self.assertAlmostEqual(m.jump_weight_error('MIDPOINT',1,.375,1),1-5/8)
  with self.assertRaises(ValueError):m.jump_weight_error('OTHER',1,.375,1)
if __name__=='__main__':unittest.main()
