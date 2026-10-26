"""Recover exact historical CLASS bytes; never compile or execute the core."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile

import q052_native_pair_v2 as controller

HERE = Path(__file__).resolve().parent


def recover(destination, archive=None):
    contract = controller.read(HERE / controller.CONTRACT)
    frozen = contract['environment_recovery']
    expected = contract['class_binary_sha256']
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / 'classy.so'
    preserved = HERE / frozen['preserved_binary_name']
    receipt = {'q': 'Q052', 'program_id': controller.ID,
               'source_commit': contract['source_commit'],
               'binary_sha256': expected, 'core_rebuilt': False,
               'native_executed': False,
               'origin_run_id': frozen['origin_run_id'],
               'origin_artifact_id': frozen['origin_artifact_id']}
    if archive is None and preserved.is_file():
        controller.need(controller.sha(preserved) == expected, 'PRESERVED_ORIGINAL_BINARY_HASH')
        shutil.copyfile(preserved, target)
        receipt['recovery_method'] = 'PRESERVED_EXACT_BINARY_OBJECT'
    else:
        if archive is None:
            archive = destination / 'original_objects.zip'
            with archive.open('wb') as output, (destination / 'download.log').open('w') as log:
                cp = subprocess.run(['gh', 'api', '--method', 'GET',
                    'repos/Morfindien/Bubbleverse/actions/artifacts/'
                    + str(frozen['origin_artifact_id']) + '/zip'],
                    stdout=output, stderr=log, timeout=240)
            controller.need(cp.returncode == 0, 'ORIGINAL_OBJECT_DOWNLOAD_FAILED')
        archive = Path(archive)
        controller.need(controller.sha(archive) == frozen['archive_sha256'],
                        'ORIGINAL_OBJECT_ARCHIVE_HASH')
        with zipfile.ZipFile(archive) as bundle:
            members = bundle.infolist()
            controller.need(len(members) <= 256 and
                            len({m.filename for m in members}) == len(members), 'ARCHIVE_MEMBER_IDENTITY')
            controller.need(sum(m.file_size for m in members) <= 512 * 1024**2, 'ARCHIVE_EXPANSION_CAP')
            member = frozen['archive_member']
            # A fixed member is read, never an archive-supplied path extracted.
            original = bundle.read(member)
            controller.need(hashlib.sha256(original).hexdigest() == expected,
                            'RECOVERED_ORIGINAL_BINARY_HASH')
            target.write_bytes(original)
        receipt.update(recovery_method='PINNED_Q047_ARTIFACT',
                       archive_sha256=frozen['archive_sha256'], member=member)
    controller.need(controller.sha(target) == expected, 'FINAL_ORIGINAL_BINARY_HASH')
    receipt['status'] = 'ORIGINAL_BINARY_RECOVERED_NOT_EXECUTED'
    controller.write(destination / 'recovery_receipt.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--archive')
    args = parser.parse_args()
    try:
        print(json.dumps(recover(args.out, args.archive), indent=2))
        return 0
    except Exception as error:
        failure = controller.persist_failure(Path(args.out) / 'failure.json',
                    f'{type(error).__name__}: {error}', 'RECOVER_ORIGINAL_BINARY')
        print(json.dumps(failure, indent=2))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
