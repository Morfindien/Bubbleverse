#!/usr/bin/env python3
"""Complete serial stock-loop checkpoint; statistical update cadence untouched.

A single binary is atomically renamed after a whole loop iteration. It stores
all pinned run_time_info components, RNG, nlikesum and failure counter. Legacy
stock state cannot restore historical RNG or pending posterior stack; importing
it requires an explicit DIAGNOSTIC-only branch, never production authorization.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess
from pathlib import Path
BASE_COMMIT='3ade6445bb3719a6db6f6e81f178765545ffc833'
TYPE_BLOB='a2a3dec74de9aa0cf1a1e97aab2bb58205742eb9'
MARKER='Q042_DURABLE_V22'
NESTED_HASHES={'850ab9aaabfd0c2747177fcca619baab322409a407e673bfcbc51fb3905a16bf',
               '87a007b72d4088714a4bcedd2eae9f86cd9d2b9c6264cb12bed5cfe7a65968ab'}

def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def replace_once(text,old,new,label):
    if text.count(old)!=1:raise ValueError(label+'=FAIL source anchor mismatch')
    return text.replace(old,new,1)
def fields(source):
    section=source.split('    type run_time_info',1)[1].split('    end type run_time_info',1)[0]
    items=[]
    for line in section.splitlines():
        m=re.match(r'\s*(integer|real\(dp\))\s*(.*?)::\s*(\w+)',line,re.I)
        if m:
            kind,attrs,name=m.groups();dim=re.search(r'dimension\(([^)]+)\)',attrs,re.I)
            rank=dim.group(1).count(',')+1 if dim else 0
            items.append((name,'i' if kind.lower()=='integer' else 'r',rank))
    if len(items)!=44:raise ValueError('RTI_SCHEMA_GATE=FAIL unexpected field count '+str(len(items)))
    return items

def array_helpers():
    parts=[]
    for kind,decl in [('i','integer'),('r','real(dp)')]:
        for rank in [1,2,3]:
            dims=','.join([':']*rank);extents=','.join(f'dims({i})' for i in range(1,rank+1))
            parts.append(f'''
    subroutine q042_put_{kind}{rank}(u,a)
        implicit none
        integer,intent(in) :: u
        {decl},allocatable,intent(in) :: a({dims})
        logical :: present_array
        present_array=allocated(a)
        write(u) present_array
        if(present_array) then
            write(u) shape(a)
            if(size(a)>0) write(u) a
        end if
    end subroutine
    subroutine q042_get_{kind}{rank}(u,a)
        use iso_fortran_env, only: int64
        implicit none
        integer,intent(in) :: u
        {decl},allocatable,intent(inout) :: a({dims})
        logical :: present_array
        integer :: dims({rank})
        read(u) present_array
        if(allocated(a)) deallocate(a)
        if(present_array) then
            read(u) dims
            if(any(dims<0) .or. any(dims>100000000)) error stop 'Q042 durable array dimensions invalid'
            if(product(int(dims,int64))>500000000_int64) error stop 'Q042 durable array too large'
            allocate(a({extents}))
            if(size(a)>0) read(u) a
        end if
    end subroutine
''')
    return '\n'.join(parts)

def helpers(schema):
    put=[];get=[]
    for name,kind,rank in schema:
        if rank:
            put.append(f'        call q042_put_{kind}{rank}(u,RTI%{name})')
            get.append(f'        call q042_get_{kind}{rank}(u,RTI%{name})')
        else:
            put.append(f'        write(u) RTI%{name}')
            get.append(f'        read(u) RTI%{name}')
    return r'''
    ! Q042_DURABLE_V22 — serialization only, after complete serial iteration.
    function q042_durable_context() result(context)
        implicit none
        character(64) :: context
        integer :: length,status
        context=''
        call get_environment_variable('Q042_DURABLE_CONTEXT',context,length=length,status=status)
        if(status==1) return
        if(status/=0 .or. length/=64 .or. verify(context,'0123456789abcdef')/=0) &
            error stop 'Q042 durable context must be exact lowercase SHA256'
    end function
    function q042_durable_path(settings,temp) result(path)
        use settings_module, only: program_settings
        implicit none
        type(program_settings),intent(in) :: settings
        logical,intent(in) :: temp
        character(1000) :: path
        path=trim(settings%base_dir)//'/'//trim(settings%file_root)//'.durable_v22'
        if(temp) path=trim(path)//'.tmp'
    end function
    subroutine q042_legacy_gate()
        implicit none
        character(64) :: context
        character(32) :: policy
        integer :: status
        context=q042_durable_context()
        if(context=='') return
        policy=''
        call get_environment_variable('Q042_DURABLE_LEGACY',policy,status=status)
        if(status/=0 .or. trim(policy)/='DIAGNOSTIC') &
            error stop 'Q042 legacy resume lacks full state; diagnostic import must be explicit'
        write(*,*) 'Q042_LEGACY_DIAGNOSTIC_ONLY historical RNG and stack are unknown'
        flush(6)
    end subroutine
    subroutine q042_durable_write(settings,RTI,nlikesum,failures)
        use settings_module, only: program_settings
        use run_time_module, only: run_time_info
        implicit none
        type(program_settings),intent(in) :: settings
        type(run_time_info),intent(in) :: RTI
        integer,intent(in) :: nlikesum(:),failures
        integer :: u,seed_size,status
        integer,allocatable :: seed(:)
        character(64) :: context
        character(1000) :: temp,final
        context=q042_durable_context()
        if(context=='') return
        call random_seed(size=seed_size)
        allocate(seed(seed_size))
        call random_seed(get=seed)
        temp=q042_durable_path(settings,.true.)
        final=q042_durable_path(settings,.false.)
        open(newunit=u,file=trim(temp),access='stream',form='unformatted',status='replace',action='write')
        write(u) 10422222,1,settings%nDims,settings%nDerived,settings%nTotal,RTI%ndead, &
                 RTI%ncluster,size(settings%grade_dims),failures,sum(RTI%nlike),seed_size
        write(u) context
        write(u) nlikesum
        write(u) seed
'''+'\n'.join(put)+r'''
        write(u) 10422223
        flush(u)
        close(u)
        call rename(trim(temp),trim(final),status)
        if(status/=0) error stop 'Q042 atomic durable rename failed'
        write(*,*) 'Q042_DURABLE_COMMIT',RTI%ndead
        flush(6)
    end subroutine
    subroutine q042_durable_read(settings,RTI,nlikesum,failures,found)
        use settings_module, only: program_settings
        use run_time_module, only: run_time_info
        implicit none
        type(program_settings),intent(in) :: settings
        type(run_time_info),intent(inout) :: RTI
        integer,intent(inout) :: nlikesum(:),failures
        logical,intent(out) :: found
        integer :: u,head(11),seed_size,footer,status
        integer,allocatable :: seed(:)
        character(64) :: context,file_context
        character(1000) :: path
        found=.false.
        context=q042_durable_context()
        if(context=='' .or. .not.settings%read_resume) return
        path=q042_durable_path(settings,.false.)
        inquire(file=trim(path),exist=found)
        if(.not.found) return
        open(newunit=u,file=trim(path),access='stream',form='unformatted',status='old',action='read')
        read(u) head
        if(head(1)/=10422222 .or. head(2)/=1) error stop 'Q042 durable magic/version mismatch'
        if(any(head(3:5)/=[settings%nDims,settings%nDerived,settings%nTotal])) &
            error stop 'Q042 durable dimensions mismatch'
        if(head(8)/=size(nlikesum)) error stop 'Q042 durable grades mismatch'
        call random_seed(size=seed_size)
        if(head(11)/=seed_size) error stop 'Q042 durable RNG ABI mismatch'
        read(u) file_context
        if(file_context/=context) error stop 'Q042 durable context mismatch'
        read(u) nlikesum
        allocate(seed(seed_size))
        read(u) seed
'''+'\n'.join(get)+r'''
        read(u) footer
        if(footer/=10422223) error stop 'Q042 durable incomplete footer'
        read(u,iostat=status) footer
        if(status>=0) error stop 'Q042 durable unexpected trailing data'
        close(u)
        if(RTI%ndead/=head(6) .or. RTI%ncluster/=head(7) .or. sum(RTI%nlike)/=head(10)) &
            error stop 'Q042 durable header/state mismatch'
        failures=head(9)
        call random_seed(put=seed)
        write(*,*) 'Q042_DURABLE_RESTORE',RTI%ndead
        flush(6)
    end subroutine
'''+array_helpers()

def patch_text(text,type_source):
    schema=fields(type_source)
    if MARKER in text:raise ValueError('ALREADY_PATCHED_GATE=FAIL use preserved baseline source')
    text=replace_once(text,'        logical :: update\n','        logical :: update\n        logical :: q042_full_restored\n','LOCAL_STATE')
    text=replace_once(text,'        ! Check if we actually want to resume\n',
        "        ! Complete serial state takes precedence over lossy stock state.\n"
        "        if(q042_durable_context()/='') then\n"
        "            if(.not.linear_mode(mpi_information)) error stop 'Q042 durable checkpoint is serial only'\n"
        "        end if\n"
        "        call q042_durable_read(settings,RTI,nlikesum,failures,q042_full_restored)\n"
        "        ! Check if we actually want to resume\n",'RESTORE_BOUNDARY')
    text=replace_once(text,'        if ( settings%read_resume .and. resume_file_exists(settings) ) then',
        "        if(q042_full_restored) then\n            call write_resuming(settings%feedback)\n"
        "        else if ( settings%read_resume .and. resume_file_exists(settings) ) then",'RESTORE_CHOICE')
    text=replace_once(text,'                call read_resume_file(settings,RTI)',
        '                call q042_legacy_gate()\n                call read_resume_file(settings,RTI)','LEGACY_GATE')
    text=replace_once(text,'            do while ( more_samples_needed(settings,RTI) .and. failures <= nfail )',
        '            call q042_durable_write(settings,RTI,nlikesum,failures)\n'
        '            do while ( more_samples_needed(settings,RTI) .and. failures <= nfail )','INITIAL_SAFE_BOUNDARY')
    text=replace_once(text,'            end do ! End of main loop body',
        '                call q042_durable_write(settings,RTI,nlikesum,failures)\n'
        '            end do ! End of main loop body','ITERATION_SAFE_BOUNDARY')
    text=replace_once(text,'end module nested_sampling_module',helpers(schema)+'\nend module nested_sampling_module','HELPERS')
    return text,schema

def apply(root,manifest,fixture=False):
    root=Path(root);ns=root/'src/polychord/nested_sampling.F90';ts=root/'src/polychord/run_time_info.f90'
    if blob(ts.read_bytes())!=TYPE_BLOB:raise ValueError('PINNED_RTI_BLOB_GATE=FAIL')
    if not fixture:
        if subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()!=BASE_COMMIT:raise ValueError('PINNED_COMMIT_GATE=FAIL')
    before=ns.read_bytes()
    if hashlib.sha256(before).hexdigest() not in NESTED_HASHES:raise ValueError('PINNED_NESTED_SOURCE_GATE=FAIL')
    patched,schema=patch_text(before.decode(),ts.read_text());ns.write_text(patched)
    report={'q':'Q-042','program_id':'Q042-DURABLE-V22','status':'SOURCE_PATCHED','base_commit':BASE_COMMIT,'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(ns.read_bytes()).hexdigest(),'rti_type_blob':TYPE_BLOB,'rti_fields':[x[0] for x in schema],'serial_only':True,'changes':['Complete binary state publication after original whole iteration','Fortran RNG, nlikesum and failures restore before next iteration'],'compression_factor_changed':False,'covariance_or_clustering_cadence_changed':False,'legacy_historical_rng_reconstructed':False,'scientific_result':False,'production_restart_authorized':False}
    Path(manifest).parent.mkdir(parents=True,exist_ok=True);Path(manifest).write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--manifest',required=True)
    a=ap.parse_args();print(json.dumps(apply(a.root,a.manifest),indent=2))
