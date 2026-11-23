"""Extend the authenticated V141 launcher at its two-probe transition."""
from pathlib import Path
from hashlib import sha256
import argparse
import shutil

KNOWN_V141_DRIVER='644ac1637f20d652e31ca973b8678e172e342af2c4424639ffecdf6f5fb4deaa'


def integrate(parent, here):
    driver=parent/'launch.py'
    raw=driver.read_bytes()
    if sha256(raw).hexdigest()!=KNOWN_V141_DRIVER:
        raise ValueError('Wrong prepared V141 launcher')
    source=raw.decode()
    anchor="             '-ex','continue','--args' ,str(wrapper),str(ini)]"
    if source.count(anchor)!=1:
        raise ValueError('Wrong launcher hook anchor')
    transition=(
        "             '-ex', 'python exec(compile(open('+repr(str(HERE/'q052_steps_v149.py'))+').read(), \"q052_steps_v149.py\", \"exec\"))',\n"
        "             '-ex','continue','--args' ,str(wrapper),str(ini)]"
    )
    modified=source.replace(anchor,transition)
    compile(modified,'launch.py','exec')
    shutil.copyfile(here/'q052_steps_v149.py',parent/'q052_steps_v149.py')
    driver.write_text(modified,encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture_kit',type=Path)
    a=p.parse_args()
    integrate(a.capture_kit,Path(__file__).resolve().parent)
