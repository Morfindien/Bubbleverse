"""Prepare and check the Q052 V141 extension of the authenticated V136 observer."""

import argparse
import copy
from hashlib import sha256
import inspect
from io import BytesIO
import json
import math
from pathlib import Path
import re
import struct
from zipfile import ZipFile

SOURCE = "5a131c91d657dd9a7c6364cc45b038710f8d0d97"
LIBRARY = "8b90e21505337cb6696c4f6460616c7c92482f6c8eba7f3450d7da5cb040fae3"
CAPTURE = "2514e250d20c456530be63e790a079176293a87a82c927b1e748d1eec405da9b"
OBSERVER = "58bbcb3fb4a2e7f86bc32774cf026bfd163cac20628ac1182140107dacea2c3c"
LAUNCHER = "67b697828400f9d7bbaa54b8459d07d0097e2ce368347b4b5030bfbc89abfbeb"
BASE_ARCHIVE = "ac862efbf369fe2cb9fbc395694ca754db3144dc069771bbdefeaa8e8024c9c1"
SITE = "0x67abe"
SCHEMA = "Q052_V141_FIRST_RHS_INPUTS_V1"
ARMS = ("L", "R")
HEX = re.compile(r"-?0x[01](?:\.[0-9a-f]{1,13})?p[+-][0-9]+")
SCALARS = ("n", "f", "m", "B")
NU_FIELDS = ("species_count", "node_count", "M", "factor")
VECTORS = ("q", "w")


def capture_effective_inputs(pba, field, hx):
    """Read the first species only, after checking pointer and declared length."""
    result = {
        "schema": "Q052_V141_FIRST_RHS_INPUTS_V1",
        "site": "0x67abe",
        "scalar": dict.fromkeys(("n", "f", "m", "B")),
        "neutrino": dict.fromkeys(("species_count", "node_count", "M", "factor", "q", "w")),
        "read_issues": [],
    }
    issues = result["read_issues"]

    def pointer(value, name):
        if int(value) != 0:
            return value
        issues.append(f"{name}: null pointer")
        return None

    params = pointer(field(pba, "scf_parameters"), "scf_parameters")
    size = int(field(pba, "scf_parameters_size"))
    if size < 4:
        issues.append(f"scf_parameters_size: {size}, need at least four")
    if params is not None and size >= 4:
        for idx, name in enumerate(("n", "f", "m", "B")):
            result["scalar"][name] = hx(params[idx])

    nu = result["neutrino"]
    nu["species_count"] = int(field(pba, "N_ncdm"))
    if nu["species_count"] < 1:
        issues.append("N_ncdm: no accessible species zero")
        return result

    for name, member in (("M", "M_ncdm"), ("factor", "factor_ncdm")):
        values = pointer(field(pba, member), member)
        if values is not None:
            nu[name] = hx(values[0])
    sizes = pointer(field(pba, "q_size_ncdm_bg"), "q_size_ncdm_bg")
    if sizes is None:
        return result
    nodes = nu["node_count"] = int(sizes[0])
    if not 1 <= nodes <= 64:
        issues.append(f"q_size_ncdm_bg[0]: {nodes}, outside safe read range 1..64")
        return result
    for name, member in (("q", "q_ncdm_bg"), ("w", "w_ncdm_bg")):
        vectors = pointer(field(pba, member), member)
        if vectors is not None:
            values = pointer(vectors[0], f"{member}[0]")
            if values is not None:
                nu[name] = [hx(values[index]) for index in range(nodes)]
    return result


def digest(data):
    return sha256(data).hexdigest()


def checked(data, expected, label):
    if digest(data) != expected:
        raise ValueError(f"SHA-256 mismatch: {label}")
    return data


def bits(value):
    if type(value) is not str or not HEX.fullmatch(value):
        raise ValueError("Expected finite binary64 in C99 hex notation")
    number = float.fromhex(value)
    if not math.isfinite(number):
        raise ValueError("Expected finite binary64")
    return struct.pack(">d", number).hex()


