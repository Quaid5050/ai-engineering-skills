#!/usr/bin/env python3
"""Advisory pre-commit checks for agent hosts and Git hooks; not a shell security boundary.

`secrets` scans the lines a commit would add for credential patterns.
`branch` blocks a commit on the default branch (main, master or origin/HEAD).

As a host PreToolUse hook it reads {"tool_input": {"command": ...}, "cwd": ...}
on stdin and acts only when a command segment really runs `git commit`.
Exit 2 with a message on stderr blocks; exit 0 allows.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

SECRET = re.compile(rb'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|"private_key"\s*:|xox[baprs]-[0-9A-Za-z-]{10,}|gh[pousr]_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{40,}|sk_live_[0-9A-Za-z]{20,}|sk-[A-Za-z0-9_-]{32,}')
MAX_COMMAND = 65536
MAX_FINDINGS = 10
# Total git time per check; hooks.json allows 30s (secrets) and 10s (branch).
SECRETS_BUDGET = 25
BRANCH_BUDGET = 8
DEADLINE = [None]  # monotonic time by which every git call must finish


class Unsafe(ValueError):
    """A command that may commit but cannot be analysed; block it."""


# --------------------------------------------------------------------------- shell lexer

class Word:
    __slots__ = ('text', 'dynamic', 'quoted', 'subs')

    def __init__(self):
        self.text = ''
        self.dynamic = False   # holds $var, ${..}, $(..) or `..`
        self.quoted = False
        self.subs = []         # token lists of command substitutions


class Op:
    __slots__ = ('op',)

    def __init__(self, op):
        self.op = op


class HereDoc:
    __slots__ = ('lines',)

    def __init__(self):
        self.lines = []


OPERATORS = ('&>>', '<<<', '<<-', '&&', '||', ';;', '|&', '>>', '<<', '>&', '<&', '&>', '<>', '>|',
             ';', '|', '&', '<', '>', '(', ')', '\n')
NAME_START = re.compile(r'[A-Za-z_]')


def lex(s, i=0, end=None, depth=0):
    """Tokenize shell text into Words, Ops and HereDocs. `end` is ')' or '`' inside a substitution."""
    if depth > 16:
        raise Unsafe('command nests substitutions too deeply to analyse')
    toks, pending = [], []
    word = None
    expect_delim = None
    paren = 0
    n = len(s)

    def flush():
        nonlocal word, expect_delim
        if word is None:
            return
        toks.append(word)
        if expect_delim is not None:
            body = HereDoc()
            toks.append(body)
            pending.append((word.text, expect_delim, body))
            expect_delim = None
        word = None

    while i < n:
        c = s[i]
        if c == '\\':
            if i + 1 < n and s[i + 1] == '\n':
                i += 2
                continue
            word = word or Word()
            word.text += s[i + 1] if i + 1 < n else ''
            word.quoted = True
            i += 2
            continue
        if c in ' \t':
            flush()
            i += 1
            continue
        if c == '#' and word is None:
            while i < n and s[i] != '\n':
                i += 1
            continue
        if c == "'":
            word = word or Word()
            j = s.find("'", i + 1)
            if j < 0:
                raise Unsafe('unterminated quote')
            word.text += s[i + 1:j]
            word.quoted = True
            i = j + 1
            continue
        if c == '"':
            word = word or Word()
            word.quoted = True
            i = lex_double(s, i + 1, word, depth)
            continue
        if c == '$':
            word = word or Word()
            i = lex_dollar(s, i, word, depth)
            continue
        if c == '`':
            if end == '`':
                flush()
                return toks, i + 1
            word = word or Word()
            inner, i = lex(s, i + 1, '`', depth + 1)
            word.subs.append(inner)
            word.dynamic = True
            continue
        op = next((o for o in OPERATORS if s.startswith(o, i)), None)
        if op is None:
            word = word or Word()
            word.text += c
            i += 1
            continue
        if op[0] in '<>' and word is not None and word.text.isdigit() and not (word.quoted or word.dynamic):
            word = None  # file-descriptor prefix such as 2>
        flush()
        if op == ')':
            if paren == 0 and end == ')':
                return toks, i + 1
            paren = max(paren - 1, 0)
        elif op == '(':
            paren += 1
        toks.append(Op(op))
        i += len(op)
        if op in ('<<', '<<-'):
            expect_delim = op == '<<-'
        elif op == '\n' and pending:
            i = read_heredocs(s, i, pending)
    flush()
    if end is not None:
        raise Unsafe('unterminated command substitution')
    return toks, i


def read_heredocs(s, i, pending):
    n = len(s)
    for delim, strip, body in pending:
        while i < n:
            nl = s.find('\n', i)
            line = s[i:] if nl < 0 else s[i:nl]
            i = n if nl < 0 else nl + 1
            if (line.lstrip('\t') if strip else line) == delim:
                break
            body.lines.append(line)
    pending.clear()
    return i


def lex_double(s, i, word, depth):
    n = len(s)
    while i < n:
        c = s[i]
        if c == '"':
            return i + 1
        if c == '\\' and i + 1 < n and s[i + 1] in '$`"\\\n':
            if s[i + 1] != '\n':
                word.text += s[i + 1]
            i += 2
        elif c == '$':
            i = lex_dollar(s, i, word, depth)
        elif c == '`':
            inner, i = lex(s, i + 1, '`', depth + 1)
            word.subs.append(inner)
            word.dynamic = True
        else:
            word.text += c
            i += 1
    raise Unsafe('unterminated quote')


def skip_balanced(s, i, open_c, close_c):
    level, n = 0, len(s)
    while i < n:
        if s[i] == '\\':
            i += 2
            continue
        if s[i] == open_c:
            level += 1
        elif s[i] == close_c:
            level -= 1
            if level == 0:
                return i + 1
        i += 1
    raise Unsafe('unterminated expansion')


def lex_dollar(s, i, word, depth):
    nxt = s[i + 1] if i + 1 < len(s) else ''
    if nxt == '(' and s.startswith('((', i + 1):
        word.dynamic = True
        return skip_balanced(s, i + 1, '(', ')')
    if nxt == '(':
        inner, j = lex(s, i + 2, ')', depth + 1)
        word.subs.append(inner)
        word.dynamic = True
        return j
    if nxt == '{':
        word.dynamic = True
        return skip_balanced(s, i + 1, '{', '}')
    if nxt == "'":
        j = i + 2
        while j < len(s) and s[j] != "'":
            j += 2 if s[j] == '\\' else 1
        if j >= len(s):
            raise Unsafe('unterminated quote')
        try:
            word.text += s[i + 2:j].encode('latin-1', 'backslashreplace').decode('unicode_escape')
        except (UnicodeError, ValueError):
            word.text += s[i + 2:j]
        word.quoted = True
        return j + 1
    if nxt == '"':
        word.quoted = True
        return lex_double(s, i + 2, word, depth)
    if nxt and (NAME_START.match(nxt) or nxt.isdigit() or nxt in '@*#?$!-'):
        j = i + 2
        if NAME_START.match(nxt):
            while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                j += 1
        word.text += s[i:j]
        word.dynamic = True
        return j
    word.text += '$'
    return i + 1


# --------------------------------------------------------------------------- command analysis

SEPARATORS = {'&&', '||', ';', ';;', '|', '|&', '&', '\n', '(', ')'}
OUTPUT_REDIRECTS = {'>', '>>', '&>', '&>>', '>|', '<>', '>&'}
HARMLESS_TARGETS = {'/dev/null', '/dev/stdout', '/dev/stderr', '/dev/tty', '-'}
KEYWORDS = {'!', '{', '}', 'if', 'then', 'else', 'elif', 'do', 'while', 'until', 'time', 'command',
            'exec', 'nohup', 'builtin'}
# Commands that run their arguments (or stdin) as shell code.
SHELLS = {'eval', 'sh', 'bash', 'zsh', 'dash', 'ksh', 'fish', 'source', '.'}
RUNNERS = {'sudo', 'doas', 'su', 'xargs', 'env', 'nice', 'timeout', 'watch', 'parallel', 'find', 'ssh', 'script'}
INTERPRETERS = {'python', 'python3', 'perl', 'ruby', 'node', 'awk', 'gawk', 'nawk', 'mawk'}
# Commands that write files; content they write before `git add` in the same command is not on disk yet.
FILE_WRITERS = {'cp', 'mv', 'tee', 'install', 'ln', 'rsync', 'dd', 'tar', 'unzip', 'curl', 'wget', 'patch'}
IN_PLACE_EDITORS = {'sed', 'gsed', 'perl'}
GIT_FILE_WRITERS = {'apply', 'stash', 'restore', 'pull', 'merge', 'cherry-pick', 'revert', 'am', 'rebase'}
BRANCH_OPS = {'merge', 'cherry-pick', 'am', 'rebase', 'revert'}
GIT_RISKY_TEXT = re.compile(r'\bgit\b[\s\S]*\b(?:commit|merge|rebase|cherry-pick|revert)\b')
ASSIGNMENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*=')
GIT_VALUE_GLOBALS = {'-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path', '--super-prefix',
                     '--config-env', '--list-cmds', '--attr-source'}
GIT_REDIRECTING = ('--git-dir', '--work-tree', '--exec-path', '--namespace', '--config-env')
GIT_BOOL_GLOBALS = {'-p', '--paginate', '-P', '--no-pager', '--no-replace-objects', '--literal-pathspecs',
                    '--glob-pathspecs', '--noglob-pathspecs', '--icase-pathspecs', '--no-optional-locks',
                    '--bare', '--no-lazy-fetch', '--no-advice'}
# Git never lets an alias shadow a built-in command, so these need no alias lookup.
GIT_BUILTINS = set('''add am annotate apply archive bisect blame branch bundle cat-file check-attr check-ignore
check-mailmap check-ref-format checkout checkout-index cherry cherry-pick citool clean clone column commit
commit-graph commit-tree config count-objects credential describe diff diff-files diff-index diff-tree difftool
fast-export fast-import fetch fetch-pack filter-branch for-each-ref for-each-repo format-patch fsck gc
get-tar-commit-id grep gui hash-object help init instaweb interpret-trailers log ls-files ls-remote ls-tree
maintenance merge merge-base merge-file merge-tree mergetool mktag mktree mv name-rev notes pack-objects
prune pull push range-diff read-tree rebase reflog remote repack replace request-pull rerere reset restore
rev-list rev-parse revert rm send-email shortlog show show-branch show-ref sparse-checkout stash status
stripspace submodule switch symbolic-ref tag update-index update-ref var verify-commit verify-pack
verify-tag version whatchanged worktree write-tree'''.split())
COMMIT_VALUE_SHORT = set('mFCct')
COMMIT_VALUE_LONG = {'--message', '--file', '--reuse-message', '--reedit-message', '--fixup', '--squash',
                     '--author', '--date', '--cleanup', '--template', '--trailer', '--pathspec-from-file'}
SEPARATE = 'stage and commit in separate commands, so the check sees the files that are really staged'


class Commit:
    def __init__(self, cwd, allow, kind='commit'):
        self.cwd = cwd
        self.allow = allow
        self.kind = kind          # 'commit', or a branch operation such as 'merge' (branch check only)
        self.all = False          # -a / --all: tracked working-tree changes are committed too
        self.paths = []           # pathspecs: their working-tree content is committed
        self.whole_tree = False   # --pathspec-from-file: unknown paths, scan every tracked change
        self.adds = []            # earlier `git add` in the same command: (cwd, paths, untracked, force)


class Add:
    def __init__(self, cwd, paths, untracked, force):
        self.cwd, self.paths, self.untracked, self.force = cwd, paths, untracked, force


def split_commands(toks):
    """Yield (separator_before, words, heredoc_bodies, output_redirect_targets) per simple command."""
    words, docs, outs, sep, redirect = [], [], [], None, None
    for t in toks:
        if isinstance(t, HereDoc):
            docs.append(t)
        elif isinstance(t, Op):
            if t.op in SEPARATORS:
                if words or docs or outs:
                    yield sep, words, docs, outs
                words, docs, outs, sep = [], [], [], t.op
            else:
                redirect = t.op   # the next word is a redirect target or heredoc delimiter
        elif redirect is not None:
            if redirect in OUTPUT_REDIRECTS:
                outs.append(t)
            redirect = None
        else:
            words.append(t)
    if words or docs or outs:
        yield sep, words, docs, outs


def contains_commit(toks, cwd):
    try:
        return bool(command_targets_from_tokens(toks, cwd, True))
    except Unsafe:
        return True


def normalized(command):
    """The command with line continuations, quotes and backslashes removed, for word mentions."""
    return re.sub(r'["\'\\]', '', command.replace('\\\n', ''))


def command_targets(command, cwd):
    if len(command) > MAX_COMMAND:
        raise Unsafe('command too large to analyse')
    toks, _ = lex(command)
    return command_targets_from_tokens(toks, cwd, bool(re.search(r'commit|merge|rebase|cherry|revert', normalized(command))))


def writes_files(name, args, outs):
    if any(o.dynamic or o.text not in HARMLESS_TARGETS and not o.text.isdigit() for o in outs):
        return True
    if name in FILE_WRITERS:
        return True
    if name in IN_PLACE_EDITORS:
        return any(a.text.startswith('--in-place') or (re.match(r'^-[A-Za-z]*i', a.text) and not a.text.startswith('--'))
                   for a in args)
    return False


def git_checkout_writes(args):
    texts = [a.text for a in args]
    if '--' in texts:
        return True
    if any(t in ('-b', '-B', '--orphan') for t in texts):
        return False
    return len([t for t in texts if not t.startswith('-')]) >= 2


def command_targets_from_tokens(toks, cwd, mentions_commit):
    commits, adds, stack = [], [], []
    current = Path(cwd)
    env_tainted = False
    wrote = False   # an earlier command in this one wrote files
    for sep, words, docs, outs in split_commands(toks):
        if sep == '(':
            stack.append(current)
        elif sep == ')' and stack:
            current = stack.pop()
        for w in words + outs:
            for inner in w.subs:
                if contains_commit(inner, current):
                    raise Unsafe('git commit inside a command substitution cannot be checked; run it directly')
        allow, redirect_env = False, False
        k = 0
        while k < len(words):
            w = words[k]
            if ASSIGNMENT.match(w.text):
                if w.text == 'GUARDRAILS_ALLOW_MAIN_COMMIT=1' and not w.dynamic:
                    allow = True
                elif w.text.startswith(('GIT_', 'PATH=')):
                    redirect_env = True
                k += 1
            elif w.text == 'function' and not w.quoted:
                k += 2   # `function name { ... }`: skip the keyword and the name
            elif w.text in KEYWORDS and not w.quoted:
                k += 1
            else:
                break
        rest = words[k:]
        if not rest:
            env_tainted = env_tainted or redirect_env
            wrote = wrote or bool(outs)
            continue
        head = rest[0]
        name = os.path.basename(head.text)
        seg_writes = writes_files(name, rest[1:], outs)
        if head.dynamic:
            if mentions_commit and any(x.text == 'commit' for x in rest[1:]) or 'git' in head.text:
                raise Unsafe('a variable-expanded command that may commit cannot be checked; run git commit directly')
            wrote = True
            continue
        if name == 'export':
            env_tainted = env_tainted or any(x.text.startswith(('GIT_', 'PATH=')) for x in rest[1:])
            continue
        if name in ('cd', 'pushd'):
            args = [x for x in rest[1:] if x.text != '--']
            if len(args) == 1 and not args[0].dynamic and args[0].text != '-':
                path = Path(os.path.expanduser(args[0].text))
                current = (current / path).resolve() if current is not None else (path if path.is_absolute() else None)
            else:
                current = None
            continue
        if name in SHELLS or name in RUNNERS or name in INTERPRETERS:
            text = ' '.join([x.text for x in rest[1:]] + ['\n'.join(d.lines) for d in docs])
            dynamic = name not in INTERPRETERS and mentions_commit and any(x.dynamic for x in rest[1:])
            if GIT_RISKY_TEXT.search(text) or dynamic:
                raise Unsafe('git commit run through %s cannot be checked; run git commit directly' % name)
            wrote = wrote or seg_writes or name in INTERPRETERS or name in SHELLS
            continue
        if name != 'git':
            wrote = wrote or seg_writes
            continue
        parsed = parse_git(rest[1:], current)
        wrote = wrote or seg_writes
        if parsed is None:
            continue
        sub, target, args, redirected = parsed
        if sub == 'add':
            adds.append(parse_add(args, target))
            continue
        if sub in ('checkout', 'switch'):
            wrote = wrote or git_checkout_writes(args)
            continue
        is_branch_op = sub in BRANCH_OPS and not any(a.text in ('--abort', '--quit') for a in args)
        if sub in GIT_FILE_WRITERS and not is_branch_op:
            wrote = True
        if sub != 'commit' and not is_branch_op:
            continue
        if redirected:
            raise Unsafe('git %s with a variable or redirected repository cannot be checked; use a literal -C path' % sub)
        if target is None:
            raise Unsafe('git %s after a directory change that cannot be resolved; cd to a literal path' % sub)
        if redirect_env or env_tainted:
            raise Unsafe('GIT_* or PATH changes repository resolution; run a plain git %s' % sub)
        if is_branch_op:
            commits.append(Commit(target, allow, sub))
            wrote = True
            continue
        commit = Commit(target, allow)
        parse_commit(args, commit)
        commit.adds = list(adds)
        takes_worktree = commit.adds or commit.all or commit.paths or commit.whole_tree
        if takes_worktree and wrote:
            raise Unsafe('files are written earlier in this command; ' + SEPARATE)
        for add in commit.adds:
            for p in add.paths:
                if add.cwd is None or (not re.search(r'[*?\[]', p) and not p.startswith(':')
                                       and not os.path.lexists(os.path.join(str(add.cwd), p))):
                    raise Unsafe('git add names a path that does not exist yet; ' + SEPARATE)
        commits.append(commit)
    return commits


def load_aliases(cwd, inline):
    aliases = {}
    try:
        result = subprocess.run(['git', '-C', str(cwd), 'config', '-z', '--get-regexp', r'^alias\.'],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=git_timeout())
        for entry in result.stdout.split(b'\0'):
            key, _, value = entry.partition(b'\n')
            if key.lower().startswith(b'alias.'):
                aliases[key[6:].decode('utf-8', 'replace').lower()] = value.decode('utf-8', 'replace')
    except OSError:
        pass
    aliases.update(inline)
    return aliases


def parse_git(args, cwd, depth=0):
    """Return (subcommand, cwd, rest, redirected) with aliases expanded; None when there is no subcommand."""
    i, target, redirected, inline = 0, cwd, False, {}
    while i < len(args) and args[i].text.startswith('-'):
        flag = args[i].text.split('=', 1)[0]
        if args[i].dynamic or flag in GIT_REDIRECTING:
            redirected = True
        if flag in GIT_VALUE_GLOBALS and '=' not in args[i].text:
            if i + 1 >= len(args):
                return None
            value = args[i + 1]
            if flag == '-C':
                if value.dynamic:
                    redirected = True
                elif target is not None:
                    target = (target / os.path.expanduser(value.text)).resolve()
            elif flag == '-c':
                if value.dynamic:
                    redirected = True
                key, _, val = value.text.partition('=')
                if key.lower().startswith('alias.'):
                    inline[key[6:].lower()] = val
            i += 2
        elif flag in GIT_VALUE_GLOBALS or flag in GIT_BOOL_GLOBALS:
            i += 1
        elif flag.startswith('-c'):
            key, _, val = args[i].text[2:].partition('=')
            if key.lower().startswith('alias.'):
                inline[key[6:].lower()] = val
            i += 1
        elif flag in ('--version', '--help', '-h', '--html-path', '--man-path', '--info-path'):
            return None
        else:
            raise Unsafe('unrecognised git global option %s; run a plain git command' % flag)
    if i >= len(args):
        return None
    sub = args[i]
    if sub.dynamic:
        raise Unsafe('a variable-expanded git subcommand cannot be checked; run git commit directly')
    rest = args[i + 1:]
    if sub.text in GIT_BUILTINS:
        return sub.text, target, rest, redirected
    if target is None or redirected:
        raise Unsafe('git %s may be an alias in a repository that cannot be resolved; use a literal path' % sub.text)
    value = load_aliases(target, inline).get(sub.text.lower())
    if value is None:
        return None   # not a command git knows; it will fail on its own
    if value.lstrip().startswith('!'):
        raise Unsafe('git alias "%s" runs a shell command, which cannot be checked; run git commit directly' % sub.text)
    if depth >= 10:
        raise Unsafe('git alias "%s" expands too deeply to check' % sub.text)
    expansion = [t for t in lex(value)[0] if isinstance(t, Word)]
    return parse_git(expansion + rest, target, depth + 1)


def parse_add(args, cwd):
    paths, untracked, force, rest_are_paths = [], True, False, False
    for a in args:
        t = a.text
        if not rest_are_paths and t == '--':
            rest_are_paths = True
        elif not rest_are_paths and t.startswith('-') and len(t) > 1:
            if t in ('-u', '--update'):
                untracked = False
            elif t == '--force' or (not t.startswith('--') and 'f' in t[1:]):
                force = True
        else:
            paths.append(t)
    return Add(cwd, paths, untracked, force)


def parse_commit(args, commit):
    i, only_paths = 0, False
    while i < len(args):
        t = args[i].text
        if only_paths or not t.startswith('-') or t == '-':
            commit.paths.append(t)
        elif t == '--':
            only_paths = True
        elif t.startswith('--'):
            name = t.split('=', 1)[0]
            if name == '--all':
                commit.all = True
            elif name == '--pathspec-from-file':
                commit.whole_tree = True
            if name in COMMIT_VALUE_LONG and '=' not in t:
                i += 1
        else:
            for pos, ch in enumerate(t[1:], 1):
                if ch == 'a':
                    commit.all = True
                elif ch in COMMIT_VALUE_SHORT:
                    if pos == len(t) - 1:
                        i += 1   # value is the next argument
                    break        # otherwise the value is attached
        i += 1


# --------------------------------------------------------------------------- git and scanning

def git_timeout():
    if DEADLINE[0] is None:
        return 20
    remaining = DEADLINE[0] - time.monotonic()
    if remaining <= 0:
        raise subprocess.TimeoutExpired('git', 0)
    return remaining


def git(cwd, args):
    result = subprocess.run(['git', '-C', str(cwd), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=git_timeout())
    if result.returncode:
        raise ValueError('git could not read the repository at %s' % cwd)
    return result.stdout


def c_unquote(raw):
    """Undo Git's C-style quoting of a path."""
    if not (raw.startswith(b'"') and raw.endswith(b'"')):
        return raw
    out, i, body = bytearray(), 0, raw[1:-1]
    simple = {ord('n'): 10, ord('t'): 9, ord('r'): 13, ord('"'): 34, ord('\\'): 92, ord('a'): 7,
              ord('b'): 8, ord('f'): 12, ord('v'): 11}
    while i < len(body):
        if body[i] == 92 and i + 1 < len(body):
            nxt = body[i + 1]
            if 48 <= nxt <= 55:
                out.append(int(body[i + 1:i + 4], 8))
                i += 4
                continue
            out.append(simple.get(nxt, nxt))
            i += 2
            continue
        out.append(body[i])
        i += 1
    return bytes(out)


