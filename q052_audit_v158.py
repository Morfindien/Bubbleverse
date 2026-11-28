"""Replay V157 and inventory the next H block from the pinned native archive.

Usage: python q052_audit_v158.py V157_DIRECTORY V152_RAW_DIRECTORY OUTPUT_JSON
Run Python with assertions enabled and mpmath 1.3.0. The raw directory
contains the measured/L and measured/R files from the V152 Actions archive.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import file_digest, sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json
import subprocess
import sys


def load(path):
    return json.loads(path.read_bytes())


def file_hash(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()


def fingerprint(mapping):
    raw = json.dumps(mapping, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


def verify_file(path, item):
    assert path.stat().st_size == item['size_bytes'], path
    assert file_hash(path) == item['sha256'], path


def binary(value):
    return Fraction.from_float(float.fromhex(value))


def hull(rows):
    return [min(Fraction(row[0]) for row in rows), max(Fraction(row[1]) for row in rows)]


def validate_block(bins, domain, count, fields):
    assert len(bins) == count
    assert [bins[0]['z'][0], bins[-1]['z'][1]] == domain
    assert all(Fraction(row['z'][0]) < Fraction(row['z'][1]) for row in bins)
    assert all(a['z'][1] == b['z'][0] for a, b in zip(bins, bins[1:]))
    for key, outer in fields.items():
        assert all(Fraction(row[key][0]) <= Fraction(row[key][1]) for row in bins)
        assert hull([row[key] for row in bins]) == list(map(Fraction, outer))


def inside(inner, outer):
    lo, hi = map(Fraction, inner)
    return Fraction(outer[0]) <= lo <= hi <= Fraction(outer[1])


def raw_rows(table):
    rows = []
    with table.open() as stream:
        header = json.loads(next(stream))
        assert header['index_bg_H'] == 1
        for i, line in enumerate(stream):
            if i > 31706:
                break
            if i >= 31702:
                row = json.loads(line)
                assert row['i'] == i
                rows.append({key: row[key] for key in ('i','z','loga')} |
                            {'H':row['background'][1], 'H_d2':row['d2background_dloga2'][1]})
    assert len(rows) == 5
    return rows


def raw_calls(trace, domain):
    selected = []
    with trace.open() as stream:
        for line, raw in enumerate(stream, 1):
            row = json.loads(raw)
            z = binary(row['z'])
            if domain[0] <= z <= domain[1]:
                selected.append({'line':line,'tag':row['tag'],'z':row['z'],'H':row['pvecback_normal'][1]})
    return selected


def verify_next_pieces(rows):
    # Decimal.ln is correctly rounded at 90 figures. Adjacent Decimal values
    # enclose the exact log. Reserve the V157 physical-to-native shift budget.
    shift = Fraction(1, 2**44) / (800 - Fraction(1, 2**44)) + Fraction(1, 2**51)
    knots = [binary(row['loga']) for row in rows]
    assert all(a < b for a, b in zip(knots, knots[1:]))
    with localcontext() as ctx:
        ctx.prec = 90
        for z, i in [(800,1),(799,2)]:
            u = -Decimal(z+1).ln()
            lo, hi = Fraction(u.next_minus())-shift, Fraction(u.next_plus())+shift
            assert knots[i] < lo <= hi < knots[i+1]
    return {'core_rows':[31703,31704,31705], 'halo_rows':[31702,31706],
            'closed_domain_z':['799','800'], 'shift_budget':str(shift)}


def main(previous, raw, output):
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    parent = load(previous/'Q052_RESULTATINDTAG_OPGAVE_V157.json')
    signature = parent.pop('fingerprint_sha256')
    assert fingerprint(parent) == signature
    assert parent['current_q'] == parent['target_q'] == 'Q052'
    assert (parent['source_state_version'],parent['target_state_version']) == ('V157','V158')
    for item in parent['output_refs']:
        verify_file(previous/item['path'], item)
    cert_path = previous/parent['result_ref']
    current = load(cert_path)
    assert parent['result']['signed_uniform'] == current['total']['exact']
    assert parent['result']['signed_relative'] == current['relative']['exact']
    assert parent['result']['domain_z'] == current['domain_z']
    assert parent['result']['assumptions'] == current['assumptions']
    validate_block(current['bins'], current['domain_z'], 1024,
                   {key:current[key]['exact'] for key in ('total','relative')})

    with TemporaryDirectory() as tmp, ZipFile(previous/parent['replay_ref']) as archive:
        tmp = Path(tmp)
        for name in archive.namelist():
            assert name == Path(name).name and name not in ('.','..')
        archive.extractall(tmp)
        for item in load(tmp/'manifest.json')['entries']:
            verify_file(tmp/item['path'],item)
        (tmp/cert_path.name).unlink()
        subprocess.run([sys.executable,'q052_verify_v157.py'],cwd=tmp,check=True)
        assert (tmp/cert_path.name).read_bytes() == cert_path.read_bytes()
        old_file = tmp/'Q052_SEGMENTCERTIFIKAT_V155.json'
        assert file_hash(old_file) == current['V155_sha256']
        old = load(old_file)
        validate_block(old['bins'], old['domain_z'],256,
                       {'total':old['uniform_total_Mpc_inverse'],'relative':old['uniform_relative']})
        assert current['native_input_extension']==old['native_real_input_extension']
        assert current['assumptions']==old['conditional_assumptions']
        assert current['source_commit']==old['source_commit']
        boundary = current['domain_z'][1]
        assert boundary == old['domain_z'][0]
        assert Fraction(current['domain_z'][0]) == 800 and Fraction(old['domain_z'][1]) == 810
        for index,key in enumerate(('total','relative')):
            assert inside(current['endpoints'][boundary][index],old['bins'][0][key])
        combined = hull([current['relative']['exact'],old['uniform_relative']])
        assert combined == list(map(Fraction,current['combined_relative_800_to_810']['exact']))
        assert max(map(abs,combined)) < Fraction(65,10**6)
        predecessor = load(tmp/'Q052_EVIDENS_V156.json')['coverage_audit']
        with ZipFile(next(tmp.glob('*V105.zip'))) as reference:
            state = json.loads(reference.read('result_raw105.json'))
            last_cell = state['cells'][-1]
            assert len(state['cells'])==142 and Fraction(last_cell['a1'])==Fraction(1,801)
            assert last_cell['energy'] == current['energy800']
            assert state['source_commit']==current['source_commit']
            anchor = {'archive_member':'result_raw105.json','cell_one_based':142,
                      'a':last_cell['a1'],'z':'800','state_phi_X':last_cell['endpoint'],
                      'energy':last_cell['energy'],'source_commit':state['source_commit'],
                      'capture_sha256':state['capture_sha256']}

    rows = None
    calls = {}
    hashes = {}
    for arm in ('L','R'):
        names = [f'measured/{arm}/{name}.jsonl' for name in ('background_table_hex','fullstate_trace')]
        for name in names:
            digest = file_hash(raw/name)
            assert digest == predecessor['raw_member_hashes'][name]
            hashes[name] = digest
        selected_rows = raw_rows(raw/names[0])
        if rows is None:
            rows = selected_rows
        assert rows == selected_rows
        prior_rows = {row['i']:row for row in predecessor['native_rows']}
        assert all(prior_rows[row['i']]==row for row in rows[:4])
        witnesses = raw_calls(raw/names[1],(799,800))
        calls[arm] = {'counts':dict(Counter(row['tag'] for row in witnesses)), 'witnesses':witnesses}
    next_pieces = verify_next_pieces(rows)
    result = {
        'case':'Q052','version':'V158','handoff_fingerprint':signature,
        'certificate_sha256':file_hash(cert_path),'replay_exact':True,'verified_output_count':len(parent['output_refs']),
        'blocks':[{'version':'V157','z':current['domain_z'],'bins':1024},
                  {'version':'V155','z':old['domain_z'],'bins':256}],
        'seam':{'z_exact':boundary,'V157_point_enclosed_in_V155_first_bin':True},
        'merged_domain_z':['800','810'],'merged_relative_exact':list(map(str,combined)),
        'merged_relative_abs_upper':'65/1000000','replayed_witness_counts':current['witness_counts'],
        'reference_endpoint':anchor, 'next_native_geometry':next_pieces,
        'native_rows':rows,'archived_next_witnesses':calls,'raw_member_hashes':hashes,
        'new_uniform_bound_below_800':None,
    }
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print({arm:item['counts'] for arm,item in calls.items()})


if __name__=='__main__':
    main(*(Path(arg).resolve() for arg in sys.argv[1:]))