def load_reference(kit):
    with ZipFile(kit / "evidence/Q052_SKALARSTART_V135.zip") as historical:
        capture = json.loads(checked(historical.read("evidence/capture.json"), CAPTURE, "capture.json"))
        with ZipFile(BytesIO(historical.read("evidence/Q052_BAGGRUNDSCERTIFIKAT_V73.zip"))) as v73:
            binding = json.loads(v73.read("result.json"))
    case = "hillipop-ede_n3"
    if (capture["source_commit"], binding["capture_sha256"], binding["frozen_case"]) != (SOURCE, CAPTURE, case):
        raise ValueError("V73 reference identity differs")
    bg = capture["cases"][case]["background"]
    params = bg["scalar"]["scf_parameters"]
    neutrino, = bg["neutrinos"]
    q, w = neutrino["q_ncdm_bg"], neutrino["w_ncdm_bg"]
    if len(params) != 6 or bg["N_ncdm"] != 1 or len(q) != 11 or len(w) != 11:
        raise ValueError("Unexpected V73 reference shape")
    reference = {
        "schema": SCHEMA,
        "site": SITE,
        "scalar": dict(zip(SCALARS, params[:4], strict=True)),
        "neutrino": {
            "species_count": bg["N_ncdm"], "node_count": len(q),
            "M": neutrino["fields"]["M_ncdm"], "factor": neutrino["fields"]["factor_ncdm"],
            "q": q, "w": w,
        },
        "read_issues": [],
    }
    return reference, {"f_scf": params[1], "theta_i": params[4]}


def check_v141_startup(pair):
    """Keep V136's numerical replay and preserve a discrepancy as evidence."""
    from readback import arm_result

    if (set(pair) != set(ARMS) or any(pair[k]["arm"] != k for k in ARMS)
            or pair["L"]["run_id"] != pair["R"]["run_id"] or pair["L"]["pid"] == pair["R"]["pid"]):
        raise ValueError("Two distinct processes of one pair required")
    arms = {}
    for arm, receipt in pair.items():
        try:
            arms[arm] = arm_result(receipt)
        except (KeyError, ValueError, OverflowError) as error:
            arms[arm] = {"status": "V136_STARTUP_REPLAY_DISAGREES_OR_UNAVAILABLE", "detail": str(error)}
    return {
        "run_id": pair["L"]["run_id"], "arms": arms,
        "libm_sha256": {arm: receipt.get("libm_sha256") for arm, receipt in pair.items()},
    }


def compare_pair(pair, reference, initializer, run_id):
    arms, errors = {}, {}
    for arm in ARMS:
        receipt = pair.get(arm)
        if receipt is None:
            errors[arm] = "Receipt absent"
            continue
        rhs = receipt.get("first_rhs")
        observed = rhs.get("effective_inputs_v141") if isinstance(rhs, dict) else None
        if not isinstance(observed, dict):
            errors[arm] = "Effective-input readback absent or malformed"
            continue
        if (receipt.get("arm"), receipt.get("run_id"), receipt.get("caller"),
                rhs.get("rhs_caller"), observed.get("site"), observed.get("schema")) != (
                arm, run_id, "main", "evolver_ndf15", SITE, SCHEMA):
            errors[arm] = "Process, call site or schema identity differs"
            continue
        if type(receipt.get("pid")) is not int or receipt["pid"] <= 0:
            errors[arm] = "Invalid process ID"
            continue

        checks = {}

        def check(name, expected, actual):
            row = {"expected": expected, "observed": actual}
            if actual is None:
                row["status"] = "UNAVAILABLE"
            elif type(expected) is int:
                row["status"] = ("INVALID" if type(actual) is not int else
                                 "MATCH" if actual == expected else "MISMATCH")
            else:
                row["expected_bits"] = bits(expected)
                try:
                    row["observed_bits"] = bits(actual)
                    row["status"] = "MATCH" if row["expected_bits"] == row["observed_bits"] else "MISMATCH"
                except (ValueError, OverflowError):
                    row["status"] = "INVALID"
            checks[name] = row

        expected_scalar, scalar = reference["scalar"], observed.get("scalar") or {}
        expected_nu, nu = reference["neutrino"], observed.get("neutrino") or {}
        initial = receipt.get("initial") or {}
        if not all(isinstance(group, dict) for group in (scalar, nu, initial)):
            errors[arm] = "Malformed scalar, neutrino or initializer fields"
            continue
        for name in SCALARS:
            check(name, expected_scalar[name], scalar.get(name))
        for name in NU_FIELDS:
            check(name, expected_nu[name], nu.get(name))
        for name in VECTORS:
            vector = nu.get(name)
            usable = vector if isinstance(vector, list) else []
            check(f"{name}.length", len(expected_nu[name]), len(usable) if isinstance(vector, list) else None)
            for index, expected in enumerate(expected_nu[name]):
                check(f"{name}[{index}]", expected, usable[index] if index < len(usable) else None)
        for name, expected in initializer.items():
            check(f"initial.{name}", expected, initial.get(name))
        arms[arm] = {"pid": receipt["pid"], "checks": checks, "read_issues": observed.get("read_issues", [])}

    if len(arms) == 2 and arms["L"]["pid"] == arms["R"]["pid"]:
        errors["pair"] = "Process IDs are identical"
    states = {row["status"] for arm in arms.values() for row in arm["checks"].values()}
    if errors:
        status = "CAPTURE_INCOMPLETE"
    elif "MISMATCH" in states:
        status = "CAPTURED_DISCREPANCY"
    elif states != {"MATCH"} or any(arm["read_issues"] for arm in arms.values()):
        status = "CAPTURE_INCOMPLETE"
    else:
        status = "CAPTURED_EXACT_INPUT_MATCH"
    return {
        "schema": "Q052_V141_COMPARISON_V1", "status": status, "run_id": run_id,
        "reference_capture_sha256": CAPTURE, "library_sha256": LIBRARY, "source_commit": SOURCE,
        "arms": arms, "identity_errors": errors,
    }


