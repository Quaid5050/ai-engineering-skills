"""Executable cohort/freshness counterexamples; adapt syntax to the target engine."""
import sqlite3
import unittest
class QueryTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:');self.addCleanup(self.db.close)
        self.db.executescript('CREATE TABLE owners(id TEXT,active INTEGER); CREATE TABLE events(owner TEXT,kind TEXT,at INTEGER);')
    def test_freshness_includes_never_seen_active_owner(self):
        self.db.executemany('INSERT INTO owners VALUES(?,?)',[('fresh',1),('stale',1),('never',1),('inactive',0)])
        self.db.executemany('INSERT INTO events VALUES(?,?,?)',[('fresh','sync',95),('stale','sync',10)])
        rows=self.db.execute("SELECT o.id FROM owners o LEFT JOIN events e ON e.owner=o.id AND e.kind='sync' WHERE o.active=1 GROUP BY o.id HAVING MAX(e.at) IS NULL OR MAX(e.at)<90 ORDER BY o.id").fetchall()
        self.assertEqual(rows,[('never',),('stale',)])
    def test_conversion_must_follow_first_ever_cohort_entry(self):
        self.db.executemany('INSERT INTO events VALUES(?,?,?)',[('old','start',1),('old','start',100),('new','start',100),('new','convert',90),('valid','start',100),('valid','convert',110)])
        rows=self.db.execute("WITH first AS (SELECT owner,MIN(at) AS entered FROM events WHERE kind='start' GROUP BY owner) SELECT f.owner FROM first f WHERE f.entered>=100 AND f.entered<200 AND EXISTS(SELECT 1 FROM events e WHERE e.owner=f.owner AND e.kind='convert' AND e.at>=f.entered AND e.at<f.entered+30)").fetchall()
        self.assertEqual(rows,[('valid',)])
