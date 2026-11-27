import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('installer',ROOT/'scripts/install_skills.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'source';self.target=Path(self.tmp.name)/'target'
        (self.root/'catalog').mkdir(parents=True)
        entries=[]
        for name,plugin,requires in [('context','foundation',[]),('tdd','quality',['context'])]:
            path=f'plugins/{plugin}/skills/{name}';p=self.root/path;p.mkdir(parents=True)
            (p/'SKILL.md').write_text('original '+name)
            entries.append({'name':name,'plugin':plugin,'path':path,'requires':requires})
        (self.root/'catalog/skills.json').write_text(json.dumps({'skills':entries}))
    def install(self,**kw):return m.install(self.target,root=self.root,**kw)
    def test_filtered_install_includes_required_skill(self):
        self.install(filters=['quality']);self.assertTrue((self.target/'context/SKILL.md').exists())
    def test_copy_upgrade_and_rollback(self):
        self.install();(self.root/'plugins/quality/skills/tdd/SKILL.md').write_text('new content')
        self.install();self.assertEqual((self.target/'tdd/SKILL.md').read_text(),'new content')
        self.install(rollback=True);self.assertEqual((self.target/'tdd/SKILL.md').read_text(),'original tdd')
    def test_foreign_symlink_and_directory_preserved(self):
        self.target.mkdir();foreign=Path(self.tmp.name)/'foreign';foreign.mkdir();(foreign/'mine').write_text('mine')
        (self.target/'tdd').symlink_to(foreign,target_is_directory=True)
        with self.assertRaises(ValueError):self.install()
        self.assertTrue((self.target/'tdd').is_symlink());self.assertEqual((foreign/'mine').read_text(),'mine')
        self.assertFalse((self.target/'context').exists())
    def test_modified_owned_content_preserved(self):
        self.install();(self.target/'tdd/SKILL.md').write_text('local work')
        with self.assertRaises(ValueError):self.install()
        self.assertEqual((self.target/'tdd/SKILL.md').read_text(),'local work')
    def test_unknown_filter_fails(self):
        with self.assertRaises(ValueError):self.install(filters=['unknown'])
    def test_each_mutation_boundary_is_recoverable(self):
        self.install()
        for point,index in [('backup',0),('install',0),('backup',1),('install',1),('manifest',0)]:
            def fail(where,number):
                if (where,number)==(point,index):raise RuntimeError('simulated interruption')
            with self.assertRaises(RuntimeError):self.install(fault=fail)
            self.install(recover=True)
            self.assertEqual((self.target/'tdd/SKILL.md').read_text(),'original tdd')
            self.assertEqual((self.target/'context/SKILL.md').read_text(),'original context')
    def test_uninstall_does_not_touch_foreign_files(self):
        self.install();(self.target/'unrelated').write_text('keep')
        self.install(uninstall=True)
        self.assertFalse((self.target/'tdd').exists());self.assertEqual((self.target/'unrelated').read_text(),'keep')
    def test_cannot_remove_required_dependency(self):
        self.install()
        with self.assertRaises(ValueError):self.install(filters=['foundation'],uninstall=True)
    def test_lock_prevents_simultaneous_installer(self):
        self.target.mkdir();handle=m.acquire(self.target)
        try:
            with self.assertRaises(ValueError):self.install()
        finally:handle.close()
    def test_required_graph_cycle_rejected(self):
        path=self.root/'catalog/skills.json';data=json.loads(path.read_text());data['skills'][0]['requires']=['tdd'];path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):self.install()
    def test_nested_symlink_rejected(self):
        (self.root/'plugins/quality/skills/tdd/escape').symlink_to(Path(self.tmp.name))
        with self.assertRaises(ValueError):self.install()

    def test_recovery_rejects_traversal_without_touching_neighbor(self):
        self.install()
        journal=self.target/m.JOURNAL;history=self.target/m.HISTORY
        history.rename(journal)
        plan=json.loads((journal/'plan.json').read_text());plan['operations'][0]['name']='../neighbor'
        (journal/'plan.json').write_text(json.dumps(plan));neighbor=self.target.parent/'neighbor';neighbor.write_text('keep')
        with self.assertRaises(ValueError):self.install(recover=True)
        self.assertEqual(neighbor.read_text(),'keep')
    def test_recovery_preserves_changed_manifest(self):
        self.install()
        def fail(where,number):
            if where=='manifest':raise RuntimeError('interrupted')
        with self.assertRaises(RuntimeError):self.install(fault=fail)
        path=self.target/m.STATE;state=json.loads(path.read_text());state['extra']='local change';path.write_text(json.dumps(state))
        with self.assertRaises(ValueError):self.install(recover=True)
        self.assertEqual(json.loads(path.read_text())['extra'],'local change')
    def test_foreign_dangling_symlink_not_followed(self):
        self.target.mkdir();(self.target/'tdd').symlink_to(self.target/'not-present')
        with self.assertRaisesRegex(ValueError,'foreign skill collision'):self.install()
        self.assertTrue((self.target/'tdd').is_symlink())
    def test_link_source_update_and_uninstall(self):
        self.install(mode='link')
        (self.root/'plugins/quality/skills/tdd/SKILL.md').write_text('new source')
        self.install(mode='link')
        self.assertEqual((self.target/'tdd/SKILL.md').read_text(),'new source')
        self.install(uninstall=True)
        self.assertEqual((self.root/'plugins/quality/skills/tdd/SKILL.md').read_text(),'new source')
    def test_filtered_uninstall_retains_shared_dependencies(self):
        self.install()
        self.install(filters=['quality'],uninstall=True)
        self.assertFalse((self.target/'tdd').exists());self.assertTrue((self.target/'context').exists())
    def test_added_empty_directory_is_local_modification(self):
        self.install();(self.target/'tdd/keep-empty').mkdir()
        with self.assertRaises(ValueError):self.install()
        self.assertTrue((self.target/'tdd/keep-empty').is_dir())
    def test_process_exit_releases_lock_without_unlink(self):
        import subprocess,sys
        self.target.mkdir()
        code="import importlib.util,sys,time;from pathlib import Path;s=importlib.util.spec_from_file_location('installer',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);h=m.acquire(Path(sys.argv[2]));print('locked',flush=True);time.sleep(30)"
        proc=subprocess.Popen([sys.executable,'-c',code,str(ROOT/'scripts/install_skills.py'),str(self.target)],stdout=subprocess.PIPE,text=True)
        try:
            self.assertEqual(proc.stdout.readline().strip(),'locked')
            with self.assertRaises(ValueError):self.install(recover=True)
        finally:
            proc.kill();proc.wait();proc.stdout.close()
        self.assertTrue((self.target/m.LOCK).exists())
        self.install();self.assertTrue((self.target/'tdd').is_dir())