def once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Qualified parent anchor differs: {old!r}")
    return source.replace(old, new, 1)


def extend(kit, archive, diagnostics):
    checked(archive.read_bytes(), BASE_ARCHIVE, "V136 archive")
    original = kit / "observe.py"
    driver = kit / "launch.py"
    library = kit / "evidence/libq052_class_v36.so"
    checked(library.read_bytes(), LIBRARY, "CLASS binary")
    observer = checked(original.read_bytes(), OBSERVER, "V136 GDB observer").decode()
    launcher = checked(driver.read_bytes(), LAUNCHER, "V136 launcher").decode()
    reference, initializer = load_reference(kit)
    controls = self_check(reference, initializer)

    observer = once(observer, "class Probe(gdb.Breakpoint):",
                    inspect.getsource(capture_effective_inputs) + "\n\nclass Probe(gdb.Breakpoint):")
    observer = once(observer,
                    "                if int(field(pba,'N_ncdm')) != 1:\n"
                    "                    raise ValueError('Expected one neutrino species in the frozen input')\n",
                    "                species_count = int(field(pba,'N_ncdm'))\n")
    observer = once(observer, "caller='main', ncdm_species=1,",
                    "caller='main', ncdm_species=species_count,")
    observer = once(observer, "!=6 or not samples:",
                    " != 6 or int(params) == 0 or (species_count == 1 and not samples):")
    observer = once(observer, "ncdm_p_over_rho=samples[-1],",
                    "ncdm_p_over_rho=samples[-1] if samples else None,")
    observer = once(observer, "            elif phase == 2:\n",
                    "            elif phase == 2:\n"
                    "                frame = gdb.newest_frame()\n"
                    "                caller = frame.older()\n"
                    "                if (frame.name() != 'background_derivs' or not caller\n"
                    "                        or caller.name() != 'evolver_ndf15' or not final_call()):\n"
                    "                    raise ValueError('Unexpected frame at first RHS readback')\n")
    observer = once(observer, "                phase=3\n",
                    "                record['first_rhs']['rhs_caller'] = caller.name()\n"
                    "                record['first_rhs']['effective_inputs_v141'] = capture_effective_inputs(pba, field, hx)\n"
                    "                phase=3\n")

    launcher = once(launcher, "from readback import check_pair", "from q052_v141 import check_v141_startup")
    launcher = once(launcher, "result=check_pair(probes)", "result=check_v141_startup(probes)")
    for name, source in (("observe.py", observer), ("launch.py", launcher)):
        compile(source, name, "exec")
    original.write_bytes(observer.encode())
    driver.write_bytes(launcher.encode())
    extended = {
        "schema": "Q052_V141_PREPARATION_V1",
        "parent_archive_sha256": BASE_ARCHIVE, "library_sha256": LIBRARY,
        "capture_sha256": CAPTURE, "source_commit": SOURCE, "site": SITE,
        "observer_source_sha256": digest(original.read_bytes()),
        "launcher_source_sha256": digest(driver.read_bytes()),
        "extension_source_sha256": digest(Path(__file__).read_bytes()),
        "controls": controls,
    }
    diagnostics.parent.mkdir(parents=True, exist_ok=True)
    diagnostics.write_text(json.dumps(extended, indent=2) + "\n")


