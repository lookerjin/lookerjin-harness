#!/usr/bin/env python3
"""Read an optional Unit plan; check structure/dependencies without executing it."""
import argparse
import json
from pathlib import Path

STATUSES = {'pending', 'active', 'verified', 'blocked'}


def strings(value, nonempty=True):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(isinstance(x, str) and x.strip() for x in value))


def check(plan):
    errors, overlaps = [], []
    if not isinstance(plan, dict) or type(plan.get('version')) is not int or plan.get('version') != 1:
        return {'status': 'fail', 'errors': ['expected plan object with version 1'], 'ready': []}
    units = plan.get('units')
    if not isinstance(units, list) or not units:
        return {'status': 'fail', 'errors': ['units must be a nonempty array'], 'ready': []}
    by_id = {}
    for index, unit in enumerate(units):
        if not isinstance(unit, dict):
            errors.append(f'unit {index}: expected object'); continue
        key = unit.get('id')
        if not isinstance(key, str) or not key.strip() or key in by_id:
            errors.append(f'unit {index}: missing or duplicate id'); continue
        by_id[key] = unit
        if not isinstance(unit.get('goal'), str) or not unit['goal'].strip():
            errors.append(f'{key}: goal required')
        for field in ('scope', 'context', 'acceptance', 'verify'):
            if not strings(unit.get(field)):
                errors.append(f'{key}: {field} must be a nonempty array of strings')
        if not strings(unit.get('depends_on'), False):
            errors.append(f'{key}: depends_on must be an array of ids')
        elif len(set(unit['depends_on'])) != len(unit['depends_on']):
            errors.append(f'{key}: duplicate dependency')
        if not isinstance(unit.get('status'), str) or unit['status'] not in STATUSES:
            errors.append(f'{key}: invalid status')
        if unit.get('status') == 'verified' and not strings(unit.get('evidence')):
            errors.append(f'{key}: verified requires evidence references (not proof of their contents)')
        if unit.get('status') == 'blocked' and not isinstance(unit.get('blocker'), str):
            errors.append(f'{key}: blocked requires blocker')
        elif unit.get('status') == 'blocked' and not unit['blocker'].strip():
            errors.append(f'{key}: blocker must not be empty')
    if errors:
        return {'status': 'fail', 'errors': errors, 'ready': []}
    for key, unit in by_id.items():
        for dependency in unit['depends_on']:
            if dependency not in by_id:
                errors.append(f'{key}: unknown dependency {dependency}')
            elif unit['status'] in {'active', 'verified'} and by_id[dependency]['status'] != 'verified':
                errors.append(f'{key}: {unit["status"]} before dependency {dependency} is verified')
    if errors:
        return {'status': 'fail', 'errors': errors, 'ready': []}
    # Kahn traversal avoids recursion limits on large migrations.
    remaining = {key: set(unit['depends_on']) for key, unit in by_id.items()}
    successors = {key: [] for key in by_id}
    for key, deps in remaining.items():
        for dep in deps:
            successors[dep].append(key)
    queue = [key for key, deps in remaining.items() if not deps]
    visited = 0
    while queue:
        key = queue.pop(); visited += 1
        for child in successors[key]:
            remaining[child].discard(key)
            if not remaining[child]:
                queue.append(child)
    if visited != len(by_id):
        errors.append('dependency cycle: ' + ', '.join(key for key, deps in remaining.items() if deps))
    ready = [key for key, unit in by_id.items() if unit['status'] == 'pending'
             and all(by_id[dep]['status'] == 'verified' for dep in unit['depends_on'])]
    # Exact shared scope is a useful signal, not a complete write-conflict detector.
    candidates = [key for key, unit in by_id.items() if key in ready or unit['status'] == 'active']
    for i, left in enumerate(candidates):
        for right in candidates[i + 1:]:
            shared = sorted(set(by_id[left]['scope']) & set(by_id[right]['scope']))
            if shared:
                overlaps.append({'units': [left, right], 'shared_scope': shared})
    return {'status': 'fail' if errors else 'pass', 'errors': errors,
            'ready': [] if errors else ready, 'scope_overlaps': overlaps,
            'limitations': 'Record structure only. Evidence truth, implicit dependencies and write isolation require review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        result = check(json.loads(args.plan.read_text()))
    except (OSError, ValueError) as exc:
        result = {'status': 'fail', 'errors': [str(exc)], 'ready': []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
