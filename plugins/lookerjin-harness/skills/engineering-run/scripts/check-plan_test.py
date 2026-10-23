#!/usr/bin/env python3
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('check-plan.py')
spec = importlib.util.spec_from_file_location('plan', SCRIPT)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


def unit(key, dependencies=()):
    return dict(id=key, goal='Preserve caller behavior', scope=[key+'.py'],
                context=['public API baseline'], acceptance=['return and side effects match'],
                verify=['run caller fixture'], depends_on=list(dependencies), status='pending')


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = dict(version=1, units=[unit('a'), unit('b', ['a']), unit('c')])

    def test_frontier_changes_after_verified_dependency(self):
        self.assertEqual(module.check(self.plan)['ready'], ['a', 'c'])
        self.plan['units'][0].update(status='verified', evidence=['run.log'])
        self.assertEqual(module.check(self.plan)['ready'], ['b', 'c'])

    def test_cycle_and_self_dependency(self):
        for deps in (['b'], ['a']):
            self.plan['units'][0]['depends_on'] = deps
            self.assertIn('cycle', ' '.join(module.check(self.plan)['errors']))

    def test_unknown_duplicate_ids_and_dependencies(self):
        for mutation in (lambda p: p['units'][1].update(depends_on=['missing']),
                         lambda p: p['units'][1].update(id='a'),
                         lambda p: p['units'][1].update(depends_on=['a', 'a'])):
            plan = copy.deepcopy(self.plan); mutation(plan)
            self.assertEqual(module.check(plan)['status'], 'fail')

    def test_active_and_verified_cannot_bypass_dependency(self):
        for status in ('active', 'verified'):
            self.plan['units'][1].update(status=status, evidence=['b.log'])
            self.assertEqual(module.check(self.plan)['status'], 'fail')

    def test_invalid_fields_fail_without_traceback(self):
        for field, value in [('status', []), ('goal', ''), ('scope', []), ('acceptance', []),
                             ('verify', 'test'), ('depends_on', None), ('context', [])]:
            plan = copy.deepcopy(self.plan); plan['units'][0][field] = value
            self.assertEqual(module.check(plan)['status'], 'fail', field)
        for value in (None, [], {}, {'version': True, 'units': []}, {'version': 1, 'units': [None]}):
            self.assertEqual(module.check(value)['status'], 'fail')

    def test_blocked_is_not_ready_and_requires_reason(self):
        self.plan['units'][0]['status'] = 'blocked'
        self.assertEqual(module.check(self.plan)['status'], 'fail')
        self.plan['units'][0]['blocker'] = 'Needs device observation'
        self.assertEqual(module.check(self.plan)['ready'], ['c'])

    def test_verified_needs_evidence_and_shared_scope_is_reported(self):
        self.plan['units'][0]['status'] = 'verified'
        self.assertEqual(module.check(self.plan)['status'], 'fail')
        self.plan['units'][0]['status'] = 'pending'
        self.plan['units'][2]['scope'] = ['a.py']
        self.assertEqual(module.check(self.plan)['scope_overlaps'][0]['units'], ['a', 'c'])

    def test_large_acyclic_plan(self):
        units = [unit(str(i), [str(i-1)] if i else []) for i in range(1500)]
        self.assertEqual(module.check(dict(version=1, units=units))['ready'], ['0'])

    def test_cli_exit_and_no_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'plan.json'; path.write_text(json.dumps(self.plan))
            before = path.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['ready'], ['a', 'c'])
            self.assertEqual(path.read_bytes(), before)
            path.write_text('{')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True)
            self.assertEqual(result.returncode, 1)


if __name__ == '__main__':
    unittest.main()
