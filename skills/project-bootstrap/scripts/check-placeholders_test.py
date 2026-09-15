#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    script = HERE / "check-placeholders.py"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".github" / "workflows").mkdir(parents=True)
        good = root / ".github" / "workflows" / "ci.yml"
        good.write_text("uses: actions/checkout@abc123\n", encoding="utf-8")
        ok = subprocess.run([sys.executable, str(script), "--root", str(root)])
        if ok.returncode != 0:
            raise SystemExit("expected clean tree to pass")
        bad = root / ".github" / "workflows" / "ci.yml"
        bad.write_text("uses: actions/checkout@REPLACE_WITH_FULL_COMMIT_SHA\n", encoding="utf-8")
        fail = subprocess.run([sys.executable, str(script), "--root", str(root)], capture_output=True)
        if fail.returncode == 0:
            raise SystemExit("expected placeholder to fail")
    print("check-placeholders_test ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
