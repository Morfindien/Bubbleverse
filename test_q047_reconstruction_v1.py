"""Finite failure-mode tests: runtime, identity, completeness and false promotion."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import os

HERE = Path(__file__).resolve().parent


class ReconstructionGates(unittest.TestCase):
    def module(self):
        path = HERE / 'q047_reconstruction_v1.py'
        self.assertTrue(path.is_file(), 'Approved reconstruction gate implementation is missing')
        spec = importlib.util.spec_from_file_location('reconstruction', path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def runtime(self):
        return {'schema': 'Q047_RUNTIME_CONTROL_V2', 'q': 'Q-047',
                'case': 'camspec-lcdm', 'origin': 'NEW_RECONSTRUCTION',
                'events': [{'checkpoint': k, 'rounding_mode': 0, 'FE_TONEAREST': 0,
                            'mxcsr': 0x1f80, 'x87_control': 0x37f}
                           for k in ['before_input', 'after_input', 'before_background',
                                     'after_background', 'before_thermal', 'after_thermal']],
                'symbol_resolution_kind': 'DLSYM_REFERENCE_NOT_CORE_GOT_PROOF',
                'symbols': [{'name': k, 'object': '/lib/libm.so.6', 'offset': '0x100'}
                            for k in ['cos', 'sincos', 'pow']],
                'cpuid_leaf1': [0, 0, 0, 0], 'cpuid_leaf7': [0, 0, 0, 0],
                'xcr0': '0x0'}

    def test_runtime_rejects_flush_to_zero_and_wrong_rounding(self):
        m = self.module()
        r = self.runtime()
        self.assertEqual(m.runtime_gate(r, 'camspec-lcdm')['status'], 'PASS')
        for field, value in [('mxcsr', 0x9f80), ('mxcsr', 0x1fc0), ('rounding_mode', 0x400)]:
            v = copy.deepcopy(r)
            v['events'][2][field] = value
            with self.assertRaisesRegex(ValueError, 'FP_ENVIRONMENT'):
                m.runtime_gate(v, 'camspec-lcdm')

    def test_runtime_rejects_a_missing_checkpoint_or_other_case(self):
        m = self.module()
        r = self.runtime()
        r['events'].pop()
        with self.assertRaisesRegex(ValueError, 'FP_CHECKPOINTS'):
            m.runtime_gate(r, 'camspec-lcdm')
        with self.assertRaisesRegex(ValueError, 'RUNTIME_IDENTITY'):
            m.runtime_gate(self.runtime(), 'hillipop-lcdm')

    def test_partial_or_wrong_branch_never_becomes_complete(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for case in m.CASES:
                d = root / case
                d.mkdir()
                raw = d / 'raw.txt'
                raw.write_text('raw fixture; not scientific data')
                obj = dict(**m.base(), case=case, execution_status='CAPTURE_COMPLETE',
                           native_processes_started=1, full_cmb_likelihood_evaluations=0,
                           internal_initializations=7, structural_gate='PASS', runtime_gate='PASS',
                           reproduction_gate='NOT_MATCHING_ARCHIVE',
                           scientific_verdict='INSUFFICIENT_EVIDENCE', final_result_gate='UNRESOLVED',
                           files={'raw.txt': hashlib.sha256(raw.read_bytes()).hexdigest()})
                for name in m.CAPTURE_OUTPUTS:
                    p = d / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text('synthetic archive-completeness fixture; not scientific evidence')
                obj['files'] = m.file_index(d)
                (d / 'worker_result.json').write_text(json.dumps(obj))
            result = m.aggregate(root)
            self.assertEqual(result['execution_status'], 'COMPLETE')
            self.assertEqual(result['final_result_gate'], 'UNRESOLVED')
            self.assertEqual(result['capture_ledger']['native_processes_started'], 4)
            d = root / m.CASES[0]
            (d / 'raw.txt').write_text('changed')
            result = m.aggregate(root)
            self.assertNotEqual(result['execution_status'], 'COMPLETE')
            self.assertIn(m.CASES[0], result['failed_jobs'])
            (d / 'worker_result.json').unlink()
            result = m.aggregate(root)
            self.assertIn(m.CASES[0], result['missing_jobs'])

    def test_unsafe_member_path_and_forged_scientific_pass_are_rejected(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            o = dict(**m.base(), case=m.CASES[0], execution_status='CAPTURE_COMPLETE',
                     native_processes_started=1, full_cmb_likelihood_evaluations=0,
                     internal_initializations=1, scientific_verdict='CONFIRMED',
                     final_result_gate='PASS', files={})
            with self.assertRaisesRegex(ValueError, 'SCIENTIFIC_PROMOTION'):
                m.branch_gate(d, o, m.CASES[0])
            o.update(scientific_verdict='INSUFFICIENT_EVIDENCE', final_result_gate='UNRESOLVED',
                     files={'../outside': '0' * 64})
            with self.assertRaisesRegex(ValueError, 'MEMBER_PATH'):
                m.branch_gate(d, o, m.CASES[0])

    def test_actual_c_runtime_capture_and_observation_fp_restore(self):
        c = HERE / 'q047_collect_state_v2.c'
        self.assertTrue(c.is_file(), 'Versioned C runtime capture is missing')
        source = Path(os.environ.get('Q047_TEST_HEADERS', str(HERE.parent / 'q047_preflight_ingestion/raw/q047_capture/original_sources')))
        if not source.is_dir():
            self.skipTest('Pinned headers absent in static job; this C test is mandatory after cache restore')
        # This instrument-only C harness never links or loads the CLASS binary.
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            harness = d / 'instrument.c'
            harness.write_text('#define main unused_native_main\n#include "' + str(c) + '"\n'
                '#undef main\nint main(int argc,char **argv){(void)argc;directory=argv[1];case_name="camspec-lcdm";'
                'if(fesetround(FE_DOWNWARD))return 3;fenv_t s=observation_begin();'
                'if(fesetround(FE_UPWARD))return 4;observation_end(&s);'
                'if(fegetround()!=FE_DOWNWARD)return 5;if(fesetround(FE_TONEAREST))return 6;'
                'const char *k[]={"before_input","after_input","before_background","after_background","before_thermal","after_thermal"};'
                'for(int i=0;i<6;i++)runtime_checkpoint(k[i]);runtime_finish();return 0;}\n')
            cmd = ['gcc', '-std=c11', '-O0', '-ffunction-sections', '-fdata-sections',
                   '-Wl,--gc-sections', '-Wl,--no-as-needed']
            cmd += ['-I' + str(source / n) for n in ['include', 'external/HyRec2020', 'external/heating', 'external/RecfastCLASS']]
            cmd += [str(harness), '-ldl', '-lm', '-o', str(d / 'instrument')]
            subprocess.run(cmd, check=True, capture_output=True)
            subprocess.run([str(d / 'instrument'), str(d)], check=True, timeout=10)
            obj = json.loads((d / 'runtime_control_v2.json').read_text())
            self.assertEqual(self.module().runtime_gate(obj, 'camspec-lcdm')['status'], 'PASS')

    def test_complete_label_cannot_hide_missing_capture_outputs(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            obj = dict(**m.base(), case=m.CASES[0], execution_status='CAPTURE_COMPLETE',
                       native_processes_started=1, full_cmb_likelihood_evaluations=0,
                       internal_initializations=1, scientific_verdict='INSUFFICIENT_EVIDENCE',
                       final_result_gate='UNRESOLVED', files={})
            with self.assertRaisesRegex(ValueError, 'CAPTURE_OUTPUT_SET'):
                m.branch_gate(d, obj, m.CASES[0])


if __name__ == '__main__':
    unittest.main()
