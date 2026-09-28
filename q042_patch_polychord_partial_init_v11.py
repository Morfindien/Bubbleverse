#!/usr/bin/env python3
"""Q042 V10 local PolyChordLite 1.22.2 patch.

Adds SERIAL-ONLY partial checkpoint/resume inside GenerateLivePoints.
It does not change nlive, nprior, priors, likelihoods, seeds, or nested-sampling
termination settings. The patch is anchored to exact upstream source text and
fails closed if the pinned source layout is not what was reviewed.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

BASE_COMMIT = "3ade6445bb3719a6db6f6e81f178765545ffc833"
CHECKPOINT_INTERVAL = 25
MARKER = "Q042_PARTIAL_INIT_V10"

HELPERS = r"""
    ! Q042_PARTIAL_INIT_V10
    ! Technical execution patch: serial-only partial checkpointing while the
    ! initial nprior live/prior population is still being generated.
    ! The checkpoint stores the complete accepted live-point vectors plus the
    ! Fortran RNG state and local generation counters.
    function q042_partial_init_file(settings,temp) result(file_name)
        use settings_module, only: program_settings
        use utils_module, only: STR_LENGTH
        implicit none
        type(program_settings), intent(in) :: settings
        logical, intent(in) :: temp
        character(len=STR_LENGTH) :: file_name
        if(temp) then
            file_name = trim(settings%base_dir)//'/'//trim(settings%file_root)//'.partial_init.tmp'
        else
            file_name = trim(settings%base_dir)//'/'//trim(settings%file_root)//'.partial_init'
        end if
    end function q042_partial_init_file

    function q042_partial_init_meta_file(settings,temp) result(file_name)
        use settings_module, only: program_settings
        use utils_module, only: STR_LENGTH
        implicit none
        type(program_settings), intent(in) :: settings
        logical, intent(in) :: temp
        character(len=STR_LENGTH) :: file_name
        if(temp) then
            file_name = trim(settings%base_dir)//'/'//trim(settings%file_root)//'.partial_init.meta.tmp'
        else
            file_name = trim(settings%base_dir)//'/'//trim(settings%file_root)//'.partial_init.meta'
        end if
    end function q042_partial_init_meta_file

    subroutine q042_write_partial_init(settings,RTI,nprior,nlike,ndiscarded,ngenerated,total_time)
        use settings_module, only: program_settings
        use run_time_module, only: run_time_info
        implicit none
        type(program_settings), intent(in) :: settings
        type(run_time_info), intent(in) :: RTI
        integer, intent(in) :: nprior,nlike,ndiscarded,ngenerated
        real(dp), intent(in) :: total_time
        integer, parameter :: magic=10421010, version=1
        integer :: u,mu,i,seed_size
        integer, allocatable :: seed(:)
        character(len=1000) :: tmp,final,mtmp,mfinal

        call random_seed(size=seed_size)
        allocate(seed(seed_size))
        call random_seed(get=seed)

        tmp=q042_partial_init_file(settings,.true.)
        final=q042_partial_init_file(settings,.false.)
        open(newunit=u,file=trim(tmp),form='unformatted',access='stream',status='replace',action='write')
        write(u) magic,version
        write(u) settings%nDims,settings%nDerived,settings%nTotal,nprior
        write(u) RTI%nlive(1),nlike,ndiscarded,ngenerated
        write(u) total_time
        write(u) seed_size
        write(u) seed
        do i=1,RTI%nlive(1)
            write(u) RTI%live(:,i,1)
        end do
        close(u)
        call rename(trim(tmp),trim(final))

        mtmp=q042_partial_init_meta_file(settings,.true.)
        mfinal=q042_partial_init_meta_file(settings,.false.)
        open(newunit=mu,file=trim(mtmp),status='replace',action='write')
        write(mu,'(A,I0)') 'version=',version
        write(mu,'(A,I0)') 'nDims=',settings%nDims
        write(mu,'(A,I0)') 'nprior=',nprior
        write(mu,'(A,I0)') 'accepted=',RTI%nlive(1)
        write(mu,'(A,I0)') 'nlike=',nlike
        write(mu,'(A,I0)') 'ndiscarded=',ndiscarded
        write(mu,'(A,I0)') 'ngenerated=',ngenerated
        write(mu,'(A,I0)') 'rng_seed_size=',seed_size
        write(mu,'(A,I0)') 'checkpoint_interval=',25
        close(mu)
        call rename(trim(mtmp),trim(mfinal))
        deallocate(seed)
    end subroutine q042_write_partial_init

    subroutine q042_read_partial_init(settings,RTI,nprior,nlike,ndiscarded,ngenerated,total_time,found)
        use settings_module, only: program_settings
        use run_time_module, only: run_time_info
        use array_module, only: add_point
        use abort_module, only: halt_program
        implicit none
        type(program_settings), intent(in) :: settings
        type(run_time_info), intent(inout) :: RTI
        integer, intent(in) :: nprior
        integer, intent(inout) :: nlike,ndiscarded,ngenerated
        real(dp), intent(inout) :: total_time
        logical, intent(out) :: found
        integer, parameter :: magic_expected=10421010, version_expected=1
        integer :: u,i,magic,version,ndims,nderived,ntotal,file_nprior
        integer :: naccepted,file_nlike,file_ndiscarded,file_ngenerated
        integer :: seed_size,current_seed_size
        integer, allocatable :: seed(:)
        real(dp) :: file_total_time
        real(dp), allocatable :: point(:)
        character(len=1000) :: final

        final=q042_partial_init_file(settings,.false.)
        inquire(file=trim(final),exist=found)
        if(.not.found) return

        open(newunit=u,file=trim(final),form='unformatted',access='stream',status='old',action='read')
        read(u) magic,version
        read(u) ndims,nderived,ntotal,file_nprior
        read(u) naccepted,file_nlike,file_ndiscarded,file_ngenerated
        read(u) file_total_time
        read(u) seed_size

        if(magic/=magic_expected .or. version/=version_expected) then
            call halt_program('Q042 partial-init checkpoint magic/version mismatch')
        end if
        if(ndims/=settings%nDims .or. nderived/=settings%nDerived .or. ntotal/=settings%nTotal) then
            call halt_program('Q042 partial-init checkpoint dimension mismatch')
        end if
        if(file_nprior/=nprior .or. naccepted<0 .or. naccepted>nprior) then
            call halt_program('Q042 partial-init checkpoint nprior/count mismatch')
        end if

        call random_seed(size=current_seed_size)
        if(seed_size/=current_seed_size) then
            call halt_program('Q042 partial-init RNG state size mismatch')
        end if
        allocate(seed(seed_size))
        read(u) seed
        allocate(point(settings%nTotal))
        do i=1,naccepted
            read(u) point
            call add_point(point,RTI%live,RTI%nlive,1)
        end do
        close(u)

        call random_seed(put=seed)
        nlike=file_nlike
        ndiscarded=file_ndiscarded
        ngenerated=file_ngenerated
        total_time=file_total_time
        deallocate(seed,point)
    end subroutine q042_read_partial_init

    subroutine q042_delete_partial_init(settings)
        use settings_module, only: program_settings
        implicit none
        type(program_settings), intent(in) :: settings
        integer :: u
        logical :: exists
        character(len=1000) :: f

        f=q042_partial_init_file(settings,.false.)
        inquire(file=trim(f),exist=exists)
        if(exists) then
            open(newunit=u,file=trim(f),status='old')
            close(u,status='delete')
        end if
        f=q042_partial_init_meta_file(settings,.false.)
        inquire(file=trim(f),exist=exists)
        if(exists) then
            open(newunit=u,file=trim(f),status='old')
            close(u,status='delete')
        end if
    end subroutine q042_delete_partial_init
