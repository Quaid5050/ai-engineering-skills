"""Executable persistence/lease example, not a production scheduler or provider guarantee."""
import hashlib
import json
import sqlite3


class Outbox:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=5)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('CREATE TABLE IF NOT EXISTS work (tenant TEXT, op TEXT, fingerprint TEXT, state TEXT, token TEXT, lease_until INTEGER, PRIMARY KEY(tenant, op))')
        self.db.commit()

    def enqueue(self, tenant, op, payload):
        fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO work VALUES (?, ?, ?, 'pending', NULL, NULL)", (tenant, op, fingerprint))
            row = self.db.execute('SELECT fingerprint FROM work WHERE tenant=? AND op=?', (tenant, op)).fetchone()
            if row[0] != fingerprint:
                raise ValueError('operation identity reused with a different payload')

    def claim(self, tenant, op, token, now, ttl):
        with self.db:
            result = self.db.execute("UPDATE work SET state='leased', token=?, lease_until=? WHERE tenant=? AND op=? AND (state='pending' OR (state='leased' AND lease_until<=?))", (token, now+ttl, tenant, op, now))
            return result.rowcount == 1

    def acknowledge(self, tenant, op, token, now):
        with self.db:
            result = self.db.execute("UPDATE work SET state='acknowledged', token=NULL, lease_until=NULL WHERE tenant=? AND op=? AND state='leased' AND token=? AND lease_until>?", (tenant, op, token, now))
            return result.rowcount == 1

    def state(self, tenant, op):
        row = self.db.execute('SELECT state FROM work WHERE tenant=? AND op=?', (tenant, op)).fetchone()
        return row[0] if row else None

    def close(self):
        self.db.close()


class IdempotentProviderFixture:
    """Persistent fixture modeling a provider with an unlimited dedupe horizon.

    Real providers may have limited horizons or lack this contract entirely.
    """
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=5)
        self.db.execute('CREATE TABLE IF NOT EXISTS accepted (tenant TEXT, op TEXT, PRIMARY KEY(tenant, op))')
        self.db.commit()

    def send(self, tenant, op):
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO accepted VALUES (?, ?)', (tenant, op))
        return 'accepted'

    def count(self):
        return self.db.execute('SELECT count(*) FROM accepted').fetchone()[0]

    def close(self):
        self.db.close()
