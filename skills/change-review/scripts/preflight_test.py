#!/usr/bin/env python3
"""Self-test: untracked files appear in preflight untracked_diff."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
        (root / "tracked.txt").write_text("old\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=root, check=True, capture_output=True)
        (root / "fresh.go").write_text("package fresh\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(HERE / "preflight.py"), "--root", str(root), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(proc.stdout)
        by_name = {item["name"]: item for item in payload["checks"]}
        if "fresh.go" not in by_name["untracked"]["output"]:
            raise SystemExit("untracked list missing fresh.go")
        if "package fresh" not in by_name["untracked_diff"]["output"]:
            raise SystemExit("untracked_diff missing file contents")
        if by_name["diff_stat"]["output"]:
            raise SystemExit("expected empty diff_stat for untracked-only change")
    print("preflight_test ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
