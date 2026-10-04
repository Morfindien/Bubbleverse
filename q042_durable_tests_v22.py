"""Finite offline tests; compiled trajectory tests run separately before pilot."""
import copy, hashlib, json, tempfile, unittest
from pathlib import Path
import q042_durable_diagnostic_v22 as driver
import q042_install_durable_v22 as installer

HERE=Path(__file__).resolve().parent
class DurableTests(unittest.TestCase):
    def test_contract_keeps_science_and_budget(self):
        c=driver.config(HERE/'q042_durable_contract_v22.json')
        self.assertEqual(c['frozen_files']['q042_production_spec_v1.json'],'41e4d8f026933f64dbe41048f894002f479ba2b504432b33dc155f4dfe71378c')
        self.assertEqual(c['maximum_production_cells'],0)
        self.assertEqual(len(c['rti_schema']),44)
        self.assertFalse(c['statistical_update_cadence_changed'])
        broken=copy.deepcopy(c);broken['probe_seconds']=28800
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'contract.json';path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(ValueError,'DURABLE_CONTRACT'):driver.config(path)

    def test_registry_addition_and_conflict_are_differential(self):
        data={'schema_version':3,'programs':{'Q042-STOCKDIAG-V21':installer.PREVIOUS_ENTRY,'UNRELATED':{'keep':'verbatim'}}}
        updated=installer.registry_update(data)
        self.assertEqual(updated['programs']['UNRELATED'],data['programs']['UNRELATED'])
        self.assertEqual(updated['programs'][installer.PROGRAM_ID],installer.ENTRY)
        self.assertEqual(installer.registry_update(updated),updated)
        conflict=copy.deepcopy(updated);conflict['programs'][installer.PROGRAM_ID]['workflow_id']='other.yml'
        with self.assertRaisesRegex(ValueError,'CONFLICT'):installer.registry_update(conflict)

    def test_readme_only_changes_authoritative_block(self):
        text='before\n'+installer.OLD+'\nafter'
        patched=installer.readme_update(text)
        self.assertEqual(patched,'before\n'+installer.NEW+'\nafter')
        self.assertEqual(installer.readme_update(patched),patched)
        with self.assertRaisesRegex(ValueError,'ANCHOR'):installer.readme_update('missing block')

    def test_completed_class_failure_is_preserved_without_replay(self):
        c=driver.config(HERE/'q042_durable_contract_v22.json')
        r=c['preserved_class_result'];self.assertFalse(r['recomputed'])
        self.assertEqual(r['original_result']['raw_result']['point_result'],'CLASS_EXCEPTION')
        self.assertIn('tau_c=',r['original_result']['raw_result']['exception'])
        self.assertEqual(c['maximum_class_point_count'],0)

    def test_v21_fetch_still_handles_absent_parent(self):
        # Regression for the actual V20 missing diag_inputs parent failure.
        from unittest.mock import patch
        module=driver.reused();c=driver.config(HERE/'q042_durable_contract_v22.json');a=c['artifacts']['ede']
        meta=dict(id=a['id'],expired=False,name=a['name'],digest='sha256:'+a['sha256'],workflow_run=dict(id=a['run_id'],head_sha=c['source_commit']))
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return json.dumps(meta).encode()
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'new_parent'/'ede'
            with patch.object(module.urllib.request,'urlopen',return_value=Response()),patch.object(module.subprocess,'run'),patch.object(module,'extract_verified'),patch.object(module,'write_json'):
                module.fetch_artifact(c,'ede',dest)
            self.assertTrue(Path(str(dest)+'.zip').is_file())

if __name__=='__main__':unittest.main()
