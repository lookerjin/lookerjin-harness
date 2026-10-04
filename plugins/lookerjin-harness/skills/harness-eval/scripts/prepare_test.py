#!/usr/bin/env python3
"""Exercise preparation through its CLI, including isolation and refusal paths."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("prepare.py")


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "app"
        self.project.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.project / "app.py").write_text("print('ready')\n", encoding="utf-8")
        self.commit()
        (self.project / "untracked.txt").write_text("not in snapshot", encoding="utf-8")
        self.old = self.root / "old"
        self.new = self.root / "new"
        for root, content in ((self.old, "old"), (self.new, "new")):
            folder = root / "work"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                "---\nname: work\ndescription: Work\n---\n" + content + "\n", encoding="utf-8",
            )
        self.output = self.root / "run"

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.project), *args], check=True, capture_output=True,
        ).stdout

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def run_script(self, *extra, success=True):
        proc = subprocess.run([
            sys.executable, str(SCRIPT), "--project", str(self.project),
            "--baseline-skills", str(self.old), "--candidate-skills", str(self.new),
            "--output", str(self.output), *extra,
        ], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0 if success else 1, proc.stderr + proc.stdout)
        return json.loads(proc.stdout)

    def test_same_snapshot_separate_outputs_and_private_mapping(self):
        result = self.run_script()
        self.assertFalse(result["agents_run"])
        mapping = json.loads((self.output / "control/assignment.json").read_text())
        self.assertEqual({x["variant"] for x in mapping["assignments"].values()}, {"baseline", "candidate"})
        self.assertNotEqual(*[x["skills_sha256"] for x in mapping["assignments"].values()])
        left, right = map(Path, result["workspaces"])
        for workspace in (left, right):
            self.assertEqual((workspace / "app.py").read_text(), "print('ready')\n")
            self.assertFalse((workspace / "untracked.txt").exists())
            self.assertFalse((workspace / "control").exists())
            head = subprocess.check_output(["git", "-C", str(workspace), "rev-parse", "HEAD"]).decode().strip()
            self.assertEqual(head, mapping["project_commit"])
            self.assertEqual(subprocess.check_output(["git", "-C", str(workspace), "remote"]), b"")
            self.assertEqual(subprocess.check_output(["git", "-C", str(workspace), "status", "--porcelain"]), b"")
            label = workspace.name
            expected = "old" if mapping["assignments"][label]["variant"] == "baseline" else "new"
            self.assertTrue((workspace / "skills/work/SKILL.md").read_text().endswith(expected + "\n"))
        (left / "app.py").write_text("changed", encoding="utf-8")
        diff = subprocess.check_output(["git", "-C", str(left), "diff"]).decode()
        self.assertIn("+changed", diff)
        self.assertEqual((right / "app.py").read_text(), "print('ready')\n")
        self.assertEqual((self.project / "app.py").read_text(), "print('ready')\n")
        self.output = self.root / "second"
        self.run_script()
        self.assertEqual(mapping, json.loads((self.output / "control/assignment.json").read_text()))

    def test_existing_output_survives(self):
        self.output.mkdir()
        sentinel = self.output / "keep"
        sentinel.write_text("untouched", encoding="utf-8")
        self.run_script(success=False)
        self.assertEqual(sentinel.read_text(), "untouched")

    def test_unsafe_and_overlapping_paths(self):
        for path in ("", ".", "../escape", "/absolute", "a\\b", ".git/skills", "a\nb"):
            with self.subTest(path=path):
                self.run_script("--skills-path", path, success=False)
                self.assertFalse(self.output.exists())
        self.output = self.project / "run"
        self.run_script(success=False)
        self.assertFalse(self.output.exists())
        self.assertFalse((self.root / "escape").exists())

    def test_project_collision_and_failure_cleanup(self):
        (self.project / "skills").mkdir()
        (self.project / "skills/keep").write_text("untouched", encoding="utf-8")
        self.commit()
        self.run_script(success=False)
        self.assertFalse(self.output.exists())
        self.assertEqual((self.project / "skills/keep").read_text(), "untouched")
        self.run_script("--skills-path", ".context/skills")
        self.assertTrue((self.output / "projects/cedar/.context/skills/work/SKILL.md").exists())

    def test_symlinks_are_refused_without_touching_targets(self):
        target = self.root / "outside"
        target.write_text("untouched", encoding="utf-8")
        (self.new / "work/link").symlink_to(target)
        self.run_script(success=False)
        self.assertFalse(self.output.exists())
        (self.new / "work/link").unlink()
        (self.project / "link").symlink_to(target)
        self.commit()
        self.run_script(success=False)
        self.assertFalse(self.output.exists())
        self.assertEqual(target.read_text(), "untouched")

    def test_invalid_ref_and_submodule_refused(self):
        self.run_script("--ref", "missing", success=False)
        self.assertFalse(self.output.exists())
        head = self.git("rev-parse", "HEAD").decode().strip()
        self.git("update-index", "--add", "--cacheinfo", f"160000,{head},nested")
        self.git("commit", "-qm", "submodule")
        self.run_script(success=False)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
