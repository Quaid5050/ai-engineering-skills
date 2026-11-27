#!/usr/bin/env python3
"""Regenerate discovery metadata from manifests and SKILL files; never bump versions."""
import json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def render():
    skills=[]
    for path in sorted(ROOT.glob('plugins/*/skills/*/SKILL.md')):
        plugin=path.parents[2].name
        data=yaml.safe_load(path.read_text().split('---',2)[1]);name=data['name']
        requires=[] if plugin=='foundation' else ['work-context','safe-agent-execution']
        if plugin not in ('foundation','quality') or (plugin=='quality' and name!='testing-doctrine'):requires.append('testing-doctrine')
        skills.append({'name':name,'plugin':plugin,'path':path.parent.relative_to(ROOT).as_posix(),
                       'version':data['metadata']['version'],'description':data['description'],
                       'requires':requires,'optional_companions':[],'support':'documented','owner':'maintainers',
                       'resources':[p.relative_to(path.parent).as_posix() for p in sorted(path.parent.rglob('*')) if p.is_file()]})
    return json.dumps({'schema_version':1,'skills':skills},indent=2)+'\n'
if __name__=='__main__':
    (ROOT/'catalog/skills.json').write_text(render())
