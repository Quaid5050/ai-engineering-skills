import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
GUARD=ROOT/'plugins/guardrails/scripts/guard.py'

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.clean=self.base/'clean';self.secret=self.base/'secret'
        for p in (self.clean,self.secret):
            p.mkdir();self.git(p,'init','-b','main')
        self.token='AK'+'IA'+'Z'*16
        (self.secret/'fixture.txt').write_text(self.token)
        self.git(self.secret,'add','fixture.txt')

    def git(self,cwd,*args):
        return subprocess.run(['git',*args],cwd=cwd,check=True,capture_output=True)

    def run_guard(self,kind,command=None,raw=None,cwd=None,hook=False):
        args=[sys.executable,str(GUARD),kind]+(['--git-hook'] if hook else [])
        payload=raw if raw is not None else json.dumps({'cwd':str(cwd or self.clean),'tool_input':{'command':command}})
        result=subprocess.run(args,input=payload,text=True,capture_output=True,cwd=cwd or self.clean)
        self.assertNotIn(self.token,result.stdout+result.stderr)
        return result

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

    def test_index_mutation_requires_separate_staging(self):
        for command in ('git add . && git commit -m test','git commit -am test','git commit fixture.txt'):
            with self.subTest(command=command):self.assertEqual(self.run_guard('secrets',command).returncode,2)

    def test_safe_feature_branch(self):
        self.git(self.clean,'switch','-c','feature')
        self.assertEqual(self.run_guard('branch','git commit -m test').returncode,0)

    def test_unusual_filename_does_not_expose_value(self):
        name='sensitive-'+self.token+'\n.txt';(self.secret/name).write_text(self.token)
        self.git(self.secret,'add','--',name)
        self.assertEqual(self.run_guard('secrets',cwd=self.secret,hook=True).returncode,2)

    def test_unstaged_secret_is_not_part_of_actual_index(self):
        (self.clean/'safe.txt').write_text('safe');self.git(self.clean,'add','safe.txt')
        (self.clean/'safe.txt').write_text(self.token)
        self.assertEqual(self.run_guard('secrets',cwd=self.clean,hook=True).returncode,0)
