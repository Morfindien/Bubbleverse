"""Finite source-expression controls, never actual cosmological admission."""
import unittest, math, copy, json
from fractions import Fraction as F
import q047_precursor_check_v1 as p
import q047_math_v1 as m

def theta():
    return {'H0':m.I(1),'gamma':m.I(1),'ur':m.I(0),'matter':m.I(0),
            'lambda':m.I(0),'K':m.I(0),'T0':m.I(3),'nH0':m.I('0.2'),
            'fHe':m.I('0.08'),'neutrinos':[], 'ede':None}

class PrecursorTests(unittest.TestCase):
    def api(self,name):
        f=getattr(p,name,None)
        self.assertTrue(callable(f),'Missing finite/source implementation: '+name)
        return f

    def test_scalar_positive_growth_closes_without_invariant_rectangle(self):
        fn=self.api('scalar_envelope'); end,alltime=fn(F(2),F('0.25'),F('.001'),F('.0001'))
        self.assertGreater(end.lo,F('.001'))
        self.assertLess(alltime.hi,F('.002'))
        self.assertGreater(F(2)*F('.002')+F('.0001'),0)

    def test_scalar_zero_and_damping_limits(self):
        fn=self.api('scalar_envelope')
        e,b=fn(F(0),F(2),F(1),F(3));self.assertEqual(e.lo,7);self.assertEqual(b.hi,7)
        e,b=fn(F(-2),F(1),F(1),F(0));self.assertLess(e.hi,1);self.assertEqual(b.hi,1)
        with self.assertRaises(ValueError):fn(F(1),F(1),F(-1),F(0))

    def test_vector_positive_growth_and_offdiagonal(self):
        fn=self.api('vector_envelope'); e,b=fn([[F(2),F(1)],[F(0),F(1)]],F('.1'),[F('.001')]*2,[F('.0001')]*2)
        self.assertGreater(e[0].lo,F('.001'));self.assertLess(b[0].hi,F('.002'))
        with self.assertRaises(ValueError):fn([[F(1),F(-1)],[F(0),F(1)]],F(1),[F(1)]*2,[F(0)]*2)

    def test_trig_outward_and_range_cap(self):
        fn=self.api('trig')
        for v in ['0','.1','-1','3']:
            for cosine in [False,True]:
                q=fn(m.I(v),cosine);ref=F.from_float((math.cos if cosine else math.sin)(float(v)))
                self.assertLess(abs(float((q.lo+q.hi)/2)-float(ref)),1e-14)
                self.assertGreaterEqual(q.hi-q.lo,0)
        with self.assertRaises(ValueError):fn(m.I(1000),False)

    def test_finite_neutrino_sum_moment_identity(self):
        fn=self.api('neutrino_sum')
        species={'mass':m.I(2),'factor':m.I(3),'nodes':[m.I(1),m.I(2)],'weights':[m.I('0.2'),m.I('0.3')]}
        r,v=fn(m.I(1),species); self.assertGreater(r.lo,0);self.assertGreater(v.lo,0);self.assertLess(v.hi,r.lo/3)
        bad=copy.deepcopy(species);bad['weights'][0]=m.I(-1)
        with self.assertRaises(ValueError):fn(m.I(1),bad)

    def test_fd_tail_and_distinct_reference(self):
        fn=self.api('fd_moments'); r,v,tail=fn(m.I(1),m.I(0),m.I(0),m.I(1),F(8),32)
        self.assertGreater(r.lo,0);self.assertLess(v.lo,r.hi/3);self.assertGreater(tail[0].hi,0)
        with self.assertRaises(ValueError):fn(m.I(1),m.I(0),m.I(0),m.I(1),F(8),0)

    def test_background_radiation_ell_is_minus_two(self):
        fn=self.api('background'); b=fn(m.I('0.01'),theta())
        self.assertLessEqual(b['ell'].lo,-2);self.assertGreaterEqual(b['ell'].hi,-2)
        self.assertLessEqual(b['H'].lo,10000);self.assertGreaterEqual(b['H'].hi,10000)
        bad=theta();bad['gamma']=m.I(-1)
        with self.assertRaises(ValueError):fn(m.I(1),bad)

    def test_ede_zero_potential_energy_damping(self):
        fn=self.api('ede_field'); t=theta();t['ede']={'F':m.I('2.435e27'),'m':m.I(0),'B':m.I(0)}
        rates,b=fn(m.I(1),[m.A(0,[m.I(1),m.I(0)]),m.A('.1',[m.I(0),m.I(1)])],t)
        self.assertLessEqual(rates[1].v.lo,F('-.3'));self.assertGreaterEqual(rates[1].v.hi,F('-.3'))
        self.assertLessEqual(p.value(b['ede_latch']).hi,0)

    def test_thermal_modes_use_different_source_equations(self):
        fn=self.api('thermal');t=theta();a=m.I('0.0001');b=self.api('background')(a,t)
        w=m.A('0.000001',[m.I(1),m.I(0)])
        e=fn('brec',a,w,t,b);late=fn('He1',a,w,t,b)
        self.assertGreater(e['rate'].d[0].lo,0)
        self.assertNotEqual(e['rate'].v.lo,late['rate'].v.lo)
        self.assertGreater(e['x'].v.lo,1+t['fHe'].lo)
        with self.assertRaises(ValueError):fn('H',a,w,t,b)

    def test_saha_onset_normalization(self):
        fn=self.api('onset');t=theta();q=fn(m.I(0),m.I(F(1,2871)),t)
        self.assertGreater(q.lo,0);self.assertLess(q.hi,t['fHe'].hi)

    def test_scalar_source_cell_closure_is_computed(self):
        fn=self.api('certify_cell')
        field=lambda u,y: [y[0]]
        cell={'t0':'0','t1':'1/100','predictor':[['1','1/100']], 'box':[['9/10','11/10']]}
        r=fn(cell,[m.I(1)],field)
        self.assertTrue(r['closed']);self.assertGreater(F(r['closure_slack'][0]),0)
        bad=copy.deepcopy(cell);bad['box']=[['1','101/100']]
        self.assertFalse(fn(bad,[m.I(1)],field)['closed'])

    def test_vector_cell_detects_between_node_excursion(self):
        fn=self.api('certify_cell')
        field=lambda u,y:[y[0]*0,y[1]*0]
        cell={'t0':'0','t1':'1','predictor':[['0','4','-4'],['0']], 'box':[['-1/10','1/10'],['-1/10','1/10']]}
        self.assertFalse(fn(cell,[m.I(0),m.I(0)],field)['closed'])

    def test_packet_refuses_forged_actual_qualification(self):
        fn=self.api('verify_packet')
        with self.assertRaisesRegex(ValueError,'ACTUAL'):
            fn({'actual_reference_qualified':True})

    def test_effective_field_exact_hex_mismatch_refused(self):
        fn=self.api('decode_field');x={'bounds':['1','1'],'native_hex':'0x1.0000000000000p+0','unit':'1','source_field':'Omega0_g'}
        self.assertEqual(fn(x,'1').lo,1)
        x['native_hex']='0x1.0000000000000p+1'
        with self.assertRaisesRegex(ValueError,'HEX'):fn(x,'1')

    def test_threshold_native_and_exact_epsilon_separate(self):
        fn=self.api('threshold_report');r=fn()
        self.assertNotEqual(r['exact_epsilon'],r['native_epsilon'])
        self.assertEqual(r['binary_equivalence_gate'],'UNRESOLVED')

    def test_conditional_lcdm_prefix_has_real_pass_path(self):
        fn=self.api('verify_packet');r=fn(fixture())
        self.assertEqual(r['conditional_prefix_gate'],'PASS',r)
        self.assertEqual(r['actual_applicability'],'INSUFFICIENT_EVIDENCE')
        self.assertEqual(r['predicates']['PT07']['status'],'PASS_FOR_DECLARED_PREFIX_ONLY')

    def test_wrong_mode_boundary_and_discontinuous_state_refused(self):
        fn=self.api('verify_packet');x=fixture();x['thermal_cells'][0]['mode']='He1'
        r=fn(x);self.assertEqual(r['conditional_prefix_gate'],'FAIL')
        x=fixture();x['thermal_cells'].append(copy.deepcopy(x['thermal_cells'][0]));x['thermal_cells'][1]['t0']='1/8000'
        with self.assertRaisesRegex(ValueError,'PARTITION'):fn(x)

    def test_reduced_variant_refuses_unmodelled_components(self):
        fn=self.api('verify_packet');x=fixture();x['flags']['has_fld']=True
        with self.assertRaisesRegex(ValueError,'REDUCED'):fn(x)

    def test_certified_source_background_and_thermal_cells_not_metadata_pass(self):
        fn=self.api('verify_packet');x=fixture();x['thermal_cells'][0]['box']=[['0','0']]
        x['thermal_cells'][0]['closed']=True;x['thermal_cells'][0]['residual_upper']='0'
        r=fn(x);self.assertEqual(r['conditional_prefix_gate'],'FAIL')

    def test_generator_produces_closed_positive_growth_cells(self):
        fn=self.api('generate_cells')
        r=fn([m.I(1)],F(0),F('0.01'),lambda a,y:[y[0]], [['9/10','11/10']],max_cells=8)
        self.assertEqual(r['status'],'COMPLETE',r)
        self.assertTrue(all(c['certificate']['closed'] for c in r['cells']))

    def test_generator_finite_cap_cannot_be_reported_complete(self):
        fn=self.api('generate_cells')
        r=fn([m.I(1)],F(0),F(1),lambda a,y:[y[0]], [['9/10','11/10']],max_cells=1)
        self.assertEqual(r['status'],'UNRESOLVED_WORK_CAP',r)

    def test_neutrino_common_enclosure_keeps_same_mass_factor(self):
        fn=self.api('common_neutrinos')
        s={'mass':m.I(1),'factor':m.I(1),'nodes':[m.I(1)],'weights':[m.I(1)],'xi':m.I(0),'Qmax':F(8),'cells':16}
        r=fn(m.I(1),s)
        self.assertGreaterEqual(r['rho'].hi,r['finite'][0].hi)
        self.assertGreaterEqual(r['rho'].hi,r['fd'][0].hi)
        self.assertGreater(r['quadrature_difference'][0].absmax(),0)

    def test_packet_ede_positive_growth_background_is_not_forcing_boolean(self):
        fn=self.api('verify_packet');x=fixture()
        x['ede']={'n':3,'attractor_ic':False,'F':['2.435e27','2.435e27'],'m':['0','0'],'B':['0','0']}
        x['background_initial_a']=x['thermal_initial_a'];x['background_initial_state']=[['0','0'],['0','0']]
        x['background_cells']=[{'t0':x['thermal_cells'][0]['t0'],'t1':x['thermal_cells'][0]['t1'],
            'predictor':[['0'],['0']],'box':[['-1/1000','1/1000'],['-1/1000','1/1000']]}]
        r=fn(x);self.assertEqual(r['conditional_prefix_gate'],'PASS',r)
        self.assertTrue(r['background_cells'][0]['source_latch_excluded'])

    def test_complete_source_path_report_requires_all_modes_and_onset(self):
        r=self.api('verify_packet')(fixture())
        self.assertFalse(r['complete_source_precursor'])
        self.assertEqual(r['predicates']['PT10']['status'],'NOT_EXECUTED')

    def test_complete_four_mode_source_control_closes_with_implicit_saha_derivative(self):
        x=fixture();start=x['thermal_initial_a'];x['thermal_cells']=[]
        for mode,end in zip(p.MODES,x['source_mode_a']):
            x['thermal_cells'].append({'t0':start,'t1':end,'mode':mode,'predictor':[['0']],
                'box':[['-1/1000000000000','1/1000000000000']]});start=end
        try:r=self.api('verify_packet')(x)
        except ValueError as e:self.fail('Complete source control did not close: '+str(e))
        self.assertTrue(r['complete_source_precursor'],r)
        self.assertEqual(r['conditional_prefix_gate'],'PASS')
        self.assertEqual(r['actual_applicability'],'INSUFFICIENT_EVIDENCE')

    def test_export_audit_distinguishes_incomplete_actual_fields(self):
        fn=self.api('audit_export')
        r=fn({'q':'Q-047','case':'camspec-lcdm','source_commit':p.SOURCE,'fields':{}},p.ROOT/'Q047_PRECURSOR_CONTRACT_V1.json')
        self.assertEqual(r['effective_field_gate'],'FAIL')
        self.assertIn('H0_CLASS',r['missing'])
        self.assertEqual(r['actual_admission_gate'],'UNRESOLVED')

    def test_repository_gate_rejects_launcher_byte_change(self):
        self.api('package_gate')
        # Temp full candidate copied before mutation: code path exercised below.
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmp:
            root=__import__('pathlib').Path(tmp)
            shutil.copytree(p.ROOT,root,dirs_exist_ok=True)
            r=p.package_gate(root);self.assertEqual(r['launcher_gate'],'PASS')
            launcher=root/'.github/workflows/00-bubbleverse-start.yml'
            launcher.write_bytes(launcher.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'LAUNCHER'):p.package_gate(root)

