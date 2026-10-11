"""Finite adversarial controls of orchestration; synthetic, never cosmological evidence."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import q047_execution_v1 as m

class Controls(unittest.TestCase):
    def test_real_prepared_package_and_launcher(self):
        m.package()
        launcher = (m.HERE / '.github/workflows/00-bubbleverse-start.yml').read_text()
        self.assertIn('program_id not in programs', launcher)
        self.assertIn('status != \'ACTIVE\'', launcher)
        self.assertNotIn('eval ', launcher)

    def test_original_archive_selection_and_rejections(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            archive = root / 'a.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('../../never-extracted', 'other')
                z.writestr('renamed/bg', 'original-bg')
                z.writestr('renamed/th', 'original-th')
            expected = {'background_sha256': hashlib.sha256(b'original-bg').hexdigest(),
                        'thermodynamics_sha256': hashlib.sha256(b'original-th').hexdigest()}
            bg, th = m.original_tables(archive, m.sha(archive), expected, root / 'good')
            self.assertEqual(bg.read_text(), 'original-bg')
            self.assertEqual(th.read_text(), 'original-th')
            self.assertFalse((root / 'never-extracted').exists())
            with self.assertRaisesRegex(ValueError, 'ORIGINAL_ARCHIVE_HASH'):
                m.original_tables(archive, 'bad', expected, root / 'wrong-hash')
            bad = dict(expected, background_sha256='0'*64)
            with self.assertRaisesRegex(ValueError, 'GOLDEN_MEMBERS_MISSING'):
                m.original_tables(archive, m.sha(archive), bad, root / 'missing')
            duplicate = root / 'duplicate.zip'
            with zipfile.ZipFile(duplicate, 'w') as z:
                z.writestr('a', 'original-bg'); z.writestr('b', 'original-bg')
            with self.assertRaisesRegex(ValueError, 'DUPLICATE_GOLDEN_MEMBER'):
                m.original_tables(duplicate, m.sha(duplicate), expected, root / 'duplicate')

    def test_worker_cache_miss_and_rerun_never_call_native(self):
        for change, error in [({'Q047_CACHE_HIT': 'false'}, 'EXACT_CACHE'),
                              ({'GITHUB_RUN_ATTEMPT': '2'}, 'NO_AUTOMATIC_RUN_REPLAY')]:
            env = {'GITHUB_REPOSITORY': m.REPO, 'GITHUB_RUN_ATTEMPT': '1', 'Q047_CACHE_HIT': 'true', **change}
            with tempfile.TemporaryDirectory() as t, patch.dict(os.environ, env), patch.object(m, 'command') as cmd:
                with self.assertRaisesRegex(ValueError, error):
                    m.worker(Path(t) / 'output')
                cmd.assert_not_called()

    def test_preflight_integrity_and_negative_gates(self):
        # Fully synthetic byte objects, explicitly independent of original CLASS.
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            contents = {'original_objects/classy.so': b'FAKE CORE',
                'observer_build/q047_observer': b'FAKE OBSERVER',
                'observer_build/observer_build.log': b'FAKE BUILD LOG',
                'original_sources/include/a.h': b'FAKE HEADER'}
            digest = lambda b: hashlib.sha256(b).hexdigest()
            c = dict(source_commit='synthetic-source', binary_sha256=digest(b'FAKE CORE'),
                observer_source_sha256='synthetic-observer-source',
                source_files_sha256={'include/a.h': digest(b'FAKE HEADER')}, cases={})
            pf = dict(source_commit=c['source_commit'], binary_sha256=c['binary_sha256'],
                binary_path='/synthetic/classy.so', python='3.11.16', platform='synthetic Linux',
                native_library_loaded=False, initialization_executed=False)
            contents['runtime_preflight.json'] = json.dumps(pf).encode()
            contents['build.json'] = b'{}'
            br = dict(binary_sha256=c['binary_sha256'], source_commit=c['source_commit'],
                observer_source_sha256=c['observer_source_sha256'], core_rebuilt=False,
                native_initialization_executed=False, observer_sha256=digest(b'FAKE OBSERVER'))
            contents['observer_build/observer_build_receipt.json'] = json.dumps(br).encode()
            for case in m.CASES:
                contents[case+'_download.log'] = b'FAKE DOWNLOAD'
                contents[case+'_preflight.json'] = json.dumps(pf).encode()
                contents['golden/'+case+'/background.tsv'] = case.encode()+b'BG'
                contents['golden/'+case+'/thermodynamics.tsv'] = case.encode()+b'TH'
                contents['golden/'+case+'/original_member_index.json'] = b'{}'
                c['cases'][case] = dict(background_sha256=digest(case.encode()+b'BG'),
                    thermodynamics_sha256=digest(case.encode()+b'TH'))
            for name, bts in contents.items():
                p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(bts)
            manifest = dict(**m.base(), source_commit=c['source_commit'], binary_sha256=c['binary_sha256'],
                execution_package_sha256=m.sha(m.HERE/'Q047_EXECUTION_PACKAGE_V1.json'),
                collection_lock_sha256=m.sha(m.HERE/'Q047_COLLECTION_LOCK_V1.json'),
                journal_sha256=m.sha(m.HERE/'Q047_SAMLET_JOURNAL.md'), expected_cases=list(m.CASES),
                execution_status='PREFLIGHT_COMPLETE_NO_NATIVE_WORK', new_native_or_theory_evaluations=0,
                initialized_cases=[], core_rebuilt=False, budget_before={'used':16,'remaining':36},
                files={name:m.sha(root/name) for name in contents})
            with patch.object(m,'package',return_value=({},c)):
                result=m.aggregate(root,manifest)
                self.assertEqual(result['final_result_gate'],'UNRESOLVED')
                self.assertEqual(result['native_capture'],'NOT_EXECUTED')
                self.assertEqual(result['budget_before'],result['budget_after'])
                for name, value in [('q','Q-046'),('run_id','OTHER'),('execution_commit','OTHER'),
                    ('source_commit','OTHER'),('journal_sha256','OTHER'),('new_native_or_theory_evaluations',1),
                    ('initialized_cases',['camspec-lcdm']),('expected_cases',list(m.CASES)[:-1]),('core_rebuilt',True)]:
                    bad=copy.deepcopy(manifest); bad[name]=value
                    with self.assertRaises(ValueError): m.aggregate(root,bad)
                bad=copy.deepcopy(manifest);bad['files'].pop('original_objects/classy.so')
                with self.assertRaisesRegex(ValueError,'OUTPUT_COMPLETENESS'):m.aggregate(root,bad)
                (root/'original_objects/classy.so').write_bytes(b'CHANGED CORE')
                with self.assertRaisesRegex(ValueError,'OUTPUT_HASH'):m.aggregate(root,manifest)

    def test_missing_worker_is_failure_receipt(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); out=root/'final.json'
            self.assertEqual(m.finalize(root,out),2)
            result=m.read(out)
            self.assertEqual(result['execution_status'],'INCOMPLETE_OR_REJECTED')
            self.assertEqual(result['final_result_gate'],'UNRESOLVED')

    def test_no_shell_or_scientific_pass_or_install_path(self):
        code=(m.HERE/'q047_execution_v1.py').read_text()
        self.assertNotIn('shell=True',code)
        self.assertNotIn("command(common + ['collect']",code)
        self.assertNotIn("final_result_gate='PASS'",code)
        wf=(m.HERE/'.github/workflows'/m.WORKFLOW).read_text()
        self.assertIn('actions/cache/restore@v4',wf)
        self.assertNotIn('restore-keys:',wf)
        self.assertNotIn('pip install',wf)
        self.assertNotIn('actions/cache/save',wf)

if __name__ == '__main__': unittest.main()
