#!/usr/bin/env python3
"""Bounded navigation records; extraction stays with language-aware tools."""
import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

KINDS = {'imports', 'calls', 'data-flow', 'state-transition', 'verifies'}
SKIP = {'.git', 'node_modules', '.venv', '__pycache__', '.cache'}
LIMITS = ['Scoped navigation only; absence is not proof of no callers.',
          'Dynamic dispatch, generated code and external consumers require separate evidence.',
          'Source fingerprints establish freshness, not semantic correctness or runtime success.']


def run(argv, root):
    return subprocess.run(argv, cwd=root, text=True, capture_output=True,
                          check=True, timeout=120).stdout


def local(root, raw):
    if not isinstance(raw, str) or not raw or '\\' in raw:
        raise ValueError('invalid relative path')
    p = PurePosixPath(raw)
    if p.is_absolute() or '..' in p.parts or p.as_posix() != raw:
        raise ValueError(f'unsafe path: {raw}')
    target = root / raw
    for part in [target, *target.parents]:
        if part == root:
            break
        if part.is_symlink():
            raise ValueError(f'symlink: {raw}')
    target.resolve().relative_to(root)
    return target


def digest(path):
    if path.stat().st_size > 8 * 1024 * 1024:
        raise ValueError(f'file exceeds 8 MiB; narrow scope: {path.name}')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def in_scope(path, scopes):
    return any(s == '.' or path == s or path.startswith(s + '/') for s in scopes)


def snapshot(root, scopes):
    for scope in scopes:
        local(root, scope)
    try:
        # Includes untracked files and respects project ignores. Missing tracked files
        # are omitted so deletion is detected against the previous snapshot.
        paths = run(['git', 'ls-files', '-z', '--cached', '--others',
                     '--exclude-standard', '--', *scopes], root).split('\0')
    except subprocess.CalledProcessError:
        paths = []
        for scope in scopes:
            p = local(root, scope)
            paths.extend(x.relative_to(root).as_posix() for x in
                         ([p] if p.is_file() else p.rglob('*')) if x.is_file())
    paths = sorted({p for p in paths if p and not SKIP.intersection(PurePosixPath(p).parts)})
    if len(paths) > 5000:
        raise ValueError('scope exceeds 5000 files; choose a subsystem')
    files = {}
    for name in paths:
        p = local(root, name)
        if p.is_file():
            files[name] = digest(p)
    try:
        commit = run(['git', 'rev-parse', 'HEAD'], root).strip()
    except subprocess.CalledProcessError:
        commit = None
    return dict(scopes=scopes, files=files, commit=commit)


def freshness(root, baseline):
    now = snapshot(root, baseline['scopes'])
    old, new = baseline['files'], now['files']
    changed = sorted(p for p in old.keys() & new.keys() if old[p] != new[p])
    added, deleted = sorted(new.keys() - old.keys()), sorted(old.keys() - new.keys())
    return dict(status='stale' if changed or added or deleted else 'current',
                changed=changed, added=added, deleted=deleted,
                built_at_commit=baseline['commit'], current_commit=now['commit'],
                scope_only=True)


