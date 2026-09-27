# Q042-PROD-V9 — self-hosted MPI capacity repair

V8 successfully prevented 19-cell fanout, but its worst-case real canary proved
that the standard GitHub-hosted runner is too small for the frozen Q42 `nprior`.

V9 does not lower nprior and does not alter science.

It moves only heavy PolyChord jobs to an ephemeral self-hosted runner labeled
`q042-hpc`, requires >=16 logical CPUs and >=24 GiB RAM, then runs the already
MPI-enabled PolyChordLite runtime with exactly 16 MPI ranks and one thread per rank.

Static/environment/V1 BOBYQA import/collector remain GitHub-hosted.

The worst-case EDE/FULL canary still runs first. The other 19 cells are released
only if:
1. runner capacity gate passes,
2. MPI smoke gate passes,
3. canary completes or creates a valid checkpoint inside the frozen 240-minute segment,
4. a separate-process resume probe succeeds.

The V1 reduced HiLLiPoP matrix continues to be reused byte-for-byte.
All 80 V1 BOBYQA records remain reused with zero recomputation.

Read `q042_selfhosted_hpc_requirements_v9.md` before launching.

START THIS:
Q042-PROD-V9
