#!/usr/bin/env python3
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('check-evidence.py')
spec = importlib.util.spec_from_file_location('evidence', SCRIPT)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, content in [('app.py', 'print(42)'), ('run.log', '42\n')]:
            (self.root/name).write_text(content)
        def entry(name):
            return dict(path=name, sha256=hashlib.sha256((self.root/name).read_bytes()).hexdigest())
        self.item = dict(id='answer', criterion='returns 42', surface='CLI', conditions='no args',
                         action='python app.py', expected='42', observed='42', environment='isolated fixture',
                         observed_at='2026-10-23T00:00:00Z', boundaries=[], status='VERIFIED',
                         inputs=[entry('app.py')], artifacts=[entry('run.log')])
        self.record = dict(version=1, records=[self.item])

    def check(self):
        return module.check(self.record, self.root, ['answer'])

    def test_valid_records_do_not_claim_behavior_proof(self):
        result = self.check()
        self.assertTrue(result['accepted_records'])
        self.assertFalse(result['behavior_verified_by_checker'])

    def test_changed_input_invalidates_even_without_commit_change(self):
        (self.root/'app.py').write_text('print(43)')
        self.assertIn('stale', ' '.join(self.check()['errors']))

    def test_changed_and_deleted_evidence(self):
        (self.root/'run.log').write_text('different')
        self.assertEqual(self.check()['status'], 'fail')
        (self.root/'run.log').unlink()
        self.assertEqual(self.check()['status'], 'fail')

    def test_missing_required_and_duplicate_acceptance(self):
        self.assertEqual(module.check(self.record, self.root, ['other'])['status'], 'fail')
        self.record['records'].append(copy.deepcopy(self.item))
        self.assertIn('duplicate', ' '.join(self.check()['errors']))

    def test_failure_not_run_and_inconclusive_are_not_pass(self):
        for status, reason in [('NOT_VERIFIED', 'FAILED'), ('NOT_VERIFIED', 'NOT_RUN'),
                               ('INCONCLUSIVE', 'wrong instance')]:
            self.item.update(status=status, reason=reason)
            result = self.check()
            self.assertEqual(result['errors'], [])
            self.assertEqual(result['unresolved'], ['answer'])
            self.assertEqual(result['status'], 'fail')

    def test_verified_needs_input_and_artifact(self):
        for field in ('inputs', 'artifacts'):
            old = self.item[field]; self.item[field] = []
            self.assertEqual(self.check()['status'], 'fail')
            self.item[field] = old

    def test_escape_and_absolute_paths_rejected(self):
        for raw in ('../run.log', '/tmp/run.log', 'x/../../run.log', 'x\\run.log'):
            self.item['artifacts'][0]['path'] = raw
            self.assertIn('unsafe', ' '.join(self.check()['errors']))

    def test_symlink_and_symlink_parent_rejected(self):
        (self.root/'link').symlink_to(self.root/'run.log')
        self.item['artifacts'][0]['path'] = 'link'
        self.assertIn('symlink', ' '.join(self.check()['errors']))
        (self.root/'dirlink').symlink_to(self.root, target_is_directory=True)
        self.item['artifacts'][0]['path'] = 'dirlink/run.log'
        self.assertIn('symlink', ' '.join(self.check()['errors']))

    def test_duplicate_file_and_invalid_digest(self):
        self.item['artifacts'].append(copy.deepcopy(self.item['artifacts'][0]))
        self.assertIn('duplicate', ' '.join(self.check()['errors']))
        self.item['artifacts'] = [dict(path='run.log', sha256='abc')]
        self.assertIn('sha256', ' '.join(self.check()['errors']))

    def test_schema_and_timezone_required(self):
        for field, value in [('observed_at', 'yesterday'), ('observed_at', '2026-10-23T00:00:00'),
                             ('observed', ''), ('environment', ''), ('status', []), ('inputs', None)]:
            saved = copy.deepcopy(self.item); self.item[field] = value
            self.assertEqual(self.check()['status'], 'fail', field)
            self.item.clear(); self.item.update(saved)
        for record in (None, [], {}, {'version': 1, 'records': [None]}):
            self.assertEqual(module.check(record, self.root, ['answer'])['status'], 'fail')
        self.assertEqual(module.check(self.record, self.root, [])['status'], 'fail')

    def test_unrelated_changes_do_not_invalidate_declared_inputs(self):
        (self.root/'unrelated.txt').write_text('not in this acceptance dependency set')
        self.assertEqual(self.check()['status'], 'pass')

    def test_actual_caller_run_then_code_change(self):
        result = subprocess.run([sys.executable, str(self.root/'app.py')], capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stdout.strip()), (0, '42'))
        (self.root/'run.log').write_text(result.stdout)
        self.item['artifacts'][0]['sha256'] = hashlib.sha256(result.stdout.encode()).hexdigest()
        self.assertEqual(self.check()['status'], 'pass')
        (self.root/'app.py').write_text('print(43)')
        changed = subprocess.run([sys.executable, str(self.root/'app.py')], capture_output=True, text=True)
        self.assertEqual(changed.stdout.strip(), '43')
        self.assertEqual(self.check()['status'], 'fail')

    def test_cli_exit_and_no_mutation(self):
        path = self.root/'records.json'; path.write_text(json.dumps(self.record))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        command = [sys.executable, str(SCRIPT), str(path), '--root', str(self.root), '--require', 'answer']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)
        (self.root/'app.py').write_text('print(99)')
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
