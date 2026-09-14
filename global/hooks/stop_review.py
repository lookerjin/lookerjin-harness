#!/usr/bin/env python3
"""Run a tiny, deterministic stop-time review.

The hook intentionally avoids full test suites. It checks only cheap Git hygiene.
If the check fails on the first stop attempt, Codex is asked to continue once.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        timeout=8,
        check=False,
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print("{}")
        return 0

    cwd = Path(payload.get("cwd") or ".").resolve()
    if not (cwd / ".git").exists():
        # 允许从子目录启动：尝试找到 repo root。
        p = run(["git", "rev-parse", "--show-toplevel"], cwd)
        if p.returncode != 0:
            print("{}")
            return 0
        cwd = Path(p.stdout.strip())

    diff = run(["git", "diff", "--check"], cwd)
    if diff.returncode == 0:
        print("{}")
        return 0

    # 避免 Stop hook 自己造成无限循环。
    if payload.get("stop_hook_active"):
        print(json.dumps({
            "systemMessage": "轻量收口检查仍失败：git diff --check 未通过，请在最终回复中明确报告。"
        }, ensure_ascii=False))
        return 0

    detail = (diff.stdout + "\n" + diff.stderr).strip()
    detail = detail[:1800]
    print(json.dumps({
        "decision": "block",
        "reason": "轻量收口检查失败。请修复 `git diff --check` 报告的问题后再结束；"
                  "如果属于用户已有修改且不应触碰，请明确说明并保留。\n\n" + detail
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
