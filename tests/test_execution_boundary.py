"""Opt-in real container boundary test. Run with RUN_CONTAINER_TESTS=1."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

IMAGE = 'python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f5296f51b4b'

@unittest.skipUnless(os.environ.get('RUN_CONTAINER_TESTS') == '1', 'set RUN_CONTAINER_TESTS=1; requires Docker')
class ExecutionBoundaryTests(unittest.TestCase):
    def test_host_denies_writes_egress_and_secret_inheritance(self):
        with tempfile.TemporaryDirectory() as folder:
            fixture=Path(folder); fixture.chmod(0o755)
            (fixture/'input.txt').write_text('synthetic public input')
            code = """
import os, socket
from pathlib import Path
assert Path('/input/input.txt').read_text() == 'synthetic public input'
assert 'SYNTHETIC_HOST_SECRET' not in os.environ
assert not Path('/var/run/docker.sock').exists()
try: assert not Path('/root/.ssh').exists()
except PermissionError: pass  # The non-root process cannot inspect this directory.
for path in ['/input/input.txt', '/forbidden-write']:
    try: Path(path).write_text('denied')
    except OSError: pass
    else: raise AssertionError('write escaped boundary')
try: socket.create_connection(('192.0.2.1', 443), timeout=1)
except OSError: pass
else: raise AssertionError('unexpected egress')
print('boundary controls passed')
"""
            command=['docker','run','--rm','--network=none','--read-only',
                     '--cap-drop=ALL','--security-opt=no-new-privileges',
                     '--pids-limit=32','--memory=128m','--cpus=1','--user=65534:65534',
                     '--mount',f'type=bind,src={fixture},dst=/input,readonly',IMAGE,'python','-c',code]
            result=subprocess.run(command,capture_output=True,text=True,timeout=90,
                                  env={**os.environ,'SYNTHETIC_HOST_SECRET':'synthetic-value'})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('boundary controls passed',result.stdout)
            self.assertEqual((fixture/'input.txt').read_text(),'synthetic public input')
