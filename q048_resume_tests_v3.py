"""Q048 regression tests: lost uncertainty, false gates and the k11 remedy."""
import copy, importlib, json, os, tempfile, unittest
from pathlib import Path
from fractions import Fraction as F

ROOT=Path(__file__).resolve().parent
e=importlib.import_module(os.environ.get('Q048_TEST_ENGINE','q048_resume_v3'))
p=e.p

def parent(case):
    return e.load(ROOT/'q048_resume_parent_v3.json')['records'][case]

def checkpoint_fixture(case,append_background=False):
    cfg=e.load(ROOT/'q048_resume_config_v3.json');r,oldmeta,sha=e.parent_from_asset(case,cfg)
    r.update(program_id=e.ID,version=e.VERSION,tests_status='PROVISIONAL',
             inherited_counts={s:len(r[s]['cells']) for s in ('background','thermal')},
             inherited_cells_hashes={s:e.objhash(r[s]['cells']) for s in ('background','thermal')})
    if append_background:
        row=e.load(ROOT/'q048_prefix_config_v1.json')['cases'][case]
        e.continue_background(r,p.parameters(row),dict(cfg,max_new_cells_per_stage=1),lambda s:None)
    root={'program_id':'Q048-RESUME-V2','config_hash':oldmeta['config_hash'],
          'run_id':oldmeta['run_id'],'checkpoint_sha256':sha}
    r['migration_root']=root
    m=dict(oldmeta,program_id=e.ID,version=e.VERSION,config_hash=e.objhash(cfg),
           stage='RAW_CONTINUATION_DONE',migration_root=root,
           background_end_a=r['background']['certified_end_a'],thermal_end_a=r['thermal']['certified_end_a'])
    return {'schema':'Q048_CHECKPOINT_V3','metadata':m,'record':r}

