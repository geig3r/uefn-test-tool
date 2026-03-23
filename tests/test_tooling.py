from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from uefn_tooling.cli import main
from uefn_tooling.config import ToolConfig
from uefn_tooling.uefn import UEFNTool


class ToolingTests(unittest.TestCase):
    def test_project_summary_discovers_project_and_verse_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Example.uefnproject").write_text(json.dumps({"title": "Example"}), encoding="utf-8")
            (root / "Verse").mkdir()
            (root / "Verse" / "hello.verse").write_text("module hello", encoding="utf-8")

            tool = UEFNTool(ToolConfig.from_env(root))
            summary = tool.project_summary()

            self.assertEqual(summary["project_file"], str(root / "Example.uefnproject"))
            self.assertEqual(summary["verse_file_count"], 1)
            self.assertEqual(summary["verse_files"], ["Verse/hello.verse"])

    def test_build_editor_launch_command_requires_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = ToolConfig.from_env(root)
            config.editor_exe = Path("C:/UEFN/Editor.exe")
            tool = UEFNTool(config)

            with self.assertRaises(FileNotFoundError):
                tool.build_editor_launch_command()

    def test_cli_detect_runs(self) -> None:
        code = main(["--project-dir", ".", "detect"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