def scan_diff_output(output, where):
    findings, path, line, header = [], None, 0, False
    for raw in output.split(b'\n'):
        if raw.startswith(b'diff --git '):
            header, path = True, None
        elif header and raw.startswith(b'+++ '):
            target = c_unquote(raw[4:])
            path = None if target == b'/dev/null' else target[2:]
        elif raw.startswith(b'@@ '):
            header = False
            match = re.match(rb'@@ -\S+ \+(\d+)', raw)
            line = int(match.group(1)) if match else 0
        elif not header and raw.startswith(b'+') and path is not None:
            if SECRET.search(raw[1:]):
                findings.append((path, line, where))
            line += 1
    return findings


DIFF = ['-c', 'core.quotePath=false', 'diff', '-U0', '--no-color', '--no-ext-diff', '--no-textconv',
        '--src-prefix=a/', '--dst-prefix=b/']


def scan_untracked(cwd, paths, force):
    findings = []
    # `git add -f` stages ignored files too, so they are scanned as well.
    standard = [] if force else ['--exclude-standard']
    listing = git(cwd, ['ls-files', '-z', '--others', *standard, '--', *paths])
    for rel in filter(None, listing.split(b'\0')):
        full = Path(cwd) / os.fsdecode(rel)
        try:
            with open(full, 'rb') as handle:
                if b'\0' in handle.read(8000):
                    continue   # binary, as git diff treats it
                handle.seek(0)
                for number, content in enumerate(handle, 1):
                    if SECRET.search(content):
                        findings.append((rel, number, 'untracked file to be added'))
        except OSError:
            raise ValueError('could not read a file that git add would stage; check it before committing')
    return findings


