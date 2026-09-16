#!/usr/bin/env python3
"""Fail if a generated project still contains bootstrap pin placeholders."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PLACEHOLDER = "REPLACE_WITH_FULL_COMMIT_SHA"
SKIP_PARTS = {".git", "node_modules", "vendor", "dist", ".venv"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    hits: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in {".yml", ".yaml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if PLACEHOLDER in text:
            hits.append(str(path.relative_to(root)))
    if hits:
        print("unpinned Action SHA placeholder remains in:", file=sys.stderr)
        for hit in hits:
            print(f"  {hit}", file=sys.stderr)
        return 1
    print("no REPLACE_WITH_FULL_COMMIT_SHA in generated workflows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