def validate(graph, root):
    if not isinstance(graph, dict) or not isinstance(graph.get('baseline'), dict):
        raise ValueError('map must be an object with a baseline')
    if graph.get('version') != 1 or not graph.get('baseline', {}).get('scopes'):
        raise ValueError('expected version 1 and a captured baseline')
    for path, sha in graph['baseline']['files'].items():
        local(root, path)
        if not re.fullmatch('[0-9a-f]{64}', sha):
            raise ValueError('invalid source fingerprint')
    if not isinstance(graph.get('limitations'), list) or not graph['limitations']:
        raise ValueError('limitations are required')
    nodes = {}
    for n in graph['nodes']:
        if not isinstance(n['id'], str) or not n['id'] or n['id'] in nodes:
            raise ValueError('empty or duplicate node id')
        if not isinstance(n['label'], str):
            raise ValueError('node label must be text')
        if not n.get('boundary', False):
            if n['path'] not in graph['baseline']['files']:
                raise ValueError('node missing from source baseline')
        nodes[n['id']] = n
    for e in graph['edges']:
        if e['source'] not in nodes or e['target'] not in nodes or e['kind'] not in KINDS:
            raise ValueError('unknown endpoint or relation kind')
        if e['basis'] not in {'static', 'observed', 'inferred'} or not e.get('evidence'):
            raise ValueError('relation needs evidence and basis')
        for proof in e['evidence']:
            if proof['path'] not in graph['baseline']['files']:
                raise ValueError('evidence missing from source baseline')
            if e['kind'] != 'imports' and (not isinstance(proof.get('line'), int) or proof['line'] < 1):
                raise ValueError('non-import evidence needs a positive source line')
    return graph


