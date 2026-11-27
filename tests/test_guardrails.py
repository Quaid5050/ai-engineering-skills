import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'plugins/guardrails/scripts'
GUARD=SCRIPTS/'guard.py'
HEREDOC_COMMIT="""git commit -m "$(cat <<'EOF'
feat(app): don't break (really); `x` $(y) | eval

Body says git commit -am "nope" && bash -c "git commit"
EOF
)\""""


def load_guard():
    spec=importlib.util.spec_from_file_location('guard_under_test',GUARD)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.clean=self.base/'clean';self.secret=self.base/'secret'
        for p in (self.clean,self.secret):
            p.mkdir();self.git(p,'init','-b','main')
            self.git(p,'config','user.email','dev');self.git(p,'config','user.name','Dev')
        self.token='AK'+'IA'+'Z'*16
        (self.secret/'fixture.txt').write_text('first line\n'+self.token+'\n')
        self.git(self.secret,'add','fixture.txt')

    def git(self,cwd,*args):
        return subprocess.run(['git',*args],cwd=cwd,check=True,capture_output=True)

    def feature(self,repo):
        self.git(repo,'switch','-c','feature')

    def commit_base(self,repo):
        (repo/'tracked.txt').write_text('safe\n');self.git(repo,'add','tracked.txt')
        self.git(repo,'commit','-m','base')

    def run_guard(self,kind,command=None,raw=None,cwd=None,hook=False):
        args=[sys.executable,str(GUARD),kind]+(['--git-hook'] if hook else [])
        payload=raw if raw is not None else json.dumps({'cwd':str(cwd or self.clean),'tool_input':{'command':command}})
        result=subprocess.run(args,input=payload,text=True,capture_output=True,cwd=cwd or self.clean)
        self.assertNotIn(self.token,result.stdout+result.stderr)
        return result

    def run_wrapper(self,script,command,cwd=None,env=None):
        payload=json.dumps({'cwd':str(cwd or self.clean),'tool_input':{'command':command}})
        result=subprocess.run(['/bin/bash',str(SCRIPTS/script)],input=payload,text=True,capture_output=True,
                              cwd=cwd or self.clean,env=env)
        self.assertNotIn(self.token,result.stdout+result.stderr)
        return result

    # existing behaviour
    def test_real_index_hook_redacts(self):
        self.assertEqual(self.run_guard('secrets',cwd=self.secret,hook=True).returncode,2)

    def test_other_repository_git_C(self):
        self.assertEqual(self.run_guard('secrets',f'git -C {self.secret} commit -m test').returncode,2)

    def test_cd_chain(self):
        self.assertEqual(self.run_guard('secrets',f'cd {self.secret} && git commit -m test').returncode,2)

    def test_global_config_option(self):
        self.assertEqual(self.run_guard('branch','git -c user.name=Test commit -m test').returncode,2)

    def test_echo_does_not_grant_override(self):
        self.assertEqual(self.run_guard('branch','echo GUARDRAILS_ALLOW_MAIN_COMMIT=1 && git commit -m test').returncode,2)

    def test_actual_override(self):
        self.assertEqual(self.run_guard('branch','GUARDRAILS_ALLOW_MAIN_COMMIT=1 git commit -m test').returncode,0)

    def test_malformed_payload(self):
        self.assertEqual(self.run_guard('branch',raw='{invalid').returncode,2)

    def test_safe_feature_branch(self):
        self.feature(self.clean)
        self.assertEqual(self.run_guard('branch','git commit -m test').returncode,0)

    def test_unusual_filename_does_not_expose_value(self):
        name='sensitive-'+self.token+'\n.txt';(self.secret/name).write_text(self.token)
        self.git(self.secret,'add','--',name)
        result=self.run_guard('secrets',cwd=self.secret,hook=True)
        self.assertEqual(result.returncode,2);self.assertIn('file name withheld',result.stderr)

    def test_unstaged_secret_is_not_part_of_actual_index(self):
        (self.clean/'safe.txt').write_text('safe');self.git(self.clean,'add','safe.txt')
        (self.clean/'safe.txt').write_text(self.token)
        self.assertEqual(self.run_guard('secrets',cwd=self.clean,hook=True).returncode,0)

    # bug 1: only a real git commit is analysed
    def test_commands_that_only_mention_commit_are_allowed(self):
        for command in ('git log | grep commit','cat docs/commit-guide.md','gh pr create --body "commit"',
                        'echo "git commit"','git log --grep=commit && git status','grep -r "git commit" docs'):
            for kind in ('secrets','branch'):
                with self.subTest(command=command,kind=kind):
                    self.assertEqual(self.run_guard(kind,command,cwd=self.secret).returncode,0)

    def test_real_commit_forms_are_allowed_on_a_clean_feature_branch(self):
        self.feature(self.clean);self.commit_base(self.clean);(self.clean/'sub').mkdir()
        for command in ('git commit -m "feat(app): x"',HEREDOC_COMMIT,'git commit -am "x"','git add . && git commit -m "x"',
                        'cd sub && git commit -m x',f'git -C {self.clean} -c core.pager=cat commit -m x',
                        'git status && git commit -m x 2>&1 | tail -n 3','git commit --amend --no-edit'):
            for kind in ('secrets','branch'):
                with self.subTest(command=command,kind=kind):
                    result=self.run_guard(kind,command)
                    self.assertEqual(result.returncode,0,result.stderr)

    def test_heredoc_message_still_checked(self):
        self.assertEqual(self.run_guard('branch',HEREDOC_COMMIT).returncode,2)
        self.assertEqual(self.run_guard('secrets',HEREDOC_COMMIT,cwd=self.secret).returncode,2)

    def test_parenthesised_message_still_checked(self):
        self.assertEqual(self.run_guard('branch','git commit -m "feat(app): x"').returncode,2)

    def test_commits_that_cannot_be_analysed_are_blocked(self):
        self.feature(self.clean)
        for command in ('eval "git commit -m x"','bash -c "git commit -m x"','sh -c \'cd x && git commit\'',
                        '$GIT commit -m x','"$GIT" commit -m x','git -C "$DIR" commit -m x','git $SUB -m x',
                        'echo $(git commit -m x)','x=`git commit -m x`','bash <<EOF\ngit commit -m x\nEOF',
                        'GIT_DIR=/elsewhere git commit -m x','export GIT_DIR=/elsewhere; git commit -m x',
                        'git --git-dir=/elsewhere commit -m x','cd "$DIR" && git commit -m x','sudo git commit -m x',
                        'xargs git commit -m x'):
            with self.subTest(command=command):
                result=self.run_guard('branch',command)
                self.assertEqual(result.returncode,2);self.assertIn('Blocked:',result.stderr)

    # bug 2: detached HEAD
    def test_detached_head_is_allowed(self):
        self.commit_base(self.clean)
        self.git(self.clean,'switch','--detach')
        self.assertEqual(self.run_guard('branch','git commit -m x').returncode,0)
        self.assertEqual(self.run_guard('branch',cwd=self.clean,hook=True).returncode,0)

    def test_master_and_remote_default_are_blocked(self):
        self.commit_base(self.clean)
        self.git(self.clean,'branch','-m','master')
        self.assertEqual(self.run_guard('branch','git commit -m x').returncode,2)
        self.git(self.clean,'branch','-m','trunk')
        self.git(self.clean,'update-ref','refs/remotes/origin/trunk','HEAD')
        self.git(self.clean,'symbolic-ref','refs/remotes/origin/HEAD','refs/remotes/origin/trunk')
        self.assertEqual(self.run_guard('branch','git commit -m x').returncode,2)

    # bug 3: added lines of the diff only, in one git call
    def test_secret_scan_uses_one_git_call_for_many_files(self):
        for n in range(200): (self.clean/f'f{n}.txt').write_text(f'line {n}\n')
        self.git(self.clean,'add','.')
        guard=load_guard();calls=[]
        real=subprocess.run
        def counting(cmd,*a,**k):
            calls.append(cmd);return real(cmd,*a,**k)
        with mock.patch.object(guard.subprocess,'run',counting):
            commit=guard.command_targets('git commit -m x',str(self.clean))[0]
            started=time.monotonic();findings=guard.scan_commit(commit)
        self.assertEqual(findings,[]);self.assertEqual(len(calls),1);self.assertIn('--cached',calls[0])
        self.assertLess(time.monotonic()-started,5)

    def test_only_added_lines_are_scanned(self):
        repo=self.clean;(repo/'old.txt').write_text(self.token+'\n');self.git(repo,'add','old.txt')
        self.git(repo,'commit','-m','old');self.feature(repo)
        (repo/'old.txt').write_text('cleaned\n');self.git(repo,'add','old.txt')
        self.assertEqual(self.run_guard('secrets','git commit -m remove').returncode,0)

    def test_commit_all_scans_tracked_working_tree_changes(self):
        self.commit_base(self.clean);(self.clean/'tracked.txt').write_text('safe\n'+self.token+'\n')
        result=self.run_guard('secrets','git commit -am "x"')
        self.assertEqual(result.returncode,2);self.assertIn('tracked.txt:2',result.stderr)
        self.assertEqual(self.run_guard('secrets','git commit -m "x"').returncode,0)

    def test_add_then_commit_scans_what_add_will_stage(self):
        self.commit_base(self.clean);(self.clean/'new.txt').write_text(self.token+'\n')
        result=self.run_guard('secrets','git add . && git commit -m "x"')
        self.assertEqual(result.returncode,2);self.assertIn('new.txt:1',result.stderr)

    def test_pathspec_commit_scans_those_paths(self):
        self.commit_base(self.clean);(self.clean/'tracked.txt').write_text(self.token+'\n')
        self.assertEqual(self.run_guard('secrets','git commit -m x -- tracked.txt').returncode,2)

    # bug 4: real path and line, never the value
    def test_block_message_names_path_and_line(self):
        result=self.run_guard('secrets','git commit -m x',cwd=self.secret)
        self.assertEqual(result.returncode,2)
        self.assertIn('fixture.txt:2',result.stderr);self.assertNotIn('path-',result.stderr)

    # bug 5: cheap pre-filter, python3 optional
    def test_wrapper_allows_non_commit_commands_without_python(self):
        env={'PATH':str(self.base/'empty-bin')}
        for script in ('check-staged-secrets.sh','no-commit-on-main.sh'):
            with self.subTest(script=script):
                result=self.run_wrapper(script,'ls -la',env=env)
                self.assertEqual(result.returncode,0);self.assertEqual(result.stderr,'')

    def test_wrapper_warns_and_allows_commit_without_python(self):
        env={'PATH':str(self.base/'empty-bin')}
        result=self.run_wrapper('no-commit-on-main.sh','git commit -m x',env=env)
        self.assertEqual(result.returncode,0);self.assertIn('python3 not found',result.stderr)

    def test_wrapper_runs_the_guard_on_a_commit(self):
        self.assertEqual(self.run_wrapper('check-staged-secrets.sh','git commit -m x',cwd=self.secret).returncode,2)
        self.assertEqual(self.run_wrapper('no-commit-on-main.sh','git commit -m x').returncode,2)
        self.assertEqual(self.run_wrapper('no-commit-on-main.sh','git log | grep commit').returncode,0)


    # review follow-up 1: files written earlier in the same command
    def test_files_written_before_add_and_commit_are_blocked(self):
        self.feature(self.clean);self.commit_base(self.clean)
        (self.base/'s').write_text(self.token)
        for command in (f'echo {self.token} > k.txt && git add k.txt && git commit -m x',
                        f'cp {self.base}/s . && git add s && git commit -m x',
                        f'cat {self.base}/s | tee tracked.txt && git commit -am x',
                        "sed -i.bak 's/safe/x/' tracked.txt && git add . && git commit -m x",
                        'git stash pop && git add . && git commit -m x',
                        'git checkout stash@{0} -- tracked.txt && git commit -am x',
                        'git add missing.txt && git commit -m x'):
            for kind in ('secrets','branch'):
                with self.subTest(command=command,kind=kind):
                    result=self.run_guard(kind,command)
                    self.assertEqual(result.returncode,2);self.assertIn('separate commands',result.stderr)

    def test_harmless_steps_before_add_and_commit_are_allowed(self):
        self.feature(self.clean);self.commit_base(self.clean)
        for command in ('git status 2>/dev/null && git add tracked.txt && git commit -m x',
                        'git checkout -b other && git add . && git commit -m x',
                        'echo done > /dev/null; git add "*.txt" && git commit -m x',
                        'git diff --stat > /dev/null && git commit -m x'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('secrets',command).returncode,0)

    def test_writes_before_a_plain_commit_are_allowed(self):
        self.feature(self.clean)
        self.assertEqual(self.run_guard('secrets','echo note > notes.txt && git commit -m x').returncode,0)

    # review follow-up 2: git add -f stages ignored files
    def test_forced_add_scans_ignored_files(self):
        self.feature(self.clean);(self.clean/'.gitignore').write_text('local.env\n')
        (self.clean/'local.env').write_text(self.token+'\n')
        result=self.run_guard('secrets','git add -f local.env && git commit -m x')
        self.assertEqual(result.returncode,2);self.assertIn('local.env:1',result.stderr)
        self.assertEqual(self.run_guard('secrets','git add . && git commit -m x').returncode,0)

    # review follow-up 3: quoting cannot hide the command from the pre-filter
    def test_wrapper_sees_quoted_and_continued_commands(self):
        for command in ('git co""mmit -m x',"g''it commit -m x",'git c\\ommit -m x','git c\\\nommit -m x',
                        'g${EMPTY}it commit -m x'):
            with self.subTest(command=command):
                result=self.run_wrapper('no-commit-on-main.sh',command)
                self.assertEqual(result.returncode,2,result.stderr)

    # review follow-up 4: aliases, functions, interpreters, branch operations
    def test_git_aliases_are_resolved(self):
        self.git(self.clean,'config','alias.ci','commit -a')
        self.git(self.clean,'config','alias.lg','log --oneline')
        self.git(self.clean,'config','alias.sh','!git commit')
        self.assertEqual(self.run_guard('branch','git ci -m x').returncode,2)
        self.assertEqual(self.run_guard('branch','git -c alias.save=commit save -m x').returncode,2)
        self.assertIn('shell command',self.run_guard('branch','git sh').stderr)
        self.assertEqual(self.run_guard('branch','git lg').returncode,0)
        self.git(self.secret,'config','alias.ci','commit');self.feature(self.secret)
        self.assertEqual(self.run_guard('secrets','git ci -m x',cwd=self.secret).returncode,2)

    def test_function_bodies_and_interpreters_are_checked(self):
        for command in ('function f { git commit -m x; }; f',
                        'python3 -c "import os; os.system(\'git commit -m x\')"',
                        "perl -e 'system(\"git commit -m x\")'",'node -e "run(\'git commit\')"',
                        "awk 'BEGIN{system(\"git commit -m x\")}'"):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,2)
        self.assertEqual(self.run_guard('branch','python3 -c "print(1)" && git status').returncode,0)

    def test_branch_operations_on_the_default_branch(self):
        self.commit_base(self.clean)
        for command in ('git merge feature','git cherry-pick abc123','git rebase --continue','git revert HEAD',
                        'git am < fix.patch'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,2)
        for command in ('git merge --abort','git rebase --quit','git log --merges'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,0)
        self.feature(self.clean)
        self.assertEqual(self.run_guard('branch','git rebase main').returncode,0)
        self.assertEqual(self.run_guard('secrets','git merge main').returncode,0)

    # review follow-up 5: git time fits the hook timeouts and a timeout blocks
    def test_git_timeout_blocks_with_a_message(self):
        guard=load_guard()
        def slow(cmd,*a,**k): raise subprocess.TimeoutExpired(cmd,k.get('timeout',0))
        payload=json.dumps({'cwd':str(self.clean),'tool_input':{'command':'git commit -m x'}})
        with mock.patch.object(guard.subprocess,'run',slow),mock.patch('sys.stdin',io.StringIO(payload)),\
                mock.patch('sys.stderr',new_callable=io.StringIO) as err:
            self.assertEqual(guard.main(['secrets']),2)
        self.assertIn('did not answer',err.getvalue())

    def test_git_budgets_fit_inside_hook_timeouts(self):
        guard=load_guard()
        hooks=json.loads((ROOT/'plugins/guardrails/hooks/hooks.json').read_text())['hooks']['PreToolUse'][0]['hooks']
        timeouts={Path(h['args'][-1]).name:h['timeout'] for h in hooks}
        self.assertLess(guard.SECRETS_BUDGET,timeouts['check-staged-secrets.sh'])
        self.assertLess(guard.BRANCH_BUDGET,timeouts['no-commit-on-main.sh'])
        for h in hooks:
            self.assertEqual(h['command'],'bash');self.assertTrue((SCRIPTS/Path(h['args'][-1]).name).exists())


    # round 2 re-review
    def test_shells_and_interpreters_fed_on_stdin_are_blocked(self):
        self.feature(self.clean)
        for command in ('echo "git commit -m x" | bash',"printf 'git commit -m x' | sh",'bash <<<"git commit -m x"',
                        'echo "import os; os.system(\'git commit\')" | python3','python3 <<<"git commit"'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,2)
        for command in ('git log --oneline | python3 -c "import sys; print(len(sys.stdin.read()))"',
                        'git status | sh -c "cat"','git log | grep commit'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,0)

    def test_alias_defined_in_the_same_command_is_blocked(self):
        self.feature(self.clean)
        for command in ('git config alias.ci commit && git ci -m x','git config --global alias.ci commit; git ci -m x',
                        'git config --local alias.ci "commit -a" && git -C . ci -m x',
                        'git config include.path ../x && git ci','echo "[alias] ci = commit" >> .git/config && git ci'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,2)
        self.assertEqual(self.run_guard('branch','git config user.name Dev && git status').returncode,0)

    def test_shell_alias_to_git_commit_is_blocked(self):
        self.feature(self.clean)
        for command in ('shopt -s expand_aliases; alias gc="git commit"; gc -m x',"alias gm='git merge'"):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,2)
        self.assertEqual(self.run_guard('branch','alias ll="ls -l"; git status').returncode,0)

    def test_pull_on_the_default_branch_is_blocked(self):
        self.commit_base(self.clean)
        for command in ('git pull','git pull --rebase origin main'):
            with self.subTest(command=command):
                self.assertEqual(self.run_guard('branch',command).returncode,2)
        self.assertEqual(self.run_guard('branch','git pull --ff-only').returncode,0)
        self.feature(self.clean)
        self.assertEqual(self.run_guard('branch','git pull --rebase').returncode,0)


if __name__=='__main__':
    unittest.main()
