#!/usr/bin/env python3
"""Cheap project preflight intended to be called by Skills or humans."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    failures = 0
    for label, cmd in [
        ("git status", ["git", "status", "--short"]),
        ("git diff --check", ["git", "diff", "--check"]),
    ]:
        code, out = run(cmd, root)
        print(f"## {label}")
        print(out or "(clean)")
        if code != 0:
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