class ResumeTests(unittest.TestCase):
    def test_first_background_cell_extends_each_exact_parent(self):
        cfg=e.load(ROOT/'q048_prefix_config_v1.json')
        settings={'max_halvings':11 if e.ID.endswith('V3') else 10,
                  'max_new_cells_per_stage':1,'background_seconds':30,'checkpoint_every_cells':8}
        for case in ('camspec-ede_n3','hillipop-ede_n3'):
            r=copy.deepcopy(parent(case));oldcells=copy.deepcopy(r['background']['cells'])
            now,current=e.cursor(r['background']);t=p.parameters(cfg['cases'][case])
            e.continue_background(r,t,settings,lambda stage:None)
            self.assertEqual(len(r['background']['cells']),len(oldcells)+1,case+' needs k11')
            self.assertEqual(r['background']['cells'][:-1],oldcells)
            cell=r['background']['cells'][-1]
            self.assertEqual(F(cell['a0']),now)
            self.assertEqual(F(cell['a1'])-now,now/F(8192))
            self.assertEqual(cell['certificate']['initial_error'],
                             [str((v.hi-v.lo)/2) for v in current])
            e.verify_background_cell(cell,now,current,t)

    def test_first_hillipop_thermal_cell_needs_k11(self):
        cfg=e.load(ROOT/'q048_prefix_config_v1.json');case='hillipop-ede_n3'
        r=copy.deepcopy(parent(case));n=len(r['thermal']['cells'])
        now=F(r['thermal']['certified_end_a']);y=[p.old.interval(v) for v in r['thermal']['endpoint']]
        settings={'max_halvings':11 if e.ID.endswith('V3') else 10,
                  'max_new_cells_per_stage':1,'thermal_seconds':30,'checkpoint_every_cells':8}
        e.continue_thermal(r,cfg['cases'][case],p.parameters(cfg['cases'][case]),settings,(now,y),lambda s:None)
        self.assertEqual(len(r['thermal']['cells']),n+1,'same thermal tube requires k11')
        self.assertEqual(r['thermal']['cells'][-1]['box'],[['-1/1000000','1/50']])
        self.assertTrue(all(F(v)>0 for v in r['thermal']['cells'][-1]['certificate']['closure_slack']))

    def test_forged_certificate_and_broken_partition_are_rejected(self):
        cfg=e.load(ROOT/'q048_prefix_config_v1.json');case='camspec-ede_n3'
        row=cfg['cases'][case];t=p.parameters(row);_,a,y=p.source_initial(row,t)
        c=copy.deepcopy(parent(case)['background']['cells'][0]);c['certificate']['endpoint'][0]=['0','0']
        with self.assertRaisesRegex(ValueError,'CERTIFICATE_MISMATCH'):e.verify_background_cell(c,a.lo,y,t)
        c=copy.deepcopy(parent(case)['background']['cells'][0]);c['a0']='1/10'
        with self.assertRaisesRegex(ValueError,'PARTITION'):e.verify_background_cell(c,a.lo,y,t)

    def test_question_and_actual_scope_cannot_be_forged(self):
        cfg=e.load(ROOT/'q048_prefix_config_v1.json');case='camspec-lcdm';row=cfg['cases'][case]
        for field,value in [('scientific_question','different question'),('actual_source_admission','PASS')]:
            r=copy.deepcopy(parent(case));r[field]=value
            with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(r,row,p.parameters(row),5)

    def test_thermal_endpoint_cannot_be_forged(self):
        cfg=e.load(ROOT/'q048_prefix_config_v1.json');case='camspec-lcdm';row=cfg['cases'][case]
        r=copy.deepcopy(parent(case));r['thermal']['endpoint']=[['0','0']]
        with self.assertRaisesRegex(ValueError,'THERMAL_ENDPOINT'):e.verify_record(r,row,p.parameters(row),20)

    def test_exact_coordinates_are_not_rounded(self):
        x='1/'+str(10**1100+1)
        self.assertEqual(e.coordinate(x),F(x))
        with self.assertRaisesRegex(ValueError,'COORDINATE_SIZE_CAP'):e.coordinate('1/'+'9'*4096)
        with self.assertRaisesRegex(ValueError,'EXACT_INPUT_REQUIRED'):e.coordinate(0.01)

    def test_migration_rejects_modified_parent_and_config(self):
        settings=e.load(ROOT/'q048_resume_config_v3.json')
        record,meta,parenthash=e.parent_from_asset('camspec-ede_n3',settings)
        self.assertEqual(parenthash,settings['parent_checkpoints']['camspec-ede_n3'])
        self.assertEqual(meta['run_id'],'38205625445')
        bad=copy.deepcopy(settings);bad['parent_checkpoints']['camspec-ede_n3']='0'*64
        with self.assertRaisesRegex(ValueError,'PARENT_CHECKPOINT_HASH'):e.parent_from_asset('camspec-ede_n3',bad)

    def test_missing_merge_never_passes(self):
        import q048_resume_merge_v3 as merge
        with tempfile.TemporaryDirectory() as d:
            r=merge.collect(d)
            self.assertEqual(r['job_completeness_gate'],'FAIL')
            self.assertEqual(r['final_result_gate'],'UNRESOLVED')
            self.assertEqual(len(r['missing_jobs']),4)

    def test_resume_cannot_discard_the_pinned_parent_prefix(self):
        settings=e.load(ROOT/'q048_resume_config_v3.json');case='camspec-ede_n3'
        x=checkpoint_fixture(case)
        r=x['record'];bg=r['background'];bg['cells']=bg['cells'][:1]
        bg['certified_end_a']=bg['cells'][-1]['a1'];bg['endpoint']=bg['cells'][-1]['certificate']['endpoint']
        r['thermal']['cells']=[];r['thermal']['certified_end_a']=str(1/(1-p.point(e.load(ROOT/'q048_prefix_config_v1.json')['cases'][case]['thermal_starts'][0]['mz']).lo))
        r['thermal']['endpoint']=[['0','0']]
        x['metadata']['background_end_a']=bg['certified_end_a'];x['metadata']['thermal_end_a']=r['thermal']['certified_end_a']
        r['verified_scientific_payload_sha256']=e.proof_binding(r);x['metadata']['verified_scientific_payload_sha256']=e.proof_binding(r)
        with self.assertRaisesRegex(ValueError,'PINNED_PARENT_PREFIX'):e.validate_checkpoint(x,case,settings)

    def test_merge_recomputes_even_a_rebound_forged_certificate(self):
        import q048_resume_merge_v3 as merge
        case='camspec-ede_n3';x=checkpoint_fixture(case,append_background=True)
        r=x['record'];r['background']['cells'][415]['certificate']['closed']=False
        r['tests_status']='COMPLETE_CONDITIONAL';r['post_verification']={'gate':'PASS_CONDITIONAL_RECOMPUTED'}
        x['metadata']['stage']='FINAL_CONDITIONAL_COMPONENT'
        r['verified_scientific_payload_sha256']=e.proof_binding(r);x['metadata']['verified_scientific_payload_sha256']=e.proof_binding(r)
        with tempfile.TemporaryDirectory() as d:
            p.old.write(Path(d)/(case+'_checkpoint_v3.json'),x)
            with self.assertRaisesRegex(ValueError,'CERTIFICATE_MISMATCH'):merge.collect(d)

    def test_incomplete_checkpoint_yields_a_partial_collection(self):
        import q048_resume_merge_v3 as merge
        case='camspec-lcdm';x=checkpoint_fixture(case)
        x['metadata']['stage']='RAW_CONTINUATION_DONE';x['record']['tests_status']='PROVISIONAL'
        with tempfile.TemporaryDirectory() as d:
            p.old.write(Path(d)/(case+'_checkpoint_v3.json'),x)
            r=merge.collect(d)
            self.assertEqual(r['job_completeness_gate'],'FAIL')
            self.assertIn(case,r['partial_records'])

if __name__=='__main__':unittest.main(verbosity=2)