"""

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def replace_once(text: str, old: str, new: str, label: str) -> str:
    n=text.count(old)
    if n != 1:
        raise SystemExit(f"{label}=FAIL expected_one_anchor got={n}")
    return text.replace(old,new,1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default="external/PolyChordLite")
    ap.add_argument("--manifest",required=True)
    a=ap.parse_args()
    root=Path(a.root)
    got=subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()
    if got != BASE_COMMIT:
        raise SystemExit(f"POLYCHORD_BASE_COMMIT_GATE=FAIL got={got}")

    gen=root/"src/polychord/generate.F90"
    nested=root/"src/polychord/nested_sampling.F90"
    gt=gen.read_text()
    nt=nested.read_text()

    if MARKER not in gt:
        gt=replace_once(gt,"    contains\n","    contains\n"+HELPERS+"\n",
                        "GENERATE_HELPER_INSERT_GATE")

        gt=replace_once(
            gt,
            "        integer :: nlike ! number of likelihood calls\n        integer :: nprior, ndiscarded\n        integer :: ngenerated ! use to track order points are generated in\n",
            "        integer :: nlike ! number of likelihood calls\n"
            "        integer :: nprior, ndiscarded\n"
            "        integer :: ngenerated ! use to track order points are generated in\n"
            "        integer :: i_saved\n"
            "        logical :: q042_partial_resumed\n",
            "GENERATE_DECLARATION_GATE",
        )

        # Stock code opens the live file before nprior/counters are known.
        gt=replace_once(
            gt,
            "            ! Open the live points file to sequentially add live points\n"
            "            if(settings%write_live) open(write_phys_unit,file=trim(phys_live_file(settings)), action='write')\n\n"
            "            ! Allocate the run time arrays, and set the default values for the variables\n"
            "            call initialise_run_time_info(settings,RTI)\n",
            "            ! Allocate the run time arrays, and set the default values for the variables\n"
            "            call initialise_run_time_info(settings,RTI)\n",
            "GENERATE_EARLY_OPEN_REMOVAL_GATE",
        )

        gt=replace_once(
            gt,
            "        total_time=0\n        if(linear_mode(mpi_information)) then\n",
            "        total_time=0\n"
            "        q042_partial_resumed=.false.\n"
            "        if(linear_mode(mpi_information) .and. is_root(mpi_information)) then\n"
            "            call q042_read_partial_init(settings,RTI,nprior,nlike,ndiscarded,ngenerated,total_time,q042_partial_resumed)\n"
            "        end if\n"
            "        if(is_root(mpi_information) .and. settings%write_live) then\n"
            "            open(write_phys_unit,file=trim(phys_live_file(settings)),action='write',status='replace')\n"
            "            if(q042_partial_resumed) then\n"
            "                do i_saved=1,RTI%nlive(1)\n"
            "                    write(write_phys_unit,fmt_dbl) RTI%live(settings%p0:settings%d1,i_saved,1), &\n"
            "                        RTI%live(settings%l0,i_saved,1)\n"
            "                end do\n"
            "                flush(write_phys_unit)\n"
            "            end if\n"
            "        end if\n"
            "        if(linear_mode(mpi_information)) then\n",
            "GENERATE_PARTIAL_RESTORE_GATE",
        )

        gt=replace_once(
            gt,
            "                        flush(write_phys_unit) ! flush the unit to force write\n"
            "                    end if\n\n"
            "                end if\n\n"
            "            end do\n",
            "                        flush(write_phys_unit) ! flush the unit to force write\n"
            "                    end if\n"
            "                    if(settings%write_resume .and. mod(RTI%nlive(1),25)==0) then\n"
            "                        call q042_write_partial_init(settings,RTI,nprior,nlike,ndiscarded,ngenerated,total_time)\n"
            "                    end if\n\n"
            "                end if\n\n"
            "            end do\n",
            "GENERATE_PERIODIC_CHECKPOINT_GATE",
        )
        gen.write_text(gt)

    if "q042_delete_partial_init_checkpoint_done" not in nt:
        nt=replace_once(
            nt,
            "        use generate_module,    only: GenerateSeed,GenerateLivePoints\n",
            "        use generate_module,    only: GenerateSeed,GenerateLivePoints,q042_delete_partial_init\n",
            "NESTED_IMPORT_GATE",
        )
        nt=replace_once(
            nt,
            "                    call write_resume_file(settings,RTI) \n"
            "                    call rename_files(settings,RTI)\n"
            "                end if\n",
            "                    call write_resume_file(settings,RTI) \n"
            "                    call rename_files(settings,RTI)\n"
            "                    call q042_delete_partial_init(settings) ! q042_delete_partial_init_checkpoint_done\n"
            "                end if\n",
            "NESTED_DELETE_AFTER_STOCK_RESUME_GATE",
        )
        nested.write_text(nt)

    if MARKER not in gen.read_text():
        raise SystemExit("POLYCHORD_PARTIAL_INIT_MARKER_GATE=FAIL")
    if "q042_delete_partial_init_checkpoint_done" not in nested.read_text():
        raise SystemExit("POLYCHORD_PARTIAL_INIT_DELETE_MARKER_GATE=FAIL")

    out={
        "status":"PASS",
        "base_commit":BASE_COMMIT,
        "checkpoint_interval":CHECKPOINT_INTERVAL,
        "serial_only":True,
        "generate_sha256":sha(gen),
        "nested_sampling_sha256":sha(nested),
        "generate_file":str(gen),
        "nested_sampling_file":str(nested),
    }
    Path(a.manifest).parent.mkdir(parents=True,exist_ok=True)
    Path(a.manifest).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("Q042_POLYCHORD_PARTIAL_INIT_SOURCE_PATCH_GATE=PASS")

if __name__=="__main__":
    main()
