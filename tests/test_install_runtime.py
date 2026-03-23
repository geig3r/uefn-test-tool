from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.install_runtime import install_runtime, main


class InstallRuntimeTests(unittest.TestCase):
    def test_install_runtime_copies_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            python_dir = install_runtime(project_root)

            self.assertEqual(python_dir, project_root / 'Content' / 'Python')
            self.assertTrue((python_dir / 'init_unreal.py').exists())
            self.assertTrue((python_dir / 'uefn_test_tool' / '__init__.py').exists())
            self.assertTrue((python_dir / 'uefn_test_tool' / 'menu.py').exists())

    def test_cli_main_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = main(['--project-dir', tmp])
            self.assertEqual(code, 0)


if __name__ == '__main__':
    unittest.main()
