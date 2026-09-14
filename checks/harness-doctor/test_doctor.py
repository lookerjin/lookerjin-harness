from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("doctor", HERE / "doctor.py")
doctor = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(doctor)


class DoctorTests(unittest.TestCase):
    def test_valid_skill(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "skills" / "x"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: x\ndescription: Use when testing x.\n---\nDo x.\n",
                encoding="utf-8",
            )
            report = doctor.Report()
            doctor.check_skills(root, report)
            self.assertEqual([], report.errors)

    def test_duplicate_skill_name(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for folder in ["a", "b"]:
                skill = root / "skills" / folder
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    "---\nname: same\ndescription: Use when testing.\n---\n",
                    encoding="utf-8",
                )
            report = doctor.Report()
            doctor.check_skills(root, report)
            self.assertTrue(any("duplicate skill name" in e for e in report.errors))


if __name__ == "__main__":
    unittest.main()
