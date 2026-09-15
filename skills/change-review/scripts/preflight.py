#!/usr/bin/env python3
"""Collect deterministic git workspace facts for change-review."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    output = "\n".join(part for part in (stdout, stderr) if part)
    return proc.returncode, output


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
