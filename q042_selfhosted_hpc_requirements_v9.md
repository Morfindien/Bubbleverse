# Q042-PROD-V9 — self-hosted HPC runner requirement

V8 proved that the frozen Q042 `nprior=10nlive` cannot reach its first resumable
PolyChord checkpoint on the standard 4-CPU GitHub-hosted runner.

V9 therefore routes only the expensive PolyChord jobs to a dedicated runner label:

`q042-hpc`

## Required runner capacity

- Ubuntu Linux x64
- at least 16 logical CPUs
- at least 24 GiB RAM
- enough free disk for the Bubbleverse runtime (50+ GiB recommended)
- internet access to GitHub
- `sudo` access
- OpenMPI is installed/reasserted by the workflow
- the runner is used ephemerally for this campaign

V9 uses exactly 16 MPI ranks and forces one computational thread per rank.

The frozen Q42 sampler settings remain unchanged:
- `nlive = 25d`
- `nprior = 10nlive`
- `num_repeats = 5d`
- same seeds
- 240-minute soft segments
- 330-minute job timeout

## Why 16 ranks

V8 measured the worst-case `hillipop / ede_n3 / FULL` initialization:

- nDims = 26
- nlive = 650
- nprior = 6500
- 951 accepted initial prior/live points in 315 minutes on one worker

V9 uses that measured throughput in a capacity gate before it spends hours on the
canary. With 16 MPI ranks PolyChord has 15 worker ranks.

## Security: public repository

Bubbleverse is a public repository. GitHub warns that permanent self-hosted runners
on public repositories can be exposed to untrusted workflow code.

Use a disposable/ephemeral VM or otherwise isolated machine. Do not run this on a
machine containing credentials or private data you care about.

Register the runner specifically for this repository and give it the custom label:

`q042-hpc`

Prefer making it a temporary runner and removing it when Q042 is finished.

GitHub UI path:

Repository -> Settings -> Actions -> Runners -> New self-hosted runner

Follow GitHub's generated install commands for Linux x64. During configuration,
assign the custom label `q042-hpc`.

After the runner shows `Idle`, install/commit the V9 files and launch:

`Q042-PROD-V9`

If the runner has fewer than 16 logical CPUs or less than 24 GiB RAM, V9 fails
immediately before the PolyChord canary.
