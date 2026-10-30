#!/usr/bin/env python3
"""Add a read-only full background-table dump to the pinned V3 C wrapper."""
import argparse, hashlib, zipfile
from pathlib import Path

ZIP_SHA="066a6e9eba624ebaae6f29134b798e5311c684af7013a9b43606ee614beb5a8e"
SOURCE_SHA="8196889a18d5dbe8f72eb3bc02e0ce61ef73f725e8852f2484c11ad5fcf16168"
MEMBER="q052_validated_diag/L-nominal/q052_validated_diag_v3.c"
ANCHOR="  if(background_init(&pr,&ba))die(ba.error_message);\n  if(thermodynamics_init(&pr,&ba,&th))die(th.error_message);"
FUNCTION=r'''
/* Additive capture only: exact binary64 values, complete interpolation arrays. */
static void q052_dump_background(struct background *b){
  if(b->bt_size<2||b->bg_size<3||b->bg_size_normal>b->bg_size||
     !b->loga_table||!b->tau_table||!b->z_table||
     !b->background_table||!b->d2background_dloga2_table)
    die("BACKGROUND_TABLE_UNAVAILABLE");
  FILE *f=open_out("background_table_hex.jsonl","wx");
  fprintf(f,"{\"schema\":\"Q052_FULL_BACKGROUND_TABLE_V30\",\"run_id\":");
  js(f,run_id);
  fprintf(f,",\"arm\":");js(f,arm);
  fprintf(f,",\"mode\":");js(f,mode);
  fprintf(f,",\"bt_size\":%d,\"bg_size\":%d,\"bg_size_normal\":%d,",b->bt_size,b->bg_size,b->bg_size_normal);
  fprintf(f,"\"index_bg_a\":%d,\"index_bg_H\":%d,\"index_bg_H_prime\":%d}\n",
          b->index_bg_a,b->index_bg_H,b->index_bg_H_prime);
  for(int i=0;i<b->bt_size;i++){
    fprintf(f,"{\"i\":%d,\"loga\":",i);jhex(f,b->loga_table[i]);
    fprintf(f,",\"tau\":");jhex(f,b->tau_table[i]);
    fprintf(f,",\"z\":");jhex(f,b->z_table[i]);
    fprintf(f,",\"background\":[");
    for(int k=0;k<b->bg_size;k++){
      if(k)fputc(',',f);jhex(f,b->background_table[(size_t)i*b->bg_size+k]);
    }
    fprintf(f,"],\"d2background_dloga2\":[");
    for(int k=0;k<b->bg_size;k++){
      if(k)fputc(',',f);jhex(f,b->d2background_dloga2_table[(size_t)i*b->bg_size+k]);
    }
    fputs("]}\n",f);
  }
  close_ok(f);
}
'''

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--archive',default='recovered_v23/v14/raw/L.zip')
 p.add_argument('--source',help='Pinned generated V3 C source in a checkout')
 p.add_argument('--output',default='q052_v30/q052_validated_diag_background_dump_v30.c')
 a=p.parse_args()
 if a.source:
  raw=Path(a.source).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:raise SystemExit('SOURCE_PIN_MISMATCH')
  src=raw.decode()
 else:
  raw=Path(a.archive).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=ZIP_SHA:raise SystemExit('ARCHIVE_PIN_MISMATCH')
  with zipfile.ZipFile(a.archive) as z: src=z.read(MEMBER).decode()
 if src.count(ANCHOR)!=1 or src.count('static void jhex(')!=1 or src.count('int main(')!=1:
  raise SystemExit('SOURCE_ANCHOR_MISMATCH')
 src=src.replace('int main(int argc,char **argv){',FUNCTION+'\nint main(int argc,char **argv){',1)
 src=src.replace(ANCHOR,'  if(background_init(&pr,&ba))die(ba.error_message);\n  q052_dump_background(&ba);\n  if(thermodynamics_init(&pr,&ba,&th))die(th.error_message);',1)
 o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(src)
 print(o,hashlib.sha256(o.read_bytes()).hexdigest())

if __name__=='__main__':main()
