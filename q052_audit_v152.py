# Q052 V152 archive audit. Run with Python 3.10+ and assertions enabled.
from bisect import bisect_right
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
from itertools import zip_longest
from pathlib import Path
import csv
import json

root = Path(__file__).resolve().parent
raw = root / "raw"
unhex = float.fromhex
manifest = json.loads((raw / "measured-manifest.json").read_text())
assert {f["path"] for f in manifest} == {
    str(p.relative_to(raw)) for p in (raw / "measured").rglob("*") if p.is_file()
}
for f in manifest:
    payload = (raw / f["path"]).read_bytes()
    assert len(payload) == f["size"] and sha256(payload).hexdigest() == f["sha256"], f["path"]


def json_lines(path):
    with path.open() as src:
        yield from map(json.loads, src)


def coordinate(z):
    with localcontext() as ctx:
        ctx.prec = 68
        return -float(Decimal.from_float(1.0+z).ln())


def cubic(u, left, right, j, number):
    lo, hi = (number(unhex(r["loga"])) for r in (left,right))
    y0, y1 = (number(unhex(r["background"][j])) for r in (left,right))
    m0, m1 = (number(unhex(r["d2background_dloga2"][j])) for r in (left,right))
    h = hi-lo
    b = (u-lo)/h
    a = 1-b
    return a*y0 + b*y1 + ((a*a*a-a)*m0 + (b*b*b-b)*m1)*h*h/6