def scan_commit(commit):
    """One git call for the staged diff; extra calls only when the commit takes working-tree changes."""
    findings = scan_diff_output(git(commit.cwd, [*DIFF, '--cached']), 'staged')
    if commit.all or commit.whole_tree:
        findings += scan_diff_output(git(commit.cwd, DIFF), 'unstaged change committed by -a')
    elif commit.paths:
        findings += scan_diff_output(git(commit.cwd, [*DIFF, '--', *commit.paths]), 'unstaged change in a committed path')
    for add in commit.adds:
        findings += scan_diff_output(git(add.cwd, [*DIFF, '--', *add.paths]), 'change to be staged by git add')
        if add.untracked:
            findings += scan_untracked(add.cwd, add.paths, add.force)
    return findings


def show_path(raw):
    text = raw.decode('utf-8', 'replace')
    if SECRET.search(raw) or any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        return '<file name withheld: it matches a secret pattern or holds control characters>'
    return text


def report(findings):
    lines = ['Blocked: possible secret in the commit (values withheld):']
    for path, line, where in findings[:MAX_FINDINGS]:
        lines.append('  %s:%d (%s)' % (show_path(path), line, where))
    if len(findings) > MAX_FINDINGS:
        lines.append('  ... and %d more' % (len(findings) - MAX_FINDINGS))
    lines.append('Remove the value (use an environment variable or a secret store), restage, and commit again.')
    return '\n'.join(lines)


