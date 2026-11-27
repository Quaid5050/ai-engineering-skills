#!/usr/bin/env python3
"""Owned skill installation with preflight, recoverable transactions and one-step rollback."""
import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = '.ai-engineering-skills.json'
LOCK = '.ai-engineering-skills.lock'
JOURNAL = '.ai-engineering-skills-transaction'
HISTORY = '.ai-engineering-skills-previous'
OWNER = 'ai-engineering-skills/v1'


def atomic_json(path, value):
    # An exclusive temporary file avoids following a pre-existing .tmp symlink.
    fd, name = tempfile.mkstemp(prefix='.skills-state-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)


def safe_name(name):
    return isinstance(name, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) is not None


def exists(path):
    return path.exists() or path.is_symlink()


def digest(path):
    if not exists(path): return None
    h = hashlib.sha256()
    if path.is_symlink():
        h.update(('link:' + os.readlink(path)).encode())
        # Development link ownership tracks identity, not changing source content.
        return h.hexdigest()
    if not path.is_dir(): raise ValueError('skill destination is not a directory')
    for item in sorted(path.rglob('*')):
        rel = item.relative_to(path).as_posix()
        if item.is_symlink(): raise ValueError('nested skill symlinks are not supported')
        if item.is_dir(): h.update(('dir:' + rel + '\0').encode())
        if item.is_file():
            h.update(rel.encode()); h.update(b'\0'); h.update(item.read_bytes()); h.update(b'\0')
        elif not item.is_dir(): raise ValueError('unsupported filesystem entry in skill')
    return h.hexdigest()


def load(path, default=None):
    if not exists(path): return default
    if path.is_symlink(): raise ValueError('metadata must not be a symlink')
    try: value = json.loads(path.read_text())
    except (ValueError, OSError): raise ValueError('unreadable installation metadata')
    if not isinstance(value, dict) or value.get('owner') != OWNER:
        raise ValueError('foreign installation metadata; refusing to replace it')
    return value


def remove_owned(path):
    if path.is_symlink(): path.unlink()
    elif path.is_dir(): shutil.rmtree(path)
    elif exists(path): raise ValueError('unexpected owned object type')


def catalogue(root):
    data = json.loads((root/'catalog/skills.json').read_text())
    items = {item['name']:item for item in data['skills']}
    if len(items) != len(data['skills']): raise ValueError('duplicate skill names')
    return items


def select(items, filters):
    plugins = {item['plugin'] for item in items.values()}
    if filters and set(filters)-plugins: raise ValueError('unknown plugin filter')
    wanted = {name for name,item in items.items() if not filters or item['plugin'] in filters}
    visiting = set(); done = set()
    def visit(name):
        if name in visiting: raise ValueError('required dependency cycle')
        if name not in items: raise ValueError('missing required skill')
        if name in done: return
        visiting.add(name)
        for dep in items[name].get('requires',[]): visit(dep)
        visiting.remove(name); done.add(name)
    for name in sorted(wanted): visit(name)
    return sorted(done)


def acquire(target, recover=False):
    lock = target/LOCK
    if lock.is_symlink(): raise ValueError('lock must not be a symlink')
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    stream = os.fdopen(fd, 'r+', encoding='utf-8')
    try:
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        content = stream.read()
        if content:
            try: info = json.loads(content)
            except ValueError: raise ValueError('invalid lock metadata')
            if not isinstance(info, dict) or info.get('owner') != OWNER:
                raise ValueError('foreign lock metadata')
        stream.seek(0); stream.truncate()
        json.dump({'owner':OWNER,'pid':os.getpid()},stream)
        stream.flush(); os.fsync(fd)
        # Never unlink this inode: the OS releases its lock on process exit.
        return stream
    except OSError:
        stream.close(); raise ValueError('installation locked or filesystem locking unavailable')
    except BaseException:
        stream.close(); raise


def recovery(target, folder):
    if folder.is_symlink() or not folder.is_dir(): raise ValueError('journal must be a local directory')
    for child in ('backup', 'stage'):
        if (folder/child).is_symlink(): raise ValueError('journal directories must not be symlinks')
    plan = load(folder/'plan.json')
    if plan is None: raise ValueError('incomplete journal metadata; inspect without deleting user files')
    operations = plan.get('operations')
    if not isinstance(operations, list) or any(not isinstance(op, dict) or not safe_name(op.get('name')) for op in operations):
        raise ValueError('invalid recovery operations')
    if len({op['name'] for op in operations}) != len(operations): raise ValueError('duplicate recovery operation')
    for op in operations:
        for key in ('before', 'after'):
            value = op.get(key)
            if value is not None and (not isinstance(value, str) or not re.fullmatch('[a-f0-9]{64}', value)):
                raise ValueError('invalid recovery digest')
    if 'old_state' not in plan or 'new_state' not in plan: raise ValueError('incomplete recovery state')
    state = load(target/STATE)
    if state != plan['old_state'] and state != plan['new_state']:
        raise ValueError('installation metadata changed; automatic rollback refused')
    # Preflight every destination before restoring any.
    for op in plan['operations']:
        current = digest(target/op['name'])
        if current not in (op['before'],op['after'],None):
            raise ValueError('installed content changed; automatic rollback refused')
        backup = folder/'backup'/op['name']
        if exists(backup) and digest(backup) != op['before']:
            raise ValueError('backup changed; automatic rollback refused')
        if op['before'] is not None and not exists(backup) and current != op['before']:
            raise ValueError('original content unavailable; automatic rollback refused')
    for op in reversed(plan['operations']):
        dest = target/op['name']; backup = folder/'backup'/op['name']
        if exists(backup):
            if exists(dest): remove_owned(dest)
            os.replace(backup,dest)
        elif op['before'] is None and exists(dest): remove_owned(dest)
    if plan['old_state'] is None:
        if exists(target/STATE): (target/STATE).unlink()
    else: atomic_json(target/STATE,plan['old_state'])
    shutil.rmtree(folder)


def install(target, filters=None, mode='copy', uninstall=False, dry_run=False, recover=False, rollback=False, root=ROOT, fault=None):
    target = Path(target).absolute()
    if target.is_symlink(): raise ValueError('target must not be a symlink')
    target.mkdir(parents=True,exist_ok=True)
    lock_handle = acquire(target,recover=recover)
    try:
        journal=target/JOURNAL; history=target/HISTORY
        if exists(journal):
            if not recover: raise ValueError('interrupted transaction; run --recover before using this installation')
            recovery(target,journal)
        if recover: return 'Recovered interrupted installation; no new install performed.'
        if rollback:
            if not exists(history): raise ValueError('no previous transaction to roll back')
            load(history/'plan.json')
            os.replace(history,journal); recovery(target,journal)
            return 'Rolled back previous transaction.'
        old=load(target/STATE)
        installed=(old or {}).get('skills',{})
        items=catalogue(root); names=select(items,filters)
        if uninstall:
            names=[n for n in names if n in installed and (not filters or items[n]['plugin'] in filters)]
        if not names: raise ValueError('no matching skills')
        updated=dict(installed); operations=[]
        for name in names:
            if not safe_name(name): raise ValueError('unsafe skill name')
            dest=target/name; owned=installed.get(name)
            if exists(dest) and owned is None: raise ValueError('foreign skill collision; nothing changed')
            current=digest(dest) if exists(dest) else None
            if owned is not None and current != owned['digest']: raise ValueError('owned content modified or missing; preserve changes before updating')
            source=(root/items[name]['path']).resolve()
            if not source.is_relative_to(root.resolve()) or not (source/'SKILL.md').is_file(): raise ValueError('unsafe or missing source skill')
            digest(source) # reject nested symlinks before writing
            operations.append({'name':name,'before':current,'after':None,'source':str(source)})
            if uninstall: updated.pop(name,None)
        if uninstall:
            for name in updated:
                if any(dep not in updated for dep in items.get(name,{}).get('requires',[])):
                    raise ValueError('uninstall would remove a required dependency')
        if dry_run: return f'Preflight passed for {len(operations)} skills; no skill content changed.'
        if exists(history):
            load(history/'plan.json')
            if history.is_symlink(): raise ValueError('history must not be a symlink')
            shutil.rmtree(history)
        journal.mkdir();(journal/'stage').mkdir();(journal/'backup').mkdir()
        # Write a valid recovery plan before staging so a failed copy is recoverable.
        plan={'owner':OWNER,'old_state':old,'new_state':old,'operations':operations}
        atomic_json(journal/'plan.json',plan)
        for op in operations:
            if uninstall: continue
            staged=journal/'stage'/op['name']
            if mode=='link': staged.symlink_to(op['source'],target_is_directory=True)
            else: shutil.copytree(op['source'],staged)
            op['after']=digest(staged)
            updated[op['name']]={'digest':op['after'],'plugin':items[op['name']]['plugin'],'mode':mode}
        plan['new_state']={'owner':OWNER,'skills':updated}
        atomic_json(journal/'plan.json',plan)
        for number,op in enumerate(operations):
            dest=target/op['name']
            if exists(dest): os.replace(dest,journal/'backup'/op['name'])
            if fault: fault('backup',number)
            if not uninstall: os.replace(journal/'stage'/op['name'],dest)
            if fault: fault('install',number)
        atomic_json(target/STATE,plan['new_state'])
        if fault: fault('manifest',0)
        os.replace(journal,history)
        return f'{"Removed" if uninstall else "Installed"} {len(operations)} owned skills; previous transaction can be rolled back.'
    finally:
        lock_handle.close()


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('target');ap.add_argument('--plugins')
    ap.add_argument('--link',action='store_true');ap.add_argument('--uninstall',action='store_true')
    ap.add_argument('--dry-run',action='store_true');ap.add_argument('--recover',action='store_true');ap.add_argument('--rollback',action='store_true')
    a=ap.parse_args()
    if sum((a.uninstall,a.recover,a.rollback))>1: ap.error('choose one operation')
    try: print(install(a.target,a.plugins.split(',') if a.plugins else None,'link' if a.link else 'copy',a.uninstall,a.dry_run,a.recover,a.rollback))
    except (ValueError,OSError,KeyError) as error:
        print('Installation failed: '+(str(error) if type(error) is ValueError else 'invalid metadata or filesystem operation; no foreign content is intentionally replaced'),file=sys.stderr);return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
