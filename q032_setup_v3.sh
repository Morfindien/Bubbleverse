#!/usr/bin/env bash
set -euo pipefail

export CURRENT_Q="Q-032"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
export COBAYA_PACKAGES_PATH="${COBAYA_PACKAGES_PATH:-$ROOT/external/cobaya_packages}"
mkdir -p q032_runtime

if [[ ! -f q032_setup_v2.sh ]]; then
  echo "Q032_V2_SETUP_PARENT_GATE=FAIL missing=q032_setup_v2.sh" >&2
  exit 2
fi
if [[ ! -f q032_planck_tt3pair_bridge_v2.py ]]; then
  echo "Q032_V2_PROGRAM_PARENT_GATE=FAIL missing=q032_planck_tt3pair_bridge_v2.py" >&2
  exit 2
fi

# V3 is CamSpec-only. Reuse the exact validated V2 CamSpec bootstrap and do not
# install or execute HiLLiPoP.
bash q032_setup_v2.sh camspec

python - <<'PY'
import hashlib, importlib.metadata as md, json, os, pathlib, subprocess, sys
root=pathlib.Path('.').resolve()
assert os.environ.get('CURRENT_Q')=='Q-032'
assert sys.version_info[:2]==(3,11),sys.version
classdir=root/'external'/'class_ede'
assert classdir.exists(), classdir
commit=subprocess.check_output(['git','-C',str(classdir),'rev-parse','HEAD'],text=True).strip()
assert commit=='5a131c91d657dd9a7c6364cc45b038710f8d0d97',commit

def digest(path):
    p=pathlib.Path(path)
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return {'path':str(p),'size':p.stat().st_size,'sha256':h.hexdigest()}

versions={}
for name in ['cobaya','PyYAML','numpy','scipy','Py-BOBYQA','getdist','Cython','sacc','astropy']:
    try: versions[name]=md.version(name)
    except md.PackageNotFoundError: versions[name]='NOT_INSTALLED'
expected={'cobaya':'3.5.6','PyYAML':'6.0.2','numpy':'1.26.4','scipy':'1.15.3','Py-BOBYQA':'1.5.0','getdist':'1.6.1','Cython':'0.29.37','sacc':'1.0.2','astropy':'7.2.2'}
for k,v in expected.items():
    assert versions[k]==v,(k,versions[k],v)

runtime={
 'q':'Q-032','run_id':'Q032-CAMSPEC-NESTED-ADDBACK-V3','result_id':'R-Q032-EDE-CAMSPEC-ADDBACK-003',
 'status':'PASS','python_version':sys.version.split()[0],
 'backend_commit':commit,'camspec_component':'planck_NPIPE_highl_CamSpec.TTTEEE',
 'parent_q032_v2_run':'Q032-PLANCK-TT3PAIR-COMMON-SUPPORT-BRIDGE-V2',
 'parent_q032_v2_result':'R-Q032-EDE-PLANCK-TT3PAIR-BRIDGE-002',
 'software_versions':versions,
 'program_hashes':{
   'q032_camspec_addback_v3.py':digest('q032_camspec_addback_v3.py'),
   'q032_planck_tt3pair_bridge_v2.py':digest('q032_planck_tt3pair_bridge_v2.py'),
   'q019_planck_cosmology_reprofile_v1.py':digest('q019_planck_cosmology_reprofile_v1.py'),
 },
 'excluded_execution_components':['HiLLiPoP','ACT','SPT','BAO','SN','lensing','low_l'],
}
pathlib.Path('q032_runtime/q032_camspec_addback_runtime_v3.json').write_text(json.dumps(runtime,indent=2,sort_keys=True)+'\n')
print('Q032_V3_CONTEXT_CONTINUITY_GATE=PASS')
print('Q032_V3_BACKEND_IDENTITY_GATE=PASS')
print('Q032_V3_CAMSPEC_RUNTIME_GATE=PASS')
PY
