#!/usr/bin/env python3
"""Collect deterministic git workspace facts for change-review."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

UNTRACKED_FILE_CAP = 80
UNTRACKED_BYTES_CAP = 256_000


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    output = "\n".join(part for part in (stdout, stderr) if part)
    return proc.returncode, output


def is_probably_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:1024]
    except OSError:
        return False
    return b"\0" in chunk


def untracked_diff(root: Path) -> tuple[int, str]:
    _, listing = run(["git", "ls-files", "--others", "--exclude-standard"], root)
    files = [line for line in listing.splitlines() if line.strip()]
    if not files:
        return 0, ""
    chunks: list[str] = []
    for rel in files[:UNTRACKED_FILE_CAP]:
        path = root / rel
        if not path.is_file():
            chunks.append(f"{rel}  (not a regular file)")
            continue
        size = path.stat().st_size
        if size > UNTRACKED_BYTES_CAP or is_probably_binary(path):
            chunks.append(f"{rel}  {size} bytes  (binary or large; content skipped)")
            continue
        code, output = run(["git", "diff", "--no-index", "--", "/dev/null", rel], root)
        if output:
            chunks.append(output)
        else:
            chunks.append(f"{rel}  {size} bytes  (git diff --no-index produced no output, exit {code})")
    omitted = len(files) - UNTRACKED_FILE_CAP
    if omitted > 0:
        chunks.append(f"... {omitted} more untracked files omitted")
    return 0, "\n\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    checks = [
        ("status", ["git", "status", "--short"]),
        ("diff_stat", ["git", "diff", "--stat"]),
        ("staged_stat", ["git", "diff", "--cached", "--stat"]),
        ("untracked", ["git", "ls-files", "--others", "--exclude-standard"]),
        ("diff_check", ["git", "diff", "--check"]),
        ("staged_check", ["git", "diff", "--cached", "--check"]),
    ]

    results = []
    failures = 0
    for name, cmd in checks:
        code, output = run(cmd, root)
        results.append({
            "name": name,
            "cmd": cmd,
            "exit_code": code,
            "output": output,
        })
        if name.endswith("_check") and code != 0:
            failures += 1

    ud_code, ud_output = untracked_diff(root)
    results.append({
        "name": "untracked_diff",
        "cmd": ["git", "diff", "--no-index", "--", "/dev/null", "<untracked>"],
        "exit_code": ud_code,
        "output": ud_output,
    })

    payload = {"root": str(root), "checks": results}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"## {item['name']} (exit {item['exit_code']})")
            print(item["output"] or "(empty)")
            print()
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
