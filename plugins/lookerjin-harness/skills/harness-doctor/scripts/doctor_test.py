#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('doctor.py')


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.put('.codex-plugin/plugin.json', json.dumps(dict(name='fixture', version='1', skills='./skills/')))
        self.put('skills/example/SKILL.md', '---\nname: example\ndescription: Example workflow\n---\n')
        self.put('README.md', '[Example](skills/example/SKILL.md)\n')

    def put(self, relative, content):
        path = self.root/relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)

    def run_doctor(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), '--json'],
                                capture_output=True, text=True)
        data = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0 if data['status'] == 'pass' else 1)
        return data

    def test_valid_fixture(self):
        self.assertEqual(self.run_doctor()['errors'], [])

    def test_active_broken_reference_fails(self):
        with (self.root/'skills/example/SKILL.md').open('a') as stream:
            stream.write('[helper](scripts/missing.py)\n')
        self.assertIn('LOCAL_LINK', [x['code'] for x in self.run_doctor()['errors']])

    def test_historical_broken_reference_warns(self):
        self.put('docs/history.md', '[old](removed.txt)')
        result = self.run_doctor()
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['warnings'][0]['code'], 'LOCAL_LINK')

    def test_missing_or_malformed_skill(self):
        (self.root/'skills/hidden').mkdir()
        self.assertIn('UNDISCOVERABLE_SKILL', [x['code'] for x in self.run_doctor()['errors']])
        self.put('skills/hidden/SKILL.md', 'No metadata')
        self.assertIn('FRONTMATTER', [x['code'] for x in self.run_doctor()['errors']])

    def test_catalog_drift_fails(self):
        self.put('README.md', '# Empty catalog')
        self.assertIn('SKILL_CATALOG', [x['code'] for x in self.run_doctor()['errors']])

    def test_private_evolution_requires_both_adapters(self):
        skill = '---\nname: harness-evolve\ndescription: Explicit evolution\n'
        self.put('skills/harness-evolve/SKILL.md', skill+'---\n')
        with (self.root/'README.md').open('a') as stream:
            stream.write('[Evolve](skills/harness-evolve/SKILL.md)\n')
        self.assertEqual(sum(x['code']=='PRIVATE_EVOLUTION' for x in self.run_doctor()['errors']), 2)
        self.put('skills/harness-evolve/SKILL.md', skill+'disable-model-invocation: true\n---\n')
        self.put('skills/harness-evolve/agents/openai.yaml', 'policy:\n  allow_implicit_invocation: false\n')
        self.assertEqual(self.run_doctor()['status'], 'pass')
        self.put('skills/harness-evolve/agents/openai.yaml', 'policy:\n  allow_implicit_invocation: true\n')
        self.assertEqual(self.run_doctor()['status'], 'fail')

    def test_python_syntax_and_manifest_escape(self):
        self.put('skills/example/scripts/bad.py', 'def incomplete(')
        self.assertIn('SCRIPT_SYNTAX', [x['code'] for x in self.run_doctor()['errors']])
        self.put('.codex-plugin/plugin.json', json.dumps(dict(name='fixture', version='1', skills='./../')))
        self.assertIn('PLUGIN_PATH', [x['code'] for x in self.run_doctor()['errors']])


if __name__ == '__main__':
    unittest.main()
