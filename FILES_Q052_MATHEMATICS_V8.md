# Q052 Matematik V8 — individuelle filer

Q052 er åben. Ny matematisk delcertificering og præcis diagnostic-kontrakt; ingen ny native integration eller GitHub-write.

- [Q052_MATHEMATICS_RESULT_AND_HANDOFF_V8.md](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_MATHEMATICS_RESULT_AND_HANDOFF_V8.md) — primary mathematical answer and proof.
- [Q052_VALIDATED_NUMERICS_CONTRACT_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_VALIDATED_NUMERICS_CONTRACT_V8.json) — new finite diagnostic/validated-error specification.
- [Q052_SAMLET_JOURNAL_V8.md](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_SAMLET_JOURNAL_V8.md) — same logical journal, exact V7 prefix plus append.
- [Q052_QUESTION_ACTIVITY_LEDGER_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_QUESTION_ACTIVITY_LEDGER_V8.json) — cumulative activity ledger,220 new points once.
- [Q052_SERIALIZED_INTERPOLANT_CERTIFICATE_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_SERIALIZED_INTERPOLANT_CERTIFICATE_V8.json) — executed exact whole-cell interpolant bounds.
- [Q052_SEPARATE_ARITHMETIC_CHECK_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_SEPARATE_ARITHMETIC_CHECK_V8.json) — executed separate stationary-root/integral check.
- [Q052_MATHEMATICS_INPUT_BUNDLE_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_MATHEMATICS_INPUT_BUNDLE_V8.json) — verbatim histories/source text/worker receipts for replay.
- [Q052_SOURCE_AND_CLAIM_REGISTER_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_SOURCE_AND_CLAIM_REGISTER_V8.json) — source identities, scope and claim evidence.
- [q052_certify_interpolants_v8.py](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/q052_certify_interpolants_v8.py) — exact rational postprocessor, no native integration.
- [q052_check_interpolants_v8.py](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/q052_check_interpolants_v8.py) — separate arithmetical control, no producer import.
- [test_q052_interpolant_v8.py](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/test_q052_interpolant_v8.py) — six analytically solved method checks.
- [Q052_MATHEMATICS_HANDOFF_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_MATHEMATICS_HANDOFF_V8.json) — structured handoff and GitHub memory update.
- [Q052_DELIVERY_VALIDATION_V8.json](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/Q052_DELIVERY_VALIDATION_V8.json) — actual delivery/contract checks.
- [FILES_Q052_MATHEMATICS_V8.md](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/FILES_Q052_MATHEMATICS_V8.md) — individual links and reproduction instructions.
- [SHA256SUMS_Q052_MATHEMATICS_V8.txt](sandbox:/workspace/scratch/0feff3e57b36/Q052_MATHEMATICS_V8/SHA256SUMS_Q052_MATHEMATICS_V8.txt) — nonrecursive final file hashes.

Originale uændrede CSV-filer, også indlejret byteidentisk i inputbundlen:

- [Q052_L-nominal_history_40350424272.csv](sandbox:/workspace/scratch/0feff3e57b36/Q052_SUCCESS_INGESTION_V7/Q052_L-nominal_history_40350424272.csv)
- [Q052_L-refined_history_40350424272.csv](sandbox:/workspace/scratch/0feff3e57b36/Q052_SUCCESS_INGESTION_V7/Q052_L-refined_history_40350424272.csv)
- [Q052_R-nominal_history_40350424272.csv](sandbox:/workspace/scratch/0feff3e57b36/Q052_SUCCESS_INGESTION_V7/Q052_R-nominal_history_40350424272.csv)
- [Q052_R-refined_history_40350424272.csv](sandbox:/workspace/scratch/0feff3e57b36/Q052_SUCCESS_INGESTION_V7/Q052_R-refined_history_40350424272.csv)

Reproduktion fra én inputbundle:

```bash
python3 q052_certify_interpolants_v8.py --input-bundle Q052_MATHEMATICS_INPUT_BUNDLE_V8.json --output audit.json
python3 -m unittest discover -s . -p "test_q052_interpolant_v8.py" -v
```

Separat checker med de fire CSV-filer i samme mappe:

```bash
python3 q052_check_interpolants_v8.py --input-dir . --certificate Q052_SERIALIZED_INTERPOLANT_CERTIFICATE_V8.json --output separate-check.json
```

1310 kumulative point; næste milepæl2000. M001 allerede leveret; ingen ny SoMe-pakke forfalden. Alle nye repo-destinationer er foreslåede rodfiler; ingen upload påstås.
