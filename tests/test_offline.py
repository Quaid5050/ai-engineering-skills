import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('queue_fixture',Path(__file__).resolve().parents[1]/'examples/offline-state/queue.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class OfflineTests(unittest.TestCase):
    def test_restart_invalid_and_account_quarantine(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'queue.db';q=m.Queue(path)
            q.enqueue('a','one','synthetic');q.invalid('a','one');q.close()
            q=m.Queue(path);self.assertEqual(q.retained(),[('a','one','needs-attention')])
            q.enqueue('a','two','synthetic-2');q.sign_out('a');q.enqueue('b','one','other');q.close()
            q=m.Queue(path);self.addCleanup(q.close)
            self.assertEqual(q.pending('a'),[]);self.assertEqual(q.pending('b'),[('one','other')])
            self.assertEqual(len(q.retained()),3)
            with self.assertRaises(ValueError):q.discard('a','one')
            q.discard('a','one',True);self.assertEqual(len(q.retained()),2)
    def test_payload_collision_and_write_failure_are_visible(self):
        with tempfile.TemporaryDirectory() as d:
            q=m.Queue(Path(d)/'queue.db');self.addCleanup(q.close)
            q.enqueue('a','one','first')
            with self.assertRaises(ValueError):q.enqueue('a','one','changed')
            q.db.execute('PRAGMA query_only=ON')
            with self.assertRaises(sqlite3.OperationalError):q.enqueue('a','two','unsaved')
            self.assertEqual(q.pending('a'),[('one','first')])
