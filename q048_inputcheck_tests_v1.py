"""Q-048 adversarial controls; fixtures are built from pinned captured metadata."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import q048_inputcheck_v1 as m

HERE = Path(__file__).resolve().parent
LOCK = HERE / 'Q048_INPUTCHECK_CONTRACT_V1.json'

class Controls(unittest.TestCase):
    def test_exact_hex(self):
        self.assertEqual(m.native('-0x0p+0').hex(), '-0x0.0p+0')
        for value in [True, 'nan', '1.0', '0x1.00000000000001p+0', '0x1p+9999']:
            with self.subTest(value=value), self.assertRaises(m.GateError):
                m.native(value)

    def test_duplicate_and_nonfinite_json(self):
        for s in ['{"q":1,"q":2}', '{"x":NaN}', '{"x":Infinity}']:
            with self.assertRaises(m.GateError): m.decode(s)

    def test_pin_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'member'; p.write_bytes(b'abc')
            m.verified_member(Path(tmp), 'member', m.sha(p), 3)
            with self.assertRaises(m.GateError): m.verified_member(Path(tmp), 'member', '0'*64, 3)
            (Path(tmp)/'link').symlink_to(p)
            with self.assertRaises(m.GateError): m.verified_member(Path(tmp), 'link', m.sha(p), 3)
            with self.assertRaises(m.GateError): m.verified_member(Path(tmp), '../member', m.sha(p), 3)

    def test_capture_semantics(self):
        c = m.read(LOCK)
        for name, spec in c['cases'].items():
            data = copy.deepcopy(spec['control_objects'])
            out = m.validate_case(name, data, c)
            self.assertEqual(out['metadata_gate'], 'PASS')
            self.assertEqual(out['continuous_no_hit_gate'], 'UNRESOLVED')
            self.assertTrue(out['late_phase_samples']['same_binary64_x_He'])
            q=out['late_phase_samples']['q_at_frec']
            self.assertLess(m.Fraction(int(q['num']),int(q['den'])),m.Fraction(1,10**6))

    def test_wrong_context(self):
        c=m.read(LOCK); name=next(iter(c['cases']))
        for field, bad in [('case','unknown'), ('run_id','other'), ('historical_export',True)]:
            d=copy.deepcopy(c['cases'][name]['control_objects']); d['worker'][field]=bad
            with self.subTest(field=field), self.assertRaises(m.GateError): m.validate_case(name,d,c)

    def test_missing_phase_or_invalid_indices(self):
        c=m.read(LOCK); name=next(iter(c['cases']))
        for change in ['missing','duplicate','boolean']:
            d=copy.deepcopy(c['cases'][name]['control_objects'])
            if change=='missing': d['thermal'].pop()
            elif change=='duplicate': d['thermal'][5]['H_index']=d['thermal'][5]['He_index']
            else: d['thermal'][5]['require_H']=True
            with self.subTest(change=change), self.assertRaises(m.GateError): m.validate_case(name,d,c)

    def test_frozen_z_and_constants(self):
        c=m.read(LOCK); name=next(iter(c['cases']))
        for change in ['z','constant']:
            d=copy.deepcopy(c['cases'][name]['control_objects'])
            if change=='z': d['background']['z_reio']='0x1p+3'
            else: d['thermal'][-1]['constants']['Tcmb']='0x1p+2'
            with self.subTest(change=change), self.assertRaises(m.GateError): m.validate_case(name,d,c)

    def test_missing_cases_never_complete(self):
        c=m.read(LOCK)
        with tempfile.TemporaryDirectory() as tmp:
            out=m.audit(Path(tmp),c)
            self.assertEqual(out['execution_status'],'PARTIAL')
            self.assertEqual(out['job_completeness_gate'],'FAIL')
            self.assertEqual(out['final_result_gate'],'UNRESOLVED')
            self.assertEqual(len(out['failed_cases']),4)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'receipt.json'; m.write(p,{'q':'Q-048'})
            with self.assertRaises(FileExistsError): m.write(p,{'q':'Q-049'})

if __name__=='__main__': unittest.main()
