#!/usr/bin/env python3
"""Deterministic health checks for lookerjin-harness or an adopted project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
DESC = re.compile(r"^description:\s*(.+?)\s*$", re.M)
MD_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ok: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def pass_(self, msg: str) -> None:
        self.ok.append(msg)


def check_skills(root: Path, report: Report) -> None:
    candidates = []
    for base in [root / "skills", root / ".agents" / "skills"]:
        if base.exists():
            candidates.extend(p for p in base.iterdir() if p.is_dir() and (p / "SKILL.md").exists())

    names: dict[str, Path] = {}
    for skill in sorted(candidates):
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        fm = FRONTMATTER.search(text)
        if not fm:
            report.error(f"{skill}: SKILL.md missing YAML frontmatter")
            continue
        name_m = NAME.search(fm.group(1))
        desc_m = DESC.search(fm.group(1))
        if not name_m or not desc_m:
            report.error(f"{skill}: frontmatter requires name and description")
            continue
        name = name_m.group(1).strip().strip('"\'')
        desc = desc_m.group(1).strip()
        if name in names:
            report.error(f"duplicate skill name {name!r}: {names[name]} and {skill}")
        else:
            names[name] = skill
        if "Use" not in desc and "use" not in desc:
            report.warn(f"{skill}: description may not state trigger conditions clearly")
        report.pass_(f"skill: {name}")


def check_hooks(root: Path, report: Report) -> None:
    hook_files = [root / "global" / "hooks" / "hooks.json", root / ".codex" / "hooks.json"]
    for hook_file in hook_files:
        if not hook_file.exists():
            continue
        try:
            data = json.loads(hook_file.read_text(encoding="utf-8"))
        except Exception as exc:
            report.error(f"{hook_file}: invalid JSON: {exc}")
            continue
        if not isinstance(data.get("hooks"), dict):
            report.error(f"{hook_file}: missing top-level hooks object")
            continue
        report.pass_(f"hooks json: {hook_file.relative_to(root)}")


def check_profiles(root: Path, report: Report) -> None:
    profiles = root / "profiles"
    if not profiles.exists():
        return
    if tomllib is None:
        report.warn("Python <3.11: skip TOML profile parsing")
        return
    seen: set[str] = set()
    for path in sorted(profiles.glob("*/profile.toml")):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            report.error(f"{path}: invalid TOML: {exc}")
            continue
        pid = data.get("id")
        if not pid:
            report.error(f"{path}: missing id")
        elif pid in seen:
            report.error(f"{path}: duplicate profile id {pid}")
        else:
            seen.add(pid)
            report.pass_(f"profile: {pid}")


def check_markdown_links(root: Path, report: Report) -> None:
    for path in root.rglob("*.md"):
        if any(part in {".git", "node_modules", "vendor"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for raw in MD_LINK.findall(text):
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                report.warn(f"{path.relative_to(root)}: local link target missing: {raw}")


def check_placeholders(root: Path, report: Report) -> None:
    # 只把高概率遗留占位符当 warning。模板目录允许显式占位。
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".toml", ".json", ".py", ".yml", ".yaml"}:
            continue
        if "assets" in path.parts or path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "<fill-me>" in text or "REPLACE_ME" in text:
            report.warn(f"{path.relative_to(root)}: unresolved placeholder")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"root not found: {root}", file=sys.stderr)
        return 2

    report = Report()
    check_skills(root, report)
    check_hooks(root, report)
    check_profiles(root, report)
    check_markdown_links(root, report)
    check_placeholders(root, report)

    print("Harness Doctor")
    print(f"root: {root}")
    print()

    for msg in report.errors:
        print(f"ERROR: {msg}")
    for msg in report.warnings:
        print(f"WARN:  {msg}")
    for msg in report.ok:
        print(f"OK:    {msg}")

    print()
    print(f"errors={len(report.errors)} warnings={len(report.warnings)} checks={len(report.ok)}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