def branch_check(cwd, allow):
    if allow or os.environ.get('GUARDRAILS_ALLOW_MAIN_COMMIT') == '1':
        return
    branch = git(cwd, ['branch', '--show-current']).decode().strip()
    if not branch:
        return   # detached HEAD is not the default branch
    defaults = {'main', 'master'}
    try:
        remote = git(cwd, ['symbolic-ref', '--short', 'refs/remotes/origin/HEAD']).decode().strip()
        if remote.startswith('origin/'):
            defaults.add(remote[len('origin/'):])
    except ValueError:
        pass
    if branch in defaults:
        raise ValueError('commit on the default branch "%s"; create a work branch first '
                         '(or set GUARDRAILS_ALLOW_MAIN_COMMIT=1 for a deliberate bootstrap commit)' % branch)


def read_targets():
    raw = sys.stdin.read(4 * MAX_COMMAND + 1)
    if len(raw) > 4 * MAX_COMMAND:
        raise ValueError('oversized hook input')
    try:
        data = json.loads(raw)
    except ValueError:
        raise ValueError('invalid hook input')
    if not isinstance(data, dict):
        raise ValueError('invalid hook input')
    tool = data.get('tool_input')
    if not isinstance(tool, dict) or not isinstance(tool.get('command'), str):
        raise ValueError('missing command in hook input')
    cwd = data.get('cwd', os.getcwd())
    if not isinstance(cwd, str):
        raise ValueError('invalid working directory')
    return command_targets(tool['command'], cwd)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('check', choices=['secrets', 'branch'])
    ap.add_argument('--git-hook', action='store_true')
    args = ap.parse_args(argv)
    budget = SECRETS_BUDGET if args.check == 'secrets' else BRANCH_BUDGET
    DEADLINE[0] = time.monotonic() + budget
    try:
        targets = [Commit(Path.cwd(), False)] if args.git_hook else read_targets()
        for commit in targets:
            if args.check == 'secrets':
                if commit.kind != 'commit':
                    continue   # merges and rebases replay commits that were already checked
                findings = scan_commit(commit)
                if findings:
                    print(report(findings), file=sys.stderr)
                    return 2
            else:
                branch_check(commit.cwd, commit.allow)
    except ValueError as error:
        print('Blocked: ' + str(error), file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print('Blocked: git did not answer within %ds, so the commit check could not complete; '
              'retry, or check the repository for a lock or a slow filesystem' % budget, file=sys.stderr)
        return 2
    except OSError:
        print('Blocked: the commit check could not complete; run git commit again or check the repository',
              file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
