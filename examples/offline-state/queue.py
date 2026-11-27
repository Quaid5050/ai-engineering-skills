"""Synthetic SQLite state fixture; add platform encryption/keystore before real use."""
import sqlite3

class Queue:
    def __init__(self,path):
        self.db=sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS queue(account TEXT, operation TEXT, payload TEXT, state TEXT, PRIMARY KEY(account,operation))")
        self.db.commit()
    def close(self): self.db.close()
    def enqueue(self,account,operation,payload):
        with self.db:
            row=self.db.execute('SELECT payload FROM queue WHERE account=? AND operation=?',(account,operation)).fetchone()
            if row and row[0]!=payload: raise ValueError('operation payload conflict')
            self.db.execute("INSERT OR IGNORE INTO queue VALUES(?,?,?,'pending')",(account,operation,payload))
    def invalid(self,account,operation):
        with self.db:self.db.execute("UPDATE queue SET state='needs-attention' WHERE account=? AND operation=?",(account,operation))
    def sign_out(self,account):
        # Authentication revocation belongs to the caller; do not delay it for queue flush.
        with self.db:self.db.execute("UPDATE queue SET state='quarantined' WHERE account=?",(account,))
    def pending(self,account):
        return self.db.execute("SELECT operation,payload FROM queue WHERE account=? AND state='pending' ORDER BY operation",(account,)).fetchall()
    def retained(self):return self.db.execute('SELECT account,operation,state FROM queue ORDER BY account,operation').fetchall()
    def discard(self,account,operation,confirmed=False):
        if not confirmed:raise ValueError('explicit discard required')
        with self.db:self.db.execute('DELETE FROM queue WHERE account=? AND operation=?',(account,operation))
