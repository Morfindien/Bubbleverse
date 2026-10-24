import importlib.util
import pathlib
import tempfile
import unittest
import subprocess
import sys
import os

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('cleanup_integrity', ROOT/'tools/maintenance/check_cleanup_integrity.py')

class IntegrityControls(unittest.TestCase):
    def checker(self):
        self.assertTrue(SPEC.origin and pathlib.Path(SPEC.origin).is_file(), 'integrity checker is not implemented')
        module=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(module)
        return module

    def test_traversal_and_symlink_escape(self):
        m=self.checker()
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            root=pathlib.Path(d)
            (root/'link').symlink_to(outside, target_is_directory=True)
            for path in ['../file','/tmp/file','link/file']:
                with self.subTest(path=path), self.assertRaises(ValueError):m.safe_path(root,path)

    def test_schema_rejects_missing_and_wrong_status(self):
        m=self.checker()
        schema={'type':'object','required':['status'],'properties':{'status':{'type':'string','enum':['PASS','FAIL']}}}
        for obj in [{},{'status':'MAGIC'},{'status':True}]:
            with self.subTest(obj=obj), self.assertRaises(ValueError):m.schema_check(obj,schema)
        m.schema_check({'status':'PASS'},schema)
        for obj,schema in [({}, {'type':'object','properties':{'optional':{'unsupported':True}}}),([],{'type':'array','items':{'unsupported':True}})]:
            with self.subTest(schema=schema),self.assertRaises(ValueError):m.schema_check(obj,schema)

    def test_changed_missing_and_permission_changed_protected_file(self):
        m=self.checker()
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); f=root/'journal.md';f.write_bytes(b'original');f.chmod(0o644)
            record=m.metadata(f);record['path']='journal.md'
            m.verify_record(root,record)
            f.write_bytes(b'changed')
            with self.assertRaises(ValueError):m.verify_record(root,record)
            f.write_bytes(b'original');f.chmod(0o755)
            with self.assertRaises(ValueError):m.verify_record(root,record)
            f.unlink()
            with self.assertRaises(ValueError):m.verify_record(root,record)

    def test_duplicate_and_incomplete_coverage(self):
        m=self.checker()
        for rows in [[{'path':'a'},{'path':'a'}],[{'path':'b'}]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):m.coverage(['a'],rows)
        m.coverage(['a'],[{'path':'a'}])

    def test_protected_and_launch_coverage_cannot_be_omitted(self):
        m=self.checker()
        rows=[{'path':'a.py','protection_classification':'PROTECTED'}]
        entries=[{'source':'a.py','kind':'python','program_id':'P','registry_source':'registry.json'}]
        args=(['a.py'],rows,[{'path':'a.py'}],entries,{('a.py','python')},{('registry.json','P')})
        m.contract_coverage(*args)
        for index in [2,3]:
            broken=list(args);broken[index]=[]
            with self.subTest(index=index),self.assertRaises(ValueError):m.contract_coverage(*broken)
        broken=list(args);broken[5]={('registry.json','OTHER')}
        with self.assertRaises(ValueError):m.contract_coverage(*broken)

    def test_special_files_are_rejected_without_blocking(self):
        m=self.checker()
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):m.metadata(pathlib.Path(d))
            fifo=pathlib.Path(d)/'fifo';os.mkfifo(fifo)
            code=('import importlib.util; s=importlib.util.spec_from_file_location("m",'+repr(SPEC.origin)+'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)\n'
                  'try: m.metadata('+repr(str(fifo))+')\nexcept ValueError: raise SystemExit(0)\nraise SystemExit(1)')
            result=subprocess.run([sys.executable,'-c',code],timeout=2,capture_output=True)
            self.assertEqual(result.returncode,0)

if __name__=='__main__':unittest.main()
