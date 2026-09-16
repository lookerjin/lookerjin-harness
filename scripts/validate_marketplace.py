#!/usr/bin/env python3

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
MANIFEST_PATHS = (
    "plugin.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
)


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_marketplace() -> dict:
    try:
        data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing marketplace: {MARKETPLACE}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON: {exc}") from exc

    require(isinstance(data, dict), "marketplace root must be an object")
    require(isinstance(data.get("name"), str) and data["name"].strip(), "marketplace.name is required")
    require(isinstance(data.get("plugins"), list), "marketplace.plugins must be an array")
    return data


def find_manifest(plugin_root: Path) -> Path | None:
    for relative in MANIFEST_PATHS:
        candidate = plugin_root / relative
        if candidate.is_file():
            return candidate
    return None


def validate_local_source(name: str, source: dict) -> None:
    raw_path = source.get("path")
    require(isinstance(raw_path, str) and raw_path.strip(), f"{name}: local source.path is required")

    plugin_root = (ROOT / raw_path).resolve()
    try:
        plugin_root.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValidationError(f"{name}: local source escapes repository: {raw_path}") from exc

    require(plugin_root.is_dir(), f"{name}: local plugin directory does not exist: {raw_path}")
    require(find_manifest(plugin_root) is not None, f"{name}: no supported plugin manifest found under {raw_path}")


def validate_git_source(name: str, source: dict) -> None:
    url = source.get("url")
    require(isinstance(url, str) and url.strip(), f"{name}: git source.url is required")

    if source.get("source") == "git-subdir":
        path = source.get("path")
        require(isinstance(path, str) and path.strip(), f"{name}: git-subdir source.path is required")
        require(not Path(path).is_absolute() and ".." not in Path(path).parts, f"{name}: unsafe git-subdir path: {path}")

    ref = source.get("ref")
    sha = source.get("sha")
    require(
        (isinstance(ref, str) and ref.strip()) or (isinstance(sha, str) and sha.strip()),
        f"{name}: remote git plugin must pin at least ref or sha",
    )


def validate_npm_source(name: str, source: dict) -> None:
    package = source.get("package")
    require(isinstance(package, str) and package.strip(), f"{name}: npm source.package is required")
    version = source.get("version")
    require(isinstance(version, str) and version.strip(), f"{name}: npm source.version must be pinned")

    registry = source.get("registry")
    if registry is not None:
        require(isinstance(registry, str) and registry.startswith("https://"), f"{name}: npm registry must use https")
        parsed = urlparse(registry)
        require(parsed.username is None and parsed.password is None, f"{name}: npm registry must not contain credentials")


def validate_structure(data: dict) -> list[dict]:
    plugins = data["plugins"]
    seen: set[str] = set()

    for index, plugin in enumerate(plugins):
        require(isinstance(plugin, dict), f"plugins[{index}] must be an object")
        name = plugin.get("name")
        require(isinstance(name, str) and name.strip(), f"plugins[{index}].name is required")
        require(name not in seen, f"duplicate plugin name: {name}")
        seen.add(name)

        source = plugin.get("source")
        require(isinstance(source, dict), f"{name}: source must be an object")
        source_type = source.get("source")

        if source_type == "local":
            validate_local_source(name, source)
        elif source_type in {"git-subdir", "url"}:
            validate_git_source(name, source)
        elif source_type == "npm":
            validate_npm_source(name, source)
        else:
            raise ValidationError(f"{name}: unsupported source type: {source_type!r}")

        policy = plugin.get("policy", {})
        require(isinstance(policy, dict), f"{name}: policy must be an object")
        installation = policy.get("installation", "AVAILABLE")
        authentication = policy.get("authentication", "ON_INSTALL")
        require(installation in {"AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"}, f"{name}: invalid installation policy")
        require(authentication in {"ON_INSTALL", "ON_USE"}, f"{name}: invalid authentication policy")

    return plugins


def normalize_git_url(url: str) -> str:
    if "://" not in url and url.count("/") == 1:
        return f"https://github.com/{url}.git"
    return url


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        command = " ".join(args)
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValidationError(f"command failed: {command}\n{detail}")
    return result.stdout.strip()


def remote_manifest_exists(repo: Path, commit: str, plugin_path: str) -> bool:
    prefix = plugin_path.strip("/")
    for manifest in MANIFEST_PATHS:
        candidate = f"{prefix}/{manifest}" if prefix else manifest
        result = subprocess.run(
            ("git", "cat-file", "-e", f"{commit}:{candidate}"),
            cwd=repo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return True
    return False


def validate_remote_git(name: str, source: dict) -> None:
    url = normalize_git_url(source["url"])
    ref = source.get("ref")
    sha = source.get("sha")
    selector = ref or sha

    with tempfile.TemporaryDirectory(prefix="marketplace-") as temp:
        repo = Path(temp)
        run("git", "init", "-q", cwd=repo)
        run("git", "remote", "add", "origin", url, cwd=repo)
        run("git", "fetch", "--depth=1", "origin", selector, cwd=repo)
        commit = run("git", "rev-parse", "FETCH_HEAD", cwd=repo)

        if sha:
            require(commit.startswith(sha), f"{name}: resolved commit {commit} does not match pinned sha {sha}")

        plugin_path = source.get("path", "")
        require(
            remote_manifest_exists(repo, commit, plugin_path),
            f"{name}: no supported plugin manifest found at remote path {plugin_path or '.'}",
        )


def validate_remote_sources(plugins: list[dict]) -> int:
    checked = 0
    for plugin in plugins:
        source = plugin["source"]
        if source.get("source") in {"git-subdir", "url"}:
            validate_remote_git(plugin["name"], source)
            checked += 1
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Agent Marketplace manifest and integration contracts.")
    parser.add_argument("--remote", action="store_true", help="also resolve remote git plugin refs and manifests")
    args = parser.parse_args()

    try:
        data = load_marketplace()
        plugins = validate_structure(data)
        print(f"marketplace ok: {data['name']} ({len(plugins)} plugins)")

        if args.remote:
            checked = validate_remote_sources(plugins)
            print(f"remote contracts ok: {checked} git plugins checked")
    except ValidationError as exc:
        print(f"marketplace validation failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
