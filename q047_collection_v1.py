#!/usr/bin/env python3
"""Q047 offline planner, optional future observer build/capture, and strict ingestion.
No network calls, installation, CLASS rebuild, repository writes, or scientific PASS.
The preflight and validate subcommands never load a native library.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import re
import signal
import struct
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
LOCK_SHA = "4b64c2b4724ae5ee1fed8c099625a33653ef6ac8d3f3ada0cfa7fcdeec1f6b7a"
SOURCE = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
BINARY = "df1e81831dae7e88b651342a3d72de7597cf2b1145586035c6226715dbca04cf"
CASES = {"camspec-lcdm", "camspec-ede_n3", "hillipop-lcdm", "hillipop-ede_n3"}
REQUIRED_OUTPUTS = ["accepted_initial_hex.json", "effective_background_hex.json",
    "thermal_starts_hex.jsonl", "effective_precision.json", "native_background.tsv",
    "native_thermodynamics.tsv", "runtime_maps.txt", "observation_counters.json"]

class GateError(ValueError):
    pass

def need(condition, reason):
    if not condition:
        raise GateError(reason)

def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, "DUPLICATE_JSON_KEY " + k)
        d[k] = v
    return d

def decode(s):
    return json.loads(s, object_pairs_hook=unique,
        parse_constant=lambda s: (_ for _ in ()).throw(GateError("NONFINITE_JSON " + s)))

def read(path):
    return decode(Path(path).read_text(encoding="utf-8"))

def write(path, data):
    # Outputs are new evidence objects; never overwrite a completed receipt.
    with Path(path).open("x", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")

def bits(x):
    return struct.pack(">d", x)

HEX = re.compile(r"-?0x[0-9a-f]+(?:\.[0-9a-f]*)?p[+-]?[0-9]+\Z")
def native(s):
    need(isinstance(s, str) and HEX.fullmatch(s), "HEX_ENCODING")
    try:
        x = float.fromhex(s)
    except (ValueError, OverflowError) as e:
        raise GateError("HEX_ENCODING") from e
    need(math.isfinite(x), "NONFINITE_HEX")
    # Reject a longer mantissa that silently rounds on Python ingestion.
    sign = -1 if s.startswith("-") else 1
    mantissa, power = s.lstrip("-")[2:].split("p")
    digits = mantissa.replace(".", "")
    after = len(mantissa.split(".")[1]) if "." in mantissa else 0
    from fractions import Fraction
    p = int(power) - 4 * after
    exact = Fraction(sign * int(digits, 16)) * (Fraction(2) ** p)
    need(Fraction.from_float(x) == exact, "HEX_NOT_EXACT_BINARY64")
    return x

def fields(obj, names):
    need(isinstance(obj, dict) and set(names) <= obj.keys(), "MISSING_FIELDS")
    return {k: native(obj[k]) for k in names}

def lock():
    p = HERE / "Q047_COLLECTION_LOCK_V1.json"
    need(sha(p) == LOCK_SHA, "LOCK_HASH")
    c = read(p)
    need(c["source_commit"] == SOURCE and c["binary_sha256"] == BINARY, "SOURCE_BINARY_PIN")
    need(set(c["cases"]) == CASES, "FOUR_CASE_SCOPE")
    need(sha(HERE / "q047_collect_state_v1.c") == c["observer_source_sha256"], "OBSERVER_SOURCE_HASH")
    need(sha(HERE / "Q047_PRECURSOR_CONTRACT_V1.json") == c["precursor_contract_sha256"], "PRECURSOR_CONTRACT_HASH")
    return c

def process(cmd, timeout=30):
    return subprocess.check_output(cmd, text=True, timeout=timeout, stderr=subprocess.STDOUT)

def source_check(root, c):
    root = Path(root).resolve()
    need(root.is_dir(), "SOURCE_DIRECTORY_MISSING")
    need(process(["git", "-C", str(root), "rev-parse", "HEAD"]).strip() == SOURCE, "SOURCE_COMMIT")
    subprocess.run(["git", "-C", str(root), "diff", "--quiet", "HEAD"], check=True, timeout=30)
    for name, h in c["source_files_sha256"].items():
        need((root / name).is_file() and sha(root / name) == h, "SOURCE_FILE " + name)
    return str(root)

def table_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        header = f.readline().rstrip("\r\n")
        need(header.startswith("# "), "TABLE_HEADER")
        columns = header[2:].split("\t")
        need(columns and all(columns) and len(columns) == len(set(columns)), "TABLE_COLUMNS")
        yield columns
        count = 0
        for row in csv.reader(f, delimiter="\t"):
            need(len(row) == len(columns), "TABLE_ROW_WIDTH")
            nums = [float(s) for s in row]
            need(all(math.isfinite(v) for v in nums), "TABLE_NONFINITE")
            count += 1
            yield nums
        need(count >= 3, "TABLE_TOO_SHORT")

def compare_tables(original, reconstructed):
    a, b = table_rows(original), table_rows(reconstructed)
    ca, cb = next(a), next(b)
    need(set(ca) == set(cb), "REPRODUCTION_COLUMNS")
    order = [cb.index(k) for k in ca]
    missing = object()
    count = 0
    for r, s in itertools.zip_longest(a, b, fillvalue=missing):
        need(r is not missing and s is not missing, "REPRODUCTION_ROW_COUNT")
        need(all(bits(r[j]) == bits(s[order[j]]) for j in range(len(ca))),
             "REPRODUCTION_BITS row=" + str(count))
        count += 1
    return {"rows": count, "columns": len(ca), "comparison": "ALL_BINARY64_BITS_INCLUDING_SIGNED_ZERO"}

def baseline_check(case, c, bg, thermal):
    expected = c["cases"][case]
    for path, key in [(bg, "background_sha256"), (thermal, "thermodynamics_sha256")]:
        need(Path(path).is_file() and sha(path) == expected[key], "ORIGINAL_MEMBER_HASH " + key)
    return expected

def preflight(args, c):
    source_check(args.source_dir, c)
    p = Path(args.binary).resolve()
    need(p.is_file() and sha(p) == BINARY, "ORIGINAL_BINARY_MISSING_OR_WRONG")
    need(platform.system() == "Linux" and platform.machine() == "x86_64", "PLATFORM")
    need(platform.python_version() == "3.11.16", "ORIGINAL_PYTHON_RUNTIME")
    need(not os.environ.get("LD_PRELOAD"), "UNDECLARED_PRELOAD")
    need(all(os.environ.get(k) == "1" for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]), "THREAD_POLICY")
    symbols = process(["nm", "-D", "--defined-only", str(p)])
    names = {line.split()[-1] for line in symbols.splitlines() if line.split()}
    need(set(c["required_symbols"]) <= names, "ORIGINAL_EXPORTED_SYMBOLS")
    if args.case:
        baseline_check(args.case, c, args.baseline_background, args.baseline_thermal)
    return {"source_commit": SOURCE, "binary_sha256": BINARY, "binary_path": str(p),
        "python": platform.python_version(), "platform": platform.platform(),
        "checked_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "native_library_loaded": False, "initialization_executed": False}

def identity(obj, case):
    need(obj.get("schema") == "Q047_CAPTURE_V1" and obj.get("case") == case, "CAPTURE_CASE_SCHEMA")
    need(obj.get("origin") == "NEW_RECONSTRUCTION" and obj.get("number_encoding") == "C99_hex_binary64", "CAPTURE_ORIGIN")

def validate_state(d, case, c):
    ba = read(d / "effective_background_hex.json")
    ini = read(d / "accepted_initial_hex.json")
    identity(ba, case); identity(ini, case)
    need(ini["callback"] == "background_initial_conditions:return_before_evolver", "INITIAL_CALLBACK")
    constants = fields(ba["fields"], ["H0", "K", "Omega0_b", "Omega0_cdm", "Omega0_g", "Omega0_lambda", "Omega0_ur", "T_cmb"])
    need(constants["H0"] > 0 and constants["T_cmb"] > 0 and constants["K"] == 0, "BACKGROUND_DOMAIN")
    need(type(ba["rounding_mode"]) is int and type(ba["FE_TONEAREST"]) is int and ba["rounding_mode"] == ba["FE_TONEAREST"], "ROUNDING_MODE")
    flags = ba["flags"]
    need(set(flags) == set(c["expected_background_flags"]), "BACKGROUND_FLAG_SET")
    need(all(type(v) is int and v in (0, 1) for v in flags.values()), "BACKGROUND_FLAG_VALUES")
    for k, v in c["expected_background_flags"].items():
        if v is not None:
            need(flags[k] == v, "UNSUPPORTED_BACKGROUND " + k)
    ede = case.endswith("ede_n3")
    need(flags["has_scf"] == int(ede) and flags["has_lambda"] == int(not ede), "MODEL_FLAGS")
    tflags = ba["thermal_flags"]
    need(set(tflags) == {"has_varconst", "has_exotic_injection", "has_idm_b", "has_idm_g", "has_idm_dr", "recombination"}, "THERMAL_FLAG_SET")
    need(all(type(tflags[k]) is int and tflags[k] == 0 for k in tflags if k != "recombination"), "UNSUPPORTED_THERMAL_FLAGS")
    need(type(tflags["recombination"]) is int and tflags["recombination"] == c["hyrec_enum"], "HYREC_ENUM")
    init_fields = fields(ini["fields"], ["loga_ini", "a_ini_native"])
    need(init_fields["loga_ini"] < 0 and 0 < init_fields["a_ini_native"] < 1, "INITIAL_SCALE")
    y = [native(v) for v in ini["integration_vector"]]
    need(type(ini["bi_size"]) is int and ini["bi_size"] == len(y) and len(y) >= 5, "INITIAL_VECTOR_SIZE")
    indices = ini["bi_indices"]
    need(set(indices) == ({"time", "tau", "rs", "D", "D_prime", "phi", "phi_prime"} if ede else {"time", "tau", "rs", "D", "D_prime"}), "INITIAL_INDICES")
    need(len(set(indices.values())) == len(indices) and all(type(i) is int and 0 <= i < len(y) for i in indices.values()), "INITIAL_INDEX_RANGE")
    need(len(indices) == len(y), "UNMAPPED_INITIAL_COMPONENT")
    if ede:
        sc = ba["scalar"]
        need(type(sc["attractor_ic_scf"]) is int and type(sc["scf_tuning_index"]) is int and sc["attractor_ic_scf"] == 0 and sc["scf_tuning_index"] == 3, "SCALAR_VARIANT")
        sp = [native(v) for v in sc["scf_parameters"]]
        need(len(sp) == 6 and sp[1] > 0 and sp[2] > 0, "SCALAR_PARAMETERS")
        need(sp != [1, 1, 1, 1, 1, 0], "REQUESTED_PLACEHOLDER_AS_EFFECTIVE")
        sf = fields(sc["fields"], ["n_scf", "CC_scf", "phi_ini_scf", "phi_prime_ini_scf"])
        need(sf["n_scf"] == 3 and sf["CC_scf"] == 1, "SCALAR_N_CC")
        initial = fields(ini["fields"], ["phi_ini", "phi_prime_ini"])
        for a, b in [("phi_ini", "phi_ini_scf"), ("phi_prime_ini", "phi_prime_ini_scf")]:
            idx = indices["phi" if a == "phi_ini" else "phi_prime"]
            need(bits(initial[a]) == bits(sf[b]) == bits(y[idx]), "INITIAL_SCALAR_LINK")
    else:
        need(ba["scalar"] is None, "LCDM_SCALAR")
    need(type(ba["N_ncdm"]) is int and ba["N_ncdm"] == 1 and len(ba["neutrinos"]) == 1, "NEUTRINO_SPECIES")
    for nu in ba["neutrinos"]:
        need(type(nu["got_files"]) is int and nu["got_files"] == 0 and type(nu["quadrature_strategy"]) is int, "NEUTRINO_DISTRIBUTION")
        nf = fields(nu["fields"], ["M_ncdm", "T_ncdm", "deg_ncdm", "ksi_ncdm", "factor_ncdm"])
        need(all(nf[k] > 0 for k in nf if k != "ksi_ncdm"), "NEUTRINO_NORMALIZATION")
        nodes, weights = [native(x) for x in nu["q_ncdm_bg"]], [native(x) for x in nu["w_ncdm_bg"]]
        need(1 <= len(nodes) <= 200000 and len(nodes) == len(weights), "NEUTRINO_ARRAY_SIZE")
        need(all(x >= 0 for x in nodes) and all(x > 0 for x in weights) and all(x < z for x, z in zip(nodes, nodes[1:])), "NEUTRINO_NODE_ORDER")
    expected = c["cases"][case]
    need(bits(native(ba["z_reio"])) == bits(float(expected["accepted_z_reio"])), "ACCEPTED_Z_REIO")
    need(bits(native(ba["tau_reio"])) == bits(expected["class_parameters"]["tau_reio"]), "REQUESTED_TAU")
    starts = [decode(s) for s in (d / "thermal_starts_hex.jsonl").read_text().splitlines()]
    need(1 <= len(starts) <= 512, "THERMAL_START_COUNT")
    first = starts[0]
    phases = first["phase_indices"]
    need(set(phases) == {"brec", "He1", "He1f", "He2", "H", "frec", "reio"}, "PHASE_INDEX_SET")
    need(all(type(i) is int and i >= 0 for i in phases.values()) and len(set(phases.values())) == 7, "PHASE_INDEX_VALUES")
    need(first["phase"] == phases["brec"], "EARLY_THERMAL_START")
    seen = set()
    previous = None
    for i, row in enumerate(starts, 1):
        identity(row, case)
        need(row["event"] == i and row["phase_indices"] == phases, "THERMAL_SEQUENCE")
        mz = native(row["mz"])
        need(mz <= 0 and (previous is None or mz >= previous), "THERMAL_CHRONOLOGY")
        previous = mz
        need(row["phase"] in phases.values(), "THERMAL_PHASE")
        seen.add(row["phase"])
        tv = [native(v) for v in row["y"]]
        need(all(type(row[k]) is int and row[k] in (0, 1) for k in ["require_H", "require_He"]), "THERMAL_REQUIRE_FLAGS")
        ids = [row["D_index"]] + [row[k] for flag, k in [("require_H", "H_index"), ("require_He", "He_index")] if row[flag]]
        need(len(set(ids)) == len(ids) == len(tv) and all(type(j) is int and 0 <= j < len(tv) for j in ids), "THERMAL_VECTOR_MAPPING")
        cf = fields(row["constants"], ["Tcmb", "nH0_SI", "fHe_CLASS", "YHe", "fHe_HyRec", "C_NR", "I_H", "I_HeI", "I_HeII", "native_xHeII_limit"])
        need(all(x > 0 for x in cf.values()), "THERMAL_CONSTANT_DOMAIN")
        need(bits(cf["fHe_CLASS"]) == bits(cf["fHe_HyRec"]), "HELIUM_NORMALIZATION")
        for a, b in [("nH0_SI", "nH0_m3"), ("fHe_CLASS", "fHe"), ("YHe", "YHe")]:
            need(bits(cf[a]) == bits(expected["native_meta"][b]), "GOLDEN_THERMAL_CONSTANT " + a)
        need(type(row["HyRec_error"]) is int and row["HyRec_error"] == 0, "HYREC_ERROR_LATCH")
        need(type(row["HyRec_MODEL"]) is int and row["HyRec_MODEL"] == c["hyrec_model"], "HYREC_MODEL")
        limits, deltas = [native(x) for x in row["ap_limits"]], [native(x) for x in row["ap_deltas"]]
        need(len(limits) == len(deltas) and len(limits) >= 7 and all(x >= 0 for x in deltas), "PHASE_BOUNDARY_ARRAYS")
    need(set(phases.values()) <= seen, "MISSING_THERMAL_PHASE_START")
    need(native(first["y"][first["D_index"]]) == 0, "INITIAL_D_TMAT")
    counters = read(d / "observation_counters.json")
    need(counters["capture_completed"] is True and counters["historical_export"] is False and
         counters["final_initial_calls"] == 1 and counters["thermal_start_calls"] == len(starts), "INTERPOSITION_COUNTERS")
    precision = read(d / "effective_precision.json")
    need(set(precision) == set(c["precision_parameter_names"]), "PRECISION_FIELD_COVERAGE")
    for k in c["precision_hex_names"]:
        native(precision[k])
    return {"structural_state_gate": "PASS", "thermal_start_events": len(starts),
        "source_continuum_admission": "UNRESOLVED", "PT01": "UNRESOLVED", "PT03": "UNRESOLVED"}

def validate(args, c):
    d = Path(args.capture_dir).resolve()
    expected = baseline_check(args.case, c, args.baseline_background, args.baseline_thermal)
    receipt = read(d / "capture_receipt.json")
    need(receipt["case"] == args.case and receipt["lock_sha256"] == LOCK_SHA and receipt["binary_sha256"] == BINARY, "CAPTURE_RECEIPT_IDENTITY")
    need(receipt["execution_status"] == "COMPLETED" and receipt["origin"] == "NEW_RECONSTRUCTION", "CAPTURE_EXECUTION_STATUS")
    canonical_ini = "".join(k + " = " + str(v) + "\n" for k, v in expected["class_parameters"].items())
    need((d / "requested_case.ini").read_text() == canonical_ini and
         sha(d / "requested_case.ini") == receipt["requested_case_sha256"], "FROZEN_REQUESTED_INPUT")
    observer = Path(receipt["observer_path"]).resolve()
    need(observer.is_file() and sha(observer) == receipt["observer_sha256"], "OBSERVER_BINARY_RECHECK")
    need(set(receipt["artifacts"]) == set(REQUIRED_OUTPUTS), "CAPTURE_ARTIFACT_SET")
    for name in REQUIRED_OUTPUTS:
        need((d / name).is_file() and not (d / name).is_symlink() and sha(d / name) == receipt["artifacts"][name], "CAPTURE_MEMBER_HASH " + name)
    binary = Path(receipt["binary_path"]).resolve()
    need(binary.is_file() and sha(binary) == BINARY, "LOADED_BINARY_RECHECK")
    maps = (d / "runtime_maps.txt").read_text()
    mapped = set()
    for line in maps.splitlines():
        row = line.split(maxsplit=5)
        if len(row) == 6 and row[5].startswith("/"):
            need(not row[5].endswith(" (deleted)"), "DELETED_LOADED_OBJECT")
            mapped.add(str(Path(row[5]).resolve()))
    need(str(binary) in mapped, "ORIGINAL_BINARY_NOT_LOADED")
    need(str(observer) in mapped, "OBSERVER_NOT_LOADED")
    need(set(receipt["mapped_file_hashes"]) == mapped, "MAPPED_FILE_COVERAGE")
    for p, h in receipt["mapped_file_hashes"].items():
        need(Path(p).is_file() and sha(p) == h, "MAPPED_DEPENDENCY_HASH")
    state = validate_state(d, args.case, c)
    bg = compare_tables(args.baseline_background, d / "native_background.tsv")
    th = compare_tables(args.baseline_thermal, d / "native_thermodynamics.tsv")
    return {"q": "Q-047", "case": args.case, "structural_validation": state,
        "reproduction": {"background": bg, "thermodynamics": th},
        "status": "RECONSTRUCTED_CANDIDATE_REPRODUCES_ARCHIVED_OUTPUTS",
        "scientific_verdict": "INSUFFICIENT_EVIDENCE", "final_first_hit_gate": "UNRESOLVED",
        "historical_internal_state_identity": "NOT_PROVEN_BY_OUTPUT_EQUALITY",
        "observer_neutrality": "NOT_FULLY_PROVEN_BY_OUTPUT_EQUALITY",
        "remaining": c["remaining_scientific_obligations"], "lock_sha256": LOCK_SHA}

def build(args, c):
    preflight(args, c)
    d = Path(args.output).resolve(); d.mkdir(parents=True, exist_ok=False)
    root = Path(args.source_dir).resolve(); binary = Path(args.binary).resolve()
    ldflags = process([args.python_config, "--embed", "--ldflags"]).split()
    command = [args.cc, "-std=c11", "-O0", "-fno-fast-math", "-ffp-contract=off", "-rdynamic",
        "-I" + str(root / "include"), "-I" + str(root / "external/HyRec2020"),
        "-I" + str(root / "external/heating"), "-I" + str(root / "external/RecfastCLASS"), str(HERE / "q047_collect_state_v1.c"),
        str(binary), "-Wl,-rpath," + str(binary.parent), "-ldl", "-lm", *ldflags,
        "-o", str(d / "q047_observer")]
    with (d / "observer_build.log").open("x") as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, check=True, timeout=120)
    write(d / "observer_build_receipt.json", {"command": command,
        "observer_sha256": sha(d / "q047_observer"), "observer_source_sha256": c["observer_source_sha256"],
        "binary_sha256": BINARY, "source_commit": SOURCE,
        "core_rebuilt": False, "native_initialization_executed": False,
        "compiler_version": process([args.cc, "--version"]),
        "original_core_compiler_flags": "NOT_RECOVERED", "arithmetic_error_proof": "NOT_PROVIDED"})
    return {"status": "OBSERVER_BUILT_NOT_EXECUTED", "output": str(d)}

def collect(args, c):
    pf = preflight(args, c)
    need(args.execute_new_reconstruction, "EXPLICIT_CAPTURE_COMMAND_REQUIRED")
    need(1 <= args.timeout <= 600, "CAPTURE_TIME_CAP_600_SECONDS")
    observer = Path(args.observer).resolve(); br = read(args.build_receipt)
    need(observer.is_file() and sha(observer) == br["observer_sha256"] and
         br["observer_source_sha256"] == c["observer_source_sha256"] and br["binary_sha256"] == BINARY and
         br["source_commit"] == SOURCE and br["core_rebuilt"] is False, "OBSERVER_BUILD_IDENTITY")
    d = Path(args.output).resolve(); d.mkdir(parents=True, exist_ok=False)
    ini = d / "requested_case.ini"
    with ini.open("x") as f:
        for k, v in c["cases"][args.case]["class_parameters"].items():
            f.write(k + " = " + str(v) + "\n")
    write(d / "attempt.json", {"case": args.case, "origin": "NEW_RECONSTRUCTION", "preflight": pf,
        "requested_case_sha256": sha(ini), "observer_build": br,
        "native_evaluation_status": "ABOUT_TO_START", "budget_before": c["budget"],
        "budget_after": "MUST_ACCOUNT_ACTUAL_EXECUTION; NO_ASSUMED_INCREMENT"})
    env = dict(os.environ, Q047_CAPTURE_DIR=str(d), Q047_CAPTURE_CASE=args.case, LC_ALL="C")
    started = time.monotonic()
    with (d / "native.log").open("x") as log:
        p = subprocess.Popen([str(observer), str(ini)], stdout=log, stderr=subprocess.STDOUT,
            env=env, cwd=str(Path(args.source_dir).resolve()), start_new_session=True)
        try:
            code = p.wait(timeout=args.timeout)
        except BaseException:
            os.killpg(p.pid, signal.SIGTERM)
            try: p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL); p.wait()
            write(d / "capture_failure.json", {"status": "INTERRUPTED", "scientific_verdict": "UNCHANGED"})
            raise
    if code:
        write(d / "capture_failure.json", {"exit_code": code, "status": "NATIVE_FAILURE", "scientific_verdict": "UNCHANGED"})
        raise GateError("NATIVE_CAPTURE_FAILED")
    mapped = {}
    for line in (d / "runtime_maps.txt").read_text().splitlines():
        row = line.split(maxsplit=5)
        if len(row) == 6 and row[5].startswith("/"):
            need(not row[5].endswith(" (deleted)"), "DELETED_LOADED_OBJECT")
            path = Path(row[5]).resolve(); mapped[str(path)] = sha(path)
    write(d / "capture_receipt.json", {"case": args.case, "origin": "NEW_RECONSTRUCTION",
        "execution_status": "COMPLETED", "elapsed_seconds": time.monotonic() - started,
        "binary_sha256": BINARY, "binary_path": pf["binary_path"], "lock_sha256": LOCK_SHA,
        "observer_path": str(observer), "observer_sha256": sha(observer), "requested_case_sha256": sha(ini),
        "artifacts": {n: sha(d / n) for n in REQUIRED_OUTPUTS}, "mapped_file_hashes": mapped,
        "scientific_qualification": "NOT_ESTABLISHED", "original_core_compiler_flags": "NOT_RECOVERED"})
    args.capture_dir = str(d)
    assessment = validate(args, c)
    write(d / "candidate_assessment.json", assessment)
    return assessment

def main():
    p = argparse.ArgumentParser(description=__doc__)
    s = p.add_subparsers(dest="action", required=True)
    s.add_parser("inspect", help="Offline package and four-case input check; no native work")
    for name in ["preflight", "build-observer", "collect", "validate"]:
        q = s.add_parser(name)
        if name != "validate":
            q.add_argument("--source-dir", required=True); q.add_argument("--binary", required=True)
        q.add_argument("--case", choices=sorted(CASES), required=name in ["collect", "validate"])
        q.add_argument("--baseline-background"); q.add_argument("--baseline-thermal")
        if name == "build-observer":
            q.add_argument("--cc", default="gcc"); q.add_argument("--python-config", default="python3-config")
        if name in ["build-observer", "collect"]:
            q.add_argument("--output", required=True)
        if name == "collect":
            q.add_argument("--observer", required=True); q.add_argument("--build-receipt", required=True)
            q.add_argument("--execute-new-reconstruction", action="store_true")
            q.add_argument("--timeout", type=int, default=600)
        if name == "validate": q.add_argument("--capture-dir", required=True)
    args = p.parse_args()
    try:
        c = lock()
        if args.action == "inspect":
            result = {"status": "OFFLINE_PACKAGE_IDENTITY_PASS", "cases": sorted(CASES),
                "native_capture": "NOT_EXECUTED", "scientific_verdict": "INSUFFICIENT_EVIDENCE",
                "required_original_binary": BINARY, "next_action": "ORIGINAL_ENVIRONMENT_PREFLIGHT"}
        else:
            if args.case:
                need(args.baseline_background and args.baseline_thermal, "ORIGINAL_TABLE_PATHS_REQUIRED")
            if args.action == "preflight": result = preflight(args, c)
            elif args.action == "build-observer": result = build(args, c)
            elif args.action == "collect": result = collect(args, c)
            else: result = validate(args, c)
        print(json.dumps(result, indent=2, allow_nan=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "BLOCKED_OR_REJECTED", "action": args.action,
            "error": str(e), "scientific_verdict": "UNCHANGED", "retry_unchanged_inputs": False}, indent=2))
        return 2

if __name__ == "__main__":
    sys.exit(main())
