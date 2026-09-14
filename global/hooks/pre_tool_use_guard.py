#!/usr/bin/env python3
"""Block a deliberately small set of high-risk shell commands.

This hook is a guardrail, not a complete security boundary.
It reads Codex PreToolUse JSON from stdin and only acts on Bash commands.
"""

from __future__ import annotations

import json
import re
import sys


BLOCK_RULES = [
    (re.compile(r"(^|\s)git\s+push\b[^\n;&|]*(--force-with-lease|--force|-f)(\s|$)"),
     "禁止强制推送远端历史。"),
    (re.compile(r"(^|\s)git\s+reset\s+--hard\b"),
     "禁止自动执行 git reset --hard；请使用可恢复方式或由用户明确处理。"),
    (re.compile(r"(^|\s)git\s+clean\b[^\n;&|]*-(?:[a-zA-Z]*f[a-zA-Z]*d[a-zA-Z]*x|[a-zA-Z]*x[a-zA-Z]*f[a-zA-Z]*d)\b"),
     "禁止自动执行包含 -f/-d/-x 的 git clean。"),
    (re.compile(r"(^|\s)rm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\s+(/|~|\$HOME)(\s|$)"),
     "禁止递归强制删除根目录或用户主目录。"),
    (re.compile(r"(^|\s)(mkfs(\.\w+)?|wipefs)\b"),
     "禁止自动执行文件系统格式化/签名擦除命令。"),
    (re.compile(r"(^|\s)dd\b[^\n;&|]*\bof=/dev/"),
     "禁止自动向块设备执行 dd。"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # Hook 自身解析失败时不阻塞正常工作，但也不输出不受支持字段。
        return 0

    if payload.get("tool_name") != "Bash":
        return 0

    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command")
    if not isinstance(command, str):
        return 0

    for pattern, reason in BLOCK_RULES:
        if pattern.search(command):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }, ensure_ascii=False))
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
