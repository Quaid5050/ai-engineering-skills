#!/usr/bin/env python3
"""Build a deterministic source bundle plus a SHA-256 manifest; does not publish."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
ROOT=Path(__file__).resolve().parents[1]
def build(destination,root=ROOT):
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    members=[]
    for name in ('plugins','catalog','schemas','scripts','docs','examples','tests','.claude-plugin','.github'):
        members.extend(p for p in (root/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    members.extend(root/name for name in ('README.md','LICENSE','requirements-dev.txt','AGENTS.md','CONTRIBUTING.md','CHANGELOG.md'))
    payload=io.BytesIO()
    with tarfile.open(fileobj=payload,mode='w',format=tarfile.PAX_FORMAT) as archive:
        for path in sorted(members):
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('bundle source escaped root')
            data=path.read_bytes();info=tarfile.TarInfo(path.relative_to(root).as_posix())
            info.size=len(data);info.mode=0o755 if path.stat().st_mode&0o111 else 0o644;info.mtime=0
            archive.addfile(info,io.BytesIO(data))
    with destination.open('wb') as output:
        with gzip.GzipFile(filename='',mode='wb',fileobj=output,mtime=0) as compressed:compressed.write(payload.getvalue())
    manifest={'artifact':destination.name,'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'files':len(members),'format_version':1}
    destination.with_suffix(destination.suffix+'.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('destination');args=parser.parse_args()
    print(json.dumps(build(args.destination)))
