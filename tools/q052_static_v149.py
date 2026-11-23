"""Recheck the four machine-code observation sites and pinned interpolation kernel."""
import argparse
from hashlib import sha256
from pathlib import Path
from subprocess import run
import json
import re

LIB='8b90e21505337cb6696c4f6460616c7c92482f6c8eba7f3450d7da5cb040fae3'
NDF='49d26ddf369c08baea9cb297825f52a734df52e568687ed1f0be12ac68417856'
SITES={
    'accepted_after_dif_update': ('evolver_ndf15','1ade2','44 3b a4 24 e8 13 00 00','cmp'),
    'dense_call': ('evolver_ndf15','1aee9','e8 62 56 ff ff','interp_from_dif@plt'),
    'background_sources_entry': ('background_sources','67f20','f3 0f 1e fa','endbr64'),
    'background_row_written': ('background_sources','67fc3','89 c3','mov'),
}
ANCHORS={
 'evolver_ndf15':{
  '18a7a':'$0x3a8,%rsp','18a81':'0x13e0(%rsp)','18aa6':'0x178(%rsp)',
  '18ad9':'%r8,0x58(%rsp)','18bf3':'%rax,%rdi','18bfa':'%rdi,0xa8(%rsp)',
  '1951d':'%xmm5,0xc0(%rsp)','19732':'0xc0(%rsp),%xmm6','1973b':'%xmm6,0x40(%rsp)',
  '19894':'0xc0(%rsp),%xmm6','1989d':'%xmm6,0xb8(%rsp)',
  '19bb6':'-0x8(%r15,%rax,8)','19f3c':'%xmm1,%xmm5',
  '19f40':'0x98(%rsp),%xmm5','19f49':'1a805','1a810':'(%rsp),%r13d',
  '1a81c':'0x198(%rsp),%r15','1a8e8':'1ade2','1ae4f':'call   *%rax',
  '1ae51':'cmp','1ae93':'0x40(%rsp),%xmm0','1ae9b':'1ae33',
  '1aeab':'0x150(%rsp)','1aeb2':'0x98(%rsp),%rsi','1aeba':'0x120(%rsp),%rdi',
  '1aeca':'0x60(%rsp),%xmm1','1aee0':'0xd8(%rsp),%xmm2',
  '1af22':'call   *%rax','1af24':'cmp',
 },
 'background_sources':{
  '67f26':'%rdi,%r13','67f2d':'%edx,%rbx','67f37':'(%rcx),%rbp',
  '67f5f':'(%rdx,%rax,8),%r12','67fbe':'background_functions@plt'
 },
 'interp_from_dif':{'15af6':'%xmm1,%xmm0','15b08':'%xmm2,%xmm0','15c35':'mulsd',
                    '15c43':'addsd','15c50':'addsd','15c55':'movsd'}
}


def instructions(path,symbol):
    asm=run(['objdump','-d',f'--disassemble={symbol}',str(path)],capture_output=True,text=True,check=True).stdout
    result={}
    for line in asm.splitlines():
        match=re.match(r'^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)[\t ]+(.*)$',line)
        if match: result[match[1]]=(match[2].strip(),match[3])
    return result


def audit(root,binary):
    hashes={'library':sha256(binary.read_bytes()).hexdigest(),
            'evolver_source':sha256((root/'tools/evolver_ndf15.c').read_bytes()).hexdigest()}
    assert hashes=={'library':LIB,'evolver_source':NDF}
    all_instructions={name:instructions(binary,name) for name in ANCHORS}
    decoded={}
    for name,(symbol,addr,code,mnemonic) in SITES.items():
        incoming,inst=all_instructions[symbol][addr]
        # objdump may wrap the eighth byte to a continuation line.
        assert code.startswith(incoming) and len(incoming.split())>=min(7,len(code.split())) and mnemonic in inst
        decoded[name]={'symbol':symbol,'offset_hex':addr,'expected_opcode':code,'disassembly':inst}
    for name,anchors in ANCHORS.items():
        for addr,needle in anchors.items():
            assert needle in all_instructions[name][addr][1],(name,addr,needle)
    dwarf=run(['readelf','--debug-dump=loc',str(binary)],capture_output=True,text=True,check=True).stdout
    assert re.search(r'000000000001ade2 000000000001b016 \(DW_OP_fbreg: -4896\)',dwarf)
    assert re.search(r'000000000001ade2 000000000001b5f4 \(DW_OP_fbreg: -4920\)',dwarf)
    assert re.search(r'000000000001ade2 000000000001ae33 \(DW_OP_reg22 \(xmm5\)\)',dwarf)
    return {'schema':'Q052_V149_STATIC_ADDRESS_AUDIT','status':'PASS',
      'hashes':hashes,'sites':decoded,'matched_instructions':sum(map(len,ANCHORS.values())),
      'dwarf_confirmations':{'t':'CFA-4896','y':'CFA-4920','err':'xmm5 at accept'},
      'native_pair_executed':False}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('class_source','binary','output'): p.add_argument(n,type=Path)
    args=p.parse_args()
    args.output.write_text(json.dumps(audit(args.class_source,args.binary),indent=2)+'\n')