audit = {
    "archive_members_verified": len(manifest),
    "arms": {},
    "body_identical": {},
    "physical_optical_depth_tau_T_and_conformal_time_eta_are_distinct": True,
}
body = {}
for arm in ("L","R"):
    d = raw / "measured" / arm
    p = d / "background_table_hex.jsonl"
    with p.open("rb") as source:
        header = json.loads(source.readline())
        body[arm] = sha256(source.read()).hexdigest()
    source = json_lines(p)
    next(source)
    rows = list(source)
    assert len(rows) == header["bt_size"] == 40000
    u_nodes = [unhex(r["loga"]) for r in rows]
    assert all(x<y for x,y in zip(u_nodes,u_nodes[1:]))
    diag = json.loads((d / "diagnostic_manifest.json").read_text())
    j = diag["background_indices"]["H"]
    assert j == header["index_bg_H"] == 1
    coords = list(json_lines(d / "coordinate_trace.jsonl"))
    for r in coords:
        assert unhex(r["loga"]).hex() == coordinate(unhex(r["z"])).hex(), r
        assert unhex(r["one_plus_z"]).hex() == (1+unhex(r["z"])).hex()
    start_coord = next(r for r in coords if unhex(r["z"]) == 810)
    traces = list(json_lines(d / "fullstate_trace.jsonl"))
    first = traces[0]
    assert first["tag"] == "RHS" and unhex(first["z"]) == 810
    assert first["phase"] == 5 and first["require_H"] == 1 and first["require_He"] == 0
    guards = json_lines(d / "hyrec_guard_trace.jsonl")
    totals = Counter()
    errors = []
    samples = {}
    for index, r in enumerate(traces):
        label = r["tag"]
        totals[label] += 1
        z = unhex(r["z"])
        assert 0<=z<=810, r
        u = coordinate(z)
        i = min(bisect_right(u_nodes,u)-1,len(rows)-2)
        assert 0<=i and u_nodes[i]<=u<=u_nodes[i+1]
        observed = unhex(r["pvecback_normal"][j])
        h = cubic(u, rows[i], rows[i+1], j, float)
        if h.hex() != observed.hex():
            errors.append({"line":index+1,"tag":label,"z_hex":r["z"],"i":i,"calc":h.hex(),"observed":observed.hex()})
        if label == "RHS":
            g = next(guards)
            assert g["z"] == r["z"] and g["xe"] == r["workspace"]["x_noreio"] and g["xHII"] == r["workspace"]["x_H"]
            converted = observed * 299792458.0 / 3.085677581282e22
            assert converted.hex() == unhex(g["H_per_s"]).hex(), (index, converted.hex(), g["H_per_s"])
            totals["HYREC_JOIN"] += 1
        if index == 0:
            exact = cubic(Fraction(u), rows[i], rows[i+1], j, Fraction)
            samples["first_RHS"] = {
                "line":1, "z":r["z"], "phase":r["phase"], "loga":start_coord["loga"],
                "H_Mpc_inverse":observed.hex(), "H_per_s_HyRec":g["H_per_s"],
                "H_Mpc_inverse_decimal":repr(observed), "observed_HyRec_branch":g["observed_child_calls"],
                "exact_native_minus_stored_H_at_used_u": str(Fraction(observed)-exact),
                "exact_native_minus_stored_H_display": repr(float(Fraction(observed)-exact)),
                "background_bracket":[ {k: rr[k] for k in ("i","z","loga")} | {
                    "H":rr["background"][j], "H_d2_du2":rr["d2background_dloga2"][j]
                } for rr in rows[i:i+2]],
                "source_trajectory_comparison": "No applicable V151 bound at this coordinate",
            }
    assert next(guards,None) is None
    phase = list(json_lines(d / "event_phase_trace.jsonl"))
    boundary = [r for r in phase if r["tag"].startswith("Z810")]
    assert len(boundary)==2 and all(unhex(r["z"])==810 for r in boundary)
    samples["event_workspace_H_at_z810"] = {r["tag"]:r["pvecback_normal"][j] for r in boundary}
    assert (totals["RHS"],totals["OUTPUT"],totals["HYREC_JOIN"]) == (
        diag["rhs_records"],diag["output_records"],diag["guard_records"])
    public = json_lines(d / "public_table_hex.jsonl")
    public_header = next(public)
    upper_file = json.loads((d / "upper_cell69.json").read_text())
    with (d / "history.csv").open() as file:
        history = csv.DictReader(file)
        last_samples = []
        for pub, hist in zip_longest(public,history):
            assert pub is not None and hist is not None
            eta = unhex(pub["eta"])
            assert eta.hex() == float(hist["eta_Mpc"]).hex()
            assert unhex(pub["z"]).hex() == float(hist["z"]).hex()
            assert unhex(pub["values"][public_header["dkappa_column"]]).hex() == float(hist["dkappa_per_Mpc"]).hex()
            if pub["i"] in (0, upper_file["lower_i"]):
                last_samples.append({k:pub[k] for k in ("i","z","eta")})
            totals["PUBLIC_HISTORY_ETA_OPACITY_JOIN"] += 1
    upper_pub = {r["i"]:{k:r[k] for k in ("i","z","eta")} for r in upper_file["top_rows"]}
    assert upper_pub[upper_file["lower_i"]] == last_samples[-1]
    eta810 = unhex(upper_file["eta810_native"])
    below, above = (upper_pub[upper_file[k]] for k in ("lower_i","upper_i"))
    assert unhex(below["z"]) < 810 < unhex(above["z"])
    assert unhex(above["eta"]) < eta810 < unhex(below["eta"])
    samples["eta_810"] = {"eta_hex":eta810.hex(), "eta_Mpc":repr(eta810),"bracket":[below,above],"table_low":last_samples[0]}
    assert not errors, errors[0] if errors else None
    audit["arms"][arm] = {"archive_counts":dict(totals),"H_exact_binary64_replay_mismatch_count":len(errors),
                          "H_first_mismatch":errors[0] if errors else None,"observed":samples}
assert body["L"] == body["R"]
assert audit["arms"]["L"]["observed"]["first_RHS"] == audit["arms"]["R"]["observed"]["first_RHS"]
assert audit["arms"]["L"]["observed"]["eta_810"] == audit["arms"]["R"]["observed"]["eta_810"]
audit["body_identical"] = {"both_40000_background_rows": True, "sha256":body["L"]}
out = root / "audit-result.json"
out.write_text(json.dumps(audit, indent=2)+"\n")
for arm, summary in audit["arms"].items():
    print(arm,summary)
