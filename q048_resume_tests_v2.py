import copy,json,unittest
from pathlib import Path
from fractions import Fraction as F
import q048_prefix_v1 as p

class ResumeTests(unittest.TestCase):
    def engine(self):
        import q048_resume_v2 as e
        return e

    def test_resume_component_exists(self):
        self.assertTrue((Path(__file__).parent/'q048_resume_v2.py').is_file(),
                        'Verified continuation component missing')

    def test_legacy_background_domain_is_reconstructed(self):
        e=self.engine();current=[p.m.I(1),p.m.I(0)];pred=[['1','1/10'],['0','1/100']]
        box=e.legacy_box(current,pred)
        self.assertEqual(list(map(F,box[0])),[F(7,10),F(13,10)])

    def test_forged_stored_certificate_is_rejected(self):
        e=self.engine();config=p.old.load(Path(__file__).parent/'q048_prefix_config_v1.json')
        seed=p.old.load(Path(__file__).parent/'q048_prefix_final_v1.json')['raw_results']['camspec-ede_n3']
        row=config['cases']['camspec-ede_n3'];t=p.parameters(row);_,a,state=p.source_initial(row,t)
        cell=copy.deepcopy(seed['background']['cells'][0]);cell['certificate']['endpoint'][0]=['0','0']
        with self.assertRaisesRegex(ValueError,'CERTIFICATE_MISMATCH'):
            e.verify_background_cell(cell,a.lo,state,t)

    def test_noncontiguous_checkpoint_is_rejected(self):
        e=self.engine();config=p.old.load(Path(__file__).parent/'q048_prefix_config_v1.json')
        seed=p.old.load(Path(__file__).parent/'q048_prefix_final_v1.json')['raw_results']['camspec-ede_n3']
        row=config['cases']['camspec-ede_n3'];t=p.parameters(row);_,a,state=p.source_initial(row,t)
        cell=copy.deepcopy(seed['background']['cells'][0]);cell['a0']='1/10'
        with self.assertRaisesRegex(ValueError,'PARTITION'):
            e.verify_background_cell(cell,a.lo,state,t)

    def test_resume_starts_at_last_certified_endpoint(self):
        e=self.engine()
        bg={'certified_end_a':'1/100','endpoint':[['1','2'],['3','4']]}
        a,y=e.cursor(bg)
        self.assertEqual(a,F(1,100));self.assertEqual(y[0].lo,1);self.assertEqual(y[1].hi,4)

    def test_long_exact_coordinates_roundtrip_and_are_bounded(self):
        e=self.engine();value='1/'+str(10**1100+1)
        self.assertEqual(e.coordinate(value),F(value))
        with self.assertRaisesRegex(ValueError,'COORDINATE_SIZE_CAP'):
            e.coordinate('1/'+('9'*4096))
        with self.assertRaisesRegex(ValueError,'EXACT_INPUT_REQUIRED'):e.coordinate(0.01)

    def test_corrupted_question_or_scope_cannot_be_resumed(self):
        e=self.engine();cfg=p.old.load(Path(__file__).parent/'q048_prefix_config_v1.json')
        r=copy.deepcopy(p.old.load(Path(__file__).parent/'q048_prefix_final_v1.json')['raw_results']['camspec-lcdm'])
        r['scientific_question']='different scientific question'
        row=cfg['cases']['camspec-lcdm'];t=p.parameters(row)
        with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(r,row,t,5)

    def test_verification_does_not_accept_a_forged_actual_gate(self):
        e=self.engine();cfg=p.old.load(Path(__file__).parent/'q048_prefix_config_v1.json')
        r=copy.deepcopy(p.old.load(Path(__file__).parent/'q048_prefix_final_v1.json')['raw_results']['camspec-lcdm'])
        r['actual_source_admission']='PASS'
        row=cfg['cases']['camspec-lcdm'];t=p.parameters(row)
        with self.assertRaisesRegex(ValueError,'SCIENTIFIC_IDENTITY'):e.verify_record(r,row,t,5)

    def test_thermal_endpoint_cannot_disagree_with_its_certificate(self):
        e=self.engine();cfg=e.load(e.ROOT/'q048_prefix_config_v1.json')
        r=copy.deepcopy(e.load(e.ROOT/'q048_prefix_final_v1.json')['raw_results']['camspec-lcdm'])
        r['thermal']['endpoint']=[['0','0']]
        row=cfg['cases']['camspec-lcdm']
        with self.assertRaisesRegex(ValueError,'THERMAL_ENDPOINT'):
            e.verify_record(r,row,p.parameters(row),10)

    def test_collection_rejects_missing_cases_and_false_physical_admission(self):
        import tempfile
        import q048_resume_merge_v2 as merge
        e=self.engine();cfg=e.load(e.ROOT/'q048_resume_config_v2.json')
        r=copy.deepcopy(e.load(e.ROOT/'q048_prefix_final_v1.json')['raw_results']['camspec-lcdm'])
        r['program_id']=e.ID
        m={'case':'camspec-lcdm','q':e.Q,'program_id':e.ID,'source_commit':e.SOURCE,
           'stage':'FINAL_CONDITIONAL_COMPONENT','run_id':'TEST','config_hash':e.objhash(cfg),
           'source_config_hash':cfg['source_config_sha256'],'background_end_a':r['background']['certified_end_a'],
           'thermal_end_a':r['thermal'].get('certified_end_a')}
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'camspec-lcdm_checkpoint_v2.json'
            path.write_text(json.dumps({'schema':'Q048_CHECKPOINT_V2','metadata':m,'record':r}))
            result=merge.collect(d)
            self.assertEqual(result['job_completeness_gate'],'FAIL')
            self.assertEqual(len(result['missing_jobs']),3)
            r['actual_source_admission']='PASS'
            path.write_text(json.dumps({'schema':'Q048_CHECKPOINT_V2','metadata':m,'record':r}))
            with self.assertRaisesRegex(ValueError,'SCOPE'):merge.collect(d)

if __name__=='__main__':unittest.main(verbosity=2)
