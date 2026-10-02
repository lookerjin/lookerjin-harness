#!/usr/bin/env python3
"""Prepare two local project snapshots with neutral labels; never run agents."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath

IGNORED = {".git", "__pycache__", ".pytest_cache"}


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def inside(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def skill_files(root: Path) -> list[Path]:
    if not root.is_dir() or not any(root.glob("*/SKILL.md")):
        raise ValueError(f"not a skills directory: {root}")
    files = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in IGNORED for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"symlink in skills source: {relative}")
        if path.is_file():
            files.append(path)
        elif not path.is_dir():
            raise ValueError(f"unsupported skills entry: {relative}")
    return files


def fingerprint(root: Path, files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(str(path.stat().st_mode & 0o777).encode() + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def clone_snapshot(project: Path, commit: str, destination: Path) -> None:
    proc = subprocess.run([
        "git", "clone", "--no-local", "--no-hardlinks", "--no-checkout",
        "--", str(project), str(destination),
    ], capture_output=True, check=False)
    if proc.returncode:
        raise ValueError(proc.stderr.decode("utf-8", errors="replace").strip())
    git(destination, "remote", "remove", "origin")
    git(destination, "checkout", "--detach", commit)


def prepare(args: argparse.Namespace) -> dict:
    project = Path(args.project).resolve()
    sources = {
        "baseline": Path(args.baseline_skills).resolve(),
        "candidate": Path(args.candidate_skills).resolve(),
    }
    output_arg = Path(args.output)
    if output_arg.is_symlink():
        raise ValueError("output must not be a symlink")
    output = output_arg.resolve()
    if output.exists():
        raise ValueError("output already exists; choose a new directory")
    if any(inside(output, root) or inside(root, output) for root in [project, *sources.values()]):
        raise ValueError("output must be separate from project and skill sources")
    relative = PurePosixPath(args.skills_path)
    if (relative.is_absolute() or not relative.parts or ".." in relative.parts
            or "\\" in args.skills_path or ".git" in relative.parts
            or any(ord(char) < 32 for char in args.skills_path)):
        raise ValueError("skills-path must be a safe, nonempty relative directory")
    actual_root = Path(git(project, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if actual_root != project:
        raise ValueError("project must be the Git repository root")
    commit = git(project, "rev-parse", "--verify", f"{args.ref}^{{commit}}").decode().strip()
    entries = git(project, "ls-tree", "-rz", commit)
    if any(entry.startswith((b"120000 ", b"160000 ")) for entry in entries.split(b"\0")):
        raise ValueError("symlinks and submodules require a separately prepared fixture")
    files = {key: skill_files(root) for key, root in sources.items()}
    hashes = {key: fingerprint(root, files[key]) for key, root in sources.items()}
    variants = ["baseline", "candidate"]
    random.Random(args.seed).shuffle(variants)
    output.mkdir(parents=True, exist_ok=False)
    try:
        mapping = {}
        for label, variant in zip(("cedar", "birch"), variants):
            workspace = output / "projects" / label
            workspace.parent.mkdir(parents=True, exist_ok=True)
            clone_snapshot(project, commit, workspace)
            skill_target = workspace.joinpath(*relative.parts)
            # Any file ancestor or existing subtree is a collision, not an overwrite.
            if skill_target.exists() or any(
                parent.is_file() for parent in skill_target.parents if inside(parent, workspace)
            ):
                raise ValueError("skills-path collides with project snapshot")
            for file in files[variant]:
                target = skill_target / file.relative_to(sources[variant])
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
            if fingerprint(skill_target, skill_files(skill_target)) != hashes[variant]:
                raise ValueError("skills source changed during preparation; retry from a fixed snapshot")
            # Injected instructions belong to the experiment, not the product diff.
            pattern = re.sub(r"([*?\[\] ])", r"\\\1", relative.as_posix())
            with (workspace / ".git/info/exclude").open("a", encoding="utf-8") as exclude:
                exclude.write(f"\n/{pattern}/\n")
            mapping[label] = {"variant": variant, "skills_sha256": hashes[variant]}
        control = output / "control"
        control.mkdir()
        (control / "assignment.json").write_text(json.dumps({
            "project_commit": commit,
            "snapshot_sha256": hashlib.sha256(entries).hexdigest(),
            "seed": args.seed,
            "skills_path": relative.as_posix(),
            "assignments": mapping,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        # Only the new tree created by this invocation may be removed.
        shutil.rmtree(output)
        raise
    return {
        "status": "prepared",
        "project_commit": commit,
        "workspaces": [str(output / "projects" / label) for label in ("cedar", "birch")],
        "skills_path": relative.as_posix(),
        "control": str(output / "control" / "assignment.json"),
        "agents_run": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--baseline-skills", required=True)
    parser.add_argument("--candidate-skills", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--skills-path", default="skills")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    try:
        result = prepare(args)
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