def fixed_inputs(root, baseline, destination):
    """Copy exactly the observed bytes, without chasing out-of-scope files."""
    for name, expected in baseline['files'].items():
        data = local(root, name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('source changed while capturing inputs; rebuild')
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    require_current(root, baseline)


def require_current(root, baseline):
    if freshness(root, baseline)['status'] != 'current':
        raise ValueError('source changed before publication; rebuild from current inputs')


def build(root, scopes, executable):
    baseline = snapshot(root, scopes)
    # Resolve before changing cwd to the temporary input copy.
    executable = str((root / executable).resolve()) if '/' in executable or '\\' in executable else shutil.which(executable)
    if not executable:
        raise ValueError('extractor is not available on PATH')
    pattern = '|'.join('^' + re.escape(s) + r'(?:/|$)' for s in scopes) if '.' not in scopes else '.'
    # include-only discards unresolved imports before we can report them. Stop
    # traversal at the scope boundary instead, retaining those dependency edges.
    stop = '(?:^|/)node_modules/|^(?!(?:' + pattern + '))'
    argv = [executable, '--no-config', '--no-cache', '--output-type', 'json',
            '--do-not-follow', stop, '--', *scopes]
    version = run([executable, '--version'], root).strip()
    with tempfile.TemporaryDirectory(prefix='code-map-inputs-') as temporary:
        frozen = Path(temporary)
        fixed_inputs(root, baseline, frozen)
        raw = json.loads(run(argv, frozen))
        if snapshot(frozen, scopes)['files'] != baseline['files']:
            raise ValueError('extractor modified its input copy; result rejected')
    nodes, edges = {}, []
    for m in raw['modules']:
        path = m['source']
        if path in baseline['files']:
            nodes[path] = dict(id=path, label=path, path=path)
    if not nodes:
        raise ValueError('no supported modules in scope')
    unresolved = []
    for m in raw['modules']:
        if m['source'] not in nodes:
            continue
        for d in m.get('dependencies', []):
            target = d.get('resolved') or d['module']
            if target not in nodes:
                # Boundary IDs cannot collide with local file IDs.
                target = 'boundary:' + target
                nodes.setdefault(target, dict(id=target, label=d['module'], boundary=True))
            if d.get('couldNotResolve'):
                unresolved.append(d['module'])
            edges.append(dict(source=m['source'], target=target, kind='imports', basis='static',
                              evidence=[dict(path=m['source'], specifier=d['module'])]))
    graph = dict(version=1, generated_at=datetime.now(timezone.utc).isoformat(),
                 producer=dict(name='dependency-cruiser', version=version, fixed_inputs=True), baseline=baseline,
                 nodes=list(nodes.values()), edges=edges,
                 limitations=LIMITS + ['Imports are module dependencies, not function calls.',
                 'Only scoped files are copied; external packages and out-of-scope config are not resolved.',
                 'Project executable config is not loaded; aliases/config-dependent resolution may be incomplete.'],
                 unresolved=sorted(set(unresolved)))
    validate(graph, root)
    if freshness(root, baseline)['status'] != 'current':
        raise ValueError('source changed during extraction; rebuild')
    return graph


def query(graph, node, direction, depth, limit, kind=None):
    nodes = {n['id']: n for n in graph['nodes']}
    if node not in nodes:
        raise ValueError('unknown node; use an exact id from the map')
    adjacent = {}
    for index, edge in enumerate(graph['edges']):
        if kind and edge['kind'] != kind:
            continue
        if direction in {'out', 'both'}:
            adjacent.setdefault(edge['source'], []).append((index, edge['target']))
        if direction in {'in', 'both'}:
            adjacent.setdefault(edge['target'], []).append((index, edge['source']))
    pending, visited, selected, seen_edges = deque([(node, 0)]), {node}, [], set()
    while pending:
        current, distance = pending.popleft()
        if distance >= depth:
            continue
        for index, target in adjacent.get(current, []):
            if index not in seen_edges:
                selected.append(index)
                seen_edges.add(index)
            if target not in visited:
                visited.add(target)
                pending.append((target, distance + 1))
    chosen = selected[:limit]
    edges = [graph['edges'][i] for i in chosen]
    keep = {node} | {e[k] for e in edges for k in ('source', 'target')}
    return dict(anchor=node, direction=direction, depth=depth, kind=kind,
                nodes=[nodes[k] for k in sorted(keep)], edges=edges,
                truncated=len(selected) > limit, omitted_edges=len(selected) - len(chosen),
                limitations=graph['limitations'], unresolved=graph.get('unresolved', []),
                behavior_verified=False)


def drawio(view):
    doc = ET.Element('mxfile', host='app.diagrams.net')
    diagram = ET.SubElement(doc, 'diagram', id='navigation', name='Code navigation')
    model = ET.SubElement(diagram, 'mxGraphModel', grid='1', gridSize='10', page='0')
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', id='0')
    ET.SubElement(root, 'mxCell', id='1', parent='0')
    note = (f"{view['anchor']} | 方向 {view['direction']} | 深度 {view['depth']} | "
            f"省略关系 {view['omitted_edges']} | 源码 {view['freshness']['status']}\n"
            '箭头保持原关系方向；虚线表示推断；边界节点位于映射范围外。\n'
            '这是代码导航证据，不代表运行行为已验证。')
    cell = ET.SubElement(root, 'mxCell', id='note', value=note,
                         style='text;html=0;whiteSpace=wrap;align=left;fontSize=14;', vertex='1', parent='1')
    ET.SubElement(cell, 'mxGeometry', x='30', y='20', width='1150', height='100', attrib={'as': 'geometry'})
    # BFS layers give the same local projection as the JSON, including cycles.
    layers, pending = {view['anchor']: 0}, deque([view['anchor']])
    while pending:
        current = pending.popleft()
        for e in view['edges']:
            other = e['target'] if e['source'] == current else e['source'] if e['target'] == current else None
            if other is not None and other not in layers:
                layers[other] = layers[current] + 1
                pending.append(other)
    rows, ids = {}, {}
    for i, n in enumerate(view['nodes']):
        layer = layers.get(n['id'], 0)
        row = rows.get(layer, 0); rows[layer] = row + 1
        ids[n['id']] = 'n' + str(i)
        label = n['label'] + ('\n[范围外边界]' if n.get('boundary') else '')
        cell = ET.SubElement(root, 'mxCell', id=ids[n['id']], value=label,
            style='rounded=1;html=0;whiteSpace=wrap;fillColor=' + ('#fff2cc;' if n.get('boundary') else '#dae8fc;'),
            vertex='1', parent='1')
        ET.SubElement(cell, 'mxGeometry', x=str(30 + layer * 410), y=str(150 + row * 130),
                      width='310', height='85', attrib={'as': 'geometry'})
    for i, e in enumerate(view['edges']):
        evidence = ', '.join(p['path'] + (':' + str(p['line']) if 'line' in p else '') for p in e['evidence'])
        obj = ET.SubElement(root, 'object', id='e' + str(i), label=e['kind'],
                            evidence=evidence, basis=e['basis'],
                            acceptance_ids=json.dumps(e.get('acceptance_ids', []), ensure_ascii=False))
        cell = ET.SubElement(obj, 'mxCell', style='edgeStyle=orthogonalEdgeStyle;html=0;endArrow=block;' +
                             ('dashed=1;' if e['basis'] == 'inferred' else ''), edge='1', parent='1',
                             source=ids[e['source']], target=ids[e['target']])
        ET.SubElement(cell, 'mxGeometry', relative='1', attrib={'as': 'geometry'})
    return ET.tostring(doc, encoding='unicode')


def write_output(path, value, root, scopes, before_publish=None):
    out = Path(path).absolute()
    if out.is_symlink():
        raise ValueError('output must not be a symlink')
    out = out.parent.resolve() / out.name
    try:
        relative = out.relative_to(root).as_posix()
    except ValueError:
        relative = None
    if relative and in_scope(relative, scopes):
        raise ValueError('write map outside observed scopes to avoid self-invalidating snapshots')
    out.parent.mkdir(parents=True, exist_ok=True)
    # A complete same-filesystem staging file is linked into place atomically.
    # link() refuses an existing destination, including a concurrent winner.
    # No direct-write fallback: unsupported filesystems fail without a partial
    # formal output. This does not promise power-loss durability of the directory.
    fd, staged = tempfile.mkstemp(prefix='.code-map-', dir=out.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(value + '\n')
            f.flush()
            os.fsync(f.fileno())
        if before_publish:
            before_publish()
        os.link(staged, out)
    finally:
        os.unlink(staged)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['snapshot', 'build', 'record', 'status', 'query', 'drawio'])
    parser.add_argument('--root', required=True)
    parser.add_argument('--scope', action='append')
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--extractor', default='depcruise')
    parser.add_argument('--node')
    parser.add_argument('--direction', choices=['in', 'out', 'both'], default='both')
    parser.add_argument('--depth', type=int, default=2)
    parser.add_argument('--limit', type=int, default=40)
    parser.add_argument('--kind', choices=sorted(KINDS))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        if not root.is_dir() or not 0 <= args.depth <= 20 or not 1 <= args.limit <= 500:
            raise ValueError('invalid root, depth (0..20), or edge limit (1..500)')
        if args.command in {'snapshot', 'build'}:
            if not args.scope:
                raise ValueError('choose --scope explicitly')
            graph = build(root, args.scope, args.extractor) if args.command == 'build' else dict(
                version=1, baseline=snapshot(root, args.scope), nodes=[], edges=[], limitations=LIMITS)
        else:
            if not args.input:
                raise ValueError('--input required')
            graph = validate(json.loads(Path(args.input).read_text()), root)
        state = freshness(root, graph['baseline'])
        result = graph
        if args.command == 'status':
            result = state
        elif args.command in {'query', 'drawio'}:
            result = query(graph, args.node, args.direction, args.depth, args.limit, args.kind)
            result['freshness'] = state
        if args.command in {'record', 'drawio'} and state['status'] != 'current':
            raise ValueError('stale source; capture and check the affected relations again')
        if args.command == 'record':
            for edge in graph['edges']:
                for proof in edge['evidence']:
                    if 'line' in proof and proof['line'] > len(local(root, proof['path']).read_bytes().splitlines()):
                        raise ValueError('evidence line is outside the source file')
        rendered = drawio(result) if args.command == 'drawio' else json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            guard = None if args.command in {'query', 'status'} else lambda: require_current(root, graph['baseline'])
            write_output(args.output, rendered, root, graph['baseline']['scopes'], guard)
            print(json.dumps(dict(output=args.output, freshness=state['status'])))
        else:
            print(rendered)
        return 2 if state['status'] == 'stale' else 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(error=str(exc)), ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
