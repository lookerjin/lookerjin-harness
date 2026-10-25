#!/usr/bin/env python3
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).with_name('code-map.py')
spec = importlib.util.spec_from_file_location('code_map', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo'
        (self.root / 'src').mkdir(parents=True)
        for path, content in {
            'entry.js': "import {work} from './barrel.js'; work();\n",
            'barrel.js': "export {work} from './worker.js';\n",
            'worker.js': "import {value} from './shared.js'; export function work(){return value;}\n",
            'shared.js': 'export const value = 42;\n',
            'decoy.js': "export const text = 'shared.js';\n",
        }.items():
            (self.root / 'src' / path).write_text(content)
        self.graph = dict(version=1, baseline=mod.snapshot(self.root, ['src']),
                          nodes=[dict(id=p, label=p, path=p) for p in ['src/entry.js', 'src/barrel.js']],
                          edges=[dict(source='src/entry.js', target='src/barrel.js', kind='imports',
                                      basis='static', evidence=[dict(path='src/entry.js')])],
                          limitations=mod.LIMITS)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args, '--root', str(self.root)],
                              capture_output=True, text=True)

    def save(self):
        path = self.base / 'map.json'
        path.write_text(json.dumps(self.graph))
        return str(path)

    def test_cli_record_query_and_drawio_same_relations(self):
        self.graph['edges'][0].update(kind='calls', basis='observed', acceptance_ids=['entry-result'])
        self.graph['edges'][0]['evidence'][0]['line'] = 1
        source = self.save()
        sealed = self.base / 'sealed.json'
        self.assertEqual(self.cli('record', '--input', source, '--output', str(sealed)).returncode, 0)
        args = ['--input', str(sealed), '--node', 'src/barrel.js', '--direction', 'in']
        result = self.cli('query', *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        view = json.loads(result.stdout)
        self.assertEqual(view['edges'][0]['acceptance_ids'], ['entry-result'])
        self.assertFalse(view['behavior_verified'])
        xml = ET.fromstring(self.cli('drawio', *args).stdout)
        self.assertEqual(len(xml.findall('.//object')), len(view['edges']))
        self.assertEqual(len(xml.findall('.//mxCell[@vertex="1"]')) - 1, len(view['nodes']))
        ids = {n.attrib['id'] for n in xml.findall('.//mxCell[@vertex="1"]')}
        for e in xml.findall('.//mxCell[@edge="1"]'):
            self.assertIn(e.attrib['source'], ids)
            self.assertIn(e.attrib['target'], ids)

    def test_uncommitted_edit_blocks_export_and_marks_query(self):
        path = self.save()
        (self.root / 'src/entry.js').write_text('changed')
        result = self.cli('query', '--input', path, '--node', 'src/entry.js')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['freshness']['changed'], ['src/entry.js'])
        self.assertEqual(self.cli('drawio', '--input', path, '--node', 'src/entry.js').returncode, 1)

    def test_added_caller_and_deleted_module_invalidate(self):
        (self.root / 'src/new.js').write_text("import './entry.js'")
        (self.root / 'src/barrel.js').unlink()
        state = mod.freshness(self.root, self.graph['baseline'])
        self.assertEqual(state['added'], ['src/new.js'])
        self.assertEqual(state['deleted'], ['src/barrel.js'])

    def test_outside_scope_edit_does_not_invalidate(self):
        (self.root / 'notes.md').write_text('unrelated')
        self.assertEqual(mod.freshness(self.root, self.graph['baseline'])['status'], 'current')

    def test_git_commit_change_with_identical_scope_is_current(self):
        mod.run(['git', 'init', '-q'], self.root)
        mod.run(['git', 'add', '.'], self.root)
        commit = ['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm']
        mod.run(commit + ['initial'], self.root)
        baseline = mod.snapshot(self.root, ['src'])
        (self.root / 'notes.md').write_text('other scope')
        mod.run(['git', 'add', '.'], self.root)
        mod.run(commit + ['notes'], self.root)
        state = mod.freshness(self.root, baseline)
        self.assertNotEqual(state['built_at_commit'], state['current_commit'])
        self.assertEqual(state['status'], 'current')
        (self.root / 'src/new.js').write_text('untracked')
        self.assertEqual(mod.freshness(self.root, baseline)['status'], 'stale')

    def test_invalid_relations_and_missing_citations_rejected(self):
        for field, value in [('target', 'unknown'), ('kind', 'dependency'), ('basis', 'verified'), ('evidence', [])]:
            draft = copy.deepcopy(self.graph)
            draft['edges'][0][field] = value
            with self.assertRaises(ValueError):
                mod.validate(draft, self.root)
        self.graph['edges'][0]['kind'] = 'calls'
        with self.assertRaises(ValueError):
            mod.validate(self.graph, self.root)

    def test_symlink_and_path_escape_rejected(self):
        for path in ['../outside', '/etc/passwd', 'src/../../outside']:
            with self.assertRaises(ValueError):
                mod.snapshot(self.root, [path])
        (self.root / 'src/link.js').symlink_to(self.root / 'src/entry.js')
        with self.assertRaises(ValueError):
            mod.snapshot(self.root, ['src'])

    def test_no_overwrite_or_self_invalidating_output(self):
        source = self.save()
        self.assertEqual(self.cli('record', '--input', source, '--output', source).returncode, 1)
        self.assertEqual(self.cli('record', '--input', source, '--output', str(self.root / 'src/map.json')).returncode, 1)
        self.assertEqual(json.loads(Path(source).read_text()), self.graph)

    def test_depth_direction_cycles_and_truncation(self):
        self.graph['edges'].append(dict(source='src/barrel.js', target='src/entry.js', kind='imports',
                                       basis='static', evidence=[dict(path='src/barrel.js')]))
        view = mod.query(self.graph, 'src/barrel.js', 'in', 2, 1)
        self.assertTrue(view['truncated'])
        self.assertEqual(view['omitted_edges'], 1)
        self.assertEqual(len(mod.query(self.graph, 'src/barrel.js', 'in', 0, 40)['edges']), 0)
        self.assertEqual(len(mod.query(self.graph, 'src/barrel.js', 'in', 2, 40, 'calls')['edges']), 0)

    def test_missing_extractor_is_explicit_failure(self):
        result = self.cli('build', '--scope', 'src', '--extractor', str(self.base / 'absent'))
        self.assertEqual(result.returncode, 1)
        self.assertIn('error', json.loads(result.stderr))

    def test_record_rejects_nonexistent_source_line(self):
        self.graph['edges'][0]['evidence'][0]['line'] = 999
        self.assertEqual(self.cli('record', '--input', self.save()).returncode, 1)

    def test_budget_keeps_nearest_relationship_first(self):
        self.graph['nodes'].append(dict(id='src/worker.js', label='Worker', path='src/worker.js'))
        self.graph['edges'].insert(0, dict(source='src/barrel.js', target='src/worker.js', kind='imports',
                                          basis='static', evidence=[dict(path='src/barrel.js')]))
        view = mod.query(self.graph, 'src/entry.js', 'out', 3, 1)
        self.assertEqual(view['edges'][0]['source'], 'src/entry.js')
        self.assertTrue(view['truncated'])

    @unittest.skipUnless(os.environ.get('DEPCRUISE'), 'optional JS extractor not installed')
    def test_real_extractor_finds_indirect_importers_without_string_false_positive(self):
        graph = mod.build(self.root, ['src'], os.environ['DEPCRUISE'])
        view = mod.query(graph, 'src/shared.js', 'in', 3, 40)
        self.assertEqual({n['id'] for n in view['nodes']},
                         {'src/entry.js', 'src/barrel.js', 'src/worker.js', 'src/shared.js'})
        self.assertEqual(len(view['edges']), 3)
        self.assertTrue(all(e['kind'] == 'imports' for e in view['edges']))

    @unittest.skipUnless(os.environ.get('DEPCRUISE'), 'optional JS extractor not installed')
    def test_real_extractor_reports_unresolved_import(self):
        (self.root / 'src/entry.js').write_text("import './absent.js';\n")
        graph = mod.build(self.root, ['src'], os.environ['DEPCRUISE'])
        self.assertIn('./absent.js', graph['unresolved'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
