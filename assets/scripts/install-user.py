#!/usr/bin/env python3
"""Install the personal layer of lookerjin-harness without overwriting user files."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def copy_if_absent(src: Path, dst: Path, apply: bool) -> str:
    if dst.exists() or dst.is_symlink():
        return f"SKIP exists: {dst}"
    if not apply:
        return f"WOULD COPY: {src} -> {dst}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"COPIED: {dst}"


def install_skill(src: Path, dst: Path, apply: bool, mode: str) -> str:
    if dst.exists() or dst.is_symlink():
        return f"SKIP exists: {dst}"

    if mode == "auto":
        mode = "copy" if os.name == "nt" else "symlink"

    if not apply:
        return f"WOULD {mode.upper()}: {src} -> {dst}"

    dst.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        try:
            dst.symlink_to(src.resolve(), target_is_directory=True)
            return f"LINKED: {dst} -> {src.resolve()}"
        except OSError as exc:
            # Windows 或受限环境下回退 copy。
            shutil.copytree(src, dst)
            return f"COPIED (symlink failed: {exc}): {dst}"

    shutil.copytree(src, dst)
    return f"COPIED: {dst}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="actually install; default is dry-run")
    p.add_argument("--mode", choices=["auto", "copy", "symlink"], default="auto")
    args = p.parse_args()

    repo = Path(__file__).resolve().parents[2]
    home = Path.home()
    codex = home / ".codex"
    user_skills = home / ".agents" / "skills"

    print(copy_if_absent(repo / "global" / "AGENTS.md", codex / "AGENTS.md", args.apply))
    # config.toml 不自动合并/覆盖，只在不存在时复制。
    print(copy_if_absent(repo / "global" / "config.toml", codex / "config.toml", args.apply))
    print(copy_if_absent(repo / "global" / "hooks" / "hooks.json", codex / "hooks.json", args.apply))
    print(copy_if_absent(repo / "global" / "hooks" / "pre_tool_use_guard.py",
                         codex / "hooks" / "pre_tool_use_guard.py", args.apply))
    print(copy_if_absent(repo / "global" / "hooks" / "stop_review.py",
                         codex / "hooks" / "stop_review.py", args.apply))

    for skill in sorted((repo / "skills").iterdir()):
        if skill.is_dir() and (skill / "SKILL.md").exists():
            print(install_skill(skill, user_skills / skill.name, args.apply, args.mode))

    if not args.apply:
        print("\nDry-run only. Re-run with --apply after reviewing the plan.")
    else:
        print("\nInstalled without overwriting existing files. Restart Codex if new skills are not detected.")
        print("Review/trust hook definitions in Codex before relying on them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