def fixture():
    # Artificial radiation parameters; an exact source-expression prefix only.
    # a-coordinate dy/da = G/a avoids uncertain logarithmic switch endpoints.
    return {'schema':'Q047-PRECURSOR-PACKET-V1','q':'Q-047','case':'camspec-lcdm',
       'scope':'CONDITIONAL_SOURCE_REAL_PREFIX','source_commit':p.SOURCE,
       'coordinate':'a','flags':{'has_fld':False,'has_idm':False,'has_idr':False,'has_dcdm':False,'has_dr':False,'has_varconst':False,'has_exotic_injection':False,'has_idm_b':False,'has_idm_g':False,'has_idm_dr':False,'has_ap_idmtca':False},
       'parameters':{'H0':['1','1'],'gamma':['1','1'],'ur':['0','0'],'matter':['0','0'],'lambda':['0','0'],'K':['0','0'],'T0':['3','3'],'nH0':['1/5','1/5'],'fHe':['2/25','2/25']},
       'neutrinos':[],'ede':None,'source_mode_a':['1/8000','1/6000','1/4000','1/2871'],
       'warning_z':['800','50'],'thermal_initial_a':'1/10000','thermal_initial_state':[['0','0']],
       'background_cells':[],
       'thermal_cells':[{'t0':'1/10000','t1':'1000001/10000000000','mode':'brec','predictor':[['0']], 'box':[['-1/1000','1/1000']]}]}

if __name__=='__main__':unittest.main()
