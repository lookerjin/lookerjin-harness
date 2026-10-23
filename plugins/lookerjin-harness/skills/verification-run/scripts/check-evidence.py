#!/usr/bin/env python3
"""Check evidence records and local fingerprints, never infer behavioral truth."""
import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath

DIGEST = re.compile(r'^[a-f0-9]{64}$')


def text(value):
    return isinstance(value, str) and bool(value.strip())


def files(entries, root, label, errors, required):
    if not isinstance(entries, list) or (required and not entries):
        errors.append(f'{label}: expected {"nonempty " if required else ""}array'); return
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or not text(entry.get('path')):
            errors.append(f'{label}: expected path and sha256'); continue
        raw, digest = entry['path'], entry.get('sha256')
        relative = PurePosixPath(raw)
        if (relative.is_absolute() or '..' in relative.parts or '\\' in raw
                or not relative.parts or any(ord(c) < 32 for c in raw)):
            errors.append(f'{label}: unsafe path {raw!r}'); continue
        canonical = relative.as_posix()
        if canonical in seen:
            errors.append(f'{label}: duplicate path {raw}'); continue
        seen.add(canonical)
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            errors.append(f'{label}: invalid sha256 for {raw}'); continue
        path = root.joinpath(*relative.parts)
        if any(parent.is_symlink() for parent in [path, *path.parents] if parent != root and root in parent.parents):
            errors.append(f'{label}: symlink not supported: {raw}'); continue
        if not path.resolve().is_relative_to(root):
            errors.append(f'{label}: path escapes root: {raw}'); continue
        try:
            if not path.is_file():
                raise ValueError('not a regular file')
            with path.open('rb') as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != digest:
                errors.append(f'{label}: stale or changed file: {raw}')
        except (OSError, ValueError) as exc:
            errors.append(f'{label}: {raw}: {exc}')


def check(record, root, required):
    errors, statuses = [], {}
    root = Path(root).resolve()
    if not isinstance(record, dict) or type(record.get('version')) is not int or record.get('version') != 1 or not isinstance(record.get('records'), list):
        return {'status': 'fail', 'errors': ['expected version 1 and records array'], 'accepted_records': False}
    if not root.is_dir():
        errors.append('root must be a directory')
    if not required or not all(text(x) for x in required) or len(set(required)) != len(required):
        errors.append('explicit, nonempty, unique required acceptance ids are mandatory')
    for index, item in enumerate(record['records']):
        if not isinstance(item, dict) or not text(item.get('id')):
            errors.append(f'record {index}: id required'); continue
        key = item['id']
        if key in statuses:
            errors.append(f'duplicate acceptance id: {key}'); continue
        status = item.get('status')
        statuses[key] = status
        if status not in ('VERIFIED', 'NOT_VERIFIED', 'INCONCLUSIVE'):
            errors.append(f'{key}: invalid status')
        for field in ('criterion', 'surface', 'conditions', 'action', 'expected', 'observed', 'environment'):
            if not text(item.get(field)):
                errors.append(f'{key}: {field} required')
        boundaries = item.get('boundaries')
        if not isinstance(boundaries, list) or not all(text(x) for x in boundaries):
            errors.append(f'{key}: boundaries must be an array of strings')
        try:
            date = datetime.fromisoformat(item.get('observed_at', '').replace('Z', '+00:00'))
            if date.utcoffset() is None:
                raise ValueError('timezone required')
        except (ValueError, TypeError, AttributeError):
            errors.append(f'{key}: observed_at must be an ISO timestamp with timezone')
        if status == 'NOT_VERIFIED' and item.get('reason') not in ('FAILED', 'NOT_RUN'):
            errors.append(f'{key}: NOT_VERIFIED requires FAILED or NOT_RUN')
        if status == 'INCONCLUSIVE' and not text(item.get('reason')):
            errors.append(f'{key}: INCONCLUSIVE requires reason')
        files(item.get('inputs'), root, f'{key}.inputs', errors, status == 'VERIFIED')
        files(item.get('artifacts'), root, f'{key}.artifacts', errors, status == 'VERIFIED')
    for key in required:
        if key not in statuses:
            errors.append(f'missing required acceptance: {key}')
    unresolved = [key for key in required if statuses.get(key) != 'VERIFIED']
    accepted = not errors and not unresolved
    return {'status': 'pass' if accepted else 'fail', 'errors': errors,
            'unresolved': unresolved, 'accepted_records': accepted,
            'behavior_verified_by_checker': False,
            'limitations': 'Validates declared records and file hashes only; does not execute actions or prove coverage, environment identity, chronology or semantic truth.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--require', action='append', required=True, dest='required')
    args = parser.parse_args()
    try:
        result = check(json.loads(args.record.read_text()), args.root, args.required)
    except (OSError, ValueError) as exc:
        result = {'status': 'fail', 'errors': [str(exc)], 'accepted_records': False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
