#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None

FM = re.compile(r"\A---\s*\n(.*?)\n---", re.S)
NAME = re.compile(r"^name:\s*(.+?)\s*$", re.M)
DESC = re.compile(r"^description:\s*(.+?)\s*$", re.M)
MD_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
PLUGIN_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9]|[.-](?![.-]))*[a-z0-9]$|^[a-z0-9]$")
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
LEGACY_ROOTS = ("global", "profiles", "assets", "checks")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    errors = []
    warnings = []
    checks = []

    plugin_path = root / "plugin.json"
    if not plugin_path.exists():
        errors.append({"code": "MISSING_PLUGIN", "message": "plugin.json not found; doctor only checks this plugin repo"})
    else:
        try:
            plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
            schema = plugin.get("$schema")
            if schema != PLUGIN_SCHEMA:
                errors.append({"code": "PLUGIN_SCHEMA", "message": f"$schema must be {PLUGIN_SCHEMA}"})
            else:
                checks.append({"code": "PLUGIN_SCHEMA", "message": schema})
            name = plugin.get("name")
            if not isinstance(name, str) or not PLUGIN_NAME.match(name) or len(name) > 64:
                errors.append({"code": "PLUGIN_NAME", "message": "plugin.json name is missing or invalid"})
            else:
                checks.append({"code": "PLUGIN_NAME", "message": name})
            version = plugin.get("version")
            if version:
                checks.append({"code": "PLUGIN_VERSION", "message": str(version)})
        except Exception as exc:
            errors.append({"code": "INVALID_PLUGIN_JSON", "message": str(exc)})

    mcp_path = root / "mcp.json"
    if mcp_path.exists():
        try:
            mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
            servers = mcp.get("mcpServers")
            if not isinstance(servers, dict):
                errors.append({"code": "MCP_SERVERS", "message": "mcpServers must be an object"})
            else:
                for key, spec in servers.items():
                    if not isinstance(spec, dict):
                        errors.append({"code": "MCP_SERVER", "message": f"{key}: server spec must be an object"})
                        continue
                    if not spec.get("type"):
                        errors.append({"code": "MCP_TYPE", "message": f"{key}: type missing"})
                    if not spec.get("url") and not spec.get("command"):
                        errors.append({"code": "MCP_ENDPOINT", "message": f"{key}: url or command required"})
                checks.append({"code": "MCP", "message": f"{len(servers)} MCP server(s)"})
        except Exception as exc:
            errors.append({"code": "INVALID_MCP_JSON", "message": str(exc)})

    skills = root / "skills"
    seen = set()
    if not skills.is_dir():
        errors.append({"code": "MISSING_SKILLS", "message": "skills directory not found"})
    else:
        for skill in sorted(p for p in skills.iterdir() if p.is_dir()):
            skill_md = skill / "SKILL.md"
            if not skill_md.exists():
                errors.append({"code": "UNDISCOVERABLE_SKILL", "message": f"{skill.name}: SKILL.md missing"})
                continue
            text = skill_md.read_text(encoding="utf-8")
            fm = FM.search(text)
            if not fm:
                errors.append({"code": "FRONTMATTER", "message": f"{skill.name}: frontmatter missing"})
                continue
            name_m = NAME.search(fm.group(1))
            desc_m = DESC.search(fm.group(1))
            if not name_m or not desc_m:
                errors.append({"code": "SKILL_METADATA", "message": f"{skill.name}: name/description missing"})
                continue
            actual = name_m.group(1).strip().strip("'\"")
            if actual != skill.name:
                errors.append({"code": "SKILL_NAME", "message": f"{skill.name}: frontmatter name is {actual}"})
            if actual in seen:
                errors.append({"code": "DUPLICATE_SKILL", "message": actual})
            seen.add(actual)
            checks.append({"code": "SKILL", "message": actual})

    profile_dir = root / "skills" / "project-bootstrap" / "references" / "profiles"
    if profile_dir.exists():
        if tomllib is None:
            errors.append({
                "code": "PROFILE_PARSE_UNAVAILABLE",
                "message": "Python <3.11 and tomli missing; cannot parse TOML profiles. Use python3.11+.",
            })
        else:
            profile_ids = set()
            for path in sorted(profile_dir.glob("*.toml")):
                try:
                    data = tomllib.loads(path.read_text(encoding="utf-8"))
                except Exception as exc:
                    errors.append({"code": "PROFILE_TOML", "message": f"{path.name}: {exc}"})
                    continue
                pid = data.get("id")
                if not pid:
                    errors.append({"code": "PROFILE_ID", "message": f"{path.name}: id missing"})
                elif pid in profile_ids:
                    errors.append({"code": "DUPLICATE_PROFILE", "message": str(pid)})
                else:
                    profile_ids.add(pid)
                    checks.append({"code": "PROFILE", "message": str(pid)})

    ci_go = root / "skills" / "project-bootstrap" / "assets" / "github" / "ci-go.yml"
    if ci_go.exists():
        if "REPLACE_WITH_FULL_COMMIT_SHA" not in ci_go.read_text(encoding="utf-8"):
            errors.append({
                "code": "CI_PLACEHOLDER_MISSING",
                "message": "ci-go.yml must keep REPLACE_WITH_FULL_COMMIT_SHA so generated workflows cannot ship unpinned actions",
            })
        else:
            checks.append({"code": "CI_PLACEHOLDER", "message": "ci-go.yml keeps pin placeholders"})

    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in MD_LINK.findall(text):
            target = raw.split("#", 1)[0]
            if target and not (path.parent / target).resolve().exists():
                warnings.append({"code": "LOCAL_LINK", "message": f"{path.relative_to(root)} -> {raw}"})

    legacy = [name for name in LEGACY_ROOTS if (root / name).exists()]
    if legacy:
        errors.append({"code": "LEGACY_ROOT", "message": ", ".join(legacy)})
    else:
        checks.append({"code": "LAYOUT", "message": "no deprecated top-level directories"})

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