def self_check(reference, initializer):
    run_id = "SYNTHETIC-Q052-V141"
    pair = {
        arm: {"arm": arm, "run_id": run_id, "pid": 101 + index, "caller": "main",
              "initial": dict(initializer), "first_rhs": {
                  "rhs_caller": "evolver_ndf15", "effective_inputs_v141": copy.deepcopy(reference),
              }}
        for index, arm in enumerate(ARMS)
    }

    def require(ok, label):
        if not ok:
            raise ValueError(f"Synthetic control failed: {label}")

    def convert(field, value):
        return value + 1 if field in ("species_count", "node_count") else math.nextafter(
            float.fromhex(value), math.inf).hex()

    def assess(samples):
        return compare_pair(samples, reference, initializer, run_id)

    require(assess(pair)["status"] == "CAPTURED_EXACT_INPUT_MATCH", "exact match")
    controls = []
    for arm in ARMS:
        for group, fields in (("scalar", SCALARS), ("neutrino", NU_FIELDS)):
            for name in fields:
                altered = copy.deepcopy(pair)
                values = altered[arm]["first_rhs"]["effective_inputs_v141"][group]
                values[name] = convert(name, values[name])
                result = assess(altered)
                check = result["arms"][arm]["checks"][name]
                require(result["status"] == "CAPTURED_DISCREPANCY" and check["status"] == "MISMATCH", (arm, name))
                controls.append((arm, name))
        for vector in VECTORS:
            for index in range(11):
                altered = copy.deepcopy(pair)
                entries = altered[arm]["first_rhs"]["effective_inputs_v141"]["neutrino"][vector]
                entries[index] = convert(vector, entries[index])
                result = assess(altered)
                name = f"{vector}[{index}]"
                check = result["arms"][arm]["checks"][name]
                require(result["status"] == "CAPTURED_DISCREPANCY" and check["status"] == "MISMATCH", (arm, name))
                require(check.get("observed_bits") != check["expected_bits"], (arm, name, "bits"))
                controls.append((arm, name))
    altered = copy.deepcopy(pair)
    altered["R"]["first_rhs"]["effective_inputs_v141"]["neutrino"]["q"].reverse()
    require(assess(altered)["arms"]["R"]["checks"]["q[0]"]["status"] == "MISMATCH", "vector order")
    altered = copy.deepcopy(pair)
    altered["R"]["first_rhs"]["effective_inputs_v141"]["neutrino"]["w"].pop()
    require(assess(altered)["arms"]["R"]["checks"]["w.length"]["status"] == "MISMATCH", "vector length")
    altered = copy.deepcopy(pair)
    altered["R"]["first_rhs"]["effective_inputs_v141"]["scalar"]["B"] = "nan"
    require(assess(altered)["status"] == "CAPTURE_INCOMPLETE", "invalid numeric text")
    altered = copy.deepcopy(pair)
    altered["R"]["first_rhs"]["effective_inputs_v141"]["scalar"]["B"] = None
    require(assess(altered)["status"] == "CAPTURE_INCOMPLETE", "missing numeric field")
    altered = copy.deepcopy(pair)
    altered["R"]["pid"] = altered["L"]["pid"]
    require(assess(altered)["status"] == "CAPTURE_INCOMPLETE", "duplicate PID")
    altered = copy.deepcopy(pair)
    altered["R"]["run_id"] += "-WRONG"
    require(assess(altered)["status"] == "CAPTURE_INCOMPLETE", "wrong run ID")
    altered = copy.deepcopy(pair)
    altered["R"]["first_rhs"]["rhs_caller"] = "input_init"
    require(assess(altered)["status"] == "CAPTURE_INCOMPLETE", "wrong caller")
    require(assess({"L": pair["L"]})["status"] == "CAPTURE_INCOMPLETE", "missing arm")
    require(bits("0x0p+0") != bits("-0x0p+0"), "signed zero")
    require(bits("0x1p+0") == bits("0x1.0000000000000p+0"), "equivalent hex encoding")

    class Pointer:
        def __init__(self, values=None):
            self.values = values

        def __int__(self):
            return int(self.values is not None)

        def __getitem__(self, index):
            if self.values is None:
                raise ValueError("Unexpected null pointer dereference")
            return self.values[index]

    nu = reference["neutrino"]
    values = {
        "scf_parameters_size": 6, "scf_parameters": Pointer([reference["scalar"][n] for n in SCALARS]),
        "N_ncdm": nu["species_count"], "q_size_ncdm_bg": Pointer([nu["node_count"]]),
        "M_ncdm": Pointer([nu["M"]]), "factor_ncdm": Pointer([nu["factor"]]),
        "q_ncdm_bg": Pointer([Pointer(nu["q"])]), "w_ncdm_bg": Pointer([Pointer(nu["w"])]),
    }

    def read(values):
        return capture_effective_inputs(values, dict.__getitem__, lambda v: v)

    require(read(values) == reference, "capture field and array mapping")
    for bad in (0, -1, 65):
        actual = read(dict(values, q_size_ncdm_bg=Pointer([bad]), q_ncdm_bg=Pointer([]), w_ncdm_bg=Pointer([])))
        require(actual["neutrino"]["node_count"] == bad and actual["neutrino"]["q"] is None, ("bounds", bad))
    actual = read(dict(values, q_size_ncdm_bg=Pointer([12]),
                       q_ncdm_bg=Pointer([Pointer(nu["q"] + [nu["q"][-1]])]),
                       w_ncdm_bg=Pointer([Pointer(nu["w"] + [nu["w"][-1]])])))
    require(actual["neutrino"]["node_count"] == 12 and len(actual["neutrino"]["q"]) == 12, "unexpected safe shape")
    actual = read(dict(values, N_ncdm=0, M_ncdm=Pointer([]), q_size_ncdm_bg=Pointer([])))
    require(actual["neutrino"]["M"] is None and actual["neutrino"]["species_count"] == 0, "zero species")
    for member, field, ptr in (("q_ncdm_bg", "q", Pointer()), ("w_ncdm_bg", "w", Pointer([Pointer()])),
                               ("M_ncdm", "M", Pointer()), ("factor_ncdm", "factor", Pointer()),
                               ("q_size_ncdm_bg", "node_count", Pointer())):
        actual = read(dict(values, **{member: ptr}))
        require(actual["neutrino"][field] is None and actual["read_issues"], ("null guard", member))
    actual = read(dict(values, scf_parameters=Pointer()))
    require(actual["scalar"]["m"] is None and actual["read_issues"], "null scalar pointer")
    actual = read(dict(values, scf_parameters_size=3, scf_parameters=Pointer([])))
    require(actual["scalar"]["m"] is None and actual["read_issues"], "short scalar array")
    return {"status": "PASS", "single_field_mutations": len(controls),
            "other_comparison_controls": 11, "capture_controls": 13,
            "native_processes": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("kit", type=Path)
    prepare.add_argument("archive", type=Path)
    prepare.add_argument("diagnostics", type=Path)
    compare = sub.add_parser("compare")
    for name in ("kit", "measured", "output"):
        compare.add_argument(name, type=Path)
    compare.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if args.mode == "prepare":
        extend(args.kit, args.archive, args.diagnostics)
        return 0

    reference, initializer = load_reference(args.kit)
    pair, file_errors = {}, {}
    for arm in ARMS:
        receipt = args.measured / arm / "scalar_start_receipt.json"
        try:
            data = json.loads(receipt.read_bytes())
            if not isinstance(data, dict):
                raise ValueError("Receipt must be an object")
            pair[arm] = data
        except (OSError, ValueError) as error:
            file_errors[arm] = str(error)
    result = compare_pair(pair, reference, initializer, args.run_id)
    result["receipt_file_errors"] = file_errors
    run_result = args.measured / "result.json"
    result["startup_replay_gate"] = "NOT_AVAILABLE"
    if run_result.is_file():
        summary = json.loads(run_result.read_bytes())
        result["nominal_export_overlap_v69"] = summary["overlap"]
        result["v136_startup_replay"] = summary["arms"]
        result["libm_sha256"] = summary["libm_sha256"]
        replay_ok = summary["run_id"] == args.run_id and all(
            "initializer_residual" in summary["arms"].get(arm, {}) for arm in ARMS
        )
        result["startup_replay_gate"] = "PASS" if replay_ok else "UNVALIDATED"
    if result["status"] == "CAPTURED_EXACT_INPUT_MATCH" and result["startup_replay_gate"] != "PASS":
        result["status"] = "CAPTURE_INCOMPLETE"
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(result["status"])
    return 2 if result["status"] == "CAPTURE_INCOMPLETE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
