import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('checker',ROOT/'scripts/check.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

class MetadataTests(unittest.TestCase):
    def setUp(self):checker.errors.clear()
    def parse(self,front):return checker.parse_frontmatter('---\n'+front+'\n---\nbody\n','fixture')
    def test_valid(self):self.assertEqual(self.parse('name: demo\ndescription: Use when needed')[0]['name'],'demo')
    def test_invalid_or_duplicate_rejected(self):
        for front in ('name: first\nname: second','description: "unclosed','name: [a]','metadata: {version: 1}', 'name: &x demo\ndescription: *x','name: !!python/object/apply:os.system [echo]'):
            with self.subTest(front=front):self.assertIsNone(self.parse(front))
    def test_error_does_not_echo_secret_or_sensitive_filename(self):
        secret='AK'+'IA'+'Z'*16
        self.assertIsNone(checker.parse_frontmatter('---\ndescription: "'+secret+'\n---\n',secret))
        self.assertNotIn(secret,' '.join(checker.errors))
    def test_multiline_description(self):
        result=self.parse('name: demo\ndescription: >\n  Use when writing\n  a task.')
        self.assertIn('writing a task',result[0]['description'])
    def test_catalog_malformed_shapes_fail_cleanly(self):
        import json
        original=checker.ROOT
        with tempfile.TemporaryDirectory() as d:
            checker.ROOT=Path(d);(checker.ROOT/'catalog').mkdir()
            try:
                for data in ({'schema_version':1,'skills':[{'name':[]}]}, {'schema_version':True,'skills':[]}, {'schema_version':1,'skills':['bad']}):
                    (checker.ROOT/'catalog/skills.json').write_text(json.dumps(data));checker.errors.clear()
                    checker.check_catalog();self.assertTrue(checker.errors)
            finally:checker.ROOT=original
