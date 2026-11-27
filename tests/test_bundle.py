import importlib.util
from pathlib import Path
import tarfile
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bundle',ROOT/'scripts/build_bundle.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class BundleTests(unittest.TestCase):
    def test_reproducible_package_contains_supporting_resources(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.tar.gz';b=Path(d)/'b.tar.gz';m.build(a);m.build(b)
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with tarfile.open(a) as archive:
                names=archive.getnames()
                self.assertIn('catalog/skills.json',names)
                self.assertIn('plugins/ai/skills/rag-pipeline/references/implementation.md',names)
                self.assertFalse(any(name.startswith('/') or '..' in Path(name).parts for name in names))
