#!/usr/bin/env python3
"""Local plugin distribution checks, including intentionally broken packages."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("marketplace", ROOT / "scripts/validate_marketplace.py")
market = importlib.util.module_from_spec(spec)
spec.loader.exec_module(market)


class DistributionTests(unittest.TestCase):
    def test_copied_skill_and_licenses_match_fixed_record(self):
        root = ROOT / "plugins/frontend-design"
        record = json.loads((root / "SOURCE.json").read_text())
        self.assertEqual(record['commit'], '58267944f92187b7d6a1c822165c96c81c864806')
        self.assertEqual(record['files']['skills/frontend-design/SKILL.md'],
                         'd91970639e9f5c37682ac7ab60094d35f1c7c1f38d731bd56396563aee10c1d3')
        for name, expected in record['files'].items():
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), expected, name)
        skill = (root / 'skills/frontend-design/SKILL.md').read_text()
        self.assertIn('name: frontend-design\n', skill)
        self.assertTrue((root / 'skills/frontend-design/LICENSE.txt').is_file())
        self.assertFalse(list(root.rglob('hooks.json')))
        self.assertFalse((root / 'mcp.json').exists())

    def test_marketplace_exposes_independent_expert(self):
        data = market.load_marketplace()
        market.validate_structure(data)
        entries = [p for p in data['plugins'] if p['name'] == 'frontend-design']
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['source'], {'source': 'local', 'path': './plugins/frontend-design'})
        self.assertEqual(len(list((ROOT / 'plugins/lookerjin-harness/skills').glob('*/SKILL.md'))), 15)

    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        plugin = root / 'plugins/demo'
        (plugin / '.codex-plugin').mkdir(parents=True)
        manifest = plugin / '.codex-plugin/plugin.json'
        manifest.write_text(json.dumps({'name': 'demo', 'skills': './skills/'}))
        (plugin / 'skills/demo').mkdir(parents=True)
        (plugin / 'skills/demo/SKILL.md').write_text('---\nname: demo\ndescription: Example.\n---\n')
        return root, plugin, manifest

    def check(self, root):
        with patch.object(market, 'ROOT', root):
            market.validate_local_source('demo', {'path': './plugins/demo'})

    def test_valid_minimal_skill_package(self):
        root, _, manifest = self.fixture()
        self.check(root)
        manifest.write_text(json.dumps({'name': 'demo', 'skills': ['./skills/demo']}))
        self.check(root)

    def test_malformed_or_nonobject_manifest_rejected(self):
        root, _, manifest = self.fixture()
        for value in ['{broken', '[]', 'null']:
            with self.subTest(value=value):
                manifest.write_text(value)
                with self.assertRaises(market.ValidationError):
                    self.check(root)

    def test_wrong_identity_and_missing_skills_rejected(self):
        root, _, manifest = self.fixture()
        for value in [{'name': 'other'}, {'name': 'demo', 'skills': './missing'},
                      {'name': 'demo', 'skills': {'path': './skills/'}},
                      {'name': 'demo', 'skills': []}]:
            with self.subTest(value=value):
                manifest.write_text(json.dumps(value))
                with self.assertRaises(market.ValidationError):
                    self.check(root)

    def test_escaping_skills_rejected(self):
        root, _, manifest = self.fixture()
        manifest.write_text(json.dumps({'name': 'demo', 'skills': './../../outside'}))
        with self.assertRaises(market.ValidationError):
            self.check(root)

    def test_empty_declared_skill_collection_rejected(self):
        root, plugin, _ = self.fixture()
        (plugin / 'skills/demo/SKILL.md').unlink()
        with self.assertRaises(market.ValidationError):
            self.check(root)

    def test_symlink_manifest_outside_plugin_rejected(self):
        root, _, manifest = self.fixture()
        outside = root / 'manifest.json'
        outside.write_bytes(manifest.read_bytes())
        manifest.unlink()
        manifest.symlink_to(outside)
        with self.assertRaises(market.ValidationError):
            self.check(root)

    def test_symlink_skill_outside_plugin_rejected(self):
        root, plugin, _ = self.fixture()
        outside = root / 'SKILL.md'
        outside.write_text('external')
        skill = plugin / 'skills/demo/SKILL.md'
        skill.unlink()
        skill.symlink_to(outside)
        with self.assertRaises(market.ValidationError):
            self.check(root)


if __name__ == '__main__':
    unittest.main()
