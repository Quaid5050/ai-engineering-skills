import importlib.util
from pathlib import Path
import tempfile
import threading
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('outbox', ROOT/'examples/durable-delivery/outbox.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'outbox.db';self.provider_path=Path(self.tmp.name)/'provider.db'

    def test_crash_before_send_retains_pending_work(self):
        first=mod.Outbox(self.path);first.enqueue('tenant-a','order-a',{'amount':20})
        self.assertTrue(first.claim('tenant-a','order-a','old',0,10));first.close()
        restarted=mod.Outbox(self.path);self.addCleanup(restarted.close)
        self.assertFalse(restarted.claim('tenant-a','order-a','new',9,10))
        self.assertTrue(restarted.claim('tenant-a','order-a','new',10,10))
        self.assertEqual(restarted.state('tenant-a','order-a'),'leased')

    def test_lost_ack_replay_and_genuine_second_operation(self):
        first=mod.Outbox(self.path);first.enqueue('tenant-a','order-a',{'amount':20})
        first.claim('tenant-a','order-a','old',0,10)
        provider=mod.IdempotentProviderFixture(self.provider_path);provider.send('tenant-a','order-a')
        first.close();provider.close()  # acceptance persisted, local acknowledgement lost
        restarted=mod.Outbox(self.path);self.addCleanup(restarted.close)
        provider=mod.IdempotentProviderFixture(self.provider_path);self.addCleanup(provider.close)
        self.assertTrue(restarted.claim('tenant-a','order-a','new',10,10))
        provider.send('tenant-a','order-a')
        self.assertTrue(restarted.acknowledge('tenant-a','order-a','new',11))
        self.assertEqual(provider.count(),1)
        restarted.enqueue('tenant-a','order-b',{'amount':20});provider.send('tenant-a','order-b')
        self.assertEqual(provider.count(),2)

    def test_stale_owner_cannot_acknowledge(self):
        db=mod.Outbox(self.path);self.addCleanup(db.close);db.enqueue('a','x',{})
        db.claim('a','x','old',0,2);db.claim('a','x','new',2,10)
        self.assertFalse(db.acknowledge('a','x','old',3))
        self.assertTrue(db.acknowledge('a','x','new',3))

    def test_concurrent_claims_one_owner(self):
        db=mod.Outbox(self.path);db.enqueue('a','x',{});db.close()
        gate=threading.Barrier(2);results=[];errors=[]
        def worker(token):
            try:
                store=mod.Outbox(self.path)
                try:
                    gate.wait(timeout=5);results.append(store.claim('a','x',token,0,10))
                finally:store.close()
            except Exception as error:errors.append(error)
        threads=[threading.Thread(target=worker,args=(t,)) for t in ('one','two')]
        for t in threads:t.start()
        for t in threads:t.join(timeout=10)
        self.assertFalse(any(t.is_alive() for t in threads));self.assertEqual(errors,[])
        self.assertEqual(sorted(results),[False,True])

    def test_tenant_identity_and_changed_payload(self):
        db=mod.Outbox(self.path);self.addCleanup(db.close)
        db.enqueue('a','x',{'value':1});db.enqueue('b','x',{'value':2})
        with self.assertRaises(ValueError):db.enqueue('a','x',{'value':2})
        self.assertEqual(db.state('a','x'),'pending');self.assertIsNone(db.state('c','x'))
