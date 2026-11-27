#!/usr/bin/env python3
"""Advisory host preflight and actual-index Git hooks; not a shell security boundary."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

SECRET = re.compile(rb'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|"private_key"\s*:|xox[baprs]-[0-9A-Za-z-]{10,}|gh[pousr]_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{40,}|sk_live_[0-9A-Za-z]{20,}|sk-[A-Za-z0-9_-]{32,}')
MAX_BLOB = 10 * 1024 * 1024


def safe_path(raw):
    # Paths themselves may hold personal data or secrets; use an opaque reference.
    return 'path-' + hashlib.sha256(raw).hexdigest()[:12]


def git(cwd, args):
    result = subprocess.run(['git', '-C', str(cwd), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=15)
    if result.returncode:
        raise ValueError('repository operation failed; inspect locally without exposing credentials')
    return result.stdout


def command_targets(command, cwd):
    """Recognize a small safe subset; reject ambiguous commit commands instead of guessing."""
    if len(command) > 65536:
        raise ValueError('command too large')
    if not re.search(r'\bcommit\b', command):
        return []
    if any(mark in command for mark in ('$(', '`', '\n', '|', ';', '>', '<', '(', ')')):
        raise ValueError('ambiguous commit command; stage separately and run a direct git commit')
    lex = shlex.shlex(command, posix=True, punctuation_chars='&')
    lex.whitespace_split = True
    tokens = list(lex)
    groups = [[]]
    for token in tokens:
        if token == '&&': groups.append([])
        elif token == '&': raise ValueError('background commit command unsupported')
        else: groups[-1].append(token)
    result = []
    current = Path(cwd)
    for group in groups:
        if not group: raise ValueError('empty command in chain')
        if group[0] == 'cd' and len(group) == 2:
            current = (current / group[1]).resolve()
            continue
        allow = False
        while group and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', group[0]):
            assignment = group.pop(0)
            if assignment == 'GUARDRAILS_ALLOW_MAIN_COMMIT=1': allow = True
            elif assignment.startswith(('GIT_', 'PATH=')):
                raise ValueError('environment changes repository resolution; use direct git commit')
        if not group or group[0] not in ('git', '/usr/bin/git'):
            # Do not interpret a string printed by echo as an environment assignment.
            if group and group[0] == 'echo': continue
            raise ValueError('unsupported command before commit; stage and commit separately')
        i = 1
        target = current
        while i < len(group) and group[i].startswith('-'):
            flag = group[i]
            if flag in ('-C', '-c') and i + 1 < len(group):
                if flag == '-C': target = (target / group[i+1]).resolve()
                # Configuration values are not executed by this scanner.
                i += 2
            elif flag.startswith('-c') and len(flag) > 2: i += 1
            else: raise ValueError('unsupported global git option; use direct git commit')
        if i == len(group) or group[i] != 'commit':
            raise ValueError('stage and commit separately so the actual index can be checked')
        options = group[i+1:]
        j = 0
        while j < len(options):
            option = options[j]
            if option in ('-m', '--message', '-F', '--file', '-C', '--reuse-message', '-c', '--reedit-message'):
                if j + 1 >= len(options): raise ValueError('missing commit option value')
                j += 2
            elif option.startswith(('--message=', '--file=', '--reuse-message=', '--reedit-message=')) or (option.startswith('-m') and len(option) > 2):
                j += 1
            elif option in ('--amend', '--no-edit', '--allow-empty', '--allow-empty-message', '--no-verify', '-n', '--signoff', '-s', '--gpg-sign', '-S', '--no-gpg-sign', '--quiet', '-q', '--verbose', '-v'):
                j += 1
            else:
                raise ValueError('unsupported commit option or path; stage explicitly and use a direct commit')
        result.append((target, allow))
    return result


def scan_index(cwd):
    entries = git(cwd, ['ls-files', '--stage', '-z']).split(b'\0')
    seen = set()
    for entry in entries:
        if not entry: continue
        metadata, path = entry.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        if stage != b'0': raise ValueError('unmerged index; resolve it before committing')
        if mode == b'160000': continue
        if oid in seen: continue
        seen.add(oid)
        size = int(git(cwd, ['cat-file', '-s', oid.decode('ascii')]))
        if size > MAX_BLOB:
            raise ValueError('staged blob exceeds scan limit; use a scanner supporting this artifact')
        content = git(cwd, ['cat-file', 'blob', oid.decode('ascii')])
        if SECRET.search(content):
            raise ValueError('possible secret in staged ' + safe_path(path) + '; value withheld')


def branch_check(cwd, allow):
    if allow or os.environ.get('GUARDRAILS_ALLOW_MAIN_COMMIT') == '1': return
    branch = git(cwd, ['branch', '--show-current']).decode().strip()
    defaults = {'main', 'master'}
    try:
        remote = git(cwd, ['symbolic-ref', '--short', 'refs/remotes/origin/HEAD']).decode().strip()
        defaults.add(remote.removeprefix('origin/'))
    except ValueError: pass
    if not branch: raise ValueError('detached HEAD: explicitly select a work branch')
    if branch in defaults: raise ValueError('direct default-branch commit blocked; use a work branch')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('check', choices=['secrets','branch'])
    ap.add_argument('--git-hook', action='store_true')
    args = ap.parse_args(argv)
    try:
        if args.git_hook:
            targets = [(Path.cwd(), False)]
        else:
            raw = sys.stdin.read(131073)
            if len(raw) > 131072: raise ValueError('oversized hook input')
            try: data = json.loads(raw)
            except (ValueError, TypeError): raise ValueError('invalid hook input')
            if not isinstance(data, dict): raise ValueError('invalid hook input')
            tool = data.get('tool_input')
            if not isinstance(tool, dict) or not isinstance(tool.get('command'), str):
                raise ValueError('missing command in hook input')
            cwd = data.get('cwd', os.getcwd())
            if not isinstance(cwd, str): raise ValueError('invalid working directory')
            targets = command_targets(tool['command'], cwd)
        for cwd, allow in targets:
            if args.check == 'secrets': scan_index(cwd)
            else: branch_check(cwd, allow)
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        # Only our safe messages are emitted; OS errors can contain sensitive paths.
        message = str(error) if type(error) is ValueError else 'check could not complete'
        print('Blocked: ' + message, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
