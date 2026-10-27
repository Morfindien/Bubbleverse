from pathlib import Path
import importlib.util,json,unittest
HERE=Path(__file__).resolve().parent

def mod(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
b=mod('builder',HERE/'q052_build_validated_diag_v3.py')

class TestQ052ValidatedDiag(unittest.TestCase):
    def test_contract_is_one_pair_and_forced_partial(self):
        c=json.loads((HERE/'Q052_VALIDATED_DIAGNOSTICS_CONTRACT_V10.json').read_text())
        self.assertEqual(c['execution']['arms'],['L','R'])
        self.assertEqual(c['execution']['modes'],['nominal'])
        self.assertEqual(c['execution']['new_native_branch_cap'],2)
        self.assertEqual(c['scientific_result_gate'],'FORCED_PARTIAL_UNTIL_VALIDATED_RESIDUAL_CERTIFICATE')
        self.assertFalse(c['frozen_science']['tau_shooting'])
        self.assertFalse(c['frozen_science']['physics_core_rebuild'])
    def test_patch_helper_fails_closed(self):
        with self.assertRaises(RuntimeError): b.one('x','missing','y','T')
        self.assertEqual(b.one('abc','b','B','T'),'aBc')
    def test_patch_source_all_anchors(self):
        src='''#define Q052_ID "Q052-NATIVEPAIR-V2"
static void jhex(FILE *f,double x){if(!isfinite(x))die("NONFINITE");fprintf(f,"\\\"%a\\\"",x);}
static double tol_scale(void)
  if(rc==_SUCCESS_ && intervention_active){
    struct thermo_vector *v=a->ptw->ptdw->ptv;
    dy[v->index_ti_x_He]=0.;
    y[v->index_ti_x_He]=q_xHeII/a->ptw->fHe;
    for(int i=0;i<v->ti_size;i++) if(!isfinite(dy[i])){snprintf(err,_ERRORMSGSIZE_,"Q052_NONFINITE_DERIV");return _FAILURE_;}
  }
  return rc;
}
  int rc=original_sources(x,y,dy,index_z,workspace,err);
  if(rc==_SUCCESS_ && intervention_active) enforce_q(a,y);
  return rc;
}
    class_call(background_at_z(pba,-limits[interval],normal_info,inter_normal,
                               &(ptw->last_index_back),pvecback),
               pba->error_message,pth->error_message);
      write_start(&tpaw,Q052_MZ_EVENT);
      intervention_active=1;
      enforce_q(&tpaw,ptw->ptdw->ptv->y);
  effective(&ba,&th);
  history(&th);
  FILE *f=open_out("runtime_result.json","wx");'''
        out=b.patch_source(src)
        self.assertIn('Q052-VALIDATEDDIAG-V3',out)
        self.assertIn('fullstate_trace.jsonl',out)
        self.assertIn('Z810_PRE_INTERVENTION',out)
        self.assertIn('q052_diag_finalize(&ba)',out)
    def test_builder_pins_historical_parent(self):
        self.assertEqual(b.EXPECTED_BASE_GIT_BLOB,'0539a22cb503af2030c4ca6cdbc7f0c41ba6e1f7')
        self.assertEqual(b.EXPECTED_BASE_SHA256,'d67bf8f8116c835864150d50fda258a0ec33258bfef258accd374dd395acbb4a')
    def test_workflow_has_only_two_nominal_workers(self):
        w=(HERE/'.github/workflows/q052-validated-diagnostics-v3.yml').read_text()
        self.assertIn('arm: [L, R]',w)
        self.assertNotIn('mode: [nominal, refined]',w)
        self.assertIn('Q052-VALIDATEDDIAG-V3',w)
        self.assertIn('LOCAL_Q052_SOURCE_REAL_ERROR_CERTIFICATE.json',w)
    def test_no_final_pass_language_in_contract(self):
        c=(HERE/'Q052_VALIDATED_DIAGNOSTICS_CONTRACT_V10.json').read_text()
        self.assertIn('cannot emit final Q052 PASS',c)
    def test_no_lowercase_json_literals_in_python(self):
        import ast
        tree=ast.parse((HERE/"q052_validated_diag_v3.py").read_text())
        bad=sorted({n.id for n in ast.walk(tree) if isinstance(n,ast.Name) and n.id in {"true","false","null"}})
        self.assertEqual(bad,[])
if __name__=='__main__':unittest.main()
