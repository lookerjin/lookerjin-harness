#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

FM = re.compile(r"\A---\s*\n(.*?)\n---", re.S)
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
DESC = re.compile(r"^description:\s*(.+?)\s*$", re.M)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    errors = []
    warnings = []
    checks = []

    for filename in ("plugin.json", "mcp.json"):
        path = root / filename
        if not path.exists():
            if filename == "plugin.json":
                errors.append({"code": "MISSING_PLUGIN", "message": "plugin.json not found"})
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            checks.append({"code": "JSON", "message": f"{filename} parsed"})
            if filename == "mcp.json" and not isinstance(data.get("mcpServers"), dict):
                errors.append({"code": "MCP_SERVERS", "message": "mcpServers must be an object"})
        except Exception as exc:
            errors.append({"code": "INVALID_JSON", "message": f"{filename}: {exc}"})

    skills = root / "skills"
    if not skills.is_dir():
        errors.append({"code": "MISSING_SKILLS", "message": "skills directory not found"})
    else:
        seen = set()
        for skill in sorted(p for p in skills.iterdir() if p.is_dir()):
            path = skill / "SKILL.md"
            if not path.exists():
                warnings.append({"code": "UNDISCOVERABLE_SKILL", "message": f"{skill.name}: SKILL.md missing"})
                continue
            text = path.read_text(encoding="utf-8")
            fm = FM.search(text)
            if not fm:
                errors.append({"code": "FRONTMATTER", "message": f"{skill.name}: frontmatter missing"})
                continue
            name = NAME.search(fm.group(1))
            desc = DESC.search(fm.group(1))
            if not name or not desc:
                errors.append({"code": "SKILL_METADATA", "message": f"{skill.name}: name/description missing"})
                continue
            actual = name.group(1).strip().strip("\"'")
            if actual != skill.name:
                errors.append({"code": "SKILL_NAME", "message": f"{skill.name}: frontmatter name is {actual}"})
            if actual in seen:
                errors.append({"code": "DUPLICATE_SKILL", "message": actual})
            seen.add(actual)
            checks.append({"code": "SKILL", "message": actual})

    result = {
        "status": "fail" if errors else "pass",
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status={result['status']} errors={len(errors)} warnings={len(warnings)} checks={len(checks)}")

    raise SystemExit(1 if errors else 0)

if __name__ == "__main__":
    main()
